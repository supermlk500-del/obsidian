`hashCode()` 方法是 Java 中 `Object` 类的一个重要方法，与 `equals()` 紧密相关。理解它对正确使用集合（如 `HashMap`、`HashSet`）至关重要。

---

### 一、`hashCode()` 的作用
- 返回一个 **整数（int）**，称为“哈希码”或“散列码”。
- 主要用于 **哈希表类数据结构**（如 `HashMap`, `HashSet`, `Hashtable`）中，**快速定位对象存储的位置**，提高查找效率。

---

### 二、核心约定（来自 Java 官方文档）
如果两个对象 **逻辑相等**（即 `equals()` 返回 `true`），那么它们的 `hashCode()` **必须返回相同的值**。

> ✅ **重要规则**：
> - 如果 `a.equals(b) == true`，则 `a.hashCode() == b.hashCode()` **必须成立**。
> - 反过来不成立：**hashCode 相同，equals 不一定为 true**（哈希冲突）。

违反这个规则会导致集合类（如 `HashMap`）行为异常，比如“存进去却找不到”。

---

### 三、默认行为（未重写时）
- `Object` 类的 `hashCode()` 默认返回对象的**内存地址**（或其某种映射）。
- 所以：**不同对象即使内容相同，hashCode 也可能不同**（除非重写）。

---

### 四、何时需要重写 `hashCode()`？
**当你重写了 `equals()` 方法时，就必须重写 `hashCode()`！**

#### 示例：错误做法（只重写 equals）
```java
class Person {
    String name;
    int age;

    @Override
    public boolean equals(Object o) {
        // ... 比较 name 和 age
    }
    // ❌ 忘记重写 hashCode()
}
```

后果：
```java
Set<Person> set = new HashSet<>();
Person p1 = new Person("Alice", 20);
Person p2 = new Person("Alice", 20);

set.add(p1);
System.out.println(set.contains(p2)); // 可能返回 false！即使 equals 为 true
```
因为 `p1` 和 `p2` 的 `hashCode()` 不同，`HashSet` 把它们放到了不同的“桶”里，根本不会调用 `equals()` 去比较！

---

### 五、如何正确重写 `hashCode()`？
推荐使用 `Objects.hash()`（Java 7+）：

```java
@Override
public int hashCode() {
    return Objects.hash(name, age);
}
```

或者手动实现（较少用）：
```java
@Override
public int hashCode() {
    int result = name != null ? name.hashCode() : 0;
    result = 31 * result + age;
    return result;
}
```

> ✅ **原则**：参与 `equals()` 比较的字段，也必须参与 `hashCode()` 计算。

---

### 六、String 的例子（已正确实现）
```java
String s1 = new String("hello");
String s2 = new String("hello");

System.out.println(s1.equals(s2));      // true
System.out.println(s1.hashCode() == s2.hashCode()); // true（内容相同，hashCode 相同）
```

这就是为什么 `String` 可以安全地用作 `HashMap` 的 key。

---

### 总结

| 场景              | 是否需要重写 `hashCode()`     |
| --------------- | ----------------------- |
| 没有重写 `equals()` | ❌ 不需要                   |
| 重写了 `equals()`  | ✅ **必须重写 `hashCode()`** |

> ⚠️ **黄金法则**：  
> **`equals()` 相等 → `hashCode()` 必须相等**  
> 否则在哈希集合中会出错！

如果你正在学习 Java 集合框架或准备面试，这一点是高频考点。建议在自定义类中使用 IDE（如 IntelliJ IDEA）自动生成 `equals()` 和 `hashCode()`，避免手写出错。