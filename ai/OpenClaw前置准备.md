# OpenClaw 安装前置准备

> 在安装 OpenClaw 之前，请确保以下环境和工具已准备好。
> 
> 本教程面向零基础用户，每一步都有详细说明。

---

## 📋 目录

1. [系统要求](#一系统要求)
2. [安装 Node.js](#二安装-nodejs)
3. [安装 Git](#三安装-git)
4. [配置 npm 镜像源](#四配置-npm-镜像源)
5. [验证安装](#五验证安装)
6. [常见问题](#六常见问题)

---

## 一、系统要求

### 1.1 操作系统

- **Windows 10**（版本 1903 或更高）
- **Windows 11**（推荐）

> ⚠️ **不支持**：Windows 7/8、macOS、Linux（本教程针对 Windows）

### 1.2 硬件要求

| 项目 | 最低要求 | 推荐配置 |
|------|----------|----------|
| 内存 | 4GB | 8GB 或以上 |
| 硬盘空间 | 1GB 可用空间 | 5GB 可用空间 |
| 网络 | 能访问国内网站 | 宽带网络 |

### 1.3 权限要求

- 需要管理员权限（安装软件时使用）
- 能修改系统环境变量

---

## 二、安装 Node.js

### 2.1 什么是 Node.js？

Node.js 是一个 JavaScript 运行环境，OpenClaw 基于它开发，必须先安装。

### 2.2 下载 Node.js

1. 打开浏览器，访问：https://nodejs.org/
2. 点击首页的 **"LTS"** 按钮（推荐大多数用户）

![[nodejs-download.png]]

> 💡 **提示**：LTS = 长期支持版，更稳定。Current = 最新版，可能有 bug。

### 2.3 安装步骤

1. 双击下载的安装包（如 `node-v22.x.x-x64.msi`）
2. 点击 **"Next"**
3. 勾选 **"I accept the terms in the License Agreement"**，点击 **"Next"**
4. 选择安装路径（默认即可），点击 **"Next"**
5. **重要！** 勾选 **"Automatically install the necessary tools"** 和 **"Add to PATH"**

![[nodejs-install-options.png]]

6. 点击 **"Next"** → **"Install"**
7. 等待安装完成，点击 **"Finish"**

### 2.4 验证安装

打开 PowerShell（右键开始菜单 → Windows PowerShell），输入：

```powershell
node --version
```

如果显示版本号（如 `v22.14.0`），说明安装成功！

再输入：

```powershell
npm --version
```

应该显示 npm 版本号（如 `10.9.2`）。

---

## 三、安装 Git

### 3.1 什么是 Git？

Git 是版本控制工具，OpenClaw 的某些功能需要它。

### 3.2 下载 Git

1. 访问：https://git-scm.com/download/win
2. 点击 **"64-bit Git for Windows Setup"**

或者使用国内镜像：
- https://registry.npmmirror.com/binary.html?path=git-for-windows/

### 3.3 安装步骤

1. 双击下载的安装包（如 `Git-2.x.x-64-bit.exe`）
2. 点击 **"Next"**
3. 选择安装路径（默认即可），点击 **"Next"**
4. 选择组件：
   - 勾选 **"Windows Explorer integration"**（右键菜单）
   - 勾选 **"Git Bash Here"**
   - 勾选 **"Git GUI Here"**
   - 其他保持默认

![[git-components.png]]

5. 点击 **"Next"**
6. 选择编辑器（默认 Vim 即可，或选择 VS Code），点击 **"Next"**
7. 一路点击 **"Next"** 使用默认选项
8. 最后点击 **"Install"**
9. 等待安装完成，点击 **"Finish"**

### 3.4 验证安装

在 PowerShell 中输入：

```powershell
git --version
```

如果显示版本号（如 `git version 2.48.1.windows.1`），说明安装成功！

---

## 四、配置 npm 镜像源

### 4.1 为什么要换镜像源？

npm 默认使用国外服务器，国内访问很慢。换成国内镜像源可以大幅提升下载速度。

### 4.2 查看当前镜像源

```powershell
npm config get registry
```

默认显示：`https://registry.npmjs.org/`（国外）

### 4.3 设置国内镜像源

#### 方案一：淘宝镜像（推荐）

```powershell
npm config set registry https://registry.npmmirror.com
```

#### 方案二：腾讯云镜像

```powershell
npm config set registry https://mirrors.cloud.tencent.com/npm/
```

#### 方案三：华为云镜像

```powershell
npm config set registry https://mirrors.huaweicloud.com/repository/npm/
```

### 4.4 验证镜像源

```powershell
npm config get registry
```

应该显示你设置的国内镜像地址。

### 4.5 恢复官方镜像（如需）

```powershell
npm config set registry https://registry.npmjs.org/
```

---

## 五、验证安装

完成以上步骤后，请依次运行以下命令，确保所有工具都已正确安装：

```powershell
# 检查 Node.js
node --version

# 检查 npm
npm --version

# 检查 Git
git --version

# 检查镜像源
npm config get registry
```

**预期输出示例：**

```
v22.14.0
10.9.2
git version 2.48.1.windows.1
https://registry.npmmirror.com
```

如果全部显示正常，说明准备工作完成，可以开始安装 OpenClaw 了！

---

## 六、常见问题

### Q1: 安装 Node.js 时提示"需要管理员权限"

**解决**：右键点击安装包 → **"以管理员身份运行"**

### Q2: 输入 `node --version` 提示"不是内部或外部命令"

**原因**：环境变量没有配置好。

**解决**：
1. 重启 PowerShell
2. 如果还不行，重启电脑
3. 检查安装时是否勾选了 "Add to PATH"

### Q3: npm 下载还是很慢

**解决**：
1. 检查镜像源是否设置成功：`npm config get registry`
2. 尝试更换其他镜像源
3. 使用代理或 VPN（不推荐，国内镜像已足够快）

### Q4: Git 安装后右键菜单没有"Git Bash Here"

**解决**：
1. 重新运行 Git 安装包
2. 选择 "Modify"
3. 确保勾选了 "Windows Explorer integration"

### Q5: 公司电脑有安全软件阻止安装

**解决**：
1. 暂时关闭杀毒软件
2. 将 Node.js 和 Git 添加到白名单
3. 或联系 IT 部门协助

---

## ✅ 准备工作检查清单

在开始安装 OpenClaw 之前，请确认：

- [ ] Windows 10/11 系统
- [ ] Node.js 已安装（版本 22+）
- [ ] Git 已安装
- [ ] npm 镜像源已换成国内
- [ ] 所有命令都能正常执行
- [ ] 有管理员权限

**全部勾选完成 → 可以开始安装 OpenClaw 了！**

---

## 🔗 相关链接

- Node.js 官网：https://nodejs.org/
- Git 下载：https://git-scm.com/download/win
- 淘宝 npm 镜像：https://npmmirror.com/
- OpenClaw 安装教程：[[OpenClaw完整安装教程]]

---

*本教程由 OpenClaw AI 助手"陈情"协助编写*