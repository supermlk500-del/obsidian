---
title: OpenClaw 完整安装教程
description: 从零开始部署 OpenClaw AI 助手（含飞书接入）
date: 2025-03-08
version: 1.0
tags: [openclaw, 教程, 飞书, ai]
---

# 🦞 OpenClaw 完整安装与配置教程

> 本教程面向零基础用户，手把手教你安装 OpenClaw 并接入飞书，实现 AI 助手功能。
> 
> **更新日期**：2025-03-08

---

## 📋 目录

1. [准备工作](#一准备工作)
2. [安装 OpenClaw](#二安装-openclaw)
3. [基础配置](#三基础配置)
4. [接入飞书](#四接入飞书)
5. [后台运行配置](#五后台运行配置)
6. [常见问题与解决方案](#六常见问题与解决方案)
7. [进阶配置](#七进阶配置)

---

## 一、准备工作

### 1.1 系统要求

| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 10/11（本教程以 Windows 为例） |
| **Node.js** | 版本 22 或以上（⚠️ 必须！） |
| **Git** | 用于拉取依赖（安装 Node.js 时可选安装） |
| **网络** | 能访问国内网站 |
| **硬盘空间** | 至少 500MB 可用空间 |

### 1.2 需要注册的账号

| 账号 | 用途 | 费用 |
|------|------|------|
| **Moonshot (Kimi)** | AI 模型 API | 充值 50 元起 |
| **DeepSeek** | AI 模型 API | 有免费额度 |
| **硅基流动** | AI 模型 API | 有免费模型/免费额度 |
| **智谱 GLM** | AI 模型 API | 通常有新手免费额度 |
| **飞书** | 消息接收和发送 | 免费 |

> ⚠️ **重要提示**：如果你想先低成本跑通，优先选带免费额度的平台；如果更看重中文体验，也可以直接选 Moonshot。

### 1.3 安装 Node.js

1. 访问官网：https://nodejs.org/
2. 下载 **LTS 版本**（长期支持版本）
3. 双击安装包，一路点击"下一步"
4. **重要！** 勾选 **"Add to PATH"**
5. 安装完成后验证：

```powershell
node --version
npm --version
```

### 1.4 安装 Git

如果电脑没装过 Git，也要先装，不然后面某些依赖、插件安装、更新和排查会很麻烦。

1. 访问官网：https://git-scm.com/
2. 下载 **Git for Windows**
3. 安装时大部分选项保持默认即可
4. 安装完成后验证：

```powershell
git --version
```

> ⚠️ 建议在正式安装 OpenClaw 前先确认下面三个命令都能正常输出：
>
> ```powershell
> node --version
> npm --version
> git --version
> ```

---

## 二、安装 OpenClaw

### 2.1 配置 npm 镜像源（解决下载慢）

由于 npm 默认使用国外服务器，国内访问很慢，需要先换成国内镜像：

```powershell
npm config set registry https://registry.npmmirror.com
```

验证是否成功：
```powershell
npm config get registry
# 应显示：https://registry.npmmirror.com
```

### 2.2 配置 Git 协议（解决依赖拉取失败）

OpenClaw 依赖 `libsignal-node` 库，默认使用 SSH 协议，国内容易失败。配置 Git 使用 HTTPS 代替：

```powershell
git config --global url."https://github.com/".insteadOf ssh://git@github.com/
git config --global url."https://github.com/".insteadOf git@github.com:
```

### 2.3 安装 OpenClaw

```powershell
npm install -g openclaw@latest
```

如果仍然很慢，可以尝试：
```powershell
npm cache clean --force
npm install -g openclaw@latest --prefer-offline
```

### 2.4 验证安装

```powershell
openclaw --version
```

---

## 三、基础配置

### 3.1 运行初始化向导

```powershell
openclaw onboard --install-daemon
```

### 3.2 选择 AI 模型

你可以按预算来选：
- **Moonshot (Kimi)**：中文体验好，但通常需要充值
- **DeepSeek**：通常有免费额度，适合先跑通
- **硅基流动**：模型选择多，常有免费模型或赠送额度
- **智谱 GLM**：中文能力不错，通常有新手免费额度

如果你想先低成本跑通，优先考虑免费额度平台。

### 3.3 配置 Moonshot API（付费方案）

1. 访问 https://platform.moonshot.cn/
2. 注册并登录账号
3. 充值至少 50 元（建议）
4. 进入"API Key 管理"页面
5. 点击"创建 API Key"
6. 复制生成的 API Key（以 `sk-` 开头）

回到向导，粘贴 API Key：
```
? 输入 Moonshot API Key: sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 3.4 配置免费 API（推荐先跑通）

#### 方案 A：DeepSeek
1. 访问 https://platform.deepseek.com/
2. 注册并登录
3. 创建 API Key
4. 在 OpenClaw 向导或配置里填入 Key
5. 模型一般可选：
   - `deepseek-chat`
   - `deepseek-reasoner`

#### 方案 B：硅基流动
1. 访问 https://siliconflow.cn/
2. 注册并登录
3. 创建 API Key
4. 选择一个免费或低成本模型
5. 把 API Key 和模型填到 OpenClaw 配置里

#### 方案 C：智谱 GLM
1. 访问 https://open.bigmodel.cn/
2. 注册并登录
3. 创建 API Key
4. 选择可用模型
5. 填入 OpenClaw 配置

> 建议：第一次安装 OpenClaw，如果主要目标是“先跑起来”，就优先用有免费额度的平台。等确认流程稳定后，再切到 Moonshot 或其他付费模型。

### 3.5 选择接入平台

```
? 选择要安装的平台插件:
  ☑ Feishu (飞书)
  ☑ Web UI (网页界面)
```

### 3.6 完成配置

按照向导提示完成剩余配置，大部分情况下直接回车选择默认即可。

配置完成后，你会看到：
```
✓ 配置已保存到: C:\Users\你的用户名\.openclaw\openclaw.json
```

### 3.7 免费 API 常见建议

如果你想尽量少花钱，可以这样选：
- **先测试流程**：优先用 DeepSeek / 硅基流动 / 智谱 GLM 的免费额度
- **中文主力长期用**：Moonshot / Kimi
- **遇到 502 / timeout**：先别急着怪飞书，先检查是不是上游模型平台超时

建议保留至少一个备用 provider，后面如果主模型挂了，可以快速切换。

---

## 四、接入飞书

### 4.1 创建飞书应用

1. 访问 https://open.feishu.cn/app/
2. 登录飞书账号
3. 点击"创建企业自建应用"
4. 填写应用信息：
   - **应用名称**：OpenClaw AI（或你喜欢的名字）
   - **应用描述**：个人 AI 助手
   - **应用头像**：可以上传一个图标

### 4.2 配置权限

1. 进入应用详情页，点击左侧"权限管理"
2. 点击"批量开通权限"
3. 添加以下权限（复制粘贴）：

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "cardkit:card:read",
      "cardkit:card:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "event:ip_list",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": ["aily:file:read", "aily:file:write", "im:chat.access_event.bot_p2p_chat:read"]
  }
}
```

4. 点击"确定"保存

### 4.3 获取凭证

1. 点击左侧"凭证与基础信息"
2. 复制以下信息：
   - **App ID**（应用 ID）
   - **App Secret**（应用密钥）

### 4.4 配置事件订阅

1. 点击左侧"事件订阅"
2. 开启"启用事件订阅"
3. 添加事件：`im.message.receive_v1`（接收消息事件）

> ⚠️ **注意**：保存时需要 OpenClaw Gateway 正在运行

### 4.5 配置 OpenClaw 飞书插件

```powershell
openclaw config set channels.feishu.appId "你的AppID"
openclaw config set channels.feishu.appSecret "你的AppSecret"
```

### 4.6 发布应用

1. 点击左侧"版本管理与发布"
2. 点击"创建版本"
3. 填写版本信息（如 1.0.0）
4. 点击"保存并发布" → "申请发布"

### 4.7 测试连接

```powershell
openclaw gateway
```

看到以下输出表示成功：
```
Gateway: bind=loopback (127.0.0.1), port=18789
RPC probe: ok
Listening: 127.0.0.1:18789
```

现在去飞书给机器人发消息测试！

### 4.8 首次飞书对话可能需要 Pairing 批准

如果第一次在飞书里给机器人发消息时出现：

```txt
OpenClaw: access not configured.
Your Feishu user id: ou_xxx
Pairing code: ABCD1234
Ask the bot owner to approve with:
openclaw pairing approve feishu ABCD1234
```

这不是模型坏了，也不是飞书配置一定错了，而是这个飞书用户/会话还没有完成准入授权。

这时在运行 OpenClaw 的机器上执行：

```powershell
openclaw pairing approve feishu ABCD1234
```

注意：
- `ABCD1234` 要替换成飞书里当次显示的 pairing code
- 如果 code 过期，就重新发一条消息拿新的 code
- 如果你配置了多个飞书机器人账号，那么 `main` 和 `chatemo` 之类的账号可能都要分别批准一次

### 4.9 安装后建议立刻检查

改完配置或完成飞书接入后，建议立刻运行：

```powershell
openclaw status
openclaw status --deep
openclaw doctor
```

重点看：
- `Feishu` 是否显示为 `configured`
- `accounts x/x` 是否正常
- 每个账号是不是 `ok`

如果刚修改过 `openclaw.json`，别忘了重启：

```powershell
openclaw gateway restart
```

---

## 五、后台运行配置

### 5.1 为什么要后台运行？

默认情况下，`openclaw gateway` 会占用一个 PowerShell 窗口，关掉就停止。配置后台运行后：
- 不占用窗口
- 开机自动启动
- 稳定运行不掉线

### 5.2 创建启动脚本

打开记事本，粘贴以下内容：

```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell.exe -WindowStyle Hidden -Command openclaw gateway", 0, False
Set WshShell = Nothing
```

保存为：`C:\Users\你的用户名\.openclaw\start-gateway-hidden.vbs`

### 5.3 创建定时任务

1. 按 `Win + R`，输入 `taskschd.msc`，回车
2. 右侧点击"创建基本任务"
3. 名称：`OpenClaw Gateway`
4. 触发器：**当特定用户登录时**
5. 操作：**启动程序**
6. 程序：`wscript.exe`
7. 参数：`"C:\Users\你的用户名\.openclaw\start-gateway-hidden.vbs"`
8. 勾选"打开属性对话框"，点击完成

### 5.4 配置任务属性

1. **常规**选项卡：勾选"使用最高权限运行"
2. **条件**选项卡：取消勾选"只有在计算机使用交流电源时才启动"
3. 点击"确定"保存

### 5.5 测试

1. 重启电脑
2. 登录后等待 10-30 秒
3. 去飞书发消息测试

### 5.6 查看运行状态

```powershell
openclaw gateway status
```

### 5.7 停止后台运行

```powershell
Stop-Process -Name wscript -Force
```

---

## 六、常见问题与解决方案

### ❌ 问题1：npm 下载很慢或超时

**原因**：默认使用国外 npm 源

**解决**：
```powershell
npm config set registry https://registry.npmmirror.com
npm cache clean --force
npm install -g openclaw@latest
```

---

### ❌ 问题2：安装时卡在 `libsignal-node`

**原因**：Git 使用 SSH 协议拉取 GitHub 依赖失败

**解决**：
```powershell
git config --global url."https://github.com/".insteadOf ssh://git@github.com/
git config --global url."https://github.com/".insteadOf git@github.com:
npm cache clean --force
npm install -g openclaw@latest
```

---

### ❌ 问题3：提示"npm 不是内部或外部命令"

**原因**：Node.js 环境变量未配置

**解决**：
1. 重新安装 Node.js，勾选"Add to PATH"
2. 重启 PowerShell
3. 如仍不行，重启电脑

---

### ❌ 问题4：飞书收不到消息 / 提示 access not configured

**排查步骤**：
1. 检查 Gateway 是否运行：`openclaw gateway status`
2. 检查飞书 AppID 和 AppSecret 是否正确
3. 检查飞书应用是否已发布
4. 检查是否添加了 `im.message.receive_v1` 事件订阅
5. 如果看到下面这种提示：

```txt
OpenClaw: access not configured.
Your Feishu user id: ou_81f7e50aa689845d0106a78d4f6894da
Pairing code: DHLULZMS
Ask the bot owner to approve with:
openclaw pairing approve feishu DHLULZMS
```

说明这是 **Pairing / 准入** 问题，不是模型问题。

直接执行：
```powershell
openclaw pairing approve feishu DHLULZMS
```

注意：
- `DHLULZMS` 只是示例，要替换成当次显示的 code
- 如果 code 失效，就重新给机器人发一句，拿新的 code
- 多个飞书账号要分别批准，不是批一次全通用

---

### ❌ 问题5：AI 回复很慢、报 502、或者 Upstream request failed

如果机器人能收到消息，但回复时出现：

```txt
502 Upstream request failed
```

通常说明：
- 飞书渠道层已经通了
- 真正失败的是上游模型提供商
- 常见是 `baseUrl`、`apiKey`、模型 id、网络超时这几类问题

建议排查：

```powershell
openclaw logs --follow
openclaw status --deep
```

如果日志里看到类似：
- `provider: jmr`
- `model: gpt-5.4`
- `failoverReason: timeout`

那就优先排查该 provider 的网络和模型可用性。

---

### ❌ 问题6：如何更换 AI 模型？

```powershell
# 查看支持的提供商
openclaw providers

# 更换为 DeepSeek（免费额度多）
openclaw config set ai.provider deepseek
openclaw config set ai.apiKey "sk-xxxxxxxx"
openclaw config set ai.model deepseek-chat
```

**免费 API 推荐**：

| 平台 | 免费额度 | 特点 |
|------|----------|------|
| DeepSeek | 5000万 tokens | 模型强，额度多 |
| 硅基流动 | 14元 + 免费模型 | 选择多，稳定 |
| 智谱 GLM | 100万 tokens | 中文强 |

---

### ❌ 问题7：如何查看日志？

日志文件位置：
```
C:\tmp\openclaw\openclaw-YYYY-MM-DD.log
```

---

## 七、进阶配置

### 7.1 使用 nrm 管理 npm 源（可选）

```powershell
# 安装 nrm
npm install -g nrm

# 查看可用源
nrm ls

# 测试速度
nrm test

# 切换到淘宝源
nrm use taobao

# 恢复官方源
nrm use npm
```

### 7.2 配置多个平台

```powershell
# Telegram
openclaw config set channels.telegram.enabled true
openclaw config set channels.telegram.botToken "你的BotToken"
```

### 7.3 配置多个 Agent / 多个飞书机器人

如果你想让不同飞书机器人分别对应不同 agent，比如：
- `main_feishu -> main`
- `chatemo -> chatemo`

最容易踩的坑：
- 账号必须写在 `channels.feishu.accounts` 下面
- 不能写成 `channels.accounts`
- 然后再通过 `bindings` 按 `accountId` 路由到不同 agent

示例结构：

```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "feishu",
        "accountId": "main_feishu"
      }
    },
    {
      "agentId": "chatemo",
      "match": {
        "channel": "feishu",
        "accountId": "chatemo"
      }
    }
  ],
  "channels": {
    "feishu": {
      "defaultAgent": "main",
      "accounts": {
        "main_feishu": {
          "appId": "你的 AppID",
          "appSecret": "你的 AppSecret"
        },
        "chatemo": {
          "appId": "你的 AppID",
          "appSecret": "你的 AppSecret"
        }
      }
    }
  }
}
```

如果写成了 `channels.accounts`，OpenClaw 会报类似：

```txt
channels.accounts: unknown channel id: accounts
```

### 7.4 自定义 AI 参数

```powershell
# 设置模型
openclaw config set ai.model moonshot/kimi-k2.5

# 设置温度（创造性，0-1）
openclaw config set ai.temperature 0.7

# 设置最大 token
openclaw config set ai.maxTokens 4000
```

### 7.5 配置代理（如需要）

```powershell
openclaw config set proxy.enabled true
openclaw config set proxy.host "127.0.0.1"
openclaw config set proxy.port 7890
```

### 7.6 文档与本机插件列表不一致怎么办

有时候官方网页文档里提到的 provider / plugin 名，在你当前安装版本里可能已经移除、改名或者未打包。

所以遇到插件相关问题时，不要只信网页文档，优先以本机实际结果为准：

```powershell
openclaw plugins list
```

如果 CLI 反复提示：
- `plugin removed: xxx`

通常说明 `openclaw.json` 里残留了失效插件配置，需要从下面两处删除：
- `plugins.allow`
- `plugins.entries`

---

## ✅ 安装检查清单

完成安装后，请确认：

- [ ] Node.js 已安装（v22+）
- [ ] npm 镜像源已换成国内
- [ ] Git 协议已配置为 HTTPS
- [ ] OpenClaw 安装成功
- [ ] Moonshot API 已配置
- [ ] 飞书应用已创建并发布
- [ ] 飞书凭证已配置到 OpenClaw
- [ ] 能正常收发消息
- [ ] 后台运行已配置（可选）

---

## 📝 总结

恭喜！按照本教程，你应该已经成功：
1. ✅ 安装了 OpenClaw
2. ✅ 配置了 AI 模型
3. ✅ 接入了飞书
4. ✅ 实现了后台自动运行

现在你可以：
- 在飞书里和 AI 助手聊天
- 让 AI 帮你处理各种任务
- 探索更多 OpenClaw 的功能

---

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai/)
- [Moonshot 平台](https://platform.moonshot.cn/)
- [DeepSeek 平台](https://platform.deepseek.com/)
- [硅基流动](https://siliconflow.cn/)
- [飞书开放平台](https://open.feishu.cn/)

---

> 💡 **提示**：遇到问题先查看日志，或参考 [[OpenClaw 快速入门]] 速查。
