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

## 添加
```bash
openclaw agents add new
```

[登录不了Antigravity](https://zhuanlan.zhihu.com/p/1989455405814936809)
[[Antigravity]]

# 停止openclaw
```bash
netstat -ano | findstr 18789
taskkill /PID 32612 /F
```
# 修改配置
```bash
openclaw configure
```

# 三省六部
我先看一下这个仓库的说明页，再给你拆成“这些 agents 是干嘛的 / 怎么用 / 飞书权限怎么配 / 怎么拉群协作”四块。这个项目本质上是一个 **基于 OpenClaw 的多 Agent 编排系统**。你可以把它理解成：**不是“一个 AI 干所有事”，而是“一个总控 + 多个专职角色分工做事”**，特别适合代码任务拆解、审查、执行、汇总。

### 1. 这些 agents 都是干什么的
按这个仓库的设计，核心角色大概是：

- **taizi（太子）**
入口分拣。判断你是在闲聊，还是在“下任务”。会整理需求、生成标题。
- **zhongshu（中书省）**
负责规划和拆解任务。比如把“做个功能”拆成后端、前端、测试、文档。
- **menxia（门下省）**
负责审核。检查方案是否合理、有没有风险、有没有遗漏。
- **shangshu（尚书省）**
总调度。把规划后的任务派发给具体执行 agent，并汇总结果。
- **hubu（户部）**
偏数据、报表、资源核算。
- **libu（礼部）**
偏文档、规范、接口说明、汇报材料。
- **bingbu（兵部）**
偏代码开发、Bug 修复、工程实现。
**如果你是做 Java/Spring Boot/Vue，这个会很常用。**
- **xingbu（刑部）**
偏安全、合规、审计、红线检查。
- **gongbu（工部）**
偏部署、Docker、CI/CD、自动化、环境搭建。
- **libu_hr（吏部）**
管 agent 管理、权限、编制。
- **zaochao（早朝官）**
定时播报、聚合信息、日报类任务。

---

### 2. 你该怎么用
你真正使用时，不一定要手动一个找 agent 聊。正常流程一般是：

**你提需求 → taizi 分拣 → zhongshu 规划 → menxia 审核 → shangshu 派发 → 各部执行 → 汇总给你**

如果你想做“代码任务协作”，推荐这样理解：

#### 适合你的最实用分工
- **bingbu**：写代码、修 bug、改功能
- **libu**：补 README、接口文档、设计说明
- **xingbu**：安全检查、权限边界、输入校验
- **gongbu**：Docker、部署、脚本、流水线
- **shangshu**：总控和串联结果

#### 一个典型例子
比如你说：

> 给我做一个 Spring Boot + Vue 的用户管理模块，包含登录、角色权限、接口文档和 Docker 部署

系统可以这样分：
- **zhongshu**：拆任务
- **menxia**：审查方案
- **bingbu**：写后端/前端代码
- **libu**：写接口文档
- **gongbu**：补 docker-compose / 部署脚本
- **xingbu**：检查鉴权、安全风险
- **shangshu**：最后汇总交付

也就是说，**你不需要亲自扮演 PM 去一个协调**，这个项目就是干这个的。

---

### 3. 权限是怎么回事
这个项目强调的是 **Agent 之间不是随便互发消息的**，而是有权限矩阵。

仓库里写得很明确，大意是：

- **taizi** 主要往 **zhongshu** 发
- **zhongshu** 可以跟 **taizi / menxia / shangshu** 协作
- **menxia** 主要负责审核，回给 **zhongshu / shangshu**
- **shangshu** 才是可以广泛派发给六部的那个
- **六部** 一般把结果回给 **shangshu**
- **不是所有 agent 都能直接互聊**

这个设计的好处是：
- 避免乱串话
- 方便审计
- 防止流程绕过审核

所以如果你后面接飞书群，也最好保持这个思路：
**飞书群是你的“皇上入口”或团队协作入口，不是让每个 agent 都随便在群里乱说话。**

---

### 4. 你要接入飞书，需要哪些权限
你这里说的“给权限”，我理解成两层：

## A. OpenClaw / Edict 内部的 agent 权限
这个通常是：
- agent 是否已注册
- sessions 之间是否可见 / 可通信
- agent 的工具权限是否配置好
- 是否复制了 API key / 模型配置到各 agent

仓库 README 里提到安装脚本会做这些事，比如：
- 创建 agent workspace
- 写入 SOUL.md
- 注册到 `openclaw.json`
- 设置 `sessions.visibility`
- 同步 API key
- 重启 Gateway

**如果你现在是“没装完全”**，很可能就卡在这里之一：
1. agent 没注册全
2. 配置没写进 `openclaw.json`
3. API key 没同步
4. gateway 没重启生效
5. dashboard 起了，但后面的 agent/session 实际不可用

---

## B. 飞书侧权限
如果你要把它接进飞书，并拉一个群来协作代码任务，通常要准备这些能力：

### 至少要有的能力
- **收消息**：机器人能收到群消息 / 私聊消息
- **发消息**：机器人能回复任务结果
- **群聊可用**：机器人被允许加入群
- **用户可 @ 机器人**
- **事件订阅**：消息事件、群聊事件
- **如果要写文档/知识库**：
- Doc 文档读写权限
- Drive/云文档权限
- Wiki/知识库权限
- **如果要操作多维表格**：
- Bitable 权限

### 你这个场景建议的飞书能力组合
如果目标是“拉群做代码任务”，建议先只要这套最小闭环：

- **机器人收发消息**
- **群聊接入**
- **@ 机器人触发任务**
- **文档写入（可选）**
- **知识库/多维表格（后续再加）**

也就是说，**第一阶段别一上来把飞书所有权限都开满**，先让它：
1. 能进群
2. 能收消息
3. 能回消息
4. 能把任务结果发回来

文档、知识库、表格这些是第二阶段再加。

---

### 5. 你应该怎么“拉一个群”来完成代码任务
我建议你这么设计，不然会很乱：

## 推荐群协作模式
### 群里参与者
- 你
- 你的团队成员
- 一个飞书机器人入口（对接 OpenClaw / Edict）

### 群里怎么说
你在群里直接发这种命令式话术就行：

- `@机器人 给 bingbu 下一个任务：修复用户登录接口 401 问题`
- `@机器人 分析这个 Spring Boot 项目的权限设计有没有漏洞`
- `@机器人 把这个需求拆成前后端、测试、部署四部分`
- `@机器人 输出一份接口文档到飞书文档`

### 最佳实践
- **群里只保留一个入口机器人**
- 不要让 10 个 agent 都直接进群发言
- 群里看到的是“总管式输出”
- 内部由 Edict 去调用多 agent 分工

否则会出现：
- 群消息爆炸
- 多 agent 互相打断
- 审计困难
- 用户看不懂谁在做什么

**结论：群里最好只有“皇上入口 / 总管入口”，底层多个 agent 在系统内协作。**

---

### 6. 你现在最该做的事
如果你已经装了一半，我建议按这个顺序排查：

#### 第一步：确认安装完整度
你需要确认这些是否都 OK：
- OpenClaw 本体能正常运行
- Edict dashboard 能打开
- 所有 agent workspace 都创建了
- `openclaw.json` 已写入 agents 配置
- API key 已配置
- Gateway 已重启
- agent 之间可通信

#### 第二步：确认飞书接入目标
你要先决定是：
- **只把飞书当消息入口**
- 还是 **消息 + 文档 + 知识库 + 表格全接**

我建议先做第一种。

#### 第三步：设计群内交互
建议先定规则：
- 群里谁能下任务
- 什么格式下任务
- 结果回到群里还是写文档再贴链接
- 长任务是同步回复，还是异步回报进度

---

### 7. 如果你是做代码任务，我给你的建议配置
按你的技术栈（Java / Spring Boot / Vue），我建议优先用这几个 agent：

- **taizi**：接需求
- **zhongshu**：拆任务
- **menxia**：审方案
- **shangshu**：控流程
- **bingbu**：主力写代码
- **libu**：补文档
- **gongbu**：部署和脚本
- **xingbu**：安全检查

可以先把：
- **hubu**
- **libu_hr**
- **zaochao**

放低优先级，后面再启用。

---

### 8. 最直接的一句话总结
你现在要做的不是“给每个 agent 都开飞书权限”，而是：

**先把 Edict 内部 agent 编排跑通 → 再接一个飞书机器人作为统一入口 → 再把代码任务从群里发进系统，由内部多 agent 自动分工。**

这样最稳，也最不乱。

# 记忆插件
## 访问`JIna`ai
[jina](https://jina.ai/)
## 登录注册

![[jina.png]]

- 得到`apikey`后
## 下载插件
[插件](https://github.com/CortexReach/memory-lancedb-pro)

## 在没有翻墙的电脑上
先在本地准备好 然后发送到对应电脑上
## 在对应电脑上的openclaw
```
{
  "plugins": {
    "load": {
      "paths": ["plugins/memory-lancedb-pro"]
    },
    "entries": {
      "memory-lancedb-pro": {
        "enabled": true
      }
    },
    "slots": {
      "memory": "memory-lancedb-pro"
    }
  }
}
```
- **修改配置文件**
- 重启`openclaw`
- **`slots.memory`“把这个插件设置记忆为第一位”**
==注意这里的插件存放的位置不重要而是这里的配置文件的paths重要需要指定==



# ollama接入openclaw

# OpenClaw 升级笔记（2026-03-24）
## 推荐方式（最省事）
在 OpenClaw 会话里直接让助手执行 `update.run`，会自动完成更新并重启 Gateway。

## 手动方式（命令行）

```bash
npm i -g openclaw@latest
```

升级后建议立刻做健康检查：
```bash
openclaw gateway status
openclaw status --deep
openclaw doctor --non-interactive
```

## 升级后排查顺序（遇到 502/异常时）
1. 先看服务是否正常：`openclaw gateway status`
2. 再看全局状态：`openclaw status --deep`
3. 最后看日志定位：`openclaw logs --follow`

## 经验
- 不要只看配置“看起来对”，升级或改配置后要做一次真实对话验证。
- 如果只改了配置但效果没变，优先执行一次 `openclaw gateway restart`。


# 浏览器自动化
## 安装MCP
[MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- 浏览器访问开启
```
chrome://inspect/#remote-debugging
```

![[自动化.png]]

# opencli
## 安装
[地址](https://github.com/jackwener/opencli)
```bash
npm install -g @jackwener/opencli
```
更新
```bash
npm install -g @jackwener/opencli@latest
```

## 使用
- 需要解压文件，然后添加到浏览器扩展中去，接着跑下面的命令
```bash
opencli doctor
```
- 这里需要显示成功才是正常了

==注意两个版本需要一致不然会出现错误==



