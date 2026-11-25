#!/usr/bin/env bash
# Install the skill from a checkout or from a downloaded copy of this script.
set -euo pipefail

usage() {
    cat <<'HELP'
Usage: bash scripts/install.sh [--client auto|codex|claude|dsh|both|all] [--project PATH]

Default: detect the active Codex/Claude session, or installed clients on PATH.
Identical copies are left alone. Changed copies are backed up and replaced.
--client NAME   Select a client explicitly, including desktop and npx sessions.
--project PATH  Install into an existing local project instead of your home.
--update        Accepted for compatibility; safe updates are already automatic.
--help          Show this help.

Run on your local workstation. This installs the cetus-pbs skill files.
HELP
}

die() { echo "Error: $*" >&2; exit 1; }

client=auto
project=
while (($#)); do
    case "$1" in
        --client|--project)
            (($# >= 2)) && [[ -n $2 && $2 != --* ]] || { usage >&2; exit 2; }
            if [[ $1 == --client ]]; then client=$2; else project=$2; fi
            shift 2 ;;
        --update) shift ;;
        -h|--help) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
    esac
done
case "$client" in auto|codex|claude|dsh|both|all) ;; *) usage >&2; exit 2 ;; esac
case "$(hostname -s)" in
    hpc-login*|hpc-exec*|hpc-head*) die 'Run this on your local workstation, outside Cetus.' ;;
esac
[[ -z ${PBS_JOBID:-} ]] || die 'Run this outside PBS allocations.'

base=$HOME
if [[ -n $project ]]; then
    [[ -d $project ]] || die "Project directory does not exist: $project"
    base=$(cd -- "$project" && pwd -P)
fi
clients=()
if [[ $client == auto ]]; then
    if [[ -n ${CODEX_THREAD_ID:-} ]]; then
        clients=(codex)
    elif [[ ${CLAUDECODE:-} == 1 ]]; then
        clients=(claude)
    else
        for executable in codex claude dsh; do
            if command -v "$executable" >/dev/null 2>&1; then
                clients+=("$executable")
            fi
        done
    fi
    (( ${#clients[@]} > 0 )) || die 'No client detected. Use --client codex, --client claude or --client dsh for a desktop/npx client.'
elif [[ $client == both ]]; then
    clients=(codex claude)
elif [[ $client == all ]]; then
    clients=(codex claude dsh)
else
    clients=("$client")
fi
printf 'Selected client: %s\n' "${clients[@]}"

# Keep temporary content and rollback state private to this invocation.
download_dir=
staging=
lock=
backup=
destination=
cleanup() {
    if [[ -n $backup && ! -e $destination && ! -L $destination ]]; then
        mv -- "$backup/cetus-pbs" "$destination" || echo "Restore from $backup/cetus-pbs" >&2
    fi
    [[ -z $staging ]] || rm -rf -- "$staging"
    [[ -z $download_dir ]] || rm -rf -- "$download_dir"
    [[ -z $lock ]] || rmdir -- "$lock"
    return 0
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

script_file=${BASH_SOURCE[0]:-}
source_dir=
if [[ -n $script_file && -f $script_file ]]; then
    root=$(cd -- "$(dirname -- "$script_file")/.." && pwd -P)
    if [[ -f "$root/skills/cetus-pbs/SKILL.md" ]]; then
        source_dir="$root/skills/cetus-pbs"
    fi
fi
if [[ -z $source_dir ]]; then
    command -v curl >/dev/null 2>&1 || die 'curl is required to download the skill.'
    command -v tar >/dev/null 2>&1 || die 'tar is required to unpack the skill.'
    download_dir=$(mktemp -d "${TMPDIR:-/tmp}/cetus-pbs-download.XXXXXXXX")
    curl -fLsS --connect-timeout 15 --max-time 120 \
        https://github.com/ChonghaoCheng/UTS_PBS_Skills/archive/refs/heads/main.tar.gz \
        -o "$download_dir/source.tar.gz"
    tar xzf "$download_dir/source.tar.gz" -C "$download_dir" \
        UTS_PBS_Skills-main/skills/cetus-pbs
    source_dir="$download_dir/UTS_PBS_Skills-main/skills/cetus-pbs"
fi
for required in SKILL.md references/ssh.md references/pbs.md assets/job.pbs; do
    [[ -s "$source_dir/$required" ]] || die "Incomplete skill source: $required"
done

for selected in "${clients[@]}"; do
    case "$selected" in
        codex) config_dir="$base/.agents" ;;
        claude)
            config_dir="$base/.claude"
            [[ -n $project ]] || config_dir=${CLAUDE_CONFIG_DIR:-$config_dir} ;;
        dsh)
            config_dir="$base/.dsh"
            [[ -n $project ]] || config_dir=${DSH_HOME:-$config_dir} ;;
    esac
    mkdir -p -- "$config_dir/skills"
    parent=$(cd -- "$config_dir/skills" && pwd -P)
    destination="$parent/cetus-pbs"
    [[ ! $destination -ef $source_dir ]] || die "Destination is the source skill: $destination"
    candidate_lock="$parent/.cetus-pbs-install.lock"
    mkdir -- "$candidate_lock" 2>/dev/null || die "Another install may be running; inspect $candidate_lock before retrying."
    lock=$candidate_lock
    if [[ -d $destination ]] && diff -qr -- "$source_dir" "$destination" >/dev/null; then
        echo "Already up to date: $destination/SKILL.md"
    else
        staging=$(mktemp -d "$parent/.cetus-pbs-install.XXXXXXXX")
        cp -R -- "$source_dir/." "$staging/"
        if [[ -e $destination || -L $destination ]]; then
            mkdir -p -- "$config_dir/skill-backups"
            backup=$(mktemp -d "$config_dir/skill-backups/cetus-pbs.XXXXXXXX")
            mv -- "$destination" "$backup/cetus-pbs"
            echo "Backup: $backup/cetus-pbs"
        fi
        mv -- "$staging" "$destination"
        staging=
        backup=
        echo "Installed: $destination/SKILL.md"
    fi
    rmdir -- "$lock"
    lock=
done
printf '\nOpen a new session. Codex: $cetus-pbs | Claude: /cetus-pbs | Harness: load cetus-pbs\n'
