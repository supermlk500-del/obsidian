# ADB 

## 1. ADB 简介与环境配置

### 1.1 什么是 ADB？

Android Debug Bridge (ADB) 是一个多功能的命令行工具，可让您与设备进行通信。ADB 命令行工具能够执行各种设备操作，例如安装和调试应用，并提供对 Unix shell 的访问，您可以使用该 shell 在设备上运行各种命令。它由三部分组成：

- **客户端**：在您的开发机器上运行，可以通过发出 adb 命令来调用。
- **守护程序 (adbd)**：在设备上作为后台进程运行。
- **服务器**：在您的开发机器上作为后台进程运行，用于管理客户端和守护程序之间的通信。

### 1.2 下载与安装

ADB 工具通常包含在 Android SDK Platform-Tools 中。您可以从 [Android 开发者官网](https://developer.android.com/tools/releases/platform-tools) 下载最新版本。下载后，解压到一个方便的目录，例如 `C:\platform-tools` (Windows) 或 `~/platform-tools` (Linux/macOS)。

### 1.3 配置环境变量

为了方便在任何目录下使用 ADB 命令，需要将其添加到系统环境变量 PATH 中。以下是 Windows 系统的配置步骤：

1.  右键点击“此电脑” -> “属性” -> “高级系统设置” -> “环境变量”。
2.  在“系统变量”下找到 `Path` 变量，双击编辑。
3.  点击“新建”，然后添加 ADB 工具的解压路径（例如 `C:\platform-tools`）。
4.  点击“确定”保存所有更改。

配置完成后，打开命令行工具（如 CMD 或 PowerShell），输入 `adb version`，如果能显示版本信息，则表示配置成功。

## 2. 设备管理

### 2.1 查看当前连接的设备

使用 `adb devices` 命令可以查看当前通过 ADB 连接的所有设备或模拟器。

```bash
adb devices
```

**作用：**

- 查看当前通过 adb 连接的所有设备/模拟器。

**常见输出：**

```
List of devices attached
127.0.0.1:7555  device
emulator-5554   device
```

![[连接.png]]

**状态说明：**

- `device`：设备可用。
- `unauthorized`：未授权 USB 调试。需要在设备上同意 USB 调试授权。
- `offline`：设备异常或未连接。

### 2.2 多设备场景下的问题与解决方案

当同时连接多台设备时，如果不指定设备，会报错 `adb.exe: more than one device/emulator`。解决方案是使用 `-s` 参数指定设备序列号。

### 2.3 指定设备 (`-s` 参数)

`-s` 参数用于指定要操作的设备序列号（serial）。

**基本格式：**

```bash
adb -s 设备序列号 命令
```

**示例：**

- 指定官方模拟器：

```bash
adb -s emulator-5554 shell
```

- 指定端口设备：

```bash
adb -s 127.0.0.1:7555 shell
```

📌 `-s` = **serial（设备序列号）**

### 2.4 ADB 无线连接 (Wi-Fi)

ADB 也支持通过 Wi-Fi 连接设备，这在 USB 连接不便时非常有用。

**步骤：**

1.  **确保设备和电脑在同一局域网内。**
2.  **通过 USB 连接设备到电脑。**
3.  **设置设备监听 TCP/IP 连接：**
    ```bash
    adb tcpip 5555
    ```
    （`5555` 是端口号，可以自定义）
4.  **断开 USB 连接。**
5.  **查找设备的 IP 地址：** 在设备上进入“设置” -> “关于手机” -> “状态信息” -> “IP 地址”。
6.  **连接设备：**
    ```bash
    adb connect <设备IP地址>:5555
    ```
    例如：`adb connect 192.168.1.100:5555`
7.  **验证连接：** 再次运行 `adb devices`，应该能看到设备以 IP 地址的形式连接。

**断开无线连接：**

```bash
adb disconnect <设备IP地址>:5555
```

## 3. 应用管理

### 3.1 安装 APK

使用 `adb install` 命令安装 APK 文件到设备。

```bash
adb -s 设备 install <APK文件路径>
```

**示例：**

```bash
adb install /path/to/your/app.apk
```

### 3.2 覆盖安装 (保留数据)

使用 `-r` 参数进行覆盖安装，通常会保留应用数据。

```bash
adb -s 设备 install -r <APK文件路径>
```

| 参数    | 含义         |
| :------ | :----------- |
| `install` | 安装应用     |
| `-r`    | 覆盖安装，保留数据 |

⚠️ **`install` 后面必须是 APK 文件路径，而不是包名。**

### 3.3 卸载应用

#### 3.3.1 普通卸载 (推荐 / 最常用)

完全卸载应用，同时删除数据和缓存。

```bash
adb -s 设备 uninstall <包名>
```

#### 3.3.2 卸载但保留数据 (新方式)

此方式尝试卸载应用但保留其数据。请注意，即使使用 `-k`，也 **不保证数据一定被保留**。

```bash
adb -s 设备 shell cmd package uninstall -k <包名>
```

📌 说明：

- `adb uninstall -k` **已废弃**。
- Android 新版本推荐使用 `adb shell cmd package uninstall -k` 方式。

### 3.4 应用包管理 (`pm`)

`pm` (Package Manager) 命令用于管理设备上的应用包。

#### 3.4.1 查看所有应用包名

```bash
adb -s 设备 shell pm list packages
```

#### 3.4.2 仅查看第三方应用

```bash
adb -s 设备 shell pm list packages -3
```

📌 `-3` = 第三方应用（非系统应用）。

#### 3.4.3 查找指定应用 (模糊匹配)

结合 `findstr` (Windows) 或 `grep` (Linux/macOS) 可以模糊匹配查找应用。

```bash
adb -s 设备 shell pm list packages | findstr 关键字  # Windows
adb -s 设备 shell pm list packages | grep 关键字     # Linux/macOS
```

**示例 (查抖音)：**

```bash
adb -s 设备 shell pm list packages | findstr aweme
```

### 3.5 应用信息获取与分析 (`aapt`)

`aapt` (Android Asset Packaging Tool) 是 Android SDK Build-Tools 中的一个工具，用于查看、创建和更新 ZIP 兼容的归档文件（包括 APK、JAR 和 Z）。`aapt dump badging` 命令可以解析 APK 文件，并显示其清单文件中的重要信息，如包名、版本号、权限、启动 Activity 等。

```bash
aapt dump badging <APK文件路径>
```

**示例：**

```bash
aapt dump badging C:\Users\lhr\Documents\xwechat_files\wxid_knn96sk7aseu22_b528\msg\file\2026-02\calculator.apk
```

## 4. 调试与信息获取

### 4.1 打开手机终端 (`adb shell`)

`adb shell` 命令可以打开设备的 Unix shell，允许您直接在设备上执行命令。

```bash
adb shell
```

在 `adb shell` 里，常用的命令有：

- **`am` = Activity Manager（活动管理器）**：用于启动 Activity、发送广播、强制停止进程等。
- **`pm` = Package Manager（包管理器）**：用于管理应用包，如安装、卸载、查询包信息等。

### 4.2 查看系统服务信息 (`dumpsys`)

`adb shell dumpsys` 命令用于打印出当前系统信息。默认情况下，它会打印出设备中所有服务 (service) 的详细信息。您可以在命令后面加上指定的 `service name` 来查看特定服务的信息。

```bash
adb shell dumpsys
```

**常用示例：**

- **查看当前前台应用 (定位页面)**：此命令用于查看当前正在显示的 Activity，在自动化测试和页面定位中非常有用。
    ```bash
    adb shell dumpsys window | findstr mCurrentFocus
    ```
- **查看电池信息/耗电量测试**：显示电量百分比、电池状态等详细信息。
    ```bash
    adb shell dumpsys battery
    ```
- **显示设备分辨率**：查看设备的屏幕尺寸和分辨率。
    ```bash
    adb shell dumpsys wms size
    ```

### 4.3 杀停进程

使用 `am force-stop` 命令强制停止指定包名的应用进程。

```bash
adb shell am force-stop <包名>
```

### 4.4 获取系统属性 (`getprop`)

`getprop` 是 Android 系统内置命令，用于获取设备的系统属性。不加参数时，它会一次性列出所有系统属性。

```bash
adb shell getprop
```

**常用示例：**

- **获取系统版本**：
    ```bash
adb shell getprop ro.build.version.release
    ```
- **获取系统 API 版本**：
    ```bash
adb shell getprop ro.build.version.sdk
    ```
- **获取手机型号与设备信息**：也可以通过读取 `build.prop` 文件来获取。
    ```bash
adb shell cat /system/build.prop
    ```

### 4.5 文件传输 (`pull` 和 `push`)

ADB 提供了 `pull` 和 `push` 命令用于在电脑和设备之间传输文件。

#### 4.5.1 从设备拉取文件 (`pull`)

将设备上的文件或目录复制到本地电脑。

```bash
adb pull <设备路径> <本地路径>
```

**示例：**

- 拉取设备上的 `/sdcard/Download/test.txt` 到本地当前目录：
    ```bash
    adb pull /sdcard/Download/test.txt .
    ```
- 拉取设备上的 `/sdcard/DCIM/Camera` 目录到本地 `/home/user/photos`：
    ```bash
    adb pull /sdcard/DCIM/Camera /home/user/photos
    ```

#### 4.5.2 推送文件到设备 (`push`)

将本地电脑上的文件或目录复制到设备。

```bash
adb push <本地路径> <设备路径>
```

**示例：**

- 推送本地的 `app.apk` 到设备上的 `/sdcard/Download` 目录：
    ```bash
    adb push app.apk /sdcard/Download/
    ```
- 推送本地的 `config.txt` 到设备上的 `/data/local/tmp` 目录：
    ```bash
    adb push config.txt /data/local/tmp/
    ```

### 4.6 查看设备日志 (`logcat`)

`adb logcat` 用于查看设备的系统日志，对于调试应用非常重要。

```bash
adb logcat
```

**常用参数：**

- `-c`：清除现有日志。
- `-d`：将日志输出到屏幕并退出。
- `-s <tag>`：只显示指定标签的日志。
- `-f <filename>`：将日志输出到指定文件。
- `*:V`、`*:D`、`*:I`、`*:W`、`*:E`、`*:F`：过滤日志级别 (Verbose, Debug, Info, Warn, Error, Fatal)。

**示例：**

- 清除日志并显示所有日志：
    ```bash
    adb logcat -c && adb logcat
    ```
- 只显示错误级别以上的日志：
    ```bash
    adb logcat *:E
    ```
- 显示指定标签的调试日志：
    ```bash
    adb logcat MyTag:D *:S
    ```
    (`*:S` 表示忽略所有其他标签的日志)

### 4.7 屏幕截图 (`screencap`)

`adb shell screencap` 命令可以在设备上进行屏幕截图。

```bash
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png .
```

**一步到位截图并保存到本地：**

```bash
adb exec-out screencap -p > screen.png
```

### 4.8 屏幕录制 (`screenrecord`)

`adb shell screenrecord` 命令可以在设备上进行屏幕录制。

```bash
adb shell screenrecord /sdcard/demo.mp4
```

**常用参数：**

- `--time-limit <seconds>`：设置录制时长，默认 180 秒。
- `--size <width>x<height>`：设置视频分辨率。
- `--bit-rate <rate>`：设置视频比特率 (bps)。

**示例：**

- 录制 30 秒，分辨率 1280x720，保存到 `/sdcard/demo.mp4`：
    ```bash
    adb shell screenrecord --time-limit 30 --size 1280x720 /sdcard/demo.mp4
    ```

录制完成后，使用 `adb pull` 命令将视频文件拉取到本地。

## 5. 系统性能与文件系统操作

### 5.1 进程与资源监控

- **动态查看设备 CPU 和内存占用情况 (`top`)**：
    ```bash
adb shell top
    ```
    - 查看占用资源前 5 的应用：
        ```bash
adb shell top -m 5
        ```
    - 刷新显示 2 次资源信息，显示 2 次后停止：
        ```bash
adb shell top -n 2
        ```
    - 查看系统资源占用前 5 的程序，并刷新 2 次：
        ```bash
adb shell top -m 5 -n 2
        ```
- **查看进程列表 (`ps`)**：
    ```bash
adb shell ps
    ```
- **查看后台 services 信息 (`service list`)**：
    ```bash
adb shell service list
    ```
- **查看当前机器内存使用情况 (`cat /proc/meminfo`)**：
    ```bash
adb shell cat /proc/meminfo
    ```
- **查看系统内存使用情况 (`free`)**：
    ```bash
adb shell free
    ```

### 5.2 文件系统操作

- **列出目录下的文件和文件夹 (`ls`)**：
    ```bash
adb shell ls
    ```
- **新建文件夹 (`mkdir`)**：
    ```bash
adb shell mkdir /sdcard/foldername
    ```
- **查看文件大小 (`du`)**：
    ```bash
adb shell du -h /sdcard/myl.txt
    ```
- **查看系统磁盘使用情况 (`df`)**：
    ```bash
adb shell df
    ```

📌 **支持 `iostat`, `vmstat`, `netstat` 等 Linux 性能监控命令。**

## 6. 常见错误与解决方案

### 6.1 `more than one device/emulator`

**原因：**

- 同时连接多台设备。
- 未使用 `-s` 指定设备。

**解决：**

```bash
adb -s 设备号 命令
```

### 6.2 `failed to stat xxx.apk`

**原因：**

- APK 文件不存在。
- 当前目录下找不到该文件。

**解决：**

- 使用绝对路径。
- 或 `cd` 到 APK 所在目录。

## 7. 命令结构总结 (通用模型)

```text
adb   -s 设备   动作        参数
工具   指定设备 做什么      怎么做
```

**示例：**

```bash
adb -s emulator-5554 install -r demo.apk
```



## logcat

## 8. 参考文献

- [1] Android Developers. [Android Debug Bridge (adb)](https://developer.android.com/tools/adb)
- [2] CSDN. [adb详细教程（一）-下载安装与环境变量配置](https://blog.csdn.net/weixin_40883833/article/details/131147009)
- [3] 腾讯云. [adb工具安装教程（附安装包）adb环境配置图文教程](https://cloud.tencent.com/developer/article/2571852)
- [4] GitHub Gist. [Adb useful commands list](https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8)
- [5] CSDN. [adb shell中的am pm命令、常用命令总结](https://blog.csdn.com/qq_43472877/article/details/116454039)
- [6] Stack Overflow. [Using ADB to capture the screen](https://stackoverflow.com/questions/27766712/using-adb-to-capture-the-screen)
