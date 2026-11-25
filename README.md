# UTS PBS Skills

**English** · [简体中文](README.zh-CN.md)

Give Codex, Claude Code or DeepSeek Harness a reusable workflow for UTS Cetus. Your AI assistant works locally, submits computation through SSH and PBS, monitors jobs, and brings back logs and results.

**Run AI clients on your local computer. All simulation, training and other research computation runs in PBS jobs.**

## Install

Run this on your local Linux or macOS workstation with Bash, curl and tar available:

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

The installer selects the active Codex or Claude session when its environment identifies it. Otherwise it detects `codex`, `claude` and `dsh` on PATH and installs for the clients it finds. It prints the installed `SKILL.md` paths. Running it again skips identical files and backs up changed copies before updating them.

For desktop clients or an `npx` Harness session, select the client explicitly:

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash -s -- --client codex
```

Use `--client claude`, `--client dsh` or `--client all` as needed. The installer installs the skill in your personal client directory. Open a new session after installation.

You can also ask your agent to install it:

> Read https://github.com/ChonghaoCheng/UTS_PBS_Skills and install its cetus-pbs skill for the client you are running in, on this local computer. Run the installer, verify the installed files, and tell me how to invoke it.

To inspect the source or install into a project:

```bash
git clone https://github.com/ChonghaoCheng/UTS_PBS_Skills.git
cd UTS_PBS_Skills
bash scripts/install.sh --client codex --project /path/to/your/project
```

## Use

Set up your local `cetus` SSH alias first using the [SSH guide](skills/cetus-pbs/references/ssh.md). Then open your local experiment repository in your AI client.

| Client | Start using the skill |
| --- | --- |
| Codex | `Use $cetus-pbs to prepare and run my experiment.` |
| Claude Code | `/cetus-pbs Prepare and run my experiment.` |
| DeepSeek Harness | Ask it to load the `cetus-pbs` skill and prepare your experiment. |

For example:

> Run a minimal experiment on Cetus using commit `<commit>`, entry point `<command>` and shared dataset `<path/version>`. Freeze the code and configuration, request 1 CPU, 2 GB and 10 minutes, submit through PBS, monitor completion, collect logs and metrics, and check the outputs. Keep AI clients on this local computer.

The skill guides SSH setup, resource sizing, job arrays, immutable snapshots, result collection and individual retries. It includes a [PBS job template](skills/cetus-pbs/assets/job.pbs) and a [complete native-command walkthrough](skills/cetus-pbs/references/pbs.md). Adapt the template's resources and frozen `command.sh` to your workload.

## Client setup and install locations

Already have a client? The skill installation above is sufficient. To set up a new client locally:

| Client | Install or launch | Sign in |
| --- | --- | --- |
| Codex, with supported Node.js/npm | `npm install -g --prefix "$HOME/.local" @openai/codex` | `codex login` |
| Claude Code | `curl -fsSL https://claude.ai/install.sh \| bash` | `claude auth login` |
| DeepSeek Harness, with Node.js | `npx @deepseek-ai/dsh web` | Configure the provider in the local Web UI. |

For installations under `~/.local/bin`, add it to your local PATH if necessary with `export PATH="$HOME/.local/bin:$PATH"`. Use the complete official Codex package. A single copied executable can lack the files required for interactive startup. Harness starts a local Web UI; it is not a terminal chat interface.

| Client | Personal skill directory | Project skill directory |
| --- | --- | --- |
| Codex | `~/.agents/skills/cetus-pbs/` | `.agents/skills/cetus-pbs/` |
| Claude Code | `~/.claude/skills/cetus-pbs/` | `.claude/skills/cetus-pbs/` |
| DeepSeek Harness | `~/.dsh/skills/cetus-pbs/` | `.dsh/skills/cetus-pbs/` |

Personal installs honor `CLAUDE_CONFIG_DIR` and `DSH_HOME`. Backups live in `skill-backups/` alongside the corresponding `skills/` directory. Client plugins that set their own skill roots may need manual installation into those roots. Each client is installed independently; if a multi-client installation fails partway, rerun after fixing the reported error.

[Codex CLI](https://learn.chatgpt.com/docs/codex/cli) · [Codex skills](https://learn.chatgpt.com/docs/build-skills) · [Claude Code](https://code.claude.com/docs/en/setup) · [Claude skills](https://code.claude.com/docs/en/skills) · [Harness setup](https://github.com/deepseek-ai/deepseek-harness#run) · [Harness skills](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)
