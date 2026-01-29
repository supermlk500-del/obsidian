# Campus Trading System

<p align="center">
  <strong>基于 Spring Boot 3 + Vue 3 的现代化校园二手交易平台</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Spring%20Boot-3.5.5-brightgreen" alt="Spring Boot">
  <img src="https://img.shields.io/badge/Vue-3.5.18-blue" alt="Vue">
  <img src="https://img.shields.io/badge/JDK-17+-orange" alt="JDK">
  <img src="https://img.shields.io/badge/MySQL-8.0-blue" alt="MySQL">
  <img src="https://img.shields.io/badge/Redis-7.0-red" alt="Redis">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

## 项目简介

Campus Trading System 是一个面向高校学生的二手商品交易平台，提供商品发布、浏览、收藏、订单管理、实时消息通信等完整的交易闭环功能。系统集成 DeepSeek AI 智能客服，为用户提供 7×24 小时在线咨询服务。

## 技术架构

### 后端技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Spring Boot | 3.5.5 | 核心框架 |
| Spring Security | 6.x | 安全认证框架 |
| Spring Data JPA | 3.x | ORM 持久层 |
| Spring Data Redis | 3.x | 缓存中间件 |
| Spring WebSocket | 3.x | 实时通信 |
| JWT (jjwt) | 0.11.5 | 令牌认证 |
| MySQL Connector | 8.x | 数据库驱动 |
| MinIO | 8.5.7 | 对象存储 |
| OkHttp | 4.12.0 | HTTP 客户端 |
| Thumbnailator | 0.4.20 | 图片压缩处理 |
| SpringDoc OpenAPI | 2.2.0 | API 文档 |
| Lombok | - | 代码简化 |

### 前端技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | 3.5.18 | 前端框架 |
| Vite | 7.0.6 | 构建工具 |
| Vue Router | 4.5.1 | 路由管理 |
| Axios | 1.13.2 | HTTP 请求 |
| @stomp/stompjs | 7.0.0 | WebSocket 客户端 |
| SockJS-client | 1.6.1 | WebSocket 兼容层 |

### 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        客户端 (Browser)                          │
│                    Vue 3 + Vite + Vue Router                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                    HTTP REST API / WebSocket
                                │
