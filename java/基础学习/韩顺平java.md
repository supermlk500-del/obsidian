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
| String    | null           | 略                                                    |
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
# 面向对象（初级）
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
- 注意引用类型String
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
#### 八皇后
##### 过程
```java

```

### 方法重载
- java中允许同一个类中，多个同名方法的存在，但要求形参列表不一致
	- 比如Systen.out.println()，可以输入不同类型的数据类型。这里就用到了方法的重载
```java
package calculate;  
  
import org.w3c.dom.ls.LSOutput;  
  
public class Overload01 {  
    public static void main(String[] args) {  
        MyCalculate mc = new MyCalculate();  
        System.out.println(mc.calculate(1,2));  
        System.out.println(mc.calculate(1,2,3));  
    }  
  
}  
class MyCalculate{  
    //这四个方法构成了重载  
    public int calculate(int n1,int n2){  
        return n1 + n2;  
    }  
    public double calculate(int n1,double n2){  
        return n1 + n2;  
    }  
    public  double calculate(double n1,int n2){  
        return n1 + n2;  
    }  
    public int calculate(int n1,int n2,int n3){  
        return n1 + n2 + n3;  
    }  
}
```

#### 细节
1. 方法名：一定相同
2. 形参列表：必须不同
3. 返回类型：无要求

### 可变参数
- 基本概念：java允许将同一个类中多个同名同功能但参数个数不同的方法，封装成一个方法
- 基本语法：访问修饰符 返回类型 方法名(数据类型  ... 形参名){}
```java
//可以使用方法重载但是比较繁琐，并且重复
class HspMethod{  
    public  int sum(int... nums){//int... 表示接收的是可变参数，类型是int；可以当作数组使用  
        System.out.println(nums.length);  
        //求和也是当作数组使用  
        int res = 0;  
        for(int i = 0;i < nums.length;i++){  
            res += nums[i];  
        }  
        return res;  
    }  
}
```


#### 细节
1. 可变参数的实参可以为0个或者任意多个
2. 可变参数的实参可以为数组
3. 可变参数的本质就是数组
4. 可变参数可以和普通类型的参数一起放在形参列表，但必须保证可变参数在最后
5. 一个形参列表中只能出现一个可变参数
##### 示例：
```java
  
class VarParamers{  
    public String showScore(String name,double... scores){  
        double totalScore = 0;  
        for(int i = 0;i < scores.length;i++){  
            totalScore += scores[1];  
        }  
        return name + scores.length + totalScore;  
    }  
}
```

### 作用域（scope）
1. 在java编程中，主要的变量就是属性（成员变量）和局部变量
2. 我们说的局部变量一般是指在成员方法中定义的变量
3. java中作用域的分类
	1. 全局变量：也就是属性，作用域为整个类体
	2. 局部变量：也就是属性，作用域为定义它的代码块中
4. 全局变量 (属性) 可以不赋值，直接使用，因为有默认值；局部变量必须赋值，它没有默认值 --- 对象的属性默认值，遵守数组的规则（见841行）

```java
class Cat{  
    //也就是属性，作用域为整个类体  
    int age = 10;  
  
    double weight;//默认值是0.0；  
    public void cry(){  
        //局部变量一般是指成员方法中定义的变量  
        // n 和 name 就是局部变量。这两个的作用域只能在cry中  
        int n = 10;  
        String name = "jack";  
        System.out.println(age);//全局变量可以在这里使用  
    }  
  
    public void eat(){  
        System.out.println(age);//全局变量可以在这里使用  
    }  
}
```
#### 细节
1. 属性和局部变量可以重名，访问时遵循就近原则
2. 在同一个作用域中，比如同一个成员方法中，两个局部变量，不能重名
3. 属性生命周期较长，伴随着对象的创建而创建，伴随着对象的死亡而死亡。局部变量，生命周期较短，伴随着它的代码块的执行而创建，伴随着代码块的结束而死亡
4. 全局变量：可以被本类使用，或其他类使用（通过对象调用）
5. 局部变量：只能在本类中对应的方法中使用
6. 全局变量/属性可以加修饰字符
7. 局部变量不可以加修饰字符
```java
class P{
	String name = "jack";
}'

class T{
	public void test(P p){
		System.out.print(p.name);
	}
}
```

### 构造器/构造方法
- 构造器的修饰符可以默认
- 构造器没有返回值
- 方法名和类名字必须一样
- 参数列表和成员方法一样的规则
- 构造器的调用由系统完成

```java
class Person{
	String name;
	int age;
	public Person(String name,int age){
		name = pName;
		age = pAge;
	}
}
public static void main(String[] args) {
	//调用
	Person p1 = new Person("smith",80);//调用并完成初始化
}
```

#### 细节
1. 一个类可以定义多个不同的构造器，即构造器重载；有时需要不同的信息，这是就可以重载构造器要达到要求。只需要年龄，或者名字，或者都需要
2. 构造器名要和类名相同
3. 构造器没有返回值
4. 构造器是完成对象的初始化，并不是创建对象
5. 在创建对象时，系统自动的调用该类的构造方法
6. 如果程序员没有定义构造方法，系统会自动给类生成一个默认无参构造方法
7. 一旦定义了自己的构造器，默认的构造器就会被覆盖，就不能再使用默认的无参构造器了，除非显式的定义一下

```java
class Dog{

	//定义自己的构造器,注意这时 Dog dog = new Dog()语句会报错
	public Dog(String name){
		//...
	}
	//默认会有无参构造器
	Dog(){
	}//显式的定义之后 Dog dog = new Dog()这样就不会报错
}
public static void main(String[] args) {
	//调用
	Dog dog = new Dog();//这里使用的是默认的无参构造器
}

```
#### 内存分析
```java
class Person{
	int age = 90;
	String name ;
	Person(String n,int a){
		name = n;
		age = a;
	}
}
Person p = new Person("peter",20);//分析如下
```
- 首先在方法区上加载person类，只会加载一次
- 在堆内存上开辟空间用来存放age和name并先默认初始化，然后显式初始化，就是看有没有指定值
- 现在构造器上场，将值赋值给属性
- 将在堆内存上开辟空间的地址赋值给 p。p是对象的引用，也叫对象名


### this关键字
- java虚拟机会给每个对象分配this，代表当前对象。this 就像 “我的” 的用法，不同的人用表示不同的意义
#### 内存分析
- this可以理解为在堆内存中存在的隐藏属性其表示地址指向自己
- 对象名和this的地址是一样的可以使用hashcode观察
#### this细节
1. this关键字可以用来访问本类的属性，方法，构造器
2. this用于区分当前类的属性和局部变量
3. 访问成员方法的语法：this.方法名(参数列表)
4. 访问构造器语法：this(参数列表); ==注意只能在构造器中使用==
5. this不能在类定义的外部使用，只能在类定义的方法中使用
```java
//调用
class T{
	String name;
	int age;
	public void f1(){
		System.out.println("f1被调用");
	}
	public void f2(){
		System.out.println("f2被调用");
		f1();
		this.f1();
		//这两种方法都可以调用f1
	}
	//在构造器中访问另一个构造器‘
	public T(){
		//访问构造器的语法一定要放在第一条语句
		this("jacl",100);//这样就访问到了构造器
		System.out.print("T() 构造器")；
		
	}
	public T(String name,int age){
		System.out.print("T(String name,int age)构造器");
	}
	public void f3(){
		String name = "simth";//一旦这里有一个name那么下面一条语句就访问不到类中的name
		System.out.println(name,age);//这里访问的name和age是按照就近原则访问的
		System.out.println(this.name,this.age);//这里明确的就是访问类的属性
	}
}
```

# 面向对象（中级）
## 包
### 包的作用（管理）
1. 区分相同名字的类
2. 当类很多时，可以很好的管理类
3. 控制访问范围
- 包的本质就是创建不同的文件来保存类文件
### 常用的包
- java.lang ：基本包，默认引入
- java.util：系统提供的工具包，工具类。使用Scanner
- java.net：网络包，网络开发
- java.awt：是做java的界面开发
### 包的导入
- import java.util.* ：表示所有类都导入。但是注意一般都是需要什么类就导入什么类，不建议使用*
### 包的注意事项和使用细节
1. package的作用就是声明当前类所在的包，需要放在类的最上面，一个类最多只有一句package
2. import指令，放在package的下面，再类定义前，可以有多句但是没有顺序要求
## 访问修饰符
- 基本。用于控制方法和属性的访问权限
	- 公开，用public修改，对外公开
	- 受保护：用protected修饰，对子类和同一个包中的类公开
	- 默认：没有修饰符号，向同一个包的类公开
	- 私有：用private修饰，只有类本身可以访问，不对外公开
#### Java 访问权限修饰符

| 修饰符    | 同类 | 同包 | 子类 | 不同包 | 说明                                     |
| :-------- | :--- | :--- | :--- | :----- | :--------------------------------------- |
| `public`    | ✔    | ✔    | ✔    | ✔      | **公开**，对所有类可见。                 |
| `protected` | ✔    | ✔    | ✔    | ✘      | **受保护**，对子类和同一个包中的类公开。 |
| `默认`      | ✔    | ✔    | ✘    | ✘      | **包级私有**，仅向同一个包的类公开。     |
| `private`   | ✔    | ✘    | ✘    | ✘      | **私有**，只有类本身可以访问。           |

**表格说明：**
*   **“默认”** 是指不书写任何修饰符（如 `int count;`）。
*   “子类”一列指的是，位于**不同包**中的子类是否可以访问。同包子类的访问权限遵循“同包”列的规则。
*   访问权限从宽到严依次为：`public` > `protected` > `默认` > `private`。
## 封装
- 介绍：就是把抽象数据和对数据的操作封装在一起，数据呗保护在内部，程序的其他部分只有通过被授权的操作，才能对数据进行操作
	- 隐藏实现细节
	- 可以对数据进行验证，保证安全合理
### 封装的实现步骤
1. 将属性进行私有化private
2. 提供一个公共的（public）set方法，用于对属性判断并赋值
3. 提供一个公共的（public）get方法，用于获取属性的值

## 继承

### 概念
继承是面向对象编程的三大特性之一（封装、继承、多态），它允许一个类（子类/派生类）继承另一个类（父类/基类）的属性和方法，并可以添加自己的新特性或修改继承的特性。

### 主要特性
1. **代码重用**：子类可以复用父类的代码，减少重复编写
2. **扩展性**：子类可以在父类基础上添加新的功能
3. **层次结构**：可以建立类的层次体系，反映现实世界的关系

### 继承类型
#### 单继承
- 一个子类只能有一个直接父类
- 大多数面向对象语言（如Java）支持单继承

#### 多继承
- 一个子类可以有多个直接父类
- C++支持多继承，Java通过接口实现类似功能

### 示例代码（Java）
```java
// 父类
class Animal {
    String name;
    
    public void eat() {
        System.out.println(name + "正在吃东西");
    }
}

// 子类继承父类
class Dog extends Animal {
    public void bark() {
        System.out.println(name + "汪汪叫");
    }
}

// 使用
public class Main {
    public static void main(String[] args) {
        Dog dog = new Dog();
        dog.name = "小黑";
        dog.eat();  // 继承自Animal的方法
        dog.bark(); // 自己的方法
    }
}
```

### 继承中的关键点
1. **super关键字**：用于访问父类的成员
   ```java
   class Cat extends Animal {
       public void display() {
           super.eat(); // 调用父类方法
       }
   }
   ```

2. **方法重写**：子类重新定义父类的方法
   ```java
   class Bird extends Animal {
       @Override
       public void eat() {
           System.out.println(name + "用嘴巴啄食");
       }
   }
   ```

3. **构造方法调用顺序**
   - 子类构造方法默认调用父类无参构造
   - 可以使用`super(参数)`显式调用父类有参构造

