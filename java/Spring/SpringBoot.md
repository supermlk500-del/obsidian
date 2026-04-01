# Spring Boot 笔记

## 1. Spring Boot 是什么
- `Spring Boot` 是 `Spring` 生态中的子项目，用于**快速构建 Spring 应用**。
- 核心目标：减少配置成本，提升开发效率。

### 1.1 核心特性
- 起步依赖（Starter）
- 内嵌 Web 容器（如 `Tomcat`、`Jetty`）
- 外部化配置（`application.yml` / `application.properties`）
- 约定优于配置，减少/不需要 XML

### 1.2 常见起步依赖
```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

### 1.3 启动类
```java
@SpringBootApplication
public class LearnApplication {
    public static void main(String[] args) {
        SpringApplication.run(LearnApplication.class, args);
    }
}
```
- 参数 1：启动类字节码对象（`LearnApplication.class`）
- 参数 2：`main` 方法参数（`args`）

---

## 2. 配置文件（YAML）
- 常用格式：`application.yml`
- YAML 语法要点：`key:` 与 `value` 之间有空格

### 2.1 示例
```yml
email:
  user: 3210783832@qq.com
  code: 需要申请
  host: smtp.qq.com
  auth: true
```

> YAML 中可以表示对象、数组、嵌套结构。

### 2.2 读取配置的两种方式
1. `@Value("${键名}")`
   - 示例：`@Value("${email.user}")`
2. `@ConfigurationProperties(prefix = "前缀")`
   - 字段名应与配置项键名对应

```java
@ConfigurationProperties(prefix = "email")
public class EmailProperties {
}
```

---

## 3. 整合 MyBatis

### 3.1 不使用 Spring Boot 时
通常需要手动配置：
- `mybatis` 依赖
- `mybatis-spring` 整合依赖
- 核心 Bean：`SqlSessionFactoryBean`、`MapperScannerConfigurer`、`DataSource`

### 3.2 使用 Spring Boot 时
- 引入 MyBatis 对应 Starter（起步依赖）
- 在配置文件中写参数，Spring Boot 自动装配读取

---

## 4. Bean 扫描

### 4.1 不使用 Spring Boot 时
- XML 标签扫描
- 注解扫描

### 4.2 使用 Spring Boot 时
常见注解：
- `@SpringBootApplication`
- `@ComponentScan`

说明：
- `@SpringBootApplication` 默认扫描**启动类所在包及其子包**
- `@ComponentScan(basePackages = "...")` 可指定扫描路径

---

## 5. Bean 注册

### 5.1 组件注解注册（项目内类）
可将类注册到 IoC 容器：
- `@Component`
- `@Controller`
- `@Service`
- `@Repository`

### 5.2 `@Bean` 注册（第三方类）
对于无法修改源码的第三方类，使用 `@Bean` 方法注册。

```java
@SpringBootApplication
public class SpringBootApplication {
    public static void main(String[] args) {
        SpringApplication.run(SpringBootApplication.class, args);
    }

    @Bean
    public Resolver resolver() {
        return new Resolver();
    }
}
```

建议：
- 将 `@Bean` 方法集中在配置类中维护
- `@Bean` 方法参数可直接声明容器中已有 Bean，Spring 会自动注入

---

## 6. `@Import`
- `@Import` 可用于手动导入配置或组件。
- 可导入 `ImportSelector` 实现类。

基本流程：
1. 定义类实现 `ImportSelector`
2. 重写 `selectImports` 方法，返回要导入的全限定类名数组

---

## 7. 条件装配（Conditional）
- Spring 提供 `@Conditional` 及其衍生注解用于按条件注册 Bean。

常见衍生注解：
1. `@ConditionalOnProperty(prefix = "...", name = "...")`
   - 配置存在且满足条件时生效
2. `@ConditionalOnMissingBean`
   - 容器中不存在指定 Bean 时生效
3. `@ConditionalOnClass`
   - 类路径存在指定类时生效（如 `DispatcherServlet`）

---

## 8. 自动配置原理（入门理解）
- Spring Boot 遵循“约定优于配置”。
- 应用启动后，Starter 对应的自动配置类会按条件生效，将需要的 Bean 注册到 IoC 容器。
- `ApplicationContext` 是 Spring Framework 的容器核心，用于管理 Bean。

---

## 9. 易错点速记
- `groupId`、`artifactId` 拼写要准确
- `@ComponentScan`、`@Repository`、`@ConditionalOnMissingBean` 注意拼写
- `prefix` 不是 `profix`
- `selectImports` 不是 `selectimport`

