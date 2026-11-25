# UTS PBS Skills

**English** | [简体中文](README.zh-CN.md)

A reusable skill for operating UTS Cetus with SSH, rsync and native PBS commands. It covers resource sizing, immutable code snapshots, job scripts, bounded job arrays, monitoring, result collection and failed-task recovery.

AI CLIs run on your local workstation. Access Cetus through SSH, and execute computational workloads through PBS. Under the policy supplied for this workflow, AI CLIs must not run on Cetus login or compute nodes.

## Install a local AI CLI

The commands below target a local Ubuntu/Bash workstation. Use the official platform-specific instructions on other operating systems.

### Codex CLI

With a supported Node.js/npm installation:

```bash
npm install -g --prefix "$HOME/.local" @openai/codex
export PATH="$HOME/.local/bin:$PATH"
codex --version
codex login
```

Use `codex login --device-auth` when browser callback login is unavailable. Install the complete official npm package or installer. Copying only a release executable can cause `CLI has no complete local package`.

[Official installation](https://learn.chatgpt.com/docs/codex/cli) · [Authentication](https://learn.chatgpt.com/docs/auth)

### Claude Code

```bash
curl -fsSL https://claude.ai/install.sh -o /tmp/claude-code-install.sh
bash /tmp/claude-code-install.sh
export PATH="$HOME/.local/bin:$PATH"
claude --version
claude auth login
```

Persist the PATH setting in your local shell configuration when necessary. Account access depends on your subscription or provider.

[Official installation](https://code.claude.com/docs/en/setup)

## Automatic skill installation

After cloning, run locally:

```bash
bash scripts/install.sh --client both
# Or choose one client
bash scripts/install.sh --client codex
bash scripts/install.sh --client claude
# Install into an existing research project
bash scripts/install.sh --client both --project /path/to/research-repo
# Update an installed copy, preserving a backup
bash scripts/install.sh --client both --update
```

This script installs the skill files. CLI installation and account authentication follow the instructions above. It refuses common Cetus hostnames and PBS allocations; run it on your own local workstation. Existing skills require explicit --update. Backups are kept in a hidden sibling directory. For a multi-client installation, filesystem failures can leave one client updated before the other; inspect the printed paths before retrying.

## Install the skill

Clone this repository locally:

```bash
git clone git@github.com:ChonghaoCheng/UTS_PBS_Skills.git
cd UTS_PBS_Skills
```

Choose the relevant installation. Inspect or back up an existing destination before copying.

```bash
# Codex, personal scope
mkdir -p "$HOME/.agents/skills"
cp -R skills/cetus-pbs "$HOME/.agents/skills/"

# Claude Code, personal scope
mkdir -p "$HOME/.claude/skills"
cp -R skills/cetus-pbs "$HOME/.claude/skills/"
```

For project scope, copy the same folder to your research repository's `.agents/skills/` for Codex or `.claude/skills/` for Claude Code. Choose one scope per CLI to avoid duplicate versions. Start a new CLI session after installation. Pull this repository and update the installed copy when upgrading.

[Codex skill discovery](https://learn.chatgpt.com/docs/build-skills) · [Claude Code skills](https://code.claude.com/docs/en/skills)

## Configure SSH

Add a local `~/.ssh/config` entry using your own UTS login and approved login node:

```sshconfig
Host cetus
    HostName hpc-login02.hpc.uts.edu.au
    User YOUR_UTS_LOGIN
    IdentityFile ~/.ssh/id_ed25519_cetus
    IdentitiesOnly yes
    ControlMaster auto
    ControlPath ~/.ssh/cetus-%C
    ControlPersist 30m
```

If enrolling a new key, choose an unused filename, set a passphrase and upload only the public key:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_cetus -C "cetus-workstation"
ssh-copy-id -i ~/.ssh/id_ed25519_cetus.pub cetus
ssh-add ~/.ssh/id_ed25519_cetus
ssh -oBatchMode=yes cetus 'hostname; command -v qsub qstat rsync'
```

Verify new host fingerprints through the university's guidance. Use the UTS VPN when required. Each client can keep its own key.

[Cetus SSH guide](https://cetus.hpc.uts.edu.au/getting_started/access_via_ssh/)

## Use

Start the CLI from your local experiment repository. In Codex:

> Use $cetus-pbs. Freeze the specified commit and input version, submit one minimal real workload through SSH/PBS, monitor it to completion, collect logs and metrics, and validate the outputs. Keep all AI CLIs on the local workstation.

In Claude Code:

> /cetus-pbs Prepare a minimal PBS experiment with the specified code, data and parameters. Check resources, preserve the run manifest, collect results and diagnose failures.

Provide the code revision, entry point, dataset path/version, parameters and resource budget. The skill contains instructions and a native PBS script example. Adapt it to the actual workload. It does not install a simulation environment or provide prebuilt submit/status/collect executables.

The [PBS reference](skills/cetus-pbs/references/pbs.md) includes a reusable job script, submission and monitoring commands, bounded arrays, per-attempt outputs and failure handling. [SSH reference](skills/cetus-pbs/references/ssh.md) covers authentication and multiple computers.

Use frozen inputs, unique run IDs and isolated code snapshots. Keep large datasets on shared storage, stage only required shards to scratch, preserve checkpoints and retry failed cases independently. Rules guide agent behavior; review resources and commands before execution.

## Repository layout

```text
README.md
README.zh-CN.md
skills/cetus-pbs/
  SKILL.md
  references/
    ssh.md
    pbs.md
```
