# Native PBS workflow

Run SSH and rsync on the local workstation. Replace example inputs with actual code, data paths and resource measurements. Prefer an existing repository submission tool if it preserves immutable snapshots and run provenance.

## Prepare

Create a unique run directory on the local workstation, freeze the selected Git revision and configuration, and upload them to a new shared directory such as $HOME/cetus-runs/<run_id>/. Do not overwrite an existing run directory. Keep an input manifest and checksums. Check queue limits with ssh cetus 'qstat -Qf'.

## Example job script

Save this as job.pbs in the remote run directory alongside code.tar. Replace the example command with the actual frozen entry point before submission. PBS resource directives apply per array subjob.

```bash
#!/bin/bash
#PBS -S /bin/bash
#PBS -l select=1:ncpus=1:mem=2gb
#PBS -l walltime=00:10:00
#PBS -j oe
set -euo pipefail
umask 077
: "${PBS_JOBID:?Submit through qsub}"
cd "$PBS_O_WORKDIR"
run=$PWD
index=${PBS_ARRAY_INDEX:-1}
mkdir -p "$run/tasks/$index"
attempt=$(mktemp -d "$run/tasks/$index/attempt-XXXXXXXX")
exec >"$attempt/stdout.log" 2>"$attempt/stderr.log"
scratch=
finish() {
    rc=$?
    trap - EXIT
    set +e
    # Exit trap also runs after application failure. Preserve scratch if copying fails.
    if [[ -n "$scratch" && -d "$scratch/results" ]]; then
        rsync -a "$scratch/results/" "$attempt/results/"
        copy_rc=$?
        if (( copy_rc != 0 )); then
            echo "Copy failed; scratch retained at $scratch" >&2
            (( rc != 0 )) || rc=$copy_rc
        fi
    fi
    date -u +%FT%TZ >"$attempt/ended_at"
    printf '%s\n' "$rc" >"$attempt/exit_status"
    exit "$rc"
}
trap finish EXIT
trap 'exit 143' TERM
date -u +%FT%TZ >"$attempt/started_at"
hostname >"$attempt/hostname"
printf '%s\n' "$PBS_JOBID" >"$attempt/pbs_job_id"
scratch=$(mktemp -d "/scratch/pbs-${USER}-XXXXXXXX")
mkdir "$scratch/code" "$scratch/results"
tar xf "$run/code.tar" -C "$scratch/code"
cd "$scratch/code"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export RESULT_DIR="$scratch/results" TASK_INDEX="$index"
# Replace this with the actual executable and frozen task configuration.
python3 experiments/run.py --task-index "$index" --output "$RESULT_DIR"
```

The example retains scratch for inspection. After verifying result transfer, remove only the job's own recorded scratch directory under the applicable cleanup policy. Hard termination may prevent the EXIT trap; save durable checkpoints during long tasks.

## Submit, inspect and collect

From the local client, after uploading the frozen run:

```bash
# Set this to the unique directory created for this submission.
run_id=YOUR_RUN_ID
ssh cetus "cd cetus-runs/$run_id && qsub job.pbs > job_id && cat job_id"
# Use the exact returned ID.
ssh cetus "qstat -fx 'JOB_ID'"
# Once terminal, collect into a new local directory.
mkdir -p "collected/$run_id"
rsync -a "cetus:cetus-runs/$run_id/tasks/" "collected/$run_id/tasks/"
```

For a batch, replace the single qsub call with `qsub -J '1-25%5' job.pbs`. The script must map each PBS_ARRAY_INDEX to an explicitly frozen parameter/seed list. Use `qstat -fxt 'ARRAY_JOB_ID'` to inspect subjobs. Each subjob requests 1 CPU and 2 GB in this example, and at most five run concurrently, subject to scheduler limits.

Before collection, check both PBS Exit_status and each attempt's exit_status, inspect stderr, and validate expected artifacts. Preserve qstat records and any PBS spool logs. Retry only failed indices in a new run using the original snapshot/config or an explicitly documented correction.

Resource values above are examples. Tune them from resources_used.mem, resources_used.walltime and CPU usage. Request GPUs or multinode resources only when the application needs them and after checking current Cetus queue syntax and eligibility.

[Job scripts](https://cetus.hpc.uts.edu.au/pbs/job_scripts/) · [Job arrays](https://cetus.hpc.uts.edu.au/pbs/array_jobs/)
