# super和this的访问规则和区别详解

## 一、核心概念对比

| 特性 | **this** | **super** |
|------|----------|-----------|
| **本质** | 当前对象的引用 | 父类部分的引用 |
| **指向** | 当前对象实例 | 当前对象的父类部分 |
| **内存** | 指向堆中的整个对象 | 指向同一对象的父类部分 |
| **使用限制** | 所有实例方法中均可使用 | 只能在子类中使用 |
| **调用构造器** | this(参数) - 调用本类其他构造器 | super(参数) - 调用父类构造器 |

## 二、详细访问规则

### 1. this的访问规则
```java
public class ThisExample {
    private String name = "实例变量";
    private static int count = 0;  // 静态变量
    
    public ThisExample(String name) {
        // 1. 区分实例变量和局部变量
        this.name = name;  // this.name指实例变量，name指参数
        
        // 2. 调用本类其他构造器（必须在第一行）
        // this();  // 可以调用无参构造器
    }
    
    public void method1() {
        String name = "局部变量";
        
        System.out.println(name);       // "局部变量" - 局部变量优先
        System.out.println(this.name);  // "实例变量" - 明确指定实例变量
        System.out.println(this);       // 输出当前对象引用
        
        // 3. 作为参数传递
        process(this);
        
        // 4. 返回当前对象（链式调用）
        // return this;
    }
    
    public static void staticMethod() {
        // System.out.println(this);  // 错误！静态方法中不能使用this
        // System.out.println(this.name);  // 错误！
        System.out.println(count);  // 可以直接访问静态变量
    }
    
    private void process(ThisExample obj) {
        System.out.println("处理对象: " + obj);
    }
}
```

### 2. super的访问规则
```java
class Parent {
    protected String name = "父类名字";
    private String secret = "父类私有";
    
    protected void parentMethod() {
        System.out.println("父类方法");
    }
    
    private void privateMethod() {
        System.out.println("父类私有方法");
    }
}

class Child extends Parent {
    private String name = "子类名字";
    
    public void test() {
        // 1. 访问被隐藏的父类字段
        System.out.println(name);        // "子类名字" - 子类的name
        System.out.println(this.name);   // "子类名字" - 子类的name  
        System.out.println(super.name);  // "父类名字" - 父类的name
        
        // 2. 调用被重写的父类方法
        parentMethod();       // 如果子类重写了，调用子类版本
        super.parentMethod(); // 明确调用父类版本
        
        // 3. 不能访问父类私有成员
        // System.out.println(super.secret);  // 编译错误
        // super.privateMethod();             // 编译错误
        
        // 4. 调用父类构造器（只能在构造器中使用）
        // super();  // 只能在构造器第一行调用
    }
    
    @Override
    protected void parentMethod() {
        System.out.println("子类重写的方法");
        
        // 先调用父类实现，再添加子类逻辑
        super.parentMethod();
        System.out.println("子类新增的逻辑");
    }
}
```

## 三、在构造器中的特殊规则

```java
class Animal {
    private String name;
    
    public Animal() {
        this("无名动物");  // 调用本类的有参构造器
        System.out.println("Animal无参构造器");
    }
    
    public Animal(String name) {
        this.name = name;
        System.out.println("Animal有参构造器: " + name);
    }
}

class Dog extends Animal {
    private String breed;
    
    // 情况1：默认调用父类无参构造器
    public Dog() {
        // 隐式 super(); 调用Animal()
        System.out.println("Dog无参构造器");
    }
    
    // 情况2：显式调用父类有参构造器
    public Dog(String name, String breed) {
        super(name);  // 必须在第一行
        this.breed = breed;
        System.out.println("Dog两参构造器");
    }
    
    // 情况3：this()和super()不能同时出现
    public Dog(String breed) {
        this("无名", breed);  // 调用本类其他构造器
        // super("xxx");  // 错误！不能在this()之后调用super()
    }
}

// 测试构造器调用顺序
public class ConstructorTest {
    public static void main(String[] args) {
        System.out.println("=== 创建Dog对象 ===");
        Dog dog1 = new Dog();
        // 输出：
        // Animal有参构造器: 无名动物
        // Animal无参构造器
        // Dog无参构造器
        
        System.out.println("\n=== 创建有参Dog对象 ===");
        Dog dog2 = new Dog("小黑", "泰迪");
        // 输出：
        // Animal有参构造器: 小黑
        // Dog两参构造器
    }
}
```

## 四、内存层面的区别

### 内存布局示意图
```
Dog对象在堆内存中：
┌─────────────────────────────────┐
│          Dog对象实例              │
├─────────────────────────────────┤
│ 对象头 (Object Header)           │
├─────────────────────────────────┤
│ 父类Animal的字段:                │
│   - Animal.name                 │ ← super.name指向这里
├─────────────────────────────────┤
│ 子类Dog的字段:                   │
│   - Dog.breed                   │ ← this.breed指向这里
│   - Dog.name (如果定义了)        │ ← this.name指向这里
└─────────────────────────────────┘
↑
this指向整个对象
super只指向父类部分
```

## 五、实际应用场景

### 场景1：方法重写时保留父类功能
```java
class DatabaseLogger {
    public void log(String message) {
        // 基础日志逻辑
        System.out.println("记录到数据库: " + message);
    }
}

class EnhancedLogger extends DatabaseLogger {
    @Override
    public void log(String message) {
        // 1. 先执行父类的基础功能
        super.log(message);
        
        // 2. 添加增强功能
        System.out.println("同时记录到文件: " + message);
        System.out.println("发送告警通知: " + message);
    }
}
```

