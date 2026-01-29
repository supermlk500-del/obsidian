```java
/**  
 * mybatis-plus逆向工程类  
 * ---兼容SpringBoot3.3  
 */package com.ai_platform.stuliu.model_backend.utils;  
  
  
import com.baomidou.mybatisplus.generator.FastAutoGenerator;  
import com.baomidou.mybatisplus.generator.config.rules.DbColumnType;  
import com.baomidou.mybatisplus.generator.engine.FreemarkerTemplateEngine;  
  
import java.sql.Types;  
  
public class ReverseEngineering {  
    public static void main(String[] args) {  
        // 生成的代码文件包输出根目录  
        String outPath = "D:/JavaProject2024/demo-springboot3/src/main/java";  
  
        // 数据库连接配置  
        String sqlUrl = "jdbc:mysql://127.0.0.1:3306/class2102db?serverTimezone=UTC&useSSL=false&useUnicode=true&characterEncoding=utf-8";  
        String sqlUserName = "root";  
        String sqlPassword = "root";  
  
        // 需要生成的数据表名,多表用逗号隔开（生成的代码会按此数据表字段进行生成对应文件）  
        String tables = "tb_user,tb_goods,userinfo";  
        /*  
         * 数据库配置  
         */        FastAutoGenerator fastAutoGenerator = FastAutoGenerator.create(sqlUrl, sqlUserName, sqlPassword);  
        /*  
         * 全局配置  
         */        fastAutoGenerator.globalConfig(builder -> {  
            builder.author("DRC")        // 设置作者  
                    .outputDir(outPath) //输出位置  
                    .disableOpenDir()     // 禁止自动打开输出目录  
                    .commentDate("yyyy-MM-dd HH:mm:dd");//注释日期  
        });  
        /*  
         * 数据库配置  
         * 兼容旧版本转换成Integer  
         */        fastAutoGenerator.dataSourceConfig(builder -> builder.typeConvertHandler((globalConfig, typeRegistry, metaInfo) -> {  
            int typeCode = metaInfo.getJdbcType().TYPE_CODE;  
            if (typeCode == Types.SMALLINT) {  
                // 自定义类型转换  
                return DbColumnType.INTEGER;  
            }  
            return typeRegistry.getColumnType(metaInfo);  
        }));  
        /*  
         * 包配置  
         */        fastAutoGenerator.packageConfig(builder -> {  
            builder.parent("com.chong.demospringboot3") // 设置父包名 - 生成文件夹的父文件（默认在根目录生成，java文件夹下的整个路径）  
                    .moduleName("")    // 设置父包模块名，添加后会在生成所有包都在这个父包下  
                    .entity("pojo")   //实体类包名(model.pojo,代表在pojo上面会再生成个父文件夹)  
                    .service("service")             // service 包名  
                    .serviceImpl("service.impl")    // impl 包名  
                    .mapper("mapper")               // mapper 包名  
                    .xml("mapperXml")               // Mapper XML 包名  
                    .controller("controller");    // Controller 包名（该生成后的必须与项目启动类Application.java路径同层）  
            // 注意：留意生成文件第一行代码（package com.chong.springboot.mapper;）路径是否正确，不正确的路径启动项目正常但是无法正常访问controller接口  
        });  
        /*  
         * 策略配置  
         * entityBuilder().naming: 默认下划线转驼峰命  
         * 重点注意：可以通过不同文件夹的策略配置设置enableFileOverride()确定是否覆盖原文件，防止自定义代码被覆盖  
         */        fastAutoGenerator.strategyConfig(builder -> {  
            // 设置需要生成的表名,多个表名用逗号隔开如："aa,bb"  
            builder.addInclude(tables)  
                    .entityBuilder()              // 【Entity 策略配置】  
                    .enableTableFieldAnnotation()//【Entity 策略配置】开启生成实体时生成字段注解  
                    .enableFileOverride()         // 【Entity 策略配置】 开启覆盖已生成文件  
                    .enableLombok()               // 【Entity 策略配置】 开启 lombok 模型  
                    .controllerBuilder()          // 【Controller 策略配置】  
                    .enableRestStyle()      // 【Controller 策略配置】开启@RestController注解  
//                  .enableFileOverride()      // 【Controller 策略配置】 开启覆盖已生成文件  
                    .mapperBuilder()              // 【mapper 策略配置】  
                    .enableMapperAnnotation()     // 【mapper 策略配置】 开启 @Mapper 注解  
//                  .serviceBuilder()             // 【service 策略配置】  
//                  .enableFileOverride()         // 【service 策略配置】 开启覆盖已生成文件  
            ;  
        });  
        /*  
         * 【生成代码模板】 使用Freemarker引擎模板，默认的是Velocity引擎模板  
         */        fastAutoGenerator.templateEngine(new FreemarkerTemplateEngine());  
        /*  
         * 运行生成  
         */        fastAutoGenerator.execute();  
  
    }  
      
}
```


![[逆向工程.png]]
![[逆向工程1.png]]![[mybatis-x.png]]