# AstrBot 使用笔记

> **版本**: v4.22.2 | **许可证**: AGPL-3.0 | **官方文档**: [astrbot.app](https://astrbot.app/)
> 
> AstrBot 是一个开源的一体化 **Agentic AI 聊天机器人平台**，支持接入主流 IM 平台和大语言模型，拥有 1000+ 插件生态。

---

## 1. 安装与部署

### 1.1 CLI 一键部署 (推荐)

```bash
# 安装 uv 包管理器 (如未安装)
pip install uv

# 安装 AstrBot
uv tool install astrbot

# 初始化 (首次运行)
astrbot init

# 启动
astrbot run

# 升级
uv tool upgrade astrbot
```

> [!warning] 
> 通过 uv 部署的 AstrBot **不支持通过 WebUI 升级**，需用命令行 `uv tool upgrade astrbot`。

### 1.2 其他部署方式

| 方式                          | 适用场景                                 |
| --------------------------- | ------------------------------------ |
| **Docker**                  | 生产环境、服务器                             |
| **桌面应用**                    | 本地使用 ChatUI                          |
| **Launcher**                | 桌面用户，支持多实例                           |
| **BT 面板 / 1Panel / CasaOS** | NAS / 面板用户                           |
| **AUR**                     | Arch Linux 用户 (`yay -S astrbot-git`) |

---

## 2. CLI 命令速查

### 2.1 核心命令

```bash
astrbot --version          # 查看版本
astrbot init               # 初始化项目
astrbot run                # 启动 AstrBot
astrbot run -p 8080        # 指定 Dashboard 端口
astrbot run -r             # 自动热重载插件
```

### 2.2 配置管理 (`astrbot conf`)

```bash
astrbot conf get                    # 查看所有可配置项
astrbot conf get <key>              # 查看指定配置
astrbot conf set <key> <value>      # 设置配置项
```

**可配置项：**

| Key | 说明 | 示例 |
|-----|------|------|
| `timezone` | 时区 | `Asia/Shanghai` |
| `log_level` | 日志级别 | `DEBUG/INFO/WARNING/ERROR/CRITICAL` |
| `dashboard.port` | Dashboard 端口 | `6185` |
| `dashboard.username` | 管理面板用户名 | `admin` |
| `dashboard.password` | 管理面板密码 | `your_password` |
| `callback_api_base` | 回调 API 地址 | `http://xxx:xxx` |

### 2.3 插件管理 (`astrbot plug`)

```bash
astrbot plug list                    # 列出已安装插件
astrbot plug search <关键词>          # 搜索插件
astrbot plug install <插件名>         # 安装插件
astrbot plug install <名> --proxy <代理>  # 通过代理安装
astrbot plug update                  # 更新插件
astrbot plug remove <插件名>          # 卸载插件
astrbot plug new                     # 创建新插件模板
```

---

## 3. 支持的消息平台

### 3.1 官方支持

| 平台 | 说明 |
|------|------|
| **QQ** | 官方 QQ 机器人 API |
| **OneBot v11** | 兼容 NapCat / Lagrange / LLOneBot 等 |
| **Telegram** | Telegram Bot API |
| **微信** | 企业微信 / 企业微信 AI Bot / 微信公众号 |
| **飞书 (Lark)** | 飞书机器人 |
| **钉钉** | 钉钉机器人 |
| **Discord** | Discord Bot |
| **Slack** | Slack Bot |
| **LINE** | LINE Bot |
| **Satori** | Satori 协议 |
| **Misskey** | Misskey 平台 |

### 3.2 社区维护

Matrix / KOOK / VoceChat

> [!tip]
> 平台接入配置在 Dashboard WebUI 中操作更方便，启动后访问 `http://localhost:6185`。

---

## 4. 支持的 LLM 服务

### 4.1 大语言模型

| 服务商 | 备注 |
|--------|------|
| **OpenAI** (及兼容 API) | GPT-4o / GPT-4 等 |
| **Anthropic** | Claude 系列 |
| **Google Gemini** | Gemini 系列 |
| **DeepSeek** | DeepSeek-V3 / R1 等 |
| **Moonshot AI** | Kimi |
| **智谱 AI** | GLM 系列 |
| **Ollama** | 本地自托管 |
| **LM Studio** | 本地自托管 |
| **SiliconFlow** | 硅基流动 |
| **ModelScope** | 魔搭 |
| **OneAPI** | API 聚合网关 |

### 4.2 LLMOps 平台

| 平台 | 说明 |
|------|------|
| **Dify** | 可视化 AI 工作流 |
| **阿里云百炼** | 阿里云 AI 应用平台 |
| **Coze** | 字节跳动 AI Bot 平台 |

### 4.3 语音能力

**语音识别 (STT)**: OpenAI Whisper / SenseVoice / 小米 MiMo Omni

**语音合成 (TTS)**: OpenAI TTS / Gemini TTS / Edge TTS / FishAudio / GPT-SoVITS / 阿里云百炼 / Azure / Minimax / 火山引擎 等

---

## 5. 核心功能

### 5.1 AI 能力

- **多模态对话** - 文本 / 图片 / 语音
- **Agent 模式** - 工具调用、自主决策
- **MCP 协议** - Model Context Protocol 支持
- **知识库** - RAG 检索增强生成
- **人设系统** - 自定义 AI 人格
- **上下文管理** - 自动压缩长对话

### 5.2 Agent 沙箱

提供隔离安全的代码执行环境：
- Shell 命令执行
- 代码运行沙箱
- 会话级资源复用

### 5.3 WebUI 管理面板

启动后访问 Dashboard 进行可视化配置：

```
http://localhost:6185
```

默认端口 `6185`，可通过以下方式修改：

```bash
astrbot conf set dashboard.port 8080
# 或启动时指定
astrbot run -p 8080
```

---

## 6. 快速上手流程

```
1. astrbot run                    # 启动服务
2. 浏览器打开 http://localhost:6185  # 进入管理面板
3. 配置 LLM 服务 (填入 API Key)     # 在 "模型" 页面
4. 接入消息平台                     # 在 "平台" 页面
5. 安装需要的插件                   # 在 "插件" 页面
6. 开始对话！
```

---

## 7. 常用配置示例

### 7.1 设置管理面板密码

```bash
astrbot conf set dashboard.username admin
astrbot conf set dashboard.password mypassword123
```

### 7.2 设置时区和日志

```bash
astrbot conf set timezone Asia/Shanghai
astrbot conf set log_level INFO
```

---

## 8. 文件目录结构

```
~/.astrbot/              # AstrBot 主配置目录
~/data/
  ├── config/            # 配置文件
  ├── plugins/           # 插件目录
  └── temp/              # 临时文件
```

---

## 9. 社区与资源

| 资源 | 链接 |
|------|------|
| 官方文档 | https://astrbot.app |
| GitHub | https://github.com/AstrBotDevs/AstrBot |
| 博客 | https://blog.astrbot.app |
| 路线图 | https://astrbot.featurebase.app/roadmap |
| QQ 群 (新) | 916228568 |
| Discord | https://discord.gg/hAVk6tgV36 |
| 邮件 | community@astrbot.app |
