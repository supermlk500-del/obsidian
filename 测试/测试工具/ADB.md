# 下载、安装、配置环境变量

# ADB 常用命令

> 适用人群：**软件测试 / 自动化测试 / Android 基础调试**  
> 场景：多设备、安装卸载、应用定位、包管理

---

## 在 `adb shell` 里：

- **am = Activity Manager（活动管理器）**
    
- **pm = Package Manager（包管理器）**
## 设备管理相关

### 1️⃣ 查看当前连接的设备

```bash
adb devices
```

**作用：**

- 查看当前通过 adb 连接的所有设备/模拟器
    

**常见输出：**

```
List of devices attached
127.0.0.1:7555  device
emulator-5554   device
```

![[连接.png]]

**状态说明：**

- `device`：设备可用
    
- `unauthorized`：未授权 USB 调试
    
- `offline`：设备异常
    

---

### 2️⃣ 多设备场景下的问题

当同时连接 **多台设备** 时，如果不指定设备，会报错：

```
adb.exe: more than one device/emulator
```

📌 解决方案：**使用 `-s` 指定设备序列号**

---

## 指定设备（-s 参数）

### 1️⃣ 基本格式

```bash
adb -s 设备序列号 命令
```

### 2️⃣ 示例

- 指定官方模拟器：
    

```bash
adb -s emulator-5554 shell
```

- 指定端口设备：
    

```bash
adb -s 127.0.0.1:7555 shell
```

📌 `-s` = **serial（设备序列号）**

---

## 应用安装相关

### 1️⃣ 安装 APK

```bash
adb -s 设备 install xxx.apk
```

### 2️⃣ 覆盖安装（保留数据）

```bash
adb -s 设备 install -r xxx.apk
```

|参数|含义|
|---|---|
|install|安装应用|
|-r|覆盖安装，保留数据|

⚠️ **install 后面必须是 APK 文件路径，而不是包名**

---

## 应用卸载相关

### 1️⃣ 普通卸载（推荐 / 最常用）

```bash
adb -s 设备 uninstall 包名
```

- 完全卸载应用
    
- 数据和缓存一起删除
    

---

### 2️⃣ 卸载但保留数据（新方式）

```bash
adb -s 设备 shell cmd package uninstall -k 包名
```

📌 说明：

- `adb uninstall -k` **已废弃**
    
- Android 新版本推荐使用此方式
    

⚠️ 即使使用 `-k`，也 **不保证数据一定被保留**

---

## 应用包管理（pm）

### 1️⃣ 查看所有应用包名

```bash
adb -s 设备 shell pm list packages
```

### 2️⃣ 仅查看第三方应用

```bash
adb -s 设备 shell pm list packages -3
```

📌 `-3` = 第三方应用（非系统应用）

---

### 3️⃣ 查找指定应用（模糊匹配）

```bash
adb -s 设备 shell pm list packages | findstr 关键字
```

**示例（查抖音）：**

```bash
adb -s 设备 shell pm list packages | findstr aweme
```

---

## 查看当前前台应用（定位页面）

```bash
adb -s 设备 shell dumpsys window | findstr mCurrentFocus
```

**作用：**

- 查看当前正在显示的 Activity
    
- 自动化测试、页面定位必用
    

---

## 常见错误与原因

### ❌ 1️⃣ more than one device/emulator

**原因：**

- 同时连接多台设备
    
- 未使用 `-s` 指定设备
    

**解决：**

```bash
adb -s 设备号 命令
```

---

### ❌ 2️⃣ failed to stat xxx.apk

**原因：**

- APK 文件不存在
    
- 当前目录下找不到该文件
    

**解决：**

- 使用绝对路径
    
- 或 `cd` 到 APK 所在目录
    

---

## 命令结构总结（通用模型）

```text
adb   -s 设备   动作        参数
工具   指定设备 做什么      怎么做
```

**示例：**

```bash
adb -s emulator-5554 install -r demo.apk
```

---
## 杀停进程
```bash
adb shell am force-stop <包名>
```

 