┌─────────────────────────────────────────────────────────────────┐
│                     Spring Boot Application                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Controller  │  │  Security   │  │    WebSocket Handler    │  │
│  │    Layer    │  │   Filter    │  │    (STOMP Protocol)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Service   │  │    AOP      │  │     DeepSeek Client     │  │
│  │    Layer    │  │  Logging    │  │      (AI Assistant)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Repository  │  │   Redis     │  │      MinIO Service      │  │
│  │  (JPA)      │  │   Cache     │  │    (File Storage)       │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌───────┴───────┐       ┌───────┴───────┐       ┌───────┴───────┐
│   MySQL 8.0   │       │   Redis 7.0   │       │     MinIO     │
│  (主数据存储)  │       │   (会话缓存)   │       │  (文件存储)   │
└───────────────┘       └───────────────┘       └───────────────┘
```

## 功能模块

### 用户模块
- 用户注册/登录（学号验证）
- JWT 令牌认证与自动续期
- 个人资料管理与头像上传
- 基于角色的权限控制 (RBAC)

### 商品模块
- 商品发布（多图上传、分类选择）
- 商品列表（分页、筛选、搜索）
- 商品详情展示
- 我的商品管理（编辑、上下架、删除）

### 收藏模块
- 商品收藏/取消收藏
- 收藏列表管理

### 订单模块
- 订单创建与状态流转
- 买卖双方确认机制
- 订单历史记录
- 订单取消功能

### 消息模块
- WebSocket + STOMP 实时通信
- 买卖双方即时聊天
- 系统通知推送
- 未读消息统计
- 消息历史持久化

### AI 客服模块
- DeepSeek AI 驱动的智能对话
- 上下文记忆与连贯对话
- 平台使用咨询
- 浮动聊天窗口

### 管理后台
- 管理员登录认证
- 数据统计仪表板
- 用户管理
- 商品审核管理
- 订单管理
- 分类管理
- 系统日志查看

## 项目结构

```
CampusSystem/
├── campus-backend/                    # 后端项目
│   ├── src/main/java/com/example/campussystem/
│   │   ├── aspect/                    # AOP 切面
│   │   │   └── LoggingAspect.java
│   │   ├── client/                    # 外部服务客户端
│   │   │   └── DeepSeekClient.java
│   │   ├── common/                    # 通用类
│   │   │   └── ApiResponse.java
│   │   ├── config/                    # 配置类
│   │   │   ├── SecurityConfig.java
│   │   │   ├── RedisConfig.java
│   │   │   ├── MinIOConfig.java
│   │   │   ├── WebSocketConfig.java
│   │   │   └── SwaggerConfig.java
│   │   ├── controller/                # 控制器层
│   │   │   ├── AuthController.java
│   │   │   ├── ProductController.java
│   │   │   ├── OrderController.java
│   │   │   ├── MessageController.java
│   │   │   ├── FavoriteController.java
│   │   │   ├── CategoryController.java
│   │   │   ├── FileUploadController.java
│   │   │   ├── AIAssistantController.java
│   │   │   ├── AdminAuthController.java
│   │   │   ├── AdminController.java
│   │   │   └── AdminManagementController.java
│   │   ├── dto/                       # 数据传输对象
│   │   ├── entity/                    # 实体类
│   │   │   ├── User.java
│   │   │   ├── Product.java
│   │   │   ├── Order.java
│   │   │   ├── Message.java
│   │   │   ├── Favorite.java
│   │   │   ├── Category.java
│   │   │   └── Admin.java
│   │   ├── exception/                 # 异常处理
│   │   │   ├── BusinessException.java
│   │   │   └── GlobalExceptionHandler.java
│   │   ├── repository/                # 数据访问层
│   │   ├── security/                  # 安全相关
│   │   │   ├── JwtAuthenticationFilter.java
│   │   │   ├── JwtAuthenticationEntryPoint.java
│   │   │   └── CustomUserDetailsService.java
│   │   ├── service/                   # 服务层
│   │   │   ├── UserService.java
│   │   │   ├── ProductService.java
│   │   │   ├── OrderService.java
│   │   │   ├── MessageService.java
│   │   │   ├── FavoriteService.java
│   │   │   ├── CategoryService.java
│   │   │   ├── FileUploadService.java
│   │   │   ├── MinIOService.java
│   │   │   ├── AIAssistantService.java
│   │   │   ├── CacheService.java
│   │   │   └── WebSocketService.java
│   │   ├── util/                      # 工具类
│   │   │   ├── JwtUtil.java
│   │   │   ├── ImageCompressor.java
│   │   │   └── SecurityUtil.java
│   │   ├── websocket/                 # WebSocket 处理
│   │   │   ├── WebSocketHandler.java
│   │   │   └── WebSocketAuthInterceptor.java
│   │   └── CampusSystemApplication.java
│   └── src/main/resources/
│       ├── application.yml
│       └── logback-spring.xml
│
├── campus-fonted/                     # 前端项目
│   ├── src/
│   │   ├── api/                       # API 接口封装
│   │   │   ├── request.js
│   │   │   ├── auth.js
│   │   │   └── admin.js
│   │   ├── components/                # Vue 组件
│   │   │   ├── Home.vue
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── ProductList.vue
│   │   │   ├── ProductDetail.vue
│   │   │   ├── ProductPublish.vue
│   │   │   ├── MyProducts.vue
│   │   │   ├── Favorites.vue
│   │   │   ├── OrderManagement.vue
│   │   │   ├── MessageCenter.vue
│   │   │   ├── AIAssistant.vue
│   │   │   ├── OptimizedImage.vue
│   │   │   ├── ToastNotification.vue
│   │   │   ├── ModalNotification.vue
│   │   │   ├── AdminLogin.vue
│   │   │   ├── AdminDashboard.vue
│   │   │   └── admin/
│   │   ├── config/                    # 配置
│   │   ├── router/                    # 路由配置
│   │   ├── services/                  # 服务层
│   │   │   ├── messageService.js
│   │   │   ├── toast.js
│   │   │   └── modal.js
│   │   ├── utils/                     # 工具函数
│   │   ├── assets/                    # 静态资源
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── db/
│   └── campus_trading.sql             # 数据库脚本
├── logs/                              # 日志目录
└── README.md
```

## 快速开始

### 环境要求

- JDK 17+
- Node.js 20.19+ 或 22.12+
- MySQL 8.0+
- Redis 7.0+
- Maven 3.9+

### 数据库初始化

```bash
# 创建数据库并导入数据
mysql -u root -p < db/campus_trading.sql
```

### 后端启动

```bash
cd campus-backend

