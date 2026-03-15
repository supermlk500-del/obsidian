[[https://docs.openclaw.ai/]]网址
注意在安装飞书插件后 请跳到标题2 因为我电脑已经安装过一遍 第二遍会不一样
# 安装
## 前置环境
如果电脑是全新环境，先装这些：
- `Node.js`：必须 `22` 或以上
- `Git`：建议提前安装，后面很多插件、更新、拉仓库、排查问题都会用到

建议先检查：
```cmd
node -v
git --version
npm -v
```

如果 `node` 或 `git` 没装：
- 先安装 `Node.js 22+`
- 再安装 `Git for Windows`
- 安装后重新打开终端再继续

- 条件：`nodejs`版本必须在22或以上

![[文档.png]]

- 在终端运行
```cmd
npm install -g openclaw@latest
```

- 基础设置
```cmd
openclaw onboard --install-daemon
```
1. 
![[设置1.png]]
2. 
![[设置2.png]]
3. ==由于我不是第一次安装 一般都是直接回车 ==到这一步我使用的时`kimi2.5`,也就是上面的`Moonshot `,去官网充值50块. 
注意:==充值不到50块那么在使用的使用容易被kimi限制==
![[设置3.png]]
4. 得到apikey后输入
![[设置4.png]]
5. 在这里如果在中国内地注册的apikey就使用`.cn`域名的apikey
![[设置5.png]]
6. 选择飞书插件和手机对话
![[设置6.png]]
![[飞书1.png]]
![[飞书2.png]]
![[飞书3.png]]
![[飞书4.png]]


7. 选择自己想要的
![[设置7.png]]
8. 上面的apikey全部选no
`hooks`全部选上 
![[这是8.png]]
9. 选择在`webui`打开
![[设置9.png]]
# 飞书
![[飞书a.png]]
填写基本信息
![[飞书b.png]]
![[飞书c.png]]
输入这些
```
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
![[飞书d.png]]

![[飞书e.png]]
![[飞书g.png]]

注意这里需要开启openclaw才能保存成功
![[飞书f.png]]
==一定要添加这个事件==



至此基本成功 因为是第二次安可能会有缺失部分会随时补充

# 安装后第一时间检查
安装或修改配置后，先跑下面几条，能少踩很多坑：
```cmd
openclaw status
openclaw status --deep
openclaw doctor
```
- `status --deep` 可以直接看到 `Feishu` 是否是 `accounts x/x`、每个账号是不是 `ok`
- 如果改了 `openclaw.json`，一定要重启：
```cmd
openclaw gateway restart
```

# 遇到的问题
## 隧道连接服务器之后本地密钥失效
![[隧道1.png]]
此时需要使用`dashboard`然后找到里面的`token`复制后在`openclaw.json`内修改好,注意此时一定要把隧道关闭

## 使用飞书机器人提示 access not configured
如果飞书里出现：
```
OpenClaw: access not configured.
Your Feishu user id: ou_81f7e50aa689845d0106a78d4f6894da
Pairing code: TUYN6Q3A
Ask the bot owner to approve with:
openclaw pairing approve feishu TUYN6Q3A
```
说明：
- 不是模型坏了
- 不是 agent 配置一定错了
- 而是这个飞书用户/会话还没有完成 pairing 授权

那么终端运行：
```cmd
openclaw pairing approve feishu TUYN6Q3A
```
注意：
- `TUYN6Q3A` 只是示例，实际要用飞书里当次显示的 pairing code
- 如果 code 过期，就重新给机器人发一句话，拿新的 code 再批准
- 如果有多个飞书机器人账号，`main` 和 `chatemo` 都可能分别触发一次 pairing，要各批各的

## main 正常接入但报 502 Upstream request failed
如果机器人已经能收到消息，但回复里出现：
```txt
502 Upstream request failed
```
并且日志里能看到类似：
- `provider: jmr`
- `model: gpt-5.4`
- `failoverReason: timeout`

那说明：
- Feishu 渠道层通常已经正常
- 真正失败的是上游模型提供商超时或异常
- 这时重点排查 `models.providers` 里的 `baseUrl`、`apiKey`、模型 id 是否可用

建议先检查：
```cmd
openclaw logs --follow
openclaw status --deep
```

## 多 Agent + 飞书双账号配置最容易写错的地方
如果你想让两个飞书机器人分别对应两个 agent，比如：
- `main_feishu -> main`
- `chatemo -> chatemo`

配置重点：
1. 账号必须写在 `channels.feishu.accounts` 下面
2. 不能写成 `channels.accounts`
3. 然后再用 `bindings` 按 `accountId` 路由到对应 agent

正确结构示例：
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
          "appId": "你的 appId",
          "appSecret": "你的 appSecret"
        },
        "chatemo": {
          "appId": "你的 appId",
          "appSecret": "你的 appSecret"
        }
      }
    }
  }
}
```

## 文档和本机插件列表不一致
有些时候官方文档里提到的 provider/plugin 名，在当前安装版本里可能已经移除或改名。
所以不要只信网页文档，要以本机实际结果为准：
```cmd
openclaw plugins list
```
如果 CLI 反复提示：
- `plugin removed: xxx`

说明配置里残留了失效插件，需要从 `openclaw.json` 的下面两处删掉：
- `plugins.allow`
- `plugins.entries`

## 修改配置后一定重启
只改 `openclaw.json` 不重启，很多效果不会立刻生效。
改完建议固定执行：
```cmd
openclaw doctor
openclaw gateway restart
openclaw status --deep
```

# 添加新Agent机器人
## 给 main 单独换模型
如果只想让 `main` 换模型，而 `chatemo` 保持原样，可以直接在 `agents.list` 里给 `main` 单独加 `model`：
```json
{
  "id": "main",
  "model": "jmr/kimi-k2.5"
}
```
这样：
- `main` 走 `jmr/kimi-k2.5`
- `chatemo` 继续继承默认模型

注意：如果你是直接替换同一个 provider 的 `apiKey`，那这个 provider 下的其它模型/agent 也会共用这把 key。

[登录不了Antigravity](https://zhuanlan.zhihu.com/p/1989455405814936809)
[[Antigravity]]

# 停止openclaw
```bash
netstat -ano | findstr 18789
taskkill /PID 32612 /F
```
