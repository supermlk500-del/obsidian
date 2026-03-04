好，这次我们直接按照 **JDK8 的真实核心源码结构** 来讲。

主角是：

- **HashSet**
    
- **HashMap**
    

因为：

> HashSet 底层 = HashMap

我会：

1️⃣ 先列出核心源码（精简版）  
2️⃣ 再逐行解释

---

# 一、HashSet 核心源码

## ① 成员变量

```java
public class HashSet<E> extends AbstractSet<E>
    implements Set<E>, Cloneable, java.io.Serializable {

    private transient HashMap<E,Object> map;

    private static final Object PRESENT = new Object();
}
```

---

## ② 构造方法

```java
public HashSet() {
    map = new HashMap<>();
}
```

---

## ③ add 方法（核心）

```java
public boolean add(E e) {
    return map.put(e, PRESENT) == null;
}
```

---

## ④ remove 方法

```java
public boolean remove(Object o) {
    return map.remove(o) == PRESENT;
}
```

---

## ⑤ contains 方法

```java
public boolean contains(Object o) {
    return map.containsKey(o);
}
```

---

# 二、第一层解释（HashSet 到 HashMap）

## add 的真正执行逻辑：

```java
set.add("java");
```

等价于：

```java
map.put("java", PRESENT);
```

所以：

```text
HashSet 存的是 key
value 永远是固定对象 PRESENT
```

---

# 三、真正核心：HashMap 的 put 源码

现在进入最关键的源码：

```java
public V put(K key, V value) {
    return putVal(hash(key), key, value, false, true);
}
```

---

## ① 计算 hash

```java
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

### 解释

```text
扰动函数 = hashCode ^ (hashCode >>> 16)
```

目的：

- 让高 16 位参与运算
    
- 降低 hash 冲突
    

---

# 四、真正核心方法：putVal

```java
final V putVal(int hash, K key, V value,
               boolean onlyIfAbsent,
               boolean evict) {

    Node<K,V>[] tab;
    Node<K,V> p;
    int n, i;

    // ① 如果数组为空，初始化
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;

    // ② 计算索引位置
    if ((p = tab[i = (n - 1) & hash]) == null)

        // ③ 当前位置为空，直接放入
        tab[i] = newNode(hash, key, value, null);

    else {

        Node<K,V> e; K k;

        // ④ 判断是否 key 相等
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))

            e = p;

        // ⑤ 红黑树情况
        else if (p instanceof TreeNode)

            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);

        // ⑥ 链表情况
        else {
            for (int binCount = 0; ; ++binCount) {

                if ((e = p.next) == null) {
                    p.next = newNode(hash, key, value, null);

                    // ⑦ 链表长度 >= 8 变红黑树
                    if (binCount >= TREEIFY_THRESHOLD - 1)
                        treeifyBin(tab, hash);

                    break;
                }

                if (e.hash == hash &&
                    ((k = e.key) == key ||
                     (key != null && key.equals(k))))
                    break;

                p = e;
            }
        }

        // ⑧ 已存在 key，替换
        if (e != null) {
            V oldValue = e.value;
            e.value = value;
            return oldValue;
        }
    }

    // ⑨ size++
    ++size;

    // ⑩ 判断是否扩容
    if (size > threshold)
        resize();

    return null;
}
```

---

# 五、根据源码完整执行流程讲解

我们执行：

```java
set.add("java");
```

---

## 第一步：调用 put

```java
put(hash("java"), "java", PRESENT)
```

---

## 第二步：计算 hash

```java
h = "java".hashCode()
hash = h ^ (h >>> 16)
```

---

## 第三步：计算数组索引

```java
index = (n - 1) & hash
```

为什么这样写？

因为数组长度一定是 2 的幂。

例如：

```text
n = 16
n - 1 = 15 = 1111（二进制）
```

按位与运算等价于取模，但更快。

---

## 第四步：判断当前位置

### 情况 1：为空

直接创建 Node 放进去。

```java
tab[index] = newNode(...)
```

---

### 情况 2：不为空

进入冲突逻辑。

---

## 第五步：冲突处理

### 1️⃣ hash 相同 + equals 相同

认为重复 → 不添加

---

### 2️⃣ 链表

遍历链表：

- 找到相同 → 不添加
    
- 找不到 → 插入尾部
    

---

### 3️⃣ 链表长度 ≥ 8

触发：

```java
treeifyBin()
```

链表 → 红黑树

---

# 六、扩容源码

```java
if (size > threshold)
    resize();
```

threshold 默认：

```text
capacity × 0.75
```

默认：

```text
16 × 0.75 = 12
```

添加第 13 个元素触发扩容。

---

## resize 核心逻辑

```java
newCap = oldCap << 1;
```

容量 × 2

然后：

- 所有元素重新计算 index
    
- 重新分布
    

---

# 七、Node 结构

```java
static class Node<K,V> implements Map.Entry<K,V> {
    final int hash;
    final K key;
    V value;
    Node<K,V> next;
}
```

这就是链表节点。

---

# 八、红黑树节点

```java
static final class TreeNode<K,V> extends LinkedHashMap.Entry<K,V> {
    TreeNode<K,V> parent;
    TreeNode<K,V> left;
    TreeNode<K,V> right;
    boolean red;
}
```

---

# 九、整个底层结构总结

```text
HashSet
   ↓
HashMap
   ↓
Node[] table
   ↓
单节点
   ↓
链表
   ↓
红黑树
```

---

# 十、最核心底层机制总结（源码级）

1. hashCode 计算
    
2. 扰动函数
    
3. 位运算取索引
    
4. 冲突判断 equals
    
5. 链表追加
    
6. ≥8 树化
    
7. 超过 threshold 扩容
    
8. 扩容重算位置
    

---

如果你愿意，下一步我可以：

- 带你画一张“添加一个元素的完整底层执行流程图”
    
- 手写一个简易版 HashSet 模拟实现
    
- 或者出 5 道源码级面试题
    

你现在已经进入“真正理解集合底层”的阶段了，这部分学扎实非常值。