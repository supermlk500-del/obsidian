# 部署
## 开源地址
(https://github.com/zai-org/Open-AutoGLM)
```shell
git clone https://github.com/zai-org/Open-AutoGLM
```
- 通过命令添加仓库


## 一、Open-AutoGLM 
### 1️⃣ 项目定位

**Open-AutoGLM = 手机自动化 Agent 框架**

它做的事是：

```
自然语言指令
→ 大模型理解
→ 生成操作步骤（点 / 滑 / 输入）
→ 通过 ADB 控制真实手机
```

📌 **它不是模型本身**  
📌 **它只是“大脑 + 手脚”的中枢**

---

### 2️⃣ 系统架构（非常重要）

```
┌──────────────┐
│  你的指令     │
└──────┬───────┘
       ↓
┌──────────────┐
│ AutoGLM Agent│  ← 本项目
└──────┬───────┘
       ↓ HTTP
┌──────────────┐
│ 模型服务      │  ← 智谱 / ModelScope / 本地
└──────┬───────┘
       ↓
┌──────────────┐
│ ADB / HDC    │
└──────┬───────┘
       ↓
📱 真实手机
```

---

## 二、环境准备（你已经做过，但这里是标准版）

### 1️⃣ Python 环境

- Python ≥ 3.10
    
- 强烈建议虚拟环境
    

```powershell
python -m venv venv
.\venv\Scripts\activate
```

---

### 2️⃣ 项目安装

```powershell
pip install -r requirements.txt
pip install -e .
```

---

## 三、模型 & API Key（最容易搞混的点）

### 1️⃣ 两条路线（一定要分清）

|路线|是否推荐新手|base-url|
|---|---|---|
|云模型（智谱 / ModelScope）|✅ 强烈推荐|非 localhost|
|本地模型（vLLM / SGLang）|❌ 不推荐|localhost:8000|

你走的是：  
👉 **云模型（智谱 BigModel）**

---

### 2️⃣ 智谱 BigModel 正确参数

```text
base-url: https://open.bigmodel.cn/api/paas/v4
model:    autoglm-phone
apikey:   sk-xxxxxx
```

---

### 3️⃣ 正确配置 API Key（安全）

#### 推荐方式：环境变量

```powershell
setx PHONE_AGENT_API_KEY "sk-你的key"
```

**重新打开终端后使用：**

```powershell
python main.py --base-url https://open.bigmodel.cn/api/paas/v4 --model autoglm-phone
```

⚠️ **API Key 永远不要发给别人**

---

## 四、ADB & 手机控制（成败关键）

### 1️⃣ ADB 是否正常

```powershell
adb devices
```

✅ 正常输出：

```text
xxxxxxxx    device
```

---

### 2️⃣ 小米 / Redmi 必须额外做的一步（重点）

❗ **必须开启：USB 调试（安全设置）**

路径（可能略有差异）：

```
设置 → 更多设置 → 开发者选项
```

同时开启：

- ✅ USB 调试
    
- ✅ USB 调试（安全设置）
    

⚠️ **然后必须重启手机**

---

### 3️⃣ 为什么这一步这么重要？

没有这个权限：

|功能|是否可用|
|---|---|
|截图|✅|
|投屏|✅|
|点击 / 滑动 / 输入|❌|

scrcpy、AutoGLM、ADB Keyboard **全部依赖它**

---

## 五、scrcpy（调试神器）

### 1️⃣ scrcpy 的作用

- 实时投屏
    
- 用鼠标验证是否能点
    
- 调试自动化行为
    

```powershell
scrcpy
```

👉 能点能滑 = 权限 OK

---

### 2️⃣ scrcpy 报错核心原因总结

```text
INJECT_EVENTS permission
```

= **没开 USB 调试（安全设置）或没重启**

---

## 六、ADB Keyboard（输入必需）

### 1️⃣ 为什么需要它？

系统输入法 **不允许 ADB 注入文本**  
ADB Keyboard 是专门给自动化用的输入法

---

### 2️⃣ 安装 & 启用

```powershell
adb shell ime enable com.android.adbkeyboard/.AdbIME
```

手机里确认启用。

---

## 七、Open-AutoGLM 的使用方式（核心）

---

### ✅ 方式 1：交互模式（推荐新手）

```powershell
python main.py `
  --base-url https://open.bigmodel.cn/api/paas/v4 `
  --model autoglm-phone
```

然后直接输入：

```text
打开微信
```

---

### ✅ 方式 2：单次任务（最稳定）

```powershell
python main.py `
  --base-url https://open.bigmodel.cn/api/paas/v4 `
  --model autoglm-phone `
  "打开微信给文件传输助手发送消息：部署成功"
```

🎉 **这是“是否成功”的黄金测试**

---

## 八、AutoGLM 能做什么？（能力边界）

### 1️⃣ 擅长的

- 打开 App
    
- 搜索 / 点击 / 滑动
    
- 多步骤任务
    
- 跨 App 操作
    

例子：

```text
打开京东搜索洗发水，比较价格后选择最便宜的
```

---

### 2️⃣ 不擅长 / 会请求接管的

- 登录
    
- 验证码
    
- 支付
    
- 银行 / 风控页面
    

👉 会触发 **Take_over（人工接管）**

---

## 九、停止 / 中断（你问过的）

### 正确停止方式

```text
Ctrl + C
```

---

### 如果手机还被控制

```powershell
adb kill-server
adb start-server
```

---

## 十、常见问题速查表（非常实用）

|问题|原因|解决|
|---|---|---|
|502 localhost:8000|没跑本地模型|用云 base-url|
|能看不能点|没开安全 USB 调试|打开 + 重启|
|中文输入失败|没 ADB Keyboard|安装并启用|
|scrcpy 报 INJECT_EVENTS|权限不足|同上|
|401 Invalid API Key|Key 错 / 过期|重建 Key|

---

## 十一、你现在的真实水平定位 🧠

你已经完成了：

- ✅ Python 环境
    
- ✅ 项目安装
    
- ✅ 云模型调用
    
- ✅ API Key 配置
    
- ✅ scrcpy 调试
    
- ✅ ADB 权限问题
    
- ✅ 真机自动化
    

👉 **已经超过 90% 新手**

---

## 十二、下一步进阶方向（你可以选）

你可以直接告诉我你想走哪条：

1. 🔧 **二次开发（改 Agent 行为）**
    
2. 🧪 **写自动化脚本 / 批量任务**
    
3. 🧠 **理解 Agent 源码结构**
    
4. 🖥 **多手机并发控制**
    
5. 🔐 **安全 / 权限 / 风控机制**
    


Open-AutoGLM 有 **两种完全不同的运行方式**：

|模式|base-url|是否需要本地模型|
|---|---|---|
|✅ 云模型（推荐）|[https://open.bigmodel.cn/](https://open.bigmodel.cn/)...|❌ 不需要|
|❌ 本地模型|[http://localhost:8000/v1](http://localhost:8000/v1)|✅ 必须先起服务|

