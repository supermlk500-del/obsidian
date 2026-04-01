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
### 13.5 获取请求参数方法
1. 通过`servletapi`获取
2. 通过控制器方法的形参获取
3. `@RequestParm`:是将请求参数和控制器方法的形参创建映射关系
4. `@RequestHeader`:将请求头信息和控制器方法的形参创建映射关系
5. `@CoookiesValue`:将`cooki`数据和控制器方法的形参创建映射关系
6. 通过`POJO`获取请求参数(实体类)
7. 这几个注解都是有三个参数`value`,`required`,`defaultvalue`
#### 实战建议
- 类上用 `@RequestMapping("/资源")`，方法上用 `@GetMapping/@PostMapping` 等细分注解。
- 纯接口项目优先 `@RestController`，避免每个方法都写 `@ResponseBody`。
- 如果看到“`@RestMapping`”说法，先确认对方实际指的是不是 `@RequestMapping`。

### 13.6 参数绑定和数据校验
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

### 13.7 异常处理（推荐统一处理）
- 使用 `@RestControllerAdvice + @ExceptionHandler` 统一返回错误信息。
- 好处：控制器更简洁，错误格式统一。

### 13.8 [域对象共享数据](域对象共享数据.md)
1. 使用`servletapi`向`requset`域对象共享数据
2. 使用`modelandview`向`request`域对象共享数据
3. 使用`model`向`request`域对象共享数据
4. 使用`map`向`request`域对象共享数据
5. 使用`modelmap`向`request`域对象共享数据
6. `model`,`modelmap`,`map`的关系
7. 向`session`域共享数据
8. 向`application`域共享数据

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

# 17 SpringMVC的视图
- 当工程引入`jstl`的依赖,转发视图会自动转换为`jstlView`
- 转发浏览器发送一次请求，另一次在服务器内部
- 重定向视图浏览器发送两次请求（地址栏路径发生变化）

---

## 22. 静态资源处理

### 22.1 问题背景
- `DispatcherServlet` 配置 `/` 会拦截静态资源（CSS/JS/图片）
- 需要配置静态资源放行

### 22.2 方法一：默认 Servlet 处理
```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        configurer.enable();
    }
}
```

### 22.3 方法二：资源映射（推荐）
```java
@Override
public void addResourceHandlers(ResourceHandlerRegistry registry) {
    registry.addResourceHandler("/static/**")
            .addResourceLocations("classpath:/static/");
}
```

### 22.4 Spring Boot 默认静态资源路径
- `classpath:/static/`
- `classpath:/public/`
- `classpath:/resources/`
- `classpath:/META-INF/resources/`

---

## 23. 类型转换器和格式化

### 23.1 内置类型转换
Spring MVC 自动转换基本类型：
```java
@GetMapping("/user")
public String get(@RequestParam Long id, @RequestParam int age) {
    // String 自动转为 Long 和 int
    return "ok";
}
```

### 23.2 日期格式化
```java
@GetMapping("/search")
public String search(@DateTimeFormat(pattern = "yyyy-MM-dd") Date startDate) {
    return "ok";
}
```

### 23.3 自定义类型转换器
```java
public class StringToUserConverter implements Converter<String, User> {
    @Override
    public User convert(String source) {
        // 自定义转换逻辑
        String[] parts = source.split(",");
        User user = new User();
        user.setId(Long.parseLong(parts[0]));
        user.setName(parts[1]);
        return user;
    }
}
```

注册转换器：
```java
@Override
public void addFormatters(FormatterRegistry registry) {
    registry.addConverter(new StringToUserConverter());
}
```

---

## 24. SpringMVC 执行流程详解（面试重点）

### 24.1 完整执行流程
1. 用户发送请求到 `DispatcherServlet`（前端控制器）
2. `DispatcherServlet` 调用 `HandlerMapping`（处理器映射器）查找 `Handler`
3. `HandlerMapping` 返回 `HandlerExecutionChain`（包含处理器和拦截器）
4. `DispatcherServlet` 调用 `HandlerAdapter`（处理器适配器）执行 `Handler`
5. `Handler` 执行完成返回 `ModelAndView`
6. `ViewResolver`（视图解析器）解析视图名称
7. `View` 渲染视图
8. 响应返回给用户