### 继承细节
1. 子类继承了所有的属性和方法，非私有的属性和方法可以再子类直接方法，但是私有属性和方法不能再子类直接访问，要父类提供公共的方法，公共的方法去访问
2. 子类必须调用父类的构造器，完成父类的初始化。（默认调用了super()）
3. 当创建子类对象时，不管使用子类的哪个构造器，默认情况下总会调用父类的无参构造器，如果父类没有提供无参构造器，则必须在子类的构造器中用super去指定使用父类的哪个构造器完成对父类的初始化工作，否则，编译不会通过[[继承构造器]]
4. 如果希望指定去调用父类的某个构造器，则显示的调用一下。如：super(对应的参数)
5. super在使用时，必须放在构造器第一行
6. super()和this()都只能放在构造器第一行，因此这两个方法不能共存在一个构造器
7. java所有类都是Object类的子类，Object是所有类的基类
8. 父类构造器的调用不限于直接父类，会一直往上追溯直到Object类
9. 子类最多只能继承一个父类（指直接继承），即java中是单继承机制
10. 不能滥用继承，子类和父类之间必须满足 is-a 的逻辑关系.（cat is a animal）

### 继承的本质
[[继承的本质]]

## super
[[super和this]] 的区别
### 介绍
- super代表父类的引用，用于访问父类的属性、方法、构造器
	- 访问父类的属性，但不能访问父类的private属性或方法
	- 访问父类的构造器

### 细节
1. 调用父类的构造器的好处（分工明确，父类的属性由父类初始化，子类的属性由子类初始化）
2. 当子类中有和父类中的成员（属性和方法）重命名时，为了访问父类的成员，可以通过super。如果没有重名，使用super，this，直接访问是一样的效果
3. super的访问不限于直接父类，如果爷爷类和本类中有同名的成员，也可以使用super去访问爷爷类的成员；如果多个基类中都有同名的成员，使用super访问遵循就近原则

## override
- 介绍：方法覆盖就是子类有一个方法，和父类的某个方法的名称、返回类型、参数一样那么我们就是说子类的这个方法覆盖了父类的方法
### 细节
1. 子类的方法的参数、方法名称，要和父类方法的参数、方法名称完全一样
2. 子类方法的返回类型和父类方法返回类型一样，或者父类返回类型的子类。比如父类返回类型是Object，子类方法返回类型是String--编译报错
3. 子类方法不能缩小父类方法的访问权限。访问权限从宽到严依次为：`public` > `protected` > `默认` > `private`
- 注意这里就可以引申出在父类中的方法输出内容时，子类方法重写可以通过super来引用父类中的方法，这样子类和父类中可以实现代码的复用性
## 多态

### 概念
多态是指同一个行为具有多个不同表现形式的能力。在面向对象编程中，多态允许使用父类引用指向子类对象，并根据实际对象类型调用相应的方法。

### 多态的具体体现
方法重载就体现了多态，同样的方法在传入不同的参数时有不同的使用效果。
方法重写也同样体现了多态

1. 一个对象的编译类型和运行类型可以不一样
2. 编译类型在定义对象时就确定了，不能改变
3. 运行类型是可以变化的
4. 编译类型看定义时=号的左边，运行类型看=号的右边（定义的时候决定了编译类型，运行类型在new的时候决定了运行类型）


### 多态的实现条件
1. **继承关系**：存在继承关系的类层次
2. **方法重写**：子类重写了父类的方法
3. **向上转型**：父类引用指向子类对象。比如：Animal animal = new Dog();

### 多态的类型
#### 编译时多态（静态多态）
- 通过方法重载实现
- 在编译时确定调用的方法

```java
class Calculator {
    // 方法重载
    public int add(int a, int b) {
        return a + b;
    }
    
    public double add(double a, double b) {
        return a + b;
    }
}
```

#### 运行时多态（动态多态）
- 通过方法重写和继承实现
- 在运行时确定调用的方法

```java
class Animal {
    public void makeSound() {
        System.out.println("动物发出声音");
    }
}

class Cat extends Animal {
    @Override
    public void makeSound() {
        System.out.println("喵喵喵");
    }
}

class Dog extends Animal {
    @Override
    public void makeSound() {
        System.out.println("汪汪汪");
    }
}

// 使用多态
public class Main {
    public static void main(String[] args) {
        Animal myAnimal;
        
        myAnimal = new Cat();
        myAnimal.makeSound(); // 输出：喵喵喵
        
        myAnimal = new Dog();
        myAnimal.makeSound(); // 输出：汪汪汪
    }
}
```

### 多态的优点
1. **可扩展性**：添加新类时无需修改现有代码
2. **代码简洁**：可以用统一的接口处理不同的对象
3. **降低耦合**：减少类之间的依赖关系

### 多态的应用
#### 1. 参数多态
```java
public class AnimalCare {
    // 参数类型为父类，可以接收任何子类对象
    public void careAnimal(Animal animal) {
        animal.eat();
        animal.makeSound();
    }
}
```

#### 2. 返回类型多态
```java
public class AnimalFactory {
    // 返回类型为父类，实际返回子类对象
    public Animal getAnimal(String type) {
        if ("cat".equals(type)) {
            return new Cat();
        } else if ("dog".equals(type)) {
            return new Dog();
        }
        return null;
    }
}
```

#### 3. 集合中的多态
```java
import java.util.ArrayList;
import java.util.List;

public class Zoo {
    public static void main(String[] args) {
        List<Animal> animals = new ArrayList<>();
        animals.add(new Cat());
        animals.add(new Dog());
        animals.add(new Bird());
        
        for (Animal animal : animals) {
            animal.makeSound(); // 每个动物调用自己的实现
        }
    }
}
```
#### 4.[[多态数组]]
##### 定义：数组的定义类型为父类类型，里面保存的实际元素类型为子类型

### 多态注意事项
1. **instanceof运算符**：用于判断对象的运行类型是否为XX类型或XX类型的子类型
   ```java
   if (animal instanceof Cat) {//返回的是boolean类型
       Cat cat = (Cat) animal; // 向下转型
       cat.catchMouse();
   }
   ```

2. **向下转型**：需要显式转换，并确保类型正确
	1. 语法：子类类型 引用名 = （子类类型）父类引用
	2. 只能强转父类的引用，不能强转父类的对象
	3. 要求父类的引用必须指向的是当前目标类型的对象
	4. 向下转型后，可以调用子类类型中所有的成员
   ```java
   Animal animal = new Cat();
   Cat cat = (Cat) animal; // 正确，animal和cat都指向同一块内存，这块内存是cat对象
   // Dog dog = (Dog) animal; // 错误：运行时ClassCastException，第三点
   ```

3. **抽象类和接口**：常用于实现多态
   ```java
   // 使用抽象类
   abstract class Shape {
       abstract double area();
   }
   
   class Circle extends Shape {
       @Override
       double area() { /* 实现 */ }
   }
   
   // 使用接口
   interface Flyable {
       void fly();
   }
   
   class Bird implements Flyable {
       @Override
       public void fly() { /* 实现 */ }
   }
   ```
3. 不能调用子类中特有的方法，在编译阶段能调用哪些成员是由编译类型决定的
4. 属性没有重写之说；属性的指看编译类型
```java

public class Zoo {
    public static void main(String[] args) {
	    //属性没有重写之说；属性的指看编译类型
        Base base = new Sub();
        base.count;//这里使用的是Base的count为10
    }
}

class Base {
	int count = 10;
}
class Sub extend Base{
	int count = 20;
}
```

### 继承与多态的关系
| 特性 | 继承 | 多态 |
|------|------|------|
| **核心概念** | 代码复用和扩展 | 同一接口不同实现 |
| **关系** | 多态的基础 | 继承的延伸和应用 |
| **实现方式** | extends关键字 | 方法重写 + 向上转型 |
| **编译时** | 确定继承关系 | 方法重载（静态多态） |
| **运行时** | - | 方法重写（动态多态） |

### 总结
继承建立了类之间的"is-a"关系（狗是动物），为代码重用和层次化组织提供了基础。多态则利用这种关系，使得程序可以以统一的方式处理不同的对象，提高了代码的灵活性和可维护性。两者结合使用，可以构建出结构清晰、易于扩展的面向对象系统。

## java的动态绑定机制

Java 的**动态绑定**（Dynamic Binding），也称为**运行时绑定**或**晚期绑定**（Late Binding），是 Java 实现**多态**（Polymorphism）的核心机制之一。它决定了在存在方法重写（Overriding）的情况下，**具体调用哪个类的方法实现**。
**动态绑定**是指：

> **在程序运行时**（而非编译时），根据对象的**实际类型**（运行类型）来决定调用哪个方法的实现。

这与**静态绑定**（如方法重载、private/static/final 方法）形成对比——静态绑定在编译期就确定了调用目标。

1. 当调用对象方法的时候，该方法会和该对象的内存地址/运行类型绑定
2. 当调用对象属性时，没有动态绑定机制，哪里声明，那里使用


```java
class Parent {
    int i = 10;

    int sum() {
        return i + 1;
    }

    int sum1() {
        return i + 2;
    }

    int getI() {
        return i;
    }
}

class Child extends Parent {
    int i = 20;  // 遮蔽（hides）父类的 i

    @Override
    int sum() {
        return i + 10;  // 使用子类的 i
    }

    @Override
    int sum1() {
        return i + 20;  // 使用子类的 i
    }

    @Override
    int getI() {
        return i;       // 返回子类的 i
    }
}

public class Test {
    public static void main(String[] args) {
        Parent p = new Child();  // 编译类型：Parent，运行类型：Child

        System.out.println(p.i);      // 输出：10（访问的是编译类型的字段）
        System.out.println(p.getI()); // 输出：20（动态绑定，调用子类方法）
        System.out.println(p.sum());  // 输出：30（20 + 10）
        System.out.println(p.sum1()); // 输出：40（20 + 20）
    }
}
```

## Object类

### equals方法
- 在 Java 中，`==` 与 `equals()` 都用于比较两个对象或值是否“相等”，但它们的含义和使用场景有本质区别：

---

### 1. `==` 运算符
- **作用**：比较两个操作数的**引用**（对于对象）或**值**（对于基本数据类型）。
- **对于基本数据类型**（如 `int`, `char`, `boolean` 等）：
  - 比较的是**实际的值**。
  ```java
  int a = 5;
  int b = 5;
  System.out.println(a == b); // true
  ```
- **对于引用类型**（如 `String`, 自定义类等）：
  - 比较的是**内存地址**，即是否指向同一个对象。
  ```java
  String s1 = new String("hello");
  String s2 = new String("hello");
  System.out.println(s1 == s2); // false（不同对象，地址不同）
  ```

---

### 2. `equals()` 方法
- **作用**：用于比较两个对象的**内容是否相等**（逻辑相等）。
- 默认情况下（来自 `Object` 类），`equals()` 的行为与 `==` 相同（比较引用）。
- **但很多类（如 `String`, `Integer`, `Date` 等）重写了 `equals()` 方法**，使其比较的是对象的内容。
  ```java
  String s1 = new String("hello");
  String s2 = new String("hello");
  System.out.println(s1.equals(s2)); // true（内容相同）
  ```

- **自定义类中**，如果需要按内容比较，应**重写 `equals()` 方法**（通常也要重写 `hashCode()`）。

---

### 对比总结

| 比较方式     | 基本类型         | 引用类型                     |
|--------------|------------------|------------------------------|
| `==`         | 比较值           | 比较引用（是否同一对象）     |
| `equals()`   | 不适用（编译错误）| 比较内容（若重写了 `equals`）|

> ⚠️ 注意：`equals()` 调用前应确保对象不为 `null`，否则会抛出 `NullPointerException`。

[[equals需要重写]]

---

