# Spring MVC 学习笔记 (重构版)

本笔记旨在为初学者提供一份清晰、循序渐进的 Spring MVC 学习指南。

---

## 第一部分: Spring MVC 入门与核心

### 第 1 章: Spring MVC 简介

#### 1.1 Spring MVC 是什么
- `Spring MVC` 是 `Spring Framework` 中用于构建 Web 应用程序的核心模块。
- 它基于**模型-视图-控制器（Model-View-Controller, MVC）**设计模式，能帮助开发者将业务逻辑、数据和界面显示清晰地分离。
- 它是 Spring 全家桶生态的重要一环，与 `Spring Boot` 结合使用可极大提升开发效率。

#### 1.2 Spring 与 Spring Boot 的关系
- `Spring Framework`：是底层引擎，提供了 `IoC`、`AOP`、`MVC`、事务等基础能力。
- `Spring Boot`：是开发加速器，在 Spring 基础上实现了自动配置、Starter 依赖管理和内嵌服务器，让开发和部署变得极其简单。

一句话：**Boot 是“开发加速器”，Framework 是“底层引擎”。**

---

### 第 2 章: 第一个 Spring MVC 应用

让我们从一个最简单的 "Hello World" 开始，感受 Spring MVC 的魅力。

#### 2.1 核心注解
- `@RestController`：一个组合注解，相当于 `@Controller` + `@ResponseBody`。它告诉 Spring，这个类是一个控制器，并且所有方法的返回值都应直接作为 HTTP 响应体（通常是 JSON 或字符串），而不是视图名。
- `@GetMapping`：一个专门处理 HTTP GET 请求的注解，是 `@RequestMapping(method = RequestMethod.GET)` 的简写。

#### 2.2 代码示例
```java
@RestController // 标记这是一个 RESTful 控制器
@RequestMapping("/user") // 所有请求路径都以 /user 开头
public class UserController {

    @GetMapping("/hello") // 处理 GET /user/hello 请求
    public String hello() {
        return "Hello, Spring MVC!";
    }
}
```
- **启动应用**：在 Spring Boot 环境下，直接运行主程序。
- **访问**：在浏览器中打开 `http://localhost:8080/user/hello`，你将看到 "Hello, Spring MVC!"。

---

### 第 3 章: Spring MVC 工作流程详解

理解 `DispatcherServlet` 的工作流程是掌握 Spring MVC 的关键。

#### 3.1 核心组件
- `DispatcherServlet`：前端控制器，所有请求的入口，负责统一调度。
- `HandlerMapping`：处理器映射器，根据请求的 URL 找到对应的处理器（Controller 方法）。
- `HandlerAdapter`：处理器适配器，负责以一种统一的方式调用不同类型的处理器。
- `Handler`：处理器，即我们编写的 Controller 方法，负责实际的请求处理。
- `ModelAndView`：一个包含模型数据和视图信息的容器。
- `ViewResolver`：视图解析器，根据处理器返回的视图名解析成具体的视图对象。
- `View`：视图对象，负责渲染模型数据并生成最终的 HTML 响应。

#### 3.2 完整执行流程
1.  **请求到达**：用户发送请求，首先被 `DispatcherServlet` 捕获。
2.  **查找处理器**：`DispatcherServlet` 调用 `HandlerMapping`，根据请求 URL 找到对应的 `HandlerExecutionChain`（包含处理器和一系列拦截器）。
3.  **适配与执行**：`DispatcherServlet` 将 `HandlerExecutionChain` 交给 `HandlerAdapter`，由它来适配并执行真正的处理器（Controller 方法）。
4.  **处理并返回**：Controller 方法执行业务逻辑，处理完成后返回一个 `ModelAndView` 对象（或直接返回响应体）。
5.  **视图解析**：如果返回的是 `ModelAndView`，`DispatcherServlet` 会请求 `ViewResolver` 将逻辑视图名解析为具体的 `View` 对象。
6.  **渲染响应**：`View` 对象使用 `ModelAndView` 中的模型数据进行渲染，生成最终的 HTML 页面。
7.  **返回给用户**：`DispatcherServlet` 将渲染后的响应返回给浏览器。

