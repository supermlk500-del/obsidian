很好 👍  
既然你已经理解了 HashSet，我们现在直接上 **源码级讲解 LinkedHashSet**。

主角：

- **LinkedHashSet**
    
- **HashSet**
    
- **LinkedHashMap**
    
- **HashMap**
    

---

# 一、LinkedHashSet 本质一句话

```text
LinkedHashSet = HashSet + 双向链表（保证有序）
```

它的底层不是 HashMap，而是：

```text
LinkedHashMap
```

---

# 二、LinkedHashSet 核心源码

来看 JDK8 精简源码。

## ① 类定义

```java
public class LinkedHashSet<E>
    extends HashSet<E>
    implements Set<E>, Cloneable, java.io.Serializable {
```

你看到关键点了吗？

```text
LinkedHashSet 继承 HashSet
```

它并没有自己实现 add。

---

## ② 构造方法（关键）

```java
public LinkedHashSet() {
    super(16, .75f, true);
}
```

注意这个 super。

我们进入 HashSet。

---

# 三、HashSet 的特殊构造器

在 HashSet 中有一个“包级构造方法”：

```java
HashSet(int initialCapacity,
        float loadFactor,
        boolean dummy) {
    map = new LinkedHashMap<>(initialCapacity, loadFactor);
}
```

看到没有？

```text
当 dummy = true
底层使用 LinkedHashMap
```

这就是核心。

---

# 四、结构关系图

```text
LinkedHashSet
    ↓ 继承
HashSet
    ↓ 持有
LinkedHashMap
    ↓ 继承
HashMap
```

所以：

```text
LinkedHashSet = LinkedHashMap 只使用 key
```

---

# 五、LinkedHashMap 底层结构

关键类：

```java
static class Entry<K,V> extends HashMap.Node<K,V> {
    Entry<K,V> before, after;
}
```

你看到了什么？

比 HashMap 的 Node 多了两个指针：

```text
before
after
```

---

# 六、真正结构图

普通 HashMap：

```text
数组
  ↓
链表
  ↓
红黑树
```

LinkedHashMap：

```text
数组
  ↓
链表 / 红黑树
  ↓
再额外维护一个全局双向链表
```

注意：

这是两个链表体系：

1️⃣ 桶内链表  
2️⃣ 全局双向链表（维护顺序）

---

# 七、添加元素全过程

执行：

```java
set.add("A");
```

本质：

```java
map.put("A", PRESENT);
```

---

## put 执行完成后

LinkedHashMap 会调用：

```java
afterNodeInsertion()
```

源码：

```java
void afterNodeInsertion(boolean evict) {
    LinkedHashMap.Entry<K,V> last;
    if (accessOrder)
        ...
}
```

默认：

```text
accessOrder = false
```

表示：

```text
按插入顺序排序
```

---

# 八、双向链表维护机制

每次插入新节点时：

```java
linkNodeLast(p);
```

源码逻辑：

```java
last.after = p;
p.before = last;
last = p;
```

维护：

```text
head <-> node1 <-> node2 <-> node3 <-> tail
```

---

# 九、为什么可以保持插入顺序？

因为：

```text
遍历时不是遍历数组
而是从 head 顺着 after 指针遍历
```

源码：

```java
public Iterator<K> iterator() {
    return new LinkedKeyIterator();
}
```

LinkedKeyIterator 底层：

```java
next = head;
next = next.after;
```

---

# 十、accessOrder 模式（高级点）

LinkedHashMap 有个构造参数：

```java
LinkedHashMap(int initialCapacity,
              float loadFactor,
              boolean accessOrder)
```

如果：

```text
accessOrder = true
```

表示：

```text
访问顺序排序
```

每次 get 后：

```java
afterNodeAccess()
```

会把节点移动到尾部。

这就是：

```text
LRU 缓存机制的核心
```

---

# 十一、扩容时会不会破坏顺序？

不会。

原因：

- 数组扩容只影响桶结构
    
- 全局双向链表不动
    

所以顺序永远稳定。

---

# 十二、时间复杂度

|操作|时间|
|---|---|
|add|O(1)|
|remove|O(1)|
|contains|O(1)|
|遍历|O(n)|

与 HashSet 相同。

只是多了维护链表的常数开销。

---

# 十三、内存对比

HashMap Node：

```text
hash
key
value
next
```

LinkedHashMap Entry：

```text
hash
key
value
next
before
after
```

多两个指针。

内存开销更大。

---

# 十四、红黑树情况下呢？

当链表树化时：

```java
TreeNode extends LinkedHashMap.Entry
```

即：

```text
红黑树节点 = 双向链表节点 + 树结构
```

所以：

即使树化，顺序仍然保持。

---

# 十五、完整运行流程总结

```text
1. 计算 hash
2. 定位数组索引
3. 桶内冲突处理（链表/红黑树）
4. 插入成功后
5. 加入全局双向链表尾部
6. size++
7. 判断扩容
```

---

# 十六、HashSet vs LinkedHashSet 对比

|特性|HashSet|LinkedHashSet|
|---|---|---|
|有序|❌|✅|
|底层|HashMap|LinkedHashMap|
|额外结构|无|双向链表|
|内存占用|小|较大|
|性能|略快|略慢|

---

# 十七、面试级问题

### 1️⃣ 为什么 LinkedHashSet 比 HashSet 慢一点？

因为：

```text
每次插入需要维护双向链表
```

---

### 2️⃣ 为什么扩容不影响顺序？

因为顺序由：

```text
全局双向链表
```

决定。

---

### 3️⃣ 为什么可以做 LRU？

因为：

```text
accessOrder + afterNodeAccess()
```

自动把访问节点移到尾部。

---

# 十八、终极总结

```text
LinkedHashSet = HashSet + 双向链表
本质是 LinkedHashMap 只用 key
通过 before/after 维护全局插入顺序
```

---

如果你愿意，下一步我可以：

- 给你手写一个简化版 LinkedHashSet
    
- 或者画出完整“数组 + 桶链表 + 全局链表”结构图
    
- 或者讲 TreeSet（红黑树）形成三大 Set 对比
    

你现在已经进入集合底层高级理解阶段了。