### 示例
```java
String a = "hello";
String b = "hello";
String c = new String("hello");

System.out.println(a == b);        // true（字符串常量池）
System.out.println(a == c);        // false
System.out.println(a.equals(c));   // true
```

### [[hashcode方法]]
- 返回该对象的哈希码值
1. 提高具有哈希结构的容器的效率
2. 两个引用，如果指向的是同一个容器，则哈希值肯定是一样的
3. 两个引用，如果指向的是不同对象，则哈希值是不一样的
4. 哈希值主要根据地址来，但是不能完全讲哈希值等价与地址
5. 如果需要也需要重写
### [[tostring方法]]
- 返回该对象的字符表示



### finalize
- 当垃圾回收器确定不存在对该对象的更多引用时，由对象的垃圾回收期调用此方法
	1. 当对象杯回收时，系统自动调用该对象的finalize方法。子类可以重写此方法，做一些==释放资源==的操作
	2. 什么时候回收：当某个对象没有任何引用时，则jvm就认为这个对象是一个垃圾对象，就会使用垃圾回收机制来销毁该对象，在销毁该对象前，会先调用jinalize方法
	3. 垃圾回收机制的调用，是由系统来决定，也可以通过System.gc()主动触发垃圾回收机制·
- 在实际开发中，几乎不会运用finalize
## 断点调式
- 在断点调试过程中，是运行状态，是以对象的运行类型来执行
- 断点测试是指在程序的某一行设置一个断点，调试时，程序运行到这一行就会停住，然后可以一步一步运行，调试过程中可以看到各个变量当前的指
- 断点调试可以帮住外面查看java底层源代码的执行过程
- 快捷键
	1. F7：跳入方法内
	2. F8：逐行执行代码
	3. F9：resume，执行到下一个断点
	4. shift+F8：跳出方法
法

# 面向对象（高级）

## 类变量和类方法
在 Java 中，**类变量**和**类方法**是属于**类本身**的成员，而不是属于某个具体的对象（实例）。它们通过 `static` 关键字定义，因此也常被称为 **静态变量** 和 **静态方法**。

---

### 一、类变量（静态变量）
- **定义**：用 `static` 修饰的成员变量。
- **特点**：
  - 在**类加载时初始化**，**整个程序运行期间只有一份**。
  - 被**所有对象共享**，无论创建多少个对象，都共用同一个类变量。
  - 可以通过 **类名直接访问**（推荐），也可以通过对象访问（不推荐）。

#### 示例：
```java
class Student {
    static int totalStudents = 0; // 类变量：记录学生总数
    String name;

    public Student(String name) {
        this.name = name;
        totalStudents++; // 每创建一个学生，总数加1
    }
}

// 使用
Student s1 = new Student("Alice");
Student s2 = new Student("Bob");

System.out.println(Student.totalStudents); // 输出：2（推荐写法）
System.out.println(s1.totalStudents);      // 也能输出 2（但不推荐）
```

> ✅ **适用场景**：计数器、全局配置、工具类中的常量等。

#### 类变量的内存布局
[[类变量内存]]


---

### 二、类方法（静态方法）
- **定义**：用 `static` 修饰的成员方法。
- **特点**：
  - 属于类，**不依赖于任何对象**，可以在没有创建对象的情况下调用。
  - **不能直接访问非静态成员（实例变量/方法）**，因为它们属于具体对象。
  - 可以访问**静态变量**和其他**静态方法**。
  - 通常用于**工具方法**或**工厂方法**。

#### 示例：
```java
class MathUtils {
    public static int add(int a, int b) {
        return a + b;
    }

    public static void printMessage() {
        System.out.println("This is a static method.");
    }
}

// 使用（无需 new 对象！）
int sum = MathUtils.add(3, 5);
MathUtils.printMessage();
```

> ⚠️ **注意**：在静态方法中，**不能使用 `this` 或 `super`**，因为没有当前对象。

---

### 三、关键区别总结

| 特性   | 实例变量/方法     | 类变量/方法（static）    |
| ---- | ----------- | ----------------- |
| 所属   | 属于对象        | 属于类               |
| 内存   | 每个对象一份      | 整个 JVM 中只有一份      |
| 调用方式 | 必须通过对象调用    | 可通过类名直接调用         |
| 访问限制 | 可访问静态和非静态成员 | **只能访问静态成员**      |
| 生命周期 | 随对象创建/销毁    | 随类加载/卸载（通常贯穿程序运行） |

---

### 四、常见用途
- **类变量**：计数器（如用户总数）、全局配置（如数据库连接池大小）、常量（`public static final`）。
- **类方法**：
  - 工具方法（如 `Math.sqrt()`, `Integer.parseInt()`）
  - 工厂方法（如 `LocalDateTime.now()`）
  - 主方法 `public static void main(String[] args)`（JVM 启动入口）

---

### 五、注意事项
1. **不要滥用 `static`**：  
   过度使用会导致代码耦合度高、难以测试（尤其是静态状态）。
2. **线程安全问题**：  
   如果多个线程修改同一个类变量，需要考虑同步（如加 `synchronized`）。
3. **命名清晰**：  
   静态常量通常全大写，如 `public static final double PI = 3.14159;`
4. **类方法调用**：类名.类方法名 或者 对象名.类方法名【前提是满足访问修饰符的访问权限和范围】
5. **使用场景**： 当方法中不涉及任何对象相关的成员，则可以将方法设计成静态方法，提高开发效率。或者当外面希望不调用实例，也可以调用某一方法。比如：工具类Math，自定义工具类等 
6. **类方法和普通方法**：都是随着类的加载而加载，将结构信息存储在方法区：类方法中无this的参数，而普通方法中隐含着this的参数。普通方法需要创建对象才能调用
7. 类方法中只能访问静态变量或静态方法，普通方法都能访问

---

| 在 `static` 方法中 | 是否允许       |
| -------------- | ---------- |
| 访问 `static` 变量 | ✅ 是        |
| 调用 `static` 方法 | ✅ 是        |
| 定义/使用局部变量      | ✅ 是        |
| 直接访问实例变量       | ❌ 否（编译错误）  |
| 直接调用实例方法       | ❌ 否（编译错误）  |
| 通过对象访问实例成员     | ✅ 是（先创建对象） |

> ✅ **核心原则**：**静态上下文中没有 `this`，也没有隐式的当前对象。**


---

✅ **一句话记住**：  
> **`static` 成员属于类，不属于对象；它们在类加载时就存在，且所有对象共享。**
>  **实例变量必须是非`static`的**


## 深入理解main方法

- 形式 **public static void main(String[] args){}**
1. main方法是由虚拟机调用
2. java虚拟机需要调用类的main()方法，所以该方法的访问权限必须是public
3. java虚拟机在执行main()方法时不必创建对象，所以该方法时static
4. 该方法接收String类型的数组参数，该数组中保存执行java命令时传递给所运行的类的参数


`main` 方法中的 `args`（即 `String[] args`）是在 **Java 程序启动时由 JVM 传入的**，它的内容来自**命令行运行程序时附加的参数**。

---

### 一、`args` 是什么？
- `args` 是一个 **字符串数组（`String[]`）**，用于接收**命令行参数**。
- 它是 `main` 方法的**唯一合法参数形式**（也可以叫别的名字，但类型必须是 `String[]` 或 `String...`）。

```java
public static void main(String[] args) { ... }
```

---

### 二、什么时候传入？谁传入的？

✅ **传入时机**：  
当你在**命令行（或 IDE）运行 Java 程序时**，JVM 会把你在命令后写的参数**自动打包成字符串数组**，并传给 `main` 方法。

✅ **传入者**：  
**Java 虚拟机（JVM）** 在启动程序时完成这一操作。

---

### 三、如何传入？示例

#### 1. 命令行方式
假设你有一个类 `Hello.java`：

```java
// Hello.java
public class Hello {
    public static void main(String[] args) {
        for (int i = 0; i < args.length; i++) {
            System.out.println("参数 " + i + ": " + args[i]);
        }
    }
}
```

编译后，在终端运行：
```bash
javac Hello.java
java Hello Alice 25 "Java Programming"
```

输出：
```
参数 0: Alice
参数 1: 25
参数 2: Java Programming
```

> ✅ 这三个参数 `"Alice"`, `"25"`, `"Java Programming"` 就被 JVM 以字符串数组形式传给了 `args`。

#### 2. 在 IDE 中（如 IntelliJ IDEA / Eclipse）
- 运行配置（Run Configuration）中可以设置 **Program arguments**。
- 例如输入：`Alice 25 "Hello World"`
- 点击运行后，IDE 会把这些参数传递给 JVM，最终进入 `args`。

![[main传参.png]]

---

### 四、关键特点

| 特性 | 说明 |
|------|------|
| **类型固定** | 必须是 `String[]`（或 `String...` 可变参数） |
| **内容全是字符串** | 即使你输入数字 `123`，它也是字符串 `"123"`，需手动转为 `int` 等 |
| **空格分隔** | 默认用空格分隔参数（带空格的参数要用引号包裹） |
| **可为空** | 如果没传参数，`args` 是一个**长度为 0 的数组**（不是 `null`！） |

---

### 五、常见用途

1. **配置程序行为**
   ```java
   // 根据参数决定运行模式
   if (args.length > 0 && "debug".equals(args[0])) {
       enableDebugMode();
   }
   ```

2. **传入文件路径、用户名、端口号等**
   ```bash
   java ServerApp --port 8080 --host localhost
   ```

3. **自动化脚本调用**
   - Shell 脚本或批处理文件中动态传参给 Java 程序。

---

### 六、注意事项

- ❌ 不要假设 `args` 一定有值，**务必检查 `args.length`**。
- ✅ 参数顺序很重要，程序通常按位置解析。
- 🔒 敏感信息（如密码）不建议通过命令行传参（可能被 `ps` 命令看到），应使用配置文件或环境变量。

---

### 总结

> **`args` 是在你运行 `java YourClass arg1 arg2 ...` 时，由 JVM 自动将命令行参数封装成字符串数组，并传入 `main` 方法的。**

这是 Java 程序与外部环境（用户、脚本、系统）交互的最基础方式之一。如果你正在学习 Java 基础或开发命令行工具，掌握 `args` 非常重要！

## 代码块（block）
- 代码块又称为初始化块，属于类中的成员【即 是类的一部分】，类似与方法，将逻辑语句封装在方法体中，通过{}包围起来
- 但是和方法不同，没有方法名，没有参数，只有方法体，而且不用通过对象或类显示调用，而是加载类时，或创建对象时隐式调用
- 不管调用每一个构造器都会调用代码块
- 基本语法
```java
[修饰符]{
	代码
}
class movie{
	private String name;
	private double price;
	private String direction;
	//下面是一个两个三个参数的三个构造器
	{}
	{}
	{}
	//在每一次构造器执行的时候都可以自动调用到上面的代码块
}
```
1. 修饰符可选，也只能写static
2. 代码块分为两类，使用static修饰的叫静态方法，没有static修饰的，叫普通代码块/非静态代码块
3. 逻辑语句可以为任何逻辑语句
4. `;` 可以写上，也可以省略
### 好处
- 相当于另一种形式的构造器（对构造器的补充机制），可以做初始化的操作
- 如果多个代码构造器中都有重复的语句，可以抽取到初始化块中，提高代码的重用性
### 细节

1. static代码块页也叫静态代码块，作用就是对类进行初始化，而且它随着类的加载而执行，并且只会执行一次。如果是普通代码块，每创建一个对象，就执行
2. 类什么时候被加载
	1. 创建对象实例的时候
	2. 创建子类对象实例，父类也会被加载。父类先被加载，子类后被加载
	3. 使用类的静态成员时（静态属性，静态方法）
