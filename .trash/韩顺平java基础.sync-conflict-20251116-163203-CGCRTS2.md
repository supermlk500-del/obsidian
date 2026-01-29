# Java 基础语法与编译运行笔记

## 编译与运行规范

### 编译阶段
```java
// 设置编码为GBK进行编译
javac -encoding gbk HelloWorld.java

// 编译后生成字节码文件
// HelloWorld.java → HelloWorld.class
```

### 运行阶段
```java
// 正确方式：不添加.class后缀
java HelloWorld

// 错误方式：添加后缀会报错
java HelloWorld.class  // 报错：找不到或无法加载主类
```

## 文件类型说明
- **.java文件**：源代码文件
- **.class文件**：字节码文件（可执行文件）

## Java 基本语法规则

### 1. 大小写敏感
```java
// 正确
String name = "John";
// 错误
string name = "John";  // String ≠ string
```

### 2. 语句结束符
```java
// 每条语句必须以分号结束
System.out.println("Hello");
int number = 10;
```

### 3. 类定义规则
```java
// 一个源文件最多只能有一个public类
public class MainClass {  // public类
    public static void main(String[] args) {
        System.out.println("Main class");
    }
}

class SecondaryClass {    // 非public类
    public static void main(String[] args) {
        System.out.println("Secondary class main");
    }
}

class ThirdClass {        // 另一个非public类
    // 可以没有main方法
}
```

### 4. 文件名规则
```java
// 如果包含public类，文件名必须与public类名一致
// 文件必须命名为：MainClass.java
public class MainClass {
    // 类内容
}
```

## 转义字符

| 转义字符 | 功能说明 | 示例 | 输出结果 |
|---------|---------|------|---------|
| `\t` | 制表符（对齐） | `"A\tB"` | A    B |
| `\n` | 换行符 | `"Hello\nWorld"` | Hello<br>World |
| `\r` | 回车符 | `"Hello\rWorld"` | World |
| `\\` | 反斜杠 | `"C:\\Windows"` | C:\Windows |
| `\"` | 双引号 | `"\"Java\""` | "Java" |
| `\'` | 单引号 | `"\'A\'"` | 'A' |

### 转义字符示例
```java
public class EscapeCharacters {
    public static void main(String[] args) {
        // 表格输出示例
        System.out.println("书名\t作者\t价格\t销量");
        System.out.println("三国\t罗贯中\t120\t1000");
        
        // 路径输出
        System.out.println("文件路径：C:\\Program Files\\Java");
        
        // 引号输出
        System.out.println("他说：\"Java很有趣！\"");
    }
}
```

## 文档注释

### 文档注释格式
```java
/**
 * 类的功能描述
 * 
 * @author 作者姓名
 * @version 版本号
 * @date 创建日期
 */
public class DocumentationExample {
    /**
     * 方法的功能描述
     * 
     * @param parameter 参数说明
     * @return 返回值说明
     * @throws Exception 异常说明
     */
    public String exampleMethod(String parameter) {
        return "result";
    }
}
```

### 生成API文档
```bash
# 使用javadoc生成文档
javadoc -encoding utf-8 -d docs DocumentationExample.java
```

## DOS 常用命令

### 目录操作命令
```bash
# 查看当前目录
dir

# 切换磁盘
D:          # 切换到D盘

# 切换目录
cd folder              # 进入folder文件夹
cd ..                  # 返回上一级目录
cd \                   # 返回根目录

# 相对路径 vs 绝对路径
cd subfolder           # 相对路径：当前目录下的subfolder
cd D:\Java\projects    # 绝对路径：完整路径
```

### 文件操作命令
```bash
# 创建目录
mkdir folder_name

# 删除文件
del filename.java

# 删除目录
rmdir folder_name

# 清屏
cls

# 查看IP配置
ipconfig
```

## 完整的Java程序示例

```java
/**
 * 学生信息管理系统示例
 * 
 * @author 刘辉荣
 * @version 1.0
 * @date 2024-12-19
 */
public class StudentManager {
    /**
     * 主方法 - 程序入口
     * 
     * @param args 命令行参数
     */
    public static void main(String[] args) {
        // 显示学生信息表格
        displayStudentInfo();
        
        // 显示文件路径示例
        displayFilePath();
    }
    
    /**
     * 显示学生信息
     */
    public static void displayStudentInfo() {
        System.out.println("学号\t姓名\t年龄\t专业");
        System.out.println("001\t张三\t20\t计算机科学");
        System.out.println("002\t李四\t19\t软件工程");
        System.out.println("003\t王五\t21\t人工智能");
    }
    
    /**
     * 显示文件路径示例
     */
    public static void displayFilePath() {
        System.out.println("\n项目路径：");
        System.out.println("D:\\Projects\\Java\\StudentSystem");
        System.out.println("配置文件：config\\app.properties");
    }
}

// 辅助类 - 演示多类编译
class Utility {
    public static void helperMethod() {
        System.out.println("辅助方法");
    }
}
```

## 编译与执行步骤

1. **编写源代码**：创建 `StudentManager.java`
2. **编译程序**：
   ```bash
   javac -encoding utf-8 StudentManager.java
   ```
3. **查看生成文件**：
   - `StudentManager.class`
   - `Utility.class`
4. **运行程序**：
   ```bash
   java StudentManager
   ```