一句话总结：**请求 → `DispatcherServlet` → `HandlerMapping` 找处理器 → `HandlerAdapter` 执行 → 返回 `ModelAndView` → `ViewResolver` 解析视图 → 渲染响应**

---

### 第 4 章: 常用注解速查

| 注解 | 作用 |
|---|---|
| `@Controller` | 标识一个类是 MVC 控制器，通常返回视图名。 |
| `@RestController` | `@Controller` + `@ResponseBody` 的组合，常用于写 RESTful 接口，返回 JSON/字符串。 |
| `@RequestMapping` | 映射请求路径，可用于类或方法上。 |
| `@GetMapping` | 专门映射 GET 请求。 |
| `@PostMapping` | 专门映射 POST 请求。 |
| `@PutMapping` | 专门映射 PUT 请求。 |
| `@DeleteMapping` | 专门映射 DELETE 请求。 |

---

## 第二部分: 请求与响应

### 第 5 章: 获取请求参数

Spring MVC 提供了多种注解，方便地从 HTTP 请求中提取数据。

#### 5.1 获取路径参数：`@PathVariable`
用于从 URL 路径中提取值。
```java
@GetMapping("/orders/{id}")
public String getById(@PathVariable Long id) {
    return "正在查询订单，ID为：" + id;
}
// 访问 /orders/123, id 的值就是 123
```

#### 5.2 获取查询参数：`@RequestParam`
用于获取 URL `?` 后面的参数。
```java
@GetMapping("/products")
public String list(@RequestParam(defaultValue = "1") int page,
                   @RequestParam(required = false) String keyword) {
    return "当前页码：" + page + ", 搜索关键词：" + keyword;
}
// 访问 /products?page=2&keyword=phone
```
- `value`: 参数名。
- `required`: 是否必需，默认为 `true`。
- `defaultValue`: 默认值，设置后 `required` 自动为 `false`。

#### 5.3 获取请求体数据：`@RequestBody`
常用于接收 POST 或 PUT 请求中的 JSON 数据，并自动将其转换为 Java 对象。
```java
@PostMapping("/users")
public String create(@RequestBody UserDTO user) {
    return "创建用户成功：" + user.getUsername();
}
```

#### 5.4 获取请求头和 Cookie
- `@RequestHeader`: 获取请求头信息。
- `@CookieValue`: 获取 Cookie 数据。

```java
@GetMapping("/info")
public String info(@RequestHeader("User-Agent") String userAgent,
                   @CookieValue(name = "JSESSIONID", required = false) String sessionId) {
    return "User-Agent: " + userAgent + "<br>Session ID: " + sessionId;
}
```

#### 5.5 POJO 自动封装
Spring MVC 支持将请求参数自动绑定到 POJO (Plain Old Java Object) 的属性上，要求参数名与属性名一致。
```java
public class QueryParams {
    private int page;
    private String keyword;
    // getters and setters...
}

@GetMapping("/search")
public String search(QueryParams params) {
    return "正在搜索第 " + params.getPage() + " 页，关键词是：" + params.getKeyword();
}
// 访问 /search?page=3&keyword=java
```

---

### 第 6 章: 域对象共享数据

在请求处理过程中，我们经常需要在不同组件之间传递数据。Spring MVC 提供了多种方式将数据放入 `request` 域。

#### 6.1 使用 `ModelAndView`
最经典的方式，同时包含数据和视图信息。
```java
@GetMapping("/welcome")
public ModelAndView welcome() {
    ModelAndView mav = new ModelAndView();
    mav.addObject("message", "欢迎使用 ModelAndView！");
    mav.setViewName("welcomePage"); // 对应 welcomePage.html
    return mav;
}
```

#### 6.2 使用 `Model`
一个更轻量级的接口，专注于传递数据。
```java
@GetMapping("/home")
public String home(Model model) {
    model.addAttribute("username", "LHR");
    return "homePage"; // 对应 homePage.html
}
```

