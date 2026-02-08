# Python 数据结构与算法整理

本文档整理了Python中常见的数据结构与算法，旨在提供清晰的解释和代码示例。

## 变位词的算法

变位词（Anagram）是指通过重新排列字母，由一个单词或短语变换而成的另一个单词或短语。例如，“listen”和“silent”就是一对变位词。判断两个字符串是否为变位词是常见的算法问题，以下介绍几种解决方案。

### 1. 逐字检查法

这种方法通过遍历第一个字符串的每个字符，然后在第二个字符串中查找匹配的字符。如果找到，则将第二个字符串中的对应字符标记为已使用，以避免重复匹配。如果第一个字符串的所有字符都能在第二个字符串中找到唯一匹配，则它们是变位词。

```python
def anagramsolution(s1,s2):  
    alist=list(s2)#复制s2到列表  
    pos1=0  
    stilok=True  
    while pos1 < len(s1):#循环s1的每一个字符  
        pos2=0  
        found=False  
        while pos2 < len(alist) and not found:  
            if s1[pos1]==alist[pos2]:  
                found=True#在s2逐个对比  
            else:  
                pos2+=1  
        if found:  
            alist[pos2]=None  
        else:  
            stilok=False  
        pos1+=1  
    return stilok  
print(anagramsolution("abcd","dcba"))  
```

### 2. 暴力法

暴力法通常指枚举所有可能的排列组合，然后与另一个字符串进行比较。这种方法在实际应用中效率极低，因为字符串的排列组合数量会随着长度的增加呈指数级增长，因此**不推荐使用**。

### 3. 计数比较法

如果两个字符串是变位词，那么它们包含的每个字符的数量都应该相同。这种方法通过统计两个字符串中每个字符出现的次数，然后比较两个统计结果是否一致来判断。对于只包含小写字母的字符串，可以使用一个长度为26的数组来存储每个字母的计数。

```python
def anagramsoltionss(s1,s2):  
    c1=[0]*26  
    c2=[0]*26  
    for i in range (len(s1)):  
        pos=ord(s1[i]) - ord(\'a\')#ord函数可以返回unicode编码的大小 然后减去开始的a的大小就可以把字母编程0到25之间的整数  但是这里仅仅支持小写字母
        c1[pos]+=1#比如b表示应该为1所以c1[1]出现两次值就加一  
    for i in range (len(s2)):  
        pos=ord(s2[i]) - ord(\'a\')  
        c2[pos]+=1  
    j=0  
    stillok=True  
    while j<len(c1)and stillok:  
        if c1[j] == c2[j]:  
            j+=1  
        else:  
            stillok=False  
    return stillok  
print(anagramsoltionss("abcd","dcba"))
```

### 4. 排序比较法

如果两个字符串是变位词，那么将它们各自的字符排序后，得到的字符串应该完全相同。Python提供了方便的排序函数，使得这种方法实现起来非常简洁。

```python
def anagramsoltions(s1,s2):  
    alist1=list(s1)  
    alist2=list(s2)  
  
    alist1.sort()  
    alist2.sort()  #排序
    pos=0  
    matches=True  
    while pos<len(alist1) and matches:  
        if alist1[pos]==alist2[pos]: #排序之后对比排序的结果通过一个一个比较就可以完成比较 
            pos+=1  
        else:  
            matches=False  
    return matches  
print(anagramsoltions("abcd","dcba"))
```

