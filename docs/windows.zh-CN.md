# Windows 安装与使用

[English](windows.md) · [返回 README](../README.zh-CN.md)

可以使用 Windows 原生客户端，或把客户端和实验仓库放在 WSL 2 中。技能安装到客户端运行的那一侧。Windows 的个人目录通常是 `C:\Users\你的用户名`，WSL 使用独立的 Linux home。

## Windows 原生客户端

Codex 桌面应用、Cursor、VS Code Copilot 等已安装时，可直接安装技能。使用本仓库自动安装器需要 Git for Windows 提供的 Git Bash。Git 默认安装路径为 `C:\Program Files\Git\bin\bash.exe`，自定义安装位置需调整下面命令。

在 PowerShell 执行，示例选择 Codex：

```powershell
$gitBash = Join-Path $env:ProgramFiles 'Git\bin\bash.exe'
if (-not (Test-Path $gitBash)) { throw '请安装 Git for Windows，或填写正确的 Git Bash 路径。' }
& $gitBash -lc 'curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash -s -- --client codex'
if ($LASTEXITCODE -ne 0) { throw '技能安装失败，请检查上面的输出。' }
```

按客户端替换 `--client codex`，例如 `claude`、`dsh`、`cursor`、`copilot`、`gemini`、`opencode`。从 Git Bash 启动时 Windows 桌面应用的会话标记可能不存在，显式指定最稳妥。检查输出路径是否位于自己的 Windows 个人目录，完成后重开客户端会话。

如果需要安装终端客户端，先安装支持的 Node.js。实测的 Harness 0.2.2-rc.5 要求 Node.js ≥24.9.0，安装其他版本时应核对其要求，本次使用 Node 24.22.3。然后在 PowerShell 运行所需的命令：

```powershell
# Codex
npm.cmd install -g @openai/codex
codex --version
codex login

# Claude Code 官方 Windows 安装器
irm https://claude.ai/install.ps1 | iex
# 安装后新开终端，再执行
claude --version
claude auth login

# DeepSeek Harness 本地 Web 界面
npx.cmd @deepseek-ai/dsh web
```

账号登录在各客户端中完成。IDE 助手按其产品官方说明安装并登录，无需额外安装同名终端程序才能使用技能。

本仓库的 PBS 命令示例使用 Bash、SSH 和 rsync。原生客户端应通过本地 WSL 或其他已配置的 Bash/rsync 环境执行这些命令，或由代理改写为可用的 OpenSSH/scp 等价流程。Windows OpenSSH 的 SSH 配置位于 `$HOME\.ssh\config`；WSL 的配置在其自己的 `~/.ssh/config`，应分别验证连接。

## WSL 2

需要完整 Linux 工具链时，可在管理员 PowerShell 中安装 WSL，然后按提示重启并完成 Ubuntu 用户创建：

```powershell
wsl --install -d Ubuntu
wsl -d Ubuntu
```

接下来在 Ubuntu 终端中准备工具。sudo 只用于自己电脑的 Ubuntu 系统依赖：

```bash
sudo apt-get update
sudo apt-get install -y git curl rsync openssh-client
```

在 WSL 中安装并登录所选客户端，再运行 README 的安装命令：

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

建议把实验仓库放在 WSL 的 `~/research/`，并在 WSL 内配置 `ssh cetus`。从 Windows IDE 使用 WSL 远程扩展时，技能也应安装到 WSL 环境。所有 AI 客户端仍在自己的电脑上运行，Cetus 只运行 PBS 计算任务。

## 验证范围

这些 Windows 步骤依据官方文档整理。当前验证环境是隔离 Linux，原生 Windows 与 WSL 2 的交互流程还需在对应系统上验证；Linux 加载成功不会自动证明 Windows 应用已加载。

[Codex WSL 指南](https://learn.chatgpt.com/docs/windows/wsl) · [Claude Windows 安装](https://code.claude.com/docs/en/setup) · [Harness](https://github.com/deepseek-ai/deepseek-harness#run) · [Git for Windows](https://gitforwindows.org/)
