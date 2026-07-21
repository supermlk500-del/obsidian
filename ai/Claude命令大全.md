# Claude Code 命令大全

> 最后更新：2026-07-15
> 适用版本：Claude Code（CLI / 桌面应用 / Web / IDE 扩展）

---

## 一、启动与 CLI 参数

### 安装

```bash
npm install -g @anthropic-ai/claude-code
```

### 基本启动

```bash
claude                    # 交互式 REPL 模式
claude "你的问题"          # 单次提问（非交互）
claude -p "你的问题"       # Print 模式：只输出结果，不进入 REPL
claude -c                 # 继续上一次会话
claude -r <session-id>    # 恢复指定会话
```

### CLI 常用参数

| 参数 | 说明 |
|------|------|
| `--help`, `-h` | 显示帮助信息 |
| `--version`, `-v` | 显示版本号 |
| `--model`, `-m <model>` | 指定使用的模型（如 `claude-opus-4-8`） |
| `--print`, `-p` | Print 模式：非交互式输出结果后退出 |
| `--continue`, `-c` | 继续上一次会话 |
| `--resume`, `-r <id>` | 恢复指定 session ID 的会话 |
| `--output-format <fmt>` | 输出格式：`text`（默认）、`json`、`stream-json` |
| `--max-turns <n>` | 限制最大对话轮数（非交互模式下有用） |
| `--system-prompt <text>` | 自定义系统提示（仅在 `--print` 模式可用） |
| `--allowedTools <tools>` | 允许使用的工具列表（逗号分隔） |
| `--disallowedTools <tools>` | 禁止使用的工具列表 |
| `--permission-mode <mode>` | 权限模式：`default`、`plan`、`auto-accept` |
| `--dangerously-skip-permissions` | 跳过所有权限提示（**危险，仅限 CI/脚本**） |
| `--verbose` | 显示详细日志 |
| `--no-markdown` | 禁用 Markdown 渲染 |
| `--input-format <fmt>` | 输入格式：`text`（默认）、`stream-json` |
| `--mcp-config <path>` | 指定 MCP 配置文件路径 |
| `--add-dir <path>` | 添加额外的工作目录 |

### 管理子命令

```bash
claude config             # 管理配置（get/set/list/remove）
claude mcp                # 管理 MCP 服务器（add/remove/list）
claude doctor             # 诊断安装与配置问题
claude update             # 更新 Claude Code 到最新版本
claude login              # 登录 Anthropic 账户
claude logout             # 退出登录
```

---

## 二、交互式命令（斜杠命令）

### 会话控制

| 命令 | 说明 |
|------|------|
| `/help` | 显示帮助信息和可用命令 |
| `/quit` 或 `/exit` | 退出 Claude Code |
| `/clear` | 清除当前会话历史 |
| `/compact` | 压缩对话上下文（将之前的对话总结以节省 token） |
| `/cost` | 显示当前会话的 token 使用量和费用 |
| `/config` | 打开配置界面（主题、模型等简单设置） |
| `/doctor` | 诊断安装和配置问题 |
| `/login` | 登录 Anthropic 账户 |
| `/logout` | 退出登录 |
| `/tasks` | 查看后台任务列表和状态 |
| `/workflows` | 查看正在运行的工作流进度 |

### 模型切换

| 命令 | 说明 |
|------|------|
| `/model <name>` | 切换到指定模型 |
| `/opus` | 切换到 Claude Opus 4.8（最强大的推理模型） |
| `/sonnet` | 切换到 Claude Sonnet 5（平衡性能与速度） |
| `/haiku` | 切换到 Claude Haiku 4.5（最快速响应） |
| `/fast` | 切换快速模式（同模型，更快输出；Opus 4.8/4.7 可用） |

### 记忆系统

| 命令 | 说明 |
|------|------|
| `/memory` | 查看和管理 Claude 的记忆 |
| `/remember <内容>` | 明确要求 Claude 记住某些信息 |
| `/forget <内容>` | 要求 Claude 忘记某些信息 |

### 项目初始化

| 命令 | 说明 |
|------|------|
| `/init` | 初始化 CLAUDE.md 文件，自动生成项目文档 |

---

## 三、技能命令（Skills）

技能是可扩展的高级功能，通过 `/` 命令调用。

### 代码质量与审查