3. 普通的代码块，在创建对象实例时，会被隐式的调用。被创建一次，就被调用一次，如果只是使用类的静态成员时，普通代码块并不会执行
4. 创建一个对象，在一个类调用顺序是：
	1. 调用静态代码块和静态属性初始化（注意：静态代码块和静态属性初始化，则按他们定义的顺序调用）
	2. 调用普通代码块和普通属性的初始化（注意：普通代码块和普通属性初始化调用的优先级一样，如果有多个普通代码块和多个普通属性初始化，则按照定义的顺序调用）
	3. 调用构造方法
5. 构造方法的最前面其实隐含了super() 和 调用普通代码块的语句
6. 创建一个子类时（有继承关系），他们的静态代码块，静态属性初始化，普通代码块，普通属性初始化，构造方法的调用顺序：
	1. 父类的静态代码块和父类的静态属性
	2. 子类的静态代码块和静态属性 **第一点和第二点与类的加载有关**
	3. 父类的普通代码块和普通属性初始化
	4. 父类的构造方法
	5. 子类的普通代码块和普通属性初始化
	6. 子类的构造方法
7. 静态代码块只能直接调用静态成员，普通代码块可以调用任意成员


## 单例设计模式

- 设计模式是在大量的实践中总结和理论化之后优选的代码结构、编程风格，以及解决问题的思考方式。
- 类的单例设计模式，就是采取一定的方法保证在整个的软件系统中，对某个类只能存在一个对象实例，并且该类只提供一个取得其对象实例的方法
- 单例模式有两种方式：饿汉模式和懒汉式

### 单例模式应用实例
#### 饿汉式
1. 构造器私有化 。防止直接new对象
2. 类的内部创建对象
3. 向外暴露一个静态的公共方法

```java
public class Singleton {

    // ② 类的内部创建对象（静态的），一定需要一个静态的否则静态方法不调用
    private static Singleton instance = new Singleton();

    // ① 构造器私有化，防止外部 new
    private Singleton() {
        System.out.println("Singleton 构造器被调用");
    }

    // ③ 对外提供一个公共的静态方法
    public static Singleton getInstance() {
        return instance;
    }
}

public class TestSingleton {
    public static void main(String[] args) {

        Singleton s1 = Singleton.getInstance();
        Singleton s2 = Singleton.getInstance();

        System.out.println(s1 == s2); // true
    }
} // 输出的是 Singleton 构造器被调用 true

```

**饿汉式单例的最大不足：不管用不用，类一加载就创建对象，可能浪费资源。**

#### 懒汉式
**对象不是类加载时创建，而是在第一次真正需要时才创建。**
1. 构造器私有化
2. 定义一个ststic静态属性对象
3. 提供一个公共的public的static方法
4. 懒汉式只有当用户
```java
public class LazySingleton {

    // ② 先不创建对象
    private static LazySingleton instance;

    // ① 构造器私有化
    private LazySingleton() {
        System.out.println("LazySingleton 构造器被调用");
    }

    // ③ 对外提供静态方法，第一次调用才创建对象
    public static LazySingleton getInstance() {
        if (instance == null) {
            instance = new LazySingleton();
        }
        return instance;
    }
}
public class TestLazySingleton {
    public static void main(String[] args) {

        System.out.println("程序开始");

        LazySingleton s1 = LazySingleton.getInstance();
        LazySingleton s2 = LazySingleton.getInstance();

        System.out.println(s1 == s2); // true
    }
}
/*
结果：
程序开始
LazySingleton 构造器被调用
true
*/
```

**✅ 优点**

- 延迟加载（用到才创建）
    
- 不浪费资源
    

##### ❌ 致命问题：线程不安全

##### 多线程下可能发生什么？

`线程A：if (instance == null) → true 线程B：if (instance == null) → true  线程A：new LazySingleton() 线程B：new LazySingleton()`

👉 **创建了两个对象，单例被破坏**


`final` 关键字在 Java 中是非常常见的，它可以修饰 **变量**、**方法**、**类**，具有不同的含义。为了帮助你深入理解，我将从 **三个方面**详细说明 `final` 的用法和特点。

---

## 一、`final` 用法总结

### 1️⃣ `final` 修饰 **变量**：常量

- **定义常量**：一旦赋值就不能更改的变量。
    
- **特点**：
    
    - **基本数据类型**：值不可变
        
    - **引用数据类型**：引用地址不可变，但对象的内容可变
        

#### 示例

```java
public class FinalExample {
    public static void main(String[] args) {
        final int x = 10; // 常量
        // x = 20; // 错误：不能修改 final 变量的值

        final String str = "Hello";
        // str = "World"; // 错误：不能修改 final 引用的对象

        final Person person = new Person("Tom");
        person.name = "Jerry"; // 允许：对象内容可变
        // person = new Person("Jerry"); // 错误：引用不可变
    }
}

class Person {
    String name;

    public Person(String name) {
        this.name = name;
    }
}
```

---

### 2️⃣ `final` 修饰 **方法**：不能被重写

- **用于方法**：表示该方法不能被子类重写。
    
- **应用场景**：防止方法在子类中被修改，确保方法的行为不变。
    

#### 示例

```java
class Parent {
    public final void show() {
        System.out.println("Parent show method");
    }
}

class Child extends Parent {
    // public void show() { // 错误：无法重写 final 方法
    //     System.out.println("Child show method");
    // }
}
```

---

### 3️⃣ `final` 修饰 **类**：不能被继承

- **用于类**：表示该类不能被继承。
    
- **应用场景**：防止类被扩展，通常用于一些不希望被修改的类，比如 `String` 类。
    

#### 示例

```java
final class FinalClass {
    public void display() {
        System.out.println("This is a final class");
    }
}

class AnotherClass extends FinalClass { // 错误：无法继承 final 类
    // ...
}
```

---

## 二、`final` 修饰的详细解释

### 1️⃣ 修饰 **变量**

- **基本数据类型**：`final` 修饰的变量值不能改变。
    
- **引用数据类型**：`final` 使得引用变量指向的内存地址不能改变，但对象的内容是可以修改的。
    

#### 例子

```java
final int a = 10; // 基本数据类型，值不可变
// a = 20; // 错误，不能修改

final String[] arr = {1, 2, 3};
arr[0] = 10; // 允许修改数组的内容
// arr = new int[]{4, 5}; // 错误，不能修改引用地址
```

### 2️⃣ 修饰 **方法**

- 当方法声明为 `final` 时，该方法不能被子类重写。
    
- 这保证了方法的行为在继承关系中保持一致。
    

#### 例子

```java
class Animal {
    public final void eat() {
        System.out.println("Animal is eating");
    }
}

class Dog extends Animal {
    // public void eat() { // 错误，不能重写 final 方法
    //     System.out.println("Dog is eating");
    // }
}
```

### 3️⃣ 修饰 **类**

- `final` 修饰的类不能被继承，通常用于确保类的行为不被改变。
    
- `String` 类就是一个典型的例子，它被设计为 `final` 类，以防止字符串类被继承和修改。
    

#### 例子

```java
final class Car {
    public void drive() {
        System.out.println("Car is driving");
    }
}

class ElectricCar extends Car { // 错误：无法继承 final 类
    // ...
}
```

---

## 三、`final` 关键字的应用场景

### 1️⃣ 创建常量

`final` 最常见的用途之一是声明常量。通常，常量是用大写字母表示，并且值不会改变。

```java
public class Constants {
    public static final int MAX_VALUE = 100;
}
```

### 2️⃣ 用于方法优化

有时，编译器和 JVM 会对 `final` 修饰的变量和方法进行优化。例如，JVM 知道一个 `final` 变量不会被修改，因此可以更高效地处理它。

### 3️⃣ 防止类继承或方法重写

- `final` 类保证了类的设计不会被子类继承，确保其行为不被修改。
    
- `final` 方法确保了方法的实现不会被子类改变，适用于一些核心功能。
    

---

## 四、总结表格

|修饰对象|说明|示例|
|---|---|---|
|**变量**|值不可修改|`final int x = 10;`|
|**引用变量**|引用不可修改，内容可修改|`final String[] arr = {1, 2, 3};`|
|**方法**|不能被子类重写|`public final void show() { }`|
|**类**|不能被继承|`final class Car { }`|

---

## 五、细节
1. final修饰的属性又叫常量，一般用大写字母加下划线来命名
2. final修饰的属性在定义时，必须赋初值，并且以后不能再修改，赋值可以在如下位置
	1. 定义时
	2. 在构造器中
	3. 在代码块中
3. 如果final修饰的属性是静态的，则初始化的位置只能是
	1. 定义时
	2. 在静态代码块
	3. 不能再构造器中赋值
4. final类不能继承，但是可以实例化对象
5. 如果类不是final类，但是含有final方法，则该方法虽然不能重写，但是可以被继承
6. final不能修饰构造方法
7. final和static往往搭配使用，效率更高，不会导致类被加载
---

## [[抽象类]]（abstract）

- 当父类的某些方法，既需要声明，但是又不能去欸的那个如何实现时，可以将其声明为抽象方法，那么这个类就是抽象类
- 当一个类中存在一个抽象方法时，需要将该类声明为抽象类
- 一般来说，抽象类会被继承，有其子类来实现抽象方法


### 介绍
1. 用abstract修饰的类或方法就是抽象类或抽象方法
2. 抽象类的价值更多作用时在于设计，然后让子类继承并实现
### 注意
1. 抽象类不能被实例化
2. 抽象类不一定要有抽象方法
3. 一旦一个类包含了抽象方法，则这个类必须声明为抽象类
4. abstract只能修饰类和方法，不能修饰属性和其他
5. 抽象类可以有任意成员（本质还是类）
6. 抽象方法不能有主题
7. 如果一个类继承了抽象类，则它必须实现抽象类的所有抽象方法，除非它自己也声明为abstract
8. 抽象方法不能使用private、final、static来修饰，因为这些关键字都是和重写相违背的

### [[模板设计模式]]


## 接口（Interface）概述

- 接口就是**定义一组规范（方法声明）**
    
- 接口本身不关心实现细节
    
- 由实现类根据具体情况实现接口中的方法
    
- 接口体现的是 **“能做什么（can-do）”**
    

---

## 接口的基本语法

```java
interface Usb {
    void connect();
    void disconnect();
}
```

### 说明

- 接口使用 `interface` 关键字定义
    
- 方法**默认是 `public abstract`**
    
- 可以省略，但**本质一定存在**
    

---

## 接口的成员特点

### 方法特点

1. 接口中的方法默认是 `public abstract`
    
2. JDK8 之后：
    
    - 可以有 **default 方法**
        
    - 可以有 **static 方法**
        

```java
interface A {
    default void f1() {
        System.out.println("默认方法");
    }

    static void f2() {
        System.out.println("静态方法");
    }
}
```

---

### 属性特点

1. 接口中的属性**只能是常量**
    
2. 默认修饰符是：
    

```java
public static final
```

```java
interface B {
    int AGE = 18; // 等价于 public static final int AGE = 18;
}
```

3. 访问方式：
    

```java
接口名.属性名
```

---

## 接口的使用规则（细节）

1. 接口不能被实例化
    
2. 普通类实现接口，必须实现接口中**所有抽象方法**
    
3. 抽象类实现接口，可以不实现接口的方法
    
4. 一个类可以实现**多个接口**
    
5. 接口不能继承类，但可以继承**多个接口**
    
6. 接口修饰符只能是 `public` 或 默认
    

---

## 接口的多态特性

> **接口多态的本质：接口类型的引用，可以指向实现该接口的对象**

---

## 接口多态的三种表现形式

---

### 1️⃣ 参数多态

```java
interface Usb {
    void connect();
}

class Mouse implements Usb {
    public void connect() {
        System.out.println("鼠标连接");
    }
}

class Keyboard implements Usb {
    public void connect() {
        System.out.println("键盘连接");
    }
}

class Computer {
    public void work(Usb usb) {
        usb.connect();
    }
}
```

