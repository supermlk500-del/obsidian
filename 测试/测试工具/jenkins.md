在wsl中linux子系统安装jenkins
![[wsl中java版本.png]]



# Jenkins 安装、配置与踩坑记录

> 本笔记根据本次实际聊天过程整理，记录从 Windows Jenkins 迁移到 WSL Ubuntu，到 Jenkins 正常运行、改端口、配置代理、修复插件和完成中文界面的全过程。
>
> 最终目标：为后续的 Git、Python、Pytest、Allure 自动化测试准备 Jenkins 环境。

---

## 一、最终环境结构

本次最终使用的结构：

~~~text
Windows
├── 浏览器：访问 Jenkins
├── Clash：提供外网代理，端口 7890
└── WSL2
    └── Ubuntu 26.04
        ├── Java 21
        ├── Jenkins
        ├── Git
        ├── Python
        ├── Pytest
        └── Allure（后续使用）
~~~

Jenkins 最初使用默认端口 8080，后来为了避免与 Spring Boot、Tomcat 等项目冲突，改成了 8088。

最终访问地址：

~~~text
http://localhost:8088
~~~

Jenkins 虽然运行在 WSL Ubuntu 中，但 Windows 浏览器可以通过 localhost 访问。

### 截图占位：最终运行环境

- 截图页面：Windows 浏览器中的 Jenkins 首页。
- 必须包含：地址栏中的 http://localhost:8088，以及 Jenkins 首页。
- 可以裁掉：浏览器收藏夹、无关窗口和个人信息。
- 建议文件名：jenkins-01-最终运行环境.png

---

## 二、为什么选择 WSL 中的 Jenkins

Windows 原生 Jenkins 安装简单，但公司的 Jenkins 更多运行在 Linux 服务器中。

WSL 的优势：

- 可以练习 Linux 命令；
- 可以练习 systemd 服务管理；
- 路径、权限、Shell 环境更接近真实服务器；
- 以后使用 Git、Python、Pytest、Docker、Pipeline 更自然；
- 学到的命令更容易迁移到公司 Linux 环境。

最终学习链路是：

~~~text
Git 拉取代码
    ↓
Jenkins Job 或 Pipeline
    ↓
Python 虚拟环境
    ↓
pytest 执行测试
    ↓
Allure 生成报告
~~~

---

## 三、卸载 Windows Jenkins

### 1. 卸载软件

在 Windows 中：

~~~text
Win + R
→ 输入 appwiz.cpl
→ 找到 Jenkins
→ 卸载
~~~

卸载后，可以在管理员 PowerShell 中检查 Jenkins 服务：

~~~powershell
Get-Service Jenkins -ErrorAction SilentlyContinue
~~~

如果没有输出，说明 Windows Jenkins 服务已经不存在。

再检查 8080 是否还被占用：

~~~powershell
netstat -ano | findstr :8080
~~~

### 2. 这里的坑

“卸载 Jenkins 软件”和“删除 Jenkins 数据”不是一回事。

如果 Jenkins 中已经有重要的 Job、插件、凭据或 Pipeline，不要随便删除 Jenkins 数据目录。

本次属于刚开始学习、没有重要 Job 的环境，所以后面才可以重置 Jenkins Home。

### 截图占位：Windows Jenkins 卸载完成

- 截图页面：Windows“程序和功能”，或 PowerShell 检查服务。
- 必须包含：找不到 Jenkins，或 Get-Service Jenkins 没有输出。
- 可以裁掉：其他软件列表、用户名和无关窗口。
- 建议文件名：jenkins-02-windows版本卸载.png

---

## 四、进入 WSL 并确认 systemd

在 Windows PowerShell 中查看 WSL：

~~~powershell
wsl -l -v
~~~

进入 Ubuntu：

~~~powershell
wsl -d Ubuntu-26.04
~~~

进入 Ubuntu 后查看系统信息：

~~~bash
cat /etc/os-release
~~~

检查第 1 号进程：

~~~bash
ps -p 1 -o comm=
~~~

