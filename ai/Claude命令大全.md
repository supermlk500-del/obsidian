# Claude Code 命令大全

> 最后更新：2026-08-05
> 适用版本：Claude Code（CLI / 桌面应用 / Web / IDE 扩展）

---

## 一、核心基础命令（重点）

### 1. 终端启动与会话管理（CLI 命令行）

在操作系统终端（Terminal / PowerShell / Git Bash）中直接运行：

#### 常用启动命令

| 命令 | 简写 / 缩写 | 完整写法 | 作用说明与适用场景 |
|------|-------------|----------|-------------------|
| **启动会话** | `claude` | `claude` | 进入交互式 REPL 模式（最基础用法） |
| **恢复上次** | `claude -c` | `claude --continue` | **继续上一次会话**（自动载入当前目录最近一次对话历史与上下文） |
| **恢复指定** | `claude -r [id]` | `claude --resume [id/搜索词]` | **恢复历史会话**（若带 ID 则直接恢复；若不带或带搜索词则打开交互选择列表） |
| **命名启动** | `claude -n <名称>` | `claude --name <会话名>` | **直接为新会话命名启动**（名称会同步显示在终端标题与 `/resume` 列表中） |
| **带提示词启动** | `claude "问题"` | `claude "你的问题"` | 进入交互模式并立即自动发送第一条提示词 |
| **单次非交互** | `claude -p "问题"` | `claude --print "你的问题"` | **Print 模式**（生成答案后立即退出终端，不进入交互，适合 Shell 脚本/管道） |
| **指定模型启动** | `claude -m <模型>` | `claude --model <model>` | 指定启动模型（如 `claude -m opus` 或 `claude -m sonnet`） |
| **后台 Agent 启动** | `claude --bg "任务"` | `claude --background "任务"` | **后台运行模式**（启动异步 Agent 执行任务并立即返回终端） |
| **Git 隔离工作树** | `claude -w [名称]` | `claude --worktree [name]` | **在独立 Git Worktree 中启动**（防止对当前主工作区造成污染） |

---

#### CLI 管理子命令

| 子命令 | 命令语法 | 作用说明与使用示例 |
|--------|----------|-------------------|
| **配置管理** | `claude config` | 查看、获取、设置或删除全局与项目配置 |
| **环境诊断** | `claude doctor` | 健康检查（排查 Node 版本、网络连接、API 密钥、代理、权限等） |
| **软件升级** | `claude update` | 将 Claude Code CLI 升级到最新版本（或 `claude upgrade`） |
| **后台 Agent 管理** | `claude agents` | 列出与管理后台运行的 Agent 任务（支持 `--json` 查看结构化列表） |
| **MCP 服务器管理** | `claude mcp` | 管理 MCP 扩展工具服务器（下有 `list`/`add`/`remove`/`login` 等子命令） |
| **插件生态管理** | `claude plugin` | 管理社区与本地插件（下有 `list`/`install`/`uninstall`/`enable` 等子命令） |
| **多 Agent 云端审查** | `claude ultrareview` | 针对当前分支或 PR 运行云端多 Agent 深度代码审查 |
| **外部配置导入** | `claude import` | 自动从 Cursor / Trae 等其他 AI 工具中导入配置 |
| **账号认证管理** | `claude auth` | 管理登录与凭证（`claude login` 登录 / `claude logout` 退出） |

---

#### 常用 CLI 高级参数标志（Flags）

| 参数标志 | 缩写 / 示例 | 说明与适用场景 |
|----------|-------------|----------------|
| `--name <name>` | `-n "修复登录Bug"` | 设置会话自定义显示名称 |
| `--effort <level>` | `--effort high` | 设置推理思考深度（可选：`low`, `medium`, `high`, `xhigh`, `max`） |
| `--permission-mode <mode>` | `--permission-mode auto` | 设置权限询问模式（`manual`, `auto`, `acceptEdits`, `dontAsk`, `plan`, `bypassPermissions`） |
| `--dangerously-skip-permissions` | `--dangerously-skip-permissions` | **跳过所有权限询问弹窗**（极其危险！仅限在安全隔离的 CI/CD 容器中使用） |
| `--allowedTools <tools>` | `--allowedTools "Bash(git *),Read"` | 允许使用的工具白名单（支持正则模糊匹配） |
| `--disallowedTools <tools>` | `--disallowedTools "Edit,Write"` | 禁止使用的工具黑名单 |
| `--safe-mode` | `--safe-mode` | **故障排查模式**：禁用所有 CLAUDE.md、技能、插件和 MCP 服务器，纯干净启动 |
| `--bare` | `--bare` | **极简模式**：跳过钩子、LSP、自动记忆和 CLAUDE.md，适合纯自动化脚本 |
| `--max-budget-usd <amount>` | `--max-budget-usd 5.0` | 设置本次运行的消费上限金额（美元），超限自动停止（结合 `-p` 使用） |
| `--mcp-config <path>` | `--mcp-config ./mcp.json` | 额外指定加载的 MCP 服务器配置文件 |
| `--add-dir <path>` | `--add-dir ../other-project` | 额外引入并授权 Claude 访问的其他项目目录 |
| `--output-format <format>` | `--output-format json` | 指定输出格式（仅限 `-p` 模式：`text`, `json`, `stream-json`） |
| `--max-turns <n>` | `--max-turns 10` | 限制最大对话轮数，防止脚本无限循环 |
| `--verbose` | `--verbose` | 开启详细调试日志输出 |