## 注意事项总结

1. **编码一致性**：编译时确保编码设置与源文件实际编码一致
2. **文件命名**：public类必须与文件名一致
3. **大小写敏感**：Java严格区分大小写
4. **语句结束**：每条语句必须以分号结束
5. **运行规范**：运行时不加 `.class` 后缀
6. **多类编译**：每个类都会生成独立的 `.class` 文件
7. **入口灵活**：main方法可以定义在非public类中
---
## + 号的使用规则

### 1. 数值加法
```java
System.out.println(100 + 98);        // 198
int a = 10 + 20;                     // 30
```

### 2. 字符串拼接
```java
System.out.println("结果是：" + 100);     // 结果是：100
System.out.println(100 + "是结果");       // 100是结果
```

### 3. 运算顺序
```java
System.out.println(100 + 3 + "hello");  // 103hello
System.out.println("hello" + 100 + 3);  // hello1003
System.out.println("总和：" + (100 + 200)); // 总和：300
```

## 数据类型

### 基本数据类型
- **数值型**：byte、short、int、long、float、double
- **字符型**：char
- **布尔型**：boolean

### 引用数据类型
- **类**：String、自定义类等
- **接口**
- **数组**

---
## 浮点数
=符号位+指数位+尾数位
1. 与整数类型类似，java浮点类型也有固定的范围和字段长度，不受具体os的影响
2. java浮点型常量默认为double型，声明float型常量，须后加 'f' 或者 'F'
3. 浮点型常量有两种表示形式：十进制和科学计数法
4. 通常形况下，应该使用double型，因为它比float更加精确
```java
float num = 1.1 ;//这样会有精度损失，程序编译报错
double num1 = 1.1;//这样不会报错
double num2 = .123//等价与0.123


double num3 = 2.7;
double num4 = 8.1 / 3;//结果num4输出的结果不是2.7，而是接近2.7的一个小数，就算是3.0也是一样的
//固当我们对运算结果是小数的进行相等判断时要注意
```
---

# Java API 笔记

## 什么是 Java API
- **API**：应用程序编程接口
- Java 提供的现成类库和工具集合
- 包含大量预定义的类、接口和方法
- 开发者直接调用，提高开发效率

## 主要 API 包分类

### 1. 核心语言包 (java.lang)
- **自动导入**，无需手动引入
- 包含基础类：Object、String、Math、System
- 包装类：Integer、Double、Boolean 等
- 线程相关：Thread、Runnable

### 2. 实用工具包 (java.util)
- 集合框架：List、Set、Map 及其实现类
- 日期时间：Date、Calendar（新版有 time 包）
- 随机数：Random
- 扫描器：Scanner

### 3. 输入输出包 (java.io)
- 文件操作：File 类
- 流处理：InputStream、OutputStream
- 读写器：Reader、Writer

### 4. 网络编程包 (java.net)
- URL 处理
- 套接字编程
- 网络连接

### 5. 图形界面包 (java.awt 和 javax.swing)
- AWT：抽象窗口工具包
- Swing：增强的图形组件

## API 文档结构
- **包概述**：包的功能介绍
- **类/接口列表**：包含的所有类型
- **字段摘要**：常量、变量说明
- **构造方法**：对象创建方式
- **方法摘要**：功能方法列表
- **详细说明**：参数、返回值、异常

## 学习重点

### 必须掌握的常用类
- **String**：字符串处理
- **Math**：数学运算
- **Arrays**：数组操作
- **ArrayList**：动态数组
- **HashMap**：键值对存储

### 文档查阅技巧
- 按包名查找相关功能
- 关注方法签名（返回值、参数）
- 注意异常说明
- 查看使用示例

### 版本特性
- Java 8：Lambda、Stream API
- Java 9：模块化系统
- Java 11：HTTP Client
- 持续关注新版本的新增 API

## 使用建议
1. **先查文档**：遇到问题先查看相关 API
2. **理解设计**：掌握常用类的设计思想
3. **实践应用**：通过实际项目熟悉 API 使用
4. **关注更新**：了解新版本的特性和改进

- ---
## 字符类型
1. 字符常量是用单引号括起来的单个字符
2. java中还允许使用转义字符 '\' 来将其后的字符转变为特殊字符型常量
3. 在java中char的本质是一个整数，在输出时，会按照对应的unicode字符
4. char类型是可以进行运算的相当于一个整数，因为它都有对应的unicode码
5. 注意即使是中文字符也有规定的unicode码
ASCII编码表，一个字节表示，128个字符，实际上一个字节可以表示256个字符
Unicode固定大小的编码，使用两个字节来表示字符，无论字母还是汉字都是2个字节，但是浪费空间
utf-8大小可变的编码，字母使用1个字节，汉字使用3个字节（可以堪称Unicode改进）
gbk可以表示汉字，范围广，字母用1个字节，一个汉字是2个字节
注：gbk能表示的汉字比utf-8少