理想结果：

~~~text
systemd
~~~

systemd 是 Linux 中负责启动和管理服务的系统。Jenkins 安装成 Linux 服务以后，通常使用以下命令：

~~~bash
sudo systemctl start jenkins
sudo systemctl stop jenkins
sudo systemctl restart jenkins
sudo systemctl status jenkins
~~~

### 截图占位：WSL 和 systemd

- 截图页面：Ubuntu 终端。
- 必须包含：wsl -l -v 的 Ubuntu 状态，以及 ps -p 1 -o comm= 输出 systemd。
- 可以裁掉：当前用户名和无关路径。
- 建议文件名：jenkins-03-wsl-systemd检查.png

---

## 五、忘记 Ubuntu 的 sudo 密码

这里要先分清楚：

- Ubuntu sudo 密码：用于执行 sudo 命令；
- Jenkins 网页密码：用于登录 Jenkins；
- 两者不是同一个密码。

### 1. 以 root 进入 WSL

先退出普通 Ubuntu，然后在 Windows PowerShell 中执行：

~~~powershell
wsl -d Ubuntu-26.04 -u root
~~~

查看普通用户：

~~~bash
ls /home
~~~

假设用户名为自己的 WSL 用户名，执行：

~~~bash
passwd 用户名
~~~

输入两遍新密码。

Linux 输入密码时屏幕不会显示字符，也不会显示星号，这是正常现象。

退出 root：

~~~bash
exit
~~~

重新进入 Ubuntu：

~~~powershell
wsl -d Ubuntu-26.04
~~~

验证 sudo：

~~~bash
sudo whoami
~~~

如果输出：

~~~text
root
~~~

说明 sudo 密码已经恢复。

### 2. 修改 sudo 密码不会影响 Docker

修改 Linux 用户密码不会删除：

- Docker 容器；
- Docker 镜像；
- Docker Volume；
- Docker 网络；
- WSL 文件；
- Docker Desktop 配置。

绝对不要把下面命令当成普通退出或重置命令：

~~~powershell
wsl --unregister Ubuntu-26.04
~~~

这个命令会删除整个 Ubuntu 发行版及其数据。

---

## 六、安装 Java 21

先更新软件源：

~~~bash
sudo apt update
~~~

安装 Java：

~~~bash
sudo apt install -y fontconfig openjdk-21-jre
~~~

如果系统只有 headless 版本，也可以安装：

~~~bash
sudo apt install -y fontconfig openjdk-21-jre-headless
~~~

检查版本：

~~~bash
java -version
~~~

本次确认使用的是 Java 21。

Jenkins 运行在 Java 虚拟机上，Java 版本不满足要求时，Jenkins 可能无法启动或插件无法正常工作。

### 已插入图片：Java 21

这是本次实际安装过程中保存的 Java 版本截图：

![[wsl中java版本.png]]

图片中可以看到 OpenJDK 21.0.11，说明 WSL Ubuntu 中的 Java 环境已经准备完成。

---

## 七、添加 Jenkins 软件源并安装

创建密钥目录：

~~~bash
sudo mkdir -p /etc/apt/keyrings
~~~

下载 Jenkins 软件源密钥：

~~~bash
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
~~~

添加 Jenkins LTS 软件源：

~~~bash
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" \
| sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
~~~

更新软件源：

~~~bash
sudo apt update
~~~

安装 Jenkins：

~~~bash
sudo apt install -y jenkins
~~~

设置 Jenkins 随 Ubuntu 服务启动：

~~~bash
sudo systemctl enable jenkins
~~~

启动 Jenkins：

~~~bash
sudo systemctl start jenkins
~~~

查看状态：

~~~bash
sudo systemctl status jenkins
~~~

成功标志：

~~~text
Active: active (running)
~~~

第一次安装时，Jenkins 默认监听 8080：

~~~bash
ss -lntp | grep 8080
~~~

### 截图占位：Jenkins 服务启动

