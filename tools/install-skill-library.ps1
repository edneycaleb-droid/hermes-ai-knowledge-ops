[CmdletBinding()]
param(
    [ValidateSet("Project", "Global")]
    [string]$Scope = "Global",

    [string[]]$Agent = @("codex", "claude-code", "hermes-agent"),

    [string[]]$Skill = @("*"),

    [switch]$AllowReview,

    [switch]$NoCopy
)

$ErrorActionPreference = "Stop"

$SkillsCli = "skills@1.5.20"
$ReviewedUpstreamCommit = "e173b8c88f2581cfdaa1b6767c6519a08155790e"
$MinimumNodeVersion = [version]"22.20.0"

function Require-Command {
    param([Parameter(Mandatory = $true)][string]$Name)

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

Require-Command "node"
Require-Command "npx"

$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) {
    $Python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $Python) {
    throw "Python 3 is required to validate the registry and enforce lifecycle eligibility."
}

$NodeVersionText = (& node --version).Trim().TrimStart("v")
try {
    $NodeVersion = [version]$NodeVersionText
}
catch {
    throw "Unable to parse Node.js version '$NodeVersionText'."
}

if ($NodeVersion -lt $MinimumNodeVersion) {
    throw "Node.js $MinimumNodeVersion or newer is required; found $NodeVersion."
}

& $Python.Source scripts/validate_skill_library.py
if ($LASTEXITCODE -ne 0) {
    throw "The canonical skill library failed validation."
}

$SelectorArguments = @("scripts/select_installable_skills.py", "--state", "approved")
if ($AllowReview) {
    $SelectorArguments += @("--state", "review")
}
foreach ($Name in $Skill) {
    $SelectorArguments += @("--skill", $Name)
}

$SelectedSkills = @(& $Python.Source @SelectorArguments)
if ($LASTEXITCODE -ne 0) {
    throw "One or more requested skills are unknown or not eligible for installation."
}
if ($SelectedSkills.Count -eq 0) {
    Write-Host "No skills are eligible for installation in the requested lifecycle states."
    return
}

$Arguments = @("--yes", $SkillsCli, "add", ".", "--yes")
if ($Scope -eq "Global") {
    $Arguments += "--global"
}
foreach ($Name in $Agent) {
    $Arguments += @("--agent", $Name)
}
foreach ($Name in $SelectedSkills) {
    $Arguments += @("--skill", $Name)
}
if (-not $NoCopy) {
    $Arguments += "--copy"
}

Write-Host "Installing governed skills with $SkillsCli"
Write-Host "Reviewed upstream commit: $ReviewedUpstreamCommit"
Write-Host "Eligible skills: $($SelectedSkills -join ', ')"
& npx @Arguments
if ($LASTEXITCODE -ne 0) {
    throw "Skill installation failed with exit code $LASTEXITCODE."
}

$ListArguments = @("--yes", $SkillsCli, "list")
if ($Scope -eq "Global") {
    $ListArguments += "--global"
}
foreach ($Name in $Agent) {
    $ListArguments += @("--agent", $Name)
}

& npx @ListArguments
if ($LASTEXITCODE -ne 0) {
    throw "Skill installation completed, but the installed-skill listing failed."
}

Write-Host "Skill installation completed. Restart each target agent so it reloads the installed skills."