| 命令 | 说明 |
|------|------|
| `/code-review` | 审查当前 diff 的代码质量（支持 `--fix` 自动修复、`--comment` 发 PR 评论） |
| `/simplify` | 审查修改的代码，检查复用性、简化和效率，并自动修复 |
| `/security-review` | 对当前分支的更改进行安全审查 |
| `/verify` | 端到端验证代码更改是否真正生效（运行而非仅测试） |

### 代码运行与测试

| 命令 | 说明 |
|------|------|
| `/run` | 启动并运行项目的应用（查看更改是否生效） |

### Git 与 PR

| 命令 | 说明 |
|------|------|
| `/review` | 审查 GitHub Pull Request |

### 研究与探索

| 命令 | 说明 |
|------|------|
| `/deep-research` | 深度研究：多源搜索、交叉验证、生成带引用的报告 |

### API 与开发

| 命令 | 说明 |
|------|------|
| `/claude-api` | Claude API / Anthropic SDK 参考（模型 ID、定价、参数、流式、工具使用等） |

### 配置与自动化

| 命令 | 说明 |
|------|------|
| `/update-config` | 配置 settings.json（Hooks、权限、环境变量等） |
| `/loop [间隔] [命令]` | 按定时间隔运行提示或命令。示例：`/loop 5m /code-review` |
| `/fewer-permission-prompts` | 扫描历史记录，自动添加常用只读命令的白名单以减少权限弹窗 |
| `/keybindings-help` | 自定义键盘快捷键配置 |

### UI / 前端设计

| 命令 | 说明 |
|------|------|
| `/frontend-design` | 创建高质量、生产级的前端界面 |
| `/ui-ux-pro-max` | UI/UX 设计（50+ 风格、161 配色、57 字体配对、25 图表类型等） |
| `/interaction-design` | 微交互、动效设计、过渡动画、用户反馈模式 |
| `/dataviz` | 数据可视化（图表、仪表板、配色方案） |

### 技能管理

| 命令 | 说明 |
|------|------|
| `/find-skills` | 发现和安装新技能 |
| `/skill-creator` | 创建新技能、编辑现有技能、运行评估 |

---

## 四、快捷键

### 输入控制

| 快捷键 | 说明 |
|--------|------|
| `Enter` | 发送消息 |
| `Shift + Enter` | 换行（多行输入） |
| `Escape` | 取消当前输入 / 中断当前操作 |
| `Ctrl + C` | 中断当前操作 |
| `Ctrl + D` | 退出 Claude Code（等同于 `/quit`） |
| `↑` / `↓` | 浏览输入历史 |
| `Tab` | 自动补全文件名和命令 |

### 权限提示时

| 快捷键 | 说明 |
|--------|------|
| `y` | 允许本次操作 |
| `n` | 拒绝本次操作 |
| `a` | 本次会话始终允许此类操作 |

---

## 五、权限模式

Claude Code 有三种权限模式控制工具使用：

| 模式 | 说明 |
|------|------|
| **Default（默认）** | 读取操作自动允许，写入/执行操作每次询问 |
| **Plan（计划）** | 只读模式，Claude 只能分析和提建议，不能修改文件 |
| **Auto-accept（自动接受）** | 自动批准所有操作（谨慎使用） |

### 权限配置文件

可在 `settings.json` 中配置允许/拒绝的工具列表：
```json
{
  "permissions": {
    "allow": ["Bash(npm test)", "Bash(npm run build)"],
    "deny": ["Bash(rm -rf)"]
  }
}
```

---

## 六、上下文引用（IDE 扩展中）

在 VS Code / JetBrains 扩展中，可使用 `#` 引用上下文：

| 引用 | 说明 |
|------|------|
| `#File` | 引用特定文件 |
| `#Folder` | 引用特定文件夹 |
| `#Codebase` | 扫描整个代码库（需要索引） |
| `#Problems` | 查看当前文件的问题 / 诊断 |
| `#Terminal` | 查看终端输出 |
| `#Git Diff` | 查看 Git 差异 |

---

## 七、终端中用户自行运行命令

```
! <command>
```

在 Claude Code 提示符中输入 `!` 前缀可直接运行 shell 命令，输出会直接进入对话上下文。
- 适用于交互式操作（如 `! gcloud auth login`、`! docker login`）
- 输出会成为后续对话的上下文

