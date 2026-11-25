# Windows installation and use

[简体中文](windows.zh-CN.md) · [Back to README](../README.md)

Use a native Windows client or run the client and experiment checkout inside WSL 2. Install skills in the environment where the agent runs. Native Windows typically uses `C:\Users\your-name`; WSL has a separate Linux home.

## Native Windows clients

An existing Codex desktop app, Cursor or VS Code Copilot can use the skill without a separate terminal client. The automatic Bash installer requires Git Bash from Git for Windows. Adjust the executable path if Git was installed outside its default location.

Run in PowerShell, selecting Codex in this example:

```powershell
$gitBash = Join-Path $env:ProgramFiles 'Git\bin\bash.exe'
if (-not (Test-Path $gitBash)) { throw 'Install Git for Windows or set the correct Git Bash path.' }
& $gitBash -lc 'curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash -s -- --client codex'
if ($LASTEXITCODE -ne 0) { throw 'Skill installation failed; inspect the output above.' }
```

Choose `claude`, `dsh`, `cursor`, `copilot`, `gemini` or `opencode` for other adapters. Desktop session markers may be absent in Git Bash, so explicit selection is reliable. Verify the printed destination is in your Windows user directory, then reopen the client session.

To set up a terminal client, first install a supported Node.js version. The tested Harness 0.2.2-rc.5 release requires Node.js ≥24.9.0; check the requirement of the version you install. The validation used Node 24.22.3. Run only the relevant commands in PowerShell:

```powershell
# Codex
npm.cmd install -g @openai/codex
codex --version
codex login

# Claude Code official Windows installer
irm https://claude.ai/install.ps1 | iex
# Open a new terminal after installation
claude --version
claude auth login

# DeepSeek Harness local Web UI
npx.cmd @deepseek-ai/dsh web
```

Authenticate through the respective client. Follow the product's setup instructions for IDE integrations; they do not require the terminal edition merely to load skills.

The PBS walkthrough uses Bash, SSH and rsync. Native clients should run those commands through local WSL or another configured Bash/rsync environment, or adapt transfers to an available OpenSSH/scp workflow. Windows OpenSSH reads `$HOME\.ssh\config`, while WSL reads its own `~/.ssh/config`; verify the connection in the actual submitting environment.

## WSL 2

From an administrator PowerShell, install Ubuntu and follow the restart and Linux-user setup prompts:

```powershell
wsl --install -d Ubuntu
wsl -d Ubuntu
```

Then prepare tools inside Ubuntu. These sudo commands install dependencies on your own computer:

```bash
sudo apt-get update
sudo apt-get install -y git curl rsync openssh-client
```

Install and sign into the chosen client inside WSL, then run the README installer:

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

Keep the research checkout under WSL's `~/research/` and configure `ssh cetus` there. When an IDE uses a WSL remote extension, install the skill inside WSL as well. The AI client stays on your computer; Cetus executes PBS computation.

## Verification scope

These Windows steps follow official documentation. Native Windows and WSL 2 interactive flows have not been run in the isolated Linux test environment. Linux loading results do not establish that a Windows app has loaded the skill.

[Codex WSL](https://learn.chatgpt.com/docs/windows/wsl) · [Claude Windows setup](https://code.claude.com/docs/en/setup) · [Harness](https://github.com/deepseek-ai/deepseek-harness#run) · [Git for Windows](https://gitforwindows.org/)
