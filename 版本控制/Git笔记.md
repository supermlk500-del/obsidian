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
git remote set-url origin git@gitee.com:deer-superman_0/text.git
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