## 布尔类型
不可以用0或非0的整数替代false和true
## 基本数据类型
当java程序在进行赋值或者运算时，精度小的类型自动转换为精度大的数据类型
大小排序
char->int->long->float->double
byte->short->int->long->float->double
## 引用数据类型
- 类
- 接口
- 数组
### 细节
1. 当有多种类型的数据混合运算时，系统首先自动将所有数据转换成容量大的数据类型，然后进行计算
2. 当我们把精度大的数据类型赋值给精度小的数据类型就会报错，反之就会自动类型转换
3. （byte，short）和char之间不会相互自动转换
4. byte，short，char三者可以计算，在计算时首先转换为int类型
5. 当把具体数（注意是一个数）赋值给byte时，先会判断数据是不是在byte范围内
```java
byte a1 = 2;
byte a2 = 3;
byte a3 = a1 + a2;//注意这样会报错
```
6. boolean不参与转换
7. 自动提升原则：表达式结果的类型自动提升为操作数中的最大类型
### 强制类型转换
自动类型的逆过程，将容量大的数据类型转换为容量小的数据类型，使用时要加上价值转换符 '()' 可能会造成精度降低或溢出
1. 强转符号只针对最近的操作数有效，往往会使用 小括号来提升优先级
2. char类型可以保存int的常量值，但不能保存int的变量值
3. byte，short，char类型在进行计算时，当作int类型处理
```java
char c1 = '男';
char c2 = '女';
System.out.println(c1 + c2);//这是输出的结果是int类型的整数
```
### 基本数据类型转为String类型
```java
int n1 = 100;
float f1 = 1.1F;
double d1 = 4.3;
boolean b1 = true;
String s1 = n1 + "";
String s2 = f1 + "";
String s3 = d1 + "";
String s4 = b1 + "";//转换为String类型字符串，注意后面必须加上双引号否则代码会报错
```
### String类型转为基本数据类型
通过基本类型的包装类调用parseXX方法即可
[[int 与 integer]]
```java
String s5 = "123";
int num1 = Integer.parseInt(s5);
double num2 = double.parseDouble(s5);
float num3 = float.parseFloat(s5);
//怎么把字符串转成字符char，其实就是得到字符串的第一个字符
System.out.println(s5.chatAt(0))//返回字符串的第一个字符
```
- 在将String类型转成基本数据类型时，要确保String类型能够转成有效的数据，比如我们可以把"123"转成一个整数，但是不能把"hello"转成一个整数
- 如果格式不正确，就会抛出异常，程序就会终止
# 运算符
### 算数运算符
| 运算符 | 运算 | 示例 | 结果 |
|--------|------|------|------|
| `+` | 正号 | `+7` | 7 |
| `-` | 负号 | `b=11; -b` | -11 |
| `+` | 加 | `9+9` | 18 |
| `-` | 减 | `10-8` | 2 |
| `*` | 乘 | `7*8` | 56 |
| `/` | 除 | `9/9` | 1 |
| `%` | 取模(取余) | `11%9` | 2 |
| `++` | 自增(前) | `a=2; b=++a` | `a=3; b=3` |
| `++` | 自增(后) | `a=2; b=a++` | `a=3; b=2` |
| `--` | 自减(前) | `a=2; b=--a` | `a=1; b=1` |
| `--` | 自减(后) | `a=2; b=a--` | `a=1; b=2` |
| `+` | 字符串相加 | `"He"+"llo"` | "Hello" |

```java
//%的本质就是一个公式：a % b = a - a / b * b
//比如 -10 % 3 => -10 -(-10) / 3 * 3 = 1
//10 % -3 => 10 - 10 / (-3) * (-3)
System.out.println(10 % 3);
System.out.println(-10 % 3);
System.out.printn(10 % -3);
System.out.println(-10 % -3);//输出-1

```
自增运算符
作为独立使用：前后++没有区别
作为表达使用：
前++：++i先自增后赋值。规则：会使用临时变量->i=i+1; temp=i;i=temp;
后++：i++先赋值后自增。规则：会使用临时变量->temp=i;i=i+1;i=temp；
```java
int i = 1;
i = i++;
System.out.println(i);//这里会输出1，而是不是2
```
### 关系运算符
| 运算符 | 运算 | 示例 | 结果 |
|--------|------|------|------|
| `==` | 相等于 | `4==3` | false |
| `!=` | 不等于 | `4!=3` | true |
| `<` | 小于 | `4<3` | false |
| `>` | 大于 | `4>3` | true |
| `<=` | 小于等于 | `4<=3` | false |
| `>=` | 大于等于 | `4>=3` | true |
| `instanceof` | 检查是否是类的对象 | `"Hello" instanceof String` | true |

### 逻辑运算符
| 运算符 | 名称 | 运算规则 | 示例 | 结果 |
|--------|------|----------|------|------|
| `&` | 逻辑与 | 两个操作数都为true时结果为true | `true & false` | false |
| `&&` | 短路与 | 两个操作数都为true时结果为true，如果第一个为false则不计算第二个 | `true && false` | false |
| `|` | 逻辑或 | 两个操作数有一个为true时结果为true | `true | false` | true |
| `||` | 短路或 | 两个操作数有一个为true时结果为true，如果第一个为true则不计算第二个 | `true || false` | true |
| `!` | 逻辑非 | 取反操作 | `!true` | false |
| `^` | 逻辑异或 | 两个操作数不同时结果为true | `true ^ false` | true |

1. a&b：&叫逻辑与：规则：当a和b同时为true，则结果为true否则为false
2. a&&b：&&叫短路与：规则：当a和b同时为true，则结果为true，否则为false
3. a|b：|叫逻辑或：规则：当a和b有一个为true，有一个为true，则结果为true，否则为false
4. a||b：||叫短路或：规则：当a和b有一个为true，则结果为true，否则为false
5. ！a：叫取反：或者非运算，当a为true，则返回false；或反之
6. a^ b:叫逻辑异或，当a和b不同时，则结果为true，否则为false

