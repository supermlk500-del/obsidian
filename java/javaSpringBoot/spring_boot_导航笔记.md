# Spring Boot 全知识体系【超详细完整版】

> 目标：**系统 + 全面 + 细节导向**，从「为什么有 Spring Boot」到「企业级生产落地」，适合作为 **学习主线 / 面试复盘 / 项目字典**。

---

## 一、Spring Boot 是什么

### 1.1 Spring Boot 的定位
- Spring Boot 是 **Spring 生态的快速开发框架**
- 目标：
  - 零 XML（约定优于配置）
  - 开箱即用
  - 快速启动 Web / 微服务项目

### 1.2 Spring Boot 解决了什么问题
| 传统 Spring | Spring Boot |
|------------|-------------|
| XML 配置繁琐 | 自动配置 |
| 依赖冲突多 | starter 统一依赖 |
| 需要外部 Tomcat | 内嵌容器 |
| 启动复杂 | main 方法启动 |

### 1.3 Spring / Spring MVC / Spring Boot 关系
- **Spring**：IOC + AOP 核心框架
- **Spring MVC**：Web MVC 框架
- **Spring Boot**：整合 Spring + Spring MVC + 第三方组件

---

## 二、Spring Boot 核心思想

### 2.1 约定优于配置
- 默认配置 > 手动配置
- 只有「不一样的地方」才需要配置

### 2.2 自动配置（Auto Configuration）
- 核心注解：`@EnableAutoConfiguration`
- 原理：
  1. 读取 `spring.factories`
  2. 加载自动配置类
  3. 条件注解判断是否生效

### 2.3 Starter 依赖思想
- `spring-boot-starter-web`
- `spring-boot-starter-data-jpa`
- 本质：**依赖聚合 + 版本统一**

---

## 三、Spring Boot 项目结构

```
com.example.demo
├── controller   控制层
├── service      业务层
├── service.impl
├── mapper       DAO 层
├── entity       实体类
├── config       配置类
├── common       通用组件
└── DemoApplication.java
```

### 启动类
```java
@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

---

## 四、@SpringBootApplication 注解拆解

```java
@SpringBootApplication =
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan
```

| 注解 | 作用 |
|----|----|
| @SpringBootConfiguration | 配置类 |
| @EnableAutoConfiguration | 启动自动配置 |
| @ComponentScan | 包扫描 |

---

## 五、配置文件体系（重点）

### 5.1 配置文件类型
- `application.properties`
- `application.yml / yaml`

### 5.2 yml 语法
```yaml
server:
  port: 8080
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/test
```

### 5.3 配置文件加载顺序（高 → 低）
1. 命令行参数
2. application-{profile}.yml
3. application.yml
4. 默认配置

---

## 六、配置绑定

### 6.1 @Value
```java
@Value("${server.port}")
private int port;
```

### 6.2 @ConfigurationProperties（推荐）
```java
@ConfigurationProperties(prefix = "user")
@Data
public class UserProperties {
    private String name;
    private Integer age;
}
```

---

## 七、IOC 与 Bean 管理

### 7.1 IOC 容器
- Spring 管理对象的创建、依赖、生命周期

### 7.2 常见组件注解
| 注解 | 层次 |
|----|----|
| @Component | 通用 |
| @Service | 业务层 |
| @Controller | 控制层 |
| @Repository | DAO 层 |

### 7.3 Bean 生命周期
1. 实例化
2. 属性注入
3. 初始化（@PostConstruct）
4. 使用
5. 销毁（@PreDestroy）

---

## 八、依赖注入（DI）

### 8.1 注入方式
- 构造器注入（推荐）
- @Autowired
- @Resource

### 8.2 构造器注入最佳实践
```java
@RequiredArgsConstructor
@Service
public class UserService {
    private final UserMapper userMapper;
}
```

---

## 九、Spring MVC（Web 核心）

### 9.1 Controller
```java
@RestController
@RequestMapping("/user")
```

### 9.2 请求映射
- @GetMapping
- @PostMapping
- @PutMapping
- @DeleteMapping

### 9.3 参数接收
| 注解 | 场景 |
|----|----|
| @RequestParam | URL 参数 |
| @PathVariable | 路径参数 |
| @RequestBody | JSON |
| @RequestHeader | 请求头 |

---

## 十、数据校验（Validation）

```java
@NotNull
@NotBlank
@Size
@Email
```

```java
@Validated
public Result save(@RequestBody @Valid UserDTO dto){}
```

---

## 十一、统一返回与异常处理

### 11.1 统一返回
```java
@Data
public class Result<T> {
    private int code;
    private String msg;
    private T data;
}
```

### 11.2 全局异常
```java
@RestControllerAdvice
public class GlobalExceptionHandler {}
```

---

## 十二、数据库整合

### 12.1 JDBC
### 12.2 MyBatis
### 12.3 MyBatis-Plus
- BaseMapper
- IService
- LambdaQueryWrapper

---

## 十三、事务管理

```java
@Transactional
```

- 回滚规则
- 传播行为
- 隔离级别

---

## 十四、AOP

### 14.1 使用场景
- 日志
- 权限
- 事务

```java
@Aspect
@Component
```

---

## 十五、Spring Security（安全）

- 认证 Authentication
- 授权 Authorization
- JWT
- 过滤器链

---

## 十六、Spring Boot 进阶

- 自定义 starter
- 自动配置原理
- 条件注解
- Actuator
- DevTools

---

## 十七、部署与运维

- jar / war
- Docker
- Nginx
- Linux

---

## 十八、Spring Boot 面试高频点

- 自动配置原理
- Bean 生命周期
- IOC / AOP
- 事务失效
- 循环依赖

---

## 十九、学习路线建议（给你）

> **基础 → 实战 → 原理 → 微服务**

1. Spring Boot + MyBatis-Plus
2. 项目实战（后台管理系统）
3. Spring 源码
4. Spring Cloud

---

📌 **这是「完整版第一版」**，如果你愿意：
- 我可以 **拆成 20 讲学习路线**
- 或 **每一章扩展成“源码级”说明**
- 或 **按面试题形式重写一版**