#### 6.3 使用 `Map` 或 `ModelMap`
`Model`、`Map`、`ModelMap` 的作用类似，最终都会被 Spring MVC 处理。
```java
@GetMapping("/dashboard")
public String dashboard(Map<String, Object> map) {
    map.put("activeUsers", 150);
    return "dashboardPage";
}
```

#### 6.4 向 `session` 域共享数据
- **方式一：通过 `HttpSession` API**
```java
@GetMapping("/login")
public String login(HttpSession session) {
    session.setAttribute("currentUser", "admin");
    return "redirect:/profile";
}
```
- **方式二：使用 `@SessionAttributes` 注解**
在 Controller 类上声明需要存入 session 的模型属性名。
```java
@Controller
@SessionAttributes("currentUser")
public class ProfileController {
    // ...
}
```

---

### 第 7 章: 视图和数据返回

#### 7.1 转发 (Forward)
服务器内部跳转，浏览器地址栏不变，是一次请求。
```java
@GetMapping("/forward")
public String forward() {
    return "forward:/user/list";
}
```

#### 7.2 重定向 (Redirect)
让浏览器重新发送一个新请求，地址栏会改变，是两次请求。
```java
@PostMapping("/save")
public String save() {
    return "redirect:/user/success";
}
```

#### 7.3 区别总结
- **转发**：一次请求，地址栏不变，可共享 `request` 数据。
- **重定向**：两次请求，地址栏改变，不共享 `request` 数据。

#### 7.4 视图解析器配置
在 Spring Boot 中，视图解析器通常是自动配置的。例如，当你引入 Thymeleaf 的 starter 后，`ThymeleafViewResolver` 会被自动注册。
手动配置示例（传统项目）：
```java
@Bean
public InternalResourceViewResolver viewResolver() {
    InternalResourceViewResolver resolver = new InternalResourceViewResolver();
    resolver.setPrefix("/WEB-INF/views/");
    resolver.setSuffix(".jsp");
    return resolver;
}
```

---

## 第三部分: 视图技术

### 第 8 章: Thymeleaf 模板引擎

#### 8.1 Thymeleaf 是什么
- `Thymeleaf` 是 Java 服务端模板引擎，常与 `Spring MVC / Spring Boot` 搭配。
- 主要价值：将后端数据渲染到 HTML 页面，适合中后台系统、管理系统、服务端渲染页面。
- 特点：
  - 自然模板（HTML 可直接在浏览器打开查看静态效果）
  - 语法贴近 HTML 属性，不破坏标签结构
  - 与 Spring 表单、国际化、校验体系整合好

#### 8.2 Spring Boot 整合 Thymeleaf
1.  **依赖**
    ```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-thymeleaf</artifactId>
    </dependency>
    ```
2.  **默认约定**
    - 模板目录：`src/main/resources/templates/`
    - 静态资源目录：`src/main/resources/static/`
    - 默认后缀：`.html`
3.  **常见配置 (`application.yml`)**
    ```yml
    spring:
      thymeleaf:
        prefix: classpath:/templates/
        suffix: .html
        mode: HTML
        encoding: UTF-8
        cache: false # 开发时关闭缓存，方便调试
    ```

#### 8.3 基础语法
- **变量表达式**: `${...}`
  ```html
  <h1 th:text="${name}">默认名称</h1>
  ```
- **文本替换**: `th:text` (转义) 和 `th:utext` (不转义)
- **条件判断**: `th:if` / `th:unless`
  ```html
  <p th:if="${age >= 18}">已成年</p>
  ```
- **循环**: `th:each`
  ```html
  <ul>
    <li th:each="user : ${users}">
      <span th:text="${user.username}">name</span>
    </li>
  </ul>
  ```
- **链接表达式**: `@{...}`
  ```html
  <a th:href="@{/orders/{id}(id=${order.id})}">详情</a>
  ```

#### 8.4 片段复用 (Layout)
- **定义片段**: `th:fragment`
  ```html
  <!-- templates/common/header.html -->
  <div th:fragment="top(title)">
    <h2 th:text="${title}">标题</h2>
  </div>
  ```
- **引入片段**: `th:replace` 或 `th:insert`
  ```html
  <div th:replace="~{common/header :: top('用户中心')}"></div>
  ```

---