```java
Computer computer = new Computer();
computer.work(new Mouse());
computer.work(new Keyboard());
```

---

### 2️⃣ 多态数组（重点）

#### 概念

- 数组类型是接口类型
    
- 数组元素是接口的实现类对象
    

---

#### 示例

```java
Usb[] usbs = new Usb[2];

usbs[0] = new Mouse();
usbs[1] = new Keyboard();

for (Usb usb : usbs) {
    usb.connect();
}
```

---

### 3️⃣ 接口多态传递

```java
interface A {
    void f1();
}

interface B extends A {
    void f2();
}

class C implements B {
    public void f1() {}
    public void f2() {}
}
```

```java
A a = new C();
B b = new C();
```

---

## ⭐ 在多态数组中调用实现类“特有的方法”（重点难点）

### 问题描述

> 多态数组中，**编译类型是接口**  
> 如何调用**实现类自己特有的方法**？

---

### 示例准备

```java
interface Usb {
    void connect();
}

class Mouse implements Usb {
    public void connect() {
        System.out.println("鼠标连接");
    }

    public void click() {
        System.out.println("鼠标点击");
    }
}

class Keyboard implements Usb {
    public void connect() {
        System.out.println("键盘连接");
    }

    public void type() {
        System.out.println("键盘输入");
    }
}
```

---

### 多态数组

```java
Usb[] usbs = new Usb[2];
usbs[0] = new Mouse();
usbs[1] = new Keyboard();
```

---

### ❌ 错误写法（编译失败）

```java
usbs[0].click(); // ❌ 编译错误
```

👉 **原因**：  
编译类型是 `Usb`，接口中没有 `click()` 方法

---

### ✅ 正确写法：instanceof + 向下转型

```java
for (Usb usb : usbs) {
    usb.connect();

    if (usb instanceof Mouse) {
        Mouse mouse = (Mouse) usb;
        mouse.click();
    } else if (usb instanceof Keyboard) {
        Keyboard keyboard = (Keyboard) usb;
        keyboard.type();
    }
}
```

---

### 执行流程说明（非常重要）

1. `usb` 编译类型：`Usb`
    
2. `usb` 运行类型：`Mouse` 或 `Keyboard`
    
3. `instanceof` 判断**真实类型**
    
4. 向下转型后，才能调用特有方法
    

---

### instanceof 使用规则总结

1. 用于判断对象的**运行类型**
    
2. 返回 `boolean`
    
3. **向下转型前一定要先 instanceof 判断**
    
4. 否则可能抛出 `ClassCastException`
    

---

## 接口多态调用规则总结（必背）

1. **编译看左边（接口）**
    
2. **运行看右边（实现类）**
    
3. 调用特有方法：
    
    - 必须 **instanceof + 强制类型转换**
        

---

## 接口设计的核心思想

- 面向接口编程
    
- 降低耦合
    
- 提高扩展性
    
- 符合开闭原则（对扩展开放，对修改关闭）
    

---

## 一句话终极总结（直接写在笔记末尾）

> **接口多态数组中：  
> 能直接调用的是接口方法，  
> 想用实现类特有方法，必须 instanceof + 向下转型**

### [[实现接口和继承类区别与联系]]

 - 当子类继承了父类，就自动拥有了父类的功能
 - 如果子类需要扩展功能，可以通过实现接口的方式扩展！！


## 内部类

- 一个类的内部又完整的嵌套了另一个类结构。被嵌套的类称为内部类，嵌套其他类的类称为外部类。是我们类的第五大成员。内部类最大的特点就是可以直接访问私有属性，并且可以体现类与类之间的包含关系

**类的五大成员**：属性，方法，构造器，代码块，内部类。


- 基本语法
```java
class Outer{//外部类
	class Inner{//内部类
	
	}
}
class Other{//外部其他类
	
}
```

### 内部类（本质还是一个类）
#### 1. 定义在外部类的局部位置上（比如方法内）
#####  局部内部类（有类名）
1. 可以直接方法外部类的所有成员，包含私有的
2. 不能添加访问修饰符，但是可以用final修饰（加了final就不能被继承了）
3. 作用类：仅仅在定义它的方法或代码块中
4. 局部内部类可以直接访问外部类的成员
5. 外部类在方法中，可以创建内部类对象，然后调用方法
6. 如果外部类和局部内部类的成员重名时，默认遵循就近原则，如果想访问外部类的成员，则可以使用：`外部类名.this.成员`.
#####  匿名内部类（没有类名）
- 需求当一个类只能用到一次时单独创建一个类不划算，这时就可以使用匿名内部类
- 基本语法
	```java
	new 类或接口（参数列表）{
		类体
	}
	```
1. 基于接口的
	1. 本质是类
	2. 同时还是一个对象
	3. 没有名字
	4. jdk底层在创建匿名内部类 `类名$1(匿名内部类在使用时底层代码会给定义的名字)`，立即马上就创建了一个实例
	5. 只使用一次就不能再使用
```java
接口类 对象名 = new 接口类(){
	//重写接口方法的方法体
}
```
2. 基于类的
	1. 同时返回了匿名内部类的对象
	2. 运行类型变成了匿名内部类而不是等号左边的类！
```java
某类 对象名 = new 某某类("这里的形参列表会传递给某某类"){
	//类体
}
```
3. 还可以基于抽象类的匿名内部类
	1. 同理一定要实现其中的抽象方法

- [[匿名内部类调用细节]]
	- 匿名内部类既是一个类的定义，同时它本身也是一个对象，因此从语法上看，它既有定义类的特征，也有创建对象的特征，


####  定义在外部类的成员位置上
#####  成员内部类（没用static修饰）
- 成员内部类是定义再外部类的成员位置，并且没有static修饰
	1. 可以直接访问外部类的所有成员，包含私有方法
	2. 可以添加任意访问修饰符，因为它的地位就是一个成员
```java
	   class A{
	   
		   class B{
			   
		   }
		   
		   public void C(){
			   B b = new B();
			   
		   }
	   }
```
	3. 作用域和外部类的其他成员一样，为整个类体，比如再外部类的成员方法中创建内部类对象，再调用哦那个方法  
	4. 成员内部类访问外部类：直接访问就行
	5. 外部类访问成员内部类：创建对象再访问
	6. 外部其他类访问成员内部类
```java
//第一种
A.B b = newB();
//第二种：再外部类中，编写一个方法，可以返回对象
```
##### 静态内部类（使用static修饰）
- 静态内部类是定义再外部类的成员位置，并且又static修饰
	1. 可以直接访问外部类的所有静态成员，包含私有的，但不能直接访问非静态成员
	2. 可以添加任意访问修饰符，它的地位就是一个成员
	3. 作用域：同其他成员，为整个类体
	4. 静态内部类访问外部类：直接访问所有静态成员
	5. 外部类访问静态内部类：创建对象再访问
	6. 外部其他类访问静态内部类（前提需要满足访问权限问题）
```java
//同成员内部类
```

# 枚举和注解

## 枚举
### 自定义枚举类（不用 enum 关键字）

- 如果一个类我们希望只有几个固定的值，但是正常使用设计类时，会发现不合适了。此时**枚举类**就出现了
- 把具体的对象一个一个列举出来


1. 构造器私有化
2. 去掉setXxx方法，防止属性被修改
3. 再类内部直接创建固定的对象
4. 可以加入final修饰符
### 目标

- 星期只能是：周一 ~ 周日
    
- 不能随便 new
    
- 不能被修改
    

---

### 示例代码（一步到位）

```java
class Week {

    // 1. 属性
    private String name;

    // 2. 构造器私有化（外部不能 new）
    private Week(String name) {
        this.name = name;
    }

    // 3. 在类内部创建固定对象
    public static final Week MONDAY = new Week("星期一");
    public static final Week TUESDAY = new Week("星期二");
    public static final Week WEDNESDAY = new Week("星期三");
    public static final Week THURSDAY = new Week("星期四");
    public static final Week FRIDAY = new Week("星期五");
    public static final Week SATURDAY = new Week("星期六");
    public static final Week SUNDAY = new Week("星期日");

    // 4. 只提供 getter，不提供 setter
    public String getName() {
        return name;
    }
}
```

---

### 使用

```java
public class Test {
    public static void main(String[] args) {
        Week today = Week.MONDAY;
        System.out.println(today.getName());
    }
}
```

### 输出

```
星期一
```

---

### 你这段代码做到了什么？

✔ 构造器私有化  
✔ 去掉 set 方法  
✔ 对象固定、不可随意创建  
✔ `final + static` 保证常量唯一

👉 **这就是“手写版枚举”**

---

### 使用 enum 关键字（推荐 ⭐）

1. 使用了关键字来实现枚举类时，要求将定义常量对象写在最前面
2. 有多个常量对象时，用`,`分隔

> Java 官方已经把上面这一套  
> 👉 **全部帮你封装好了**

---

### 示例代码（超级简洁）

```java
enum Week {
    MONDAY("星期一"),
    TUESDAY("星期二"),
    WEDNESDAY("星期三"),
    THURSDAY("星期四"),
    FRIDAY("星期五"),
    SATURDAY("星期六"),
    SUNDAY("星期日");

    private String name;

    // 构造器默认就是 private
    Week(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
```

---

### 使用方式

```java
public class Test {
    public static void main(String[] args) {
        Week today = Week.FRIDAY;
        System.out.println(today.getName());
    }
}
```

---

### enum 帮你“偷偷”做了哪些事？（重点🔥）

当你写：

```java
enum Week { MONDAY, TUESDAY }
```

**Java 自动帮你做了：**

| 功能                          | 是否自动 |
| --------------------------- | ---- |
| 构造器 private                 | ✅    |
| 对象固定                        | ✅    |
| 不能 new                      | ✅    |
| 继承 Enum 类                   | ✅    |
| toString / values / valueOf | ✅    |
| 支持 switch                   | ✅    |

---

### enum 特有方法示例

```java
public class Test {
    public static void main(String[] args) {

        // 遍历所有枚举值
        for (Week w : Week.values()) {
            System.out.println(w + " -> " + w.getName());
        }

        // 字符串转枚举
        Week w = Week.valueOf("MONDAY");
        System.out.println(w.getName());
    }
}
```

---

### 什么时候用 enum？（考试 & 实战必背）

✅ **值是固定的、有限的**

- 星期
    
- 性别
    
- 状态（成功 / 失败）
    
- 订单状态（已支付 / 未支付）
    

❌ **值不确定、可动态变化**

- 用户
    
- 商品
    
- 数据库数据
    

### enum关键字

**javap**：是用来反编译的

1. 当我们使用enum关键字开发一个枚举类时，默认会继承Enum类，而且是一个final类
2. 如果我们使用的是无参构造器吗，创建常量对象，则实参列表和括号都可以省略
3. 简化为`MONDAY("星期一")`时这里调用了构造器
4. 使用了enum关键字后，就不能再继承其它类了，因为enum会隐式继承Enum
5. 枚举类和普通类一样，可以实现接口
#### 继承的Enum方法一览表
来，给你一张**一眼就能背、面试直接用**的👇  
👉 **继承的 `Enum` 方法一览表（完整 + 常用）**

| 方法名                                       | 返回值类型      | 作用说明                         | 常见使用场景    |
| ----------------------------------------- | ---------- | ---------------------------- | --------- |
| `name()`                                  | `String`   | 返回枚举常量的**名字（定义时的名称）**        | 日志、调试、序列化 |
| `ordinal()`                               | `int`      | 返回枚举常量的**定义顺序（从 0 开始）**      | 不推荐业务使用   |
| `toString()`                              | `String`   | 返回枚举常量的字符串表示（默认等同于 `name()`） | 输出、打印     |
| `compareTo(E o)`                          | `int`      | 比较两个枚举常量的顺序                  | 排序        |
| `equals(Object obj)`                      | `boolean`  | 判断是否为同一个枚举常量                 | 对象比较      |
| `hashCode()`                              | `int`      | 返回枚举常量的 hash 值               | 集合存储      |
| `getDeclaringClass()`                     | `Class<E>` | 返回定义该枚举的 Class 对象            | 反射        |
| `valueOf(Class<T> enumType, String name)` | `T`        | 根据名字获取指定枚举对象                 | 字符串转枚举    |