- 截图页面：Ubuntu 终端中的 systemctl status jenkins。
- 必须包含：jenkins.service、Active: active (running)、8080 监听结果。
- 可以裁掉：无关日志和用户路径。
- 建议文件名：jenkins-05-服务启动成功.png

---

## 八、首次打开 Jenkins

浏览器访问：

~~~text
http://localhost:8080
~~~

首次进入会出现：

~~~text
Unlock Jenkins
~~~

在 Ubuntu 中获取初始管理员密码：

~~~bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
~~~

把密码复制到网页中。

### 已插入图片：当前 Jenkins 登录页

这是当前 Jenkins 在 8088 端口运行时自动截取的真实登录页面：

![[jenkins-login-当前实景.png]]

注意：这张图是登录页，不是首次安装时的 Unlock Jenkins 页面。首次初始化截图仍需要保留原始截图后再补入。

### 1. 安装推荐插件

进入插件选择页面后选择：

~~~text
Install suggested plugins
安装推荐的插件
~~~

推荐插件一般会包含：

- Git；
- Pipeline；
- Credentials；
- SSH 相关组件；
- 构建工具；
- 中文本地化插件等。

### 2. 创建管理员用户

随后创建 Jenkins 网页管理员账号。

注意：这个账号密码和 Ubuntu sudo 密码不同。

### 3. 配置 Jenkins URL

第一次可以先使用：

~~~text
http://localhost:8080/
~~~

之后改端口时再更新访问地址。

### 已插入图片：当前 Jenkins 工作台

这是当前登录后的 Jenkins 工作台实景，地址为 8088：

![[jenkins-workspace-current.png]]

### 截图占位：首次初始化

- 截图页面：Unlock Jenkins、推荐插件安装、创建管理员用户。
- 必须包含：页面标题和当前操作按钮。
- 必须遮挡：初始密码、网页密码、邮箱、Token。
- 建议文件名：jenkins-06-首次初始化向导.png

---

## 九、把 Jenkins 端口从 8080 改成 8088

### 1. 为什么改端口

8080 是 Spring Boot、Tomcat 等项目的常用端口。

为了避免 Jenkins 和后端项目冲突，最终采用：

~~~text
Jenkins：8088
Spring Boot：8080
~~~

### 2. 不要直接修改 Jenkins 自带 service 文件

不要直接修改：

~~~text
/lib/systemd/system/jenkins.service
~~~

因为软件升级可能覆盖这个文件。

推荐使用 systemd override，也就是为原服务增加一个单独的覆盖配置。

### 3. 本次最终使用的命令

创建配置目录：

~~~bash
sudo mkdir -p /etc/systemd/system/jenkins.service.d
~~~

写入端口配置：

~~~bash
echo -e '[Service]\nEnvironment="JENKINS_PORT=8088"' | \
sudo tee /etc/systemd/system/jenkins.service.d/override.conf
~~~

重新加载 systemd：

~~~bash
sudo systemctl daemon-reload
~~~

重启 Jenkins：

~~~bash
sudo systemctl restart jenkins
~~~

查看服务：

~~~bash
sudo systemctl status jenkins
~~~

检查 8088：

~~~bash
ss -lntp | grep 8088
~~~

也可以同时检查 8080 和 8088：

~~~bash
ss -lntp | grep -E '8080|8088'
~~~

最后访问：

~~~text
http://localhost:8088
~~~

### 4. 如果使用 systemctl edit

也可以执行：

~~~bash
sudo systemctl edit jenkins
~~~

写入：

~~~ini
[Service]
Environment="JENKINS_PORT=8088"
~~~

nano 保存退出：

~~~text
Ctrl + O → Enter → Ctrl + X
~~~

然后执行：

~~~bash
sudo systemctl daemon-reload
sudo systemctl restart jenkins
~~~

### 截图占位：端口改为 8088

- 截图页面：override.conf 内容、Jenkins 状态和端口检查。
- 必须包含：JENKINS_PORT=8088、Active: active (running)、8088 监听结果。
- 可以裁掉：用户名、无关日志。
- 建议文件名：jenkins-07-端口改为8088.png