### 第 9 章: 静态资源处理

#### 9.1 问题背景
当 `DispatcherServlet` 的 `url-pattern` 配置为 `/` 时，它会拦截所有请求，包括对 CSS、JS、图片等静态资源的请求，导致 404。

#### 9.2 Spring Boot 的解决方案
Spring Boot 默认已经配置好了静态资源处理。你只需要将静态文件放在以下任意目录即可：
- `classpath:/static/` (最常用)
- `classpath:/public/`
- `classpath:/resources/`
- `classpath:/META-INF/resources/`

#### 9.3 手动配置（Java Config）
如果需要自定义，可以通过实现 `WebMvcConfigurer` 接口来配置。
```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    // 方法一：资源映射（推荐）
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/static/**") // 浏览器访问路径
                .addResourceLocations("classpath:/static/"); // 文件存放的物理/类路径
    }

    // 方法二：委托给默认 Servlet 处理
    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        configurer.enable();
    }
}
```

---

## 第四部分: Spring MVC 进阶

### 第 10 章: 拦截器 (Interceptor)

#### 10.1 拦截器是什么
- 拦截器是 Spring MVC 提供的机制，用于在请求处理的特定阶段（调用 Controller 方法之前、之后，或视图渲染之后）执行自定义逻辑。
- 常见场景：登录校验、权限检查、日志记录、性能监控。

#### 10.2 拦截器 vs 过滤器 (Filter)
| 特性 | 拦截器 (Interceptor) | 过滤器 (Filter) |
|---|---|---|
| 归属 | Spring MVC 框架 | Servlet 规范 |
| 拦截范围 | 仅限于 Controller 的方法 | 所有进入容器的请求 |
| 执行时机 | 在 `DispatcherServlet` 之后 | 在 `DispatcherServlet` 之前 |
| 访问 Spring 容器 | 可以，能直接注入 Bean | 不方便 |

#### 10.3 自定义拦截器
需要实现 `HandlerInterceptor` 接口。
```java
public class LoginInterceptor implements HandlerInterceptor {

    // 在 Controller 方法执行前调用
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        HttpSession session = request.getSession();
        if (session.getAttribute("user") == null) {
            response.sendRedirect("/login");
            return false; // 拦截，请求不再向下执行
        }
        return true; // 放行
    }

    // 在 Controller 方法执行后、视图渲染前调用
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        // 可以修改 ModelAndView
    }

    // 在整个请求完成，视图渲染后调用
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        // 常用于资源清理
    }
}
```

#### 10.4 注册拦截器
通过实现 `WebMvcConfigurer` 接口来注册。
```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LoginInterceptor())
                .addPathPatterns("/**") // 指定要拦截的路径
                .excludePathPatterns("/login", "/register", "/static/**"); // 指定要排除的路径
    }
}
```

---

### 第 11 章: 文件上传和下载

#### 11.1 文件上传
1.  **配置**: 在 `application.yml` 中开启 multipart 支持。
    ```yml
    spring:
      servlet:
        multipart:
          enabled: true
          max-file-size: 10MB
          max-request-size: 50MB
    ```
2.  **Controller**: 使用 `MultipartFile` 接收文件。
    ```java
    @PostMapping("/upload")
    public String upload(@RequestParam("file") MultipartFile file) throws IOException {
        if (file.isEmpty()) {
            return "文件为空";
        }
        String filename = file.getOriginalFilename();
        // 建议重命名文件，避免重名覆盖
        file.transferTo(new File("/uploads/" + filename));
        return "上传成功";
    }
    ```

#### 11.2 文件下载
使用 `ResponseEntity<Resource>` 返回文件资源。
```java
@GetMapping("/download/{filename}")
public ResponseEntity<Resource> download(@PathVariable String filename) throws IOException {
    Path path = Paths.get("/uploads/" + filename);
    Resource resource = new UrlResource(path.toUri());

    return ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename="" + filename + """)
            .body(resource);
}
```

---

### 第 12 章: 数据校验与格式化

