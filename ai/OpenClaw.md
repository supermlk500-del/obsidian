[[https://docs.openclaw.ai/]]网址
注意在安装飞书插件后 请跳到标题2 因为我电脑已经安装过一遍 第二遍会不一样
# 安装
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