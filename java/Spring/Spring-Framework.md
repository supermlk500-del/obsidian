# Spring Framework 笔记

## 1. Spring Framework 是什么
- `Spring Framework` 是 Java 生态中主流的基础框架，核心能力是：
  - `IoC`（控制反转）
  - `AOP`（面向切面编程）
- 它不仅是一个框架，更是一套**基础设施标准**，可整合 `MyBatis`、`Hibernate`、`Redis`、`MQ`、`Security` 等。

---

## 2. 核心特点
- **非侵入式**：业务代码不强依赖框架 API，领域模型污染小。
- **IoC / DI**：对象创建和依赖管理交给容器。
- **AOP**：在不修改业务代码的前提下进行增强（日志、事务、权限等）。
- **容器化管理**：统一管理 Bean 生命周期。
- **组件化**：按职责拆分组件，便于维护和扩展。
- **生态完整**：与 Spring 全家桶及主流中间件深度整合。

---

## 3. IoC（控制反转）与 DI（依赖注入）

### 3.1 为什么需要 IoC
传统方式是对象自己 `new` 依赖，耦合高、难测试。
IoC 将“对象控制权”交给容器，业务类只声明依赖。

### 3.2 DI 的常见方式
- 构造器注入（推荐，依赖更明确）
- Setter 注入
- 字段注入（简洁但测试/可维护性相对弱）

```java
@Service
public class UserService {
    private final UserDao userDao;

    public UserService(UserDao userDao) {
        this.userDao = userDao;
    }
}
```

---

## 4. Bean 管理

### 4.1 常见组件注解
- `@Component`：通用组件
- `@Controller`：表现层（Spring MVC 控制器）
- `@Service`：业务层
- `@Repository`：持久层（可触发数据访问异常转换）

### 4.2 Bean 作用域（Scope）
- `singleton`：单例（默认）
- `prototype`：多例
- `request`：一次请求一个（Web 环境）
- `session`：一次会话一个（Web 环境）

### 4.3 生命周期（常见）
1. 实例化
2. 依赖注入
3. 初始化（如 `@PostConstruct`）
4. 使用
5. 销毁（如 `@PreDestroy`，单例容器关闭时）

### 4.4 第三方对象注册
```java
@Configuration
public class AppConfig {
    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper();
    }
}
```

---

## 5. AOP（面向切面编程）

### 5.1 AOP 解决什么问题
把通用横切逻辑（日志、事务、权限、监控）从业务代码中抽离，减少重复。

### 5.2 关键术语
- `Aspect`：切面
- `JoinPoint`：连接点（可被拦截的方法）
- `Pointcut`：切点（匹配规则）
- `Advice`：通知（增强逻辑）

### 5.3 通知类型
- `@Before`
- `@After`
- `@AfterReturning`
- `@AfterThrowing`
- `@Around`（最强，常用）

```java
@Aspect
@Component
public class LogAspect {
    @Around("execution(* com.example.service..*(..))")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        try {
            return pjp.proceed();
        } finally {
            long cost = System.currentTimeMillis() - start;
            System.out.println(pjp.getSignature() + " cost=" + cost + "ms");
        }
    }
}
```

---

## 6. Spring MVC（Web 核心）

### 6.1 基本流程
1. 请求进入 `DispatcherServlet`
2. 由处理器映射找到目标控制器方法
3. 执行控制器方法
4. 返回视图或 JSON

### 6.2 `@Controller` 的用法与意义
- 标识一个类是 MVC 控制器，负责接收请求并返回视图/数据。
- 若要直接返回 JSON，常用：
  - 类上 `@RestController`（=`@Controller + @ResponseBody`）
  - 或方法上加 `@ResponseBody`

```java
@Controller
@RequestMapping("/user")
public class UserController {

    @GetMapping("/hello")
    @ResponseBody
    public String hello() {
        return "hello";
    }
}
```

---

## 7. `web.xml` 与 `servlet-mapping`（重点补充）

> 在纯 `Servlet` 或早期 Spring MVC 项目里常见；Spring Boot 中通常由自动配置替代。