### 24.2 核心组件
- `DispatcherServlet`：前端控制器，统一调度
- `HandlerMapping`：根据 URL 找到处理器
- `HandlerAdapter`：适配不同类型的处理器
- `Handler`：实际处理请求的控制器方法
- `ViewResolver`：视图解析器
- `View`：视图对象

### 24.3 一句话总结
请求 → `DispatcherServlet` → `HandlerMapping` 找处理器 → `HandlerAdapter` 执行 → 返回 `ModelAndView` → `ViewResolver` 解析视图 → 渲染响应

---

## 25. 异常处理（统一异常处理）

### 25.1 局部异常处理
```java
@Controller
public class UserController {

    @ExceptionHandler(Exception.class)
    public String handleException(Exception e, Model model) {
        model.addAttribute("error", e.getMessage());
        return "error";
    }
}
```

### 25.2 全局异常处理（推荐）
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    public Result<String> handleException(Exception e) {
        return Result.error(e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Result<String> handleValidException(MethodArgumentNotValidException e) {
        String msg = e.getBindingResult().getFieldError().getDefaultMessage();
        return Result.error("参数校验失败：" + msg);
    }
}
```

### 25.3 自定义业务异常
```java
public class BusinessException extends RuntimeException {
    private int code;
    
    public BusinessException(int code, String message) {
        super(message);
        this.code = code;
    }
}
```

---

## 26. 数据校验（JSR-303/Hibernate Validator）

### 26.1 常用校验注解
- `@NotNull`：不能为 null
- `@NotEmpty`：不能为空（集合、字符串）
- `@NotBlank`：不能为空白（字符串）
- `@Size(min, max)`：长度范围
- `@Min` / `@Max`：数值范围
- `@Email`：邮箱格式
- `@Pattern(regexp)`：正则匹配

### 26.2 使用示例
```java
public class UserDTO {
    @NotBlank(message = "用户名不能为空")
    @Size(min = 3, max = 20, message = "用户名长度 3-20")
    private String username;

    @NotBlank(message = "密码不能为空")
    @Size(min = 6, message = "密码至少 6 位")
    private String password;

    @Email(message = "邮箱格式不正确")
    private String email;
}
```

### 26.3 Controller 中使用
```java
@PostMapping("/register")
public Result<String> register(@Valid @RequestBody UserDTO dto, BindingResult br) {
    if (br.hasErrors()) {
        String msg = br.getFieldError().getDefaultMessage();
        return Result.error(msg);
    }
    return Result.success("注册成功");
}
```

### 26.4 分组校验
```java
public interface Create {}
public interface Update {}

public class UserDTO {
    @NotNull(groups = Update.class)
    private Long id;

    @NotBlank(groups = {Create.class, Update.class})
    private String username;
}

@PostMapping("/save")
public String save(@Validated(Create.class) @RequestBody UserDTO dto) {
    return "ok";
}
```

---

## 27. HttpMessageConverter（消息转换器）

### 27.1 作用
- 负责 HTTP 请求体和响应体的序列化/反序列化
- `@RequestBody` 和 `@ResponseBody` 底层依赖它

### 27.2 常见转换器
- `StringHttpMessageConverter`：处理字符串
- `MappingJackson2HttpMessageConverter`：处理 JSON（依赖 Jackson）
- `FormHttpMessageConverter`：处理表单数据

### 27.3 自定义消息转换器
```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
        // 自定义 JSON 转换器
        MappingJackson2HttpMessageConverter converter = new MappingJackson2HttpMessageConverter();
        ObjectMapper mapper = new ObjectMapper();
        mapper.setDateFormat(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"));
        converter.setObjectMapper(mapper);
        converters.add(0, converter);
    }
}
```

---

## 28. 视图解析器配置

### 28.1 InternalResourceViewResolver（JSP）
```java
@Bean
public InternalResourceViewResolver viewResolver() {
    InternalResourceViewResolver resolver = new InternalResourceViewResolver();
    resolver.setPrefix("/WEB-INF/views/");
    resolver.setSuffix(".jsp");
    return resolver;
}
```

### 28.2 ThymeleafViewResolver（Thymeleaf）
Spring Boot 自动配置，手动配置示例：
```java
@Bean
public ThymeleafViewResolver thymeleafViewResolver(SpringTemplateEngine templateEngine) {
    ThymeleafViewResolver resolver = new ThymeleafViewResolver();
    resolver.setTemplateEngine(templateEngine);
    resolver.setCharacterEncoding("UTF-8");
    return resolver;
}
```

---

## 29. 重定向和转发

### 29.1 转发（Forward）
```java
@GetMapping("/forward")
public String forward() {
    return "forward:/user/list";  // 服务器内部跳转
}
```

### 29.2 重定向（Redirect）
```java
@GetMapping("/redirect")
public String redirect() {
    return "redirect:/user/list";  // 浏览器重新请求
}
```

### 29.3 区别总结
- 转发：一次请求，地址栏不变，可共享 request 数据
- 重定向：两次请求，地址栏改变，不共享 request 数据

---

## 30. 常见面试题总结

### 30.1 SpringMVC 执行流程？
请求 → DispatcherServlet → HandlerMapping 查找处理器 → HandlerAdapter 执行 → 返回 ModelAndView → ViewResolver 解析 → 渲染视图 → 响应

### 30.2 拦截器和过滤器的区别？
- 拦截器属于 Spring MVC，过滤器属于 Servlet
- 拦截器只拦截 Controller，过滤器拦截所有请求
- 拦截器可访问 Spring 容器，过滤器不方便

### 30.3 如何解决跨域问题？
- `@CrossOrigin` 注解
- 全局 CORS 配置
- 使用 CorsFilter

### 30.4 如何处理文件上传？
使用 `MultipartFile` 接收文件，配置文件大小限制

### 30.5 如何统一异常处理？
使用 `@RestControllerAdvice` + `@ExceptionHandler`

### 30.6 `@RequestParam` 和 `@PathVariable` 区别？
- `@RequestParam`：获取查询参数（?id=1）
- `@PathVariable`：获取路径参数（/user/1）

### 30.7 如何实现参数校验？
使用 `@Valid` 或 `@Validated` + JSR-303 注解

---

## 31. 最佳实践建议

1. **Controller 职责单一**：只做参数接收、调用 Service、返回结果
2. **统一响应格式**：使用 Result 包装返回数据
3. **统一异常处理**：使用全局异常处理器
4. **参数校验**：使用 JSR-303 注解校验
5. **RESTful 规范**：遵循 REST 设计原则
6. **日志记录**：使用 AOP 或拦截器记录请求日志
7. **接口文档**：使用 Swagger/Knife4j 生成文档
8. **版本控制**：API 加版本号（/api/v1/users）

---

## 32. Spring MVC 与 Spring Boot 对比

| 特性 | Spring MVC | Spring Boot |
|------|-----------|-------------|
| 配置方式 | XML 或 Java Config | 自动配置 |
| 启动方式 | 需要外部容器（Tomcat） | 内嵌容器 |
| 依赖管理 | 手动管理 | Starter 依赖 |
| 开发效率 | 较低 | 高 |
| 适用场景 | 传统项目 | 现代微服务 |

**总结**：Spring Boot 是 Spring MVC 的增强版，简化了配置和部署。

---

## 33. 补充：Spring MVC 注解速查表

| 注解 | 作用 |
|------|------|
| `@Controller` | 标识控制器 |
| `@RestController` | `@Controller` + `@ResponseBody` |
| `@RequestMapping` | 映射请求路径 |
| `@GetMapping` | GET 请求映射 |
| `@PostMapping` | POST 请求映射 |
| `@PutMapping` | PUT 请求映射 |
| `@DeleteMapping` | DELETE 请求映射 |
| `@RequestParam` | 获取请求参数 |
| `@PathVariable` | 获取路径变量 |
| `@RequestBody` | 接收请求体（JSON） |
| `@ResponseBody` | 返回响应体 |
| `@ModelAttribute` | 绑定模型属性 |
| `@SessionAttribute` | 获取 Session 属性 |
| `@CookieValue` | 获取 Cookie 值 |
| `@RequestHeader` | 获取请求头 |
| `@CrossOrigin` | 跨域配置 |
| `@ExceptionHandler` | 异常处理 |
| `@RestControllerAdvice` | 全局异常处理 |
| `@Valid` / `@Validated` | 参数校验 |

---

**笔记完成！涵盖 Spring MVC 核心知识点，适合面试和实战。**

---

## 19. 拦截器（Interceptor）（高频考点）

### 19.1 拦截器是什么
- 拦截器用于在请求处理前后执行自定义逻辑
- 常见场景：登录校验、权限检查、日志记录、性能监控

### 19.2 拦截器 vs 过滤器
| 特性 | 拦截器（Interceptor） | 过滤器（Filter） |
|------|---------------------|-----------------|
| 归属 | Spring MVC | Servlet 规范 |
| 拦截范围 | Controller 方法 | 所有请求 |
| 执行时机 | DispatcherServlet 之后 | DispatcherServlet 之前 |
| 访问 Spring 容器 | 可以 | 不方便 |

### 19.3 自定义拦截器
```java
public class LoginInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, 
                           HttpServletResponse response, 
                           Object handler) throws Exception {
        // 请求处理前执行
        HttpSession session = request.getSession();
        if (session.getAttribute("user") == null) {
            response.sendRedirect("/login");
            return false; // 拦截
        }
        return true; // 放行
    }

    @Override
    public void postHandle(HttpServletRequest request, 
                          HttpServletResponse response, 
                          Object handler, 
                          ModelAndView modelAndView) throws Exception {
        // Controller 方法执行后、视图渲染前执行
    }

    @Override
    public void afterCompletion(HttpServletRequest request, 
                               HttpServletResponse response, 
                               Object handler, 
                               Exception ex) throws Exception {
        // 视图渲染后执行（常用于资源清理）
    }
}
```

### 19.4 注册拦截器
```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LoginInterceptor())
                .addPathPatterns("/**")           // 拦截所有
                .excludePathPatterns("/login", "/static/**"); // 排除路径
    }
}
```

### 19.5 拦截器执行顺序
- 多个拦截器按注册顺序执行
- `preHandle`：顺序执行
- `postHandle` 和 `afterCompletion`：逆序执行

---

## 20. 文件上传下载（实际应用）

### 20.1 文件上传配置
```yml
spring:
  servlet:
    multipart:
      enabled: true
      max-file-size: 10MB
      max-request-size: 50MB