---

### 2. 会话内部斜杠命令（REPL 实时控制命令）

在 `claude` 交互式会话界面中，在输入框中以 `/` 开头输入：

#### 基础会话与控制

| 斜杠命令 | 语法示例 | 作用与使用场景 |
|----------|----------|----------------|
| `/help` | `/help` | 显示帮助菜单、快捷键及当前可用命令列表 |
| `/clear` | `/clear` | **清空当前会话**（重置上下文历史，开启新对话，不退出应用） |
| `/compact` | `/compact` | **压缩/总结上下文**（对话太长消耗 token 时，让 Claude 总结前期对话并释放窗口） |
| `/resume` | `/resume [id]` | **恢复/切换会话**（在会话内交互式选择或直接恢复指定的历史对话） |
| `/rename` | `/rename <新名称>` | **重命名当前会话**（修改当前 Session 的显示名称，在标签页与历史恢复列表中生效） |
| `/cost` | `/cost` | **查看 Token 消耗与费用**（显示当前 Session 的 Input/Output Token 数及预估金额） |
| `/config` | `/config` | **交互式设置界面**（实时调整主题、模型、提示方式、权限等） |
| `/quit` 或 `/exit` | `/quit` | **退出 Claude Code** |
| `/doctor` | `/doctor` | 在会话内实时运行环境与网络健康诊断 |
| `/bug` | `/bug` | 向 Anthropic 提交 Bug 反馈 |

#### 模型与性能切换

| 斜杠命令 | 语法 / 示例 | 作用说明与适用场景 |
|----------|-------------|-------------------|
| `/model` | `/model` | **查看与选择模型**：打开交互式模型与推理强度（Effort）选择菜单 |
| `/model <名称>` | `/model opus`<br>`/model sonnet`<br>`/model haiku`<br>`/model <model-id>` | **直接切换模型**：快速指定切换到目标模型（如 `opus`、`sonnet`、`haiku` 或具体模型 ID） |
| `/fast` | `/fast` | **Fast Mode（快速模式）**：切换 Fast 极速输出模式（开启/关闭切换） |

#### 任务、工具与隔离环境

| 斜杠命令 | 作用说明 |
|----------|----------|
| `/init` | **生成 `CLAUDE.md`**（自动分析代码库并创建项目规范与说明文件） |
| `/tasks` | **查看后台任务**（查看正在后台运行的 Agent、Shell 进程或自动化任务状态） |
| `/workflows` | **查看工作流**（查看正在运行的多 Agent 编排工作流进度） |
| `/worktree` | **创建 Git 工作树**（在隔离的 Git Worktree 中进行试验性开发，不污染主分支） |
| `/mcp` | **管理 MCP 服务**（在会话内查看或重新连接外部 MCP 工具服务器） |
| `/memory` | **查看与管理记忆**（打开保存的持久记忆文件） |
| `/remember <内容>` | 强制 Claude 记住规则或偏好（写回项目/用户持久记忆） |
| `/forget <内容>` | 删除指定的历史记忆 |

---

### 3. 会话内输入技巧与按键

#### 对话输入快捷键

- `Enter`：发送消息
- `Shift + Enter`：**换行**（多行输入）
- `Ctrl + C`：**中断/取消**当前操作或代码生成
- `Ctrl + D`：**快速退出**（等同于 `/quit`）
- `Escape`：取消当前输入 / 中断运行
- `↑` / `↓`：翻阅历史输入的命令
- `Tab`：补全文件名、路径、命令

#### 权限询问控制（弹窗时按键）

当 Claude 尝试编辑文件或运行 Shell 命令提示确认时：
- `y`：同意本次执行
- `n`：拒绝本次执行
- `a`：**本次会话内始终允许**同类操作（如以后允许所有读取/写入）

#### 在对话中执行本地命令 (`!`)

在提示符中输入 `!` 开头的命令直接运行 Shell，结果自动作为上下文交给 Claude：
```bash
! git status                  # 查看代码状态
! npm test                    # 运行单元测试
! gcloud auth login           # 交互式登录认证
```

#### 管道处理文本 (Pipeline)