### 场景2：解决命名冲突
```java
class Shape {
    protected int x, y;
    
    public void draw() {
        System.out.println("在(" + x + "," + y + ")绘制形状");
    }
}

class Circle extends Shape {
    private int x, y;  // 圆心坐标（隐藏了父类的x,y）
    private int radius;
    
    @Override
    public void draw() {
        // 使用父类的x,y作为基准点
        super.draw();
        
        // 使用子类的x,y作为圆心
        System.out.println("绘制圆形: 圆心(" + this.x + "," + this.y + 
                         "), 半径" + radius);
    }
    
    public void move(int dx, int dy) {
        // 同时移动父类基准点和子类圆心
        super.x += dx;  // 父类的x
        super.y += dy;  // 父类的y
        this.x += dx;   // 子类的x
        this.y += dy;   // 子类的y
    }
}
```

### 场景3：链式调用
```java
class QueryBuilder {
    private String sql = "";
    
    public QueryBuilder select(String columns) {
        this.sql += "SELECT " + columns;
        return this;  // 返回this实现链式调用
    }
    
    public QueryBuilder from(String table) {
        this.sql += " FROM " + table;
        return this;
    }
    
    public QueryBuilder where(String condition) {
        this.sql += " WHERE " + condition;
        return this;
    }
    
    public String build() {
        return this.sql;
    }
}

// 使用链式调用
String sql = new QueryBuilder()
    .select("id, name, age")
    .from("users")
    .where("age > 18")
    .build();
```

## 六、常见误区与注意事项

### 误区1：在静态上下文中使用
```java
class Example {
    int instanceVar = 10;
    static int staticVar = 20;
    
    public static void staticMethod() {
        // System.out.println(this.instanceVar);  // 错误！
        // System.out.println(super.toString());  // 错误！
        System.out.println(staticVar);  // 正确
    }
    
    public void instanceMethod() {
        System.out.println(this.instanceVar);  // 正确
        // System.out.println(super.toString());  // 如果Example有父类，正确
    }
}
```

### 误区2：无限递归
```java
class RecursiveExample {
    public void methodA() {
        this.methodA();  // 无限递归！
    }
    
    public void methodB() {
        super.toString();  // 正确，调用Object.toString()
    }
}
```

### 误区3：错误的构造器调用
```java
class Base {
    public Base(int x) {
        System.out.println("Base构造器: " + x);
    }
}

class Derived extends Base {
    public Derived() {
        // super();  // 错误！Base没有无参构造器
        super(10);  // 正确！必须显式调用父类有参构造器
    }
    
    public Derived(int x) {
        this();     // 正确！调用本类无参构造器
        // super(x); // 错误！不能同时用this()和super()
    }
}
```

## 七、综合示例

```java
class Employee {
    private String name;
    private double salary;
    
    public Employee(String name, double salary) {
        this.name = name;
        this.salary = salary;
    }
    
    public void showInfo() {
        System.out.println("员工: " + name + ", 薪资: " + salary);
    }
    
    public final String getName() {
        return this.name;
    }
}

class Manager extends Employee {
    private double bonus;
    private String name;  // 隐藏父类的name
    
    public Manager(String name, double salary, double bonus) {
        super(name, salary);  // 初始化父类部分
        this.name = "经理-" + name;  // 初始化子类name
        this.bonus = bonus;
    }
    
    @Override
    public void showInfo() {
        // 调用父类方法显示基本信息
        super.showInfo();
        
        // 添加经理特有信息
        System.out.println("职位: 经理");
        System.out.println("奖金: " + bonus);
        System.out.println("总薪酬: " + (bonus + 0));  // 注意：不能直接访问父类私有salary
        
        // 显示不同的name
        System.out.println("员工名册: " + super.getName());  // 父类的name
        System.out.println("办公室门牌: " + this.name);     // 子类的name
    }
    
    public void showAllNames() {
        // 各种访问name的方式
        System.out.println("1. name: " + name);           // 子类name
        System.out.println("2. this.name: " + this.name); // 子类name
        System.out.println("3. getName(): " + getName()); // 父类name（通过方法）
        System.out.println("4. super.getName(): " + super.getName()); // 父类name
    }
}

public class Test {
    public static void main(String[] args) {
        Manager mgr = new Manager("张三", 10000, 5000);
        mgr.showInfo();
        System.out.println("\n=== 访问所有name ===");
        mgr.showAllNames();
    }
}
```

## 八、总结表格

| 方面 | **this** | **super** |
|------|----------|-----------|
| **主要用途** | 访问当前对象的成员 | 访问父类的成员 |
| **可访问范围** | 本类所有可见成员 | 父类中非private成员 |
| **构造器中** | this()调用本类其他构造器 | super()调用父类构造器 |
| **位置限制** | 必须在构造器第一行（如果是this()） | 必须在构造器第一行（如果是super()） |
| **静态方法** | 不可使用 | 不可使用 |
| **返回类型** | 返回当前对象引用 | 无返回类型概念 |
| **内存指向** | 整个对象 | 对象的父类部分 |
| **多态影响** | 不影响，指向实际对象 | 不影响，指向父类部分 |
| **链式调用** | 支持（return this） | 不支持 |

**核心记忆点：**
- `this`代表"我这个对象"，`super`代表"我里面的父类部分"
- 字段访问看类型（编译时决定），方法调用看对象（运行时决定）
- 构造器中`this()`和`super()`必须第一行，且不能同时存在
- 使用`super`主要是为了：①调用被重写的方法 ②访问被隐藏的字段 ③调用父类构造器