
### 表达式只能是byte，short，int，char，JDK5开始支持枚举，JDK7开始支持string，不支持double，float，long

你描述的是 **`switch`语句**中`case`标签（即`case`后面的值）所支持的表达式类型。

### 总结一下支持的表达式类型：

1.  **基本类型**：`byte`, `short`, `int`, `char`
2.  **它们的包装类**：`Byte`, `Short`, `Integer`, `Character`
3.  **字符串**：`String` (从 **JDK 7** 开始)
4.  **枚举类型**：`Enum` (从 **JDK 5** 开始)
在java中，只要有值返回，就是一个表达式
### 不支持的类型：

*   `long`, `float`, `double`, `boolean` 及其对应的包装类。

**原因**：`switch`语句的设计初衷是用于对一组离散的、数量不多的常量值进行判断。`long`、`float`、`double`由于精度问题，很难有绝对相等的匹配，而且它们的可能取值数量非常庞大，不适合用`switch`。`boolean`只有两个值，直接用`if-else`更清晰。

---

## 代码示例

### 示例 1：支持的基本类型 (`int`, `char`)

```java
// 支持 int 类型
int dayOfWeek = 3;
switch (dayOfWeek) {
    case 1:
        System.out.println("星期一");
        break;
    case 2:
        System.out.println("星期二");
        break;
    case 3:
        System.out.println("星期三"); // 这行会被执行
        break;
    default:
        System.out.println("其他日子");
}

// 支持 char 类型
char grade = 'B';
switch (grade) {
    case 'A':
        System.out.println("优秀");
        break;
    case 'B':
        System.out.println("良好"); // 这行会被执行
        break;
    case 'C':
        System.out.println("及格");
        break;
    default:
        System.out.println("不及格");
}
```

### 示例 2：JDK 5 开始支持的枚举 (`Enum`)

```java
// 定义一个枚举
enum Color {
    RED, GREEN, BLUE
}

public class SwitchExample {
    public static void main(String[] args) {
        Color myColor = Color.GREEN;

        switch (myColor) {
            case RED:
                System.out.println("红色");
                break;
            case GREEN:
                System.out.println("绿色"); // 这行会被执行
                break;
            case BLUE:
                System.out.println("蓝色");
                break;
        }
    }
}
```

### 示例 3：JDK 7 开始支持的字符串 (`String`)

```java
String fruit = "Apple";

switch (fruit) {
    case "Banana":
        System.out.println("这是香蕉");
        break;
    case "Apple":
        System.out.println("这是苹果"); // 这行会被执行
        break;
    case "Orange":
        System.out.println("这是橙子");
        break;
    default:
        System.out.println("未知水果");
}
```

---

## 不支持的类型的代码示例（会导致编译错误）

### 示例 4：尝试使用 `long` (会报错)

```java
long bigNumber = 1000L;

// 以下代码无法编译！会报错：Incompatible types. Found: 'long', required: 'char, byte, short, int, Character, Byte, Short, Integer, String, or an enum'
switch (bigNumber) { // 编译错误！
    case 1000L:
        System.out.println("一千");
        break;
    default:
        System.out.println("其他数字");
}
```

### 示例 5：尝试使用 `double` (会报错)

```java
double price = 9.99;

// 以下代码无法编译！会报错：Incompatible types. Found: 'double', required: 'char, byte, short, int, Character, Byte, Short, Integer, String, or an enum'
switch (price) { // 编译错误！
    case 9.99:
        System.out.println("特价");
        break;
    default:
        System.out.println("原价");
}
```

### 示例 6：尝试使用 `boolean` (会报错)

```java
boolean isRaining = true;

// 以下代码无法编译！会报同样的类型不兼容错误
switch (isRaining) { // 编译错误！
    case true:
        System.out.println("带伞");
        break;
    case false:
        System.out.println("不用带伞");
        break;
}
// 对于boolean，应该使用 if-else
if (isRaining) {
    System.out.println("带伞");
} else {
    System.out.println("不用带伞");
}
```

### 总结表格

| 类型                             | 是否支持 | 从哪个JDK版本开始 | 备注                  |
| :----------------------------- | :--: | :--------: | :------------------ |
| `byte`, `short`, `int`, `char` |  ✅   |  JDK 1.0   | 基本支持                |
| 枚举 (`Enum`)                    |  ✅   |   JDK 5    |                     |
| 字符串 (`String`)                 |  ✅   |   JDK 7    |                     |
| `long`, `float`, `double`      |  ❌   |     -      | 由于精度和取值范围原因不支持      |
| `boolean`                      |  ❌   |     -      | 只有两个值，用`if-else`更合适 |