#### 12.1 数据校验 (JSR-303)
1.  **添加依赖**: `spring-boot-starter-validation`。
2.  **在 DTO 中添加注解**:
    ```java
    public class UserDTO {
        @NotBlank(message = "用户名不能为空")
        private String username;

        @Email(message = "邮箱格式不正确")
        private String email;
    }
    ```
3.  **在 Controller 中开启校验**: 使用 `@Valid` 或 `@Validated` 注解。
    ```java
    @PostMapping("/register")
    public String register(@Valid @RequestBody UserDTO dto, BindingResult br) {
        if (br.hasErrors()) {
            // 获取第一个错误信息
            String msg = br.getFieldError().getDefaultMessage();
            return "参数校验失败：" + msg;
        }
        return "注册成功";
    }
    ```

#### 12.2 日期格式化
使用 `@DateTimeFormat` 注解。
```java
@GetMapping("/search")
public String search(@DateTimeFormat(pattern = "yyyy-MM-dd") Date startDate) {
    return "查询日期：" + startDate;
}
```

---

### 第 13 章: 统一异常处理

使用 `@RestControllerAdvice` + `@ExceptionHandler` 可以构建全局异常处理机制，让 Controller 代码更整洁。

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    // 处理所有未被捕获的异常
    @ExceptionHandler(Exception.class)
    public Result<String> handleException(Exception e) {
        // 实际项目中应记录日志
        return Result.error("服务器内部错误：" + e.getMessage());
    }

    // 处理自定义的业务异常
    @ExceptionHandler(BusinessException.class)
    public Result<String> handleBusinessException(BusinessException e) {
        return Result.error(e.getCode(), e.getMessage());
    }

    // 处理参数校验异常
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Result<String> handleValidException(MethodArgumentNotValidException e) {
        String msg = e.getBindingResult().getFieldError().getDefaultMessage();
        return Result.error("参数校验失败：" + msg);
    }
}
```

---

### 第 14 章: 跨域处理 (CORS)

#### 14.1 什么是跨域
浏览器出于安全考虑，限制脚本从一个源（协议、域名、端口）去请求另一个源的资源，这就是**同源策略**。违反同源策略的请求即为**跨域**。

#### 14.2 解决方案
- **方法一：`@CrossOrigin` 注解**
  在 Controller 或方法上添加，适合局部配置。
  ```java
  @RestController
  @CrossOrigin(origins = "http://localhost:3000")
  public class ApiController { ... }
  ```
- **方法二：全局配置（推荐）**
  通过实现 `WebMvcConfigurer` 接口进行全局配置，更灵活。
  ```java
  @Configuration
  public class CorsConfig implements WebMvcConfigurer {
      @Override
      public void addCorsMappings(CorsRegistry registry) {
          registry.addMapping("/**") // 对所有路径生效
                  .allowedOrigins("http://localhost:3000") // 允许的源
                  .allowedMethods("GET", "POST", "PUT", "DELETE") // 允许的方法
                  .allowCredentials(true) // 是否允许携带 cookie
                  .maxAge(3600); // 预检请求的有效期
      }
  }
  ```

---

## 第五部分: Spring 核心与传统配置

### 第 15 章: Spring 核心回顾 (IoC & AOP)

#### 15.1 IoC (控制反转) 与 DI (依赖注入)
- **IoC (Inversion of Control)**：一种设计思想。传统方式是对象自己 `new` 依赖，IoC 将“对象创建和依赖管理的控制权”从代码中移交给了外部容器（Spring 容器）。
- **DI (Dependency Injection)**：IoC 的一种实现方式。容器通过**注入**的方式，将一个对象所依赖的其他对象传递给它。常见注入方式有构造器注入、Setter 注入和字段注入。

#### 15.2 AOP (面向切面编程)
- **AOP (Aspect-Oriented Programming)**：一种编程范式，用于将散布在应用中多个模块的**横切关注点**（如日志、事务、权限）从业务逻辑中分离出来，形成可重用的“切面”。
- 核心术语：`Aspect` (切面), `JoinPoint` (连接点), `Pointcut` (切点), `Advice` (通知)。

---

### 第 16 章: 传统 `web.xml` 配置 (了解即可)

在 Spring Boot 普及之前，Java Web 项目依赖 `web.xml` 文件进行配置。了解它有助于理解 Spring MVC 的演进。

#### 16.1 `web.xml` 的作用
- `web.xml` 是 Java Web 项目的部署描述文件（Deployment Descriptor）。
- 核心用途：注册 `Servlet` / `Filter` / `Listener`，配置启动参数和 URL 映射规则。

#### 16.2 核心标签
- `<servlet>`: 定义一个 Servlet，包括它的名称和实现类。
- `<servlet-mapping>`: 将一个 URL 模式映射到一个已定义的 Servlet。
- `<init-param>`: 为 Servlet 提供初始化参数。
- `<load-on-startup>`: 指定 Servlet 在 Web 应用启动时被加载的顺序（值越小优先级越高）。

#### 16.3 典型 Spring MVC 配置
```xml
<web-app>
    <servlet>
        <servlet-name>springmvc</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <!-- 指定 Spring MVC 配置文件的位置 -->
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:springmvc.xml</param-value>
        </init-param>
        <!-- 容器启动时就加载该 Servlet -->
        <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>springmvc</servlet-name>
        <!-- 拦截除 JSP 外的所有请求 -->
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```
**注意**: 在现代 Spring Boot 项目中，`web.xml` 已被自动配置和 Java Config 完全替代。

---

## 第六部分: 总结

### 第 17 章: 面试题精选

1.  **Spring MVC 的执行流程是什么？**
    > 请求 → DispatcherServlet → HandlerMapping 找处理器 → HandlerAdapter 执行 → 返回 ModelAndView → ViewResolver 解析 → 渲染视图 → 响应。

2.  **`@Controller` 和 `@RestController` 有什么区别？**
    > `@Controller` 通常返回一个视图名，用于服务端渲染。`@RestController` 是 `@Controller` 和 `@ResponseBody` 的组合，默认返回 JSON 或字符串，用于构建 RESTful API。

3.  **拦截器 (Interceptor) 和过滤器 (Filter) 的区别？**
    > - **归属不同**：拦截器属于 Spring MVC，过滤器属于 Servlet 规范。
    > - **执行时机不同**：过滤器在 DispatcherServlet 之前执行，拦截器在之后。
    > - **拦截范围不同**：过滤器能拦截所有请求，而拦截器只作用于经过 DispatcherServlet 的请求。
    > - **访问容器不同**：拦截器可以方便地访问 Spring 容器中的 Bean，过滤器则不行。

4.  **`@RequestParam` 和 `@PathVariable` 的区别？**
    > - `@RequestParam` 用于获取查询参数（URL 中 `?` 后面的部分，如 `?id=1`）。
    > - `@PathVariable` 用于获取路径参数（URL 中占位符部分，如 `/users/1`）。

5.  **Spring 事务为什么有时会失效？**
    > - **方法可见性**：`@Transactional` 必须用在 `public` 方法上。
    > - **代理失效**：在同一个类中，一个非事务方法调用该类的另一个事务方法，会导致事务失效（因为绕过了代理）。
    > - **异常类型不匹配**：Spring 默认只对 `RuntimeException` 和 `Error` 回滚。如果方法抛出的是受检异常（Checked Exception），需要通过 `rollbackFor` 属性指定。

---

### 第 18 章: 最佳实践

1.  **Controller 职责单一**：只做参数接收、调用 Service、返回结果，保持轻量。
2.  **统一响应格式**：定义一个全局的 `Result` 类来包装所有 API 的返回数据，包含 code, message, data。
3.  **统一异常处理**：使用 `@RestControllerAdvice` 进行全局异常捕获，避免在 Controller 中写大量 `try-catch`。
4.  **参数校验**：在 Controller 入口处使用 JSR-303 注解进行参数校验，尽早发现问题。
5.  **遵循 RESTful 规范**：使用名词表示资源，用 HTTP 方法 (GET, POST, PUT, DELETE) 表示操作。
6.  **接口文档**：使用 Swagger / OpenAPI 自动生成并维护 API 文档。
7.  **API 版本控制**：在 URL 中加入版本号（如 `/api/v1/users`），方便未来升级。
