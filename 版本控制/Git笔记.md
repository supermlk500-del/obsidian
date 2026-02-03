# Git 有两种推送方式

|方式|远程地址形式|是否需要 SSH Key|
|---|---|---|
|HTTPS|`https://gitee.com/xxx/xxx.git`|❌|
|SSH|`git@gitee.com:xxx/xxx.git`|✅|

> ⚠️ 如果使用 SSH，却没有配置 SSH Key  
> 👉 一定会报：`Permission denied (publickey)`

## ssh
### 在gitee新建一个仓库

![[新建仓库2.png]]
![[新建仓库2.png]]
- 不需要勾选下面的东西

### 初始化仓库
- 命令
```bash
git init
```

- 结果。初始化成功后有一个`.git`文件夹
![[初始化成功文件夹变化.png]]

![[命令行成功变化.png]]

### 查看状态

- 新建一个文件；查看状态命令
```bash
git status
```
- 结果
![[新建后查看状态.png]]
**这里说明git已经识别到了新增的文件，但是还没有纳入管理**


- git在使用时分为工作区和暂存区
	- 文件需要先在暂存区保存，然后才能推送到工作区
```bash
git add .
```
**这里是把所有识别到的都添加到暂存区；你也可以把`.`更换成其他文件的名字**
```bash
git commit -m "日志"
```
**这里是提交到本地仓库，一定需要写上传的日志，这里可以写你想要写的和项目相关的内容**

==注意：缺少任何一步在push的时候都会失败==
### 关联

![[新建的仓库页面.png]]
```bash
git remote add origin https://gitee.com/你的用户名/仓库名.git
```
![[导航.png]]
- 查看是否成功
```bash
git remote -v
```
### 已经添加过仓库时，需要修改
```bash
git remote set-url origin git@gitee.com:用户名/仓库地址
```

### 推送
- 查看分支，再推送的时候需要指定推送哪一个
```bash
git branch
```
- 命令
```bash
git push -u origin '分支'

```

#### 推送会报错
 - 第一次时没有配置`ssh key`
**验证**
```bash
ls ~/.ssh
```
![[ssh key验证.png]]
出现这样的说明没有配置过`ssh key`
#### ==生成ssh key==
```bash
ssh-keygen -t rsa -b 4096 -C "你的邮箱"
```
导航
```text
Enter file in which to save the key:   👉 直接回车
Enter passphrase:                     👉 直接回车
Enter same passphrase again:          👉 直接回车

```
#### 查看
```bash
cat ~/.ssh/id_rsa.pub
```

![[密钥结果.png]]
- 去gitee添加密钥
![[添加密钥导航.png]]
- 测试是否成功
```bash
ssh -T git@gitee.com
```
- 正确结果
```bash
Hi xxx! You've successfully authenticated.
```
==至此已经可以正确推送==


##  版本回退
- 每一次`commit`的时候的日志都会被记录
**查看提交历史**
```bash
git log --oneline
```
预期结果
![[版本历史.png]]

- 最上面一个历史是最近版本的
- 左边是commit id
### 写错了未提交

```bash
git restore text.txt
```



## 回退之前必须先做的事（很重要）

### 先看提交历史

```bash
git log --oneline
```

示例输出：

```text
a1b2c3d 更新笔记A
e4f5g6h 初始化笔记
```

- 左边：commit id（前 7 位够用）
    
- 上面的是最新提交
    

---

## 不同回退场景，对应不同命令

---

## 场景一：只是写错了，还没提交

### 使用场景

- 改了文件
    
- 后悔了
    
- **还没执行 git commit**
    

### 操作方式

```bash
git restore 文件名
```

或者恢复全部：

```bash
git restore .
```

### 预期结果

```text
工作区文件恢复到最近一次提交状态
```

---

## 场景二：已经 add 了，但还没 commit

### 使用场景

- 执行过 `git add`
    
- 发现不该提交
    

### 操作方式

```bash
git restore --staged 文件名
```

或者全部取消暂存：

```bash
git restore --staged .
```

### 预期结果

```text
文件从暂存区移回工作区
内容不丢失
```

---

## 场景三：已经 commit，但想“回到上一个版本”

### 使用场景

- 提交完立刻后悔
    
- 不想要刚刚那次提交
    

---

### 安全回退（推荐）

```bash
git reset --soft HEAD^
```

含义说明：

- 回退一个提交
    
- **修改内容仍然保留**
    
- 文件处于暂存区
    

### 预期结果

```text
提交消失
文件内容仍在
```

---

### 中等回退（常用）

```bash
git reset --mixed HEAD^
```

含义说明：

- 回退一个提交
    
- 内容保留在工作区
    
- 暂存区清空
    

---

### 强制回退（慎用）

```bash
git reset --hard HEAD^
```

⚠️ **危险操作**

含义说明：

- 提交消失
    
- 修改内容直接丢失
    

---

## 场景四：回退到任意一次历史提交

### 使用场景

- 想回到很早之前的版本
    

### 操作方式

```bash
git reset --hard commit_id
```

示例：

```bash
git reset --hard a1b2c3d
```

### 预期结果

```text
当前分支回到指定提交状态
后续提交不再可见
```

---

## 场景五：已经 push 过，还想回退（重点）

### 强烈建议：**不要用 reset**

因为：

- reset 会改历史
    
- 会影响远程仓库
    
- 多人协作容易出问题
    

---

### 正确做法：使用 revert（推荐）

```bash
git revert commit_id
```

含义说明：

- 不删除历史
    
- 新增一次“反向提交”
    
- 安全、可追溯
    

### 预期结果

```text
生成一个新的提交
用于撤销指定版本的修改
```

---

## 场景六：我不知道回退到哪了，想“救命”

### 使用 reflog（救命神器）

```bash
git reflog
```

示例：

```text
a1b2c3d HEAD@{0}: reset: moving to HEAD^
e4f5g6h HEAD@{1}: commit: 更新笔记
```

然后：

```bash
git reset --hard e4f5g6h
```

---

## 已经 push 但还是要强制回退（不推荐）

```bash
git push origin main --force
```

⚠️ **风险说明**

- 会覆盖远程历史
    
- 别人本地会乱
    
- 只适合个人仓库 / 笔记仓库
    

---

## 你这种「个人笔记仓库」的推荐方案

|场景|推荐操作|
|---|---|
|未提交|restore|
|已提交未推送|reset|
|已推送|revert|
|回退救命|reflog|



## 创建分支
- 创建分支，同时会自动切换到分支。而且这里的分支会自动有main分支的东西
```bash
git checkout -b dev
```
- 切换分支
```bash
git checkout dev
```
- 在分支创建一个文件时
```bash
touch text.text
vim text.txt
```

#### **如果没有执行以下操作，那么只要不发生冲突，未提交的工作区内容，会被原样带回到主分支中**
```bash
git add text.txt
git commit -m "xxx"
```
 - 这时在主分支查看分支创建的内容就会被看到
 - 只要执行了上面两行内容，主分支就看不到这里的内容
#### 合并分支
```bash
git merge dev
```
#### 删除分支
```bash
git branch -d dev
```
- 含义是只删除已经合并过的分支

```bash
git branch -D dev
```
- 不管是否合并过强制删除

##### 删除远程分支

```bash
git push origin --delete dev
```

## 更新
```bash
git pull
git pull gitee main
```
