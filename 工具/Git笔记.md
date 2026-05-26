# Git 团队协作指南

---

## 一、Git 是怎么工作的

在动手之前，先理解 Git 的四个区域：

|区域|说明|
|---|---|
|工作区（Working Directory）|你正在编辑的文件|
|暂存区（Staging Area）|`git add` 之后，准备提交的文件|
|本地仓库（Local Repo）|`git commit` 之后，已保存的版本|
|远程仓库（Remote Repo）|`git push` 之后，团队共享的版本|

数据流向：

```text
工作区  ──git add──▶  暂存区  ──git commit──▶  本地仓库  ──git push──▶  远程仓库
```

---

## 二、环境准备

### 2.1 推送方式

|方式|远程地址形式|是否需要 SSH Key|
|---|---|---|
|HTTPS|`https://gitee.com/xxx/xxx.git`|不需要|
|SSH|`git@gitee.com:xxx/xxx.git`|需要|

### 2.2 配置 SSH Key（使用 SSH 方式时需要）

**检查是否已有 SSH Key：**

```bash
ls ~/.ssh
```

如果看到 `id_rsa` 和 `id_rsa.pub`，说明已经配置过。

**生成 SSH Key：**

```bash
ssh-keygen -t rsa -b 4096 -C "你的邮箱@example.com"
```

三次提示都直接回车即可。

**查看公钥：**

```bash
cat ~/.ssh/id_rsa.pub
```

将输出的内容复制到代码托管平台的 SSH Key 设置中（GitHub: Settings → SSH and GPG keys；Gitee: 设置 → SSH 公钥）。

**测试连接：**

```bash
ssh -T git@gitee.com    # Gitee
ssh -T git@github.com   # GitHub
```

成功会显示类似 `Hi xxx! You've successfully authenticated.`

> 一个 SSH Key 可以同时用于 GitHub 和 Gitee，不会冲突。

---

## 三、基本操作

### 3.1 初始化仓库

```bash
git init
```

执行后项目根目录会生成 `.git` 文件夹，Git 从此开始追踪这个项目。

### 3.2 查看状态

```bash
git status
```

它会告诉你：哪些文件修改了、哪些在暂存区、哪些还没被追踪。

### 3.3 添加到暂存区

```bash
git add .                  # 添加所有变更
git add 文件名              # 添加指定文件
```

### 3.4 提交到本地仓库

```bash
git commit -m "feat: 完成了登录页面"
```

提交信息后面会讲到规范，现在先记住：**每次 commit 必须写清楚改了什么。**

### 3.5 关联远程仓库

```bash
git remote add origin https://gitee.com/用户名/仓库名.git
```

验证是否关联成功：

```bash
git remote -v
```

如果需要修改已关联的地址：

```bash
git remote set-url origin git@gitee.com:用户名/仓库名.git
```

### 3.6 推送到远程

```bash
git branch                  # 先确认当前在哪个分支
git push -u origin main     # 首次推送需要 -u
git push                    # 后续推送直接用
```

### 3.7 从远程更新

```bash
git pull origin main
```

---

## 四、版本回退

### 4.1 查看提交历史

```bash
git log --oneline
```

输出示例：

```text
a1b2c3d feat: 更新用户页面
e4f5g6h feat: 添加登录功能
```

每次 `commit` 都有一条记录，左边是 commit id，上面是最新的。

### 4.2 场景一：改乱了，还没 add

文件改坏了，想回到最近一次 commit 的状态：

```bash
git restore 文件名
git restore .              # 恢复所有文件
```

### 4.3 场景二：已经 add 了，但还没 commit

把文件从暂存区撤回来，修改内容保留：

```bash
git restore --staged 文件名
git restore --staged .     # 取消所有暂存
```

### 4.4 场景三：已经 commit 了，想撤销

**安全回退（推荐）**—— 提交撤销，修改内容保留在暂存区：

```bash
git reset --soft HEAD^
```

