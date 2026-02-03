1. timer对象，指定需要反复运行的语句和只需要运行一次的“安装语句”
2. 然后调用这个对象的timeit方法，其中可以指定反复运行多少次
### 模板
t=timeit("要反复运行的语句","只需要运行一次的安装语句，比如反复运行的语句是一个函数，那么这个安装语句就是这个函数所在的位置，比如在main中")
## 例子

```python
def text1():  
    l = []  
    for i in range(100):  
        l.append(i)  # Efficient O(1) per operation  
  
if __name__ == '__main__':  
    from timeit import timeit  
    # Time the function 1000 times and print results  
    print(timeit("text1()", setup="from __main__ import text1", number=1000))
```