---

#### enum **自身**提供的静态方法（不是 Enum 里的）

> 这个点 **面试很容易混淆**，单独列出来 👇

|方法名|返回值类型|作用|
|---|---|---|
|`values()`|`E[]`|返回该枚举的所有枚举常量|
|`valueOf(String name)`|`E`|根据名称获取枚举常量|

---

#### 小 Demo（帮助你把表格“活”起来）

```java
enum Week {
    MONDAY, TUESDAY, WEDNESDAY
}

public class Test {
    public static void main(String[] args) {

        Week w = Week.MONDAY;

        System.out.println(w.name());        // MONDAY
        System.out.println(w.ordinal());     // 0
        System.out.println(w.toString());    // MONDAY

        System.out.println(w.compareTo(Week.TUESDAY)); // -1

        for (Week week : Week.values()) {
            System.out.println(week);
        }

        Week w2 = Week.valueOf("MONDAY");
        System.out.println(w == w2); // true（枚举是单例）
    }
}
```

---

#### 面试高频补充 ⚠️（加分点）

- ✅ 枚举**天生是单例**，`==` 可直接比较
    
- ❌ **不要用 `ordinal()` 做业务逻辑**
    
- ✅ 枚举 **不能继承类**（已经继承了 `Enum`）
    
- ✅ 枚举可以实现接口
    

---

#### 一句话记忆版

> **Enum = 常量 + 顺序 + 类型安全 + 单例**

如果你要，我可以下一步直接帮你整理一份  
👉 **「enum 高频面试题 + 标准答案」**  
或者  
👉 **「enum vs 常量接口 vs final 常量」对比表**



## 注解(Annotation)
1. 注解也被称为元数据，用于修饰解释包、类、方法、属性、构造器、几步变量等数据信息
2. 和注释一样，注解不影响程序逻辑，但注解可以被编译或运行，相当于嵌入在代码中的补充信息
3. 在使用时要在其前面增加@符号，并把该注解当成一个修饰符使用。用于修饰他支持的程序元素
### 三个基本的注解
#### @Override：限定某个方法，是重写父类方法，该注解只能用于方法
1. 如果写了这个注解，编译器会去检查该方法是否真的重写了父类的方法，如果确实重写了，则编译通过；如果没有构成重写，则编译不通过
	1. **`@interface`** 不是接口而是表示这个是一个注解类
	2. 只能修饰方法
	3. @Target是用于修饰注解的注解，称为元注解
#### @Depercated：用于表示某个程序元素（类、方法）已过时
1. 修饰某个元素，表示该元素已经过时；即不推荐使用，但是仍可以使用
2. 可以修饰方法、类、字段、包、参数
3. **作用：可以找到新旧版本的兼容和过渡**

#### @SuppressWarings：抑制编译警告
```java
@SuppressWarings({""})
//可以指定警告信息
```
1. 作用范围是和你放置的位置相关

# 异常

```java
int a = 10;
int b = 0;
int res = a / b;
//程序抛出异常，崩溃程序停止
```
- java设计者提供了异常处理机制来解决这个问题
```java
try{

}catch( Exception e ){
	//这里可以输出异常信息
}
```
- 此时如果再**try**内抛出异常但是程序依旧可以运行
- **将程序执行中发生的不正常情况称为“异常”**（开发过程中的语法错误和逻辑错误不是异常）
	- Ettor（错误）：java虚拟机无法解决的严重问题。严重错误程序会崩溃
	- Exception：其他因变成错误或偶然的外在因素导致的一般性问题，可以使用针对性的代码进行处理
		- 1. 运行时异常;编译器检查不出来
		- 2. 编译时异常;编译器必须处理的异常
```php
Java 异常体系
│
├── Throwable（所有异常和错误的根类）
│
├── Error（错误，程序员一般不处理）
│   │
│   ├── VirtualMachineError
│   │   ├── OutOfMemoryError（内存溢出）
│   │   └── StackOverflowError（栈溢出）
│   │
│   └── 其他 Error
│       └── NoClassDefFoundError
│
└── Exception（异常，程序可以处理）
    │
    ├── RuntimeException（运行时异常【非受检】）
    │   │
    │   ├── NullPointerException（空指针）
    │   ├── ArithmeticException（算术异常 / 除0）
    │   ├── ArrayIndexOutOfBoundsException（数组越界）
    │   ├── ClassCastException（类型转换异常）
    │   ├── NumberFormatException（数字格式异常）
    │   └── IndexOutOfBoundsException
    │
    └── Checked Exception（编译时异常【受检】）
        │
        ├── IOException
        │   ├── FileNotFoundException
        │   └── EOFException
        │
        ├── SQLException
        ├── ClassNotFoundException
        ├── InterruptedException
        └── ParseException
```



---
## try-catch-finally 

### 基本结构

```java
try {
    // 可能发生异常的代码
} catch (异常类型1 e) {
    // 处理异常1
} catch (异常类型2 e) {
    // 处理异常2
} finally {
    // 一定会执行的代码
}
```

---

### 各部分作用（必须理解）

### 1️⃣ try

- **包裹可能出异常的代码**
    
- try 中一旦发生异常，**try 后面的代码不再执行**，会直接执行catch的代码
    

---

### 2️⃣ catch

- **捕获并处理异常**
    
- 一个 try 可以对应 **多个 catch**
    
- **子类异常写在前，父类异常写在后**
    

❌ 错误示例：

```java
catch (Exception e) {}
catch (NullPointerException e) {} // 编译报错
```

✅ 正确示例：

```java
catch (NullPointerException e) {}
catch (Exception e) {}
```

---

### 3️⃣ finally（重点‼）

**特点：**

- 不管有没有异常，**都会执行**
    
- 一般用于：
    
    - 释放资源
        
    - 关闭流
        
    - 关闭数据库连接
        

```java
finally {
    System.out.println("一定会执行");
}
```

⚠️ 只有一种情况 finally 不执行：

> **JVM 退出（System.exit(0)）**

---

### 常见用法大全（面试 + 实战）

---

### ✅ 用法 1：try + catch（最常见）

```java
try {
    int a = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("除数不能为0");
}
```

📌 特点：

- 捕获异常
    
- 程序不会直接崩溃
    

---

### ✅ 用法 2：try + catch + finally（标准写法 ⭐）

```java
try {
    int[] arr = {1, 2, 3};
    System.out.println(arr[5]);
} catch (ArrayIndexOutOfBoundsException e) {
    System.out.println("数组越界");
} finally {
    System.out.println("释放资源");
}
```

📌 **不论是否越界，finally 都执行**

---

### ✅ 用法 3：多 catch 捕获不同异常

```java
try {
    String s = "abc";
    int num = Integer.parseInt(s);
} catch (NumberFormatException e) {
    System.out.println("数字格式错误");
} catch (Exception e) {
    System.out.println("其他异常");
}
```

---

### ✅ 用法 4：JDK7+ 合并 catch（推荐）

```java
try {
    // 代码
} catch (NumberFormatException | NullPointerException e) {
    System.out.println("发生运行时异常");
}
```

📌 条件：

- 异常之间 **不能是父子关系**
    

---

### finally 和 return 的关系（高频考点🔥）

### ❓ try/catch 里有 return，finally 还执行吗？

👉 **执行！而且先执行 finally**

```java
public static int test() {
    try {
        return 1;
    } finally {
        System.out.println("finally 执行");
    }
}
```

输出：

```
finally 执行
```

返回值：`1`

---

### ❗ finally 中有 return（强烈不推荐）

```java
public static int test() {
    try {
        return 1;
    } finally {
        return 2;
    }
}
```

📌 **最终返回 2（finally 覆盖一切）**

👉 面试一句话：

> finally 中不要写 return

---

### try-with-resources（JDK7+，强烈推荐）

👉 **自动关闭资源，等价于 finally**

```java
try (FileInputStream fis = new FileInputStream("a.txt")) {
    fis.read();
} catch (IOException e) {
    e.printStackTrace();
}
```

📌 特点：

- 资源类必须实现 `AutoCloseable`
    
- 自动调用 `close()`
    
- 比 finally 更安全
    

---

###  try-catch 的执行流程（必背）

```
进入 try
  ↓
是否发生异常？
  ↓ 否 → 执行完 try → 执行 finally → 结束
  ↓ 是
匹配 catch？
  ↓ 否 → 抛给 JVM → finally → 程序终止
  ↓ 是
执行 catch → 执行 finally → 继续执行
```

---

## thows

### 一、throws 是什么？（一句话版）

> **`throws` 用在方法声明上，用来把异常抛给调用者处理**

📌 核心思想：  
**当前方法不处理异常 → 交给上层方法处理**

---

### 二、基本用法（语法）

```java
public void 方法名() throws 异常类型1, 异常类型2 {
    // 可能产生异常的代码
}
```

#### 示例 1：抛出一个编译时异常（最经典）

```java
public void readFile() throws IOException {
    FileInputStream fis = new FileInputStream("a.txt");
    fis.read();
}
```

📌 说明：

- `IOException` 是 **编译时异常**
    
- 不写 `throws` → 编译直接报错
    

---

### 三、throws 的传播机制（非常重要🔥）

```java
public void methodA() throws IOException {
    methodB();
}

public void methodB() throws IOException {
    new FileInputStream("a.txt");
}
```

👉 异常**一层一层往上抛**，直到：

1️⃣ 被 `try-catch` 捕获  
2️⃣ 或者抛到 JVM → 程序终止

---

### 四、throws vs try-catch（核心对比）

|对比点|throws|try-catch|
|---|---|---|
|位置|方法声明|方法体|
|是否处理异常|❌ 不处理|✅ 处理|
|谁来处理|调用者|当前方法|
|常用于|底层方法|上层/业务方法|

👉 **真实项目原则**：

> 底层多 `throws`，上层统一 `try-catch`

---

### 五、throws 可以抛哪些异常？

### 1️⃣ 编译时异常（必须）

```java
throws IOException, SQLException
```

---

### 2️⃣ 运行时异常（可以，但没必要）

```java
throws NullPointerException
```

📌 说明：

- RuntimeException **不强制**
    
- 写了只是给人看的（文档作用）
    

---

### 3️⃣ 多个异常一起抛

```java
public void test() throws IOException, ClassNotFoundException {
}
```

---

### 六、子类重写方法时 throws 的规则（高频🔥）

### 📌 规则一句话

> **子类重写方法，抛出的异常不能比父类更大**

---

### 示例对比

#### 父类：

```java
class A {
    public void test() throws IOException {}
}
```

#### 子类（✅ 合法）：

```java
class B extends A {
    public void test() throws FileNotFoundException {}
}
```

#### 子类（❌ 不合法）：

```java
class C extends A {
    public void test() throws Exception {}
}
```

---

### 七、throws + main 方法（你一定见过）

```java
public static void main(String[] args) throws Exception {
    // 偷懒写法
}
```

📌 说明：

- 异常直接抛给 JVM
    
- **学习阶段可以用**
    
- **真实项目不推荐**
    

---

### 八、throws vs throw（别混了‼）

| 关键字    | 作用         | 意义           | 位置    | 后面跟的东西 |
| ------ | ---------- | ------------ | ----- | ------ |
| throws | 声明异常（方法上）  | 异常处理的一种方式    | 方法声明处 | 异常类型   |
| throw  | 手动抛异常（方法内） | 手动生成异常对象的关键字 | 异常对象  | 异常对象   |