### 赋值运算符
| 运算符 | 描述 | 示例 | 等价于 |
|--------|------|------|--------|
| `=` | 简单赋值 | `int a = 10;` | - |
| `+=` | 加等于 | `a += b;` | `a = a + b;` |
| `-=` | 减等于 | `a -= b;` | `a = a - b;` |
| `*=` | 乘等于 | `a *= b;` | `a = a * b;` |
| `/=` | 除等于 | `a /= b;` | `a = a / b;` |
| `%=` | 模等于 | `a %= b;` | `a = a % b;` |

### 三元运算符
条件表达式?表达式1：表达式2；
如果条件表达式为true，运算后的结果是表达式1；或反之
1. 表达式1和表达式2要为可以赋给接收变量的类型
```java
int a = 3;
int b = 8;
int c = a > b ? 1.1 : 3.4;//会报错c为it类型，而表达式赋值为double类型
```
2. 本质是if--else语句

### 位运算符
| 运算符   | 描述    | 示例        | 结果  |     |     |
| ----- | ----- | --------- | --- | --- | --- |
| `&`   | 按位与   | `5 & 3`   | 1   |     |     |
| `     | `     | 按位或       | `5  | 3`  | 7   |
| `^`   | 按位异或  | `5 ^ 3`   | 6   |     |     |
| `~`   | 按位取反  | `~5`      | -6  |     |     |
| `<<`  | 左移    | `5 << 2`  | 20  |     |     |
| `>>`  | 右移    | `5 >> 2`  | 1   |     |     |
| `>>>` | 无符号右移 | `5 >>> 2` | 1   |     |     |

### 运算符优先级
| 优先级   | 运算符                                 | 结合性                             |      |      |
| ----- | ----------------------------------- | ------------------------------- | ---- | ---- |
| 1     | `()` `[]` `{}`                      | 从左向右                            |      |      |
| 2     | `!` `~` `++` `--`                   | 从右向左                            |      |      |
| 3     | `*` `/` `%`                         | 从左向右                            |      |      |
| 4     | `+` `-`                             | 从左向右                            |      |      |
| [[5（位运算）]] | `<<` `>>` `>>>`                     | 从左向右                            |      |      |
| 6     | `<` `<=` `>` `>=` `instanceof`      | 从左向右                            |      |      |
| 7     | `==` `!=`                           | 从左向右                            |      |      |
| 8     | `&`                                 | 从左向右                            |      |      |
| 9     | `^`                                 | 从左向右                            |      |      |
| 10    | `                                   | `                               | 从左向右 |      |
| 11    | `&&`                                | 从左向右                            |      |      |
| 12    | `                                   |                                 | `    | 从左向右 |
| 13    | `?:`                                | 从右向左                            |      |      |
| 14    | `=` `+=` `-=` `*=` `/=` `%=` `&=` ` | =` `^=` `~=` `<<=` `>>=` `>>>=` | 从右向左 |      |

### 标识符的命名规则和规范

1. java对各种变量、方法和类等命名时使用的字符序列为标识符
2. 凡是自己起的名字都叫标识符
命名规则
3. 由26个英文字母大小写，数字，$符号
4. 数字不能开头
5. 不可以使用关键字和保留字，但能包含关键字和保留字
6. java中严格区分大小写，长度无限制。
7. 标识符不能包含空格
命名规范
8. 包名：多单词组成时所有字母都小写
9. 类名、接口名：多单词组成时，所有单词的首字母都大写
10. 变量名、方法名：多单词组成时第一个单词的首字母小写，第二个单词开始每个单词首字母大写
11. 常量名：所有字母都大写。多单词时每个单词用下划线连接
### 键盘输入
Scanner类表示简单文本扫描器，在java.util内
（1） 导入该类所在的报
（2）创建Scanner对象，new创建一个对象
```java
import java.util.Scanner
...
Scanner scanner = new Scanner(System.in);
System.out.println("请输入名字");
String name = scanner.next();//接收用户的输入
System.out.println("请输入年龄");
int age = scanner.nextInt();
//读取字符
char ch = scanner.next().charAt(0);
```

