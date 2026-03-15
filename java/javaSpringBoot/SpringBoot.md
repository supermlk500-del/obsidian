- `SpringBoot`是`spring`提供的一个子项目,用于快速构建`Spring`应用程序
- `springboot`起步依赖(Maven坐标)是,解决了起步依赖特别麻烦
```java
<dependency>
	<groupId>org.springframework.boot</graoupId>
	<artifactId>spring-boot-starter-web</artifactId>
</dependency>
```
- 内嵌的`Tomcat,Jetly`
- 外部化配置
- 不需要XML配置
```java
@SpringBootApplication  
public class LearnApplication {  
  
    public static void main(String[] args) {  
        SpringApplication.run(LearnApplication.class, args);  
    }  
  
}
```
- 这两个参数一个是当前字节码文件，一个是`main`方法的`args`

## 配置文件