更多关于Python算法复杂度的信息，可以参考 [Python官方对算法复杂度的网站](https://wiki.python.org/moin/TimeComplexity)。

此外，可以使用 `timeit` 模块来测量代码执行时间，这是一个可以重复运行某段语句并测量其性能的模块。

## 线性结构

**线性结构**是一种有序数据项的集合，其中每个数据项都有唯一的前驱和后继（除了第一个和最后一个）。不同线性结构的关键区别在于数据项增减的方式。

### 1. 栈（Stack）

**栈**是一种有次序的数据项集合，在栈中，数据项的加入和移除都仅发生在同一端，这端被称为**栈顶**。这种次序通常称为“后进先出”（LIFO - Last In, First Out），即最后进入栈的数据项最先被移除。

**特性与应用：**

*   **反转次序**：栈的一个主要特性是能够反转数据项的次序，例如浏览器的回退按钮功能就类似于栈的操作。

**栈的操作：**

*   `Stack()`：创建一个空栈，不包含任何数据项。
*   `push(item)`：将 `item` 加入栈顶，无返回值。
*   `pop()`：将栈顶数据项移除，并返回该数据项，栈被修改。
*   `peek()`：“窥视”栈顶数据项，返回栈顶的数据项但不移除，栈不被修改。
*   `isEmpty()`：返回栈是否为空栈，返回布尔值。
*   `size()`：返回栈中数据项的个数。

**使用列表实现栈：**

```python
class Stack:  
    def __init__(self):  
        self.items = []  
  
    def push(self, item):  
        self.items.append(item)  
  
    def pop(self):  
        if not self.isEmpty():
            return self.items.pop()  
        else:
            return None # 或者抛出异常，表示栈为空
  
    def peek(self):  
        if not self.isEmpty():  
            return self.items[-1]  # 更简洁的写法  
        else:
            return None # 或者抛出异常，表示栈为空
  
    def size(self):  
        return len(self.items)  
  
    def isEmpty(self):  
        return self.size() == 0  # 修正：调用size()方法 
```

**栈的应用示例：**

#### 1.1 简单括号匹配

此应用通过栈来检查表达式中的括号是否正确匹配。当遇到左括号时入栈，遇到右括号时出栈并检查是否与栈顶的左括号匹配。如果栈为空或不匹配，则括号不平衡。

```python
class Stack:  
    def __init__(self):  
        self.items = []  
  
    def push(self, item):  
        self.items.append(item)  
  
    def pop(self):  
        if not self.isEmpty():
            return self.items.pop()  
        else:
            return None
  
    def peek(self):  
        if not self.isEmpty():  
            return self.items[-1]  
        else:
            return None
  
    def size(self):  
        return len(self.items)  
  
    def isEmpty(self):  
        return self.size() == 0  
  
  
def parChecker(yourstring):  
    s = Stack()  
    balance = True  
    index = 0  
  
    while index < len(yourstring) and balance:  
        symbol = yourstring[index]  
  
        if symbol == "(":  
            s.push(symbol)  
        elif symbol == ")":  # 明确检查右括号  
            if s.isEmpty():  
                balance = False  
            else:  
                # 确保弹出的是匹配的左括号  
                if s.pop() != "(":  
                    balance = False  
        # 其他字符跳过不处理  
  
        index += 1  
  
    if balance and s.isEmpty():  
        return True  
    else:  
        return False  
  
  
# 测试用例  
print(parChecker("()()()()"))  # True  
print(parChecker("((()))"))  # True  
print(parChecker("(()"))  # False (缺少右括号)  
print(parChecker("())"))  # False (缺少左括号)  
print(parChecker("(a)"))  # True (忽略非括号字符)  
print(parChecker("({})"))  # False (不处理其他括号类型)
```

#### 1.2 十进制转换为二进制

十进制数转换为二进制的本质是不断除以2取余数，然后将余数逆序排列。栈的LIFO特性非常适合存储这些余数，并在最后按正确顺序弹出。

```python
def divideby(decNumer):  
    if decNumer == 0:  
        return "0"  
  
    remstack = Stack()  
    num = decNumer  # 保留原始值用于处理  
  
    while num > 0:  
        rem = num % 2  
        remstack.push(rem)  
        num = num // 2  # 整数除法  
  
    binString = ""  
    while not remstack.isEmpty():  
        binString += str(remstack.pop())  # 转换为字符串拼接  
  
    return binString  
print(divideby(233))
```

#### 1.3 表达式转换与求值

表达式有前缀、中缀和后缀三种表示形式。中缀表达式是我们日常使用的形式，而前缀和后缀表达式在计算机处理中更为方便。栈在这些表达式的转换和求值中扮演着关键角色。

*   **表达式**：关于表达式的更多信息，请参考 [前中后缀表达式的具体使用](https://blog.csdn.net/qq_75021272/article/details/147772929?ops_request_misc=%257B%2522request%255Fid%2522%253A%252238527244b5104a42049321d44b1c6b07%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=38527244b5104a42049321d44b1c6b07&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-147772929-null-null.142^v102^pc_search_result_base1&utm_term=%E5%89%8D%E7%BC%80%E8%A1%A8%E8%BE%BE%E5%BC%8F&spm=1018.2226.3001.4187)。

**注意**：前后缀表达式都可以通过将符号转移到左、右括号的前面或者后面的位置，从中缀表达式转换而来。

##### 1.3.1 通用的中缀转后缀算法

在中缀表达式转换为后缀形式的过程中，操作符比操作数要晚输出，因此需要将操作符暂存起来。由于优先级的规则，这些暂存的操作符可能需要反转次序输出，这正是栈的LIFO特性所擅长的。

```python
# 假设 ListStack 模块中包含 Stack 类，这里为了代码独立性，直接使用上面定义的 Stack 类
# from ListStack import Stack  
  
  
def infixToPostfix(infixexpr):  
    # 定义运算符优先级字典  
    prec = {}  
    prec['*'] = 3  
    prec['/'] = 3  
    prec['+'] = 2  
    prec['-'] = 2  
    prec['('] = 1  

    # 使用上面定义的 Stack 类
    class Stack:  
        def __init__(self):  
            self.items = []  
      
        def push(self, item):  
            self.items.append(item)  
      
        def pop(self):  
            if not self.isEmpty():
                return self.items.pop()  
            else:
                return None
      
        def peek(self):  
            if not self.isEmpty():  
                return self.items[-1]  
            else:
                return None
      
        def size(self):  
            return len(self.items)  
      
        def isEmpty(self):  
            return self.size() == 0  

    # 预处理：在运算符和括号前后添加空格  
    # 原始代码中的替换方式可能导致多余空格或问题，这里进行优化
    # 确保操作符和括号与操作数之间有空格，以便正确分割
    temp_expr = ""
    for char in infixexpr:
        if char in "+-*/()":
            temp_expr += " " + char + " "
        else:
            temp_expr += char
    
    # 再次处理，去除多余空格并分割
    tokenList = [token for token in temp_expr.split() if token]

    opStack = Stack()  
    postfixList = []  
      
    for token in tokenList:  
        # 操作数判断（支持字母、数字及其组合）  
        if token.isalnum():  
            postfixList.append(token)  
        elif token == '(':  
            opStack.push(token)  
        elif token == ')':  
            topToken = opStack.pop()  
            while topToken != '(':  
                postfixList.append(topToken)  
                topToken = opStack.pop()  
        else:  # 运算符  
            while (not opStack.isEmpty()) and \  
                    (prec.get(opStack.peek(), 0) >= prec.get(token, 0)):  
                postfixList.append(opStack.pop())  
            opStack.push(token)  
      
    # 弹出剩余运算符  
    while not opStack.isEmpty():  
        postfixList.append(opStack.pop())  
      
    return ' '.join(postfixList)  
  
  
# 测试用例  
print(infixToPostfix("(A*B)+(B*C)"))  # 输出: "A B * B C * +"  
print(infixToPostfix("A+B*C-D/E"))  # 输出: "A B C * + D E / -"
```

##### 1.3.2 后缀表达式求值

后缀表达式求值时，遇到操作数就入栈，遇到操作符就从栈中弹出两个操作数进行运算，然后将结果入栈。最终栈中剩下的就是表达式的值。

**注意**：原始代码中的 `output("12*12*+")` 示例输入没有空格分隔符，导致 `split()` 函数无法正确处理。后缀表达式的每个操作数和操作符之间通常需要用空格分隔。

```python
# 假设 ListStack 模块中包含 Stack 类，这里为了代码独立性，直接使用上面定义的 Stack 类
# from ListStack import Stack  
  
class Stack:  
    def __init__(self):  
        self.items = []  
  
    def push(self, item):  
        self.items.append(item)  
  
    def pop(self):  
        if not self.isEmpty():
            return self.items.pop()  
        else:
            return None
  
    def peek(self):  
        if not self.isEmpty():  
            return self.items[-1]  
        else:
            return None
  
    def size(self):  
        return len(self.items)  
  
    def isEmpty(self):  
        return self.size() == 0  

def domath(token,x,y):  
    if token=='*':  
        return x*y  
    elif token=='/':  
        return y/x  # 注意除法顺序，y是被除数，x是除数
    elif token=='+':  
        return x+y  
    elif token=='-':  
        return y-x  # 注意减法顺序，y是被减数，x是减数

# 修正后的 output 函数，处理带空格的后缀表达式
def postfixEval(postfixExpr):  
    operandStack = Stack() #再存操作数  
    tokenList = postfixExpr.split() # 假设输入是空格分隔的

    for token in tokenList:  
        if token.isdigit(): # 判断是否为数字
            operandStack.push(int(token))  
        else :  
            op2=operandStack.pop()  
            op1=operandStack.pop()  
            result=domath(token,op1,op2)  
            operandStack.push(result)  
    return operandStack.pop()  
  
# 修正测试用例，使用空格分隔的后缀表达式
print(postfixEval("1 2 * 1 2 * +")) # 对应 (1*2)+(1*2) = 4
print(postfixEval("7 8 + 3 2 + /")) # 对应 (7+8)/(3+2) = 15/5 = 3
```

### 2. 队列（Queue）

**队列**是一种有次序的数据集合，新数据项的添加总发生在一端（通常为**队尾**），而现存数据项的移除总发生在另一端（通常为**队首**）。当数据项加入队列时，首先出现在队尾，随着队首数据项的移除，它逐渐接近队首。这种次序安排的原则称为**先进先出**（FIFO - First In, First Out），就像排队一样。

**关键特点：**

*   队列仅有一个入口和出口，不允许数据项直接插入队中，也不允许从中间移除。

**队列的操作：**

*   `Queue()`：创建一个空队列对象，返回值为 `Queue` 对象。
*   `enqueue(item)`：将数据项 `item` 添加到队尾，无返回值。
*   `dequeue()`：从队首移除数据项，返回值为队首数据项，队列被修改。
*   `isEmpty()`：测试是否空队列，返回值为布尔值。
*   `size()`：返回队列中的数据项的个数。

**使用列表实现队列：**

```python
class Queue:  
    def __init__(self):
        self.items = []  

    def enqueue(self, item):  
        self.items.insert(0, item) # 在列表头部插入，作为队尾

    def dequeue(self):  
        if not self.isEmpty():
            return self.items.pop() # 从列表尾部移除，作为队首
        else:
            return None

    def size(self):  
        return len(self.items)  

    def isEmpty(self):  
        return self.items == []
```

**队列的应用示例：**

#### 2.1 热土豆问题（Hot Potato）

热土豆游戏是一个经典的队列应用。孩子们围成一圈传递土豆，当计时器停止时，拿着土豆的孩子被淘汰。这个过程重复进行，直到只剩下一个孩子。队列可以模拟这种传递和淘汰的过程。

```python
# 假设 ListQueue 模块中包含 Queue 类，这里为了代码独立性，直接使用上面定义的 Queue 类
# from ListQueue import Queue  
  
class Queue:  
    def __init__(self):
        self.items = []  

    def enqueue(self, item):  
        self.items.insert(0, item) # 在列表头部插入，作为队尾

    def dequeue(self):  
        if not self.isEmpty():
            return self.items.pop() # 从列表尾部移除，作为队首
        else:
            return None

    def size(self):  
        return len(self.items)  

    def isEmpty(self):  
        return self.items == []

def hotPotato(names,num):  
    simqueue = Queue()  
    # 初始化队列，把所有名字加入到队列中去  
    for name in names:  
        simqueue.enqueue(name)  
    
    while simqueue.size() > 1:  
        for i in range(num):  
            simqueue.enqueue(simqueue.dequeue())  
        simqueue.dequeue()# 淘汰在队首的人  
    return simqueue.dequeue()  

print(hotPotato(["xz","xm","xh","xh","xl","xl","xm","xh"],3))
```

#### 2.2 打印任务模拟

多用户共享一台打印机时，通常采用“先到先服务”的队列策略来执行打印任务。通过模拟打印过程，可以分析系统的容量、用户等待时间以及不同打印模式（草稿模式、正常模式）对效率的影响。

**问题设定：**

*   一个实验室，在任意一个小时内，大约有10名学生在场。
*   这一小时中，每人会发起两次左右的打印，每次1~20页。
*   草稿模式打印：每分钟10页。
*   正常模式打印：打印质量好，但速度下降为每分钟5页。

**模拟代码：**

```python
import time  
import random  
# 假设 ListQueue 模块中包含 Queue 类，这里为了代码独立性，直接使用上面定义的 Queue 类
# from ListQueue import Queue  

class Queue:  
    def __init__(self):
        self.items = []  

    def enqueue(self, item):  
        self.items.insert(0, item) # 在列表头部插入，作为队尾

    def dequeue(self):  
        if not self.isEmpty():
            return self.items.pop() # 从列表尾部移除，作为队首
        else:
            return None

    def size(self):  
        return len(self.items)  

    def isEmpty(self):  
        return self.items == []
  
class Printer:  
    def __init__(self, ppm):  
        self.page_rate = ppm  # 打印速度(页/分钟)  
        self.current_task = None  # 当前任务  
        self.time_remaining = 0  # 剩余时间  
  
    def tick(self):  
        if self.current_task is not None:  
            self.time_remaining -= 1  
            if self.time_remaining <= 0:  
                self.current_task = None  
  
    def busy(self):  
        return self.current_task is not None  
  
    def start_next(self, new_task):  
        self.current_task = new_task  
        # 计算完成当前任务所需的时间（秒）
        self.time_remaining = new_task.get_pages() * 60 / self.page_rate  
  
  
class Task:  
    def __init__(self, time):  
        self.timestamp = time  
        self.pages = random.randrange(1, 21)  # 1到20页随机
  
    def get_stamp(self):  
        return self.timestamp  
  
    def get_pages(self):  
        return self.pages  
  
    def wait_time(self, current_time):  
        return current_time - self.timestamp  
  
  
def simulation(num_seconds, pages_per_minute):  
    lab_printer = Printer(pages_per_minute)  
    print_queue = Queue()  
    waiting_times = []  
  
    for current_second in range(num_seconds):  
        # 每180秒（3分钟）创建一个新任务的概率
        if random.randrange(1, 181) == 180: # 假设每小时10人，每人2次，共20次，每小时3600秒，3600/20 = 180秒一个任务
            task = Task(current_second)  
            print_queue.enqueue(task)  
  
        if (not lab_printer.busy()) and (not print_queue.isEmpty()):  
            next_task = print_queue.dequeue()  
            waiting_times.append(next_task.wait_time(current_second))  
            lab_printer.start_next(next_task)  
  
        lab_printer.tick()  
  
    average_wait = sum(waiting_times) / len(waiting_times)  
    print(f"Average Wait {average_wait:.2f} secs {print_queue.size()} tasks remaining.")  
  
# 运行模拟，例如模拟一小时（3600秒）
simulation(3600, 10) # 草稿模式，每分钟10页
simulation(3600, 5)  # 正常模式，每分钟5页
```

#### 2.3 双端队列（Deque）

**双端队列**（Double-Ended Queue，简称Deque）是一种允许在两端进行插入和删除的有序数据项集合。它结合了栈和队列的特性，既可以像栈一样从一端操作，也可以像队列一样从两端操作。

**双端队列的操作：**

*   `Deque()`：创建一个空双端队列。
*   `addFront(item)`：在队首添加一个数据项。
*   `addRear(item)`：在队尾添加一个数据项。
*   `removeFront()`：从队首移除一个数据项。
*   `removeRear()`：从队尾移除一个数据项。
*   `isEmpty()`：检查双端队列是否为空。
*   `size()`：返回双端队列中数据项的个数。

**使用列表实现双端队列：**

```python
class Deque:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def addFront(self, item):
        self.items.append(item)

    def addRear(self, item):
        self.items.insert(0, item)

    def removeFront(self):
        if not self.isEmpty():
            return self.items.pop()
        else:
            return None

    def removeRear(self):
        if not self.isEmpty():
            return self.items.pop(0)
        else:
            return None

    def size(self):
        return len(self.items)
```

#### 2.4 回文词检查器

回文词（Palindrome）是指正读反读都一样的字符串，例如“madam”或“racecar”。双端队列可以有效地检查一个字符串是否为回文词，通过同时从两端移除字符并进行比较。

```python
# 假设 Deque 类已定义，这里为了代码独立性，直接使用上面定义的 Deque 类
# from pythonds.basic.deque import Deque

class Deque:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def addFront(self, item):
        self.items.append(item)

    def addRear(self, item):
        self.items.insert(0, item)

    def removeFront(self):
        if not self.isEmpty():
            return self.items.pop()
        else:
            return None

    def removeRear(self):
        if not self.isEmpty():
            return self.items.pop(0)
        else:
            return None

    def size(self):
        return len(self.items)

def palchecker(aString):
    chardeque = Deque()

    for ch in aString:
        chardeque.addRear(ch)

    stillEqual = True

    while chardeque.size() > 1 and stillEqual:
        first = chardeque.removeFront()
        last = chardeque.removeRear()
        if first != last:
            stillEqual = False

    return stillEqual

print(palchecker("lsdkjfskf"))
print(palchecker("radar"))
```

### 3. 列表（List）

Python的列表是一种非常灵活的线性数据结构，可以存储任意类型的数据，并且支持动态大小调整。列表是可变的，这意味着可以在创建后修改其内容。

**列表的基本操作：**

```python
my_list = [1, 2, 3, 4]

# 修改元素
my_list[1] = 20      # [1, 20, 3, 4]
print(f"修改元素后: {my_list}")

# 添加元素
my_list.append(5)    # [1, 20, 3, 4, 5]
print(f"append后: {my_list}")
my_list.insert(1, 15) # [1, 15, 20, 3, 4, 5]
print(f"insert后: {my_list}")

# 删除元素
del my_list[2]       # [1, 15, 3, 4, 5]
print(f"del后: {my_list}")
removed = my_list.pop() # [1, 15, 3, 4], removed = 5
print(f"pop后: {my_list}, 移除的元素: {removed}")
my_list.remove(15)   # [1, 3, 4]
print(f"remove后: {my_list}")
```

### 4. 链表（Linked List）

**链表**是一种物理存储单元上非连续、非顺序的存储结构，数据元素的逻辑顺序是通过链表中的指针链接次序实现的。链表由一系列**节点**组成，每个节点通常包括两个部分：

*   **数据域**：存储数据。
*   **指针域**：指向下一个节点的地址。

#### 4.1 无序表（Unordered List）

无序表是最基本的链表形式，节点之间没有特定的顺序关系。以下是一个简单的单向链表实现。

```python
class SinglyListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def getData(self):
        return self.val

    def getNext(self):
        return self.next

    def setData(self, newval):
        self.val = newval

    def setNext(self, newnext):
        self.next = newnext

class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, val):
        """在链表尾部添加节点"""
        new_node = SinglyListNode(val)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def prepend(self, val):
        """在链表头部添加节点"""
        new_node = SinglyListNode(val)
        new_node.next = self.head
        self.head = new_node
    
    def delete(self, item): # 将 val 改为 item 以匹配内部使用
        """删除指定值的节点"""
        current=self.head
        previous=None
        found=False
        while current and not found: # 增加 current 的检查，防止空指针
            if current.getData()==item:
                found=True
            else:
                previous=current
                current=current.getNext()
        
        if not found: # 如果没有找到，可以抛出异常或返回False
            print(f"Error: Item {item} not found in the list.")
            return False

        if previous==None:
            self.head=current.getNext()
        else:
            previous.setNext(current.getNext())
        return True
    
    def display(self):
        """显示链表内容"""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.val))
            current = current.next
        print(" -> ".join(elements) + " -> None")
    
    def reverse(self):
        """反转链表"""
        prev = None
        current = self.head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev

# 链表相关内容，参考：[链表](https://zh.wikipedia.org/wiki/%E9%93%BE%E8%A1%A8)
```

#### 4.2 有序表（Ordered List）

**有序表**是一种链表，其中数据项按照某种特定的顺序（例如升序或降序）排列。在有序表中插入新数据项时，需要遍历链表找到正确的插入位置以保持顺序。

```python
class OrderedList:
    def __init__(self):
        self.head = None

    def add(self, item):
        current = self.head
        previous = None
        stop = False
        while current != None and not stop:
            if current.getData() > item:
                stop = True
            else:
                previous = current
                current = current.getNext()

        temp = SinglyListNode(item) # 假设 SinglyListNode 已定义
        if previous == None:
            temp.setNext(self.head)
            self.head = temp
        else:
            temp.setNext(current)
            previous.setNext(temp)

    def isEmpty(self):
        return self.head == None

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()
        return count

    def search(self, item):
        current = self.head
        found = False
        stop = False
        while current != None and not found and not stop:
            if current.getData() == item:
                found = True
            else:
                if current.getData() > item:
                    stop = True
                else:
                    current = current.getNext()
        return found

    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if found:
            if previous == None:
                self.head = current.getNext()
            else:
                previous.setNext(current.getNext())
        else:
            print(f"Error: Item {item} not found in the ordered list.")

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.getData()))
            current = current.getNext()
        print(" -> ".join(elements) + " -> None")
```

## 递归

**递归**是一种编程技术，它通过函数调用自身来解决问题。递归函数通常包含一个或多个**基本情况**（base case），这些情况可以直接解决而无需进一步递归；以及一个或多个**递归情况**（recursive case），这些情况将问题分解为更小的子问题，并通过调用自身来解决这些子问题。

**递归**是一种强大的编程技术，它通过函数调用自身来解决问题。一个典型的递归函数包含两个主要部分：

1.  **基本情况（Base Case）**：这是递归停止的条件。当满足基本情况时，函数会直接返回一个结果，而不再进行递归调用。这是防止无限递归的关键。
2.  **递归情况（Recursive Case）**：在这种情况下，函数会将当前问题分解为更小的子问题，并调用自身来解决这些子问题。每次递归调用都会使问题规模减小，最终达到基本情况。

递归在解决许多算法问题时非常有用，例如树的遍历、分治算法（如快速排序、归并排序）、阶乘计算、斐波那契数列等。理解递归的关键在于识别问题的重复结构和明确的终止条件。