# 进制
1. 二进制：0、1，满二进一，以0b或0B开头
2. 八进制：0-7，满八进一，以数字0开头
3. 十进制：0-9，满十进一
4. 十六进制：0-9及A(10)-F(15)，满十六进一，以0x或0X开头。A-F不区分大小写
### 进制的转换
- 二进制转十进制 ：从最低位开始，将每个位的数提取出来，乘以2的（位数-1）次方然后求和
- 八进制转十进制：从最低位子开始，将每个位的数提取出来，乘以8的（位数-1）次方然后求和
- 十六进制转十进制：从最低位子开始，将每个位的数提取出来，乘以16的（位数-1）次方然后求和
- 十进制转二进制：将该数不断除以2，知道商为0为止，然后将每步得到的余数倒过来
- 八进制转二进制：将该数不断除以8，知道商为0为止，然后将每步得到的余数倒过来
- 十六进制转二进制：将该数不断除以16，知道商为0为止，然后将每步得到的余数倒过来
- 二进制转八进制：从最低位开始，将二进制每三位一组，转成对应的八进制
- 二进制转十六进制：从最低位开始，将二进制每四位一组，转成对应的八进制
- 八进制转二进制：将八进制数每一位，转成对应的一个3位的二进制数即可
- 十六进制转二进制：将十六进制数每一位，转成对应的一个4位的二进制数即可
#### 位运算
java中有7个位运算符（&、|、^、~、>>、<<、>>>）
##### 运算规则
1. 按位与&：两位全为1，结果为1，否则为0
2. 按位或：两位有一个为1，结果为1，否则为0
3. 按位异^：两位一个为1，结果为1，否则为0
4. 按位取反~：0->1，1->0
```java
//先得到 2 的补码=> 2 的原码（三码合一）也就是00000000 00000000 00000000 00000010
//3 的补码同理
System.out.println(2&3);
//运算后结果是00000000 00000000 00000000 00000010 也就是2 
```

- ==先得到原码->反码->补码->操作->得到操作后的反码->再得到原码==
#### 原码，反码，补码
1. 二进制的最高位十符号位：0表示正数，1表示负数
2. 正数的原码、反码、补码都一样
3. 负数的反码=它的原码符号位不变，其他位取反
4. 负数的补码=它的反码+1，负数的反码=负数的补码-1
5. 0的反码、补码都是0
6. java中没有无符号数，java中的数都是由符号的
7. ==在计算机运算的时候，都是以补码的方式来运算的==
8. 当我们看运算结果的时候，要看它的原码

# 控制结构
## 顺序控制
- 程序从上到下逐行执行，中间没有判断和跳转
## 分支控制
1. **条件表达式**：必须是布尔类型（boolean）或返回布尔值的表达式
2. **代码块**：使用大括号 `{}` 包围，如果只有一条语句可以省略大括号
3. **执行流程**：从上到下依次判断条件，第一个为true的条件对应的代码块会被执行
4. **else匹配**：else总是与最近的if匹配
## 循环控制
### switch
[[switch语法]]

### for循环
```java
for(循环变量初始化; 循环条件; 循环变量迭代){
	循环语句;
}
```
1. 循环条件是返回一个布尔值的表达式
2. for循环中的循环变量初始换和循环变量迭代可以写在其他地方，但是分号不能省略
```java
for(;循环条件;;){
	循环条件;
	
}
```
### while
```java
while(循环条件){
	循环体;
	循环变量迭代;
}
```
1. 循环条件依旧返回boolean
2. 先判断后执行
### do..while循环
```java
do{
	循环体;
	循环变量迭代;
}while(循环条件);
```
1. do while是关键字
2. 先执行，后判断
3. while后面有一个分号

### 九九乘法表

```java
for(int i = 1;i <= 9;i++){  
    for(int j = 1;j <= i;j++){  
        System.out.print(i + "*" + j + "=" + (i * j) + "\t");  
    }  
    System.out.println( );  
}
```
### 金字塔
```java
for(int i = 1;i <= 5;i++){
	for(int k = 1;k <= 5 - i;k++){
		System.out.print(" ");
	}
	for(int j =1;j <= 2 * i - 1;j++){
		System.out.print("*");
	}
}
```
### 空心金字塔

```java
for(int i = 1;i <= 5;i++){
	for(int k = 1;k <= 5 - i;k++){
		System.out.print(" ");
	}
	for(int j =1;j <= 2 * i - 1;j++){
		if(j == 1 || j == 2 * i -1 ||i == 5){
			System.out.print("*");
		}else{
			System.out.print(" ");
		}
	}
}
```
## switch和if
- 如果判断的具体数值不多，而且符合byte，short，int，char，enum，String。虽然两个语句都可以使用，建议使用switch
- 其他情况：对区间判断，对结果为boolean类型判断，使用if，if的使用范围更广
## break
1. break语句出现在多层嵌套的语句块中时，可以通过标签指明要终止的时哪一层语句块
```java
lable1:
for(){
lable2
	for(){
		break lable2;
	}
}
```
```java
String name1 = "java";
String name2 = "javaxuexi"
//字符串比较
System.out.println(name2.equals(name1));//输出的是false
```
## continue
- 用于结束本次循环，继续执行下一次循环
- continue语句出现在多层嵌套的循环语句体中时，可以通过标签指明要跳过的是哪一层循环

## return
- 使用在方法，表示跳出所在的方法。如果写在main中就会退出程序
# 数组
- 数组可以存放多个同一类型的数据。是一种数据类型，是引用数据类型
## 数组的动态初始化
- 数据类型 数组名[] = new 数据类型[大小]
```java
int a[] = new int[5];//创建一个名字为a长度为5的int类型的数组
```
- 先声明数组：int a[]; 或者 int[] a;然后创建数组：数组名 = new 数据类型[大小]：a = new int[10];

