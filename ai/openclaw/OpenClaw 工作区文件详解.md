---
title: OpenClaw 工作区文件详解
description: 理解 OpenClaw 工作区各 MD 文件的作用
---

# 📁 OpenClaw 工作区文件详解

工作区路径：`C:\Users\<用户名>\.openclaw\workspace`

---

## 核心文件

### AGENTS.md
```yaml
用途: 启动序列、操作清单、行为规则
加载时机: 每次轮次（所有 Agent）
可见性: 子 Agent 可见
```

### SOUL.md
```yaml
用途: AI 人格定义、价值观、语气风格
加载时机: 每次轮次
可见性: 子 Agent 可见
示例内容: "你是温柔体贴的 AI 助手"
```

### USER.md
```yaml
用途: 用户画像、偏好、关系背景
加载时机: 每次轮次（仅主会话）
可见性: 子 Agent 不可见（保护隐私）
```

### TOOLS.md
```yaml
用途: 环境特定信息
内容: SSH 配置、TTS 语音、摄像头、设备别名
加载时机: 每次轮次
可见性: 子 Agent 可见
```

### IDENTITY.md
```yaml
用途: AI 自我描述
内容: 名称、Emoji、头像
加载时机: 每次轮次
可见性: 子 Agent 可见
```

---

## 记忆系统

### memory/YYYY-MM-DD.md
- 每日自动生成的原始日志
- 记录当天所有对话和操作

### MEMORY.md
- 长期记忆的精华版
- 重要事件、决策、教训
- 需要定期从 daily 文件整理而来

---

## 其他文件

| 文件 | 用途 |
|------|------|
| `HEARTBEAT.md` | 定时任务配置 |
| `BOOTSTRAP.md` | 首次运行引导（首次后删除） |
| `AGENTS.md` | 全局行为规则 |

---

## 文件加载优先级

```
系统启动
  ↓
读取 AGENTS.md（规则）
  ↓
读取 SOUL.md（人格）
  ↓
读取 IDENTITY.md（身份）
  ↓
读取 USER.md（用户，仅主会话）
  ↓
读取 TOOLS.md（工具配置）
  ↓
读取 memory/今日.md（上下文）
  ↓
开始对话
```

---

## 💡 最佳实践

1. **SOUL.md** - 定义 AI 的性格，让它更像你想要的助手
2. **USER.md** - 填写你的偏好，让 AI 更懂你
3. **TOOLS.md** - 记录你的设备信息，方便 AI 调用
4. **MEMORY.md** - 定期整理，把重要信息沉淀下来
5. **HEARTBEAT.md** - 配置定时检查任务

---

> 详见：[OpenClaw 官方文档 - 工作区](https://docs.openclaw.ai/)
