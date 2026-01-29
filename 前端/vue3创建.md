在 Windows 系统上创建 Vue 项目（**与宝塔面板无关**，宝塔用于服务器部署，本地开发需独立环境），请按以下步骤操作。**即使你使用宝塔面板管理服务器，本地开发也需在自己电脑完成**：

---

### ✅ 一、环境准备（必须先完成）
#### 1. 安装 Node.js
- 下载地址：https://nodejs.org/zh-cn/  
  **选择 LTS 版本**（当前最新 LTS 是 v20.x）
- 安装时**勾选** `Automatically install necessary tools`（自动安装构建工具）
- 验证安装：
  ```powershell
  node -v  # 应显示 v20.x
  npm -v   # 应显示 10.x+
  ```

#### 2. 配置国内镜像（加速安装）
```powershell
npm config set registry https://registry.npmmirror.com
```

---

### ✅ 二、创建 Vue 项目（3种方式任选其一）
#### ⭐ 推荐方式：使用 `create-vue`（官方最新工具，Vue 3）
```powershell
# 1. 创建项目目录
mkdir my-vue-app && cd my-vue-app

# 2. 初始化项目（自动安装依赖）
npm create vue@latest

# 3. 按提示操作：
# ? Project name: (直接回车用默认名)
# ? Add TypeScript? No
# ? Add JSX Support? No
# ? Add Vue Router? Yes  # 需要路由选 Yes
# ? Add Pinia? Yes       # 需要状态管理选 Yes
# ? Add Vitest? No
# ? Add Cypress? No
# ? Add ESLint? Yes      # 强烈建议开启
# ? Add Prettier? Yes    # 强烈建议开启

# 4. 安装依赖
npm install

# 5. 启动开发服务器
npm run dev
```
✅ **成功标志**：  
终端显示 `Local: http://localhost:5173/`，浏览器打开此地址看到 Vue 默认页面。

---

#### 备选方式1：Vue CLI（传统方式，支持 Vue 2/3）
```powershell
# 1. 全局安装 Vue CLI
npm install -g @vue/cli

# 2. 创建项目
vue create my-project
# 按方向键选择：
#   > Default ([Vue 3] babel, eslint)  # 推荐
#   > Manually select features          # 自定义配置

# 3. 进入项目 & 启动
cd my-project
npm run serve
```

#### 备选方式2：Vite 原生命令（极速创建）
```powershell
npm create vite@latest my-vue-app -- --template vue
cd my-vue-app
npm install
npm run dev
```

---

### ✅ 三、关键目录说明
```diff
my-vue-app/
├── node_modules/   # 依赖包（勿提交到 git）
├── public/         # 静态资源（favicon.ico 等）
├── src/
│   ├── assets/     # 项目图片/字体
│   ├── components/ # 组件
│   ├── App.vue     # 根组件
│   └── main.js     # 入口文件
├── .eslintrc.cjs   # ESLint 配置
├── vite.config.js  # Vite 配置
├── package.json    # 项目依赖和脚本
└── index.html      # 单页入口
```

---

### ✅ 四、开发常用命令
| 命令                | 作用                     |
|---------------------|--------------------------|
| `npm run dev`       | 启动开发服务器（实时编译）|
| `npm run build`     | **构建生产环境文件**（部署用）|
| `npm run preview`   | 本地预览生产构建结果      |
| `npm run lint`      | 修复代码格式问题          |

> 💡 **重要提示**：  
> - **开发时用 `npm run dev`**，生成的文件在内存中，**不会**生成 `dist` 目录  
> - **部署时必须执行 `npm run build`**，生成 `dist` 目录（含所有静态文件）

---

### ✅ 五、部署到宝塔面板（后续步骤）
当项目开发完成需上线时：
1. 在本地执行构建：
   ```powershell
   npm run build  # 生成 dist 目录
   ```
2. 通过宝塔面板操作：
   - **Linux 服务器**（推荐）：
     1. 在宝塔创建网站（如 `vueapp.yourdomain.com`）
     2. 上传 `dist` 目录内所有文件到网站根目录
     3. 设置伪静态（SPA 需要）：
        ```nginx
        location / {
          try_files $uri $uri/ /index.html;
        }
        ```
   - **Windows 服务器**（不推荐，仅测试用）：
     1. 上传 `dist` 文件到 `C:\BtSoft\wwwroot\你的站点`
     2. 无需伪静态（IIS 需单独配置，复杂且不推荐）

> ⚠️ **血泪建议**：  
> **永远不要在 Windows 服务器部署 Vue 项目**！  
> - Windows 版宝塔对 Node.js 支持极差  
> - 静态文件服务性能低下  
> - 路由刷新 404 问题难解决  
> **✅ 正确做法**：  
> 1. 本地开发 → 2. `npm run build` 生成静态文件 → 3. **部署到 Linux 服务器的宝塔面板**

---

### ❌ 常见错误解决
| 问题现象                  | 解决方案                                  |
|---------------------------|------------------------------------------|
| `command not found: vue`  | 重新安装：`npm install -g @vue/cli`       |
| 启动后白屏                | 检查控制台错误，通常因路由未配置 404 降级 |
| 依赖安装卡在 `sill idealTree` | 换淘宝镜像：`npm config set registry https://registry.npmmirror.com` |
| 端口 5173 被占用          | 在 `vite.config.js` 中修改：`server: { port: 8080 }` |

---

### 💡 终极建议
1. **开发环境**：  
   - 用 VSCode + [Volar 插件](https://marketplace.visualstudio.com/items?itemName=Vue.volar)  
   - 安装 [Vue Devtools](https://devtools.vuejs.org/) 浏览器插件
2. **生产部署**：  
   - **放弃 Windows 服务器**，购买 Linux 云服务器（阿里云/腾讯云 24 元/月 轻量应用服务器）  
   - 在 Linux 安装[宝塔面板](https://www.bt.cn) → 用「网站」功能托管 `dist` 静态文件  
   - 配置 Nginx 伪静态（[官方文档](https://www.bt.cn/bbs/thread-36540-1-1.html)）

> 🌐 **学习资源**：  
> - Vue 3 官方教程：https://cn.vuejs.org/  
> - Vite 文档：https://cn.vitejs.dev/  
> - 宝塔部署 Vue 指南：https://www.bt.cn/bbs/thread-47889-1-1.html  

遇到具体报错时，提供**完整错误截图+操作步骤**可进一步分析！