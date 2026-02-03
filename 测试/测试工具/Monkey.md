## monkey压力测试

```bash
monkey -p [包名] -p [包名] -v 100//指定包模拟用户随机事件运行100次
```

### 保存日志

```bash
adb shell monkey -p com.miui.calculator.go -v 500 > "D:\apk\monkey.log"
```

### 不同 `-v` 输出有什么区别（重点）

#### 1️⃣ `-v`（一级日志）

`monkey -p com.xxx.app -v 100`

输出内容：

- Monkey 启动信息
    
- 随机种子 seed
    
- 执行事件总数
    
- 是否崩溃 / ANR
    
- 最终结果（PASS / FAIL）
    

📌 适合：  
**快速看有没有挂**

---

#### 2️⃣ `-v -v`（二级日志）

`monkey -p com.xxx.app -v -v 100`

在 `-v` 基础上 **多输出**：

- 每个事件的类型（点击 / 滑动 / 按键）
    
- 当前运行的 Activity
    
- 事件序号
    

📌 适合：  
**定位问题大概发生在哪**

---

#### 3️⃣ `-v -v -v`（三级日志，最常用🔥）

`monkey -p com.xxx.app -v -v -v 100`

在 `-vv` 基础上 **再多输出**：

- **每一个事件的详细内容**
    
- 精确到点击坐标
    
- 完整 Activity 切换过程

### `-s`
### `--throttle`
- 在事件之间插入固定延迟。通过这个选项可以减缓Monkey的执行速度。
```bash
adb shell monkey -p com.ibox.calculators --throttle 300 -v 100
```
- 人的思考时间是300毫秒一个动作
### 事件
**只对 `com.ibox.calculators` 这个 App，执行 1000 次随机事件，其中 80% 是点击事件，20% 是滑动/手势事件。**
```bash
adb shell monkey -p com.ibox.calculators --pct-touch 800 --pct-motion 200 1000
```

## Monkey脚本

# 🐒 MonkeyRunner 常用 API 命令整理（官方文档向）

> MonkeyRunner：基于 **Python** 的 Android 自动化测试工具  
> 主要用于 **UI 操作、功能自动化、回放脚本**

---

### 输入与交互类 API（最常用 ⭐⭐⭐）

|API|参数说明|功能说明|
|---|---|---|
|`device.touch(x, y, type)`|`x,y`：屏幕坐标`type`：DOWN / UP / DOWN_AND_UP|模拟触摸/点击|
|`device.drag(x1, y1, x2, y2, duration, steps)`|起点、终点坐标`duration`：拖动时间(s)`steps`：步数|模拟拖拽/滑动|
|`device.press(keycode, type)`|`keycode`：按键码`type`：DOWN / UP / DOWN_AND_UP|模拟物理/虚拟按键|
|`device.type(text)`|`text`：字符串|向当前焦点输入文本|
|`device.wait(ms)`|`ms`：毫秒|等待一段时间|

📌 **说明**：

- 这是对你截图中 `Tap / Drag / DispatchPress` 的 **官方 Python 形式**
    
- 实际项目里更常用这种写法
    

---

### 常用封装动作（和你截图一一对应）

|截图中的命令|MonkeyRunner 官方等价 API|说明|
|---|---|---|
|`Tap(x,y,duration)`|`device.touch(x,y,MonkeyDevice.DOWN_AND_UP)`|点击|
|`DispatchPress(keycode)`|`device.press(keycode, MonkeyDevice.DOWN_AND_UP)`|按键|
|`DispatchString(input)`|`device.type(input)`|输入文本|
|`UserWait(ms)`|`time.sleep(ms/1000)`|脚本等待|
|`Drag(x1,y1,x2,y2,steps)`|`device.drag(...)`|拖拽|
|`RotateScreen(rotation,persist)`|`device.setOrientation()`|旋转屏幕|
|`RunCmd(cmd)`|`device.shell(cmd)`|执行 Shell|

---

### 屏幕与设备控制 API

|API|参数说明|功能|
|---|---|---|
|`device.wake()`|无|点亮屏幕|
|`device.sleep()`|无|关闭屏幕|
|`device.setOrientation(orientation)`|`natural / left / right`|设置屏幕方向|
|`device.getProperty(name)`|系统属性名|获取设备信息|
|`device.reboot()`|无|重启设备|

---

### 截图与图像识别 API（MonkeyRunner 特色 ⭐）

|API|参数说明|功能|
|---|---|---|
|`device.takeSnapshot()`|无|截取当前屏幕|
|`image.writeToFile(path, format)`|保存路径、格式|保存截图|
|`image.getSubImage(rect)`|区域|截取局部|
|`image.sameAs(other, threshold)`|对比图像|判断页面是否变化|

📌 常用于：

- 页面跳转校验
    
- UI 回归测试
    
- 简单图像对比断言
    

---

### Shell / 系统操作 API

|API|参数说明|作用|
|---|---|---|
|`device.shell(cmd)`|Shell 命令|执行 adb shell|
|`device.installPackage(path)`|apk 路径|安装应用|
|`device.removePackage(pkg)`|包名|卸载应用|
|`device.startActivity(component)`|Activity|启动页面|

---

### 常用 KeyCode（必背）

|KeyCode|含义|
|---|---|
|`KEYCODE_HOME`|Home|
|`KEYCODE_BACK`|返回|
|`KEYCODE_MENU`|菜单|
|`KEYCODE_POWER`|电源|
|`KEYCODE_VOLUME_UP`|音量+|
|`KEYCODE_VOLUME_DOWN`|音量-|
|`KEYCODE_ENTER`|回车|

---

### 一个完整官方示例（理解 API 用）

```python
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

device = MonkeyRunner.waitForConnection()

device.touch(500, 800, MonkeyDevice.DOWN_AND_UP)
MonkeyRunner.sleep(1)

device.type("hello")
device.press("KEYCODE_ENTER", MonkeyDevice.DOWN_AND_UP)

device.drag(300, 1000, 300, 300, 1.0, 10)
```

## 完整过程
- 先在电脑上写好脚本
```bash
adb push (文件位置) (目标位置)
```
- 查看脚本
```bash
adb shell cat /sdcard/monkey.txt
```
- 运行脚本
```bash
adb shell monkey -f /sdcard/monkey.txt 1
```
	- 这里的1是执行次数
	- `-f`是表示允许文件

