## 变位词的算法
### 逐字检查法
从一个字符的第一位开始与第二个字符比较 一旦比较成功就把第二个字符的副本标记为none 之后的比较就不用重复比较了
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
### 暴力法 

也就是暴力枚举 把每一种情况都列举出来 一般不推荐使用
### 计数比较
变位词的比较可以转换为两个字符的字母数量出现的次数
```python
def anagramsoltionss(s1,s2):  
    c1=[0]*26  
    c2=[0]*26  
    for i in range (len(s1)):  
        pos=ord(s1[i]) - ord('a')#ord函数可以返回unicode编码的大小 然后减去开始的a的大小就可以把字母编程0到25之间的整数  但是这里仅仅支持小写字母
        c1[pos]+=1#比如b表示应该为1所以c1[1]出现两次值就加一  
    for i in range (len(s2)):  
        pos=ord(s2[i]) - ord('a')  
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
### 排序比较法
python中有特殊的排序函数可以让字符按照字母表排序
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

python[[python官方对算法复杂的网站]](https://wiki.python.org/moin/TimeComplexity)
* 扩展[[timeit模块]]这是一个可以让某一段语句运行多次的模块
## 线性结构

*  定义：线性结构是一种有序数据项的集合，其中每个数据项都有唯一的前驱和后继（除了第一个和最后一个）
* 不同线性结构的关键区别在于数据项增减的方式
#### 栈Stack
* 一种有次序的数据项集合，在栈中，数据项的加入和一处都仅发生在同一端。这端就叫做栈顶*
* 这种次序通常称为“后进先出LIFO”时间越短的离栈顶越近或反之
1. 特性：反转次序。比如浏览器的回退按钮
2. 栈的操作：
	* stack()：创建一个空栈，不包含任何数据项
	* push(item)：将item加入栈顶，无返回值
	* pop()：将栈顶数据项移除，并返回，栈被修改
	* peek()：“窥视栈顶数据项，返回栈顶的数据项但不移除，栈不被修改”
	* isEmpty()：返回栈是否为空栈
	* size()：返回栈中有多少个数据项
3. 这里有使用列表来实现栈的内容
	```python
class Stack:  
    def __init__(self):  
        self.items = []  
  
    def push(self, item):  
        self.items.append(item)  
  
    def pop(self):  
        return self.items.pop()  
  
    def peek(self):  
        if not self.isEmpty():  
            return self.items[-1]  # 更简洁的写法  
  
    def size(self):  
        return len(self.items)  
  
    def isEmpty(self):  
        return self.size() == 0  # 修正：调用size()方法 