```java
  int a[];//声明也可以int[] a; 内存中还没有分配空间
  a = new int[10];//分配内存空间，可以存放数据了
```
- 静态初始化：数据类型 数组名[] = {元素值······}
```java
int a[] = {1,2,3,4,5,6,7,8};
```
## 数组的引用
```java
a[0];//访问a数组的第一个元素
```
## 数组使用细节
1. 数组是多个相同类型数据的组合，实现对这些数据的同意管理
2. 数组中的元素可以是任何数据类型，包括基本类型和引用类型，但是不能混用
3. 数组创后，如果没有赋值，会有默认值
4. 使用数组的步骤 (1) 声明数组并开辟空间 (2) 给数组各个元素赋值 (3) 使用数组
5. 数组的下标是从0开始的
6. 数组下标必须在指定范围内使用，否则会报越界错误
7. 数组属于引用类型，数组型数据是对象
```java
char[] chars = new char[26];  
for(int i = 0;i < chars.length;i++){  
    chars[i] = (char)('A' + i);  
}  
for(int i = 0;i < chars.length;i++){  
    System.out.print(chars[i]);  
}
```
### 数组赋值机制
```java
//基本数据类型
int a = 10;
int b = a;
b = 20;
//b只拷贝值，且不影响a的值。而数组不一样
System.out.println("a=" + a);//这是a等于10
System.out.println("b=" + b);//这时b等于20
System.out.println("====================");
//数组不一样，数组在默认情况下是引用传递，赋的值是地址，赋值方式为引用传递
int[] arr1 = {1,2,3}
int[] arr2 = arr1;
arr[2] = 10;
for(int i = 0;i < arr1.length;i++){  
    System.out.println(arr1[i]);//会发现arr1[2]的值也发生了变化  
}
```
### 数组拷贝
```java
int[] arr1 = {10,12,13};
int arr2 = new int[arr1.length];//默认值为0
//使用for循环拷贝
```
### 数组反转
```java
//使用双指针
int[] arr = {1,2,3,4,5,6,7};  
int[] result = new int[arr.length];  
int start = 0;  
int end = arr.length - 1;  
while(start < end){  
    if(start < end ){  
        result[start]=arr[end];  
        result[end]=arr[start];  
        start+=1;  
        end-=1;  
    }else if(start == end){  
        result[start] = arr[start]; 
        break; 
    }else{  
        break;  
    }  
}  
for(int i = 0;i < result.length;i++){  
    System.out.println(result[i]);  
}
//直接交换
int[] arr = {1,2,3,4,5,6,7};  
for(int i = 0;i < arr.length;i++){
	int temp = arr[arr.length - 1 = arr[i];
	arr[arr.length - 1 - i] = arr[i];
	arr[i] = temp;
}
//
```
### 数组扩容
```java
//定义一个新数组，长度应该是数组.length+1
int[] arr = {1,2,3};
int[] arrNew = new int[arr.length + 1];
for(int i = 0;i < arr.length;i++){
	arrNew[i] = arr[i];
}
arrNew[arr.length - 1] = 4;
arr = arrNew;
```
### 数组的默认值

