# Android Monkey 压力测试指南与实战笔记

---

## 1. 核心概念与架构区分

在 Android 自动化与压力测试中，经常会遇到 **Monkey**、**Monkey Script** 和 **MonkeyRunner**。三者虽然名字相似，但底层原理、使用场景和语法存在本质区别：

| 特性 / 工具 | Monkey | Monkey Script | MonkeyRunner |
| :--- | :--- | :--- | :--- |
| **底层实现** | Android 系统自带的 C/Java 命令行工具 (`/system/bin/monkey`) | 原生 Monkey 识别的特定文本格式 (`raw events`) | 基于 Python / Jython 的独立自动化框架 |
| **核心逻辑** | **伪随机**产生用户事件流（点击、滑动、按键等） | 顺序执行预定义的硬编码事件序列 | 通过 Socket 通信驱动设备，支持控制逻辑与图像对比 |
| **运行位置** | 直接运行在 Android 设备的 **Shell 环境** 中 | 被推送到设备后由 `monkey -f` 加载执行 | 运行在 **PC 端**，通过 ADB 控制手机 |
| **主要用途** | **稳定性/压力测试**，寻找 Crash 和 ANR | 简单的特定路径重复操作/回放 | **功能自动化测试**、UI 回归测试、多设备交互 |
| **灵活度** | 随机性强，不可控制业务逻辑 | 固定坐标和动作，无条件判断能力 | 极高，支持 Python 完整逻辑、截图对比与断言 |

---

## 2. Monkey 命令行参数详解

Monkey 通过命令行启动，通用参数格式如下：

```bash
adb shell monkey [选项] <事件总数>
```

### 2.1 基础控制参数

*   **`-p <package_name>`**：指定目标应用包名。
    *   指定单个应用：`adb shell monkey -p com.example.app 1000`
    *   指定多个应用：`adb shell monkey -p com.app1 -p com.app2 1000`
*   **`-v` (日志详细度)**：控制输出日志的详细程度（分为三级）：
    *   `-v`（一级）：只输出启动信息、Seed 值、执行事件数和最终 PASS/FAIL 结果。适合**快速查看是否崩溃**。
    *   `-v -v`（二级）：在 Level 1 基础上输出发送给 Activity 的具体事件类型、坐标及 Activity 切换过程。适合**定位问题发生的大致模块**。
    *   `-v -v -v`（三级，最常用 🔥）：输出最详尽的日志，包括每个事件的精确点击坐标、按键 KeyCode、详细系统状态。适合**排查与复现 Bug**。
*   **`-s <seed>` (随机数种子)**：
    *   伪随机生成器的种子值。如果用相同的 Seed 值再次运行 Monkey，它将产生**完全相同的事件序列**。
    *   示例：`adb shell monkey -p com.example.app -s 12345 1000`
    *   📌 **核心价值**：**100% 重现压力测试中发现的随机崩溃或 ANR。**
*   **`--throttle <milliseconds>` (事件延迟)**：
    *   设置每个事件之间的固定延迟时间（毫秒）。
    *   示例：`adb shell monkey -p com.example.app --throttle 300 1000`
    *   📌 说明：模拟正常用户的思考和操作节奏（通常人类连续点击间隔约 300ms）。不加延迟会导致事件触发过快，可能引起非预期卡死或过载。

---

### 2.2 事件比例控制参数 (11 种事件类型)

Monkey 允许自定义各种事件占总事件数的百分比（参数值为百分数，无需写 `%` 符号，如 `--pct-touch 70`）：

```bash
adb shell monkey -p com.example.app \
  --pct-touch 50 \
  --pct-motion 20 \
  --pct-appswitch 10 \
  --pct-syskeys 10 \
  --pct-nav 10 \
  10000
```