### throw 示例：

```java
if (age < 0) {
    throw new IllegalArgumentException("年龄不能为负数");
}
```

---

### 九、什么时候用 throws？（实战原则）

✅ 适合 `throws` 的场景：

- 工具方法
    
- 底层 IO / 数据库
    
- 不知道怎么处理异常
    

❌ 不适合：

- 业务入口（Controller / main）
    
- 可以明确处理的业务异常
    

---

### 十、初学者最常犯 5 个错误

❌ throws 写在方法体里  
❌ 把 try-catch 和 throws 一起乱用  
❌ throws Exception 一路抛到 main  
❌ 子类抛更大的异常  
❌ 不区分 throw 和 throws

---


## 自定义异常的两种方式（重点🔥）

**当 Java 内置异常不能准确表达业务错误时，就需要自定义异常**

### 方式一：继承 RuntimeException（推荐 ⭐）

> **最常用、最灵活、真实项目首选**

### 1️⃣ 定义异常类

`public class AgeIllegalException extends RuntimeException {      public AgeIllegalException() {         super();     }      public AgeIllegalException(String message) {         super(message);     } }`

---

### 2️⃣ 使用异常（throw）

`public class UserService {      public void register(int age) {         if (age < 0 || age > 150) {             throw new AgeIllegalException("年龄不合法：" + age);         }         System.out.println("注册成功");     } }`

---

### 3️⃣ 调用方处理（可选）

`public class Test {     public static void main(String[] args) {         UserService service = new UserService();         try {             service.register(-1);         } catch (AgeIllegalException e) {             System.out.println(e.getMessage());         }     } }`

📌 特点总结：

- 不强制 try-catch
    
- 写代码不被异常“绑架”
    
- **企业项目最常见**
    

---

### 方式二：继承 Exception（受检异常）

> **强制调用者处理（较少用）**

### 定义：

`public class BalanceNotEnoughException extends Exception {     public BalanceNotEnoughException(String message) {         super(message);     } }`

---

### 使用（必须 throws）：

`public void withdraw(double money) throws BalanceNotEnoughException {     if (money > balance) {         throw new BalanceNotEnoughException("余额不足");     } }`

📌 特点：

- 编译器强制处理
    
- 代码侵入性强
    
- **一般不推荐，除非强制流程控制**

# 八大wapper类(包装)

## 包装类

| 基本数据类型  | 包装类           |
| ------- | ------------- |
| byte    | **Byte**      |
| short   | **Short**     |
| int     | **Integer**   |
| long    | **Long**      |
| float   | **Float**     |
| double  | **Double**    |
| char    | **Character** |
| boolean | **Boolean**   |

### 包装类和数据类型的转换
1. jdk5前的手动装箱和拆箱方式，装箱：基本类型 -> 包装类型，反之为拆箱
2. jdk5之后为自动的装箱和拆箱
```java
//装箱
int n = 100;
Integer integer = new Integer(n);
Integer integer = Integer.valueof(n);
//拆箱
int i = integer.inValue();
```


## 包装类 → String

### 方式一：`toString()`（推荐，最常用）

```java
Integer i = 100;
String s = i.toString();
```

📌 说明

- 所有包装类都继承自 `Object`
    
- 都重写了 `toString()` 方法
    
- **安全、直观、不容易出错**
    

---

### 方式二：`String.valueOf()`（通用方式）

```java
Integer i = 100;
String s = String.valueOf(i);
```

📌 说明

- **任何类型都能转成 String**
    
- 如果参数是 `null`，返回 `"null"`（不会抛异常）
    

```java
Integer i = null;
System.out.println(String.valueOf(i)); // 输出 "null"
```

---

### 方式三：`+ ""`（不推荐但常见）

```java
Integer i = 100;
String s = i + "";
```

📌 说明

- 底层仍然调用 `StringBuilder`
    
- **可读性差，不推荐在正式代码中使用**
    

---

## String → 包装类（非常重要🔥）

### 通用规则

> **使用包装类的 `parseXxx()` 方法**

---

### 示例

```java
String s1 = "123";

Integer i = Integer.parseInt(s1);
Double d = Double.parseDouble(s1);
Float f = Float.parseFloat(s1);
Long l = Long.parseLong(s1);
```

📌 返回的是 **基本数据类型**

---

### String → 包装类对象

```java
String s = "100";
Integer i = Integer.valueOf(s);
```

📌 区别总结：

|方法|返回类型|
|---|---|
|`parseXxx()`|基本数据类型|
|`valueOf()`|包装类对象|

---

## 包装类 ↔ 基本数据类型（补充完整）

### 手动拆箱（jdk5 之前）

```java
Integer integer = new Integer(100);
int n = integer.intValue();
```

---

### 自动装箱 & 自动拆箱（jdk5 之后）

```java
int a = 10;
Integer b = a;   // 自动装箱

Integer c = 20;
int d = c;       // 自动拆箱
```

📌 本质（面试必说）：

```java
Integer b = Integer.valueOf(a);
int d = c.intValue();
```

---

## ⚠️ 注意事项（你笔记里**一定要有**）

### 1️⃣ 包装类可以为 null，基本类型不行

```java
Integer i = null;
// int a = null; // 编译错误
```

---

### 2️⃣ 拆箱时如果是 null，会抛异常

```java
Integer i = null;
int a = i; // NullPointerException
```

---

### 3️⃣ Integer 缓存机制（面试高频🔥）

```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b); // true

Integer c = 128;
Integer d = 128;
System.out.println(c == d); // false
```

📌 原因

- `Integer` 对 `-128 ~ 127` 做了缓存
    
- `==` 比较的是 **地址**
    
- **包装类比较一律用 `equals()`**
    

# String
- 用于保存字符串
- 用双引号扣起来的字符序列
- 使用Unicode字符编码，一个字符（不管是汉字还是字母）都是占两个字节
- String实现了Serializable，说明String可以串行化，意味着可以在网络传输
- String实现类Comparable接口，说明String对象可以比较
- String有属性private final char value `[]`；用于存放字符串类型
- value是一个final类型，不可以修改：即value不能指向新的地址，但是单个字符内容是可以变化的
### 两种创建String对象的区别

#### 一、直接赋值

```java
String s1 = "xxa";
```

##### 1️⃣ 创建过程

- JVM **先去字符串常量池（String Constant Pool）里找**
    
- 如果池中 **已经有 `"xxa"`**  
    👉 `s1` **直接指向已有对象**
    
- 如果 **没有**  
    👉 在 **常量池中创建一个 `"xxa"` 对象**，`s1` 指向它
    

##### 2️⃣ 特点总结

✅ **可能不创建新对象**                                              
✅ **效率高，节省内存**  
✅ **推荐使用**

##### 3️⃣ 示意

```java
String s1 = "xxa";
String s2 = "xxa";

System.out.println(s1 == s2); // true
```

> 因为它们指向的是 **同一个常量池对象**

---

#### 二、调用构造器

```java
String s2 = new String("xxa");
```

##### 1️⃣ 创建过程（重点❗）

这一步 **至少创建 1 个对象，最多 2 个**

流程是：

1. **先检查常量池**
    
    - 如果 `"xxa"` 不存在 → 在常量池中创建
        
2. **一定会在堆中 new 一个新的 String 对象**
    
    - 内容是 `"xxa"`
        
    - `s2` 指向 **堆中的新对象**
        

##### 2️⃣ 特点总结

❌ **一定创建新对象（堆中）**  
❌ **内存浪费、效率低**  
❌ **一般不推荐**

##### 3️⃣ 示意

```java
String s1 = "xxa";
String s2 = new String("xxa");

System.out.println(s1 == s2); // false
```

> 一个在 **常量池**，一个在 **堆**

---

#### 三、内存对比图（非常重要）

##### ① 直接赋值

```
栈        常量池
s1  ───▶  "xxa"
s2  ───▶  "xxa"
```

##### ② new String

```
栈        堆              常量池
s2 ───▶  new String("xxa") ───▶ "xxa"
```

---

#### 四、对比总结表（建议背）

|对比点|`String s = "xxa"`|`String s = new String("xxa")`|
|---|---|---|
|是否用常量池|✅ 是|✅ 是|
|是否创建新对象|❌ 不一定|✅ 一定|
|对象位置|常量池|堆|
|内存占用|少|多|
|`==` 比较|可能为 true|一定为 false|
|推荐程度|⭐⭐⭐⭐⭐|⭐|
```text
┌──────────────┐
│  栈 Stack     │
│              │
│  s ───────────────┐
└──────────────┘     │
                     ▼
               ┌──────────────┐
               │ 常量池         │
               │ String Pool   │
               │              │
               │  "xxa"        │
               └──────────────┘

```

```text
┌──────────────┐
│  栈 Stack     │
│              │
│  s ───────────────┐
└──────────────┘     │
                     ▼
               ┌──────────────┐
               │   堆 Heap     │
               │              │
               │ new String   │
               │   value ───────┐
               └──────────────┘ │
                                 ▼
                         ┌──────────────┐
                         │ 常量池         │
                         │ String Pool   │
                         │              │
                         │  "xxa"        │
                         └──────────────┘

```


---

## String的内存布局

好，直接给你一张 **“一看就懂、面试也能复述”** 的  
👉 **String 内存变化流程图（ASCII版）**  
（完全按 JVM 真实逻辑来画）

---

### 一、`String s = "xxa"` 内存变化流程图

```text
┌──────────────┐
│  栈 Stack     │
│              │
│  s ───────────────┐
└──────────────┘     │
                     ▼
               ┌──────────────┐
               │ 常量池         │
               │ String Pool   │
               │              │
               │  "xxa"        │
               └──────────────┘
```

#### 运行流程

1️⃣ JVM 先去 **字符串常量池** 查找 `"xxa"`  
2️⃣ 如果存在 → **直接复用**  
3️⃣ 如果不存在 → **在常量池创建 `"xxa"`**  
4️⃣ 栈中的 `s` 指向常量池对象

✅ **最多只会有 1 个 `"xxa"` 对象**

---

### 二、`String s = new String("xxa")` 内存变化流程图（重点）

```text
┌──────────────┐
│  栈 Stack     │
│              │
│  s ───────────────┐
└──────────────┘     │
                     ▼
               ┌──────────────┐
               │   堆 Heap     │
               │              │
               │ new String   │
               │   value ───────┐
               └──────────────┘ │
                                 ▼
                         ┌──────────────┐
                         │ 常量池         │
                         │ String Pool   │
                         │              │
                         │  "xxa"        │
                         └──────────────┘
```

#### 运行流程（非常关键）

1️⃣ JVM **先检查常量池** 是否有 `"xxa"`

- 没有 → 创建 `"xxa"`（常量池）
    
- 有 → 直接用
    

2️⃣ **一定在堆中创建一个新的 String 对象**

3️⃣ `s` 指向的是 **堆中的对象**，不是常量池

⚠️ **至少 1 个对象，最多 2 个对象**

---

### 三、对比强化图（一眼区分）

#### 情况一：直接赋值

```java
String a = "java";
String b = "java";
```

```text
a ─┐
   ├──▶ "java"（常量池）
b ─┘
```

`a == b → true`

---

#### 情况二：new String

```java
String a = "java";
String b = new String("java");
```

```text
a ─────▶ "java"（常量池）

b ─────▶ new String("java")（堆）
```

`a == b → false`

---