| 数据类型      | 默认值            | 示例                                                   |
| --------- | -------------- | ---------------------------------------------------- |
| `byte`    | `0`            | `byte[] arr = new byte[3];` → `[0, 0, 0]`            |
| `short`   | `0`            | `short[] arr = new short[2];` → `[0, 0]`             |
| `int`     | `0`            | `int[] arr = new int[3];` → `[0, 0, 0]`              |
| `long`    | `0L`           | `long[] arr = new long[2];` → `[0, 0]`               |
| `float`   | `0.0f`         | `float[] arr = new float[2];` → `[0.0, 0.0]`         |
| `double`  | `0.0d`         | `double[] arr = new double[3];` → `[0.0, 0.0, 0.0]`  |
| `char`    | `\u0000` (空字符) | `char[] arr = new char[2];` → `['\u0000', '\u0000']` |
| `boolean` | `false`        | `boolean[] arr = new boolean[2];` → `[false, false]` |
## 排序
### 冒泡排序
```java
int[] b = {33,2,55,4,66,67,56,32};  
for(int i = 0; i < b.length - 1; i++){  
    for(int j = 0; j < b.length - 1 - i; j++){  
        if(b[j] > b[j + 1]){  
            int temp = b[j];  
            b[j] = b[j + 1];  
            b[j + 1] = temp;  
        }  
    }  
}  
for(int i = 0; i < b.length; i++){  
    System.out.println(b[i]);  
}
```
- 还有其他排序方法快排等
### 查找
### 顺序查找
```java
略
```
## 二维数组
```java
int[][] arr = {{1,2,3},{1,2,4},{5,5,6}};
int arr[][] = new int[2][3];//两行三列，里面的一位数组依旧是引用传递
//先声明
int arr[][];
arr = new int[2][3];
//输出
for(int i = 0;i < arr.length;i++){//遍历二维数组的每一个一维数组元素
	for(int j = 0;arr[i].length;j++){//遍历二维数组中一维数组的每一个小元素
		System.out.print(arr[i][j]);//访问应该是 arr[i][j] 表示第i个一维数组的第j个元素
	}
	System.out.println();
}
```
- 注意二维数组的元素是一维数组的数量，而不是一维数组的小元素之和。
```java
//一维数组的元素数量不一样
int[][] arr = new int[3][];
for(int i = 0;i < arr.length;i++){
	//遍历arr每个一维数组，给每一个一维数组开空间。
	arr[i] = new int[i + 1];
	//遍历数组，赋值
	for(int j = 0;j < arr[i].length;j++){
		arr[i][j] = i + 1;
	}
	for(int i = 0;i < arr.length;i++){
		for(int j = 0;j < arr[i].length;j++){
			System.out.print(arr[i][j] + " ");
		}
	}
}
```
### 杨辉三角
```java
//第n行有n个元素
//每一行的第一个元素和最后一个元素都是1
//从第三行开始，对于非第一个元素和最后一个元素arr[i][j] = arr[i-1][j] + arr[i-1][j-1]
int[][] yangHui = new int[10][];//为yangHui二维数组开空间
for(int i = 0;i < yangHui.length;i++){//遍历yangHui的每一个元素
	yangHui[i] = new int[i+1];//给每一个一维数组开空间
	for(int j = 0;j < yangHui[i].length;j++){
		if(j == 0 || j == yangHui[i].length - 1){
			yangHui[i][j] = 1;
		}else{
			yangHui[i][j] = yangHui[i-1][j] + yangHui[i-1][j-1];
		}
	}
}
for(int j = 0;i < yangHui.length;i++){
	for(int j = 0;j < yangHui[i].length;j++){
		System.out.print(yangHui[i][j] + " ");
	}
	System.out.println();
}
```
### 二维数组使用细节
1. 一维数组的声明方式：int[] x 或者 int x[]
2. 二维数组的声明方式
```java
int[][] y 或者 int y[][]
```
3. 二维数组实际上是由多个一维数组组成的，它的各个一维数组的长度可以相同也可以不相同。
4. 在Java中，数组声明的方括号 `[]` 可以放在类型后面，也可以放在变量名后面。当使用逗号分隔多个变量时：
- `int[] a, b;` → `a` 和 `b` 都是一维数组
- `int a[], b;` → `a` 是一维数组，`b` 是普通int变量
- `int[] a, b[];` → `a` 是一维数组，`b` 是二维数组
- 数组的插入与扩容的代码
```java
int[] arr5 = {10, 12, 45, 90};  
Scanner scanner = new Scanner(System.in);  
int temp = scanner.nextInt();  
int[] arr6 = new int[arr5.length + 1];  
int insertIndex = arr5.length;  
for (int i = 0; i < arr5.length; i++) {  
    if (arr5[i] > temp) {  
        insertIndex = i;  
        break;  
    }  
}  
for (int i = 0; i < insertIndex; i++) {  
    arr6[i] = arr5[i];  
}  
arr6[insertIndex] = temp;   
for (int i = insertIndex; i < arr5.length; i++) {  
    arr6[i + 1] = arr5[i];  
}  
for (int i = 0; i < arr6.length; i++) {  
    System.out.print(arr6[i] + " ");  
}
```
# 面向对象
## 类与对象（oop编程）
### 介绍
1. 属性/成员变量
	- 从概念或叫法上看：成员变量 = 属性 = field字段 （即成员变量是用来表示属性的，统一叫属性）
2. 属性是类的一个组成部分，一般是基本数据类型，也可以是引用数据类型（对象，数组）。
	- 类就是数据类型
	- 对象就是一个具体的实例
```java
class Cat{
	String name;
	int age;
	String color;
}
```
- 使用
- 对象的属性默认值，遵守数组的规则（见841行）
```java
Cat cat1 = new Cat();//cat1的作用是指向对象空间/new Cat()才是对象，类似人名与人的关系
//对属性赋值
cat1.name = "小白";//使用 . 
cat1.age = 1;
cat1.color = "白色"
```
- 注意可以通过输出对象的hashCode来看对象是否是同一个
#### 创建
1. 先声明再创建
```java
Cat cat ;
cat = new Cat();
```
2. 直接创建
```java
Cat cat = new Cat();
```
### 对象再内存中的存在形式
```
Java内存结构：
┌─────────────────┐
│   方法区(Method Area)   │ ← 存储类信息、常量、静态变量
├─────────────────┤
│   堆(Heap)              │ ← 对象实例、数组（主要关注点）
├─────────────────┤
│   栈(Stack)             │ ← 局部变量、方法调用
├─────────────────┤
│   程序计数器(PC Register) │ ← 当前线程执行的指令地址
├─────────────────┤
│   本地方法栈(Native Method Stack) │ ← Native方法
└─────────────────┘
```
#### 具体内存情况
```java
Person p1 = new Person();//会在堆内存中开辟空间，这个空间内有默认属性值。其次站内存中的p1会指向空间
p1.age = 10;//找到空间，赋值
p1.name = "小明";//同理，此时要注意堆内存中的应该是地址，因为String是引用类型，在方法区内的，“小明”也就是在方法区内，而堆内存中的地址则指向方法区内的“小明”
Person p2 = p1;//这里的p2也是和p1指向同一地址空间
System.out.println(p2.age);
```
## 成员方法
- 成员方法是定义在类中、描述对象行为的函数，也称为实例方法。
```java
[访问修饰符] [返回类型] 方法名([参数列表]) {
    // 方法体
    [return 返回值;]
}
```
### [[方法调用机制]]
- 当程序执行到方法时，会在栈内开辟一个独立的栈空间
- 当方法执行完毕，或者执行到return语句时，就会返回
- 返回到调用方法的地方
- 返回后，继续执行后面的代码，方法开辟的独立的栈空间此时就被销毁
- 当main方法的栈空间执行完毕后，整个程序也就退出了