**中等回退**—— 提交撤销，修改内容保留在工作区：

```bash
git reset --mixed HEAD^
```

**强制回退（慎用）**—— 提交和修改内容全部丢弃：

```bash
git reset --hard HEAD^
```

### 4.5 场景四：回退到指定的历史版本

```bash
git reset --hard a1b2c3d
```

### 4.6 场景五：已经 push 了，需要撤销

**不要用 `reset` + `--force` 去覆盖远程历史**（多人协作时这会破坏别人的工作）。

正确做法是用 `revert`，生成一个新的"反向提交"来撤销之前的修改：

```bash
git revert a1b2c3d
```

这样做的好处：
- 历史记录完整，可追溯
- 不影响团队其他人
- 安全、可控

### 4.7 场景六：回退之后后悔了——reflog 救命

```bash
git reflog
```

输出示例：

```text
a1b2c3d HEAD@{0}: reset: moving to HEAD^
e4f5g6h HEAD@{1}: commit: feat: 更新页面
```

找到你想回去的那个 commit id，再 reset 过去即可：

```bash
git reset --hard e4f5g6h
```

### 4.8 回退策略速查

|场景|推荐命令|
|---|---|
|改乱了没 add|`git restore`|
|add 了没 commit|`git restore --staged`|
|commit 了没 push|`git reset --soft HEAD^`|
|已经 push 了|`git revert`（不用 reset）|
|回退后后悔了|`git reflog` + `git reset`|

---

## 五、分支操作

### 5.1 为什么需要分支

分支让你在不影响主线的情况下开发新功能。每个人在自己的分支上工作，互不干扰。

### 5.2 创建并切换分支

```bash
git checkout -b feature/login    # 创建并切换到新分支
git checkout main                # 切换回 main
git branch                       # 查看所有分支
```

新分支会自动继承来源分支的所有内容。

### 5.3 在分支上开发

```bash
# 写代码...
git add .
git commit -m "feat: add login page"
```

> 注意：如果只修改了文件但没有 commit，切换回主分支时未提交的改动会被带过去。**在分支上开发完一定要 commit。**

### 5.4 合并分支

先切换到目标分支（比如 main），再把功能分支合并进来：

```bash
git checkout main
git merge feature/login
```

### 5.5 删除分支

```bash
git branch -d feature/login           # 删除已合并的本地分支
git branch -D feature/login           # 强制删除（不管是否合并）
git push origin --delete feature/login # 删除远程分支
```

---

## 六、团队协作工作流

### 6.1 核心原则

**不要直接修改 `main` 分支。所有开发在 `feature` 分支进行，通过 Pull Request 合并。**

### 6.2 推荐分支结构

```text
main              ← 稳定、可发布版本
develop           ← 团队日常开发主线
feature/login     ← 功能分支
feature/schedule
fix/login-token   ← 修复分支
```

### 6.3 标准工作流程

**第一步：从 develop 拉出自己的分支**

```bash
git checkout develop
git pull origin develop
git checkout -b feature/login
```

**第二步：在自己分支开发和提交**

```bash
git add .
git commit -m "feat: add login form"
```

**第三步：推送自己的分支**

```bash
git push -u origin feature/login
```

**第四步：在平台上发起 Pull Request**

```text
feature/login  →  develop
```

**第五步：负责人 Review 后合并**

审核要点：
- 代码逻辑是否正确
- 是否有冲突
- 命名和注释是否清晰
- 是否混入了无关改动

**第六步：功能稳定后，develop 合并到 main**

```text
feature/*  →  develop  →  main
```

### 6.4 为什么不能直接推 main

所有人直接推 main 会导致：
- 一个人的错误代码影响所有人
- 多人同时改同一文件，冲突频繁
- 出问题难以定位责任人
- 没有代码审查，质量无法保证

### 6.5 团队成员分工

**普通成员：**
- 从 develop 拉分支
- 在自己分支开发
- 提交 PR 并等待 review
- 根据反馈修改代码

