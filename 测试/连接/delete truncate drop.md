在 MySQL 中，**DELETE、TRUNCATE、DROP** 都和“删除”有关，但**删除的对象、力度、是否可恢复**完全不同。下面用**对比 + 示例**帮你一次搞清楚 👍

---

## 一、DELETE —— 删除**表中数据**

👉 **表结构还在**

### 用法

```sql
DELETE FROM 表名;
DELETE FROM 表名 WHERE 条件;
```

### 示例

```sql
-- 删除 emp 表中 eid=101 的记录
DELETE FROM emp WHERE eid = 101;

-- 删除 emp 表中所有数据
DELETE FROM emp;
```

### 特点

- ✔ 可以加 `WHERE`
    
- ✔ **逐行删除**
    
- ✔ 可回滚（在事务中）
    
- ❌ **不会重置 AUTO_INCREMENT**
    
- ❌ 大数据量时较慢
    

---

## 二、TRUNCATE —— 清空**表中所有数据**

👉 **表结构还在**

### 用法

```sql
TRUNCATE TABLE 表名;
```

### 示例

```sql
TRUNCATE TABLE emp;
```

### 特点

- ❌ **不能加 WHERE**
    
- ✔ 删除所有数据
    
- ✔ **重置 AUTO_INCREMENT**
    
- ✔ 速度快（相当于重建表）
    
- ❌ 不能回滚
    
- ❌ 不触发 DELETE 触发器
    

---

## 三、DROP —— 删除**整张表**

👉 **表结构 + 数据全部删除**

### 用法

```sql
DROP TABLE 表名;
```

### 示例

```sql
DROP TABLE emp;
```

### 特点

- ❌ 表直接没了
    
- ❌ 不能回滚
    
- ❌ 数据、结构、索引、约束全部删除
    
- ✔ 最彻底
    

---

## 四、三者对比（重点）

| 对比项            | DELETE | TRUNCATE | DROP   |
| -------------- | ------ | -------- | ------ |
| 删除内容           | 表中数据   | 表中全部数据   | 表 + 数据 |
| WHERE 条件       | ✅ 可以   | ❌ 不行     | ❌ 不行   |
| 表结构            | 保留     | 保留       | ❌ 删除   |
| AUTO_INCREMENT | ❌ 不重置  | ✅ 重置     | ❌      |
| 回滚             | ✅（事务中） | ❌        | ❌      |
| 执行速度           | 慢      | 快        | 最快     |

---

## 五、什么时候用哪个？

- 🔹 **删部分数据** → `DELETE`
    
- 🔹 **清空表，重新开始** → `TRUNCATE`
    
- 🔹 **表都不要了** → `DROP`
    

---

## 六、常见面试一句话总结

> DELETE 是“删数据”，TRUNCATE 是“清空表”，DROP 是“删表”。
