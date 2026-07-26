#!/usr/bin/env bash
set -euo pipefail

SKILLS_CLI="skills@1.5.20"
REVIEWED_UPSTREAM_COMMIT="e173b8c88f2581cfdaa1b6767c6519a08155790e"
SCOPE="global"
COPY_MODE=1
AGENTS=("codex" "claude-code" "hermes-agent")
SKILLS=("*")

usage() {
  cat <<'EOF'
Usage: tools/install-skill-library.sh [options]

Options:
  --global                 Install into each agent's global skill directory (default).
  --project                Install into project-local agent directories.
  --agent NAME             Replace defaults on first use; may be repeated.
  --skill NAME             Replace defaults on first use; may be repeated.
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
      if [[ $custom_skills -eq 0 ]]; then SKILLS=(); custom_skills=1; fi
      SKILLS+=("$1")
      ;;
    --no-copy) COPY_MODE=0 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

command -v node >/dev/null 2>&1 || { echo "node is required" >&2; exit 1; }
command -v npx >/dev/null 2>&1 || { echo "npx is required" >&2; exit 1; }

node -e '
const current = process.versions.node.split(".").map(Number);
const minimum = [22, 20, 0];
for (let i = 0; i < minimum.length; i++) {
  if (current[i] > minimum[i]) process.exit(0);
  if (current[i] < minimum[i]) process.exit(1);
}
' || { echo "Node.js 22.20.0 or newer is required; found $(node --version)" >&2; exit 1; }

if [[ -f scripts/validate_skill_library.py ]]; then
  if command -v python3 >/dev/null 2>&1; then
    python3 scripts/validate_skill_library.py
  elif command -v python >/dev/null 2>&1; then
    python scripts/validate_skill_library.py
  fi
fi

args=(--yes "$SKILLS_CLI" add . --yes)
[[ "$SCOPE" == "global" ]] && args+=(--global)
for agent in "${AGENTS[@]}"; do args+=(--agent "$agent"); done
for skill in "${SKILLS[@]}"; do args+=(--skill "$skill"); done
[[ $COPY_MODE -eq 1 ]] && args+=(--copy)

echo "Installing governed skills with $SKILLS_CLI"
echo "Reviewed upstream commit: $REVIEWED_UPSTREAM_COMMIT"
npx "${args[@]}"

list_args=(--yes "$SKILLS_CLI" list)
[[ "$SCOPE" == "global" ]] && list_args+=(--global)
for agent in "${AGENTS[@]}"; do list_args+=(--agent "$agent"); done
npx "${list_args[@]}"

echo "Skill installation completed. Restart each target agent so it reloads the installed skills."