# StringBuffer类
- java.lang.StringBuffer 代表可变的字符序列,可以对字符串内容进行增删
- 很多方法与string相同,但StringBuffer是可变长度的
- StringBuffer是一个容器
- 可以串行化
- 直接父类AbstractStringBuilder有属性char`[]` value,不是final;该value数组存放字符串内容,引出存放在堆中的
- StringBuffer是一个final类
### 和String的区别
1. String保存的是字符串常量,里面的值不能更改,每次String类的更新实际上就是更改地址;因为这里保存值的是 `private final char value[]`
2. StringBuffer保存的是字符串变量,里面的值可以更改每次StringBuffer的更新实际上可以更新内容,不用每次更新地址效率更高;保存值得是 `char[] value` 放在堆中


### 构造器

1. StringBuffer():构造一个不带字符得字符串缓冲区,其初始容量为16个字符
```java
StringBuffer S = new StringBuffer();
```
2. StringBuffer(100),通过指定`char[]`大小
```java
StringBuffer S = new StringBuffer(100);
```
3. 通过一个String创建StringBuffer
```java
StringBuffer S = new StringBuffer("hello");
```
	1. 这里创建char`[]`大小是给的字符长度加上16
	2. 先创建一个21长得char`[]`,然后通过append()初始化为hello

### String和StringBuffer之间的转化
####  String->StringBuffer

1. 使用构造器,对String本身没有影响
```java
String S = "hello";
StringBuffer Sb = new StringBuffer(s);
```
2. 直接使用Append加入到一个空的StringBuffer
#### StringBuffer->String
1. 使用StringBuffer提供的`toString`方法
```java
StringBuffer s = new StringBuffer("hello");
String str = s.toString();
```
2. 使用String的构造器
```java
String str1 = new String(s);
```


# Math类
- **常用方法**
### 绝对值`abs`
```java
int abd = Math.abs(-99);
```
### 求幂`pow`
```java
double pow = Math.pow(2,4);//2的4次方
```
### 向上取整`ceil`
- 返回`>=`该参数的最小整数
```java
double ceil = Math.ceil(-3.0001);
```
####  向下取整`floor`
- 返回`<=`该参数的最大整数
```java
double floor = Math.floor(-3.0001);

```
#### 四舍五入`round`
```java
long round = Math.floor(-5,5);//6
```
#### 开方`sqrt`
```java
double sqrt = Math.sqrt(9);
```
#### 随机数`random`
- 返回的是`0 <= x < 1`之间的一个小数
```java
double d = Math.random()
```

# Arrays类
## toString方法
- 直接使用toString显示数组(遍历数组)
```java
System.out.pringln(Arrays.toString())
```
## 排序`sort`
- 数组是引用类型,通过sort排序后,会直接影响实参
```java
integer arr[] = [9,0,2,2,5];
System.out.print(arr.sort);
```
- 这里是从小到大
- sort重载的,可以通过传入一个接口Comparator来实现定制排序

Java 中排序主要分为 **两种方式**：

1. **自然排序**（Comparable）
    
2. **定制排序**（Comparator）
    

---

### 二、自然排序（Comparable）

#### 1️⃣ 概念

- **类自己定义排序规则**
    
- 实现 `Comparable<T>` 接口
    
- 重写 `compareTo()` 方法
    

👉 **一个类只能有一种自然排序规则**

---

#### 2️⃣ 使用场景

- 对象有**固定、唯一**的排序规则  
    （如：按 id、按年龄）
    

---

#### 3️⃣ 示例

```java
class Person implements Comparable<Person> {
    String name;
    int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public int compareTo(Person o) {
        // 按年龄升序
        return this.age - o.age;
    }
}
```

```java
Person[] arr = {
    new Person("张三", 20),
    new Person("李四", 18)
};

Arrays.sort(arr);
```

---

#### 4️⃣ compareTo 返回值规则

|返回值|含义|
|---|---|
|`< 0`|当前对象在前|
|`= 0`|相等|
|`> 0`|当前对象在后|

---

### 三、定制排序（Comparator）⭐⭐⭐（重点）

#### 1️⃣ 概念

- **外部指定排序规则**
    
- 不修改原有类
    
- 一个类可以有 **多种排序方式**
    

👉 **面试 & 实战最常用**

---

#### 2️⃣ 核心方法

```java
int compare(T o1, T o2)
```

---

#### 3️⃣ 基本示例（数组排序）

```java
Integer[] arr = {3, 1, 5, 2};

Arrays.sort(arr, new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        // 降序
        return o2 - o1;
    }
});
```

---

### 四、对象定制排序（多条件排序🔥）

#### 示例需求

👉 学生排序规则：

1. 年龄升序
    
2. 年龄相同 → 成绩降序
    

---

#### Student 类

```java
class Student {
    String name;
    int age;
    double score;

    public Student(String name, int age, double score) {
        this.name = name;
        this.age = age;
        this.score = score;
    }
}
```

---

#### Comparator 写法

```java
list.sort(new Comparator<Student>() {
    @Override
    public int compare(Student s1, Student s2) {
        if (s1.age != s2.age) {
            return s1.age - s2.age;   // 年龄升序
        }
        return Double.compare(s2.score, s1.score); // 成绩降序
    }
});
```

---

### 五、Lambda 排序（Java 8+）

```java
list.sort((s1, s2) -> {
    if (s1.age != s2.age) {
        return s1.age - s2.age;
    }
    return Double.compare(s2.score, s1.score);
});
```

---

### 六、官方推荐 Comparator 写法（⭐⭐⭐⭐⭐）

```java
list.sort(
    Comparator.comparingInt((Student s) -> s.age)
              .thenComparing((s1, s2) -> Double.compare(s2.score, s1.score))
);
```

### 优点

- 可读性强
    
- 不容易写错
    
- 面试官非常喜欢
    

---

### 七、Arrays.sort vs Collections.sort

|方法|适用对象|
|---|---|
|`Arrays.sort()`|数组|
|`Collections.sort()`|List|
|`list.sort()`|Java 8 推荐|

---

## binarySearch
- 通过二叉搜索法进行查找是否有一个数,要求必须排好序
- 不存在就返回`return -(low + 1)` ;这个`low`表示的是要查找的数如果在数组内的话应该在什么位置
```java
int i = Array.binarySearch(arr,1);//返回的是下标
```



## System 类（java.lang.System）

System 类位于 **java.lang 包**下，使用时**不需要导包**，主要用于完成**与 JVM 和操作系统相关的功能**。

特点说明：

- System 是 **final 类**，不能被继承
    
- 构造方法是 **private**，不能创建对象
    
- 常用成员 **全部是 static**
    
- 属于 **系统级工具类**
    

---

## 常用成员变量

### System.out（标准输出流）

```java
System.out.println("Hello Java");
System.out.print("Hello");
```

说明：

- 类型是 `PrintStream`
    
- 默认输出到 **控制台**
    
- 用于输出正常信息
    
- 本质是 **标准输出流 stdout**
    

---

### System.err（标准错误输出流）

```java
System.err.println("发生错误");
```

说明：

- 类型同样是 `PrintStream`
    
- 也是输出到控制台
    
- 用于输出错误信息
    
- 本质是 **错误输出流 stderr**
    

实际项目中：

- `System.out` → 普通日志
    
- `System.err` → 错误日志
    

---

## 常用方法（核心）

### exit —— 退出当前 JVM

```java
System.exit(0);
```

作用：

- **立即终止 JVM**
    
- 后面的代码不会再执行
    

参数说明：

- `0`：正常退出
    
- 非 0：异常退出（通常表示程序错误）
    

示例：

```java
System.out.println("程序开始");
System.exit(0);
System.out.println("这里不会执行");
```

补充理解：

- `return`：退出方法
    
- `System.exit()`：退出整个 JVM
    

---

### arraycopy —— 数组拷贝（底层高效）

```java
System.arraycopy(src, srcPos, dest, destPos, length);
```

参数含义：

- `src`：源数组
    
- `srcPos`：源数组起始索引
    
- `dest`：目标数组
    
- `destPos`：目标数组起始索引
    
- `length`：拷贝元素个数
    

示例：

```java
int[] src = {1, 2, 3, 4, 5};
int[] dest = new int[5];

System.arraycopy(src, 0, dest, 0, src.length);

for (int i : dest) {
    System.out.println(i);
}
```

特点说明：

- 属于 **native 方法**
    
- 底层使用 C/C++ 实现
    
- 性能比 for 循环高
    
- 常用于 JDK 底层和性能敏感场景
    

注意事项：

- 源数组和目标数组类型必须兼容
    
- 索引越界会抛异常
    
- 是 **浅拷贝**
    

---

### currentTimeMillis —— 获取当前时间戳

```java
long time = System.currentTimeMillis();
```

说明：

- 返回的是 **1970-01-01 00:00:00（UTC）到现在的毫秒数**
    
- 常用于：
    
    - 计算程序耗时
        
    - 生成时间戳
        
    - 简单性能测试
        

示例（计算代码执行时间）：

```java
long start = System.currentTimeMillis();

for (int i = 0; i < 100000; i++) {
    // 模拟耗时操作
}

long end = System.currentTimeMillis();
System.out.println("耗时：" + (end - start) + "ms");
```

补充：

- 精度是毫秒
    
- Java 8 以后推荐使用 `java.time` 包（如 `Instant`）
    

---

### gc —— 建议 JVM 执行垃圾回收

```java
System.gc();
```

说明：

- 只是 **向 JVM 发出建议**
    
- JVM **不一定立即执行 GC**
    
- 实际是否回收由 JVM 决定
    

特点：

- 本质等价于 `Runtime.getRuntime().gc()`
    
- 一般不建议在业务代码中频繁调用
    

补充理解：

- GC 是否执行
    
- GC 何时执行
    
- GC 回收多少  
    👉 **全部由 JVM 控制**
    

---

## System 类使用场景总结

- 程序退出控制 → `System.exit`
    
- 高效数组复制 → `System.arraycopy`
    
- 性能计时 / 时间戳 → `System.currentTimeMillis`
    
- 调试或测试 GC → `System.gc`
    
- 控制台输出 → `System.out / System.err`
    

---

## 面试常见问法补充

- System 能不能 new？  
    → 不能，构造器是 private
    
- `arraycopy` 和 for 循环区别？  
    → native 方法，性能更高
    
- `System.exit` 和 return 区别？  
    → exit 退出 JVM，return 只退出方法
    
- `System.gc()` 一定会 GC 吗？  
    → 不一定，只是建议
    


# 集合（Collection Framework）

- 可以动态保存任意多个对象，使用方便
    
- 提供了一系列操作对象的方法（增、删、改、查等）
    
- 使用集合进行添加、删除等操作，不需要关心数组长度
    
**集合主要是两组（单列集合：存值。双列集合：存键值对）**

---

## Collection（单列集合）
- collenction实现子类可以存放多个元素,每个元素可以是Object
- 有些collection的实现类,可以存放重复的元素
- 有些collection的实现类,有些是有序的
- collection接口没有直接的实现子类,是通过它的子接口Set和List来实现的
### 常用类(使用ArrayList演示)
1. `add`添加单个元素
```java
List list = new ArrayList();
list.add("jack");
list.add(10);
list.add(true);
```
2. `remove`删除单个元素
```java
list.remove(0);//删除第一个元素
list.remove("jack");//指定元素
```
3. `contains`查找元素是否存在
```java
list.contains("jack");//返回布尔值
```
4. `size`获取元素个数
5. `isEmpty`判断是否为空
6. `clear`清空元素
7. `addAll`添加多个元素
```java
//一个新ArrayList
ArrayList list2 = new ArrsyList();
list2.add("xxa");
list2.add("xxb");
list.addAll(list2);
```
8. `contains`查找多个元素;使用和`7`类似


### List（有序、可重复）

- ArrayList

- LinkedList

- Vector


---

### Set（无序、不可重复）

- HashSet
    
- TreeSet
    

---

## Map（双列集合）

### HashMap
#### `LinkedHashMap`

### TreeMap

### Hashtable

### Properties













