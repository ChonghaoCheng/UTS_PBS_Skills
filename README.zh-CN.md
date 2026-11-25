# UTS PBS Skills

[English](README.md) · **简体中文**

面向 UTS Cetus 的 Agent Skill，提供 SSH 接入、PBS 资源配置、任务提交、状态监控、结果回收及失败任务重跑的操作规程与脚本模板。适用于支持 Agent Skills、能够访问文件和调用终端工具的桌面应用、IDE 助手及终端客户端。

AI 客户端运行在本地工作站。Cetus 登录节点负责文件传输、轻量检查和调度操作；仿真、训练及其他计算密集型任务通过 PBS 在计算节点执行。

## 环境要求

- 技能安装需要 Bash、curl 和 tar。
- 实验工作流使用 Git、SSH、rsync 和 Python 3，并要求具备有效的 Cetus 账号及网络访问权限。
- 技能安装到代理实际执行命令的环境。Windows 原生客户端与 WSL 使用各自的个人目录，具体步骤见 [Windows 安装指南](docs/windows.zh-CN.md)。

## 安装技能

在本地终端执行：

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash
```

默认模式优先根据环境变量识别当前 Codex 或 Claude 会话，否则检测 PATH 中支持的客户端命令。未检测到客户端时，脚本返回错误并提示显式选择。

桌面应用、IDE 助手或通过 `npx` 启动的客户端可以显式指定安装目标：

```bash
curl -fsSL https://raw.githubusercontent.com/ChonghaoCheng/UTS_PBS_Skills/main/scripts/install.sh | bash -s -- --client codex
```

`--client` 支持 `codex`、`claude`、`dsh`、`cursor`、`copilot`、`gemini` 和 `opencode`。客户端发现路径及使用界面见[兼容性说明](docs/clients.zh-CN.md)。

从源码安装时：

```bash
git clone https://github.com/ChonghaoCheng/UTS_PBS_Skills.git
cd UTS_PBS_Skills
bash scripts/install.sh --client codex
```

| 参数 | 行为 |
| --- | --- |
| 无参数或 `--client auto` | 自动选择客户端，默认安装到个人技能目录 |
| `--client NAME` | 安装到指定客户端的技能目录 |
| `--client all` | 为全部七个内置适配器安装技能 |
| `--project PATH` | 安装到已存在的项目目录，可与 `--client` 配合使用 |
| `--skills-dir PATH` | 指定其他宿主的技能目录，单独使用，不与 `--client`、`--project` 混用 |
| `--help` | 输出完整参数说明 |

安装器输出 `SKILL.md` 的实际路径。重复安装时，内容一致则跳过，有变化则先备份再替换。技能文件应完整保留 `references/` 和 `assets/`。安装完成后开启新的代理会话。

也可以将以下指令交给当前助手执行：

> 阅读 https://github.com/ChonghaoCheng/UTS_PBS_Skills ，在本地为当前客户端安装 cetus-pbs。检查安装脚本，选择对应适配器或官方技能目录，执行安装并报告实际路径和调用方式。

## 执行实验

先按 [SSH 接入指南](skills/cetus-pbs/references/ssh.md) 配置本地 `cetus` 别名，再在客户端中打开实验仓库并加载 `cetus-pbs`。Codex 可使用 `$cetus-pbs`，Claude Code 可使用 `/cetus-pbs`；其他客户端按其技能调用机制加载。

提交任务时提供代码版本、启动命令、数据版本、资源需求和输出要求。例如：

```text
使用 cetus-pbs 执行一次最小实验。
仓库：<本地仓库路径>
代码版本：<Git commit>
启动命令：<入口及完整参数>
输入数据：<共享目录中的版本化路径及校验值>
PBS 资源：select=1:ncpus=1:mem=2gb，walltime=00:10:00
预期输出：<指标文件、结果文件及判断标准>

冻结代码和配置后提交一次，监控至任务结束，回收日志和指标，
记录 run_id、PBS Job ID、数据版本、时间及退出状态，并分析失败原因。
```

上述资源仅用于最小实验示例。正式任务应根据实测 CPU、内存、运行时间及当前队列限制配置。

## 执行约束

- 每次实验使用独立的 `run_id`、代码快照、配置和输出目录，排队任务与后续代码修改隔离。
- 记录 Git commit、参数、数据标识及校验值、PBS Job ID、起止时间、退出状态和结果文件。
- 独立种子或参数扫描使用带并发上限的 Job Array，各索引和重试分别保存输出。
- 提交后保存调度器回执，状态查询设置间隔和截止时间。连接中断或任务记录缺失时，先核对调度器和已有回执，再决定后续操作。
- 失败任务保留原始日志，仅对已定位的失败项创建新运行，并记录父运行与任务索引。
- 删除任务或覆盖实验结果前必须获得用户确认。禁止循环提交任务，禁止在 Cetus 登录节点或计算节点运行 AI 客户端。

## 文档与模板

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](skills/cetus-pbs/SKILL.md) | 技能入口与执行规约 |
| [SSH 接入](skills/cetus-pbs/references/ssh.md) | SSH 配置、密钥认证和连接诊断 |
| [PBS 工作流](skills/cetus-pbs/references/pbs.md) | 代码冻结、提交、任务数组、监控及结果回收 |
| [job.pbs](skills/cetus-pbs/assets/job.pbs) | 可复用的 PBS 作业模板 |
| [客户端兼容性](docs/clients.zh-CN.md) | 宿主适配与技能发现方式 |
| [Windows 指南](docs/windows.zh-CN.md) | Windows 原生与 WSL 2 的安装和使用 |
