# UTS PBS Skills

**English** · [简体中文](README.zh-CN.md)

A portable Agent Skill for UTS Cetus, usable from compatible desktop apps, IDE assistants and terminal clients. Your AI assistant works locally, submits computation through SSH and PBS, monitors jobs, and brings back logs and results.

**Run AI clients on your local computer. All simulation, training and other research computation runs in PBS jobs.**

[Windows setup](docs/windows.md) · [Client compatibility](docs/clients.md) · [Installation verification](docs/validation.md)

## Install

Run this on your local Linux or macOS workstation with Bash, curl and tar available:

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

The installer selects the active Codex or Claude session when its environment identifies it. Otherwise it detects supported client commands on PATH. For a desktop or IDE assistant without a command entry, select it explicitly. It prints the installed `SKILL.md` paths. Running it again skips identical files and backs up changed copies before updating them.

For a desktop or IDE client without a command on PATH, or an `npx` Harness session, select the client explicitly:

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash -s -- --client codex
```

Choose `codex`, `claude`, `dsh`, `cursor`, `copilot`, `gemini`, `opencode` or `all`. The installer installs the skill in your personal skill directory. Open a new session after installation.

You can also ask your agent to install it:

> Read https://github.com/ChonghaoCheng/UTS_PBS_Skills and install its cetus-pbs skill for the client you are running in, on this local computer. Run the installer, verify the installed files, and tell me how to invoke it.

To inspect the source or install into a project:

```bash
git clone https://github.com/ChonghaoCheng/UTS_PBS_Skills.git
cd UTS_PBS_Skills
bash scripts/install.sh --client codex --project /path/to/your/project
```

For any other Agent Skills client, pass its documented skill directory:

```bash
bash scripts/install.sh --skills-dir /path/to/client/skills
```

## Choose your client

| Client | Installer selection | Interface |
| --- | --- | --- |
| Codex | `--client codex` | Desktop, IDE, terminal |
| Claude Code | `--client claude` | Code desktop surface, IDE, terminal |
| DeepSeek Harness | `--client dsh` | Local Web UI |
| Cursor | `--client cursor` | IDE agent |
| GitHub Copilot | `--client copilot` | Supported IDE and agent interfaces |
| Gemini CLI | `--client gemini` | Terminal |
| OpenCode | `--client opencode` | Supported agent interfaces |
| Other Agent Skills hosts | `--skills-dir PATH` | The host's documented skill directory |

The same `SKILL.md`, references and PBS template are used by every adapter. The agent needs local file access and tools for SSH and file transfer. Install into the environment where it runs, including WSL or a remote IDE workspace when applicable. Local installation does not automatically sync to another computer or cloud worker.

See [client setup and discovery paths](docs/clients.md) and the [Windows native / WSL 2 guide](docs/windows.md). Existing desktop and IDE clients can use the skill without installing a terminal edition.

## Use

Set up your local `cetus` SSH alias first using the [SSH guide](skills/cetus-pbs/references/ssh.md). Then open your local experiment repository in your AI client.

In a new session, ask the agent to load `cetus-pbs`. Codex also accepts `$cetus-pbs`; Claude Code accepts `/cetus-pbs`. Give it your experiment details, for example:

> Run a minimal experiment on Cetus using commit `<commit>`, entry point `<command>` and shared dataset `<path/version>`. Freeze the code and configuration, request 1 CPU, 2 GB and 10 minutes, submit through PBS, monitor completion, collect logs and metrics, and check the outputs. Keep AI clients on this local computer.

The skill guides SSH setup, resource sizing, job arrays, immutable snapshots, result collection and individual retries. It includes a [PBS job template](skills/cetus-pbs/assets/job.pbs) and a [complete native-command walkthrough](skills/cetus-pbs/references/pbs.md). Adapt the template's resources and frozen `command.sh` to your workload.

## Verification

Clean-home Linux checks covered real installations of Codex CLI, Claude Code and DeepSeek Harness, automatic detection, repeated installation and skill-body loading. Twenty local regression tests cover installer behavior and the PBS template. The PBS checks simulate the scheduler locally.

Other client paths were checked against official documentation. Their runtime loading, macOS and Windows flows still require testing on those systems. See the [validation record](docs/validation.md) for versions, evidence and limits.
