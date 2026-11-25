---
name: cetus-pbs
description: Operate UTS Cetus through SSH and native PBS commands. Use for SSH setup, resource sizing, job scripts and arrays, monitoring, collecting logs and results, and rerunning failed tasks.
---

# UTS Cetus PBS

Run the AI client on the local workstation. The user requires AI clients to stay off Cetus login and compute nodes, including PBS allocations. Use SSH/rsync from the workstation for remote operations. Limit the login node to lightweight inspection, transfer and scheduler commands; submit research computation and expensive tests/analysis through PBS.

Read [SSH access](references/ssh.md) when setting up or diagnosing a connection. Read [PBS workflow](references/pbs.md) when preparing, submitting or collecting a run. Copy [the job template](assets/job.pbs) into a fresh run directory and adapt its resources and command launcher to the workload.

## Prepare

Inspect the user's repository and existing submission tools first. Reuse working tools when they preserve the requirements below. Confirm the code revision, entry point, arguments, input version, seeds and workload size. Resolve missing values from repository context or ask when they affect execution.

Create a unique run ID. Freeze code, configuration and launchers in an independent snapshot with a manifest recording the commit, input identifiers and checksums. Git archive includes committed content subject to export attributes; separately stage required untracked files, submodule content and actual Git LFS data when needed. Queued work must not depend on later changes to a live checkout or mutable dataset.

Keep durable inputs on shared storage. Use read-only, versioned paths or hashes and stage only the needed shard into node-local scratch for heavy I/O. Write logs and checkpoints to the durable run directory during long tasks because a hard kill can prevent final writeback.

## Allocate and submit

Run a minimal real workload first and check expected outputs. Size each subjob's CPU, RAM and walltime from representative cases, including startup and writeback. Query current limits with qstat -Qf. CPU allocation does not configure application parallelism; align workers and library threads with the requested ncpus. Request GPUs or multiple nodes only when supported by the application and queue.

For independent seeds/parameters, use job arrays with a concurrency cap and separate index/attempt outputs. Group short cases and shard slow ones. Separate workloads with different resource requirements into different arrays.

Submit once per run and save the PBS receipt. Use an exclusive submission marker as in the reference. If acceptance becomes uncertain after a connection failure, inspect the receipt or unique job name before considering a new submission. Do not automatically resubmit.

## Monitor and recover

Poll with an interval and finite deadline. Check array subjobs as well as the parent. Preserve terminal scheduler status before history expires. A missing qstat entry alone cannot establish completion or success.

Collect logs and metrics into a new local collection directory. Check scheduler Exit_status and worker exit_status, result-transfer errors and expected result files. Validate scientific outputs using the experiment's criteria. Run compute-heavy validation through PBS. Distinguish application/scientific failures from staging, environment and transfer failures.

Retry only identified failed work with a new run ID and parent/index provenance. Keep prior outputs. Deleting jobs or overwriting experiment results requires the user's confirmation. Private scratch created by this job may be cleaned after successful transfer, as in the template. Never loop over submissions or silently enlarge the experiment.
