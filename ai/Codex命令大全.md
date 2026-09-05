# Codex CLI 命令大全

> 最后更新：2026-08-14  
> 运行环境：WSL (Windows Subsystem for Linux)  
> 适用版本：Codex CLI

---

## 一、历史对话查看与管理（重点常用）

### 1. 终端命令行查看与恢复历史对话

在 WSL 终端中直接通过命令行查看或恢复历史对话：

| 命令 | 缩写/语法 | 作用说明与适用场景 |
|------|-----------|-------------------|
| **列出所有历史会话** | `codex sessions`<br>`codex session list` | 查看本地保存的所有历史对话会话列表（显示 Session ID、时间、项目路径等） |
| **交互式恢复历史对话** | `codex resume`<br>`codex -r` | **（最推荐）** 打开交互式列表选择并继续之前的历史会话 |
| **指定恢复特定会话** | `codex resume <session-id>`<br>`codex -r <session-id>` | 通过指定的 Session ID 或名称直接恢复特定的历史对话 |
| **继续上次当前项目对话** | `codex -c`<br>`codex --continue` | 快速恢复当前目录下最近一次的对话上下文 |
| **查看历史输入/指令日志** | `codex history` | 打印当前或历史在终端中输入的指令记录 |

---

### 2. 会话内部斜杠命令（在运行中查看）

在 `codex` 交互界面内部，输入以下斜杠命令：

| 斜杠命令 | 作用与使用场景 |
|----------|----------------|
| `/history` | **在当前会话窗口中打印查看历史对话记录与上下文** |
| `/resume` 或 `/sessions` | **在会话内部直接弹出历史对话列表**，可选择切换或恢复其他历史会话 |

---

### 3. WSL 本地文件存储路径直接查看

Codex 在 WSL 本地以 JSONL / 文件形式保存了完整的对话日志，可以直接通过 Shell 工具查阅：

- **历史会话存储目录**：`~/.codex/sessions/` 或 `~/.config/codex/sessions/`
- **历史输入日志文件**：`~/.codex/history.jsonl`

**WSL 查看常用 Shell 命令**：
```bash
# 1. 查看保存的历史 Session 文件列表（按修改时间倒序）
ls -lt ~/.codex/sessions/

# 2. 查阅历史输入的命令与对话日志
cat ~/.codex/history.jsonl | tail -n 30

# 3. 使用 jq 格式化查看详细的历史 JSONL 会话
jq . ~/.codex/sessions/<session-id>.json
```

---

## 二、核心基础命令（CLI 命令行）

在 WSL 终端（Bash / Zsh）中直接运行：

### 1. 常用启动与会话命令

| 命令 | 完整写法 / 缩写 | 作用说明与适用场景 |
|------|------------------|-------------------|
| **启动交互界面** | `codex` | 进入 Codex 交互式 TUI 终端界面（最常用模式） |
| **单次提问/非交互** | `codex "提示词"` 或 `codex exec "提示词"` | 传入提示词自动执行并输出结果，不保持交互 |
| **继续上次会话** | `codex resume` 或 `codex -c` | 恢复上一次在当前项目中的对话上下文 |
| **恢复指定历史** | `codex resume <id>` 或 `codex -r <id>` | 恢复指定的历史会话 |
| **指定模型启动** | `codex -m <model>` 或 `codex --model <model>` | 指定调用的模型（如 `codex -m o3-mini` 或 `codex -m gpt-4o`） |
| **指定工作目录** | `codex -C <dir>` 或 `codex --cd <dir>` | 切换到指定目录并启动 Codex |
| **只读/安全模式** | `codex --read-only` | 以只读模式启动（禁止修改文件及运行高危命令） |

---

### 2. CLI 管理子命令

