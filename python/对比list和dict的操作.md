
| 类型  | list                 | dict      |
| --- | -------------------- | --------- |
| 索引  | 自然数                  | 不可变类型值    |
| 添加  | append，extend，insert | b[k]=v    |
| 删除  | pop，remove，          | pop       |
| 更新  | a[i]=v               | b[k]=v    |
| 正查  | a[i],a[i:j]          | b[k],copy |
| 反查  | index(v),count(v)    | 无         |
## 使用列表来实现栈的操作
```python
class Stack:  
    def __init__(self):  
        self.items = []  
    def push(self, item):  
        self.items.append(item)  
    def pop(self):  
        return self.items.pop()  
    def peek(self):  
        return self.items[len(self.items)-1]  
    def size(self):  
        return len(self.items)
```
