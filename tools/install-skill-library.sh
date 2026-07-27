#!/usr/bin/env bash
set -euo pipefail

SKILLS_CLI="skills@1.5.20"
REVIEWED_UPSTREAM_COMMIT="e173b8c88f2581cfdaa1b6767c6519a08155790e"
SCOPE="global"
COPY_MODE=1
ALLOW_REVIEW=0
AGENTS=("codex" "claude-code" "hermes-agent")
REQUESTED_SKILLS=("*")

usage() {
  cat <<'EOF'
Usage: tools/install-skill-library.sh [options]

Options:
  --global                 Install into each agent's global skill directory (default).
  --project                Install into project-local agent directories.
  --agent NAME             Replace defaults on first use; may be repeated.
  --skill NAME             Replace defaults on first use; may be repeated.
  --allow-review           Permit review-state skills for isolated testing only.
  --no-copy                Use the installer's symlink mode instead of copying.
  -h, --help               Show this help.
EOF
}

custom_agents=0
custom_skills=0
while (($#)); do
  case "$1" in
    --global) SCOPE="global" ;;
    --project) SCOPE="project" ;;
    --agent)
      shift
      [[ $# -gt 0 ]] || { echo "--agent requires a value" >&2; exit 2; }
      if [[ $custom_agents -eq 0 ]]; then AGENTS=(); custom_agents=1; fi
      AGENTS+=("$1")
      ;;
    --skill)
      shift
      [[ $# -gt 0 ]] || { echo "--skill requires a value" >&2; exit 2; }
      if [[ $custom_skills -eq 0 ]]; then REQUESTED_SKILLS=(); custom_skills=1; fi
      REQUESTED_SKILLS+=("$1")
      ;;
    --allow-review) ALLOW_REVIEW=1 ;;
    --no-copy) COPY_MODE=0 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

command -v node >/dev/null 2>&1 || { echo "node is required" >&2; exit 1; }
command -v npx >/dev/null 2>&1 || { echo "npx is required" >&2; exit 1; }
if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "Python 3 is required to validate the registry and enforce lifecycle eligibility." >&2
  exit 1
fi

node -e '
const current = process.versions.node.split(".").map(Number);
const minimum = [22, 20, 0];
for (let i = 0; i < minimum.length; i++) {
  if (current[i] > minimum[i]) process.exit(0);
  if (current[i] < minimum[i]) process.exit(1);
}
' || { echo "Node.js 22.20.0 or newer is required; found $(node --version)" >&2; exit 1; }

"$PYTHON" scripts/validate_skill_library.py

selector=(scripts/select_installable_skills.py --state approved)
[[ $ALLOW_REVIEW -eq 1 ]] && selector+=(--state review)
for skill in "${REQUESTED_SKILLS[@]}"; do selector+=(--skill "$skill"); done

if ! selected_output=$("$PYTHON" "${selector[@]}"); then
  echo "One or more requested skills are unknown or not eligible for installation." >&2
  exit 1
fi
if [[ -z "$selected_output" ]]; then
  echo "No skills are eligible for installation in the requested lifecycle states."
  exit 0
fi
mapfile -t SELECTED_SKILLS <<< "$selected_output"

args=(--yes "$SKILLS_CLI" add . --yes)
[[ "$SCOPE" == "global" ]] && args+=(--global)
for agent in "${AGENTS[@]}"; do args+=(--agent "$agent"); done
for skill in "${SELECTED_SKILLS[@]}"; do args+=(--skill "$skill"); done
[[ $COPY_MODE -eq 1 ]] && args+=(--copy)

echo "Installing governed skills with $SKILLS_CLI"
echo "Reviewed upstream commit: $REVIEWED_UPSTREAM_COMMIT"
echo "Eligible skills: ${SELECTED_SKILLS[*]}"
npx "${args[@]}"

list_args=(--yes "$SKILLS_CLI" list)
[[ "$SCOPE" == "global" ]] && list_args+=(--global)
for agent in "${AGENTS[@]}"; do list_args+=(--agent "$agent"); done
npx "${list_args[@]}"

echo "Skill installation completed. Restart each target agent so it reloads the installed skills."