- 把输出的功能，写到一个类的方法中，然后调用该方法
### 细节
#### 返回类型
1. 一个 方法最多有一个返回值。想要返回多个可以使用数组
```java
public int[] getSumAndSub(int n1,int n2){
	int[] resArr = new int[2];
	resArr[0] = n1 + n2;
	resArr[1] = n1 - n2;
	return resArr;
}
```
2. 返回类型可以为任意类型，包含基本数据类型和引用数据类型（数组，对象）
3. 如果方法要求有返回数据类型，则方法体中最后的执行语句必须为 return 值；而且要求返回值类型必须和 return 的值类型一致或兼容
4. 如果方法是void，则方法体中可以没有return语句，或者只写return
#### 形参列表
1. 一个方法可以有0个参数，也可以有多个参数，中间好用逗号隔开
2. 参数类型可以为任意类型，包含基本类型和引用类型
3. 调用带参数的方法时，一定对应着参数列表传入相同类型或兼容类型的参数
4. 实参和形参的类型要一个或兼容、个数，顺序要一致
#### 方法调用说明
1. 同一个类中的方法调用：直接调用就行
2. 跨类中的方法A类调用B类方法：需要通过对象名调用
3. 跨类的方法和调用和方法的访问修饰符相关
#### 成员方法传参机制
1. 基本数据类型，传递的是值，形参的任何改变不影响实参
2. 引用数据类型，传递的是地址，指向了同一个对空间，所以形参的改变会影响实参。（类，接口，数组）。

#### 编写思路
1. 确定返回方法的类型
2. 名字
3. 方法的形参
4. 方法体+返回值

## 递归
- 递归就是方法自己调用自己，每次调用时传入不同的变量，递归有助于编程者解决复杂问题，同时可以让代码变得简洁
1. 执行一个方法时，就是创建一个新的手保护的独立空间（栈空间）
2. 方法的局部变量是独立的，不会相互影响
3. 如果方法中使用的是引用类型变量，就会共享该引用类型的数据
4. 递归必须向退出递归的条件逼近
5. 当一个方法执行完毕，或者遇到return，就会返回，遵守谁调用，就将结果返回给谁，同时当方法执行完毕或者返回时，该方法也就执行完毕
### 内存
- 每一次调用自己的时候会在栈中开辟一个空间
- 所以最后输出的时候是从最上面一个栈空间开始输出
- 每一次返回下一个空间的时候上面的栈都会销毁
- 只有当最上面一个栈空间的代码执行完了，才会执行下一个栈空间未执行的代码（不包括调用自己的代码，已经执行了）
- 返回的时候会返回到下一层调用的函数中

#### 走迷宫
1. 小球得到的路径，和程序员设置的找策略有关：找路的上下左右的顺序相关
2. 再得到小球路径时，看看路径是不是又变化
3. 回溯
##### 过程
1. 先创建迷宫，用二维数组表示
2. 先规定 map 数组的元素值：0 表示可以走 1 表示
```java
int [][] map = new int[8][7]
```
3. 将最上面一行和最下面一行全部设置为1
```java
for(int i = 0;i< 7;i++){
	map[0][i] = 1;
	map[7][i] = 1;
}
```
		输出当前的地图
```java
for(int i = 0;i < map.length;i++){
	for(int i = 0;i < map[i].length;i++){
		System.out.print(map[i][j] + " ");
	}
	System.out.println();
}

```
4. 将最右面一行和最左面一行全部设置为1
```java
for(int i = 0;i< 8;i++){
	map[i][0] = 1;
	map[i][6] = 1;
}
```
5. findway方法用来找出迷宫的路径
6. 找到就返回true，否则false
7. i，j 是老鼠的位置，初始化的位置为（1，1）
8. 因为是递归的找路，所以先规定 map数组的各个值得含义
		0 表示可以走 1 表示障碍物 2 表示可以走 3 表示走过，但表示走不通是死路
9. 当map 6]5] = 2 就说明找到通路，就可以救赎，否则就继续找\
10. 先确定老鼠找路得策略 下->右->上->左
```java
public boolean findWay(int[][] map,i,j){
	if(map[6][5]){
		return true;
	}else{
		if(map[i][j] == 0){//当前位置为0，说明表示可以走通
			map[i][j] = 2;//我们假定可以走通
			//使用找路策略，来确定该位置是否真的可以走通
			if(findWay(map,i + 1,j)){//向下走
				return true;
			}else if(findWay(map,i,j + 1)){//向右走
				return true;
			}else if(findWay(map,i - 1,j)){//向上走
				return true;
			}else if(findWay(map,i,j - 1)){//向左走
				return true;
			}else{
				map[i][j] = 3;
				return false;
			}
		}
	}
}
```

- 求出最短路径 
- 穷举
- 图 -> 求出最短路径。广度优先，深度优先等 

#### 汉诺塔
##### 过程
```java
public void move(int num,char a,char b,char c){
	//如果只有一个盘 num = 1
	if(num == 1){
		System.out.println(a + "->" + c);
	}else{
		//如果有多个盘，可以看成两个，最下面的和上面的所有盘(num - 1)
		//1. 先移动上面所有的盘到b，借助c
		move(num - 1,a,c,b);
		//2. 把最下面的盘，移动到c
		System.out.println(a + "->" + c);
		//3. 再把b塔的所有盘，移动到c，借助a
		move(num - 1,b,a,c);
	}
}
```

