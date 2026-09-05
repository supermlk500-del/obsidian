# MLK Space REST API 接口文档（学习版）

> 文档版本：v1.0  
> 核对日期：2026-07-26  
> 当前实现：Spring Boot 3.5.15、Spring Security、JWT、MyBatis-Plus、MySQL  
> 接口数量：63 个  
> 事实来源：当前后端 Controller、DTO、VO、Service 与安全配置

本文档是一份独立的接口学习文档。旧版《系统开发文档》中的接口清单属于开发前设计稿，本文件以当前代码为准，覆盖已经实现的接口、请求参数、响应结构、认证方式、业务约束和调用示例。

## 1. 阅读与使用方式

建议按以下顺序学习：

1. 阅读“通用协议”，理解请求头、统一响应和错误码。
2. 调用公开接口，熟悉 GET、查询参数和分页。
3. 调用管理员登录接口，取得 Access Token 和 Refresh Token。
4. 使用 Access Token 调用 `/api/auth/me` 和 `/api/admin/**`。
5. 学习 JSON 写接口、文件上传接口和批量接口。
6. 最后使用 Postman、Apifox 或 JMeter 编排完整业务链路。

### 1.1 本地地址

后端直连地址：

```text
http://127.0.0.1:8080
```

前端开发服务器通过 Vite 代理访问：

```text
http://127.0.0.1:5173/api
```

本文档中的路径统一从 `/api` 开始。例如：

```text
GET http://127.0.0.1:8080/api/posts
```

### 1.2 接口状态标记

- `公开`：不登录也可以访问。
- `可选登录`：游客可以访问；携带有效 Token 时使用登录用户身份。
- `已登录`：必须携带有效 Access Token。
- `管理员`：必须携带角色为 `ADMIN` 的有效 Access Token。
- `未启用`：路径已经存在，但业务流程尚未实现。

## 2. 通用协议

### 2.1 Content-Type

JSON 接口：

```http
Content-Type: application/json
```

文件上传接口：

```http
Content-Type: multipart/form-data
```

客户端使用 `FormData` 或 JMeter 的文件上传功能时，不要手工填写 multipart boundary。

### 2.2 JWT 认证

管理员接口使用 Bearer Token：

```http
Authorization: Bearer <accessToken>
```

默认令牌时间：

| 令牌 | 默认有效期 | 配置项 |
|---|---:|---|
| Access Token | 30 分钟，即 1800 秒 | `MLK_ACCESS_TOKEN_MINUTES` |
| Refresh Token | 30 天 | `MLK_REFRESH_TOKEN_DAYS` |

Access Token 用于访问受保护接口。Refresh Token 只用于刷新 Access Token 和退出登录。

### 2.3 统一成功响应