```bash
cat build.log | claude -p "分析构建失败的原因"
git diff | claude -p "生成 Git 提交日志"
```

#### IDE 扩展中的上下文引用标记 (`#`)

在 IDE 插件 / 扩展中使用：
- `#File` / `#Folder`：引用指定文件/文件夹
- `#Codebase`：全项目索引检索
- `#Problems`：引用 IDE 诊断面板中的报错和 Warning
- `#Terminal`：引用 IDE 内置终端输出
- `#Git Diff`：引用未提交的代码变更

---

## 二、高级扩展技能与插件命令（Skills & Plugins）

通过 `/技能名` 或 `claude plugin` 调用的增强扩展功能：

### 1. 常用扩展技能（Skills）

| 技能命令 | 类别 | 作用说明 |
|----------|------|----------|
| `/code-review` | 代码质量 | 审查当前代码改动（支持 `--fix` 自动修复、`--comment` 发布 PR 评论） |
| `/simplify` | 代码质量 | 审查并精简代码，重构冗余逻辑，提升执行效率 |
| `/security-review` | 代码质量 | 针对代码改动进行安全漏洞扫描与防御审查 |
| `/verify` | 开发调试 | 端到端运行并驱动应用程序，验证改动是否真正生效 |
| `/run` | 开发调试 | 自动识别并启动当前项目的 App / 开发服务器 |
| `/loop [间隔] [命令]` | 自动化 | 循环定时运行（如 `/loop 5m /code-review` 每 5 分钟自动审核） |
| `/fewer-permission-prompts` | 配置优化 | 扫描历史记录，自动生成白名单配置以减少频繁弹窗 |
| `/keybindings-help` | 配置优化 | 配置自定义快捷键绑定 |
| `/deep-research <主题>` | 检索研究 | 启动多源并发联网搜索与交叉验证，生成带参考文献的专业报告 |
| `/claude-api` | 检索研究 | 查询 Anthropic API / SDK 最新开发参考手册（参数、模型 ID、流式传输等） |
| `/frontend-design` | 前端设计 | 生产级前端页面与组件设计与代码生成 |
| `/ui-ux-pro-max` | 前端设计 | 包含 50+ 风格、161 配色的 UI/UX 全套设计指南 |
| `/dataviz` | 前端设计 | 专业图表、仪表板与数据可视化设计 |
| `/interaction-design` | 前端设计 | 微交互、动效与过渡动画设计 |
| `/find-skills` | 技能管理 | 查找并安装社区与本地新技能 |
| `/skill-creator` | 技能管理 | 创建新技能、编辑技能及测试评估 |

---

### 2. CLI 插件管理常用命令（`claude plugin`）

```bash
claude plugin list                 # 列出已安装的所有插件
claude plugin install <名称>       # 从 Marketplace 安装指定插件
claude plugin uninstall <名称>     # 卸载已安装的插件
claude plugin enable <名称>        # 启用插件
claude plugin disable <名称>       # 禁用插件
claude plugin update <名称>        # 升级插件至最新版本
claude plugin init <名称>          # 脚手架初始化新建一个本地插件
```

---

### 3. MCP 工具服务常用命令（`claude mcp`）

```bash
claude mcp list                    # 查看当前配置的所有 MCP 服务器
claude mcp add <名称> <命令/URL>    # 添加新的 MCP 服务器（支持 stdio 和 HTTP/SSE）
claude mcp remove <名称>           # 移除 MCP 服务器
claude mcp get <名称>              # 查看指定 MCP 服务器的健康状态与详细信息
claude mcp login <名称>            # 为需要 OAuth 认证的 MCP 服务登录鉴权
```

---

## 三、配置与架构规范

### 1. CLAUDE.md 项目规范文件

- **位置**：`<项目根目录>/CLAUDE.md` 或 `~/.claude/CLAUDE.md`（全局）
- **作用**：让 Claude 启动即了解项目背景、规范、构建命令与约束条件

### 2. 配置层级（优先级从高到低）

1. `<项目>/.claude/settings.local.json` （本地个人配置，不提交 git）
2. `<项目>/.claude/settings.json` （项目共享配置，提交 git）
3. `~/.claude/settings.json` （全局用户配置）

---

## 四、环境变量配置（代理与中转站）

### Linux / macOS (`~/.zshrc` 或 `~/.bashrc`)
```bash
export ANTHROPIC_AUTH_TOKEN="你的API密钥"
export ANTHROPIC_BASE_URL="https://your-proxy-domain.com"
```

### Windows PowerShell
```powershell
$env:ANTHROPIC_AUTH_TOKEN = "你的API密钥"
$env:ANTHROPIC_BASE_URL = "https://your-proxy-domain.com"

# 永久写入系统用户变量
[Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "你的API密钥", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "https://your-proxy-domain.com", "User")
```
