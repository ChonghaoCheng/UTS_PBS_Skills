---
name: cetus-pbs
description: Use UTS Cetus through SSH and native PBS commands for access setup, job scripts, resource requests, arrays, status checks, output collection and failed-task retries.
---

# UTS Cetus PBS

Operate from the user's submission environment using the host's file and terminal tools. Keep the AI client outside Cetus. Use login nodes for lightweight inspection, transfer and scheduler commands; run compute-intensive programs through PBS. The examples use Bash, SSH, rsync, tar and SHA256 tools; when local `rsync` is unavailable (such as on native Windows), use the `tar`-over-`ssh` transfer commands in the PBS reference. Git and application runtimes are needed only for tasks that use them. On Windows, use the tools available in the actual Windows/WSL execution environment.

Read [SSH access](references/ssh.md) for connection setup and diagnosis. Read [PBS operations](references/pbs.md) for submission, arrays, status, collection or cancellation. Adapt [the job template](assets/job.pbs) to the requested workload. Resolve relative paths from this skill's directory.

## Discover the requested task

Match the user's requested operation and scope. A status or collection request does not authorize a new submission. For a run request, inspect the current task directory, its instructions, launch scripts, configuration and any existing PBS tooling. A Git repository, dataset, metrics file or particular application is not required. Reuse working tools and infer settings from evidence rather than asking the user to fill a standard research form.

Determine the entry point, arguments, runtime/dependencies, inputs and expected outputs where applicable. Reuse the user's SSH alias, account and storage locations. If non-interactive SSH access is not yet configured and setup is requested, prepare the local key and SSH config, give the user the one-time interactive public-key enrollment command to run in their own terminal (never ask for passwords or MFA codes in chat), and verify with the fresh-key probe; on connection timeouts outside campus, ask the user to verify UTS VPN first. Ask together only for execution-critical information that remains unavailable or ambiguous. Do not invent paths, credentials, workload parameters, queue names or resource requirements.

A minimal or smoke run is appropriate when requested or agreed for setup diagnosis. Do not automatically reduce an existing workload, run an extra test job or expand a single task into a batch. Generate run identifiers and operational records without asking the user to provide them.

## Prepare an isolated run

Create a unique run directory and freeze the files needed for this task, configuration and launchers. Copy or archive files independently of a live working directory. When Git applies, record the selected revision and account for needed uncommitted/untracked files, submodules and Git LFS content. Git archive alone captures committed content subject to export attributes. For other tasks, record the source files and snapshot checksums.

Record the command, actual resource request, relevant input identifiers, snapshot/checksums, PBS receipt, times, exit status and collected files. Record input versions or hashes where useful; do not require a dataset for jobs without one. Use user-approved storage accessible to the selected compute nodes. For I/O-heavy or many-small-file workloads, verify a site-approved node-local scratch path (such as `/scratch` on Cetus execution nodes) and configure `CETUS_SCRATCH_ROOT` rather than defaulting heavy scratch I/O onto networked home storage; retain important outputs and checkpoints on durable storage. Choose paths from the current task and site guidance, not a previous user's layout.

## Request resources and submit

Check current queues and limits with `qstat -Qf`. Select the queue (`REQUEST_QUEUE` when needed, such as CPU vs GPU queues), CPU, RAM, walltime, GPUs (`ngpus` or site-defined chunk attributes), node count and software environment from the workload's configuration or measurements and current site policy. There is no universal queue or numeric resource default. Initialize non-interactive shells explicitly in `command.sh` before calling `module` or `conda`, and configure application processes and library threads to match the `ncpus` allocation. Multi-node programs require a suitable distributed launcher.

For independent tasks, use arrays with a concurrency cap and a frozen index-to-input/argument mapping. Keep each index and attempt separate. Use different arrays for workloads with different resource requirements. Array ranges and concurrency must match the requested task set and queue limits.

Submit once per run and save the receipt. Use an exclusive submission marker as in the reference. If acceptance becomes uncertain, inspect the receipt and scheduler state before deciding the next action. Do not automatically resubmit.

## Monitor, collect and recover

Poll with an interval and finite deadline, including array subjobs when applicable. Preserve terminal scheduler records before history expires. A missing qstat entry alone does not establish completion or success.

Collect logs and requested outputs into a fresh local directory. Check scheduler Exit_status, worker exit_status, transfer errors and the task's expected files. Collect metrics or perform domain-specific analysis only when relevant to the task. Put compute-intensive checks through PBS. Distinguish application, environment, input/staging, resource-limit and transfer failures.

When a retry is requested or already authorized, rerun only identified failed work under a new run ID and record its parent/index. Keep earlier outputs. Obtain user authorization before cancelling jobs or replacing results; an explicit request to cancel specified jobs already provides that authorization. Never loop over submissions or silently increase the workload. Clean only private work directories created by this run after successful transfer.
