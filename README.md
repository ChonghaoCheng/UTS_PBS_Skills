# UTS PBS Skills

**English** · [简体中文](README.zh-CN.md)

An Agent Skill for UTS Cetus with procedures and templates for SSH access, PBS submission, job monitoring and result collection. It supports desktop applications, IDE assistants and terminal clients with file access and terminal tools.

## Install with one sentence

Send this sentence to the AI assistant you are using:

```text
Read https://github.com/ChonghaoCheng/UTS_PBS_Skills, install cetus-pbs for this client automatically, and check that the skill and its supporting files are complete.
```

The assistant selects the installation method from the current client, operating system and available tools. It defaults to personal scope and reports the installed path and invocation. Repeated installation skips identical content and backs up existing copies before updates. Open a new session after installation.

## Run with one sentence

Open the client in the directory containing your task files and send:

```text
Use cetus-pbs to submit a PBS job on Cetus from this directory's task configuration, then collect the logs and outputs and report its status.
```

The assistant first reads task instructions, launch scripts, configuration, existing PBS tools and SSH settings. It prepares independent task files, selects resources, submits and monitors the job. It generates or captures the `run_id`, file snapshot or applicable Git revision, PBS Job ID and timestamps. Tasks can use ordinary directories; Git, datasets and metric files are optional.

It asks together only for unresolved execution-critical information such as the command, required inputs, SSH identity or resource requirements. The account, connection alias, paths, software environment, queue and resource request come from the current task and environment. An initial test or minimal task runs only when requested or agreed.

Add the task scope, output requirements or “inspect the configuration without submitting” to the same sentence when needed. Codex also accepts `$cetus-pbs`; Claude Code accepts `/cetus-pbs`.

## Skill contents

The skill package includes the `SKILL.md` operating rules, SSH/PBS references and the `job.pbs` job template. The assistant combines these with the current task configuration and uses SSH, rsync and native PBS commands for the following workflow:

| Capability | Contents |
| --- | --- |
| SSH access | Reuse connection settings, guide key authentication and connection multiplexing, and diagnose network or permission failures |
| Task preparation | Read commands and configuration, prepare independent file snapshots, launchers and a `run_id` for the requested scope, and record a revision when Git applies |
| Resource configuration | Size CPU, memory and walltime from existing settings, measured overhead and queue limits, and align process/thread counts with the allocation |
| Submission and monitoring | Capture the PBS Job ID and submission receipt, prevent duplicate submission, and monitor jobs and array subjobs with a polling interval and deadline |
| Batch tasks | Run independent tasks as concurrency-limited job arrays, with separate configuration, logs and results per task index |
| Files and storage | Determine task inputs, outputs and writable directories; record checksums and use approved node-local work storage when needed, preserving files that must persist |
| Output collection | Retrieve logs and required outputs, check scheduler and application exit status, and perform metrics checks or domain-specific analysis when relevant |
| Failure recovery | Distinguish application, environment, staging and transfer failures, rerun identified failed tasks individually, and preserve original results and parent-run provenance |

The bundled template receives resource requests through `qsub -l` and defines no queue, CPU, memory or walltime defaults. Configure application threads and work directories for the task and execution environment. Values and directory names in the reference walkthrough are demonstration examples.

## Manual installation

Expand the instructions below to use a terminal directly or select an installation scope. Separate instructions cover [native Windows and WSL 2](docs/windows.md).

<details>
<summary>Installation commands and options</summary>

Skill installation requires Bash, curl and tar. Run in a local terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

The default mode identifies the active Codex or Claude session when available, then falls back to supported client commands on PATH. Select an adapter explicitly for a desktop application without a command entry:

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash -s -- --client codex
```

Alternatively, install from source:

```bash
git clone https://github.com/ChonghaoCheng/UTS_PBS_Skills.git
cd UTS_PBS_Skills
bash scripts/install.sh --client codex
```

| Option | Behavior |
| --- | --- |
| No arguments or `--client auto` | Detect clients and install at personal scope by default |
| `--client NAME` | Select `codex`, `claude`, `dsh`, `cursor`, `copilot`, `gemini` or `opencode` |
| `--client all` | Install for all seven built-in adapters |
| `--project PATH` | Install into an existing project directory; can be combined with `--client` |
| `--skills-dir PATH` | Use another host's skill directory; cannot be combined with `--client` or `--project` |
| `--help` | Print the complete option reference |

The installer prints the actual `SKILL.md` path. Keep the entire skill directory, including `references/` and `assets/`. Install in the environment where the agent executes commands. Native Windows clients and WSL use separate home directories.

</details>

## Execution rules

- The AI client runs in the submission environment outside Cetus. Cetus login nodes handle file transfer, lightweight inspection and scheduling. Compute-intensive workloads run on compute nodes through PBS.
- Give each new submission an independent `run_id`, file snapshot, configuration and output directory. Record commands, resource requests, applicable versions/checksums, PBS Job ID, timestamps and exit status.
- Use concurrency-limited arrays for independent batch tasks, with ranges, mappings and concurrency determined by the requested workload. Inspect, collect or cancel existing jobs as requested.
- Preserve submission receipts and monitor with a polling interval and deadline. Reconcile uncertain submissions against existing jobs. When a retry is requested, create new runs for identified failures with their original logs and provenance retained.
- Obtain user authorization before cancelling jobs or overwriting outputs; a request to cancel specified jobs provides that authorization. Do not loop over submissions or change task scope silently. This workflow keeps AI clients in the submission environment outside Cetus.

## Documentation and templates

| File | Purpose |
| --- | --- |
| [SKILL.md](skills/cetus-pbs/SKILL.md) | Skill entry point and execution rules |
| [SSH access](skills/cetus-pbs/references/ssh.md) | Connection configuration and authentication diagnosis |
| [PBS operations](skills/cetus-pbs/references/pbs.md) | Snapshots, resources, submission, arrays, monitoring, collection and cancellation |
| [job.pbs](skills/cetus-pbs/assets/job.pbs) | Reusable PBS job template |
| [Client compatibility](docs/clients.md) | Host adapters and skill discovery |
| [Windows guide](docs/windows.md) | Native Windows and WSL 2 installation and usage |