| 参数选项 | 事件类型说明 | 说明与建议 |
| :--- | :--- | :--- |
| **`--pct-touch`** | 触摸点击事件 | 屏幕上的 Down -> Up 动作（单点点击）。**推荐占比 50%~70%** |
| **`--pct-motion`** | 动作/手势事件 | 屏幕上的滑动、拖拽（Down -> Move -> Up）。**推荐占比 10%~20%** |
| **`--pct-pinchzoom`** | 双指缩放事件 | 模拟双指放大/缩小手势 |
| **`--pct-trackball`** | 轨迹球事件 | 模拟轨迹球轨迹移动（早期设备，现极少使用） |
| **`--pct-rotation`** | 屏幕旋转事件 | 模拟竖屏与横屏之间的旋转切换 |
| **`--pct-nav`** | 基本导航事件 | 上/下/左/右方向键（如 TV App 或键盘操作） |
| **`--pct-majornav`** | 主要导航事件 | 模拟引发界面导航的按键（如 Home 键、Back 返回键、Menu 菜单） |
| **`--pct-syskeys`** | 系统按键事件 | 保留给系统的按键（如 Home 键、音量键、Power 电源键、拨号键） |
| **`--pct-appswitch`** | Activity 切换事件 | 调整应用内 Activity 之间跳转及切后台的频率 |
| **`--pct-flip`** | 键盘弹起/收起事件 | 模拟硬件键盘的展开与折叠 |
| **`--pct-permission`** | 动态权限授权事件 | 自动对 Android 6.0+ 的 Runtime 权限弹窗进行允许/拒绝操作 |
| **`--pct-anyevent`** | 任意其他事件 | 包含除上述事件外的所有其他不常用事件（按键/按压等） |

---

### 2.3 调试与容错参数 (夜间无人值守压测必备 🔥)

默认情况下，Monkey 遇到应用崩溃 (Crash) 或无响应 (ANR) 会立即停止运行。在长期压测（如夜间 8~12 小时测试）中，必须配置容错参数，确保 Monkey 忽略偶发错误继续运行：

*   **`--ignore-crashes`**：当应用发生崩溃 (Crash) 或未捕获异常时，Monkey 继续发送事件直至总数结束。
*   **`--ignore-timeouts`**：当应用发生 ANR (Application Not Responding) 无响应超时时，Monkey 继续发送事件。
*   **`--ignore-security-exceptions`**：忽略系统许可或权限异常（如 SecurityException），防止授权阻断测试。
*   **`--monitor-native-crashes`**：监视并记录 Android C/C++ Native 层代码发生的崩溃。
*   **`--kill-process-after-error`**：发生错误时通知系统杀掉崩溃的应用进程，而不是停留在错误弹窗页。
*   **`--pkg-whitelist-file <file_path>`**：指定包名白名单文件。Monkey 只会在白名单中的应用内发送事件。
*   **`--pkg-blacklist-file <file_path>`**：指定包名黑名单文件。Monkey 绝对不会进入黑名单中的 App（如防误触系统“设置”或“电话”）。

---

### 2.4 日志保存与重定向输出

在 CMD / PowerShell 或 Bash 终端中运行重定向命令，将标准输出和错误日志写入 PC 本地文件：

```bash
adb shell monkey -p com.example.app -v -v -v --throttle 300 100000 > D:\monkey_test.log 2>&1
```

---

## 3. Monkey 日志分析与异常排查指南

压力测试完成后，第一步是检查日志文件中是否存在异常信息。

### 3.1 日志结构解读

典型的 Monkey 日志包含四个关键阶段：
1.  **启动头信息**：记录了测试包名、Seed 值、运行事件数、各类事件占比配置。
2.  **事件执行过程**：根据 `-v` 的详细级别输出的具体 Action。
3.  **异常捕获段**（若有）：Crash 堆栈、ANR 提示或 Native 崩溃信号。
4.  **统计尾信息**：成功执行事件数（如 `Events injected: 100000`）和耗时。

---

### 3.2 常见异常特征与关键字搜索

打开日志文件（如 `monkey.log`），快速检索以下核心关键字：

#### 1️⃣ Java / Kotlin 崩溃 (Crash)
*   **搜索关键字**：`CRASH:`、`Exception`、`NullPointerException`、`Short Msg`
*   **日志特征**：
    ```text
    // CRASH: com.example.app (pid 14205)
    // Short Msg: java.lang.NullPointerException
    // Long Msg: java.lang.NullPointerException: Attempt to invoke virtual method ...
    // Build Label: Android/sdk_gphone64_x86_64/sdk_gphone64_x86_64:12/...
    // Stack Keep-Alive: ...
    at com.example.app.MainActivity.onClick(MainActivity.java:45)
    ```

#### 2️⃣ 应用无响应 (ANR - Application Not Responding)
*   **搜索关键字**：`ANR in`、`// NOT RESPONDING`、`Reason: Input dispatching timed out`
*   **日志特征**：
    ```text
    // NOT RESPONDING: com.example.app (pid 14205)
    // ANR Reason: Input dispatching timed out (Waiting to send non-key event because the touched window has not finished processing...)
    // Load: 4.5 / 2.1 / 1.0
    ```

#### 3️⃣ C/C++ Native 层崩溃 (Native Crash)
*   **搜索关键字**：`Native crash`、`Segmentation fault`、`Fatal signal 11 (SIGSEGV)`
*   **日志特征**：底层 C/C++ 代码指针越界、空指针解引用或内存破坏。

