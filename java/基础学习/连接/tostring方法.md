`toString()` 是 Java 中 `Object` 类的一个方法，**用于返回对象的字符串表示形式**。它的主要作用是**便于调试、日志打印或显示对象信息**。

---

### 一、默认行为（未重写时）
- `Object` 类中的默认实现返回的是：
  ```
  类名@哈希码的十六进制
  ```
  例如：
  ```java
  Person p = new Person();
  System.out.println(p); // 输出类似：Person@1b6d3586
  ```

- 这种输出对开发者**几乎没有实际意义**，无法看出对象的内容。

---

### 二、为什么要重写 `toString()`？
为了让对象在被打印或转换为字符串时，**显示有意义的信息**，比如关键字段的值。

#### 示例（重写后）：
```java
class Person {
    String name;
    int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }
}

// 使用
Person p = new Person("Alice", 20);
System.out.println(p); // 输出：Person{name='Alice', age=20}
```

> ✅ 这样在调试、日志或测试时，能一眼看出对象状态。

---

### 三、常见使用场景
1. **`System.out.println(obj)`**  
   会自动调用 `obj.toString()`。
2. **字符串拼接**  
   ```java
   String msg = "User: " + user; // 等价于 "User: " + user.toString()
   ```
3. **日志框架（如 Log4j、SLF4J）**  
   打印对象时依赖 `toString()`。
4. **调试器（IDE 的变量查看）**  
   显示对象时通常调用 `toString()`。

---

### 四、最佳实践
- **包含所有关键字段**（尤其是参与 `equals()` 比较的字段）。
- **格式清晰、一致**，建议使用 `{field=value, ...}` 风格。
- **避免返回 null**，应始终返回有效字符串。
- **不要在 `toString()` 中抛异常**（会影响调试和日志）。

#### 推荐写法（使用 IDE 自动生成）：
大多数 IDE（如 IntelliJ IDEA、Eclipse）可以自动生成规范的 `toString()`：

```java
@Override
public String toString() {
    return "Person{" +
           "name='" + name + '\'' +
           ", age=" + age +
           '}';
}
```

或者使用第三方库（如 Lombok）：
```java
@ToString
class Person {
    String name;
    int age;
}
// 自动生成 toString()
```

---

### 五、与 `equals()` / `hashCode()` 的关系
虽然 `toString()` 不像 `equals()` 和 `hashCode()` 那样有强制一致性要求，但**良好的 `toString()` 实现能极大提升代码可读性和可维护性**，尤其是在排查问题时。

---

### 总结
| 是否重写 | 输出示例 | 用途 |
|--------|--------|------|
| ❌ 默认 | `Person@1b6d3586` | 几乎无用 |
| ✅ 重写 | `Person{name='Alice', age=20}` | 调试、日志、展示 |

> 💡 **建议**：**所有自定义类都应重写 `toString()`**，哪怕只是临时开发，也能节省大量排查时间。

如果你正在学习 Java 面向对象编程（比如在培训班中），养成重写 `toString()` 的习惯会让你的代码更专业、更易维护。