---

## 十、第一次插件安装失败：根因是网络和代理

### 1. 表面现象

第一次安装推荐插件时，出现大量红色或粉红色错误：

- Git Plugin 加载失败；
- Pipeline 加载失败；
- Credentials Binding Plugin 加载失败；
- JUnit Plugin 加载失败；
- Email Extension Plugin 连带失败；
- 中文插件或其他插件状态异常。

### 2. 日志中最重要的错误

~~~text
Failed to update the default Update Site 'default'
java.net.SocketException: Connection reset
~~~

Connection reset 的意思是连接被重置，表示 Jenkins 下载插件或插件依赖时网络连接中途断开。

### 3. 为什么会出现大量插件错误

很多插件并不是自己坏了，而是底层依赖没有下载成功。

例如：

~~~text
credentials 缺失
    ↓
Credentials Binding 失败
    ↓
Git Plugin 加载失败
~~~

~~~text
jackson2-api 缺失
    ↓
JJWT、GitHub API、Gradle、Pipeline Model API 等插件连锁失败
~~~

~~~text
workflow-durable-task-step 缺失
    ↓
Pipeline Basic Steps 失败
    ↓
Pipeline 失败
~~~

因此，看到很多红色插件时，不要认为是很多个独立故障。应该先找最底层的网络错误或依赖错误。

### 截图占位：插件加载失败

- 截图页面：Installed plugins 页面，或 Ubuntu 中的 Jenkins 日志。
- 必须包含：Connection reset、Failed to update、Plugin is missing 等文字。
- 必须遮挡：密码、Token 和敏感服务器信息。
- 建议文件名：jenkins-08-插件依赖失败.png

---

## 十一、确认 Ubuntu 能联网，但 Jenkins 没有继承代理

在 Ubuntu 中执行：

~~~bash
curl -I https://updates.jenkins.io/update-center.json
curl -I https://updates.jenkins.io
env | grep -i proxy
sudo systemctl show jenkins -p Environment
~~~

本次 curl 能正常访问，出现过：

~~~text
HTTP/1.1 200 Connection established
HTTP/2 301
location: https://updates.jenkins.io/current/update-center.json
~~~

这里的 301 是重定向，不是失败。

终端环境中可以看到代理：

~~~text
HTTP_PROXY=http://172.19.208.1:7890
HTTPS_PROXY=http://172.19.208.1:7890
~~~

问题在于：

~~~text
Ubuntu 用户终端
    ↓
继承了代理环境变量
    ↓
curl 可以联网

Jenkins systemd 服务
    ↓
不会自动继承当前终端的代理变量
    ↓
插件下载 Connection reset
~~~

这次排查得到的关键经验：

> 终端里的命令能联网，不代表由 systemd 启动的服务也能联网。

### 截图占位：代理排查命令

- 截图页面：Ubuntu 终端。
- 必须包含：curl 返回结果、proxy 环境变量、systemctl show jenkins 的结果。
- 必须遮挡：如果输出中出现账号、密码或 Token，必须打码。
- 建议文件名：jenkins-09-代理排查.png

---

## 十二、在 Jenkins 中配置 HTTP Proxy

进入：

~~~text
Manage Jenkins
→ System
→ HTTP Proxy Configuration
~~~

中文界面通常是：

~~~text
系统管理
→ 系统配置
→ HTTP Proxy Configuration
~~~

填写：

~~~text
Server：172.19.208.1
Port：7890
Username：留空
Password：留空
~~~

No Proxy Host 可以填写：

~~~text
localhost
127.0.0.1
::1
~~~

如果有测试 URL，填写：

~~~text
https://updates.jenkins.io/update-center.json
~~~

点击：

~~~text
Validate Proxy
验证代理
~~~

显示 Success 或 HTTP 200 后保存。

然后进入：

~~~text
Manage Jenkins
→ Plugins
→ Available plugins
~~~

如果插件列表可以正常加载，就说明 Jenkins 已经可以访问 Update Center。

