---
name: cetus-pbs
description: Operate UTS Cetus through SSH and native PBS commands. Use for SSH access, resource sizing, job scripts and arrays, monitoring, collecting logs and results, and rerunning failed tasks.
---

# UTS Cetus PBS

Run AI CLIs on the local workstation. AI CLIs are prohibited on Cetus login and compute nodes, including inside PBS jobs, under the user's stated policy. Access Cetus with SSH and rsync. Use the login node for lightweight file and scheduler operations; run computational work through PBS.

Read [SSH access](references/ssh.md) for authentication and multiple clients. Read [PBS workflow](references/pbs.md) for reusable job scripts, submission and monitoring.

## Reproducible execution

Confirm the intended repository revision, executable, arguments, input version, seeds and workload size. Ask for missing values that materially affect execution. Inspect the selected revision and input paths before submission.

Give every submission a unique run ID. Stage an independent code snapshot and frozen configuration, job script and input manifest. Record hashes or versioned dataset paths. Git archives can omit untracked, ignored and submodule content; stage required inputs explicitly. Queued jobs must use the frozen snapshot.

First run a minimal real workload and check scheduler status, worker exit and an expected result. Size CPU, memory and walltime from representative and heavy cases, including startup, input staging and output writeback. Query current queue limits. Set worker/thread counts to match allocated CPUs.

For independent cases use bounded job arrays with separate output directories by index and execution attempt. Group short cases and shard expensive cases. Use separate arrays for materially different resource requirements.

Keep durable inputs and outputs on shared storage. Stage only the required input shard into private node-local scratch for intensive I/O. Periodically save checkpoints for long tasks. Node-local scratch is not shared or durable.

## Monitoring and recovery

Submit once and save the PBS receipt, code revision, configuration, input identifiers and timestamps. If SSH disconnects before acceptance is clear, inspect the receipt or unique PBS job name before resubmitting.

Poll with an interval and deadline. Inspect array subjobs as well as the parent. Preserve terminal qstat output before history expires. A missing job ID does not establish success.

Record execution host, scheduler/worker exits, resource usage, logs and result paths. Collect compact metrics first when practical. Distinguish infrastructure errors from application failures and validate saved outputs.

Retry identified failed cases with a fresh run ID and parent/index provenance. Preserve previous attempts. Require explicit user confirmation before deleting jobs or overwriting results. Never loop over automatic submissions.

[Resources](https://cetus.hpc.uts.edu.au/pbs/resources/) · [Queues](https://cetus.hpc.uts.edu.au/pbs/queues/) · [Job arrays](https://cetus.hpc.uts.edu.au/pbs/array_jobs/) · [Storage](https://cetus.hpc.uts.edu.au/hardware/layout/)