#### 4️⃣ 内存溢出 (OOM - Out Of Memory)
*   **搜索关键字**：`OutOfMemoryError`、`GC overhead limit exceeded`

---

### 3.3 深度定位：ANR 与 Native Crash 的日志抓取

单纯看 Monkey 日志有时无法获取 ANR 的完整调用栈，需要提取系统生成的 Trace 和 Tombstone 文件：

#### 📌 ANR Trace 日志提取
当发生 ANR 时，系统会在 `/data/anr/` 目录下生成堆栈文件。使用 ADB 将其拉取到本地分析：

```bash
# 查看设备上 anr 目录下的文件
adb shell ls -l /data/anr/

# 拉取最新的 traces.txt 或 anr_* 文件到 PC 本地
adb pull /data/anr/traces.txt D:\anr_traces.txt
```
*在 `traces.txt` 中搜索目标应用的包名，查找主线程 (main thread) 的状态（如 `SUSPENDED`、`BLOCKED` 或 `MONITOR`），查看卡死在哪个具体函数上。*

#### 📌 Native Crash Tombstones 文件提取
如果崩溃发生在 Native 层，系统会在 `/data/tombstones/` 目录记录：

```bash
adb pull /data/tombstones/ D:\tombstones\
```

---

### 3.4 Bug 100% 精确复现流程

当 Monkey 测试抛出 Crash 或 ANR 后，按照以下四步进行精准复现：

1.  **从错误日志中查找启动参数**：
    搜索日志顶部的 `:Monkey: seed=` 行，获取当时的 Seed 值。
    例如：`:Monkey: seed=1722659821456 count=50000`
2.  **定位发生崩溃时的事件序号**：
    在崩溃日志上方找到最近发生的事件序号（如已执行到第 12450 个事件时崩溃）。
3.  **使用相同 Seed 重新复现**：
    在设备连接抓包工具与 `adb logcat` 的同时，以**相同的 Seed 值**重新运行（可以适当减少执行总数，比崩溃点稍微多一点即可）：
    ```bash
    adb shell monkey -p com.example.app -s 1722659821456 -v -v -v 13000
    ```
4.  **收集实时 Logcat**：
    ```bash
    adb logcat *:E > D:\crash_logcat.txt
    ```

---

## 4. 原生 Monkey 脚本 (Monkey Script) 规范与实例

Monkey 支持运行预先编写好的原生脚本（**Monkey Script**），用以实现固定操作序列的重复执行。

### 4.1 脚本标准文件头声明

Monkey 脚本文件（通常为 `.script` 或 `.txt` 格式）必须以特定的 Header 开头：

```text
type= raw events
count= 10
speed= 1.0
start data >>
```
*   `type= raw events`：固定写法，表示原始事件脚本。
*   `count= 10`：脚本循环执行次数（注意：此处的 count 在执行命令中通常由命令行参数覆盖）。
*   `speed= 1.0`：执行速率。
*   `start data >>`：必须包含这一行，此行下方开始编写具体动作命令。

---

### 4.2 常用 Monkey Script 核心指令

| 指令名称 | 语法与参数 | 说明 |
| :--- | :--- | :--- |
| **`DispatchPointer`** | `DispatchPointer(downTime, eventTime, action, x, y, pressure, size, metaState, xPrecision, yPrecision, device, edgeFlags)` | **模拟触摸点击/滑动**。<br>`action`: 0代表Touch Down，1代表Touch Up，2代表Move |
| **`DispatchPress`** | `DispatchPress(keycode)` | **模拟按键点击**（如 `DispatchPress(KEYCODE_BACK)` 或 `DispatchPress(66)`） |
| **`DispatchString`** | `DispatchString(input_text)` | **模拟输入字符串**（在输入框焦点处输入文本） |
| **`UserWait`** | `UserWait(milliseconds)` | **等待/休眠指定毫秒数** |
| **`LaunchActivity`** | `LaunchActivity(pkg_name, activity_name)` | **启动指定的 Activity 页面** |
| **`RotateScreen`** | `RotateScreen(degree, persist)` | **旋转屏幕**。<br>`degree`: 0(0度), 1(90度), 2(180度), 3(270度) |

---

### 4.3 完整脚本实例与运行步骤

#### 1️⃣ 编写脚本 `login_test.script`