```
4. 栈的应用：
	1.   简单括号匹配
```python
	class Stack:  
    def __init__(self):  
        self.items = []  
  
    def push(self, item):  
        self.items.append(item)  
  
    def pop(self):  
        return self.items.pop()  
  
    def peek(self):  
        if not self.isEmpty():  
            return self.items[-1]  # 更简洁的写法  
  
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
	*思考能不能从中间来判断？*
	2. 十进制转换为二进制
		a. 注意十进制转换成二进制本质上就是十进制数除以二的余数来作为栈底数据项
		b. 具体代码如下
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
[[表达式]]
[前中后缀表达式的具体使用](https://blog.csdn.net/qq_75021272/article/details/147772929?ops_request_misc=%257B%2522request%255Fid%2522%253A%252238527244b5104a42049321d44b1c6b07%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=38527244b5104a42049321d44b1c6b07&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-147772929-null-null.142^v102^pc_search_result_base1&utm_term=%E5%89%8D%E7%BC%80%E8%A1%A8%E8%BE%BE%E5%BC%8F&spm=1018.2226.3001.4187)
*注意前后缀表达式其实都可以使用中缀表达式转换即==把符号转移到左，右括号的前面或者后面的位置==*
2. 通用的中缀转后缀算法
	1. 在中缀表达式转换为后缀形式的处理过程中，操作符比操作数要晚输出——所以在扫描到对应的第二个操作数之前，需要把操作符先保存起来
	2. 而这些暂存的操作符，由于优先级的规则，==还有可能要反转次序输出——这种反转特性，是的我们考虑用栈来保存暂时为处理的操作符==
```python
from ListStack import Stack  
  
  
def infixToPostfix(infixexpr):  
    # 定义运算符优先级字典  
    prec = {}  
    prec['*'] = 3  
    prec['/'] = 3  
    prec['+'] = 2  
    prec['-'] = 2  
    prec['('] = 1  
  
    # 预处理：在运算符和括号前后添加空格  
    infixexpr = infixexpr.replace('(', ' ( ').replace(')', ' ) ')  
    infixexpr = infixexpr.replace('+', ' + ').replace('-', ' - ')  
    infixexpr = infixexpr.replace('*', ' * ').replace('/', ' / ')  
  
    # 初始化数据结构  
    opStack = Stack()  
    postfixList = []  
  
    # 分割并过滤空字符串  
    tokenList = [token for token in infixexpr.split() if token]  
  
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
		3.后置表达式求值 
			* 注意"split()`函数要求输入字符串用空格分隔，但示例输入`"12*12*+"`没有空格分隔符，导致整个字符串被当作单个元素处理。"*
```python
from ListStack import Stack  
  
  
def domath(token,x,y):  
    if token=='*':  
        return x*y  
    elif token=='/':  
        return x/y  
    elif token=='+':  
        return x+y  
    elif token=='-':  
        return x-y  
  
def output(outexpr):  
    operandStack = Stack() #再存操作数  
    for token in outexpr:  
        if token in "0123456789":  
            operandStack.push(int(token))  
        else :  
            x=operandStack.pop()  
            y=operandStack.pop()  
            result=domath(token,x,y)  
            operandStack.push(result)  
    return operandStack.pop()  
  
print(output("12*12*+"))
```
#### 队列 Queue
1. 是一种有次序的数据集合
	1. 新数据项的添加总发生在一端（通常为“尾rear”端）
		1. 而现存数据项的移除总发生在另一端（通常为“首front”端）
	2. 当数据项加入队列，首先出现在队尾，随着队首数据项的移除，它逐渐接近队首 
		- 新加入的数据项必须在数据集末尾等待，而等待时间最长的数据项则是队首
		- 这种次序安排的原则称为先进先出
		- 排队就是例子
		- 队列仅有一个入口和出口——注意不允许数据项直接插入队中，也不允许从中间移除   
2. 操作定义
	1. Queue()：创建一个空队列对象，返回值为Queue对象
	2. enqueue(item)：将数据项item添加到队尾，无返回值
	3. dequeue：从队首移除数据项，返回值为队首数据项，队列被修改
	4. isEmpty：测试是否空队列，返回值为布尔值
	5. size：返回队列中的数据项的个数
3. c采用LIst来实现ADT Queue
```python
class Queue:  
    def __init__(self):  
        self.queue = []  
    def enqueue(self, item):  
        self.queue.append(item)  
    def dequeue(self):  
        return self.queue.pop()  
    def size(self):  
        return len(self.queue)  
    def isEmpty(self):  
        return self.size == []
```
4. 热土豆问题
	1. 按照传递方向从队首传到队尾：队首哪个人始终拥有土豆
	2. 只需要加航队首的人出队，随机在到队尾入队，算是土豆的一次传递：传递num次后，将队首的人移除，不在入队，反复下去知道队列中只剩1人
```python
from ListQueue import Queue  
  
  
def hotPotato(names,num):  
    simqueue = Queue()  
    #初始化队列把所有名字加入到队列中去  
    for name in names:  
        simqueue.enqueue(name)  
        while simqueue.size() > 1:  
            for i in range(num):  
                simqueue.enqueue(simqueue.dequeue())  
            simqueue.dequeue()#淘汰在队首的人  
        return simqueue.dequeue()  
print(hotPotato(["xz","xm","xh","xh","xl","xl","xm","xh"],3))
```
5. 打印任务
	1. 多人共享一台打印机，采取“先到先服务”的队列策略来执行打印任务
	2. 几个问题
		1. 这种打印作业系统的容量有多大
		2. 在能够接受的等待时间内，系统能容纳多少用户以多高频率提交多少打印任务
		3. 实例 怎么样设定打印机的模式，让大家都不会等太久的前提下尽量提高打印质量
		4. 一个实验室，在任意的一个小时内，大约有10名学成在场
		5. 这一小时中，没人会发起两次左右的打印，每次1~20页
		6. 一草稿模式打印的话，每分钟10页
		7. 以正常模式打印的话，打印质量好，但是速度下降为每分钟5页
```python
import time  
import random  
from ListQueue import Queue  
  
  
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
        self.time_remaining = new_task.get_pages() * 60 / self.page_rate  
  
  
class Task:  
    def __init__(self, time):  
        self.timestamp = time  
        self.pages = random.randrange(1, 21)  
  
    def get_stamp(self):  
        return self.timestamp  
  
    def get_pages(self):  
        return self.pages  
  
    def wait_time(self, current_time):  
        return current_time - self.timestamp  
  
  
def new_print_task():  
    return random.randrange(1, 181) == 1  
  
  
def simulation(num_seconds, pages_per_minute):  
    printer = Printer(pages_per_minute)  
    print_queue = Queue()  
    waiting_times = []  
  
    for current_second in range(num_seconds):  
        if new_print_task():  
            print_queue.enqueue(Task(current_second))  
  
        if (not printer.busy()) and (not print_queue.isEmpty()):  
            next_task = print_queue.dequeue()  
            waiting_times.append(next_task.wait_time(current_second))  
            printer.start_next(next_task)  
  
        printer.tick()  
  
    if waiting_times:  # 避免除零错误  
        average_wait = sum(waiting_times) / len(waiting_times)  
        print(f"平均等待时间: {average_wait:.2f}秒，剩余任务: {print_queue.size()}")  
    else:  
        print("没有处理任何任务")  
  
  
# 示例：模拟1小时(3600秒)，打印速度5页/分钟  
simulation(3600, 5)
```
#### 双端队列 Deque
1. 是一种有次序的数据集，在deque中数据项既可以从队首加入，也可以从队尾加入；数据项也可以从两端移除。从某种意义上来说双端队列集成了栈和队列的能力
2. 双端队列不具有内在的lifo后者fifo特性
3. 使用List来实现deque [[双端队列]]
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
        return self.items.pop()  
    def removeRear(self):  
        return self.items.pop(0)  
    def size(self):  
        return len(self.items)
```
	。实现回文词判断的实现
```python
from Listdeque import Deque  
  
  
def palchecker(string):  
    chsrdeque=Deque()  
    for ch in string:  
        chsrdeque.addRear(ch)  
  
    stillEqual=True  
    while chsrdeque.size()>1 and stillEqual:  
        last=chsrdeque.removeRear()  
        first=chsrdeque.removeFront()  
        if first==last:  
            stillEqual=True  
        else:  
            stillEqual=False  
  
    return stillEqual  
  
print(palchecker("上海自来水来自海上"))
```
#### 列表 List
一种数据项按照相对位置存放的数据集

```python
# 空列表
empty_list = []
empty_list = list()

# 包含元素的列表
numbers = [1, 2, 3, 4, 5]
fruits = ['apple', 'banana', 'orange']
mixed = [1, 'hello', 3.14, True]
```

```python
my_list = ['a', 'b', 'c', 'd', 'e']

# 索引访问（从0开始）
print(my_list[0])    # 'a'
print(my_list[2])    # 'c'

# 负数索引（从末尾开始）
print(my_list[-1])   # 'e'
print(my_list[-2])   # 'd'

# 切片操作
print(my_list[1:3])  # ['b', 'c']
print(my_list[:3])   # ['a', 'b', 'c']
print(my_list[2:])   # ['c', 'd', 'e']
```

```python
my_list = ['a', 'b', 'c', 'd', 'e']

# 索引访问（从0开始）
print(my_list[0])    # 'a'
print(my_list[2])    # 'c'

# 负数索引（从末尾开始）
print(my_list[-1])   # 'e'
print(my_list[-2])   # 'd'

# 切片操作
print(my_list[1:3])  # ['b', 'c']
print(my_list[:3])   # ['a', 'b', 'c']
print(my_list[2:])   # ['c', 'd', 'e']
```

```python
my_list = [1, 2, 3, 4]

# 修改元素
my_list[1] = 20      # [1, 20, 3, 4]

# 添加元素
my_list.append(5)    # [1, 20, 3, 4, 5]
my_list.insert(1, 15) # [1, 15, 20, 3, 4, 5]

# 删除元素
del my_list[2]       # [1, 15, 3, 4, 5]
removed = my_list.pop() # [1, 15, 3, 4], removed = 5
my_list.remove(15)   # [1, 3, 4]
```
#### 链[[链表]]表
##### 无序表
链表由一系列节点组成，每个节点包括两个部分
. 数据域：存储数据
. 指针域：指向下一个节点的地址

```python
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
    
    def delete(self, val):
        """删除指定值的节点"""
        current=self.head
        previous=None
        found=False
        while not found:
	        if current.getData()==item:
		        found=True
		    else:
			    previous=current
			    curren=curren.getNext()
		if previous==None:
			self.head=current.getNext()
		else:
			previous.setNext(current.getNext())
    
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

```
##### 有序表
```python
class OrderedList:
	def _init_(self):
		self.head=None
```
## 递归
