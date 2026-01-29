这个问题的答案取决于 **这个“类”是否重写了 `equals()` 方法**。

---

### 一、如果这个类 **没有重写 `equals()` 方法**
- 那么它继承的是 `Object` 类中的默认 `equals()` 实现。
- `Object.equals()` 的行为和 `==` **完全一样**：**比较的是对象的引用（内存地址）**。
- 即使两个对象的**内容完全相同**，只要它们是通过两次 `new` 创建的（即两个不同的对象），`equals()` 就会返回 **`false`**。

#### 示例（未重写 `equals`）：
```java
class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

Person p1 = new Person("Alice", 20);
Person p2 = new Person("Alice", 20);

System.out.println(p1.equals(p2)); // false！因为 Person 没有重写 equals()
```

> 虽然 `p1` 和 `p2` 内容一样，但它们是两个不同的对象，`Object.equals()` 只看地址。

---

### 二、如果这个类 **重写了 `equals()` 方法**
- 开发者通常会根据业务逻辑，在 `equals()` 中比较对象的**关键字段是否相等**（比如 `name` 和 `age`）。
- 此时，即使 `p1` 和 `p2` 是两个不同的对象，只要内容一致，`equals()` 就会返回 **`true`**。

#### 示例（重写了 `equals`）：
```java
class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Person p = (Person) obj;
        return age == p.age && Objects.equals(name, p.name);
    }
}

Person p1 = new Person("Alice", 20);
Person p2 = new Person("Alice", 20);

System.out.println(p1.equals(p2)); // true！因为 equals 被正确重写了
```

---

### 特别说明：`String`、`Integer` 等 JDK 类
- 这些类**已经重写了 `equals()`**，所以：
  ```java
  String s1 = new String("hello");
  String s2 = new String("hello");
  System.out.println(s1.equals(s2)); // true
  ```
  因为 `String.equals()` 比较的是字符内容。

---

### 总结

| 类是否重写 `equals()` | `new` 出的两个内容相同的对象调用 `equals()` |
|------------------------|---------------------------------------------|
| ❌ 没有重写            | `false`（比较的是引用）                     |
| ✅ 重写了              | `true`（如果内容逻辑相等）                  |

> 所以，**不能一概而论**。关键看该类有没有按“内容相等”的语义去重写 `equals()` 方法。

如果你正在学习 Java 面向对象编程（比如在培训班中），掌握这一点对理解集合（如 `HashSet`、`HashMap`）的行为非常重要。