```text
type= raw events
count= 1
speed= 1.0
start data >>

# 1. 启动应用主界面
LaunchActivity(com.example.calculator, com.example.calculator.MainActivity)
UserWait(2000)

# 2. 点击屏幕上的坐标 (x=500, y=1000) - 按下与抬起
DispatchPointer(0, 0, 0, 500, 1000, 0, 0, 0, 0, 0, 0, 0)
DispatchPointer(0, 0, 1, 500, 1000, 0, 0, 0, 0, 0, 0, 0)
UserWait(1000)

# 3. 输入字符串
DispatchString("123456")
UserWait(1000)

# 4. 按下返回键
DispatchPress(KEYCODE_BACK)
UserWait(1000)
```

#### 2️⃣ 将脚本推送至设备并运行

```bash
# 将 PC 本地脚本推送至手机 SD 卡或 /data/local/tmp 目录
adb push login_test.script /sdcard/login_test.script

# 验证文件是否存在
adb shell cat /sdcard/login_test.script

# 使用 monkey -f 参数运行脚本（最后一个数字 '10' 代表重复循环 10 次）
adb shell monkey -f /sdcard/login_test.script -v 10
```

---

## 5. MonkeyRunner 自动化框架 (Python API)

**MonkeyRunner** 是基于 Python / Jython 的框架，运行在电脑端，通过控制 API 与 Android 设备交互。

### 5.1 核心模块架构

MonkeyRunner 包含三大核心 API 模块：

```text
MonkeyRunner (全局控制与连接)
   ├── MonkeyDevice (设备交互：点击/拖拽/按键/安装)
   └── MonkeyImage  (图像截图与对比)
```

---

### 5.2 MonkeyRunner API 分类汇总

#### 1️⃣ `MonkeyRunner` 模块（设备连接与全局等待）

| API 命令 | 说明 |
| :--- | :--- |
| `MonkeyRunner.waitForConnection(timeout, deviceId)` | 等待并连接指定序列号的 Android 设备，返回 `MonkeyDevice` 对象 |
| `MonkeyRunner.sleep(seconds)` | 脚本暂停运行指定的秒数（支持小数，如 0.5） |
| `MonkeyRunner.choice(message, choices, title)` | 弹出 UI 窗口供测试人员在 PC 端选择选项 |
| `MonkeyRunner.input(message, initial, title)` | 弹出 UI 输入框让测试人员输入文本 |

#### 2️⃣ `MonkeyDevice` 模块（设备操作）

| API 命令 | 说明与示例 |
| :--- | :--- |
| `device.touch(x, y, type)` | 点击指定坐标。<br>`type`: `MonkeyDevice.DOWN`, `UP`, `DOWN_AND_UP` |
| `device.drag(start, end, duration, steps)` | 滑动/拖拽。<br>`device.drag((100,500), (100,100), 1.0, 10)` |
| `device.press(name, type)` | 按键。<br>`device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)` |
| `device.type(text)` | 向当前焦点输入框发送文本。例如：`device.type("Admin123")` |
| `device.takeSnapshot()` | 截取当前屏幕，返回 `MonkeyImage` 对象 |
| `device.installPackage(path)` | 安装 APK 文件 |
| `device.removePackage(pkg)` | 卸载应用包 |
| `device.startActivity(component)` | 启动页面。<br>`device.startActivity(component="com.pkg/.MainActivity")` |
| `device.shell(cmd)` | 在设备上执行原生 adb shell 命令并返回结果字符串 |

#### 3️⃣ `MonkeyImage` 模块（图像对比与断言）

| API 命令 | 说明与示例 |
| :--- | :--- |
| `image.writeToFile(path, format)` | 将截图保存到 PC 硬盘。<br>`image.writeToFile('d:/shot.png', 'png')` |
| `image.getSubImage(rect)` | 截取局部区域图像。<br>`rect`: `(x, y, width, height)` |
| `image.sameAs(otherImage, tolerance)` | 比较两张图片是否一致。<br>`tolerance`: 相似度容忍度（0.0~1.0），1.0 表示完全相同 |

---

### 5.3 常用 KeyCode 快速查表

在 `device.press()` 中常用的按键 KeyCode：

| 键名 | 常用 KeyCode 字符串 | 含义 |
| :--- | :--- | :--- |
| **Home 键** | `'KEYCODE_HOME'` | 返回桌面 |
| **返回键** | `'KEYCODE_BACK'` | 返回上一级 |
| **菜单键** | `'KEYCODE_MENU'` | 弹出菜单栏 |
| **电源键** | `'KEYCODE_POWER'` | 电源键（息屏/亮屏） |
| **音量+ / -** | `'KEYCODE_VOLUME_UP'` / `'DOWN'` | 调整音量 |
| **回车键** | `'KEYCODE_ENTER'` | 确认 / 回车 |
| **删除键** | `'KEYCODE_DEL'` | 退格删除字符 |