```

### 20.2 单文件上传
```java
@PostMapping("/upload")
public String upload(@RequestParam("file") MultipartFile file) throws IOException {
    if (file.isEmpty()) {
        return "文件为空";
    }
    
    String filename = file.getOriginalFilename();
    String path = "/uploads/" + filename;
    file.transferTo(new File(path));
    
    return "上传成功：" + filename;
}
```

### 20.3 多文件上传
```java
@PostMapping("/batch-upload")
public String batchUpload(@RequestParam("files") MultipartFile[] files) {
    for (MultipartFile file : files) {
        if (!file.isEmpty()) {
            // 保存文件
        }
    }
    return "批量上传成功";
}
```

### 20.4 文件下载
```java
@GetMapping("/download/{filename}")
public ResponseEntity<Resource> download(@PathVariable String filename) throws IOException {
    Path path = Paths.get("/uploads/" + filename);
    Resource resource = new UrlResource(path.toUri());
    
    return ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_DISPOSITION, 
                   "attachment; filename=\"" + filename + "\"")
            .body(resource);
}
```

### 20.5 文件上传最佳实践
- 校验文件类型和大小
- 重命名文件（UUID + 原扩展名）
- 分目录存储（按日期/用户）
- 大文件考虑分片上传
- 敏感文件做访问权限控制

---

## 21. 跨域处理（CORS）（前后端分离必备）

### 21.1 什么是跨域
- 浏览器同源策略限制：协议、域名、端口任一不同即为跨域
- 前后端分离项目常见问题

### 21.2 方法一：`@CrossOrigin` 注解
```java
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:3000")
public class ApiController {
    // ...
}
```

### 21.3 方法二：全局配置（推荐）
```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("http://localhost:3000")
                .allowedMethods("GET", "POST", "PUT", "DELETE")
                .allowedHeaders("*")
                .allowCredentials(true)
                .maxAge(3600);
    }
}
```

### 21.4 方法三：过滤器方式
```java
@Bean
public CorsFilter corsFilter() {
    CorsConfiguration config = new CorsConfiguration();
    config.addAllowedOrigin("*");
    config.addAllowedMethod("*");
    config.addAllowedHeader("*");
    
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", config);
    
    return new CorsFilter(source);
}
```


