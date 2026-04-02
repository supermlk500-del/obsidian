# Claude 命令大全

## 基础命令

### 会话控制
- `/quit` - 退出应用
- `/clear` - 清除当前会话
- `/help` - 获取帮助信息
- `/fast` - 切换快速模式（使用相同的 Claude Opus 4.6 模型，但输出更快）

### 模型切换
- `/opus` - 切换到 Claude Opus 4.6（最强大的模型）
- `/sonnet` - 切换到 Claude Sonnet 4.6（平衡性能和速度）
- `/haiku` - 切换到 Claude Haiku 4.5（最快速的模型）

## 技能命令（Skills）

### 配置管理
- `/update-config` - 配置 Claude Code 设置（settings.json）

### 代码质量
- `/simplify` - 审查修改的代码，检查复用性、质量和效率，并修复发现的问题

### 自动化
- `/loop` - 按定时间隔运行提示或命令
  - 示例：`/loop 5m /foo`（每5分钟运行一次）
  - 默认间隔：10分钟

### API 开发
- `/claude-api` - 使用 Claude API 或 Anthropic SDK 构建应用

### Git 操作
- `/commit` - 创建 Git 提交
- `/review-pr` - 审查 Pull Request

## 上下文引用

### 文件和文件夹
- `#File` - 引用特定文件
- `#Folder` - 引用特定文件夹
- `#Codebase` - 扫描整个代码库（需要索引）

### 环境信息
- `#Problems` - 查看当前文件的问题
- `#Terminal` - 查看终端输出
- `#Git Diff` - 查看 Git 差异

## 工作模式

### Autopilot 模式
- 允许 Claude 在打开的工作区内自主修改文件

### Supervised 模式
- 用户可以在应用更改后撤销操作

### Worktree（工作树）
- `/worktree` - 创建隔离的 Git 工作树进行开发
- 用于在独立环境中测试更改，不影响主分支

## Hooks（钩子）

可以配置自动触发的钩子：
- 消息发送时触发
- Agent 执行完成时触发
- 新会话创建时触发
- 保存代码文件时触发

配置位置：Explorer 视图的 "Agent Hooks" 部分，或使用命令面板 "Open Kiro Hook UI"

## Steering（引导规则）

位置：`.kiro/steering/*.md`

包含类型：
- 始终包含（默认）
- 条件包含（使用 front-matter 配置 `inclusion: fileMatch`）
- 手动包含（配置 `inclusion: manual`，通过 `#` 引用）

## MCP（Model Context Protocol）

### 配置文件
- 工作区配置：`.kiro/settings/mcp.json`
- 用户级配置：`~/.kiro/settings/mcp.json`

### 管理
- 命令面板搜索 "MCP" 查找相关命令
- MCP Server 视图可重新连接服务器

## Spec（规范）

结构化方式构建和记录功能：
- 文件引用格式：`#[[file:<relative_file_name>]]`
- 支持增量开发复杂功能

## 记忆系统（Memory）

### 自动记忆
- Claude 会自动保存重要信息到 `~/.claude/projects/<project>/memory/`
- 记忆类型：
  - `user` - 用户角色、偏好、知识背景
  - `feedback` - 用户对工作方式的反馈和指导
  - `project` - 项目目标、进展、决策
  - `reference` - 外部系统资源位置

### 记忆命令
- `/remember` - 明确要求 Claude 记住某些信息
- `/forget` - 要求 Claude 忘记某些信息
- 记忆会在未来对话中自动加载和使用

## 终端命令

### 用户自行运行命令
- `! <command>` - 在当前会话中运行命令（输出直接进入对话）
- 适用于交互式登录等场景（如 `gcloud auth login`）

### 任务管理
- `/tasks` - 查看当前任务列表和状态

### 定时任务（Cron）
- 支持按 cron 表达式定时执行任务
- 可设置一次性或循环任务
- 任务在 REPL 空闲时触发

## 模型信息

- 当前模型：Claude Sonnet 4.6 (`claude-sonnet-4-6`)
- 知识截止日期：2025年8月
- 最新模型系列：Claude 4.5/4.6
  - Opus 4.6: `claude-opus-4-6`
  - Sonnet 4.6: `claude-sonnet-4-6`
  - Haiku 4.5: `claude-haiku-4-5-20251001`

## 可用平台

- CLI（命令行）
- 桌面应用（Mac/Windows）
- Web 应用（claude.ai/code）
- IDE 扩展（VS Code、JetBrains）

## 反馈和帮助

- 问题反馈：https://github.com/anthropics/claude-code/issues

使用中转站开源在环境变量里面配置令牌和网址
如下

```bash
echo 'export ANTHROPIC_AUTH_TOKEN="你的API密钥"' >> ~/.zshrc
echo 'export ANTHROPIC_BASE_URL="base-url"' >> ~/.zshrc
source ~/.zshrc
```
