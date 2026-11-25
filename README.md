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

Open the client in your local experiment repository and send:

```text
Use cetus-pbs to run one minimal experiment on Cetus from this repository's configuration, then collect the logs and metrics and report the outcome.
```

The assistant first reads repository instructions, experiment configurations, launch scripts, existing PBS tools and SSH settings. It then freezes the code, selects resources, submits once, monitors the job and analyzes the results. It generates or captures the `run_id`, version records, PBS Job ID and timestamps.

It asks together only for execution-critical information that remains unresolved, such as the experiment entry point, input dataset or SSH identity. Resource selection starts from the repository's existing small-run settings and accounts for queue limits.

Add constraints to the same sentence when needed, for example, “use the current committed code, run one seed, and limit walltime to 10 minutes.” Codex also accepts `$cetus-pbs`; Claude Code accepts `/cetus-pbs`.

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

- The AI client runs on the local workstation. Cetus login nodes handle file transfer, lightweight inspection and scheduling. Compute-intensive workloads run on compute nodes through PBS.
- Give each experiment an independent `run_id`, code snapshot, configuration and output directory. Record code and data versions, parameters, PBS Job ID, timestamps, exit status and result files.
- Use concurrency-limited job arrays for independent batch experiments. A minimal experiment runs one bounded case; scaling requires a defined experiment scope.
- Preserve submission receipts and monitor with a polling interval and deadline. Reconcile uncertain submissions against existing jobs. When a retry is requested, create new runs for identified failures with their original logs and provenance retained.
- Obtain user confirmation before deleting jobs or overwriting experiment results. Do not loop over submissions. Do not run AI clients on Cetus login or compute nodes.

## Documentation and templates

| File | Purpose |
| --- | --- |
| [SKILL.md](skills/cetus-pbs/SKILL.md) | Skill entry point and execution rules |
| [SSH access](skills/cetus-pbs/references/ssh.md) | Connection configuration and authentication diagnosis |
| [PBS workflow](skills/cetus-pbs/references/pbs.md) | Snapshots, submission, arrays, monitoring and result collection |
| [job.pbs](skills/cetus-pbs/assets/job.pbs) | Reusable PBS job template |
| [Client compatibility](docs/clients.md) | Host adapters and skill discovery |
| [Windows guide](docs/windows.md) | Native Windows and WSL 2 installation and usage |
