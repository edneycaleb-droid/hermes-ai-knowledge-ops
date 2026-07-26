[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$InstallRoot = (Join-Path $HOME ".local\share\frenemy"),
    [string]$PinnedCommit = "dd460e61c2ff932d019266c8701290274ed2b495",
    [switch]$ForceRefresh
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Assert-Command {
    param([Parameter(Mandatory)][string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

Assert-Command git
Assert-Command node
Assert-Command claude
Assert-Command codex

$repoUrl = "https://github.com/noblehacks/frenemy.git"
$parent = Split-Path -Parent $InstallRoot
New-Item -ItemType Directory -Force -Path $parent | Out-Null

if (Test-Path $InstallRoot) {
    if (-not $ForceRefresh) {
        throw "Install path already exists: $InstallRoot. Re-run with -ForceRefresh to replace it."
    }
    if ($PSCmdlet.ShouldProcess($InstallRoot, "Remove existing pinned Frenemy checkout")) {
        Remove-Item -Recurse -Force $InstallRoot
    }
}

if ($PSCmdlet.ShouldProcess($InstallRoot, "Clone Frenemy and pin commit $PinnedCommit")) {
    git clone --filter=blob:none --no-checkout $repoUrl $InstallRoot
    git -C $InstallRoot checkout --detach $PinnedCommit
}

$actualCommit = (git -C $InstallRoot rev-parse HEAD).Trim()
if ($actualCommit -ne $PinnedCommit) {
    throw "Pinned commit verification failed. Expected $PinnedCommit, got $actualCommit."
}

$requiredFiles = @("ask-claude-mcp.mjs", "install.ps1", "CLAUDE-codex-section.md", "LICENSE")
foreach ($file in $requiredFiles) {
    if (-not (Test-Path (Join-Path $InstallRoot $file))) {
        throw "Required upstream file missing: $file"
    }
}

Push-Location $InstallRoot
try {
    if ($PSCmdlet.ShouldProcess($InstallRoot, "Run upstream Frenemy installer")) {
        & .\install.ps1
    }
}
finally {
    Pop-Location
}

Write-Host "Frenemy installed from verified commit $actualCommit"
Write-Host "Restart Codex, then test: Ask Claude to review any file in this repository."
Write-Host "Write-capable ask_claude_write remains approval-gated by upstream design."