---

## 八、配置体系

### 配置文件层级（优先级从高到低）

| 位置 | 作用域 | 文件 |
|------|--------|------|
| `<项目>/.claude/settings.json` | 项目级（提交到 Git） | 团队共享配置 |
| `<项目>/.claude/settings.local.json` | 项目级（不提交） | 个人项目配置 |
| `~/.claude/settings.json` | 用户级 | 全局配置 |

### CLAUDE.md 系统

CLAUDE.md 是项目级的指导文件，Claude 会自动读取：

| 位置 | 说明 |
|------|------|
| `项目根目录/CLAUDE.md` | 整个项目的指导规则 |
| `子目录/CLAUDE.md` | 该目录及子目录的特定规则 |
| `~/.claude/CLAUDE.md` | 全局规则（所有项目生效） |

典型内容包括：
- 项目结构说明
- 编码规范和风格要求
- 构建/测试/部署命令
- 技术栈说明
- 常见注意事项

### 记忆系统

记忆文件存储在 `~/.claude/projects/<项目>/memory/` 目录下：

| 记忆类型 | 说明 |
|----------|------|
| `user` | 用户角色、偏好、知识背景 |
| `feedback` | 用户对工作方式的反馈和指导 |
| `project` | 项目目标、进展、决策 |
| `reference` | 外部系统资源、URL、工单 |

记忆会在未来对话中自动加载。

---

## 九、MCP（Model Context Protocol）

MCP 允许 Claude Code 连接外部工具和数据源。

### 配置方式

**CLI 方式：**

```bash
claude mcp add <name> <command> [args...]      # 添加 MCP 服务器
claude mcp add <name> -s user <command>         # 添加到用户级（全局）
claude mcp remove <name>                        # 移除 MCP 服务器
claude mcp list                                 # 列出已配置的服务器
```

**配置文件方式：**

项目级：`.claude/settings.json`
用户级：`~/.claude/settings.json`

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@some/mcp-server"],
      "env": {
        "API_KEY": "your-key"
      }
    }
  }
}
```

---

## 十、Hooks（钩子系统）

Hooks 是在特定事件触发时自动执行的命令，配置在 `settings.json` 中：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": ["echo 'About to run bash command'"]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": ["npx prettier --write $CLAUDE_FILE_PATH"]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": ["notify-send 'Claude' '$CLAUDE_NOTIFICATION'"]
      }
    ]
  }
}
```

### 可用的 Hook 事件

| 事件 | 触发时机 |
|------|----------|
| `PreToolUse` | 工具调用之前 |
| `PostToolUse` | 工具调用之后 |
| `Notification` | 发送通知时 |
| `Stop` | Claude 停止响应时 |

### Hook 环境变量

| 变量 | 说明 |
|------|------|
| `$CLAUDE_FILE_PATH` | 当前操作的文件路径 |
| `$CLAUDE_TOOL_NAME` | 工具名称 |
| `$CLAUDE_NOTIFICATION` | 通知消息内容 |

---

## 十一、Agent 类型

在多代理工作流中，可使用以下 Agent 类型：

| 类型 | 说明 |
|------|------|
| `claude` | 通用代理，适合不属于其他特定类型的任务 |
| `claude-code-guide` | 专门回答 Claude Code / SDK / API 使用问题 |
| `Explore` | 只读搜索代理，适合大范围代码搜索 |
| `general-purpose` | 通用代理，搜索代码和执行多步骤任务 |
| `Plan` | 软件架构师代理，设计实现方案 |
| `code-reviewer` | 代码审查代理 |

---

## 十二、Worktree（工作树）

工作树允许在隔离的 Git 环境中工作：

```
请在工作树中工作 / use a worktree
```

- 自动创建 `.claude/worktrees/` 下的独立分支
- 工作完成后可选择保留或删除
- 适合并行开发、测试危险操作

---

## 十三、环境变量

### 认证相关

| 变量 | 说明 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API 密钥 |
| `ANTHROPIC_AUTH_TOKEN` | 认证令牌（中转站常用） |
| `ANTHROPIC_BASE_URL` | API 基础 URL（中转站/代理地址） |

### 行为控制