# 修改配置文件 src/main/resources/application.yml
# 配置数据库连接、Redis、MinIO、DeepSeek API Key 等

# 编译打包
mvn clean package -DskipTests

# 启动服务
mvn spring-boot:run
# 或
java -jar target/CampusSystem-0.0.1-SNAPSHOT.jar
```

后端服务默认运行在 `http://localhost:8081/api/v1`

### 前端启动

```bash
cd campus-fonted

# 安装依赖
npm install

# 开发模式启动
npm run dev

# 生产构建
npm run build
```

前端服务默认运行在 `http://localhost:5173`

## 配置说明

### 核心配置项 (application.yml)

```yaml
# 数据库配置
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/campus_trading
    username: root
    password: your_password

# Redis 配置
  data:
    redis:
      host: localhost
      port: 6379
      password: your_redis_password

# JWT 配置
jwt:
  secret: your_jwt_secret_key_at_least_32_characters
  expiration: 86400000  # 24小时

# MinIO 配置
minio:
  endpoint: http://your-minio-server:9000
  access-key: your_access_key
  secret-key: your_secret_key
  bucket-name: campus-system

# DeepSeek AI 配置
deepseek:
  api:
    key: your_deepseek_api_key
    base-url: https://api.deepseek.com
    model: deepseek-chat
```

### 前端环境变量 (.env)

```properties
VITE_API_BASE_URL=http://localhost:8081/api/v1
```

## API 文档

启动后端服务后访问 Swagger UI：

- Swagger UI: `http://localhost:8081/api/v1/swagger-ui/index.html`
- OpenAPI JSON: `http://localhost:8081/api/v1/v3/api-docs`

### 主要 API 端点

| 模块 | 端点 | 方法 | 说明 |
|------|------|------|------|
| 认证 | `/auth/register` | POST | 用户注册 |
| 认证 | `/auth/login` | POST | 用户登录 |
| 商品 | `/products` | GET | 商品列表 |
| 商品 | `/products` | POST | 发布商品 |
| 商品 | `/products/{id}` | GET | 商品详情 |
| 订单 | `/orders` | POST | 创建订单 |
| 订单 | `/orders` | GET | 订单列表 |
| 收藏 | `/favorites` | POST | 添加收藏 |
| 消息 | `/messages` | GET | 消息列表 |
| AI | `/ai-assistant/chat` | POST | AI 对话 |
| 文件 | `/files/upload` | POST | 文件上传 |
| 管理 | `/admin/auth/login` | POST | 管理员登录 |
| 管理 | `/admin/dashboard/stats` | GET | 统计数据 |

## 部署指南

### Docker 部署

```yaml
# docker-compose.yml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: campus_trading
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7.0-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./campus-backend
    ports:
      - "8081:8081"
    depends_on:
      - mysql
      - redis
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/campus_trading
      SPRING_REDIS_HOST: redis

  frontend:
    build: ./campus-fonted
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  mysql_data:
```

### Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/campus-frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/v1 {
        proxy_pass http://localhost:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 性能优化

### 后端优化
- HikariCP 连接池（最大 20 连接）
- Redis 多级缓存策略
- 图片自动压缩（85% 质量，最大 1920px）
- OkHttp 连接池复用
- AOP 日志异步处理

### 前端优化
- OptimizedImage 组件懒加载
- Vite 代码分割
- HTTP 缓存策略
- 响应式设计适配

## 安全措施

- JWT 令牌认证
- BCrypt 密码加密
- Spring Security 权限控制
- CORS 跨域配置
- 参数校验 (JSR-303)
- 全局异常处理
- SQL 注入防护 (JPA 参数化查询)

## 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

## 联系方式

- 维护者：Maven
- 邮箱：15035267995@163.com
- Gitee：https://gitee.com/lancemorii-git/campus-system.git
- GitHub：https://github.com/LanceMorii/CampusSystem.git

---

> 本项目仅供学习研究使用，生产环境部署前请确保遵守相关法律法规。