### 已插入图片：插件管理页面

这是当前登录后的插件管理页面实景：

![[jenkins-plugins-current.png]]

这张图能帮助回忆插件管理页面的入口、Updates、Available plugins 和 Installed plugins 的位置；具体插件依赖错误仍应使用错误发生时的原始截图。

当前已安装插件页面实景：

![[jenkins-installed-current.png]]

### 这里的坑

Jenkins 页面能够打开，只代表 Jenkins 服务和端口正常，不代表 Jenkins 能访问外网。

需要分开判断：

~~~text
Jenkins 页面打不开
→ 查 systemd、服务状态和端口

Jenkins 页面能打开，但插件下载失败
→ 查 Update Center、代理、Clash 和网络
~~~

### 截图占位：HTTP Proxy 配置成功

- 截图页面：System → HTTP Proxy Configuration。
- 必须包含：Server、Port、No Proxy Host、验证成功结果。
- 必须遮挡：代理账号和密码；本次为空也要注意不要显示其他敏感信息。
- 建议文件名：jenkins-10-http代理配置.png

---

## 十三、插件依赖问题的正确处理方式

代理配置成功后，不要看到红色插件就随便卸载或禁用。

先查看：

~~~text
Failed to load
Plugin is missing
This plugin cannot be disabled
~~~

本次遇到的底层插件包括：

~~~text
Credentials
Jackson 2 API
Plain Credentials
Pipeline: Nodes and Processes
~~~

对应的依赖名称包括：

~~~text
credentials
jackson2-api
plain-credentials
workflow-durable-task-step
~~~

### 1. Credentials Binding 缺少 SSH Credentials

曾经看到：

~~~text
Credentials Binding Plugin
缺少 ssh-credentials
~~~

处理方式：

~~~text
Available plugins
→ 搜索 SSH Credentials
→ 安装
→ 重启 Jenkins
→ 再检查 Credentials Binding
~~~

### 2. JUnit 缺少 ECharts API

曾经看到：

~~~text
JUnit Plugin
Plugin is missing: echarts-api
~~~

处理方式：

~~~text
Available plugins
→ 搜索 ECharts API
→ 安装
→ 重启 Jenkins
→ 再检查 JUnit
→ 再检查 Email Extension
~~~

依赖关系可以理解为：

~~~text
ECharts API
    ↓
JUnit Plugin
    ↓
Email Extension Plugin
~~~

### 3. 灰色禁用开关不是错误

如果看到：

~~~text
This plugin cannot be disabled
It has one or more enabled dependents.
~~~

意思是：

> 这个插件被其他已启用插件依赖，所以不能禁用。

这不是插件加载失败。

Installed plugins 中红色圆圈 x 通常是卸载入口，也不等于当前插件一定坏了。

### 插件排错原则

1. 先看最底层依赖错误；
2. 不要被上层连锁错误带偏；
3. 插件安装成功不代表插件已经成功加载；
4. 被依赖的插件禁用开关变灰是正常现象；
5. 真正的加载失败通常会出现 Failed to load 或 Plugin is missing；
6. 不要为了“看起来干净”随便卸载底层插件。

### 截图占位：插件依赖恢复

- 截图页面：Installed plugins 中 Credentials、Credentials Binding、SSH Credentials、JUnit 等插件状态。
- 必须包含：插件名称、Health、启用状态或错误提示消失。
- 可以裁掉：无关插件和大量空白区域。
- 建议文件名：jenkins-11-插件依赖恢复.png

---

## 十四、插件太多错误后，从头初始化 Jenkins

当时插件已经出现大量依赖错误，继续一个个补依赖效率很低。

因为这是刚安装的学习环境，没有重要 Job、凭据和 Pipeline，所以决定清空 Jenkins Home 后重新初始化。

### 1. 先备份代理配置

停止 Jenkins：

~~~bash
sudo systemctl stop jenkins
~~~

备份 proxy.xml：

~~~bash
sudo cp /var/lib/jenkins/proxy.xml /tmp/jenkins-proxy.xml
~~~