**负责人/组长：**
- 划分模块边界，避免冲突
- 维护 develop 和 main 的稳定
- 审核 PR
- 处理合并冲突
- 控制版本发布节奏

---

## 七、分支保护设置

### 7.1 在哪里设置

```text
GitHub/Gitee 仓库 → Settings → Branches → Branch protection rules
```

设置分支保护需要 Owner 或 Admin 权限。

### 7.2 推荐对 main 和 develop 开启的选项

**必开：**
- `Require a pull request before merging` —— 必须通过 PR 才能合并
- `Require approvals`（设为 1）—— 至少一人审批
- `Dismiss stale pull request approvals when new commits are pushed` —— 有新提交时重新审批
- `Restrict who can push to matching branches` —— 限制谁能直接推送

**推荐开：**
- `Require conversation resolution before merging` —— 所有讨论解决后才能合并
- `Require linear history` —— 保持线性历史

**不建议开：**
- `Allow force pushes` —— 允许强制推送（危险）
- `Allow deletions` —— 允许删除分支

### 7.3 关于 "不允许绕过"

如果勾选 `Do not allow bypassing the above settings`，所有成员（包括管理员）都必须遵守规则。

如果想保留管理员紧急情况下的处理权限，可以不勾选此项。

---

## 八、推送被拒绝的原因与处理

推送时遇到 `rejected` 不要紧张，通常是以下原因：

### 8.1 分支保护规则生效

比如分支要求至少 1 人审批，你自己不能给自己审批。这不是 Git 坏了，是保护规则在正常工作。

**处理方式：** 走正常的 PR + Review 流程。

### 8.2 远程分支比本地更新

报错示例：

```text
! [rejected] main -> main (fetch first)
```

说明别人已经推送了新提交，你的本地版本落后了。

**处理方式：**

```bash
git pull origin main     # 先拉取最新代码
# 如有冲突先解决冲突
git push origin main     # 再推送
```

---

## 九、提交规范

### 9.1 分支命名

统一前缀，见名知意：

|前缀|用途|示例|
|---|---|---|
|`feature/`|新功能|`feature/login`|
|`fix/`|修复问题|`fix/token-refresh`|
|`docs/`|文档|`docs/api-guide`|
|`refactor/`|重构|`refactor/user-module`|
|`ui/`|界面调整|`ui/dashboard`|

### 9.2 Commit Message 规范

```text
feat:     新功能
fix:      修复 bug
docs:     文档修改
refactor: 重构（不改变功能）
style:    格式调整（空格、分号等）
test:     测试相关
chore:    构建、依赖等杂项
```

示例：

```bash
git commit -m "feat: add login form validation"
git commit -m "fix: resolve token auto-refresh failure"
git commit -m "docs: update deployment guide"
```

### 9.3 提交身份配置

Git 提交记录中显示的用户信息来自本地配置，建议团队成员统一设置：

```bash
git config --global user.name "张三"
git config --global user.email "zhangsan@company.com"
```

---

## 十、常见问题速查

### push 报错 `src refspec xxx does not match any`

原因：要推送的分支在本地不存在，或还没有 commit。

```bash
git checkout -b feature/new
git add .
git commit -m "feat: new feature"
git push -u origin feature/new
```

### git pull 后进入了 Vim 界面

Git 需要你确认 merge 的提交信息。操作方式：

```text
按 Esc
输入 :wq
按 Enter
```

---

## 总结

### 一句话版

**不要直接改 main，每个人在自己的 feature 分支开发，通过 PR 合并到 develop，稳定后再进 main。**

### 六步版

1. 拉最新 develop
2. 创建自己的 feature 分支
3. 在分支上开发和提交
4. push 到远程
5. 发起 PR 等待 review
6. 审核通过后合并

### 最终目标

- `main` 永远稳定，随时可发布
- `develop` 持续集成，团队共享进度
- `feature` 隔离开发，互不干扰
- PR 保证代码质量
- Review 保证团队协作有序
