# OpenCode 命令大全

> 最后更新：2026-08-05
> 适用版本：OpenCode CLI（开源 AI 编程 Agent 命令行工具）

---

## 一、核心基础命令（CLI 命令行）

在终端（Terminal / PowerShell / Git Bash）中直接运行：

### 1. 常用启动与会话命令

| 命令 | 完整写法 | 作用说明与适用场景 |
|------|----------|-------------------|
| **启动交互界面** | `opencode` | 打开终端交互式 TUI 模式（默认最常用方式） |
| **单次非交互** | `opencode "提示词"` | 传入提示词执行单次任务，不进入交互界面 |
| **恢复/指定会话** | `opencode session <session-id>` | 恢复或连接到指定 Session ID 的会话 |
| **指定模型启动** | `opencode -m <model>` | 指定本次使用的模型（如 `opencode -m claude-3-5-sonnet`） |
| **指定供应商启动** | `opencode -p <provider>` | 指定供应商（如 `anthropic`, `openai`, `ollama`, `openrouter`） |
| **指定配置文件** | `opencode --config <path>` | 使用指定的 `opencode.json` 配置文件路径 |

---

### 2. CLI 管理子命令

| 命令 | 作用说明与示例 |
|------|----------------|
| `opencode mcp add <name> <command>` | 添加 MCP 工具服务器（例如 `opencode mcp add github npx -y @modelcontextprotocol/server-github`） |
| `opencode mcp list` | 列出已配置的 MCP 工具服务器 |
| `opencode mcp remove <name>` | 移除指定的 MCP 服务器 |
| `opencode session list` | 查看历史保存的 Session 会话列表 |

---

## 二、会话内部斜杠命令（TUI 交互控制）

在运行 `opencode` 进入交互界面后，在输入框中以 `/` 开头输入：

| 斜杠命令              | 语法示例       | 作用与使用场景            |
| ----------------- | ---------- | ------------------ |
| `/help`           | `/help`    | 显示帮助菜单与可用命令列表      |
| `/clear`          | `/clear`   | 清空当前对话与上下文历史       |
| `/compact`        | `/compact` | 压缩/总结当前上下文窗口       |
| `/model`          | `/model`   | 交互式查看与切换模型/供应商     |
| `/undo`           | `/undo`    | 撤销上一步由 AI 执行的代码修改  |
| `/mcp`            | `/mcp`     | 会话内部管理并连接 MCP 扩展工具 |
| `/quit` 或 `/exit` | `/quit`    | 退出 OpenCode 交互界面   |

---

## 三、配置与环境变量

### 1. 配置文件（`opencode.json`）

- **项目级配置**：`<项目根目录>/opencode.json`
- **全局配置**：`~/.config/opencode/config.json`

**示例结构**：
```json
{
  "provider": "anthropic",
  "model": "claude-3-5-sonnet-20241022",
  "instructions": "使用 TypeScript 规范并编写单元测试",
  "mcp": {}
}
```

### 2. 常用环境变量

```bash
# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI
export OPENAI_API_KEY="sk-..."

# 其他代理/自定义端点
export ANTHROPIC_BASE_URL="https://your-proxy-domain.com"
```