2. case给出的值不能重复，且只能是字面量，不能是变量
3. 穿透性的例子
你说得非常对！**`switch`语句确实有穿透（Fall-through）的性质**。

**穿透（Fall-through）** 指的是：当某个`case`分支匹配成功后，如果该分支**没有以`break`语句结束**，程序会**继续执行下一个`case`分支的代码**，而不会判断下一个`case`的值是否匹配。

---

## 穿透的例子

### 示例 1：月份天数判断（经典的穿透用法）

```java
int month = 2;
int year = 2020; // 闰年
int days = 0;

switch (month) {
    case 1: case 3: case 5: case 7: case 8: case 10: case 12:
        days = 31;
        break; // 遇到break才会跳出switch
        
    case 4: case 6: case 9: case 11:
        days = 30;
        break;
        
    case 2:
        // 对于2月，需要判断是否是闰年
        if ((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)) {
            days = 29; // 闰年
        } else {
            days = 28; // 平年
        }
        break;
        
    default:
        System.out.println("无效的月份");
        break;
}

System.out.println(month + "月有 " + days + " 天"); // 输出：2月有 29 天
```

在这个例子中：
- `case 1: case 3: case 5:` 等使用了穿透特性，让多个`case`共享同一段代码
- 这样避免了为每个有31天的月份都写一遍 `days = 31; break;`

### 示例 2：成绩等级评定（演示穿透效果）

```java
char grade = 'B';
System.out.println("你的等级是 " + grade + "，评语：");

switch (grade) {
    case 'A':
        System.out.println("优秀！");
    case 'B':
        System.out.println("良好！"); // 会执行
    case 'C':
        System.out.println("及格！"); // 会执行（穿透到这里）
    case 'D':
        System.out.println("需要努力！"); // 会执行（穿透到这里）
    case 'F':
        System.out.println("不及格！"); // 会执行（穿透到这里）
        break;
    default:
        System.out.println("无效等级");
}

// 输出结果：
// 你的等级是 B，评语：
// 良好！
// 及格！
// 需要努力！
// 不及格！
```

**分析执行过程：**
1. `grade`是`'B'`，匹配到 `case 'B':`
2. 执行 `System.out.println("良好！");`
3. **没有`break`**，程序**穿透**到下一个`case 'C'`，执行其代码
4. 继续**穿透**到`case 'D'`，执行其代码
5. 继续**穿透**到`case 'F'`，执行其代码
6. 遇到`break`，跳出`switch`

### 示例 3：工作日判断（忘记写break的常见错误）

```java
int day = 2; // 星期二

switch (day) {
    case 1:
        System.out.println("星期一");
    case 2:
        System.out.println("星期二"); // 会执行
    case 3:
        System.out.println("星期三"); // 会执行（穿透）
    case 4:
        System.out.println("星期四"); // 会执行（穿透）
    case 5:
        System.out.println("星期五"); // 会执行（穿透）
        break;
    case 6:
        System.out.println("星期六");
        break;
    case 7:
        System.out.println("星期日");
        break;
    default:
        System.out.println("无效日期");
}

// 输出结果：
// 星期二
// 星期三
// 星期四
// 星期五
```

---

## 如何避免意外的穿透？

### 方法1：总是使用`break`（推荐）

```java
switch (variable) {
    case 1:
        // 代码...
        break; // 总是记得写break
    case 2:
        // 代码...
        break;
    default:
        // 代码...
        break;
}
```

### 方法2：使用`return`代替`break`（如果在方法中）

```java
public String getDayName(int day) {
    switch (day) {
        case 1: return "星期一";
        case 2: return "星期二";
        case 3: return "星期三";
        default: return "未知";
    }
    // 不需要break，因为return已经退出方法了
}
```

### 方法3：使用新的`switch表达式`（JDK 14+）

```java
// JDK 14+ 的switch表达式，没有穿透问题
int day = 2;
String dayName = switch (day) {
    case 1 -> "星期一";
    case 2 -> "星期二"; // 使用箭头语法，自动break
    case 3 -> "星期三";
    default -> "未知";
};
System.out.println(dayName); // 输出：星期二
```

## 总结

- **穿透是`switch`语句的固有特性**，不是bug
- **有意使用穿透**可以简化代码（如多个case共享逻辑）
- **无意穿透**是常见的编程错误，记得写`break`
- **现代Java**推荐使用`switch表达式`来避免穿透问题

穿透特性就像一把双刃剑，用得好可以写出简洁的代码，用不好会导致难以发现的bug！