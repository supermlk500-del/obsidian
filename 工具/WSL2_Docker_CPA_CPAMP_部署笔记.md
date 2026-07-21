---
title: Windows 11 + WSL2 + Docker Desktop 部署 CLIProxyAPI / CPA Manager Plus
date: 2026-07-14
tags:
  - WSL2
  - Docker Desktop
  - CLIProxyAPI
  - CPA Manager Plus
  - Codex OAuth
---

# Windows 11 + WSL2 + Docker Desktop 部署 CLIProxyAPI / CPA Manager Plus

本文记录一套可直接执行的部署流程。环境如下：

- Windows 11
- WSL2
- Ubuntu 26.04
- Docker Desktop
- Windows 本地 HTTP/Mixed 代理端口：`7890`

> 如果你的代理端口不是 `7890`，请把文中的 `7890` 全部替换成实际端口。

---

## 1. 部署结构

```text
Windows 11
├─ Docker Desktop
├─ 本地代理：127.0.0.1:7890
└─ WSL2
   └─ Ubuntu-26.04
      └─ ~/cpa-manager-plus
         ├─ CLIProxyAPI
         └─ CPA Manager Plus
```

代理地址分两种(要看自己的梯子是什么端口我的端口是7890)：

```text
WSL 内部程序：
http://127.0.0.1:7890

Docker 容器访问 Windows：
http://host.docker.internal:7890
```

![[最终环境与服务结构.png]]

---

## 2. 准备 Ubuntu 26.04

在 Windows PowerShell 中查看 WSL 发行版：

```powershell
wsl -l -v
```

如果同时存在旧的 `Ubuntu` 和新的 `Ubuntu-26.04`，并且已经确认旧发行版不再需要，可以删除旧发行版：

```powershell
wsl --unregister Ubuntu
```

设置 Ubuntu 26.04 为默认发行版：

```powershell
wsl --set-default Ubuntu-26.04
```

进入 Ubuntu：

```powershell
wsl -d Ubuntu-26.04
```

![[清理后的 WSL 发行版列表.png]]

后续命令使用普通 Linux 用户执行，不需要切换到 root。

---

## 3. 配置 WSL 网络和 Windows 代理

打开 Windows 的“适用于 Linux 的 Windows 子系统设置”，进入“网络”，设置：

```text
网络模式：Mirrored
启用 localhost 转发：开
自动代理：开
DNS 相关选项：开
```

![[WSL 镜像网络和自动代理设置.png]]
![[wsl网络.png]]

也可以在 PowerShell 中编辑：

```powershell
notepad $env:USERPROFILE\.wslconfig
```

写入：

```ini
[wsl2]
networkingMode=mirrored
autoProxy=true
dnsTunneling=true
```

保存后执行：

```powershell
wsl --shutdown
wsl -d Ubuntu-26.04
```

进入 Ubuntu 后检查网络：

```bash
ip route
ping -c 3 1.1.1.1
curl -I https://www.microsoft.com
env | grep -i proxy
```



![[WSL 网络恢复后的检查结果.png]]

---

## 4. 配置 Docker Desktop(在windows系统下下载docker)

打开 Docker Desktop，确认左下角显示：

```text
Engine running
```

进入：

```text
Settings
→ Resources
→ WSL Integration
```

开启：

```text
Ubuntu-26.04
```

点击：

```text
Apply & restart
```

![[启用 Ubuntu-26.04 的 WSL Integration.png]]

在 Docker Desktop 的代理设置中使用系统代理；如果系统代理未被识别，则手动填写：

```text
HTTP Proxy:  http://127.0.0.1:7890
HTTPS Proxy: http://127.0.0.1:7890
```

回到 Ubuntu，验证 Docker：

```bash
docker --version
docker compose version
docker run --rm hello-world
```

成功时会显示：

```text
Hello from Docker!
```

![[Docker hello-world 测试成功.png]]

> 直接使用 Docker Desktop 提供的 Docker Engine，不需要在 Ubuntu 中安装 `docker.io`。

---

## 5. 安装 CLIProxyAPI 和 CPA Manager Plus

在 Ubuntu 中执行：

```bash
cd ~
mkdir -p cpa-install
cd cpa-install
```

下载安装脚本：

```bash
curl -fsSLO https://raw.githubusercontent.com/seakee/CPA-Manager-Plus/main/bin/install-cpamp.sh
```

运行：

```bash
bash install-cpamp.sh
```

安装时选择：

```text
语言：简体中文
安装范围：CPA + CPAMP 完整安装
部署方式：Docker
安装目录：默认
CPAMP 端口：18317
Docker 镜像：默认
```

需要最终确认时输入：

```text
confirm
```

![[参数选择.png]]

安装完成后的正式目录通常为：

```text
~/cpa-manager-plus
```

进入正式目录：

```bash
cd ~/cpa-manager-plus
```

检查容器：

```bash
docker compose ps
```

应看到两个服务处于运行状态：

```text
cli-proxy-api
cpa-manager-plus
```

![[CPA 与 CPAMP 容器状态.png]]

---

## 6. 配置 CLIProxyAPI 的容器代理

