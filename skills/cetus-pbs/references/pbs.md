# Native PBS operations

Use existing submission tools when suitable. The workflow applies to scripts, binaries, file-processing tasks and other PBS workloads, with or without Git or input data. Match the requested operation: inspecting or collecting an existing job does not require a new submission.

The commands below are an **optional shell-only demonstration**. The `cetus` SSH alias, `cetus-runs` directory names, example resources and array range are replaceable conventions, not PBS requirements or defaults for other tasks. Use the user's existing paths and current queue limits for real work. The bundled template is for a single execution node; distributed tasks need an appropriate launcher and node/staging design.

## 1. Prepare a frozen run

Set `skill_dir` to the installed skill directory. Choose a writable local run root with adequate space. The example uses a directory under the current user's home and does not require a project repository or application runtime. Run the demonstration steps in the same Bash session so their variables remain available.

```bash
set -euo pipefail
umask 077
skill_dir=/absolute/path/to/cetus-pbs
local_base="$HOME/cetus-runs"
mkdir -p "$local_base"
local_run=$(mktemp -d "$local_base/$(date -u +%Y%m%dT%H%M%SZ)-XXXXXXXX")
run_id=${local_run##*/}
mkdir "$local_run/source"
printf 'example input\n' >"$local_run/source/input.txt"
tar -C "$local_run/source" -cf "$local_run/code.tar" .
cp "$skill_dir/assets/job.pbs" "$local_run/job.pbs"
printf 'run_id=%s\ncreated_at=%s\n' \
    "$run_id" "$(date -u +%FT%TZ)" >"$local_run/manifest.txt"
cat >"$local_run/request.env" <<'REQUEST'
# Demonstration values for this tiny shell task only. Size real jobs separately.
REQUEST_SELECT=select=1:ncpus=1:mem=2gb
REQUEST_WALLTIME=00:10:00
REQUEST
cat >"$local_run/command.sh" <<'COMMAND'
#!/bin/bash
set -euo pipefail
# Arguments: task index and private output directory.
# Load the task's runtime and configure its processes/threads here when needed.
cat input.txt >"$2/output.txt"
printf '%s\n' "$1" >"$2/task_index.txt"
COMMAND
(cd "$local_run" && sha256sum code.tar job.pbs command.sh request.env manifest.txt >SHA256SUMS)
```

For a real task, replace the demonstration files and launcher with an independent copy/archive of the required inputs, program and configuration. Keep the snapshot outside any source tree being archived, and record the command and relevant input identifiers/checksums. Avoid shared mutable launchers.

If the task uses Git, record the selected revision and stage any required uncommitted/untracked files, submodules and actual Git LFS content. `git archive` captures committed files subject to export attributes; it is one snapshot option. Tasks without Git use file manifests/checksums. Required files and archive exclusions depend on the task; no universal `results/`, `runs/` or `logs/` exclusion is applied.

The template has **no queue, CPU, memory or walltime directives**. Freeze the actual resource request in `request.env` before checksumming. The submission below passes those values to `qsub`. Add an approved queue (`-q`), GPU resources or other scheduler options only when required by the task and supported by the site. Inspect `qstat -Qf` for current limits; no queue-limit table is assumed to stay current.

For node-local work, use site-approved storage. The template uses an explicitly configured `CETUS_SCRATCH_ROOT`, otherwise the execution environment's `TMPDIR`, otherwise a private directory within the run. To select a different root for a particular job, set it in the copied job script before checksumming, or freeze and pass the specific variable with `qsub -v`. Check its accessibility and capacity; do not copy a previous user's scratch path. Configure application parallelism in `command.sh`, not by relying on a fixed thread count in the template.

## 2. Stage and submit once

These operations run on the submission computer. Replace `cetus` with the user's working SSH alias if different. For the demonstration, the remote run root is `$HOME/cetus-runs`; for real work, use a suitable user-approved directory accessible to the selected nodes and update both transfer and job paths consistently.

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
# Read only the frozen, inspected configuration for this run.
source request.env
: "${REQUEST_SELECT:?Missing resource selection}"
: "${REQUEST_WALLTIME:?Missing walltime}"
mkdir submission
mkdir pbs
qsub -N "$2" -l "$REQUEST_SELECT" -l "walltime=$REQUEST_WALLTIME" \
    -j oe -o "$PWD/pbs/" job.pbs >submission/job_id.tmp
