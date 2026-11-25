#!/usr/bin/env bash
# Install this repository's skill on the local workstation.
set -euo pipefail

usage() {
    cat <<'HELP'
Usage: bash scripts/install.sh [--client auto|codex|claude|dsh|both|all] [--project PATH] [--update]
Installs the skill only. Install and authenticate the AI CLI separately.
Default: detect codex, claude and dsh executables on PATH and install for each found CLI.
Default scope is personal (~/.agents/skills, ~/.claude/skills, ~/.dsh/skills).
For customized DSH homes, use the documented skill location and install manually.
--project PATH installs into an existing local project directory.
--update backs up existing skills before replacing them.
HELP
}
client=auto
project=
update=false
while (($#)); do
    case "$1" in
        --client|--project)
            (($# >= 2)) || { usage >&2; exit 2; }
            if [[ $1 == --client ]]; then client=$2; else project=$2; fi
            shift 2 ;;
        --update) update=true; shift ;;
        -h|--help) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
    esac
done
case "$client" in auto|codex|claude|dsh|both|all) ;; *) usage >&2; exit 2 ;; esac
case "$(hostname -s)" in
    hpc-login*|hpc-exec*|hpc-head*)
        echo "Run this installer on your local workstation, outside Cetus." >&2
        exit 1 ;;
esac
if [[ -n ${PBS_JOBID:-} ]]; then
    echo "Run this installer outside PBS allocations." >&2
    exit 1
fi
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
source_dir="$root/skills/cetus-pbs"
[[ -f "$source_dir/SKILL.md" ]] || { echo "Missing skill source." >&2; exit 1; }
base=$HOME
if [[ -n $project ]]; then
    [[ -d $project ]] || { echo "Project directory does not exist: $project" >&2; exit 1; }
    base=$(cd -- "$project" && pwd)
fi
clients=()
if [[ $client == auto ]]; then
    for executable in codex claude dsh; do
        if command -v "$executable" >/dev/null 2>&1; then
            clients+=("$executable")
        fi
    done
    if (( ${#clients[@]} == 0 )); then
        echo "No supported CLI found on PATH. Install a CLI or specify --client codex|claude|dsh." >&2
        exit 1
    fi
    printf 'Detected CLI: %s\n' "${clients[@]}"
elif [[ $client == both ]]; then
    clients=(codex claude)
elif [[ $client == all ]]; then
    clients=(codex claude dsh)
else
    clients=("$client")
fi
destinations=()
for selected in "${clients[@]}"; do
    case "$selected" in
        codex) destinations+=("$base/.agents/skills/cetus-pbs") ;;
        claude) destinations+=("$base/.claude/skills/cetus-pbs") ;;
        dsh) destinations+=("$base/.dsh/skills/cetus-pbs") ;;
    esac
done

# Check every destination before making changes.
for destination in "${destinations[@]}"; do
    if [[ -e $destination || -L $destination ]]; then
        if [[ $update == false ]]; then
            echo "Already exists: $destination. Use --update to back it up and replace it." >&2
            exit 1
        fi
        if [[ $(cd -- "$destination" && pwd -P) == $(cd -- "$source_dir" && pwd -P) ]]; then
            echo "Destination is the source skill: $destination" >&2
            exit 1
        fi
    fi
done

for destination in "${destinations[@]}"; do
    parent=$(dirname -- "$destination")
    mkdir -p -- "$parent"
    staging=$(mktemp -d "$parent/.cetus-install-XXXXXXXX")
    trap 'rm -rf -- "$staging"' EXIT
    cp -R -- "$source_dir/." "$staging/"
    if [[ -e $destination || -L $destination ]]; then
        backup=$(mktemp -d "$parent/.cetus-backup-XXXXXXXX")
        # Keep backups outside the skill scanner's direct children.
        mv -- "$destination" "$backup/cetus-pbs"
        echo "Backup: $backup/cetus-pbs"
    fi
    mv -- "$staging" "$destination"
    trap - EXIT
    echo "Installed: $destination"
done
echo 'Start a new CLI session. Codex: $cetus-pbs. Claude Code: /cetus-pbs. DeepSeek Harness: ask it to load cetus-pbs.'
