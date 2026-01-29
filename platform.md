下面是一份面向开发与测试的接口文档草案，基于你现有的后端实现（Spring Boot + Spring Security + JWT）。文档用中文撰写，包含端点、请求/响应格式、认证方式、错误码与示例，方便前端对接与后端自测。

一、总览

- 基础前缀：/user
- 认证方式：登录后通过 JWT（Bearer Token）进行鉴权，后续需要鉴权的接口通过 Authorization: Bearer 访问
- 令牌有效期：1 天（application.yml 中 jwt.expiration = 86400000，实际可根据环境调整）
- 密钥管理：JWT 秘钥通过环境变量 JWT_SECRET 注入，默认值仅用于本地测试
- CSRF：已禁用，无状态会话（STATELESS）

二、鉴权要点

- 未认证的请求（未携带或携带无效 token）会返回未授权错误，典型响应为 401，错误体包含 path、timestamp 等信息
- 仅 /user/register、/user/login 这两个端点对外暴露，无需认证，其它端点需要携带有效的 JWT
- token 内容通常包含用户的手机号（phone）作为标识，在后续鉴权时会以 phone 作为用户名进行加载

三、端点总览

1. 注册用户

- 路径与方法
    - POST /user/register
- 认证要求
    - 无需认证
- 请求(示例)
    - Content-Type: application/json
    - body: { "username": "测试用户", "password": "Abcd1234", // 满足密码策略：8-20 位，包含大写字母和数字 "gender": "男", // "男" 或 "女" "phone": "13800138000", // 中国大陆手机号格式 "level": 1 }
- 响应(示例)
    - 成功 { "code": 200, "message": "success", "data": { "username": "测试用户", "phone": "13800138000", "gender": "男", "level": 1 } }
    - 失败（示例） { "code": 400, "message": "手机号码已存在", "data": null }
- 说明
    - 服务器端会对输入进行双重校验，注册成功后会返回用户的核心信息，密码不会返回
    - 注册时会对输入进行自定义校验（如 XSS/注入防护），遇到非法输入会返回失败信息

2. 登录用户

- 路径与方法
    - POST /user/login
- 认证要求
    - 无需认证
- 请求(示例)
    - Content-Type: application/json
    - body: { "phone": "13800138000", "password": "UserPassword123" // 前端需确保传输明文密码，后端哈希比对 }
- 响应(示例)
    - 成功（返回 JWT token） { "code": 200, "message": "success", "data": { "token": "", "phone": "13800138000" } }
    - 失败（示例） { "code": 400, "message": "密码错误", "data": null }
- 说明
    - 成功后前端需保存 token，后续请求请将 Authorization 设置为 Bearer

3. 更新用户信息

- 路径与方法
    - POST /user/update
- 认证要求
    - 需要有效的 JWT（Authorization: Bearer ）
- 请求(示例)
    - Content-Type: application/json
    - body: { "username": "新的用户名", "password": "NewPassw0rd", // 8-20 位，含大写字母和数字 "gender": "女", "phone": "13800138001", // 新手机号 "lastPhone": "13800138000" // 旧手机号，用于定位用户记录 }
- 响应(示例)
    - 成功 { "code": 200, "message": "success", "data": { "username": "新的用户名", "phone": "13800138001", "gender": "女" } }
    - 失败 { "code": 400, "message": "原手机号不存在，无法更新", "data": null }
- 说明
    - 更新前会根据 lastPhone 查找当前用户；若新手机号已存在，会返回冲突错误
    - 更新后密码会进行哈希存储，返回字段中不包含敏感信息

四、响应体结构（服务端 Response 封装）

- 成功响应通常包含 data 字段，示例： { "code": 200, "message": "success", "data": { ... } }
- 失败响应通常包含 message 字段，示例： { "code": 400, "message": "错误原因", "data": null }
- 未授权错误（未登录/无权限）示例： { "code": 401, "message": "未授权，请先登录", "path": "/user/xxx", "timestamp": 1630000000000 }

五、错误码与含义（常用）

- 200 OK：成功
- 400 Bad Request：请求参数校验失败或业务校验未通过
- 401 Unauthorized：未认证/无权限
- 403 Forbidden：访问被拒绝
- 409 Conflict：资源冲突（如手机号已存在）
- 500 Internal Server Error：服务端异常

六、认证与安全要点

- 使用 Authorization: Bearer 访问需要鉴权的接口
- 为了安全，尽量在 HTTPS 下使用 API，避免明文传输
- JWT 秘钥通过环境变量注入：JWT_SECRET，生产环境应确保密钥高强度且定期轮换
- 不在日志中输出敏感信息（如明文密码、token 明文等）
- 对输入进行服务端校验，避免前端伪造请求绕过前端校验

七、环境变量与部署

- JWT 秘钥
    - 在生产环境中设置：JWT_SECRET=你自己的高强度密钥
    - 本地开发默认值为 ChangeMePleaseSetInEnv，仅作演示，强烈建议设定实际密钥
- 数据库连接
    - 已在 application.yml 中定义 MySQL 连接信息，请按实际环境配置
- 运行方式
    - 启动应用后，使用上述端点进行注册、登录与更新

八、快速自测命令（补充示例）

- 注册（正确输入）
    - curl -X POST [http://localhost:8080/user/register](http://localhost:8080/user/register) -H "Content-Type: application/json" -d '{"username":"测试用户","password":"Abcd1234","gender":"男","phone":"13800138000","level":1}'
- 登录
    - curl -X POST [http://localhost:8080/user/login](http://localhost:8080/user/login) -H "Content-Type: application/json" -d '{"phone":"13800138000","password":"Abcd1234"}'
- 使用 Token 访问需要鉴权的接口（示例，需替换为实际 token）
    - curl -X POST [http://localhost:8080/user/update](http://localhost:8080/user/update) -H "Content-Type: application/json" -H "Authorization: Bearer " -d '{"username":"新名","password":"NewPassw0rd","gender":"女","phone":"13800138001","lastPhone":"13800138000"}'

九、版本与变更

- 版本1.0（初始接口文档草案）
- 版本1.1（已实现日志安全改进、修正登录逻辑、环境变量密钥注入、注册/更新的服务端自校验调用等）
- 未来计划（可选）
    - 增强验证码与速率限制
    - 增加忘记密码与邮箱/短信验证流程
    - 引入 OpenAPI/Swagger 文档以便前后端自动化对接
    - 增加更多客户端友好字段的统一响应格式

如需，我也可以把以上内容整理成公开的 OpenAPI 规范（YAML/JSON）或生成一个更详细的接口文档站点（Swagger UI/Redoc），方便前端和测试团队使用。需要的话告诉我你偏好的格式（OpenAPI/Swagger、Markdown、HTML 文档等），我就按格式输出完整版本。