| 子命令 | 命令语法 | 作用说明与使用示例 |
|--------|----------|-------------------|
| **查看历史会话列表** | `codex session list` / `codex sessions` | 列出本地所有历史会话 ID、创建时间及关联项目 |
| **登录与认证** | `codex auth login` / `codex login` | 登录 OpenAI 账号或配置 API Key 鉴权 |
| **配置管理** | `codex config` | 查看与修改本地 Codex 配置 |
| **健康诊断** | `codex doctor` | 检查 WSL 环境、网络连通性及依赖项状态 |
| **软件更新** | `codex update` | 升级 Codex CLI 至最新版本 |
| **MCP 扩展管理** | `codex mcp list` / `codex mcp add` | 管理 Model Context Protocol (MCP) 服务器 |

---

### 3. 常用标志参数 (Flags)

| 参数标志 | 缩写/示例 | 说明与适用场景 |
|----------|-----------|----------------|
| `--approval-mode <mode>` | `--approval-mode auto` | 自动/手动确认文件修改及 Shell 命令 |
| `--full-auto` / `-y` | `codex -y "分析项目"` | 开启无阻碍自动执行模式（自动同意所有读写与命令） |
| `--model <name>` | `-m gpt-4o` | 指定本次使用的 AI 模型 |
| `--config <path>` | `--config ./codex.json` | 加载自定义配置文件 |
| `--system-prompt <text>` | `--system-prompt "..."` | 注入自定义系统级 Prompt |
| `--verbose` | `-v` / `--verbose` | 开启调试模式，查看详细日志输出 |

---

## 三、会话内部斜杠命令（TUI 交互模式控制）

在运行 `codex` 进入交互界面后，在输入框中以 `/` 开头输入：

| 斜杠命令 | 作用说明与使用场景 |
|----------|--------------------|
| `/history` | **查看/打印当前与历史对话记录** |
| `/resume` 或 `/sessions` | **在会话内部直接调出历史对话列表并切换/恢复** |
| `/help` | 显示帮助菜单与所有可用的命令 |
| `/clear` | 清空当前对话上下文与历史记录 |
| `/compact` | 压缩与重写当前上下文，释放 Token |
| `/model` | 在界面中实时查看与选择切换模型 |
| `/config` | 打开并调整实时设置选项 |
| `/undo` | 撤销上一次由 Codex 自动执行的代码变更 |
| `/diff` | 审查当前更改与未提交的代码差异 |
| `/mcp` | 检查并管理连通的 MCP 服务 |
| `/quit` 或 `/exit` | 退出 Codex CLI |

---

## 四、WSL 环境下的快捷键与使用技巧

### 1. 快捷键

- `Enter`：发送消息
- `Shift + Enter` / `Alt + Enter`：换行输入
- `Ctrl + C`：打断当前生成或命令执行
- `Ctrl + D`：快速退出 Codex（等同于 `/quit`）
- `↑` / `↓`：翻阅历史输入记录

### 2. WSL 跨环境与管道技巧

- **跨文件系统访问**：可以直接在 WSL 中定位到 Windows 盘符路径（如 `cd /mnt/c/Users/...`）并直接运行 `codex`。
- **与 Linux 管道结合**：
  ```bash
  git diff | codex "帮助生成详细且规范的 Git Commit Message"
  cat build.log | codex "分析日志中的错误原因并给出修复方案"
  ```
- **Terminal 建议**：推荐在 **Windows Terminal** 中配合 WSL 使用，享受最佳的渲染体验与彩盘显示。

---

## 五、配置文件与环境变量

### 1. 配置文件位置
- **全局配置**：`~/.codex/config.json` 或 `~/.config/codex/config.json`
- **项目级配置**：`<项目根目录>/.codex.json` 或 `<项目根目录>/CODEX.md`

### 2. WSL 环境变量配置（建议写入 `~/.bashrc` 或 `~/.zshrc`）

```bash
# 配置 OpenAI API 密钥
export OPENAI_API_KEY="sk-..."

# 自定义代理/中转端点（如需要）
export OPENAI_BASE_URL="https://your-proxy-domain.com/v1"

# 默认模型设置
export CODEX_DEFAULT_MODEL="gpt-4o"
```

配置完成后运行 `source ~/.bashrc` 即可在当前 WSL 会话中生效。
