# Windows installation and use

[简体中文](windows.zh-CN.md) · [Back to README](../README.md)

Use a native Windows client or run the client and task files inside WSL 2. Install skills in the environment where the agent runs. Native Windows typically uses `C:\Users\your-name`; WSL has a separate Linux home.

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

Install and authenticate the client using its official setup instructions. See [client compatibility](clients.md) for skill adapters. An existing desktop app or IDE integration can install the skill directly.

The PBS walkthrough uses Bash, SSH and rsync. Native clients should run those commands through local WSL or another configured Bash/rsync environment, or adapt transfers to an available OpenSSH/scp workflow. Windows OpenSSH reads `$HOME\.ssh\config`, while WSL reads its own `~/.ssh/config`; verify the connection in the actual submitting environment.

## WSL 2

Reuse an existing suitable WSL 2 distribution when available. The following is an Ubuntu setup example. From an administrator PowerShell, install it and follow the restart and Linux-user setup prompts:

```powershell
wsl --install -d Ubuntu
wsl -d Ubuntu
```

Then prepare tools inside Ubuntu. These sudo commands install dependencies on your own computer:

```bash
sudo apt-get update
sudo apt-get install -y curl rsync openssh-client
```

Install and sign into the chosen client inside WSL, then run the README installer:

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

Choose a WSL working directory for the actual task and use the SSH settings available in that environment. `cetus` is an example alias. When an IDE uses a WSL remote extension, install the skill inside WSL as well. The AI client stays on your computer; Cetus executes PBS computation.

[Codex WSL](https://learn.chatgpt.com/docs/windows/wsl) · [Claude Windows setup](https://code.claude.com/docs/en/setup) · [Harness](https://github.com/deepseek-ai/deepseek-harness#run) · [Git for Windows](https://gitforwindows.org/)