---

### 5.4 完整 Python 自动化脚本示例

在 PC 端创建 `test_script.py`：

```python
# -*- coding: encoding -*-
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

# 1. 连接设备
print("正在连接 Android 设备...")
device = MonkeyRunner.waitForConnection(5.0, "127.0.0.1:7555")

if not device:
    print("连接失败！")
    sys.exit(1)

# 2. 唤醒设备屏幕
device.wake()

# 3. 启动应用
print("启动应用...")
device.startActivity(component="com.miui.calculator/com.miui.calculator.cal.CalculatorActivity")
MonkeyRunner.sleep(2)

# 4. 截图 baseline
shot1 = device.takeSnapshot()
shot1.writeToFile('D:/calc_launch.png', 'png')

# 5. 点击数字与按键 (x, y)
device.touch(500, 1200, MonkeyDevice.DOWN_AND_UP)
MonkeyRunner.sleep(0.5)

# 6. 滑动屏幕
device.drag((300, 1000), (300, 400), 1.0, 10)
MonkeyRunner.sleep(1)

# 7. 按返回键退出
device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)
print("测试完成。")
```

**运行命令**（需在安装了 Android SDK 的环境中）：
```bash
monkeyrunner test_script.py
```

---

## 6. 企业级压力测试实战与避坑指南

### 6.1 夜间 8~12 小时无人值守压测模板

在企业实际测试中，通常在夜间进行 8~12 小时的大概率随机稳定性压力测试。以下是经过生产环境验证的标准化测试命令：

```bash
adb shell monkey -p com.yourcompany.app \
  --throttle 300 \
  --pct-touch 60 \
  --pct-motion 20 \
  --pct-appswitch 10 \
  --pct-syskeys 5 \
  --pct-nav 5 \
  --ignore-crashes \
  --ignore-timeouts \
  --ignore-security-exceptions \
  --kill-process-after-error \
  --monitor-native-crashes \
  -v -v -v 1000000 > D:\monkey_overnight_test.log 2>&1
```

*说明：按 300ms 延迟计算，1,000,000 次事件大约运行 8.3 小时。*

---

### 6.2 防“跑偏”与防“误触”策略

Monkey 的伪随机点击可能会跳出 App，甚至误触系统设置（如关闭 Wi-Fi、开启飞行模式、关机或修改系统语言），导致测试中断。

#### 💡 避坑防护四要点：

1.  **屏蔽系统设置与关键 App（使用包名黑名单）**：
    创建 `blacklist.txt` 文件并推送到手机：
    ```text
    com.android.settings
    com.android.phone
    com.android.systemui
    ```
    运行命令中加入：`--pkg-blacklist-file /sdcard/blacklist.txt`

2.  **降低系统键与导航键比例**：
    将 `--pct-syskeys` 和 `--pct-nav` 控制在 **5% 以下**，避免频繁触发 Home 键或关机长按菜单。

3.  **锁定输入法与键盘**：
    测试前切换设备输入法为 **Null Keyboard**（空输入法）或专用的测试输入法，防止点击输入框时弹出巨大的软键盘遮挡 UI。

4.  **自动保持屏幕常亮与静音**：
    在压测前执行以下 ADB 命令配置设备状态：
    ```bash
    # 设置屏幕超时时间为永久常亮
    adb shell settings put system screen_off_timeout 2147483647

    # 关闭自动旋转
    adb shell settings put system accelerometer_rotation 0

    # 静音设备
    adb shell media volume --stream 3 --set 0
    ```

---

### 6.3 稳定性评估指标与合格标准

在软件发布前，稳定性压力测试通常有明确的量化质量门禁（Quality Gate）：

$$\text{Crash 率} = \frac{\text{Crash 发生次数}}{\text{测试运行总时长 (小时)}}$$

$$\text{ANR 率} = \frac{\text{ANR 发生次数}}{\text{测试运行总时长 (小时)}}$$

| 评估指标 | 行业常见标准 / 门禁要求 | 备注 |
| :--- | :--- | :--- |
| **Crash 率** | $< 0.05$ 次/小时（或 **千分之一 / 万分之五** 事件） | 核心主流程 Activity 必须 **0 Crash** |
| **ANR 率** | $< 0.01$ 次/小时 | 主线程无严重卡死阻断 |
| **测试执行完成率** | $100\%$ | 能够在指定时间内完成指定事件数 |
| **内存泄漏 (Memory Leak)** | 8 小时压测后，内存无持续阶梯状上涨，无 OOM | 结合 `dumpsys meminfo` 监控 |

---