| 变量 | 说明 |
|------|------|
| `CLAUDE_CODE_MAX_TURNS` | 限制非交互模式下的最大对话轮数 |
| `CLAUDE_CODE_USE_BEDROCK` | 使用 AWS Bedrock（值为 `1`） |
| `CLAUDE_CODE_USE_VERTEX` | 使用 Google Vertex AI（值为 `1`） |
| `CLAUDE_MODEL` | 覆盖默认模型 |
| `DISABLE_PROMPT_CACHING` | 禁用提示缓存 |
| `HTTP_PROXY` / `HTTPS_PROXY` | HTTP/HTTPS 代理设置 |

### 中转站 / 第三方配置示例

```bash
# Linux / macOS
export ANTHROPIC_AUTH_TOKEN="你的API密钥"
export ANTHROPIC_BASE_URL="https://your-proxy.com"

# 写入配置文件使其永久生效
echo 'export ANTHROPIC_AUTH_TOKEN="你的API密钥"' >> ~/.zshrc
echo 'export ANTHROPIC_BASE_URL="base-url"' >> ~/.zshrc
source ~/.zshrc
```

```powershell
# Windows PowerShell
$env:ANTHROPIC_AUTH_TOKEN = "你的API密钥"
$env:ANTHROPIC_BASE_URL = "https://your-proxy.com"

# 永久设置（用户级）
[Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "你的API密钥", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "base-url", "User")
```

---

## 十四、模型信息

### 最新可用模型（2026年7月）

| 模型 | Model ID | 定位 |
|------|----------|------|
| Claude Fable 5 | `claude-fable-5` | Claude 5 系列 |
| Claude Opus 4.8 | `claude-opus-4-8` | 最强大的推理模型（1M 上下文） |
| Claude Sonnet 5 | `claude-sonnet-5` | 平衡性能与速度 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 最快速、最经济 |

- 知识截止日期：2026年1月
- 构建 AI 应用时建议默认使用最新最强的 Claude 模型
- Fast 模式在 Opus 4.8/4.7 上可用（同模型更快输出，不降级）

---

## 十五、可用平台

| 平台 | 说明 |
|------|------|
| **CLI（命令行）** | `npm install -g @anthropic-ai/claude-code` |
| **桌面应用** | Mac / Windows 原生应用 |
| **Web 应用** | [claude.ai/code](https://claude.ai/code) |
| **VS Code 扩展** | 在 VS Code 中集成使用 |
| **JetBrains 扩展** | 在 IntelliJ / WebStorm 等 IDE 中使用 |

---

## 十六、实用技巧

### 多行输入
- `Shift + Enter` 换行
- 支持粘贴多行文本

### 管道输入
```bash
cat error.log | claude -p "分析这个错误日志"
git diff | claude -p "审查这些代码变更"
echo "解释这段代码" | claude
```

### 与 Git 配合
```bash
# 让 Claude 基于 diff 生成提交信息
git diff --staged | claude -p "为这些更改生成一个中文 commit message"
```

### 图片输入
Claude Code 支持直接读取图片文件（PNG、JPG 等）并进行视觉分析。

### PDF 输入
支持读取 PDF 文件，可指定页码范围（如 `1-5`，每次最多 20 页）。

---

## 十七、常用工作流示例

### 1. 新项目初始化
```
/init                     # 生成 CLAUDE.md
```

### 2. 代码审查流程
```
/code-review              # 审查当前 diff
/code-review --fix        # 审查并自动修复
/code-review --comment    # 审查并发布 PR 评论
/security-review          # 安全审查
```

### 3. 深度研究
```
/deep-research 某个技术主题的深入分析
```

### 4. 前端开发
```
/frontend-design          # 创建前端界面
/dataviz                  # 数据可视化
```

### 5. 查看费用
```
/cost                     # 查看当前会话消耗
```

---

## 十八、问题排查

```bash
claude doctor             # 诊断安装和配置问题
claude --verbose          # 启用详细日志
```

### 常见问题

- **权限提示太多**：使用 `/fewer-permission-prompts` 或在 settings.json 中配置 allow 列表
- **上下文太长**：使用 `/compact` 压缩对话历史
- **模型响应慢**：使用 `/fast` 启用快速模式
- **连接问题**：检查 `ANTHROPIC_BASE_URL` 和代理设置

---

## 反馈与帮助

- GitHub Issues：https://github.com/anthropics/claude-code/issues
- 官方文档：https://docs.anthropic.com/en/docs/claude-code