WSL 中的 `127.0.0.1:7890` 不能直接用于 Docker 容器。CLIProxyAPI 容器应使用：

```text
http://host.docker.internal:7890
```

先验证容器可以连接 Windows 代理：

```bash
docker run --rm curlimages/curl:latest \
  -x http://host.docker.internal:7890 \
  -I https://auth.openai.com
```

只要输出包含：

```text
HTTP/1.1 200 Connection established
```

就说明代理隧道可用。

![[容器访问 Windows 7890 代理成功.png]]

备份 CLIProxyAPI 配置：

```bash
cd ~/cpa-manager-plus

cp cliproxyapi/config.yaml \
   cliproxyapi/config.yaml.bak.$(date +%Y%m%d-%H%M%S)
```

写入代理地址：

```bash
if grep -qE '^[[:space:]]*proxy-url:' cliproxyapi/config.yaml; then
  sed -i 's#^[[:space:]]*proxy-url:.*#proxy-url: "http://host.docker.internal:7890"#' \
    cliproxyapi/config.yaml
else
  printf '\nproxy-url: "http://host.docker.internal:7890"\n' \
    >> cliproxyapi/config.yaml
fi
```

检查：

```bash
grep -n '^proxy-url:' cliproxyapi/config.yaml
```

应显示：

```yaml
proxy-url: "http://host.docker.internal:7890"
```

重启 CLIProxyAPI：

```bash
docker compose restart cli-proxy-api
sleep 3
docker compose ps
```

确认容器读取到配置：

```bash
docker compose exec cli-proxy-api \
  sh -c 'grep -n "^proxy-url:" /CLIProxyAPI/config.yaml'
```

---

## 7. 登录 CPA Manager Plus

在 Windows 浏览器打开：

```text
http://localhost:18317/management.html
```

读取 CPAMP 管理员密钥：

```bash
cd ~/cpa-manager-plus
cat secrets/cpamp-admin-key
```

复制输出的完整 `cpamp_...` 密钥并登录。

三个密钥用途不同：

```text
secrets/cpamp-admin-key
用于登录 CPA Manager Plus

secrets/cpa-management-key
用于 CPA 管理接口

secrets/cpa-demo-client-key
用于示例客户端 API 调用
```

登录管理面板时使用：

```text
secrets/cpamp-admin-key
```


---

## 8. 完成 Codex OAuth

在管理面板中进入 Codex OAuth 页面，点击：

```text
开始 Codex 登录
```

打开生成的授权链接，并完成 OpenAI 登录。

授权完成后，浏览器会跳转到类似：

```text
http://localhost:1455/auth/callback?code=...&state=...
```

浏览器可能显示无法访问该页面。此时：

1. 按 `Ctrl + L` 选中地址栏。
2. 复制完整的回调 URL。
3. 返回 CPA Manager Plus 的 OAuth 页面。
4. 粘贴到“回调 URL”输入框。
5. 点击“提交回调 URL”。
6. 等待认证成功。

![[OAuth 回调页面连接被拒绝.png]]

![[手动提交 Codex OAuth 回调 URL.png]]

需要粘贴的是完整地址：

```text
http://localhost:1455/auth/callback?code=...&state=...
```

回调 URL 含有一次性授权信息，不要公开或重复使用。

---

## 9. 验证部署结果

检查容器：

```bash
cd ~/cpa-manager-plus
docker compose ps
```

检查代理配置：

```bash
grep -n '^proxy-url:' cliproxyapi/config.yaml
```

检查最近日志：

```bash
docker compose logs --since=10m cli-proxy-api
```

打开管理页面：

```text
http://localhost:18317/management.html
```

确认以下项目：

- CPA Manager Plus 可以正常登录；
- Codex 凭证已经生成；
- 凭证状态正常；
- Codex 额度可以刷新；
- CLIProxyAPI 日志没有持续网络错误。

---

## 10. 常用管理命令

先进入项目目录：

```bash
cd ~/cpa-manager-plus
```

查看状态：

```bash
docker compose ps
```

启动：

```bash
docker compose up -d
```

停止：

```bash
docker compose down
```

重启全部服务：

```bash
docker compose restart
```

查看日志：

```bash
docker compose logs --tail=200
```

实时查看 CLIProxyAPI 日志：

```bash
docker compose logs -f cli-proxy-api
```

更新镜像：

```bash
docker compose pull
docker compose up -d
```

查看镜像：

```bash
docker compose images
```

验证容器代理：

```bash
docker run --rm curlimages/curl:latest \
  -x http://host.docker.internal:7890 \
  -I https://auth.openai.com
```

---

## 完成状态

- [x] Ubuntu 26.04 已设为默认 WSL
- [x] WSL Mirrored 网络已启用
- [x] WSL 自动代理已启用
- [x] Docker Desktop WSL Integration 已启用
- [x] Docker Engine 工作正常
- [x] CLIProxyAPI 已部署
- [x] CPA Manager Plus 已部署
- [x] CLIProxyAPI 容器代理已配置
- [x] CPAMP 管理员密钥已获取
- [x] Codex OAuth 已完成
- [x] Codex 额度可以正常刷新
