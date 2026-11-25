# Native PBS workflow

Run the following client commands on the local workstation. The example starts with one small Python smoke job. Adapt the frozen launcher to the real workload after this completes. Read the template before use and choose resources from measurements and current queue limits.

## 1. Freeze a run locally

Set `skill_dir` to the installed cetus-pbs directory printed by the installer. Run from the intended local Git checkout. The selected commit is recorded before archiving so a later commit cannot change this run.

```bash
skill_dir=/absolute/path/to/cetus-pbs
repo=$(git rev-parse --show-toplevel)
commit=$(git rev-parse HEAD)
mkdir -p "$repo/.cetus-runs"
local_run=$(mktemp -d "$repo/.cetus-runs/$(date -u +%Y%m%dT%H%M%SZ)-XXXXXXXX")
run_id=${local_run##*/}
printf 'run_id=%s\ncommit=%s\ncreated_at=%s\n' \
    "$run_id" "$commit" "$(date -u +%FT%TZ)" >"$local_run/manifest.txt"
git -C "$repo" archive --format=tar -o "$local_run/code.tar" "$commit" -- . \
    ':(exclude,top)results' ':(exclude,top)runs' ':(exclude,top)logs' ':(exclude,top).cetus-runs'
cp "$skill_dir/assets/job.pbs" "$local_run/job.pbs"
cat >"$local_run/command.sh" <<'COMMAND'
#!/bin/bash
set -euo pipefail
# The job template passes the frozen task index and private output directory.
python3 - "$1" "$2" <<'PY'
import json, pathlib, socket, sys
metrics = dict(task_index=int(sys.argv[1]), node=socket.gethostname(), checksum=sum(i*i for i in range(10)))
with (pathlib.Path(sys.argv[2]) / 'metrics.json').open('x') as stream:
    json.dump(metrics, stream)
print(metrics)
PY
COMMAND
(cd "$local_run" && sha256sum code.tar job.pbs command.sh manifest.txt >SHA256SUMS)
```

This archive intentionally excludes root output directories. It contains the chosen commit subject to Git export attributes, not uncommitted edits or external dependencies. Stage any required input files, submodules or Git LFS data separately and add them to the checksum manifest. For shared inputs, record a stable dataset version/path and checksum, and verify it in the launcher. Use fixed dependency versions and load the appropriate compute-node runtime there. Keep scientific parameters in a frozen task configuration.

## 2. Stage and submit once

Check SSH and current queue limits. Create a new remote run directory and upload into it. The run ID generated above contains only safe filename characters.

```bash
ssh -o BatchMode=yes cetus 'command -v qsub qstat rsync tar sha256sum; qstat -Qf'
ssh cetus bash -s -- "$run_id" <<'REMOTE'
set -euo pipefail
[[ $1 =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]]
umask 077
cd "$HOME"
mkdir -p cetus-runs
mkdir "cetus-runs/$1"
REMOTE
rsync -a -- "$local_run/" "cetus:cetus-runs/$run_id/"
ssh cetus bash -s -- "$run_id" "ct${run_id: -8}" <<'REMOTE'
set -euo pipefail
cd "$HOME/cetus-runs/$1"
sha256sum -c SHA256SUMS
mkdir submission
mkdir pbs
qsub -N "$2" -j oe -o "$PWD/pbs/" job.pbs >submission/job_id.tmp
mv submission/job_id.tmp submission/job_id
cat submission/job_id
REMOTE
```

The exclusive `submission/` directory prevents the same run from being submitted twice through this procedure. A failed or interrupted qsub leaves that marker for diagnosis. Read `submission/job_id`, its temporary file, and the scheduler's unique job name before deciding whether a new submission is needed. Do not remove the marker and blindly repeat qsub.

For a job array, replace the single qsub invocation with `qsub -J '1-25%5' -N "$2" -j oe -o "$PWD/pbs/" job.pbs` using the same receipt redirection and submission marker. Freeze an index-to-task mapping containing each task's inputs and arguments before submitting. The example launcher reports each index; replace it with the real task lookup. Array resources are per subjob. At most five subjobs are eligible to run at once, subject to scheduler limits.

The template verifies SHA256SUMS, uses a private scratch directory, and writes logs into a unique per-index attempt. It transfers regular output files, then cleans its own scratch after a successful transfer. A failed transfer retains scratch and yields a nonzero worker exit. Scratch is still node-local and can be lost. Long jobs need checkpoints on shared storage before they finish.

## 3. Monitor and collect

Use the exact PBS ID returned by qsub. Quote array IDs, which contain shell wildcard characters. Save each scheduler observation locally.

```bash
job_id=12345.server
[[ $job_id =~ ^[0-9]+(\[\])?\.[A-Za-z0-9._-]+$ ]]
mkdir -p "$local_run/status"
observation=$(mktemp -d "$local_run/status/observation-XXXXXXXX")
ssh cetus "qstat -fxt '$job_id'" >"$observation/qstat.txt" 2>"$observation/stderr.log"
cat "$observation/qstat.txt"
```

Check the parent and every subjob. Wait for terminal state (`F`, or terminal array subjobs `X`) and inspect `Exit_status`. Poll at a reasonable interval with a deadline. If history has expired, use previously captured terminal records and worker logs; an unknown job ID alone does not establish success.

After termination, collect into a fresh local directory:

```bash
mkdir -p "$local_run/collections"
collection=$(mktemp -d "$local_run/collections/collection-XXXXXXXX")
rsync -a -- "cetus:cetus-runs/$run_id/tasks/" "$collection/tasks/"
rsync -a -- "cetus:cetus-runs/$run_id/pbs/" "$collection/pbs/"
cp "$observation/qstat.txt" "$collection/qstat.txt"
```

The smoke result must have checksum 285, worker exit_status 0 and PBS Exit_status 0, with a compute-node hostname. Inspect stderr and expected result files as well. For large experiments, use rsync filters to retrieve logs/selected metrics first, then specific result files as needed. Keep prior collections intact.

When a task fails, inspect scheduler comment, exits, resource use, worker stderr and output-transfer messages. Create a fresh run for identified failed indices, preserving the original inputs/code unless applying an explicit correction, and record parent run/index. Match the application worker count and thread limits to ncpus. Different resource classes should use separate arrays.

[Job scripts](https://cetus.hpc.uts.edu.au/pbs/job_scripts/) · [Arrays](https://cetus.hpc.uts.edu.au/pbs/array_jobs/) · [Resources](https://cetus.hpc.uts.edu.au/pbs/resources/) · [Queues](https://cetus.hpc.uts.edu.au/pbs/queues/)