mv submission/job_id.tmp submission/job_id
cat submission/job_id
REMOTE
```

The exclusive `submission/` marker prevents duplicate submission through this procedure. If `qsub` or the connection fails, retain that marker. Inspect `submission/job_id`, its temporary file and the scheduler's unique job name before deciding whether a new submission is necessary. Do not remove the marker and blindly repeat `qsub`.

For independent batch tasks, replace the single invocation with an array request while retaining the same receipt/marker handling, for example:

```bash
qsub -J '1-25%5' -N "$2" -l "$REQUEST_SELECT" -l "walltime=$REQUEST_WALLTIME" \
    -j oe -o "$PWD/pbs/" job.pbs >submission/job_id.tmp
```

This range is an example: use the actual task indices, concurrency cap and current queue limits. Freeze an index-to-task mapping with the inputs and arguments for each task. The demonstration launcher only records its index; replace it with the appropriate lookup for real batch work. Resources are requested per subjob. Separate tasks with different resource requirements into different arrays. Preserve outputs per index and attempt, including zero-based indices when used.

## 3. Inspect status and collect outputs

Use the exact ID from the saved receipt, or the existing job ID provided for a status request. The values below use `local_run` from the preparation step and first copy the remotely saved receipt. For an existing job, choose a local record directory and use its known ID without creating or resubmitting that job.

```bash
mkdir -p "$local_run/submission"
rsync -a -- "cetus:cetus-runs/$run_id/submission/" "$local_run/submission/"
job_id=$(cat "$local_run/submission/job_id")
[[ $job_id =~ ^[0-9]+(\[([0-9]+)?\])?\.[A-Za-z0-9._-]+$ ]]
mkdir -p "$local_run/status"
observation=$(mktemp -d "$local_run/status/observation-XXXXXXXX")
ssh cetus "qstat -fxt '$job_id'" >"$observation/qstat.txt" 2>"$observation/stderr.log"
cat "$observation/qstat.txt"
```

Check each relevant subjob as well as the parent. Preserve terminal records and `Exit_status`; array parents can hide individual failures. Poll with a chosen interval and deadline. If history has expired, use previously captured terminal records and worker logs. A missing job entry alone does not establish success.

After termination, collect into a fresh directory:

```bash
mkdir -p "$local_run/collections"
collection=$(mktemp -d "$local_run/collections/collection-XXXXXXXX")
rsync -a -- "cetus:cetus-runs/$run_id/tasks/" "$collection/tasks/"
rsync -a -- "cetus:cetus-runs/$run_id/pbs/" "$collection/pbs/"
cp "$observation/qstat.txt" "$collection/qstat.txt"
```

For this shell demonstration, `output.txt` must contain `example input`, `task_index.txt` must match the task index, and worker/scheduler exits must be zero. For other tasks, use their expected outputs and success criteria. Metrics, checkpoints and domain-specific analysis apply only when the program produces or requires them. Use rsync filters for selected outputs when transferring everything would be excessive.

The template verifies its checksum manifest and creates a private working directory and a unique per-index attempt. It copies regular output files back, then removes only its private working directory after successful transfer. A transfer error retains that directory and returns a nonzero worker exit. Node-local storage can be lost after a job ends, and hard kills can prevent final writeback. Programs needing durable progress should write important outputs/checkpoints to approved persistent storage during execution.

## 4. Cancel or retry when authorized

For an explicit request to cancel an identified job, check that the ID matches the intended task, then use `qdel`. Cancelling an array parent affects its subjobs; use the selected subjob ID when only that task should be cancelled.

```bash
ssh cetus "qdel '$job_id'"
```

Use the same ID validation as for status. User authorization is required; an explicit request to cancel that ID is sufficient. Do not repeatedly ask for an authorization already provided.

For a requested retry, inspect scheduler comments, exit statuses, actual resource use, worker stderr and transfer errors. Distinguish application, runtime, missing input, resource-limit and transfer failures. Create a new run only for the identified failed work and record the parent run/index. Preserve previous results. Changes to inputs, code or resource requests must be recorded; do not silently enlarge the workload or loop over submissions.

[Cetus PBS](https://cetus.hpc.uts.edu.au/pbs/) · [First job example](https://cetus.hpc.uts.edu.au/getting_started/running/) · [Queues](https://cetus.hpc.uts.edu.au/pbs/queues/)