所有 Controller 成功时当前都返回 HTTP `200`，包括创建、更新和删除接口。

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "requestId": "4de192ac-84bf-4a26-82a2-3bd5a55bff2d",
  "timestamp": "2026-07-26 18:00:00"
}
```

字段说明：

| 字段 | 类型 | 说明 |
|---|---|---|
| `code` | integer | 业务状态码，当前与 HTTP 状态码保持一致 |
| `message` | string | 成功时为 `success`，失败时为错误信息 |
| `data` | any/null | 业务数据；无返回数据时为 `null` |
| `requestId` | string | 请求链路标识，可用于查日志 |
| `timestamp` | string | UTC 时间，格式为 `yyyy-MM-dd HH:mm:ss` |

### 2.4 统一失败响应

```json
{
  "code": 401,
  "message": "用户名或密码错误",
  "data": null,
  "requestId": "4de192ac-84bf-4a26-82a2-3bd5a55bff2d",
  "timestamp": "2026-07-26 18:00:00"
}
```

通用状态码：

| HTTP 状态码 | 含义 | 常见原因 |
|---:|---|---|
| `200` | 成功 | 请求处理完成 |
| `400` | 请求错误 | 参数为空、格式错误、枚举错误、业务字段不合法 |
| `401` | 未认证 | 登录失败、Token 缺失、Token 无效或过期 |
| `403` | 无权限 | 已登录，但角色不允许访问 |
| `404` | 资源不存在 | 文章、项目、评论、文件或用户不存在 |
| `409` | 业务冲突 | slug 重复、资源仍被引用、功能未配置或未启用 |
| `413` | 请求体过大 | 上传内容超过服务端限制 |
| `500` | 服务端错误 | 未处理异常、文件读写失败等 |

Bean Validation 失败时，错误消息通常包含字段名：

```json
{
  "code": 400,
  "message": "title: 不能为空; slug: 不能为空",
  "data": null
}
```

### 2.5 Request ID

客户端可以传入：

```http
X-Request-Id: perf-login-0001
```

要求长度不超过 64 个字符。未传、为空或过长时，服务端会生成 UUID。服务端同时通过响应头和响应 JSON 返回该值。

### 2.6 分页结构

分页请求通常使用：

| 参数 | 类型 | 默认值 | 规则 |
|---|---|---:|---|
| `page` | long | `1` | 小于 1 时按 1 处理 |
| `size` | long | `10` | 最小 1，最大 100 |

分页响应中的 `data`：

```json
{
  "total": 25,
  "page": 1,
  "size": 10,
  "records": []
}
```

### 2.7 常用枚举

| 枚举 | 可用值 |
|---|---|
| 文章状态 `PostStatus` | `DRAFT`、`PUBLISHED`、`OFFLINE` |
| 文章内容类型 `PostContentType` | `MARKDOWN`、`PDF` |
| 项目状态 `ProjectStatus` | `DEVELOPING`、`ONLINE`、`MAINTAINING`、`ARCHIVED` |
| 评论目标 `CommentTargetType` | `POST`、`PROJECT`、`MESSAGE` |
| 评论状态 `CommentStatus` | `PENDING`、`VISIBLE`、`HIDDEN`、`DELETED` |
| 文件业务类型 `FileBizType` | `POST`、`PROJECT`、`RESUME`、`SITE`、`OTHER` |
| 文件状态 `FileStatus` | `ACTIVE`、`DELETED` |
| 配置类型 `ConfigValueType` | `STRING`、`NUMBER`、`BOOLEAN`、`JSON` |
| 用户角色 `UserRole` | `ADMIN`、`USER` |
| 用户状态 `UserStatus` | `ACTIVE`、`DISABLED` |

枚举请求值建议始终使用大写。

## 3. 全量接口索引

### 3.1 认证与公开接口

| 编号 | 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|---|
| AUTH-01 | POST | `/api/auth/admin/login` | 公开 | 管理员登录 |
| AUTH-02 | POST | `/api/auth/refresh` | 公开 | 刷新并轮换令牌 |
| AUTH-03 | POST | `/api/auth/logout` | 公开 | 撤销 Refresh Token |
| AUTH-04 | GET | `/api/auth/me` | 已登录 | 获取当前用户 |
| AUTH-05 | GET | `/api/auth/github/authorize` | 公开 | 获取 GitHub 授权地址 |
| AUTH-06 | GET | `/api/auth/github/callback` | 未启用 | GitHub OAuth 回调 |
| DICT-01 | GET | `/api/categories` | 公开 | 获取启用分类 |
| DICT-02 | GET | `/api/tags` | 公开 | 获取标签 |
| POST-01 | GET | `/api/posts` | 公开 | 公开文章分页 |
| POST-02 | GET | `/api/posts/{slug}` | 公开 | 公开文章详情 |
| PROJECT-01 | GET | `/api/projects` | 公开 | 公开项目分页 |
| PROJECT-02 | GET | `/api/projects/{slug}` | 公开 | 公开项目详情 |
| COMMENT-01 | GET | `/api/comments` | 公开 | 获取公开评论树 |
| COMMENT-02 | POST | `/api/comments` | 可选登录 | 提交评论或留言 |
| SITE-01 | GET | `/api/site/profile` | 公开 | 获取公开站点配置 |
| SITE-02 | GET | `/api/resume` | 公开 | 获取在线简历 |

### 3.2 管理员接口

以下接口全部需要 `ADMIN` Access Token。

| 编号 | 方法 | 路径 | 说明 |
|---|---|---|---|
| ADMIN-01 | GET | `/api/admin/dashboard` | 后台仪表盘 |
| APOST-01 | GET | `/api/admin/posts` | 后台文章分页 |
| APOST-02 | GET | `/api/admin/posts/{id}` | 后台文章详情 |
| APOST-03 | POST | `/api/admin/posts` | 创建文章 |
| APOST-04 | PUT | `/api/admin/posts/{id}` | 更新文章 |
| APOST-05 | DELETE | `/api/admin/posts/{id}` | 逻辑删除文章 |
| APOST-06 | PUT | `/api/admin/posts/{id}/publish` | 发布文章 |
| APOST-07 | PUT | `/api/admin/posts/{id}/offline` | 下架文章 |
| APOST-08 | PUT | `/api/admin/posts/batch-publish` | 批量发布 |
| APOST-09 | POST | `/api/admin/posts/import-md` | 导入 Markdown 正文 |
| APOST-10 | POST | `/api/admin/posts/import-notes-zip` | 批量导入 ZIP 笔记库 |
| APROJECT-01 | GET | `/api/admin/projects` | 后台项目分页 |
| APROJECT-02 | GET | `/api/admin/projects/{id}` | 后台项目详情 |
| APROJECT-03 | POST | `/api/admin/projects` | 创建项目 |
| APROJECT-04 | PUT | `/api/admin/projects/{id}` | 更新项目 |
| APROJECT-05 | DELETE | `/api/admin/projects/{id}` | 逻辑删除项目 |
| APROJECT-06 | POST | `/api/admin/projects/{id}/images` | 添加项目图片 |
| APROJECT-07 | PUT | `/api/admin/projects/{id}/images/sort` | 调整项目图片排序 |
| APROJECT-08 | DELETE | `/api/admin/projects/{id}/images/{imageId}` | 删除项目图片关联 |
| ACATEGORY-01 | GET | `/api/admin/categories` | 获取全部未删除分类 |
| ACATEGORY-02 | POST | `/api/admin/categories` | 创建分类 |
| ACATEGORY-03 | PUT | `/api/admin/categories/{id}` | 更新分类 |
| ACATEGORY-04 | DELETE | `/api/admin/categories/{id}` | 删除分类 |
| ACATEGORY-05 | PUT | `/api/admin/categories/{id}/enable` | 启用分类 |
| ACATEGORY-06 | PUT | `/api/admin/categories/{id}/disable` | 禁用分类 |
| ATAG-01 | GET | `/api/admin/tags` | 获取全部未删除标签 |
| ATAG-02 | POST | `/api/admin/tags` | 创建标签 |
| ATAG-03 | PUT | `/api/admin/tags/{id}` | 更新标签 |
| ATAG-04 | DELETE | `/api/admin/tags/{id}` | 删除标签 |
| ATAG-05 | POST | `/api/admin/tags/merge` | 合并标签 |
| ACOMMENT-01 | GET | `/api/admin/comments` | 后台评论分页 |
| ACOMMENT-02 | PUT | `/api/admin/comments/{id}/visible` | 设为可见 |
| ACOMMENT-03 | PUT | `/api/admin/comments/{id}/hide` | 隐藏评论 |
| ACOMMENT-04 | PUT | `/api/admin/comments/{id}/delete` | 标记删除 |
| ACOMMENT-05 | DELETE | `/api/admin/comments/{id}` | 标记删除 |
| AFILE-01 | POST | `/api/admin/files/upload` | 上传文件 |
| AFILE-02 | GET | `/api/admin/files` | 文件分页 |
| AFILE-03 | DELETE | `/api/admin/files/{id}` | 删除文件 |
| ARESUME-01 | PUT | `/api/admin/resume` | 更新在线简历 |
| ARESUME-02 | POST | `/api/admin/resume/pdf` | 上传 PDF 简历 |
| ASETTING-01 | GET | `/api/admin/settings` | 获取全部站点配置 |
| ASETTING-02 | PUT | `/api/admin/settings` | 批量保存站点配置 |
| AUSER-01 | GET | `/api/admin/users` | 用户分页 |
| AUSER-02 | GET | `/api/admin/users/{id}` | 用户详情 |
| AUSER-03 | PUT | `/api/admin/users/password` | 修改当前管理员密码 |
| AUSER-04 | PUT | `/api/admin/users/{id}/disable` | 禁用用户 |
| AUSER-05 | PUT | `/api/admin/users/{id}/enable` | 启用用户 |

## 4. 认证接口

### AUTH-01 管理员登录

```http
POST /api/auth/admin/login
Content-Type: application/json
```

请求体：

| 字段 | 类型 | 必填 | 校验 |
|---|---|---|---|
| `username` | string | 是 | 不能为空 |
| `password` | string | 是 | 不能为空 |

```json
{
  "username": "admin",
  "password": "仅填写测试环境密码"
}
```

成功条件：

- 用户名存在；
- 用户角色为 `ADMIN`；
- 用户状态为 `ACTIVE`；
- 用户未被逻辑删除；
- BCrypt 密码校验通过；
- 已配置 `MLK_JWT_SECRET`。

成功响应 `data`：

```json
{
  "accessToken": "eyJ...",
  "refreshToken": "JLU...",
  "accessTokenExpiresIn": 1800,
  "user": {
    "id": 1,
    "username": "admin",
    "nickname": "管理员",
    "email": "admin@example.com",
    "avatarUrl": null,
    "role": "ADMIN"
  }
}
```

每次成功登录都会更新最后登录时间、插入一条 Refresh Token 记录并插入一条登录操作日志。

常见错误：

- `400`：用户名或密码为空；
- `401`：用户名或密码错误；
- `409`：JWT Secret 未配置。

### AUTH-02 刷新并轮换令牌

```http
POST /api/auth/refresh
Content-Type: application/json
```

请求体：

```json
{
  "refreshToken": "<登录接口返回的 refreshToken>"
}
```

处理过程：

1. 计算 Refresh Token 的 SHA-256 摘要；
2. 查找未撤销且未过期的令牌；
3. 撤销当前 Refresh Token；
4. 检查用户仍为 `ACTIVE`；
5. 返回新的 Access Token 和新的 Refresh Token。

成功响应与 AUTH-01 的 `data` 相同。

常见错误：

- `400`：`refreshToken` 为空；
- `401`：令牌不存在、已撤销、已过期或用户不可用。

同一个 Refresh Token 成功使用后不能再次使用。

### AUTH-03 退出登录

```http
POST /api/auth/logout
Content-Type: application/json
```

请求体：

```json
{
  "refreshToken": "<需要撤销的 refreshToken>"
}
```

成功响应：

```json
{
  "code": 200,
  "message": "success",
  "data": null
}
```

说明：

- 接口本身不要求 Access Token；
- 找不到对应令牌时仍返回成功；
- 退出只撤销指定 Refresh Token；
- 已签发的 Access Token 不会立即进入黑名单，仍可能使用到过期。

### AUTH-04 获取当前用户

```http
GET /api/auth/me
Authorization: Bearer <accessToken>
```

成功响应 `data`：

```json
{
  "id": 1,
  "username": "admin",
  "nickname": "管理员",
  "email": "admin@example.com",
  "avatarUrl": null,
  "role": "ADMIN"
}
```

该接口适合验证 Token 是否有效，也适合在性能测试中单独测量“JWT 解析 + 用户查询”的鉴权开销。

### AUTH-05 获取 GitHub OAuth 授权地址

```http
GET /api/auth/github/authorize
```

成功响应 `data` 是 GitHub 授权 URL 字符串。

前置配置：

- `MLK_GITHUB_CLIENT_ID`
- `MLK_GITHUB_CLIENT_SECRET`
- `MLK_GITHUB_REDIRECT_URI`

未完整配置时返回 `409 GitHub OAuth 未配置`。

### AUTH-06 GitHub OAuth 回调

```http
GET /api/auth/github/callback?code=<github-code>
```

当前状态：**未启用**。

即使 GitHub OAuth 配置完整，当前仍固定返回：

```json
{
  "code": 409,
  "message": "GitHub OAuth 回调交换尚未启用",
  "data": null
}
```

不要把该接口加入正常成功率测试。

## 5. 公开分类与标签接口

### DICT-01 获取启用分类

```http
GET /api/categories
```

无请求参数。只返回：

- `enabled = 1`；
- `deletedAt = null`。

排序规则：`sortOrder` 升序，再按 `createdAt` 降序。

成功响应 `data` 类型：`Category[]`。

### DICT-02 获取标签

```http
GET /api/tags
```

无请求参数。只返回未删除标签，按创建时间降序。

成功响应 `data` 类型：`Tag[]`。

## 6. 公开文章接口

### POST-01 公开文章分页

```http
GET /api/posts
```

查询参数：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---:|---|
| `page` | long | 否 | `1` | 页码 |
| `size` | long | 否 | `10` | 每页数量，最大 100 |
| `categoryId` | long | 否 | - | 分类 ID |
| `categorySlug` | string | 否 | - | 分类 slug |
| `tagId` | long | 否 | - | 标签 ID |
| `tagSlug` | string | 否 | - | 标签 slug |
| `keyword` | string | 否 | - | 搜索标题、摘要和正文 |

示例：

```http
GET /api/posts?page=1&size=10&categorySlug=java&keyword=spring
```

规则：

- 只返回状态为 `PUBLISHED` 且未删除的文章；
- `categoryId` 与 `categorySlug` 同时传入时优先使用 `categoryId`；
- `tagId` 与 `tagSlug` 同时传入时优先使用 `tagId`；
- 分类或标签 slug 不存在时返回空分页；
- 按 `publishedAt` 降序。

响应 `records` 元素：

```json
{
  "id": 1,
  "title": "Spring Boot 学习记录",
  "slug": "spring-boot-notes",
  "summary": "文章摘要",
  "coverUrl": "/uploads/2026/07/26/example.webp",
  "category": {
    "id": 1,
    "name": "Java",
    "slug": "java",
    "description": "Java 技术文章"
  },
  "tags": [
    {
      "id": 1,
      "name": "Spring Boot",
      "slug": "spring-boot"
    }
  ],
  "viewCount": 10,
  "publishedAt": "2026-07-26 10:00:00"
}
```

### POST-02 公开文章详情

```http
GET /api/posts/{slug}
```

路径参数：

| 参数 | 类型 | 说明 |
|---|---|---|
| `slug` | string | 文章唯一 URL 标识 |

成功响应 `data`：

```json
{
  "id": 1,
  "title": "Spring Boot 学习记录",
  "slug": "spring-boot-notes",
  "summary": "文章摘要",
  "content": "# Markdown 正文",
  "contentType": "MARKDOWN",
  "pdfUrl": null,
  "coverUrl": null,
  "category": {},
  "tags": [],
  "viewCount": 11,
  "seoTitle": null,
  "seoDescription": null,
  "publishedAt": "2026-07-26 10:00:00",
  "previous": {
    "id": 2,
    "title": "上一篇",
    "slug": "previous-post"
  },
  "next": null
}
```

规则：

- 只允许读取已发布且未删除文章；
- 每次成功访问都会执行 `view_count = view_count + 1`；
- `previous` 和 `next` 可能为 `null`；
- 文章不存在时返回 `404 文章不存在`。

## 7. 公开项目接口

### PROJECT-01 公开项目分页

```http
GET /api/projects
```

查询参数：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---:|---|
| `page` | long | 否 | `1` | 页码 |
| `size` | long | 否 | `10` | 每页数量，最大 100 |
| `status` | string | 否 | - | 项目状态，不区分输入大小写 |
| `featured` | boolean | 否 | - | 是否精选 |

示例：

```http
GET /api/projects?page=1&size=10&status=ONLINE&featured=true
```

排序规则：

1. 精选项目优先；
2. `sortOrder` 升序；
3. `createdAt` 降序。

无效状态返回 `400 项目状态无效`。

响应 `records` 元素类型：`ProjectListVO`，字段见第 20 章。

### PROJECT-02 公开项目详情

```http
GET /api/projects/{slug}
```

返回项目基本信息、Markdown 正文、技术栈、封面 URL 和有序图片列表。

项目图片结构：

```json
{
  "id": 1,
  "imageType": "SCREENSHOT",
  "url": "/uploads/2026/07/26/project.webp",
  "caption": "项目首页",
  "altText": "项目首页截图",
  "sortOrder": 0
}
```

项目不存在时返回 `404 项目不存在`。

## 8. 公开评论接口

### COMMENT-01 获取公开评论树

```http
GET /api/comments?targetType=POST&targetId=1
```

查询参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `targetType` | string | 是 | `POST`、`PROJECT` 或 `MESSAGE` |
| `targetId` | long | 是 | 目标 ID；留言板使用 `0` |

只返回状态为 `VISIBLE` 且未删除的评论，并按创建时间升序组装为树。

成功响应 `data`：

```json
[
  {
    "id": 1,
    "parentId": null,
    "nickname": "访客",
    "avatarUrl": null,
    "content": "评论内容",
    "createdAt": "2026-07-26 18:00:00",
    "children": [
      {
        "id": 2,
        "parentId": 1,
        "nickname": "管理员",
        "avatarUrl": null,
        "content": "回复内容",
        "createdAt": "2026-07-26 18:05:00",
        "children": []
      }
    ]
  }
]
```

### COMMENT-02 提交评论或留言

```http
POST /api/comments
Content-Type: application/json
Authorization: Bearer <accessToken>
```

`Authorization` 为可选。

请求体：

| 字段 | 类型 | 必填 | 校验与说明 |
|---|---|---|---|
| `targetType` | enum | 是 | `POST`、`PROJECT`、`MESSAGE` |
| `targetId` | long | 是 | `MESSAGE` 必须为 `0` |
| `parentId` | long | 否 | 回复的父评论 ID |
| `guestNickname` | string | 游客必填 | 最大 64 字符 |
| `guestEmail` | string | 否 | 最大 128 字符 |
| `content` | string | 是 | 非空，最大 2000 字符 |

游客留言示例：

```json
{
  "targetType": "MESSAGE",
  "targetId": 0,
  "parentId": null,
  "guestNickname": "学习者",
  "guestEmail": "learner@example.com",
  "content": "网站做得很好。"
}
```

登录用户评论示例：

```json
{
  "targetType": "POST",
  "targetId": 1,
  "parentId": null,
  "content": "这篇文章对我很有帮助。"
}
```

业务规则：

- 登录用户的昵称、头像和用户 ID 来自 Token 对应用户；
- 登录用户提交的游客昵称和邮箱会被忽略；
- 评论文章必须存在、已发布且未删除；
- 评论项目必须存在且未删除；
- 子评论必须与父评论的目标类型和目标 ID 一致；
- 评论内容会进行基础 HTML 字符转义；
- 默认评论状态由 `MLK_COMMENT_DEFAULT_STATUS` 决定，默认 `PENDING`；
- 若启用验证码但未接入服务商，接口返回 `409`。

新建接口返回 `CommentVO`，但状态为 `PENDING` 时不会立即出现在 COMMENT-01 中。

## 9. 站点与简历公开接口

### SITE-01 获取公开站点配置

```http
GET /api/site/profile
```

只返回 `publicFlag = 1` 的配置。

成功响应：

```json
{
  "settings": {
    "siteName": "MLK Space",
    "tagline": "个人技术空间",
    "github": "https://github.com/example",
    "showStats": true
  }
}
```

配置值会按 `STRING`、`NUMBER`、`BOOLEAN`、`JSON` 转换为对应 JSON 类型。转换失败时返回原始字符串。

### SITE-02 获取在线简历

```http
GET /api/resume
```

成功响应 `data`：

```json
{
  "content": "# 在线简历",
  "pdfUrl": "/uploads/2026/07/26/resume.pdf",
  "updatedAt": "2026-07-26 18:00:00"
}
```

数据库尚无简历记录时返回：

```json
{
  "content": "",
  "pdfUrl": null,
  "updatedAt": null
}
```

## 10. 管理员通用调用方式

先调用 AUTH-01，再将 Access Token 写入请求头：

```http
Authorization: Bearer <accessToken>
```

所有 `/api/admin/**` 接口要求角色为 `ADMIN`。

Access Token 解析后，服务端还会根据用户 ID 查询一次 `sys_user`，检查用户是否仍为 `ACTIVE` 且未删除。

## 11. 管理员仪表盘

### ADMIN-01 获取后台仪表盘

```http
GET /api/admin/dashboard
Authorization: Bearer <accessToken>
```

成功响应 `data`：

```json
{
  "postCount": 10,
  "projectCount": 4,
  "commentCount": 20,
  "userCount": 3,
  "recentComments": [],
  "recentPosts": [],
  "recentProjects": []
}
```

说明：

- 四个数量统计只排除逻辑删除记录；
- 最近评论、文章和项目各最多返回 10 条；
- 最近文章和项目的 `content` 会被置为 `null`，避免仪表盘响应过大。

## 12. 管理员文章接口

### APOST-01 后台文章分页

```http
GET /api/admin/posts?page=1&size=10&status=DRAFT&categoryId=1&keyword=Spring
```

查询参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `page` | long | 否 | 默认 1 |
| `size` | long | 否 | 默认 10，最大 100 |
| `status` | string | 否 | 按文章状态精确筛选 |
| `categoryId` | long | 否 | 分类 ID |
| `keyword` | string | 否 | 搜索标题和摘要 |

响应 `records` 为 `Post[]`，列表中的 `content` 固定为 `null`。

### APOST-02 后台文章详情

```http
GET /api/admin/posts/{id}
```

成功响应 `data`：

```json
{
  "post": {
    "id": 1,
    "title": "文章标题",
    "content": "# 完整正文"
  },
  "tagIds": [1, 2],
  "pdfUrl": null
}
```

文章不存在时返回 `404 文章不存在`。

### APOST-03 创建文章

```http
POST /api/admin/posts
Content-Type: application/json
```

Markdown 文章示例：

```json
{
  "title": "性能测试学习记录",
  "slug": "performance-testing-notes",
  "categoryId": 1,
  "summary": "使用个人网站学习性能测试。",
  "content": "# 性能测试\n\n正文内容",
  "contentType": "MARKDOWN",
  "pdfFileId": null,
  "coverFileId": null,
  "status": "DRAFT",
  "seoTitle": "性能测试学习记录",
  "seoDescription": "性能测试学习笔记",
  "tagIds": [1, 2]
}
```

字段：

| 字段 | 类型 | 必填 | 校验与默认值 |
|---|---|---|---|
| `title` | string | 是 | 最大 200 |
| `slug` | string | 是 | 最大 200，全局唯一 |
| `categoryId` | long | 是 | 分类必须存在且未删除 |
| `summary` | string | 否 | 最大 500；为空时尝试从正文生成 |
| `content` | string | 条件必填 | `MARKDOWN` 时必须有正文 |
| `contentType` | enum | 否 | 默认 `MARKDOWN` |
| `pdfFileId` | long | 条件必填 | `PDF` 时必须引用有效 PDF 文件 |
| `coverFileId` | long | 否 | 封面文件 ID |
| `status` | enum | 否 | 默认 `DRAFT` |
| `seoTitle` | string | 否 | 最大 200 |
| `seoDescription` | string | 否 | 最大 500 |
| `tagIds` | long[] | 否 | 标签必须存在且未删除，重复值会去重 |

PDF 文章请求示例：

```json
{
  "title": "PDF 学习资料",
  "slug": "pdf-study-material",
  "categoryId": 1,
  "summary": "PDF 资料摘要不能为空。",
  "content": "",
  "contentType": "PDF",
  "pdfFileId": 10,
  "status": "DRAFT",
  "tagIds": []
}
```

常见错误：

- `400 分类不存在`；
- `400 部分标签不存在`；
- `400 Markdown 正文不能为空`；
- `400 请上传有效的 PDF 正文文件`；
- `409 文章 slug 已存在`。

### APOST-04 更新文章

```http
PUT /api/admin/posts/{id}
Content-Type: application/json
```

请求体结构和校验与 APOST-03 相同。当前更新属于完整字段更新，客户端应提交完整文章表单，不应只提交单个变化字段。

### APOST-05 逻辑删除文章

```http
DELETE /api/admin/posts/{id}
```

将 `deletedAt` 设置为当前时间，不会直接物理删除数据库记录。

成功时 `data = null`。

### APOST-06 发布文章

```http
PUT /api/admin/posts/{id}/publish
```

将状态改为 `PUBLISHED`，并把 `publishedAt` 设置为当前时间。

成功响应 `data` 类型：`Post`。

### APOST-07 下架文章

```http
PUT /api/admin/posts/{id}/offline
```

将状态改为 `OFFLINE`。成功响应 `data` 类型：`Post`。

### APOST-08 批量发布文章

```http
PUT /api/admin/posts/batch-publish
Content-Type: application/json
```

请求体：

```json
{
  "postIds": [1, 2, 3]
}
```

规则：

- `postIds` 不能为空；
- 单次最多 5000 个 ID；
- 重复 ID 会去重；
- 任意文章不存在或已删除时，整个请求失败；
- 所有文章使用同一个 `publishedAt`。

成功响应：

```json
{
  "published": 3
}
```

### APOST-09 导入 Markdown 正文

```http
POST /api/admin/posts/import-md
Content-Type: multipart/form-data
```

表单字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `postId` | long | 是 | 已存在文章 ID |
| `file` | file | 条件必填 | UTF-8 Markdown 文件 |
| `text` | string | 条件必填 | 直接提交 Markdown 文本 |

`file` 和 `text` 至少提供一个；同时提供时优先使用 `file`。

如果原文章摘要为空，服务端会从 Markdown 正文生成摘要。

PowerShell 示例：

```powershell
curl.exe -X POST "http://127.0.0.1:8080/api/admin/posts/import-md" `
  -H "Authorization: Bearer $env:MLK_TEST_ACCESS_TOKEN" `
  -F "postId=1" `
  -F "file=@D:\notes\performance.md;type=text/markdown"
```

### APOST-10 批量导入 ZIP 笔记库

```http
POST /api/admin/posts/import-notes-zip
Content-Type: multipart/form-data
```

表单字段：

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---:|---|
| `file` | file | 是 | - | ZIP 笔记包 |
| `categoryId` | long | 是 | - | 启用且未删除的默认分类 |
| `createTags` | boolean | 否 | `true` | 是否根据 Front Matter 创建标签 |

限制：

- ZIP 最大 200MB；
- 解压后总大小最大 1GB；
- 最多 20000 个有效文件；
- 单个 Markdown 最大 5MB；
- 单个图片或 PDF 最大 30MB；
- 资源扩展名支持 `png`、`jpg`、`jpeg`、`gif`、`webp`、`pdf`；
- 自动忽略 `__MACOSX`、`.git`、`.obsidian` 和隐藏文件；
- 导入文章统一保存为 `DRAFT`。

成功响应：

```json
{
  "importedPosts": 2,
  "uploadedAssets": 3,
  "skippedFiles": 1,
  "notes": [
    {
      "id": 10,
      "title": "JMeter 学习",
      "slug": "jmeter-study",
      "sourcePath": "性能测试/JMeter.md"
    }
  ],
  "warnings": []
}
```

## 13. 管理员项目接口

### APROJECT-01 后台项目分页

```http
GET /api/admin/projects?page=1&size=10
```

返回所有未删除项目，按 `updatedAt` 降序。列表中的 `content` 为 `null`。

### APROJECT-02 后台项目详情

```http
GET /api/admin/projects/{id}
```

成功响应：

```json
{
  "project": {},
  "images": []
}
```

`images` 按 `sortOrder` 升序。

### APROJECT-03 创建项目

```http
POST /api/admin/projects
Content-Type: application/json
```

请求示例：

```json
{
  "name": "MLK Space",
  "slug": "mlk-space",
  "summary": "个人技术空间项目",
  "content": "# 项目详情",
  "status": "DEVELOPING",
  "techStack": "[\"Spring Boot\",\"Vue 3\",\"MySQL\"]",
  "coverFileId": null,
  "demoUrl": "https://example.com",
  "repoUrl": "https://github.com/example/mlk-space",
  "featured": true,
  "sortOrder": 0,
  "seoTitle": "MLK Space",
  "seoDescription": "个人技术空间"
}
```

重要：当前接口中的 `techStack` 类型是字符串，字符串内容必须是合法 JSON 数组。不能直接传：

```json
{
  "techStack": ["Spring Boot", "Vue 3"]
}
```

字段规则：

| 字段 | 必填 | 规则 |
|---|---|---|
| `name` | 是 | 最大 120 |
| `slug` | 是 | 最大 160，全局唯一 |
| `summary` | 是 | 最大 500 |
| `content` | 是 | 非空 |
| `status` | 否 | 默认 `DEVELOPING` |
| `techStack` | 是 | 合法 JSON 数组字符串 |
| `coverFileId` | 否 | 文件 ID |
| `demoUrl` | 否 | 最大 500 |
| `repoUrl` | 否 | 最大 500 |
| `featured` | 否 | 默认 `false` |
| `sortOrder` | 否 | 默认 `0` |
| `seoTitle` | 否 | 最大 200 |
| `seoDescription` | 否 | 最大 500 |

### APROJECT-04 更新项目

```http
PUT /api/admin/projects/{id}
Content-Type: application/json
```

请求结构和校验与 APROJECT-03 相同。当前属于完整字段更新。

### APROJECT-05 逻辑删除项目

```http
DELETE /api/admin/projects/{id}
```

设置 `deletedAt`，不会直接物理删除项目记录。

### APROJECT-06 添加项目图片

```http
POST /api/admin/projects/{id}/images
Content-Type: application/json
```

请求体：

```json
{
  "fileId": 20,
  "imageType": "SCREENSHOT",
  "caption": "系统首页",
  "altText": "MLK Space 系统首页截图",
  "sortOrder": 0
}
```

规则：

- 项目必须存在；
- 文件必须存在、状态为 `ACTIVE` 且 MIME 类型以 `image/` 开头；
- `imageType` 会转成大写；
- 设计文档建议使用 `SCREENSHOT`、`ARCHITECTURE`、`DATABASE`、`OTHER`，但当前代码没有强制枚举校验；
- `caption` 和 `altText` 最大 255；
- `sortOrder` 默认 0。

### APROJECT-07 调整项目图片排序

```http
PUT /api/admin/projects/{id}/images/sort
Content-Type: application/json
```

请求体：

```json
{
  "items": [
    {
      "imageId": 10,
      "sortOrder": 0
    },
    {
      "imageId": 11,
      "sortOrder": 1
    }
  ]
}
```

`items` 不能为空。`sortOrder` 为空时按 0 处理。

成功时 `data = null`。

### APROJECT-08 删除项目图片关联

```http
DELETE /api/admin/projects/{id}/images/{imageId}
```

只删除 `project_image` 关联记录，不删除对应的文件资源。

关联不存在时返回 `404 项目图片不存在`。

## 14. 管理员分类接口

### ACATEGORY-01 获取全部分类

```http
GET /api/admin/categories
```

返回全部未删除分类，包括已禁用分类。

### ACATEGORY-02 创建分类

```http
POST /api/admin/categories
Content-Type: application/json
```

请求体：

```json
{
  "name": "性能测试",
  "slug": "performance-testing",
  "description": "性能测试学习文章",
  "sortOrder": 0,
  "enabled": true
}
```

字段规则：

- `name` 必填，最大 64；
- `slug` 必填，最大 100；
- `description` 最大 255；
- `sortOrder` 默认 0；
- `enabled` 默认 true；
- 名称或 slug 与未删除分类重复时返回 `409`。

### ACATEGORY-03 更新分类

```http
PUT /api/admin/categories/{id}
Content-Type: application/json
```

请求结构与 ACATEGORY-02 相同。

### ACATEGORY-04 删除分类

```http
DELETE /api/admin/categories/{id}
```

规则：

- 分类不存在时返回 `404`；
- 仍被未删除文章引用时返回 `409 分类仍被文章引用，不能删除`；
- 成功时执行逻辑删除并同时禁用分类。

### ACATEGORY-05 启用分类

```http
PUT /api/admin/categories/{id}/enable
```

将 `enabled` 设置为 1，返回更新后的 `Category`。

### ACATEGORY-06 禁用分类

```http
PUT /api/admin/categories/{id}/disable
```

将 `enabled` 设置为 0，返回更新后的 `Category`。

## 15. 管理员标签接口

### ATAG-01 获取全部标签

```http
GET /api/admin/tags
```

返回全部未删除标签，按创建时间降序。

### ATAG-02 创建标签

```http
POST /api/admin/tags
Content-Type: application/json
```

```json
{
  "name": "JMeter",
  "slug": "jmeter"
}
```

`name` 最大 64，`slug` 最大 100。名称或 slug 重复时返回 `409`。

### ATAG-03 更新标签

```http
PUT /api/admin/tags/{id}
Content-Type: application/json
```

请求结构与 ATAG-02 相同。

### ATAG-04 删除标签

```http
DELETE /api/admin/tags/{id}
```

当前执行逻辑删除。成功时 `data = null`。

### ATAG-05 合并标签

```http
POST /api/admin/tags/merge
Content-Type: application/json
```

请求体：

```json
{
  "sourceTagId": 10,
  "targetTagId": 2
}
```

处理结果：

- 把源标签的文章关联迁移到目标标签；
- 已存在的目标关联不会重复插入；
- 删除源标签关联；
- 逻辑删除源标签。

源标签和目标标签相同时返回 `400 不能合并同一个标签`。

## 16. 管理员评论接口

### ACOMMENT-01 后台评论分页

```http
GET /api/admin/comments?page=1&size=10&status=PENDING&targetType=POST&keyword=测试
```

查询参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `page` | long | 否 | 默认 1 |
| `size` | long | 否 | 默认 10，最大 100 |
| `status` | string | 否 | 评论状态 |
| `targetType` | string | 否 | 评论目标类型 |
| `keyword` | string | 否 | 搜索评论正文 |

响应 `records` 为完整后台 `Comment` 数据，包括游客邮箱、审核字段、IP 摘要和 User-Agent，因此只能在管理员界面使用。

### ACOMMENT-02 设为可见

```http
PUT /api/admin/comments/{id}/visible
```

将状态设置为 `VISIBLE`，记录审核管理员和审核时间。

### ACOMMENT-03 隐藏评论

```http
PUT /api/admin/comments/{id}/hide
```

将状态设置为 `HIDDEN`。

### ACOMMENT-04 标记删除

```http
PUT /api/admin/comments/{id}/delete
```

将状态设置为 `DELETED`，同时设置 `deletedAt`。

### ACOMMENT-05 删除评论

```http
DELETE /api/admin/comments/{id}
```

当前行为与 ACOMMENT-04 相同，仍是逻辑删除，并返回更新后的 `Comment`。

## 17. 管理员文件接口

### AFILE-01 上传文件

```http
POST /api/admin/files/upload
Content-Type: multipart/form-data
```

表单字段：

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---:|---|
| `file` | file | 是 | - | 上传文件 |
| `bizType` | enum | 否 | `OTHER` | 文件业务类型 |

允许的扩展名与 MIME：

| 扩展名 | MIME |
|---|---|
| `jpg`、`jpeg` | `image/jpeg`、`image/jpg` |
| `png` | `image/png` |
| `gif` | `image/gif` |
| `webp` | `image/webp` |
| `pdf` | `application/pdf` |
| `md` | `text/markdown`、`text/plain`、`application/octet-stream` |

应用默认上传限制：

- 单文件最大 200MB；
- 整个请求最大 210MB。

成功响应：

```json
{
  "id": 20,
  "originName": "cover.webp",
  "publicUrl": "/uploads/2026/07/26/uuid.webp",
  "mimeType": "image/webp",
  "extension": "webp",
  "sizeBytes": 102400,
  "bizType": "POST",
  "status": "ACTIVE",
  "createdAt": "2026-07-26 18:00:00"
}
```

### AFILE-02 文件分页

```http
GET /api/admin/files?page=1&size=10
```

只返回未删除文件，按创建时间降序。

响应 `records` 为完整 `FileResource` 数据。

### AFILE-03 删除文件

```http
DELETE /api/admin/files/{id}
```

以下任一资源仍引用文件时返回 `409`：

- 文章封面；
- 文章 PDF 正文；
- 项目封面；
- 项目图片；
- 简历 PDF。

成功后：

- 数据库记录设置为 `DELETED` 并写入 `deletedAt`；
- 尝试删除磁盘文件；
- 磁盘删除失败时当前仍返回业务成功，但服务端会记录警告日志。

## 18. 管理员简历与配置接口

### ARESUME-01 更新在线简历

```http
PUT /api/admin/resume
Content-Type: application/json
```

请求体：

```json
{
  "content": "# 个人简历\n\nMarkdown 内容"
}
```

`content` 不能为 `null`，允许为空字符串。简历固定使用数据库 ID `1`。

成功响应 `data` 类型：`Resume`。

### ARESUME-02 上传 PDF 简历

```http
POST /api/admin/resume/pdf
Content-Type: multipart/form-data
```

表单字段：

| 字段 | 类型 | 必填 |
|---|---|---|
| `file` | file | 是 |

文件必须同时满足：

- 文件名以 `.pdf` 结尾；
- MIME 为 `application/pdf`。

上传成功后会更新简历记录中的 `pdfFileId`。

### ASETTING-01 获取全部站点配置

```http
GET /api/admin/settings
```

按 `configKey` 升序返回完整 `SiteConfig[]`，包括非公开配置。

### ASETTING-02 批量保存站点配置

```http
PUT /api/admin/settings
Content-Type: application/json
```

请求体：

```json
{
  "items": [
    {
      "key": "siteName",
      "value": "MLK Space",
      "valueType": "STRING",
      "description": "站点名称",
      "publicFlag": true
    },
    {
      "key": "showStats",
      "value": "true",
      "valueType": "BOOLEAN",
      "description": "是否显示统计信息",
      "publicFlag": true
    }
  ]
}
```

字段规则：

| 字段 | 必填 | 说明 |
|---|---|---|
| `items` | 是 | 非空数组 |
| `key` | 是 | 最大 100 |
| `value` | 否 | 数据库存储为字符串 |
| `valueType` | 否 | 默认 `STRING` |
| `description` | 否 | 最大 255 |
| `publicFlag` | 否 | 默认 false |

安全规则：

配置键包含以下敏感词时拒绝保存：

```text
password, passwd, secret, token, jwt, oauth,
client_secret, database, db_password
```

`NUMBER`、`BOOLEAN`、`JSON` 的 `value` 必须能按声明类型解析，否则返回 `400 配置值与类型不匹配`。

## 19. 管理员用户接口

### AUSER-01 用户分页

```http
GET /api/admin/users?page=1&size=10
```

返回未删除用户，按创建时间降序。响应中的 `passwordHash` 会被服务端设置为 `null`。

### AUSER-02 用户详情

```http
GET /api/admin/users/{id}
```

成功响应 `data` 类型：`SysUser`，其中 `passwordHash = null`。

用户不存在时返回 `404 用户不存在`。

### AUSER-03 修改当前管理员密码

```http
PUT /api/admin/users/password
Content-Type: application/json
```

请求体：

```json
{
  "oldPassword": "当前密码",
  "newPassword": "新的强密码",
  "confirmPassword": "新的强密码"
}
```

规则：

- 三个字段均不能为空；
- 新密码长度为 8～72；
- 两次新密码必须一致；
- 新密码不能与原密码相同；
- 原密码必须校验通过；
- 成功后撤销当前用户的全部未撤销 Refresh Token。

成功时 `data = null`。

注意：当前 Access Token 不会因修改密码立即失效，仍可使用到默认 30 分钟过期。

### AUSER-04 禁用用户

```http
PUT /api/admin/users/{id}/disable
```

将用户状态设置为 `DISABLED`，同时撤销该用户全部未撤销 Refresh Token。

由于后台请求每次都会查询用户状态，已禁用用户的现有 Access Token 随后也不能通过后台鉴权。

### AUSER-05 启用用户

```http
PUT /api/admin/users/{id}/enable
```

将用户状态设置为 `ACTIVE`。不会恢复之前已撤销的 Refresh Token。

## 20. 响应数据模型

以下字段名均为 JSON camelCase。

### 20.1 Category

| 字段 | 类型 |
|---|---|
| `id` | long |
| `name` | string |
| `slug` | string |
| `description` | string/null |
| `sortOrder` | integer |
| `enabled` | integer，`1` 或 `0` |
| `createdAt` | datetime |
| `updatedAt` | datetime |
| `deletedAt` | datetime/null |

### 20.2 Tag

| 字段 | 类型 |
|---|---|
| `id` | long |
| `name` | string |
| `slug` | string |
| `createdAt` | datetime |
| `updatedAt` | datetime |
| `deletedAt` | datetime/null |

### 20.3 Post

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | long | 主键 |
| `categoryId` | long | 分类 ID |
| `title` | string | 标题 |
| `slug` | string | 唯一 URL 标识 |
| `summary` | string | 摘要 |
| `content` | string/null | Markdown；列表接口可能固定为 null |
| `contentType` | string | `MARKDOWN` 或 `PDF` |
| `pdfFileId` | long/null | PDF 正文文件 ID |
| `coverFileId` | long/null | 封面文件 ID |
| `status` | string | 文章状态 |
| `viewCount` | long | 阅读量 |
| `seoTitle` | string/null | SEO 标题 |
| `seoDescription` | string/null | SEO 描述 |
| `publishedAt` | datetime/null | 发布时间 |
| `createdBy` | long | 创建管理员 |
| `updatedBy` | long | 更新管理员 |
| `createdAt` | datetime | 创建时间 |
| `updatedAt` | datetime | 更新时间 |
| `deletedAt` | datetime/null | 逻辑删除时间 |

### 20.4 Project

| 字段 | 类型 |
|---|---|
| `id` | long |
| `name` | string |
| `slug` | string |
| `summary` | string |
| `content` | string/null |
| `status` | string |
| `techStack` | JSON array/object 或 JSON 字符串，取决于映射结果 |
| `coverFileId` | long/null |
| `demoUrl` | string/null |
| `repoUrl` | string/null |
| `featured` | integer，`1` 或 `0` |
| `sortOrder` | integer |
| `seoTitle` | string/null |
| `seoDescription` | string/null |
| `createdBy` | long |
| `updatedBy` | long |
| `createdAt` | datetime |
| `updatedAt` | datetime |
| `deletedAt` | datetime/null |

### 20.5 ProjectImage

| 字段 | 类型 |
|---|---|
| `id` | long |
| `projectId` | long |
| `fileId` | long |
| `imageType` | string |
| `caption` | string/null |
| `altText` | string/null |
| `sortOrder` | integer |
| `createdAt` | datetime |

### 20.6 Comment（后台模型）

| 字段 | 类型 |
|---|---|
| `id` | long |
| `targetType` | string |
| `targetId` | long |
| `parentId` | long/null |
| `userId` | long/null |
| `guestNickname` | string/null |
| `guestEmail` | string/null |
| `content` | string |
| `status` | string |
| `ipHash` | string/null |
| `userAgent` | string/null |
| `reviewedBy` | long/null |
| `reviewedAt` | datetime/null |
| `createdAt` | datetime |
| `updatedAt` | datetime |
| `deletedAt` | datetime/null |

公开评论接口使用 `CommentVO`，不会返回游客邮箱、IP 摘要和审核信息。

### 20.7 FileResource

| 字段 | 类型 |
|---|---|
| `id` | long |
| `originName` | string |
| `storedName` | string |
| `storagePath` | string |
| `publicUrl` | string |
| `mimeType` | string |
| `extension` | string |
| `sizeBytes` | long |
| `sha256` | string/null |
| `bizType` | string |
| `status` | string |
| `uploadedBy` | long |
| `createdAt` | datetime |
| `deletedAt` | datetime/null |

### 20.8 Resume

| 字段 | 类型 |
|---|---|
| `id` | integer，固定为 1 |
| `content` | string |
| `pdfFileId` | long/null |
| `updatedBy` | long |
| `updatedAt` | datetime |

### 20.9 SiteConfig

| 字段 | 类型 |
|---|---|
| `id` | long |
| `configKey` | string |
| `configValue` | string/null |
| `valueType` | string |
| `description` | string/null |
| `publicFlag` | integer，`1` 或 `0` |
| `updatedBy` | long |
| `updatedAt` | datetime |

### 20.10 SysUser

| 字段 | 类型 |
|---|---|
| `id` | long |
| `username` | string/null |
| `nickname` | string |
| `email` | string/null |
| `avatarUrl` | string/null |
| `githubId` | string/null |
| `passwordHash` | null，用户管理接口主动清空 |
| `role` | string |
| `status` | string |
| `lastLoginAt` | datetime/null |
| `createdAt` | datetime |
| `updatedAt` | datetime |
| `deletedAt` | datetime/null |

## 21. PowerShell 学习示例

### 21.1 调用公开接口

```powershell
$baseUrl = 'http://127.0.0.1:8080'
Invoke-RestMethod -Method Get -Uri "$baseUrl/api/posts?page=1&size=10"
```

### 21.2 登录并保存 Token

```powershell
$baseUrl = 'http://127.0.0.1:8080'
$loginBody = @{
    username = $env:MLK_PERF_ADMIN_USERNAME
    password = $env:MLK_PERF_ADMIN_PASSWORD
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod `
    -Method Post `
    -Uri "$baseUrl/api/auth/admin/login" `
    -ContentType 'application/json' `
    -Body $loginBody

$accessToken = $loginResponse.data.accessToken
$refreshToken = $loginResponse.data.refreshToken
```

不要把正式管理员密码直接写入 `.ps1`、JMeter `.jmx` 或 Git 仓库。

### 21.3 调用管理员接口

```powershell
$headers = @{
    Authorization = "Bearer $accessToken"
    'X-Request-Id' = 'learning-dashboard-0001'
}

Invoke-RestMethod `
    -Method Get `
    -Uri "$baseUrl/api/admin/dashboard" `
    -Headers $headers
```

### 21.4 刷新 Token

```powershell
$refreshBody = @{
    refreshToken = $refreshToken
} | ConvertTo-Json

$refreshResponse = Invoke-RestMethod `
    -Method Post `
    -Uri "$baseUrl/api/auth/refresh" `
    -ContentType 'application/json' `
    -Body $refreshBody

$accessToken = $refreshResponse.data.accessToken
$refreshToken = $refreshResponse.data.refreshToken
```

刷新成功后，旧 Refresh Token 已被撤销，必须保存新值。

## 22. Postman / Apifox 学习流程

建议建立以下环境变量：

```text
baseUrl=http://127.0.0.1:8080
accessToken=
refreshToken=
```

推荐调用顺序：

1. `GET {{baseUrl}}/api/categories`
2. `GET {{baseUrl}}/api/posts?page=1&size=10`
3. `POST {{baseUrl}}/api/auth/admin/login`
4. 保存 `data.accessToken` 和 `data.refreshToken`
5. `GET {{baseUrl}}/api/auth/me`
6. `GET {{baseUrl}}/api/admin/dashboard`
7. 创建一条 `DRAFT` 测试文章
8. 查询后台文章列表
9. 删除测试文章
10. 调用刷新与退出接口

测试写接口时使用独立测试数据库或明确标记的测试数据。

## 23. JMeter 性能测试学习链路

为了区分不同开销，建议建立四个 Thread Group。

### 23.1 公开读取

请求：

```text
GET /api/categories
GET /api/posts?page=1&size=10
GET /api/projects?page=1&size=10
```

用于观察公开查询的响应时间、吞吐量和错误率。

### 23.2 认证开销

每个线程先登录一次：

```text
POST /api/auth/admin/login
```

使用 JSON Extractor：

```text
JSONPath: $.data.accessToken
Variable: accessToken
```

循环请求：

```text
GET /api/auth/me
Authorization: Bearer ${accessToken}
```

这组场景主要测 JWT 解析和用户状态查询。

### 23.3 后台业务

登录一次后循环：

```text
GET /api/admin/dashboard
Authorization: Bearer ${accessToken}
```

这组场景包含鉴权查询和仪表盘业务查询。

### 23.4 登录接口

单独压测：

```text
POST /api/auth/admin/login
```

注意：

- BCrypt 本身是刻意设计的高成本计算；
- 每次成功登录都会更新用户、插入 Refresh Token、插入操作日志；
- 同一管理员高并发登录会产生同一用户行的写竞争；
- `auth_refresh_token` 和 `operation_log` 会持续增长；
- 应使用专用测试管理员和独立测试数据库；
- 真实个人网站通常不会出现大量管理员并发登录。

### 23.5 JMeter 断言

至少添加：

- HTTP 状态码断言：`200`；
- JSON 断言：`$.code` 等于 `200`；
- 登录响应断言：`$.data.accessToken` 不为空；
- 错误率观察；
- P90、P95、P99 响应时间；
- 吞吐量与服务端 CPU、内存、数据库连接一起观察。

## 24. 当前实现状态与学习注意事项

1. GitHub OAuth 授权地址接口已经存在，但回调交换尚未实现。
2. 评论验证码配置已经存在，启用后若没有服务商实现会返回 409。
3. 前端目前保存 Refresh Token，但没有自动调用刷新接口。
4. 密码修改会撤销 Refresh Token，不会立即撤销当前 Access Token。
5. 后台 JWT 鉴权每次都会查询用户状态，不是完全无数据库访问的纯无状态鉴权。
6. 所有成功接口当前统一返回 HTTP 200，没有使用 201 或 204。
7. 当前没有 `/api/v1` 版本前缀。
8. 当前没有自动生成的 Swagger/OpenAPI 页面，本文档由当前代码人工核对生成。
9. 公开文章详情会增加阅读量，不应当作为完全无副作用的 GET 请求看待。
10. 成功登录、评论提交、上传、导入和所有后台写接口都会修改数据库。

## 25. 文档维护规则

后续修改接口时，至少同步更新：

- 请求方法和路径；
- 权限要求；
- DTO 字段与校验；
- 响应模型；
- 状态枚举；
- 业务错误；
- 示例请求；
- 接口总数和全量索引。

接口代码的主要位置：

```text
backend/src/main/java/com/mlk/mlkbackend/controller
backend/src/main/java/com/mlk/mlkbackend/dto
backend/src/main/java/com/mlk/mlkbackend/vo
backend/src/main/java/com/mlk/mlkbackend/service
backend/src/main/java/com/mlk/mlkbackend/config/SecurityConfig.java
backend/src/main/java/com/mlk/mlkbackend/exception/GlobalExceptionHandler.java
```

---

本文档用于学习、调试和性能测试设计。生产压测前，应另行确认测试环境、数据清理方案、监控指标和允许的最大负载。