proxy.xml 保存的是 Jenkins 页面中配置的 HTTP Proxy。

### 2. 清空 Jenkins Home

~~~bash
sudo rm -rf /var/lib/jenkins/*
~~~

### 重要警告

这条命令会删除：

- 已安装插件；
- 管理员账号；
- Jenkins 初始化状态；
- Job；
- Pipeline；
- 凭据；
- Jenkins 全局配置；
- 插件缓存。

它不会删除：

- Java；
- Jenkins 软件包；
- WSL Ubuntu；
- Docker 容器和镜像；
- Windows 文件；
- systemd override 中的 8088 端口配置。

所以这条命令只适合刚安装、没有重要 Jenkins 数据的学习环境。

### 3. 恢复代理并修复权限

~~~bash
sudo cp /tmp/jenkins-proxy.xml /var/lib/jenkins/proxy.xml
sudo chown -R jenkins:jenkins /var/lib/jenkins
~~~

启动 Jenkins：

~~~bash
sudo systemctl start jenkins
sudo systemctl status jenkins
~~~

重新访问：

~~~text
http://localhost:8088
~~~

重新读取初始密码：

~~~bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
~~~

然后重新选择：

~~~text
Install suggested plugins
安装推荐的插件
~~~

由于代理配置已经恢复，重新安装推荐插件时可以正常下载依赖。

### 4. 清空后浏览器还停在旧插件页面

清空 Jenkins Home 后，浏览器可能仍然停留在：

~~~text
http://localhost:8088/manage/pluginManager/installed
~~~

此时看到：

~~~text
No plugins installed
~~~

不一定代表重装失败，可能只是浏览器还停留在旧插件页面。

应该回到根地址：

~~~text
http://localhost:8088/
~~~

必要时强制刷新：

~~~text
Ctrl + Shift + R
~~~

### 截图占位：重新初始化成功

- 截图页面：清空后重新出现的 Unlock Jenkins 和推荐插件安装页面。
- 必须包含：8088 地址、Unlock Jenkins 或插件安装进度。
- 必须遮挡：初始密码和管理员密码。
- 建议文件名：jenkins-12-重新初始化.png

---

## 十五、安装并确认中文界面

Jenkins 没有单独的“中文版安装包”，而是通过本地化插件完成中文显示。

主要插件：

~~~text
Localization: Chinese (Simplified)
~~~

检查路径：

~~~text
Manage Jenkins
→ Plugins
→ Installed plugins
→ 搜索 Chinese 或 Localization
~~~

如果没有安装：

~~~text
Available plugins
→ 搜索 Localization: Chinese (Simplified)
→ 安装
~~~

如果安装后仍然是英文，可以安装 Locale 插件，并设置：

~~~text
zh_CN
~~~

### 汉化不是 100%

本次最终出现了部分中文、部分英文，这是正常的：

- System 可能显示为“系统配置”；
- Tools 可能显示为“全局工具配置”；
- Plugins 可能显示为“插件管理”；
- Clouds 可能仍然是英文；
- Appearance 可能仍然是英文；
- 第三方插件页面可能仍然是英文；
- Pipeline 错误和 Console Output 可能仍然是英文；
- Git、Python 等命令输出不会自动翻译。

翻译是否完整，取决于 Jenkins 核心和每个插件有没有对应语言包。

### 截图占位：中文界面

- 截图页面：Manage Jenkins / 系统管理首页。
- 必须包含：系统配置、全局工具配置、插件管理等中文菜单。
- 可以保留：Clouds、Appearance 等仍然为英文的真实情况。
- 建议文件名：jenkins-13-中文界面.png

---

## 十六、Manage Jenkins 页面重点

### 1. System / 系统配置

用于 Jenkins 的全局设置：

- Jenkins URL；
- 系统消息；
- 环境变量；
- HTTP Proxy；
- 全局属性；
- 插件提供的全局设置。

本次代理配置就在这里完成。

当前系统配置页面实景：

![[jenkins-system-current.png]]

### 2. Tools / 全局工具配置

告诉 Jenkins Git、JDK、Maven、Gradle、Allure 等工具在哪里。

后面运行 Git、Python、Pytest、Allure 时，经常需要进入 Tools 配置。

当前全局工具配置页面实景：

![[jenkins-tools-current.png]]

### 3. Plugins / 插件管理

用于：

- 安装插件；
- 更新插件；
- 启用插件；
- 禁用插件；
- 卸载插件。

### 4. Nodes and Clouds / 节点和云管理

Jenkins 可以把构建任务交给其他机器的 Agent：

~~~text
Jenkins Controller
    ├── Linux Agent
    ├── Windows Agent
    └── Docker Agent
~~~

当前个人学习环境直接使用 Built-In Node 即可。

### 5. Clouds

用于连接云环境、Kubernetes，根据任务动态创建 Agent。当前不用研究。

### 6. Appearance

用于主题和界面显示设置。

### 7. Global Security / 全局安全配置

用于控制登录、Job 权限、构建权限、认证方式、权限策略和 CSRF 等安全设置。

个人学习环境保持默认即可。

### 8. Credentials / 凭据管理

不要把账号密码直接写进 Pipeline 或脚本，而是放在 Jenkins Credentials 中，再通过 credentialsId 引用。

常见凭据：

- GitHub Token；
- Gitee Token；
- Git 用户名密码；
- SSH 私钥；
- 测试环境账号；
- Docker Registry 凭据。

### 9. 顶部橙色警告

内容类似：

~~~text
Building on the built-in node can be a security issue.
You should set up distributed builds.
~~~

意思是当前 Jenkins 控制器同时承担构建任务，正式环境更建议使用 Agent。

本次是个人学习环境，直接使用 Built-In Node 可以暂时忽略。

### 10. 顶部蓝色 CSP 提示

CSP 是 Content Security Policy，中文是内容安全策略，用于防止 XSS 和恶意脚本。

它和 Jenkins 启动、Git 拉取、pytest 执行、Pipeline 运行没有直接关系，学习环境可以暂时忽略。

### 截图占位：Manage Jenkins 总览

- 截图页面：Manage Jenkins / 系统管理首页。
- 必须包含：System、Tools、Plugins、Nodes、Credentials 等入口。
- 可以裁掉：个人头像、浏览器其他标签页和无关提示。
- 建议文件名：jenkins-14-系统管理入口.png

当前 Manage Jenkins 页面实景：

![[jenkins-manage-current.png]]

---

## 十七、电脑重启后 Jenkins 是否需要手动启动

### 1. Jenkins 服务层面

执行过：

~~~bash
sudo systemctl enable jenkins
~~~

表示只要 Ubuntu 发行版启动，systemd 就会自动启动 Jenkins。

确认：

~~~bash
systemctl is-enabled jenkins
~~~

如果输出：

~~~text
enabled
~~~

说明 Jenkins 已经配置为自动启动。

### 2. Windows 和 WSL 是两层

真实关系：

~~~text
Windows 重启
    ↓
WSL Ubuntu 是否启动
    ↓
systemd 是否启动
    ↓
Jenkins 是否启动
~~~

enable 只解决 Ubuntu 启动后 Jenkins 自动启动，不一定保证 Windows 登录后 WSL 立即自动运行。

学习阶段的做法：

1. Windows 重启；
2. 打开 Ubuntu，或执行：

~~~powershell
wsl -d Ubuntu-26.04
~~~

3. WSL 启动后，Jenkins 由 systemd 自动启动；
4. 浏览器访问：

~~~text
http://localhost:8088
~~~

如果想让 Windows 登录后自动唤醒 WSL，可以使用任务计划程序执行：

~~~powershell
wsl.exe -d Ubuntu-26.04 --exec /bin/true
~~~

但当前学习阶段不必马上配置。

### 3. Jenkins 启动和外网访问是两回事

即使 Jenkins 自动启动，如果 Windows 上的 Clash 没有启动，Jenkins 页面仍可能能打开，但插件下载、GitHub 或其他外网访问可能失败。

最终结构：

~~~text
Windows
└── Clash :7890
    └── WSL Ubuntu
        └── Jenkins :8088
~~~

### 截图占位：自启动验证

- 截图页面：Ubuntu 终端和 Jenkins 浏览器页面。
- 必须包含：systemctl is-enabled jenkins 输出 enabled，以及 8088 页面访问成功。
- 可以裁掉：个人路径和无关命令。
- 建议文件名：jenkins-15-自启动验证.png

---

## 十八、错误速查表

| 现象 | 根因 | 处理方式 |
|---|---|---|
| java: command not found | Ubuntu 没有安装 Java | 安装 openjdk-21-jre |
| Connection reset | Jenkins 下载插件时网络被重置 | 配置 Jenkins HTTP Proxy，检查 Update Center |
| Ubuntu curl 成功但 Jenkins 下载失败 | Shell 有代理，systemd 服务没有继承 | 在 Jenkins System 中配置 HTTP Proxy |
| Available plugins 加载失败 | Jenkins 到 Update Center 不通 | 检查代理、Clash 和更新中心 |
| 大量插件红色失败 | 底层依赖没有下载成功 | 先处理最底层 Plugin is missing |
| Credentials Binding 缺 ssh-credentials | SSH Credentials 未安装 | 安装 SSH Credentials |
| JUnit 缺 echarts-api | ECharts API 未安装 | 安装 ECharts API |
| This plugin cannot be disabled | 其他插件依赖它 | 不要把灰色开关当成错误 |
| No plugins installed | 浏览器停留在旧插件页面 | 回到根地址并强制刷新 |
| 8080 被占用 | Jenkins 与其他项目共用端口 | 用 systemd override 改成 8088 |
| 改端口后仍访问 8080 | 浏览器地址未更新或 systemd 未 reload | 访问 8088，执行 daemon-reload 后重启 |
| Windows 重启后 Jenkins 不可访问 | WSL 尚未被唤醒 | 打开 Ubuntu 或执行 wsl -d Ubuntu-26.04 |
| 中文没有全部生效 | 部分插件没有对应翻译 | 安装本地化插件，接受部分英文 |

---

## 十九、最终检查清单

~~~text
[ ] Windows 旧 Jenkins 已卸载
[ ] WSL Ubuntu 正常运行
[ ] systemd 正常
[ ] Java 21 已安装
[ ] Jenkins 服务为 active (running)
[ ] Jenkins 已执行 systemctl enable
[ ] Jenkins 最终监听 8088
[ ] 浏览器可以访问 http://localhost:8088
[ ] Jenkins HTTP Proxy 已配置为 172.19.208.1:7890
[ ] Available plugins 可以正常加载
[ ] Git 插件正常
[ ] Pipeline 插件正常
[ ] Credentials 相关插件正常
[ ] Localization: Chinese (Simplified) 已安装或已确认
[ ] 没有把真实密码、Token 写入笔记
[ ] 明白 Jenkins Home 清空命令具有破坏性
[ ] 明白 Windows 重启后需要先唤醒 WSL
~~~

---

## 二十、这次学习的核心结论

1. Jenkins 软件安装成功，不等于插件安装成功；
2. Jenkins 页面能打开，不等于 Jenkins 能访问外网；
3. 终端的代理环境和 systemd 服务环境可能不同；
4. 插件大量报错时，先找最底层依赖和网络错误；
5. systemctl enable 解决的是 Ubuntu 启动后的 Jenkins 自启动；
6. Windows 重启后，可能需要先唤醒 WSL；
7. Jenkins 端口应该使用 systemd override 修改；
8. 中文界面依靠本地化插件，不保证所有页面和日志都翻译；
9. rm -rf /var/lib/jenkins/* 只适合刚安装、没有重要数据的学习环境；
10. Jenkins 后续真正要学习的是 Git、Pipeline、Python、Pytest 和 Allure 的完整自动化链路。
