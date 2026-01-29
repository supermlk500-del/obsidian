# NotBlank 
## .`@NotBlank` 注解本身

- 这是 JSR 380（Java 参数校验规范）中的核心注解，专门用于**字符串类型**的字段 / 参数校验。
- 校验规则：被标注的字段必须满足两个条件 ——
    
    - 不能是 `null`（空对象）；
    - 去除首尾空格后，字符串长度必须大于 0（比如只填空格的 " " 也会校验失败）。
    
- 注意区分易混淆注解（帮你避坑）：
    - `@NotNull`：只校验不为 null，空字符串 ""或空格" " 会通过；
    - `@NotEmpty`：校验不为 null 且长度 > 0，但空格 " " 会通过；
    - `@NotBlank`：最严格，专门针对字符串，排除 null、空字符串、纯空格。
[[NotBlank.png]]


1. 使用MyBatisX生成代码
2. servrce层需要写接口。
3. 建立config包，创建密码封装类。这里需要添加依赖```
```pom
<!-- Spring Boot 3 对应的Spring Security Starter依赖 --> <dependency> <groupId>org.springframework.boot</groupId> <artifactId>spring-boot-starter-security</artifactId> </dependency>
```
4. 建立common包，这里存放全局统一响应类
5. 建立dto包，不同层之间安全传输数据的类[[DTO]]
6. 