# UTS PBS Skills

**English** · [简体中文](README.zh-CN.md)

An Agent Skill for UTS Cetus providing operating procedures and script templates for SSH access, PBS resource configuration, job submission, monitoring, result collection and failed-task retries. It supports Agent Skills hosts with file access and terminal tools, including desktop applications, IDE assistants and terminal clients.

The AI client runs on the local workstation. Cetus login nodes handle file transfers, lightweight inspection and scheduler operations. Simulation, training and other compute-intensive workloads run on compute nodes through PBS.

## Requirements

- Skill installation requires Bash, curl and tar.
- The experiment workflow uses Git, SSH, rsync and Python 3, with a valid Cetus account and network access.
- Install the skill in the environment where the agent executes commands. Native Windows clients and WSL use separate home directories. See the [Windows guide](docs/windows.md).

## Install the skill

Run in a local terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

The default mode identifies the active Codex or Claude session from environment variables when available. Otherwise it detects supported client commands on PATH. If none are found, it exits with an error and requests explicit selection.

For desktop applications, IDE assistants or clients launched through `npx`, select the installation target explicitly:

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash -s -- --client codex
```

Supported `--client` values include `codex`, `claude`, `dsh`, `cursor`, `copilot`, `gemini` and `opencode`. See [client compatibility](docs/clients.md) for discovery paths and supported interfaces.

To install from source:

```bash
git clone https://github.com/ChonghaoCheng/UTS_PBS_Skills.git
cd UTS_PBS_Skills
bash scripts/install.sh --client codex
```

| Option | Behavior |
| --- | --- |
| No arguments or `--client auto` | Detect clients and install at personal scope by default |
| `--client NAME` | Install for the selected client |
| `--client all` | Install for all seven built-in adapters |
| `--project PATH` | Install into an existing project directory; can be combined with `--client` |
| `--skills-dir PATH` | Use another host's skill directory; cannot be combined with `--client` or `--project` |
| `--help` | Print the complete option reference |

The installer prints the actual `SKILL.md` path. Repeated installation skips identical content and backs up changed copies before replacing them. Keep the complete skill folder, including `references/` and `assets/`. Open a new agent session after installation.

Alternatively, give the current agent this instruction:

> Read https://github.com/ChonghaoCheng/UTS_PBS_Skills and install cetus-pbs locally for the current client. Inspect the installer, select the matching adapter or documented skill directory, run the installation, and report the installed path and invocation.

## Run an experiment

Configure a local `cetus` alias using the [SSH guide](skills/cetus-pbs/references/ssh.md). Open the experiment repository in the client and load `cetus-pbs`. Codex accepts `$cetus-pbs` and Claude Code accepts `/cetus-pbs`. Other hosts use their own skill invocation mechanism.

Provide the code revision, launch command, data version, resource request and output requirements. For example:

```text
Use cetus-pbs to run one minimal experiment.
Repository: <local repository path>
Code revision: <Git commit>
Launch command: <entry point and complete arguments>
Input data: <versioned shared path and checksum>
PBS resources: select=1:ncpus=1:mem=2gb, walltime=00:10:00
Expected outputs: <metric files, result files and acceptance criteria>

Freeze the code and configuration, submit once, monitor until termination,
collect logs and metrics, and record the run_id, PBS Job ID, data version,
timestamps and exit status. Analyze any failures.
```

The resource request above is for a minimal example. Size production jobs from measured CPU, memory and runtime requirements and the current queue limits.

## Execution rules

- Give each experiment an independent `run_id`, code snapshot, configuration and output directory. Queued jobs must be isolated from subsequent code changes.
- Record the Git commit, parameters, input identifiers and checksums, PBS Job ID, start/end times, exit status and result files.
- Use concurrency-limited job arrays for independent seeds or parameter sweeps. Keep outputs separate for each index and retry.
- Save the submission receipt and monitor with a polling interval and deadline. After a connection failure or missing scheduler entry, inspect scheduler state and existing receipts before deciding the next action.
- Preserve failed-run logs. Create new runs only for identified failed tasks, recording the parent run and task index.
- Obtain user confirmation before deleting jobs or overwriting experiment results. Do not loop over submissions. Do not run AI clients on Cetus login or compute nodes.

## Documentation and templates

| File | Purpose |
| --- | --- |
| [SKILL.md](skills/cetus-pbs/SKILL.md) | Skill entry point and execution rules |
| [SSH access](skills/cetus-pbs/references/ssh.md) | SSH configuration, key authentication and connection diagnosis |
| [PBS workflow](skills/cetus-pbs/references/pbs.md) | Snapshots, submission, arrays, monitoring and result collection |
| [job.pbs](skills/cetus-pbs/assets/job.pbs) | Reusable PBS job template |
| [Client compatibility](docs/clients.md) | Host adapters and skill discovery |
| [Windows guide](docs/windows.md) | Native Windows and WSL 2 installation and usage |
