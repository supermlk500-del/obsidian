---
title: Windows 11 + WSL2 + Docker Desktop 部署 CLIProxyAPI / CPA Manager Plus
date: 2026-07-14
tags:
  - WSL2
  - Docker Desktop
  - CLIProxyAPI
  - CPA Manager Plus
  - Codex OAuth
  - Windows 代理
---

# Windows 11 + WSL2 + Docker Desktop 部署 CLIProxyAPI / CPA Manager Plus

> 本笔记记录一次完整部署过程，包括 WSL 清理、Docker Desktop 集成、7890 代理配置、CPA/CPAMP 安装、Codex OAuth 登录，以及“额度获取失败”的排查与修复。
>
> 环境：Windows 11、WSL2、Ubuntu 26.04、Docker Desktop、Windows 本地 HTTP/Mixed 代理端口 `7890`。

---

## 目录

- [1. 最终架构](#1-最终架构)
- [2. 清理旧 Ubuntu，保留 Ubuntu 26.04](#2-清理旧-ubuntu保留-ubuntu-2604)
- [3. 从 PowerShell 进入 WSL](#3-从-powershell-进入-wsl)
- [4. 切换 root 用户](#4-切换-root-用户)
- [5. 配置 Docker Desktop 的 WSL Integration](#5-配置-docker-desktop-的-wsl-integration)
- [6. 配置 WSL 镜像网络和自动代理](#6-配置-wsl-镜像网络和自动代理)
- [7. 修复 WSL 无网络和 DNS 丢失](#7-修复-wsl-无网络和-dns-丢失)
- [8. 验证 WSL 的 7890 代理](#8-验证-wsl-的-7890-代理)
- [9. 验证 Docker 环境](#9-验证-docker-环境)
- [10. 安装 CLIProxyAPI 和 CPA Manager Plus](#10-安装-cliproxyapi-和-cpa-manager-plus)
- [11. 清理误放在主目录中的配置文件](#11-清理误放在主目录中的配置文件)
- [12. 检查容器与访问管理面板](#12-检查容器与访问管理面板)
- [13. 完成 Codex OAuth 登录](#13-完成-codex-oauth-登录)
- [14. 修复“额度获取失败：auth token not found”](#14-修复额度获取失败auth-token-not-found)
- [15. 最终验证](#15-最终验证)
- [16. 常用运维命令](#16-常用运维命令)
- [17. 本次踩坑总结](#17-本次踩坑总结)
- [18. 安全注意事项](#18-安全注意事项)

---

## 1. 最终架构

最终使用的结构如下：

```text
Windows 11
├─ Docker Desktop
│  ├─ docker-desktop WSL 发行版
│  └─ Docker Engine
├─ Windows 本地代理
│  └─ HTTP / Mixed 端口：7890
└─ WSL2
   └─ Ubuntu-26.04
      └─ ~/cpa-manager-plus
         ├─ CLIProxyAPI 容器
         └─ CPA Manager Plus 容器
```

网络关系：

```text
WSL 内的 curl / apt / git
  └─ http://127.0.0.1:7890
     └─ Windows 本地代理

Docker 容器
  └─ http://host.docker.internal:7890
     └─ Windows 本地代理
```

关键区别：

- 在 WSL 镜像网络模式中，WSL 可以通过 `127.0.0.1:7890` 使用 Windows 上的代理。
- 在 Docker 容器中，`127.0.0.1` 指向容器本身。
- Docker 容器访问 Windows 主机代理，应使用：

```text
http://host.docker.internal:7890
```

![[最终环境与服务结构.png]]
---

## 2. 清理旧 Ubuntu，保留 Ubuntu 26.04

当 Windows 中同时存在：

```text
docker-desktop
Ubuntu
Ubuntu-26.04
```

目标是删除旧的 `Ubuntu`，保留 `Ubuntu-26.04`。

### 2.1 查看已安装的 WSL 发行版

在 Windows PowerShell 中执行：

```powershell
wsl -l -v
```

### 2.2 删除旧 Ubuntu

确认旧发行版名称确实是 `Ubuntu` 后执行：

```powershell
wsl --unregister Ubuntu
```

这条命令会永久删除旧 `Ubuntu` 发行版中的全部 Linux 文件、软件和配置。

不要误执行：

```powershell
wsl --unregister Ubuntu-26.04
```

### 2.3 设置默认发行版

```powershell
wsl --set-default Ubuntu-26.04
```

再次检查：

```powershell
wsl -l -v
```

![[清理后的 WSL 发行版列表.png]]

### 本步骤踩坑

- `wsl --unregister` 不是普通卸载，它会直接删除发行版数据。
- 发行版名称必须与 `wsl -l -v` 显示的名称完全一致。
- `docker-desktop` 是 Docker Desktop 使用的内部 WSL 发行版，不要删除。

---

## 3. 从 PowerShell 进入 WSL

进入默认 WSL：

```powershell
wsl
```

明确进入 Ubuntu 26.04：

```powershell
wsl -d Ubuntu-26.04
```

退出 WSL，返回 PowerShell：

```bash
exit
```

查看当前所在路径：

```bash
pwd
```

WSL 中常见路径：

```text
/home/<用户名>              Linux 用户主目录
/mnt/c/Users/<Windows用户> Windows C 盘用户目录
```

项目文件建议放在 Linux 文件系统中，例如：

```text
~/cpa-manager-plus
```

不建议长期放在：

```text
/mnt/c/Users/...
```

原因包括文件权限、I/O 性能和 Docker 挂载兼容性。



---

## 4. 切换 root 用户

在 Ubuntu 中切换到 root：

```bash
sudo -i
```

检查当前身份：

```bash
whoami
```

输出应为：

```text
root
```

退出 root：

```bash
exit
```

也可以从 PowerShell 直接以 root 身份进入指定发行版：

```powershell
wsl -d Ubuntu-26.04 -u root
```

日常操作建议使用普通用户。只在需要管理员权限时使用：

```bash
sudo <命令>
```

例如：

```bash
sudo apt update
```


### 本步骤踩坑

- 一直使用 root 容易导致项目文件所有者变成 `root`，后续普通用户无法编辑。
- Docker Desktop 的 WSL 集成通常不需要 `sudo docker ...`。
- 项目目录应由普通用户创建和维护。

---

## 5. 配置 Docker Desktop 的 WSL Integration

打开 Docker Desktop：

```text
Settings
→ Resources
→ WSL Integration
```

执行以下操作：

1. 开启默认 WSL 发行版集成。
2. 在发行版列表中开启 `Ubuntu-26.04`。
3. 点击 `Apply & restart`。

Docker Desktop 左下角应显示：

```text
Engine running
```

![[启用 Ubuntu-26.04 的 WSL Integration.png]]

### 验证 Docker 命令

进入 Ubuntu 后执行：

```bash
docker --version
docker compose version
```

再运行测试容器：

```bash
docker run --rm hello-world
```

成功时会显示：

```text
Hello from Docker!
```


![[Docker hello-world 测试成功.png]]

### 本步骤踩坑

不要在当前 Ubuntu 中重复安装另一套 Docker Engine：

```bash
sudo apt install docker.io
```

当前方案使用 Docker Desktop 提供的 Docker Engine。重复安装可能导致：

- `docker` 客户端连接到错误的 daemon；
- 两套容器和镜像互相不可见；
- Docker Compose 行为混乱；
- 权限和 socket 冲突。

---

## 6. 配置 WSL 镜像网络和自动代理

Windows 使用本地代理：

```text
127.0.0.1:7890
```

WSL 默认 NAT 模式下，可能出现警告：

```text
检测到 localhost 代理配置，但未镜像到 WSL。
NAT 模式下的 WSL 不支持 localhost 代理。
```

因此使用 WSL 镜像网络模式。

### 6.1 在 WSL 设置应用中配置

打开 Windows 的“适用于 Linux 的 Windows 子系统设置”，进入：

```text
网络
```

建议设置：

```text
网络模式：Mirrored
启用 localhost 转发：开
自动代理：开
DNS 相关选项：开
```

![[WSL 镜像网络和自动代理设置.png]]

![[wsl网络.png]]

### 6.2 使用 `.wslconfig` 配置

在 PowerShell 中：

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

保存后彻底关闭 WSL：

```powershell
wsl --shutdown
```

重新进入：

```powershell
wsl -d Ubuntu-26.04
```

### 本步骤踩坑

- 修改 WSL 网络配置后，只关闭终端窗口不够。
- 必须执行：

```powershell
wsl --shutdown
```

- 代理软件必须实际监听 `7890`。
- `7890` 应是 HTTP 端口或 Mixed 端口。若是纯 SOCKS 端口，URL 应改为 `socks5://...`。

---

## 7. 修复 WSL 无网络和 DNS 丢失

配置镜像网络后，曾出现以下错误：

```text
curl: (6) Could not resolve host: www.google.com
ping: connect: Network is unreachable
cat: /etc/resolv.conf: No such file or directory
```

这不是单纯的代理问题，因为：

- `ping 1.1.1.1` 不依赖 HTTP 代理；
- `Network is unreachable` 表示缺少可用网络路由；
- `/etc/resolv.conf` 不存在表示 DNS 配置没有生成。

### 7.1 重启并更新 WSL

先退出 Ubuntu：

```bash
exit
```

在 PowerShell 中：

```powershell
wsl --shutdown
wsl --update
wsl -d Ubuntu-26.04
```

### 7.2 检查网络接口、路由和 DNS

在 Ubuntu 中：

```bash
ip addr
ip route
ls -l /etc/resolv.conf
ping -c 3 1.1.1.1
```

正常结果应包括：

- 某个网络接口为 `UP`；
- 获得局域网 IP，例如 `192.168.1.x`；
- 存在默认路由，例如：

```text
default via 192.168.1.1 dev eth1
```

- `/etc/resolv.conf` 指向 WSL 生成的文件；
- `ping 1.1.1.1` 成功。

![[WSL 网络恢复后的检查结果.png]]


### 7.3 如果 `/etc/resolv.conf` 仍不存在

检查：

```bash
cat /etc/wsl.conf
```

如果存在：

```ini
[network]
generateResolvConf=false
```

编辑：

```bash
sudo nano /etc/wsl.conf
```

改为：

```ini
[network]
generateResolvConf=true
```

删除旧文件或错误链接：

```bash
sudo rm -f /etc/resolv.conf
```

退出 WSL：

```bash
exit
```

回到 PowerShell：

```powershell
wsl --shutdown
wsl -d Ubuntu-26.04
```

再次检查：

```bash
cat /etc/resolv.conf
ip route
```

### 本步骤踩坑

- `curl` 无法解析域名，不一定只是 DNS 问题；代理也可能参与域名解析。
- `ping 1.1.1.1` 可以区分“基础网络故障”和“DNS 故障”。
- 在 WSL 自动 DNS 模式下，不建议随意手写 `/etc/resolv.conf`。
- 先让 WSL 自动生成 DNS，再处理代理。

---

## 8. 验证 WSL 的 7890 代理

网络恢复后，先测试普通访问：

```bash
getent hosts www.microsoft.com
curl -I https://www.microsoft.com
```

再检查环境变量：

```bash
env | grep -i proxy
```

正常情况下会看到：

```text
http_proxy=http://127.0.0.1:7890
https_proxy=http://127.0.0.1:7890
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

测试结果中出现：

```text
HTTP/1.1 200 Connection established
```

表示 HTTP CONNECT 代理隧道建立成功。


### 临时手动设置代理

自动代理没有生效时，可临时执行：

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
export no_proxy=localhost,127.0.0.1
export NO_PROXY=localhost,127.0.0.1
```

测试：

```bash
curl -I https://www.google.com
```

### 本步骤踩坑

- `getent hosts` 没有输出，但 `curl` 成功时，可能是代理服务器代为解析域名。
- 可以使用以下命令测试不经过代理的直接连接：

```bash
curl --noproxy '*' -I https://www.microsoft.com
```

- 不要在 `~/.bashrc` 中重复写多套代理变量，否则以后更换代理端口时容易混乱。
- WSL 自动代理已正常工作时，不需要再手动永久写入代理变量。

---

## 9. 验证 Docker 环境

在 Ubuntu 中：

```bash
docker version
docker compose version
docker run --rm hello-world
```

查看 Docker Desktop 内部发行版：

```powershell
wsl -l -v
```

通常会看到：

```text
docker-desktop
Ubuntu-26.04
```

### 注意

WSL 的环境变量代理与 Docker 容器的代理不是同一个层级：

```text
WSL 进程 → 127.0.0.1:7890
Docker 容器 → host.docker.internal:7890
```

WSL 中能联网，不代表容器中的应用一定能联网。

---

## 10. 安装 CLIProxyAPI 和 CPA Manager Plus

项目建议安装到 Linux 用户主目录中。

### 10.1 创建临时安装目录

```bash
cd ~
mkdir -p cpa-install
cd cpa-install
```

### 10.2 下载安装脚本

```bash
curl -fsSLO https://raw.githubusercontent.com/seakee/CPA-Manager-Plus/main/bin/install-cpamp.sh
```

检查文件：

```bash
ls -lh install-cpamp.sh
```

### 10.3 运行安装脚本

```bash
bash install-cpamp.sh
```

安装选项：

```text
语言：简体中文
安装范围：CPA + CPAMP 完整安装
部署方式：Docker
安装目录：使用默认值
CPAMP 端口：18317
Docker 镜像：使用默认值
```

遇到以下提示时：

```text
CPAMP Docker 镜像 [seakee/cpa-manager-plus:latest]:
```

直接按 Enter。

CPA 镜像也使用默认值。

最后确认安装时，按脚本提示输入：

```text
confirm
```


![[参数选择.png]]

### 安装后的目录

正式目录通常为：

```text
~/cpa-manager-plus
```

临时安装脚本目录：

```text
~/cpa-install
```

---

## 11. 清理误放在主目录中的配置文件

曾从教程作者处另外下载：

```text
~/config.yaml
~/docker-compose.yml
```

同时 Windows 下载来源标记还产生了类似：

```text
config.yaml Zone.Identifier
docker-compose.yml Zone.Identifier
```

这些文件位于用户主目录，而安装脚本已经在正式项目目录中生成自己的配置，因此容易误用。

### 11.1 删除主目录中的额外配置

```bash
cd ~

rm -f config.yaml docker-compose.yml

find ~ -maxdepth 1 -type f \( \
  -name 'config.yaml*Zone.Identifier*' -o \
  -name 'docker-compose.yml*Zone.Identifier*' \
\) -delete
```

检查：

```bash
ls -la ~
```

不要删除：

```text
~/cpa-manager-plus
~/.docker
~/.config
~/.bashrc
~/.profile
```

安装完成后，临时目录可以删除：

```bash
rm -rf ~/cpa-install
```


### 本步骤踩坑

- 在 `~` 目录直接运行 `docker compose up -d` 时，Docker Compose 会优先寻找当前目录的 `docker-compose.yml`。
- 如果主目录残留教程作者的 Compose 文件，可能启动另一套错误服务。
- 正确做法是先进入正式目录：

```bash
cd ~/cpa-manager-plus
```

再运行 Docker Compose 命令。

---

## 12. 检查容器与访问管理面板

进入正式目录：

```bash
cd ~/cpa-manager-plus
```

查看服务：

```bash
docker compose ps
```

正常应看到两个容器处于 `Up` 或 `healthy`：

```text
cli-proxy-api
cpa-manager-plus
```

没有启动时：

```bash
docker compose up -d
docker compose ps
```

查看日志：

```bash
docker compose logs --tail=100
```

在 Windows 浏览器打开：

```text
http://localhost:18317/management.html
```

![[CPA 与 CPAMP 容器状态.png]]

登录页面会要求密钥

在wsl中执行
```shell
cd ~/cpa-manager-plus
cat secrets/cpamp-admin-key
```
此时输出的`cpamp`开头就是密钥了

### 如果浏览器显示 `ERR_CONNECTION_REFUSED`

检查：

```bash
cd ~/cpa-manager-plus
docker compose ps
docker compose logs --tail=100 cpa-manager-plus
```

还可以检查端口：

```bash
docker compose port cpa-manager-plus 18317
```

若容器正在运行但页面仍打不开，尝试：

```bash
docker compose restart cpa-manager-plus
```

---

## 13. 完成 Codex OAuth 登录

在管理面板中进入 Codex OAuth 页面，点击：

```text
开始 Codex 登录
```

打开生成的 OpenAI 授权链接，完成登录授权。

授权结束后，浏览器会跳转到类似：

```text
http://localhost:1455/auth/callback?code=...&state=...
```

此时浏览器可能显示：

```text
ERR_CONNECTION_REFUSED
```

这不一定表示 OAuth 失败。

### 正确处理方式

1. 保持 CPA Manager Plus 的 OAuth 页面打开。
2. 在报错页面按 `Ctrl + L`。
3. 复制地址栏中的完整回调 URL。
4. 返回 CPA Manager Plus。
5. 将完整 URL 粘贴到“回调 URL”输入框。
6. 点击“提交回调 URL”。
7. 等待认证状态变为成功。

必须复制的是：

```text
http://localhost:1455/auth/callback?code=...&state=...
```

不要复制最开始的：

```text
https://auth.openai.com/oauth/authorize?...
```

![[OAuth 回调页面连接被拒绝.png]]
![[手动提交 Codex OAuth 回调 URL.png]]
粘贴`http://localhost:1455/auth/callback?code=...&state=...`在回调url中
### 本步骤踩坑

- 回调 URL 中包含一次性授权码，不能重复使用。
- 出现 `state mismatch`、`expired` 或 `409` 时，应重新开始 OAuth。
- 不要把回调 URL、授权码或 Token 截图发给别人。
- 无需为了 `localhost:1455` 的报错直接关闭防火墙。
- 远程浏览器模式下，手动提交完整回调 URL 是正常流程。

---

## 14. 修复“额度获取失败：auth token not found”

OAuth 页面显示认证成功、认证文件也已生成，但额度页面仍出现：

```text
额度获取失败：auth token not found
```

### 14.1 查看容器日志

```bash
cd ~/cpa-manager-plus

docker compose images
docker compose logs --tail=120 cli-proxy-api
docker compose logs --tail=120 cpa-manager-plus
```

日志中出现了关键错误：

```text
Failed to exchange authorization code for tokens
Post "https://auth.openai.com/oauth/token":
dial tcp [IPv6 地址]:443: connect: network is unreachable
```

还出现：

```text
POST "/v0/management/api-call" 502
```

这说明：

- WSL 本身已经能通过 `127.0.0.1:7890` 上网；
- 但 CLIProxyAPI 运行在 Docker 容器中；
- 容器没有使用 WSL 的代理环境变量；
- 容器尝试直接使用 IPv6 访问 OpenAI；
- Docker 容器没有可用 IPv6 路由，因此失败；
- OAuth 文件可能生成了，但后续额度 API 访问仍失败。

### 14.2 测试 Docker 容器能否访问 Windows 代理

执行：

```bash
docker run --rm curlimages/curl:latest \
  -x http://host.docker.internal:7890 \
  -I https://auth.openai.com
```

第一次执行会拉取 `curlimages/curl` 镜像。

成功的关键标志：

```text
HTTP/1.1 200 Connection established
```

后面即使出现：

```text
HTTP/2 403
cf-mitigated: challenge
```

也不代表代理失败。

`403` 是因为 `curl` 直接访问登录站点，被 Cloudflare 浏览器验证拦截。只要出现 `200 Connection established`，就证明容器已经能够通过 Windows 的 7890 代理建立 HTTPS 隧道。

![[容器访问 Windows 7890 代理成功.png]]

### 14.3 为 CLIProxyAPI 配置容器代理

进入项目目录：

```bash
cd ~/cpa-manager-plus
```

先备份配置：

```bash
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

检查配置：

```bash
grep -n '^proxy-url:' cliproxyapi/config.yaml
```

应看到：

```yaml
proxy-url: "http://host.docker.internal:7890"
```


### 14.4 重启 CLIProxyAPI

```bash
docker compose restart cli-proxy-api
sleep 3
docker compose ps
```

检查容器内部读取到的配置：

```bash
docker compose exec cli-proxy-api \
  sh -c 'grep -n "^proxy-url:" /CLIProxyAPI/config.yaml'
```

查看最新日志：

```bash
docker compose logs --since=2m cli-proxy-api
```

回到浏览器：

1. 按 `Ctrl + Shift + R` 强制刷新页面。
2. 点击“刷新额度”。

修复后，额度页面应能正常显示。

### 本步骤最关键的坑

#### 坑 1：WSL 有代理，不等于容器有代理

以下配置只对 WSL 进程有效：

```text
http://127.0.0.1:7890
```

Docker 容器不能使用这个地址访问 Windows 代理。

#### 坑 2：容器中的 `127.0.0.1` 是容器自身

错误配置：

```yaml
proxy-url: "http://127.0.0.1:7890"
```

正确配置：

```yaml
proxy-url: "http://host.docker.internal:7890"
```

#### 坑 3：`HTTP/2 403` 不一定表示代理失败

测试 `auth.openai.com` 时：

```text
HTTP/1.1 200 Connection established
HTTP/2 403
cf-mitigated: challenge
```

含义是：

1. 代理隧道已建立；
2. 请求已到达 Cloudflare；
3. Cloudflare 因为请求不是正常浏览器而返回验证页面。

因此真正判断代理是否成功，要看：

```text
HTTP/1.1 200 Connection established
```

#### 坑 4：错误表象是 `auth token not found`，根因是网络

前端显示：

```text
auth token not found
```

但日志真正显示的是：

```text
connect: network is unreachable
```

排查此类问题必须优先看容器日志，而不是只看网页提示。

---

## 15. 最终验证

### 15.1 检查容器状态

```bash
cd ~/cpa-manager-plus
docker compose ps
```

### 15.2 检查代理配置

```bash
grep -n '^proxy-url:' cliproxyapi/config.yaml
```

### 15.3 检查最新错误

```bash
docker compose logs --since=10m cli-proxy-api | grep -iE \
'error|failed|unreachable|timeout|502'
```

没有输出通常表示近期没有匹配到这些错误。

### 15.4 检查面板

浏览器打开：

```text
http://localhost:18317/management.html
```

确认：

- 管理面板可访问；
- Codex 凭证存在；
- 凭证状态正常；
- 额度可以刷新；
- 容器日志不再出现 `network is unreachable`。

---

## 16. 常用运维命令

所有 Docker Compose 命令都建议先进入正式目录：

```bash
cd ~/cpa-manager-plus
```

### 查看容器状态

```bash
docker compose ps
```

### 启动服务

```bash
docker compose up -d
```

### 停止服务

```bash
docker compose down
```

### 重启全部服务

```bash
docker compose restart
```

### 只重启 CLIProxyAPI

```bash
docker compose restart cli-proxy-api
```

### 只重启 CPA Manager Plus

```bash
docker compose restart cpa-manager-plus
```

### 查看全部日志

```bash
docker compose logs --tail=200
```

### 实时查看 CLIProxyAPI 日志

```bash
docker compose logs -f cli-proxy-api
```

### 实时查看管理面板日志

```bash
docker compose logs -f cpa-manager-plus
```

### 更新镜像

```bash
docker compose pull
docker compose up -d
```

### 查看镜像版本

```bash
docker compose images
```

### 查看当前 Compose 配置

```bash
docker compose config
```

### 检查项目目录

```bash
find ~/cpa-manager-plus -maxdepth 2 -type f | sort
```

### 检查 WSL 代理

```bash
env | grep -i proxy
```

### 检查 WSL 网络

```bash
ip addr
ip route
cat /etc/resolv.conf
```

### 测试 WSL 网络

```bash
ping -c 3 1.1.1.1
curl -I https://www.microsoft.com
```

### 测试 Docker 容器代理

```bash
docker run --rm curlimages/curl:latest \
  -x http://host.docker.internal:7890 \
  -I https://auth.openai.com
```

---

## 17. 本次踩坑总结

| 现象 | 表面原因 | 实际原因 | 解决方案 |
|---|---|---|---|
| WSL 提示 localhost 代理未镜像 | WSL 不支持代理 | 使用 NAT 模式，WSL 无法直接访问 Windows localhost | 切换 `Mirrored`，开启 `autoProxy` |
| `ping: Network is unreachable` | DNS 或代理异常 | WSL 网络接口或默认路由未建立 | `wsl --shutdown`，更新并重启 WSL |
| `/etc/resolv.conf` 不存在 | DNS 文件被删除 | `generateResolvConf` 被禁用或 WSL 未重新生成 | 开启 `generateResolvConf=true` 后重启 WSL |
| WSL 可以 `curl`，Docker 容器仍失败 | OpenAI 服务异常 | 容器没有继承 WSL 代理 | 容器使用 `host.docker.internal:7890` |
| OAuth 跳转到 localhost:1455 后连接被拒绝 | OAuth 登录失败 | 浏览器无法直接连接容器中的临时回调服务 | 复制完整回调 URL，手动提交 |
| 额度页面显示 `auth token not found` | Token 文件坏了 | 后端容器无法访问 OpenAI Token/额度接口 | 查看日志并配置 `proxy-url` |
| 容器日志显示 IPv6 `network is unreachable` | DNS 解析错误 | 域名优先解析 IPv6，但容器无 IPv6 路由 | 让 CLIProxyAPI 通过代理访问 |
| 测试代理得到 HTTP 403 | 代理被拒绝 | Cloudflare 要求浏览器验证 | 看到 `200 Connection established` 即证明代理可用 |
| 主目录出现额外 `config.yaml` | 安装脚本重复生成 | 手动下载的教程配置文件放错位置 | 删除主目录额外文件，只使用正式项目目录 |
| 在任意目录执行 Compose 命令 | Docker 服务异常 | Compose 使用了当前目录下错误的 YAML | 始终先 `cd ~/cpa-manager-plus` |
| Ubuntu 中再次安装 `docker.io` | 认为 WSL 中没有 Docker | 忽略了 Docker Desktop 的 WSL Integration | 直接使用 Docker Desktop 提供的 Engine |

---

## 18. 安全注意事项

以下内容不要截图、上传到公开仓库或发送给别人：

```text
CPAMP 管理员密钥
CPA Management Key
客户端 API Key
OAuth 回调 URL
OAuth code
OAuth state
access_token
refresh_token
Codex 认证 JSON
完整 config.yaml
```

查看日志并准备分享时，可先过滤敏感信息：

```bash
docker compose logs --tail=200 cli-proxy-api \
  | sed -E \
    -e 's/(access_token["=: ]+)[^", ]+/\1***REDACTED***/Ig' \
    -e 's/(refresh_token["=: ]+)[^", ]+/\1***REDACTED***/Ig' \
    -e 's/(Authorization: Bearer )[A-Za-z0-9._-]+/\1***REDACTED***/Ig'
```

配置文件备份中也可能包含敏感数据：

```text
cliproxyapi/config.yaml.bak.*
```

不要将整个项目目录直接上传到公开 GitHub 仓库。

建议为项目目录设置合理权限：

```bash
chmod 700 ~/cpa-manager-plus
```

如果凭证目录存在，可进一步限制：

```bash
find ~/cpa-manager-plus -type d -name '*auth*' -exec chmod 700 {} \;
```

---

## 完成状态

最终完成了以下内容：

- [x] 删除旧 Ubuntu，保留 Ubuntu 26.04
- [x] 设置 Ubuntu 26.04 为默认 WSL
- [x] 配置 Docker Desktop WSL Integration
- [x] 开启 WSL Mirrored 网络
- [x] 开启 WSL 自动代理
- [x] 修复 WSL 网络和 DNS
- [x] 验证 WSL 使用 `127.0.0.1:7890`
- [x] 部署 CLIProxyAPI
- [x] 部署 CPA Manager Plus
- [x] 清理多余配置文件
- [x] 完成 Codex OAuth
- [x] 处理 localhost:1455 回调
- [x] 修复 Docker 容器无法使用代理
- [x] 配置 `host.docker.internal:7890`
- [x] 修复 Codex 额度获取失败