### 7.1 `web.xml` 基本结构
```xml
<web-app>
    <servlet>
        <servlet-name>springmvc</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:springmvc.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>springmvc</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

### 7.2 `init-param` 配置位置和名称
- 写在 `<servlet>` 内部。
- Spring MVC 常见参数名：`contextConfigLocation`
- 用途：指定 Spring MVC 容器配置文件位置。

### 7.3 `load-on-startup` 作用
- 值 `>=0`：容器启动时初始化该 Servlet。
- 值越小优先级越高（一般写 `1`）。
- 好处：启动时提前发现配置错误，首请求响应更快。

### 7.4 `url-pattern` 中 `/`、`/*` 的区别
- `/`：拦截除 JSP 外的大多数请求（常用于 `DispatcherServlet`）
- `/*`：拦截所有请求（包括静态资源和 JSP），通常不建议用于 Spring MVC 前端控制器
- 精确匹配：如 `/api/*` 仅拦截该路径前缀

---

## 8. 事务管理（Spring 非常重要）

### 8.1 声明式事务
常用 `@Transactional`：

```java
@Service
public class TransferService {

    @Transactional
    public void transfer() {
        // 扣款
        // 加款
    }
}
```

### 8.2 常见事务属性
- `propagation`：传播行为（如 `REQUIRED`）
- `isolation`：隔离级别
- `readOnly`：是否只读
- `rollbackFor`：指定回滚异常类型

### 8.3 注意点
- 默认只对运行时异常回滚
- 同类方法内部调用可能导致事务失效（绕过代理）
- `@Transactional` 建议放在 `public` 方法

---

## 9. Spring 与 Spring Boot 的关系
- `Spring Framework`：基础能力（IoC、AOP、MVC、事务等）
- `Spring Boot`：在 Spring 基础上做自动配置、Starter 依赖管理、快速启动

一句话：**Boot 是“开发加速器”，Framework 是“底层引擎”。**

---

## 10. 常见面试高频问答（速记）
- `IoC` 是什么？
  - 对象控制权交给容器。
- `DI` 和 `IoC` 关系？
  - `IoC` 是思想，`DI` 是实现方式。
- `AOP` 典型应用？
  - 日志、事务、权限、监控。
- `@Controller` 和 `@RestController` 区别？
  - 后者默认返回响应体（JSON/字符串）。
- Spring 事务为什么有时不生效？
  - 代理失效（如同类内调用）、异常类型不匹配、方法可见性问题等。

---

## 11. 易错点纠正
- `SpringIoc` → `Spring IoC`
- `java-EE` 现代写法常见为 `Java EE / Jakarta EE`
- `url-patter` → `url-pattern`
- `init-parm` → `init-param`
- 术语建议统一：`Spring Framework`、`IoC`、`AOP`、`DispatcherServlet`

---

## 12. 学习路径建议（按顺序）
1. IoC / DI（容器和 Bean）
2. AOP（切面思想）
3. Spring MVC（请求处理）
4. 声明式事务
5. 与 MyBatis / Spring Boot 的整合

> 学完这一版后，你可以继续补一份《Spring MVC 注解速查表》与《事务失效排查清单》。

---

## 13. Spring MVC 补充

### 13.1 `DispatcherServlet` 的工作流程（务必理解）
1. 请求进入 `DispatcherServlet`（前端控制器）
2. `HandlerMapping` 根据 URL 找到处理器（Controller 方法）
3. `HandlerAdapter` 负责调用目标方法
4. 方法执行后返回 `ModelAndView` 或响应体
5. 如果是视图名，交给 `ViewResolver` 解析视图
6. 渲染结果并返回客户端

一句话：`DispatcherServlet` 负责“统一接收 + 分发处理 + 统一返回”。

### 13.2 `@Controller` 和 `@RestController` 深入区别
- `@Controller`：默认返回“视图名”，通常用于页面跳转（JSP/Thymeleaf）
- `@RestController`：默认返回“响应体”（JSON/字符串）

```java
@Controller
@RequestMapping("/page")
public class PageController {
    @GetMapping("/home")
    public String home() {
        return "home"; // 视图名
    }
}

@RestController
@RequestMapping("/api")
public class ApiController {
    @GetMapping("/user")
    public Map<String, Object> user() {
        return Map.of("id", 1, "name", "Tom");
    }
}
```

### 13.3 常用请求注解（实战高频）
- 路径映射：`@RequestMapping`、`@GetMapping`、`@PostMapping`
- 路径参数：`@PathVariable`
- 查询参数：`@RequestParam`
- 请求体 JSON：`@RequestBody`
- 响应体：`@ResponseBody`

```java
@RestController
@RequestMapping("/orders")
public class OrderController {

    @GetMapping("/{id}")
    public String getById(@PathVariable Long id) {
        return "order-" + id;
    }

    @GetMapping
    public String list(@RequestParam(defaultValue = "1") int page) {
        return "page=" + page;
    }
}
```

### 13.4 关于 `@RequestMapping 的说明与使用
日常里有人说“`@RestMapping`”，通常指下面两种组合：
1. `@RequestMapping`（负责请求路径/方法映射）
2. `@RestController`（让返回值默认作为响应体输出）

也可以理解为：
- `@RestController + @RequestMapping` ≈ 大家口语里说的“Rest 风格映射写法”

#### 推荐写法示例
```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    public String get(@PathVariable Long id) {
        return "user-" + id;
    }

    @PostMapping
    public String create(@RequestBody String body) {
        return "created";
    }
}
```

#### `@RequestMapping` 常见属性
- `value` / `path`：请求路径
- `method`：请求方式（GET/POST/PUT/DELETE...）
- `produces`：返回内容类型
- `consumes`：接收内容类型
- `params`：限定请求必须携带的参数（及参数值），满足条件才会路由到该方法
- `headers`：限定请求头必须满足的条件，满足条件才会路由到该方法

```java
@RequestMapping(
    value = "/search",
    method = RequestMethod.GET,
    produces = "application/json"
)
public String search() {
    return "ok";
}
```

#### 实战建议
- 类上用 `@RequestMapping("/资源")`，方法上用 `@GetMapping/@PostMapping` 等细分注解。
- 纯接口项目优先 `@RestController`，避免每个方法都写 `@ResponseBody`。
- 如果看到“`@RestMapping`”说法，先确认对方实际指的是不是 `@RequestMapping`。

### 13.5 参数绑定和数据校验
- Spring MVC 支持将请求参数自动绑定到 Java 对象。
- 配合 `@Valid` + `BindingResult` 可进行参数校验。

```java
@PostMapping("/save")
public String save(@Valid @RequestBody UserDTO dto, BindingResult br) {
    if (br.hasErrors()) {
        return "参数校验失败";
    }
    return "ok";
}
```

### 13.5 异常处理（推荐统一处理）
- 使用 `@RestControllerAdvice + @ExceptionHandler` 统一返回错误信息。
- 好处：控制器更简洁，错误格式统一。

---

## 14. `web.xml` 补充笔记（传统项目重点）

### 14.1 `web.xml` 的定位
- `web.xml` 是 Java Web 项目的部署描述文件（传统方式）。
- 核心用途：注册 Servlet / Filter / Listener，配置启动参数和映射规则。
- 在 Spring Boot 中，大多由自动配置替代。

### 14.2 核心标签作用
- `<servlet>`：定义 Servlet 类及其初始化参数
- `<servlet-mapping>`：配置 URL 到 Servlet 的映射
- `<filter>` + `<filter-mapping>`：定义并映射过滤器
- `<listener>`：监听容器生命周期或会话事件
- `<welcome-file-list>`：默认首页配置

### 14.3 `servlet-mapping` 的 `url-pattern` 规则
- 精确匹配：`/login`
- 路径匹配：`/api/*`
- 扩展名匹配：`*.do`
- 默认匹配：`/`

特别注意：
- 对 `DispatcherServlet` 常用 `/`
- 不建议写 `/*`（会过度拦截，可能影响 JSP/静态资源）

### 14.4 `init-param` 与 `load-on-startup`
- `init-param`：传初始化参数给指定 Servlet
- `load-on-startup`：控制 Servlet 是否在启动时初始化
  - `>=0`：容器启动时初始化（推荐）
  - `<0` 或不写：首次请求时初始化

### 14.5 典型 `web.xml` 示例（Spring MVC）
```xml
<web-app>
    <display-name>springmvc-demo</display-name>

    <servlet>
        <servlet-name>springmvc</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:springmvc.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>springmvc</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>

    <welcome-file-list>
        <welcome-file>index.jsp</welcome-file>
    </welcome-file-list>
</web-app>
```

### 14.6 常见错误排查
- 404：`url-pattern` 与请求路径不一致
- 启动报错：`contextConfigLocation` 写错或配置文件不存在
- 静态资源访问失败：前端控制器拦截范围过大，未放行资源目录

---

## 15. 这一块的面试总结（可背）
- Spring MVC 通过 `DispatcherServlet` 统一分发请求，是典型前端控制器模式。
- `@Controller` 偏页面，`@RestController` 偏接口 JSON。
- `web.xml` 是传统 Java Web 的总配置入口，Boot 项目里通常被注解和自动配置替代。

---

## 16. Thymeleaf（全面笔记）

### 16.1 Thymeleaf 是什么
- `Thymeleaf` 是 Java 服务端模板引擎，常与 `Spring MVC / Spring Boot` 搭配。
- 主要价值：将后端数据渲染到 HTML 页面，适合中后台系统、管理系统、服务端渲染页面。
- 特点：
  - 自然模板（HTML 可直接在浏览器打开查看静态效果）
  - 语法贴近 HTML 属性，不破坏标签结构
  - 与 Spring 表单、国际化、校验体系整合好

### 16.2 与 JSP 的核心差异（理解定位）
- `JSP`：依赖 JSP 容器与标签体系，历史项目常见
- `Thymeleaf`：更现代、与 Spring Boot 集成更顺滑，模板可读性更好
- 在 Spring Boot 新项目中，一般优先 `Thymeleaf`（若是前后端分离则多用 REST + Vue/React）

### 16.3 Spring Boot 整合 Thymeleaf
#### 1) 依赖
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

#### 2) 默认约定
- 模板目录：`src/main/resources/templates/`
- 静态资源目录：`src/main/resources/static/`
- 默认后缀：`.html`

#### 3) 常见配置（`application.yml`）
```yml
spring:
  thymeleaf:
    prefix: classpath:/templates/
    suffix: .html
    mode: HTML
    encoding: UTF-8
    cache: false
```

说明：
- 开发阶段建议 `cache: false`，方便实时改模板。
- 生产环境建议开启缓存提高性能。

### 16.4 MVC 返回页面的基本方式
```java
@Controller
@RequestMapping("/user")
public class UserPageController {

    @GetMapping("/profile")
    public String profile(Model model) {
        model.addAttribute("name", "LHR");
        model.addAttribute("age", 20);
        return "user/profile"; // 对应 templates/user/profile.html
    }
}
```

### 16.5 页面取值与基础表达式
```html
<h1 th:text="${name}">默认名称</h1>
<p th:text="${age}">0</p>
```
- `${...}`：变量表达式（从 `Model`、`request` 等上下文取值）
- `th:text`：替换标签文本内容（自动 HTML 转义，防 XSS）
- `th:utext`：不转义输出（谨慎使用，可能引入 XSS）

### 16.6 常用标准语法（高频）
#### 1) 文本与属性
- `th:text`：设置文本
- `th:value`：设置 input 的 value
- `th:href` / `th:src`：设置链接/资源地址
- `th:attr`：设置多个属性

#### 2) 条件判断
```html
<p th:if="${age >= 18}">已成年</p>
<p th:unless="${age >= 18}">未成年</p>
```

#### 3) 循环
```html
<ul>
  <li th:each="u, stat : ${users}">
    <span th:text="${stat.count}">1</span>
    <span th:text="${u.username}">name</span>
  </li>
</ul>
```
- `stat` 是状态变量，可用 `index`、`count`、`first`、`last`。

#### 4) `switch/case`
```html
<div th:switch="${role}">
  <p th:case="'ADMIN'">管理员</p>
  <p th:case="'USER'">普通用户</p>
  <p th:case="*">访客</p>
</div>
```

### 16.7 链接表达式与路径写法
```html
<a th:href="@{/orders/{id}(id=${order.id})}">详情</a>
<img th:src="@{/images/logo.png}" alt="logo">
```
- `@{...}`：URL 表达式，自动处理上下文路径。
- 推荐用 `@{}` 生成链接，避免项目部署路径变化导致 URL 失效。

### 16.8 内联表达式与字符串拼接
```html
<p th:text="|当前用户：${name}，年龄：${age}|">占位文本</p>
<p th:text="${name} + ' - ' + ${age}">占位文本</p>
```

### 16.9 片段复用（布局复用重点）
#### 1) 定义片段
```html
<!-- templates/common/header.html -->
<div th:fragment="top(title)">
  <h2 th:text="${title}">标题</h2>
</div>
```

#### 2) 引入片段
```html
<div th:replace="~{common/header :: top('用户中心')}"></div>
```

常见方式：
- `th:insert`：插入到标签体内
- `th:replace`：整个标签被替换（更常用）
- `th:include`：旧语法，现代版本中不推荐

### 16.10 表单处理与对象绑定
```java
@GetMapping("/form")
public String form(Model model) {
    model.addAttribute("userForm", new UserForm());
    return "user/form";
}

@PostMapping("/form")
public String submit(@Valid @ModelAttribute("userForm") UserForm form,
                     BindingResult br) {
    if (br.hasErrors()) {
        return "user/form";
    }
    return "redirect:/user/success";
}
```

```html
<form th:action="@{/user/form}" th:object="${userForm}" method="post">
  <input type="text" th:field="*{username}">
  <input type="password" th:field="*{password}">
  <button type="submit">提交</button>
</form>
```

说明：
- `th:object` 指定表单绑定对象
- `th:field="*{...}"` 绑定字段并自动回显

### 16.11 校验错误显示
```html
<div th:if="${#fields.hasErrors('username')}" th:errors="*{username}"></div>
<div th:if="${#fields.hasErrors('*')}" th:errors="*{*}"></div>
```

### 16.12 国际化（i18n）
#### 1) 资源文件
- `messages.properties`
- `messages_zh_CN.properties`
- `messages_en_US.properties`

#### 2) 页面取值
```html
<h1 th:text="#{home.title}">首页</h1>
```
- `#{...}`：消息表达式，按语言环境解析文本。

### 16.13 Thymeleaf 内置工具对象（常用）
- `#dates`：日期处理（旧版）
- `#temporals`：Java 8 时间处理（推荐）
- `#strings`：字符串工具
- `#numbers`：数字格式化
- `#lists`：集合工具
- `#bools`：布尔工具

示例：
```html
<p th:text="${#strings.toUpperCase(name)}">NAME</p>
<p th:text="${#numbers.formatDecimal(price,1,2)}">0.00</p>
```

### 16.14 与 Spring Security 集成（常见场景）
引入 `thymeleaf-extras-springsecurity6` 后可在页面做权限控制：
```html
<div sec:authorize="isAuthenticated()">已登录用户可见</div>
<div sec:authorize="hasRole('ADMIN')">仅管理员可见</div>
```

### 16.15 前端静态资源与缓存策略
- CSS/JS/图片放 `static` 下
- 页面中资源路径统一用 `@{}`
- 生产环境可结合版本号/指纹（如 `app.js?v=1.0.3`）防缓存问题

### 16.16 常见错误与排查
1. `TemplateInputException`：模板文件不存在或路径错误
2. 返回视图 404：`return` 的视图名与模板目录不匹配
3. 表达式报错：变量名不一致，模型里没放数据
4. 页面中文乱码：编码配置不统一（UTF-8）
5. 静态资源 404：资源没放到 `static` 或路径写错
6. 表单回显失败：未使用 `th:object` + `th:field`

### 16.17 最佳实践（项目可落地）
- 控制器只做流程编排，页面展示逻辑留给模板
- 公共头部、菜单、脚部使用片段复用
- 页面文案走 i18n 配置，避免硬编码
- 尽量使用 `th:text`，少用 `th:utext`
- 开发环境关闭模板缓存，生产开启
- 复杂页面拆分模板，保持单页职责清晰

### 16.18 一句话总结（面试版）
- `Thymeleaf` 是 Spring 生态下主流服务端模板引擎，通过 `Model + 视图模板` 完成服务端渲染，语法清晰、与 Spring MVC/Boot 集成成本低，适合需要 SSR 页面的业务系统。


