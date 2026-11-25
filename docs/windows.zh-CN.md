# Windows 安装与使用

[English](windows.md) · [返回 README](../README.zh-CN.md)

可以使用 Windows 原生客户端，或把客户端和任务文件放在 WSL 2 中。技能安装到客户端运行的那一侧。Windows 的个人目录通常是 `C:\Users\你的用户名`，WSL 使用独立的 Linux home。

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

客户端按其产品官方说明安装和登录，技能适配方式见[客户端兼容性](clients.zh-CN.md)。已有桌面应用或 IDE 扩展时，直接安装技能即可。

本仓库的 PBS 命令示例使用 Bash、SSH 和 rsync。原生客户端应通过本地 WSL 或其他已配置的 Bash/rsync 环境执行这些命令，或由代理改写为可用的 OpenSSH/scp 等价流程。Windows OpenSSH 的 SSH 配置位于 `$HOME\.ssh\config`；WSL 的配置在其自己的 `~/.ssh/config`，应分别验证连接。

## WSL 2

已有适用的 WSL 2 发行版时直接复用。以下以新建 Ubuntu 环境为例，在管理员 PowerShell 中执行，并按提示重启和完成用户创建：

```powershell
wsl --install -d Ubuntu
wsl -d Ubuntu
```

接下来在 Ubuntu 终端中准备工具。sudo 只用于自己电脑的 Ubuntu 系统依赖：

```bash
sudo apt-get update
sudo apt-get install -y curl rsync openssh-client
```

在 WSL 中安装并登录所选客户端，再运行 README 的安装命令：

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

按实际任务选择 WSL 中的工作目录，并在该环境使用已有 SSH 配置或配置所需连接。`cetus` 是示例别名。从 Windows IDE 使用 WSL 远程扩展时，技能也应安装到 WSL 环境。所有 AI 客户端仍在自己的电脑上运行，Cetus 只运行 PBS 计算任务。

[Codex WSL 指南](https://learn.chatgpt.com/docs/windows/wsl) · [Claude Windows 安装](https://code.claude.com/docs/en/setup) · [Harness](https://github.com/deepseek-ai/deepseek-harness#run) · [Git for Windows](https://gitforwindows.org/)
