---
title: OpenClaw 快速入门
description: OpenClaw 安装与基础配置速查
date: 2025-03-12
tags: [openclaw, ai, 飞书]
---

# 🦞 OpenClaw 快速入门

> 个人 AI 助手部署指南 | [官方文档](https://docs.openclaw.ai/)

---

## ⚡ 快速开始

### 1. 环境检查
```powershell
# Node.js 必须 v22+
node --version  # v22.x.x
```

### 2. 安装
```powershell
npm install -g openclaw@latest
```

### 3. 初始化配置
```powershell
openclaw onboard --install-daemon
```

配置向导步骤：
1. 选择 **Moonshot (Kimi)** 作为 AI 提供商
2. 输入 API Key（充值建议 ≥50元，避免限制）
3. 选择 **飞书** + **Web UI** 平台
4. 其余选项默认回车即可

---

## 🔧 飞书接入（精简版）

### 创建应用
1. 访问 [飞书开放平台](https://open.feishu.cn/app/)
2. 创建企业自建应用
3. 记录 **App ID** 和 **App Secret**

### 配置权限
进入「权限管理」→ 批量开通：
```json
{
  "scopes": {
    "tenant": [
      "im:message",
      "im:message:send_as_bot",
      "im:message:readonly",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:chat.members:bot_access",
      "im:chat.access_event.bot_p2p_chat:read"
    ]
  }
}
```

### 配置 OpenClaw
```powershell
openclaw config set channels.feishu.appId "cli_xxx"
openclaw config set channels.feishu.appSecret "xxx"
```

### 启动测试
```powershell
openclaw gateway
```

---

## 🚀 常用命令

| 命令 | 说明 |
|------|------|
| `openclaw gateway` | 启动服务 |
| `openclaw gateway status` | 查看状态 |
| `openclaw config set ai.model moonshot/kimi-k2.5` | 切换模型 |
| `openclaw --version` | 查看版本 |

---

## 📁 重要路径

```
C:\Users\<用户名>\.openclaw\
├── openclaw.json      # 主配置
├── workspace\         # 工作区
│   ├── SOUL.md        # AI 人格
│   ├── USER.md        # 用户画像
│   └── MEMORY.md      # 长期记忆
└── logs\              # 日志
```

---

## ⚠️ 常见问题

| 问题 | 解决 |
|------|------|
| npm 下载慢 | `npm config set registry https://registry.npmmirror.com` |
| 卡在 libsignal-node | `git config --global url."https://github.com/".insteadOf ssh://git@github.com/` |
| 飞书收不到消息 | 检查 Gateway 状态 + 事件订阅 `im.message.receive_v1` |
| API 被限制 | Moonshot 充值 ≥50元 |

---

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai/)
- [Moonshot 平台](https://platform.moonshot.cn/)
- [飞书开放平台](https://open.feishu.cn/)

---

> 💡 **提示**：详细安装教程见 [[OpenClaw完整安装教程]]
