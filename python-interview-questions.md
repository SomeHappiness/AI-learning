# Python面试常见问题总结

## 1. Python基础

### 1.1 Python的特点
- 解释型语言：代码在运行时逐行解释执行，无需编译
- 动态类型：变量类型在运行时确定，无需事先声明
- 面向对象：支持类、继承、多态等面向对象特性
- 丰富的标准库：内置大量标准库，无需外部依赖
- 跨平台：同一代码可在不同操作系统上运行
- 可扩展性：可通过C/C++扩展提高性能
- 简洁易读：语法简洁，使用缩进表示代码块
- 强大的社区支持：拥有活跃的开发者社区和大量第三方库

**常见面试问题：**
1. Python 2和Python 3的主要区别是什么？
2. Python是如何管理内存的？
3. Python的GIL是什么，它对多线程编程有什么影响？
4. 什么是Python的命名空间和作用域？

### 1.2 Python中的数据类型
- 基本类型：
  - int：整数类型，如`x = 10`
  - float：浮点数类型，如`y = 3.14`
  - bool：布尔类型，值为`True`或`False`
  - str：字符串类型，如`s = "Hello"`
- 容器类型：
  - list：列表，如`lst = [1, 2, 3]`
  - tuple：元组，如`tup = (1, 2, 3)`
  - dict：字典，如`d = {"key": "value"}`
  - set：集合，如`s = {1, 2, 3}`
- 不可变类型：int, float, bool, str, tuple, frozenset
- 可变类型：list, dict, set

**常见面试问题：**
1. 如何判断两个变量是否指向同一个对象？
   ```python
   # 使用is操作符
   a = [1, 2, 3]
   b = a
   c = [1, 2, 3]
   print(a is b)  # True - 指向同一对象
   print(a is c)  # False - 不同对象
   print(a == c)  # True - 值相等
   ```

2. 解释Python中的深拷贝和浅拷贝。
   ```python
   import copy
   original = [[1, 2, 3], [4, 5, 6]]
   shallow = copy.copy(original)  # 浅拷贝
   deep = copy.deepcopy(original)  # 深拷贝
   
   original[0][0] = 99
   print(shallow)  # [[99, 2, 3], [4, 5, 6]] - 受影响
   print(deep)     # [[1, 2, 3], [4, 5, 6]] - 不受影响
   ```

3. 什么情况下应该使用列表、元组、集合和字典？

### 1.3 列表和元组的区别
- 列表可变，元组不可变
- 列表用`[]`，元组用`()`
- 列表适合存储动态数据，元组适合存储固定数据
- 元组比列表更节省内存和性能更好
- 元组可作为字典的键，列表不可以
- 元组传递给函数时更安全，因为它不能被修改

**常见面试问题：**
1. 如何高效地合并两个列表？
   ```python
   # 方法1：使用+运算符
   list1 = [1, 2, 3]
   list2 = [4, 5, 6]
   merged = list1 + list2  # [1, 2, 3, 4, 5, 6]
   
   # 方法2：使用extend方法
   list1.extend(list2)  # list1变为[1, 2, 3, 4, 5, 6]
   
   # 方法3：使用列表推导式
   [*list1, *list2]  # [1, 2, 3, 4, 5, 6]
   ```

2. 如何移除列表中的重复元素？
   ```python
   # 使用集合（保持顺序）
   my_list = [1, 2, 2, 3, 1, 4]
   unique_list = list(dict.fromkeys(my_list))  # [1, 2, 3, 4]
   
   # 使用集合（不保持顺序）
   unique_list = list(set(my_list))  # 顺序可能改变
   ```

3. 元组为什么比列表更节省内存？

### 1.4 字符串操作
- 字符串是不可变的序列类型
- 支持索引、切片、拼接、重复等操作
- 提供丰富的方法：split, join, strip, replace等

**常见面试问题：**
1. 解释字符串的不可变性，以及它的优缺点。
2. 如何高效地拼接多个字符串？
   ```python
   # 不推荐（低效）
   result = ""
   for s in ["a", "b", "c", "d"]:
       result += s
   
   # 推荐（高效）
   result = "".join(["a", "b", "c", "d"])
   ```
3. 如何格式化字符串？比较各种方法的优缺点。
   ```python
   name = "Alice"
   age = 30
   
   # %操作符（传统方式）
   print("Name: %s, Age: %d" % (name, age))
   
   # format方法
   print("Name: {}, Age: {}".format(name, age))
   
   # f-string（Python 3.6+，推荐）
   print(f"Name: {name}, Age: {age}")
   ```

### 1.5 字典和集合
- 字典：键值对的无序集合，通过键快速访问值
- 集合：唯一元素的无序集合，支持集合运算

**常见面试问题：**
1. 什么是字典的键的要求？为什么列表不能作为字典的键？
2. 如何安全地获取字典中可能不存在的键的值？
   ```python
   # 方法1：使用get方法
   d = {"a": 1, "b": 2}
   value = d.get("c", 0)  # 如果键不存在，返回默认值0
   
   # 方法2：使用setdefault方法
   value = d.setdefault("c", 0)  # 如果键不存在，添加键并设置默认值0
   
   # 方法3：使用defaultdict
   from collections import defaultdict
   d = defaultdict(int)  # 默认值为0
   d["a"] += 1  # 即使"a"不存在，也不会报错
   ```
3. 集合的常用操作有哪些？如何高效地使用集合？
   ```python
   # 创建集合
   s1 = {1, 2, 3}
   s2 = {3, 4, 5}
   
   # 集合运算
   print(s1 & s2)  # 交集: {3}
   print(s1 | s2)  # 并集: {1, 2, 3, 4, 5}
   print(s1 - s2)  # 差集: {1, 2}
   print(s1 ^ s2)  # 对称差集: {1, 2, 4, 5}
   
   # 判断子集和超集
   print({1, 2}.issubset(s1))  # True
   print(s1.issuperset({1, 2}))  # True
   ```

## 2. Python高级特性

### 2.1 装饰器
装饰器是一种用于修改或增强函数或方法行为的特殊函数，它遵循了设计模式中的装饰器模式。

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@my_decorator
def my_function():
    print("Inside function")
```

**带参数的装饰器：**
```python
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")
```

**常见面试问题：**
1. 解释装饰器的工作原理。
2. 装饰器有什么实际应用场景？
   - 日志记录
   - 性能测量
   - 权限验证
   - 缓存
   - 错误处理
3. 如何保留被装饰函数的元数据？
   ```python
   from functools import wraps
   
   def my_decorator(func):
       @wraps(func)  # 保留原函数的元数据
       def wrapper(*args, **kwargs):
           return func(*args, **kwargs)
       return wrapper
   ```
4. 如何创建类装饰器？
   ```python
   class CountCalls:
       def __init__(self, func):
           self.func = func
           self.count = 0
       
       def __call__(self, *args, **kwargs):
           self.count += 1
           print(f"调用次数: {self.count}")
           return self.func(*args, **kwargs)
   
   @CountCalls
   def say_hello():
       print("Hello!")
   ```

### 2.2 生成器
生成器是一种特殊的迭代器，它使用`yield`语句返回值，并在下次调用时从上次暂停的位置继续执行。Python 3.5+使用`async/await`语法支持协程。

```python
def my_generator():
    yield 1
    yield 2
    yield 3

# 使用
gen = my_generator()
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
# print(next(gen))  # StopIteration异常

# 或者
for i in my_generator():
    print(i)  # 打印1, 2, 3
```

**生成器表达式：**
```python
# 列表推导式（一次性生成所有元素）
squares = [x**2 for x in range(10)]

# 生成器表达式（惰性生成）
squares_gen = (x**2 for x in range(10))
```

**常见面试问题：**
1. 生成器与列表的区别是什么？
2. 生成器的优势是什么？
   - 内存效率高：仅在需要时生成元素
   - 适合处理大量数据或无限序列
   - 可以表示复杂的流程控制
3. 如何实现无限序列？
   ```python
   def infinite_counter():
       i = 0
       while True:
           yield i
           i += 1
   ```
4. 什么是生成器的`send`、`throw`和`close`方法？
   ```python
   def echo_generator():
       value = yield "Ready"
       while True:
           value = yield value
   
   gen = echo_generator()
   print(next(gen))  # Ready
   print(gen.send("Hello"))  # Hello
   gen.throw(Exception("Error"))  # 向生成器抛出异常
   gen.close()  # 关闭生成器
   ```

### 2.3 上下文管理器
上下文管理器是一种用于管理资源分配和释放的协议，通常与`with`语句一起使用。

```python
# 使用with语句
with open('file.txt', 'r') as f:
    content = f.read()

# 自定义上下文管理器
class MyContextManager:
    def __enter__(self):
        print("Entering context")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")
        # 返回True表示异常已处理，False表示异常未处理
        return False
```

**使用contextlib：**
```python
from contextlib import contextmanager

@contextmanager
def my_context():
    print("Entering context")
    try:
        yield "Context value"
    finally:
        print("Exiting context")

with my_context() as value:
    print(f"Inside context: {value}")
```

**常见面试问题：**
1. 上下文管理器的主要用途是什么？
2. `__enter__`和`__exit__`方法的作用是什么？
3. 如何使用上下文管理器处理异常？
   ```python
   class HandleException:
       def __enter__(self):
           return self
       
       def __exit__(self, exc_type, exc_val, exc_tb):
           if exc_type is ValueError:
               print(f"捕获到ValueError: {exc_val}")
               return True  # 异常已处理
           return False  # 其他异常未处理
   
   with HandleException():
       raise ValueError("这个异常将被处理")
   ```
4. 使用上下文管理器的实际场景有哪些？
   - 文件操作
   - 数据库连接
   - 锁管理
   - 临时改变设置
   - 计时和性能测量

### 2.4 迭代器
迭代器是一种提供访问集合元素的对象，它实现了`__iter__`和`__next__`方法。

```python
class MyIterator:
    def __init__(self, max_num):
        self.max_num = max_num
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.max_num:
            self.current += 1
            return self.current - 1
        raise StopIteration
```

**常见面试问题：**
1. 迭代器和可迭代对象的区别是什么？
2. 为什么迭代器必须实现`__iter__`和`__next__`方法？
3. 如何检查一个对象是否可迭代？
   ```python
   def is_iterable(obj):
       try:
           iter(obj)
           return True
       except TypeError:
           return False
   ```

### 2.5 函数式编程
Python支持函数式编程范式，提供了一些内置函数如`map`、`filter`、`reduce`以及匿名函数lambda。

```python
# map函数
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))  # [1, 4, 9, 16, 25]

# filter函数
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]

# reduce函数
from functools import reduce
sum_all = reduce(lambda x, y: x + y, numbers)  # 15
```

**常见面试问题：**
1. 什么是纯函数？它有什么优势？
2. 如何使用`functools.partial`创建部分应用函数？
   ```python
   from functools import partial
   
   def power(base, exponent):
       return base ** exponent
   
   square = partial(power, exponent=2)
   print(square(5))  # 25
   ```
3. 列表推导式、生成器表达式和map/filter函数的比较。
4. 什么是闭包？它有什么用途？
   ```python
   def counter():
       count = 0
       
       def increment():
           nonlocal count
           count += 1
           return count
       
       return increment
   
   my_counter = counter()
   print(my_counter())  # 1
   print(my_counter())  # 2
   ```

## 3. 面向对象编程

### 3.1 类的基本概念
- 封装：将数据和方法捆绑在一起，隐藏实现细节
- 继承：一个类可以继承另一个类的属性和方法
- 多态：不同类的对象对相同方法的调用有不同的行为
- 抽象类：不能被实例化的类，用于定义接口
- 接口：定义类应该实现的方法集合

**示例：**
```python
# 封装
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # 私有属性
    
    def deposit(self, amount):
        self.__balance += amount
        return self.__balance
    
    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
    def get_balance(self):
        return self.__balance

# 继承
class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, interest_rate=0.01):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate
    
    def add_interest(self):
        balance = self.get_balance()
        interest = balance * self.interest_rate
        self.deposit(interest)
        return interest
```

**常见面试问题：**
1. 解释Python中单继承和多继承的区别。
2. 什么是方法解析顺序(MRO)？它如何工作？
   ```python
   class A: pass
   class B(A): pass
   class C(A): pass
   class D(B, C): pass
   
   print(D.__mro__)  # MRO顺序
   ```
3. 如何实现私有属性和方法？
4. 抽象类和接口在Python中如何实现？
   ```python
   from abc import ABC, abstractmethod
   
   class Shape(ABC):
       @abstractmethod
       def area(self):
           pass
       
       @abstractmethod
       def perimeter(self):
           pass
   ```

### 3.2 魔术方法
魔术方法（也称为双下方法）是Python类中以双下划线开始和结束的特殊方法，它们允许类实例支持特定的操作。

- `__init__`: 构造函数，对象创建时调用
- `__str__`: 定义对象的字符串表示，用于str()和print()
- `__repr__`: 定义对象的开发者字符串表示，用于repr()
- `__len__`: 定义len()函数的行为
- `__getitem__`: 定义索引访问的行为，如obj[key]
- `__setitem__`: 定义索引赋值的行为，如obj[key] = value
- `__del__`: 析构函数，对象被垃圾回收前调用
- `__call__`: 使对象可调用，如obj()
- `__add__`, `__sub__`, `__mul__`等：定义算术运算符的行为

**示例：**
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)  # Vector(4, 6)
print(v1 == v2)  # False
```

**常见面试问题：**
1. `__str__`和`__repr__`的区别是什么？
2. 如何实现自定义容器类？
   ```python
   class MyList:
       def __init__(self, items):
           self.items = items
       
       def __len__(self):
           return len(self.items)
       
       def __getitem__(self, index):
           return self.items[index]
       
       def __setitem__(self, index, value):
           self.items[index] = value
       
       def __iter__(self):
           return iter(self.items)
   ```
3. 如何使类的实例可调用？
   ```python
   class Adder:
       def __call__(self, a, b):
           return a + b
   
   add = Adder()
   print(add(3, 4))  # 7
   ```
4. 如何自定义对象的比较行为？
   ```python
   class Person:
       def __init__(self, name, age):
           self.name = name
           self.age = age
       
       def __eq__(self, other):
           return self.age == other.age
       
       def __lt__(self, other):
           return self.age < other.age
   ```

### 3.3 类方法和静态方法
Python支持定义类方法和静态方法：
- 实例方法：第一个参数是self，操作实例的数据
- 类方法：第一个参数是cls，操作类的数据
- 静态方法：没有特殊的第一个参数，不操作类或实例的数据

```python
class MyClass:
    class_var = 0
    
    def __init__(self, instance_var):
        self.instance_var = instance_var
    
    def instance_method(self):
        return self.instance_var
    
    @classmethod
    def class_method(cls):
        cls.class_var += 1
        return cls.class_var
    
    @staticmethod
    def static_method(x, y):
        return x + y
```

**常见面试问题：**
1. 什么时候应该使用类方法而不是实例方法？
2. 什么时候应该使用静态方法？
3. 如何使用类方法作为替代构造函数？
   ```python
   class Date:
       def __init__(self, year, month, day):
           self.year = year
           self.month = month
           self.day = day
       
       @classmethod
       def from_string(cls, date_string):
           year, month, day = map(int, date_string.split('-'))
           return cls(year, month, day)
       
       @classmethod
       def today(cls):
           from datetime import date
           today = date.today()
           return cls(today.year, today.month, today.day)
   ```

## 4. 并发编程

### 4.1 多线程
Python的标准库提供了`threading`模块用于多线程编程。

```python
import threading
import time

def worker(name):
    print(f"Worker {name} started")
    time.sleep(2)
    print(f"Worker {name} finished")

# 创建线程
thread1 = threading.Thread(target=worker, args=("A",))
thread2 = threading.Thread(target=worker, args=("B",))

# 启动线程
thread1.start()
thread2.start()

# 等待线程完成
thread1.join()
thread2.join()

print("All threads finished")
```

**线程安全：**
```python
import threading

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:  # 线程安全
            self.value += 1
    
    def get_value(self):
        with self.lock:
            return self.value
```

**常见面试问题：**
1. 什么是GIL？它如何影响Python的多线程性能？
2. 什么是线程安全？如何确保线程安全？
3. 什么是死锁？如何避免死锁？
4. 如何使用线程池？
   ```python
   from concurrent.futures import ThreadPoolExecutor
   
   def task(n):
       return n * n
   
   with ThreadPoolExecutor(max_workers=5) as executor:
       results = executor.map(task, range(10))
       for result in results:
           print(result)
   ```

### 4.2 多进程
Python的`multiprocessing`模块提供了类似于`threading`模块的API，但使用进程而不是线程。

```python
import multiprocessing
import time

def worker(name):
    print(f"Worker {name} started")
    time.sleep(2)
    print(f"Worker {name} finished")

if __name__ == "__main__":  # 重要：在Windows上必须有这个条件
    # 创建进程
    process1 = multiprocessing.Process(target=worker, args=("A",))
    process2 = multiprocessing.Process(target=worker, args=("B",))
    
    # 启动进程
    process1.start()
    process2.start()
    
    # 等待进程完成
    process1.join()
    process2.join()
    
    print("All processes finished")
```

**进程间通信：**
```python
from multiprocessing import Process, Queue

def producer(q):
    q.put('Hello from producer')

def consumer(q):
    msg = q.get()
    print(msg)

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
```

**常见面试问题：**
1. 多进程与多线程的区别是什么？
2. 何时应该使用多进程而不是多线程？
3. 如何在进程间共享数据？
   ```python
   from multiprocessing import Process, Value, Array
   
   def worker(n, a):
       n.value += 1
       for i in range(len(a)):
           a[i] += 1
   
   if __name__ == "__main__":
       num = Value('i', 0)  # 共享整数
       arr = Array('i', [0, 0, 0, 0])  # 共享数组
       
       p = Process(target=worker, args=(num, arr))
       p.start()
       p.join()
       
       print(num.value)  # 1
       print(list(arr))  # [1, 1, 1, 1]
   ```
4. 如何使用进程池？
   ```python
   from multiprocessing import Pool
   
   def f(x):
       return x * x
   
   if __name__ == "__main__":
       with Pool(5) as p:
           print(p.map(f, [1, 2, 3, 4, 5]))
   ```

### 4.3 协程
协程是一种用户态的轻量级线程，可以在函数执行过程中挂起和恢复。Python 3.5+使用`async/await`语法支持协程。

```python
import asyncio

async def my_coroutine():
    print("Coroutine started")
    await asyncio.sleep(1)  # 模拟I/O操作
    print("Coroutine finished")

async def main():
    # 并发运行多个协程
    await asyncio.gather(
        my_coroutine(),
        my_coroutine(),
        my_coroutine()
    )

# Python 3.7+
asyncio.run(main())
```

**异步I/O：**
```python
import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for url, result in zip(urls, results):
        print(f"{url}: {len(result)} bytes")

asyncio.run(main())
```

**常见面试问题：**
1. 协程与线程的区别是什么？
2. 什么是事件循环？它在异步编程中的作用是什么？
3. 如何处理协程中的异常？
   ```python
   async def risky_coroutine():
       raise ValueError("Something went wrong")
   
   async def main():
       try:
           await risky_coroutine()
       except ValueError as e:
           print(f"Caught exception: {e}")
   
   asyncio.run(main())
   ```
4. 什么是异步上下文管理器和异步迭代器？
   ```python
   # 异步上下文管理器
   class AsyncContextManager:
       async def __aenter__(self):
           print("Entering context")
           return self
       
       async def __aexit__(self, exc_type, exc_val, exc_tb):
           print("Exiting context")
   
   # 异步迭代器
   class AsyncIterator:
       def __init__(self, limit):
           self.limit = limit
           self.current = 0
       
       def __aiter__(self):
           return self
       
       async def __anext__(self):
           if self.current < self.limit:
               self.current += 1
               await asyncio.sleep(0.1)
               return self.current - 1
           raise StopAsyncIteration
   ```

## 5. 内存管理

### 5.1 垃圾回收
Python使用引用计数为主要的垃圾回收机制，同时使用分代收集来解决循环引用问题。

- 引用计数：每个对象都有一个引用计数，当计数为0时，对象被回收
- 标记-清除：解决循环引用问题的算法
- 分代回收：基于对象生命周期的假设，对不同"代"的对象使用不同的回收频率

**手动控制垃圾回收：**
```python
import gc

# 获取当前引用计数
import sys
obj = [1, 2, 3]
print(sys.getrefcount(obj) - 1)  # 减1是因为getrefcount本身会增加一个引用

# 手动触发垃圾回收
gc.collect()

# 禁用自动垃圾回收
gc.disable()

# 启用自动垃圾回收
gc.enable()
```

**常见面试问题：**
1. Python如何处理循环引用？
   ```python
   # 循环引用示例
   a = {}
   b = {}
   a['b'] = b
   b['a'] = a  # a和b互相引用
   
   # 打破循环引用
   a['b'] = None
   b['a'] = None
   ```
2. 为什么Python使用分代收集？
3. 弱引用是什么？如何使用它？
   ```python
   import weakref
   
   class MyClass:
       pass
   
   obj = MyClass()
   weak_ref = weakref.ref(obj)
   
   # 检查对象是否仍然存在
   print(weak_ref() is not None)  # True
   
   # 删除对象
   del obj
   
   # 弱引用现在返回None
   print(weak_ref() is None)  # True
   ```
4. 如何跟踪内存泄漏？
   ```python
   # 使用tracemalloc（Python 3.4+）
   import tracemalloc
   
   tracemalloc.start()
   
   # 运行代码
   # ...
   
   snapshot = tracemalloc.take_snapshot()
   top_stats = snapshot.statistics('lineno')
   
   for stat in top_stats[:10]:
       print(stat)
   ```

### 5.2 内存泄漏
内存泄漏是指程序分配的内存在使用完后未被释放，导致内存消耗持续增加。

主要原因：
- 循环引用：对象之间相互引用，且至少一个对象有`__del__`方法
- 全局变量：长时间运行的程序中无限增长的全局变量
- 未关闭的资源：文件、网络连接等资源未正确关闭
- 缓存：未限制大小的缓存
- 事件处理器：未正确注销的事件处理器

**避免内存泄漏的方法：**
```python
# 使用上下文管理器自动关闭资源
with open('file.txt', 'r') as f:
    content = f.read()

# 使用弱引用实现缓存
import weakref
cache = weakref.WeakValueDictionary()

# 限制缓存大小
from functools import lru_cache
@lru_cache(maxsize=100)
def expensive_function(n):
    return n * n
```

**常见面试问题：**
1. 如何检测Python程序中的内存泄漏？
2. 为什么全局变量可能导致内存泄漏？
3. 如何实现一个内存安全的缓存？
4. 使用`__del__`方法有什么潜在的问题？

## 6. 性能优化

### 6.1 常用优化技巧
- 使用生成器：处理大数据集时避免一次性加载所有数据
  ```python
  # 不推荐（内存占用大）
  def load_data(file_path):
      lines = []
      with open(file_path, 'r') as f:
          for line in f:
              lines.append(line.strip())
      return lines
  
  # 推荐（内存高效）
  def load_data(file_path):
      with open(file_path, 'r') as f:
          for line in f:
              yield line.strip()
  ```

- 使用列表推导式：比循环更高效
  ```python
  # 不推荐
  squares = []
  for i in range(1000):
      squares.append(i * i)
  
  # 推荐
  squares = [i * i for i in range(1000)]
  ```

- 使用内置函数：内置函数通常用C实现，性能更好
  ```python
  # 不推荐
  total = 0
  for num in numbers:
      total += num
  
  # 推荐
  total = sum(numbers)
  ```

- 避免全局变量：局部变量访问更快
  ```python
  # 不推荐
  counter = 0
  def increment():
      global counter
      counter += 1
  
  # 推荐
  def counter():
      count = 0
      def increment():
          nonlocal count
          count += 1
          return count
      return increment
  ```

- 使用适当的数据结构：选择合适的数据结构可以大大提高性能
  ```python
  # 不推荐（O(n)查找）
  items = [1, 2, 3, 4, 5]
  if 3 in items:  # 线性搜索
      print("Found")
  
  # 推荐（O(1)查找）
  items = {1, 2, 3, 4, 5}  # 集合
  if 3 in items:  # 常数时间搜索
      print("Found")
  ```

- 字符串拼接优化
  ```python
  # 不推荐（每次+=都创建新字符串）
  result = ""
  for i in range(1000):
      result += str(i)
  
  # 推荐
  result = "".join(str(i) for i in range(1000))
  ```

- 使用本地化变量优化循环
  ```python
  # 不推荐
  import math
  result = []
  for i in range(1000):
      result.append(math.sin(i))
  
  # 推荐（本地化函数和列表）
  import math
  sin = math.sin  # 局部变量
  result = []
  append = result.append  # 局部变量
  for i in range(1000):
      append(sin(i))
  ```

### 6.2 性能分析工具

- **cProfile**：标准库提供的性能分析工具
  ```python
  import cProfile
  
  def slow_function():
      total = 0
      for i in range(1000000):
          total += i
      return total
  
  # 分析单个函数
  cProfile.run('slow_function()')
  
  # 分析整个脚本
  # python -m cProfile script.py
  ```

- **timeit**：测量小代码片段执行时间
  ```python
  import timeit
  
  # 测量单行代码
  print(timeit.timeit('[i for i in range(1000)]', number=10000))
  
  # 测量函数
  setup = '''
  def slow_function():
      return [i for i in range(1000)]
  '''
  print(timeit.timeit('slow_function()', setup=setup, number=10000))
  ```

- **memory_profiler**：内存使用分析
  ```python
  # pip install memory_profiler
  from memory_profiler import profile
  
  @profile
  def memory_hungry_function():
      return [i for i in range(1000000)]
  
  memory_hungry_function()
  ```

- **line_profiler**：逐行性能分析
  ```python
  # pip install line_profiler
  # 使用@profile装饰函数（不需要导入）
  @profile
  def slow_function():
      total = 0
      for i in range(1000000):
          total += i
      return total
  
  # 运行：kernprof -l -v script.py
  ```

### 6.3 CPU密集型与I/O密集型任务优化

**CPU密集型任务优化**：
```python
# 使用多进程（绕过GIL）
import multiprocessing

def cpu_bound_task(data):
    # 大量计算
    result = 0
    for i in range(10000000):
        result += i * i
    return result

def process_data(data_chunks):
    with multiprocessing.Pool() as pool:
        results = pool.map(cpu_bound_task, data_chunks)
    return results
```

**I/O密集型任务优化**：
```python
# 使用异步I/O
import asyncio
import aiohttp

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = ["https://example.com" for _ in range(100)]
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# 或使用多线程
import concurrent.futures
import requests

def fetch_url_sync(url):
    return requests.get(url).text

def download_all(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(fetch_url_sync, urls))
    return results
```

### 6.4 常见性能问题和解决方案

**问题：循环中的重复计算**
```python
# 不推荐
for i in range(n):
    for j in range(n):
        result = expensive_function(i)  # 注意：i不依赖于j，但在j循环中重复计算
        # 处理结果

# 推荐
for i in range(n):
    result = expensive_function(i)  # 只计算一次
    for j in range(n):
        # 使用result处理
```

**问题：不必要的列表创建**
```python
# 不推荐（创建不必要的中间列表）
data = [1, 2, 3, 4, 5]
squared = [x**2 for x in data]  # 创建中间列表
filtered = [x for x in squared if x > 10]  # 创建另一个列表

# 推荐（使用生成器表达式链接操作）
data = [1, 2, 3, 4, 5]
result = [x for x in (i**2 for i in data) if x > 10]
# 或更好
result = [x**2 for x in data if x**2 > 10]
```

**问题：字典查找开销**
```python
# 不推荐
config = {'key1': 'value1', 'key2': 'value2'}
for i in range(1000000):
    value = config['key1']  # 每次循环都查找

# 推荐
config = {'key1': 'value1', 'key2': 'value2'}
key1_value = config['key1']  # 查找一次
for i in range(1000000):
    value = key1_value
```

**常见面试问题：**
1. 如何确定代码中的性能瓶颈？
2. Python中字典的实现原理及其性能特性？
3. 列表和数组（numpy.ndarray）在性能上有什么区别？
4. 为什么Python中的某些操作（如字符串拼接）性能较差？如何优化？
5. 如何优化递归函数以避免栈溢出？
   ```python
   # 使用尾递归优化（但Python不自动优化尾递归）
   def factorial(n, acc=1):
       if n == 0:
           return acc
       return factorial(n-1, n*acc)
   
   # 使用显式栈代替递归
   def factorial_iter(n):
       result = 1
       for i in range(1, n+1):
           result *= i
       return result
   ```
6. 如何处理大文件而不消耗过多内存？
   ```python
   # 分块读取大文件
   def process_large_file(file_path, chunk_size=1024*1024):
       with open(file_path, 'r') as f:
           while True:
               data = f.read(chunk_size)
               if not data:
                   break
               yield data
   
   # 使用
   for chunk in process_large_file('huge_file.txt'):
       process_chunk(chunk)
   ```

## 7. 设计模式

### 7.1 常用设计模式
设计模式是解决软件设计中常见问题的可复用解决方案。Python中常用的设计模式包括：

- **单例模式**：确保一个类只有一个实例，并提供全局访问点
- **工厂模式**：提供创建对象的接口，允许子类决定实例化的类
- **观察者模式**：定义对象间的一对多依赖关系，当一个对象改变状态，依赖它的对象会收到通知
- **策略模式**：定义一系列算法，将每个算法封装起来，使它们可以互换
- **装饰器模式**：动态地给对象添加新功能，不改变其结构
- **适配器模式**：使接口不兼容的类能一起工作
- **命令模式**：将请求封装成对象，从而使用不同的请求参数化客户端
- **迭代器模式**：提供顺序访问集合元素的方法，不暴露底层表示
- **模板方法模式**：定义算法的骨架，允许子类重定义部分步骤
- **状态模式**：允许对象在内部状态改变时改变它的行为

### 7.2 单例模式实现
单例模式确保一个类只有一个实例，并提供一个全局访问点。

```python
# 方法1：使用__new__方法
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# 测试
s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True

# 方法2：使用装饰器
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class SingletonClass:
    pass

# 方法3：使用元类
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class SingletonWithMeta(metaclass=SingletonMeta):
    pass
```

**线程安全的单例模式：**
```python
import threading

class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
```

### 7.3 工厂模式
工厂模式提供了创建对象的接口，将实例化的逻辑与使用对象的代码分离。

**简单工厂：**
```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")

# 使用
factory = AnimalFactory()
dog = factory.create_animal("dog")
print(dog.speak())  # Woof!
```

**工厂方法：**
```python
from abc import ABC, abstractmethod

class Creator(ABC):
    @abstractmethod
    def factory_method(self):
        pass
    
    def operation(self):
        product = self.factory_method()
        return f"Creator: {product.operation()}"

class ConcreteCreator1(Creator):
    def factory_method(self):
        return ConcreteProduct1()

class ConcreteCreator2(Creator):
    def factory_method(self):
        return ConcreteProduct2()

class Product(ABC):
    @abstractmethod
    def operation(self):
        pass

class ConcreteProduct1(Product):
    def operation(self):
        return "Result of ConcreteProduct1"

class ConcreteProduct2(Product):
    def operation(self):
        return "Result of ConcreteProduct2"

# 使用
creator1 = ConcreteCreator1()
print(creator1.operation())
```

### 7.4 观察者模式
观察者模式定义了对象间的一对多依赖关系，当一个对象改变状态，依赖它的对象会收到通知。

```python
class Subject:
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        self._state = state
        self.notify()

class Observer:
    def update(self, subject):
        pass

class ConcreteObserverA(Observer):
    def update(self, subject):
        print(f"ConcreteObserverA: Reacted to the state change: {subject.state}")

class ConcreteObserverB(Observer):
    def update(self, subject):
        print(f"ConcreteObserverB: Reacted to the state change: {subject.state}")

# 使用
subject = Subject()

observer_a = ConcreteObserverA()
subject.attach(observer_a)

observer_b = ConcreteObserverB()
subject.attach(observer_b)

subject.state = "New State"  # 触发通知
```

### 7.5 策略模式
策略模式定义了一系列算法，将每个算法封装起来，使它们可以互换。

```python
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute(self, data):
        pass

class ConcreteStrategyA(Strategy):
    def execute(self, data):
        return sorted(data)  # 升序排序

class ConcreteStrategyB(Strategy):
    def execute(self, data):
        return sorted(data, reverse=True)  # 降序排序

class ConcreteStrategyC(Strategy):
    def execute(self, data):
        return sorted(data, key=len)  # 按长度排序

class Context:
    def __init__(self, strategy):
        self._strategy = strategy
    
    @property
    def strategy(self):
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy
    
    def execute_strategy(self, data):
        return self._strategy.execute(data)

# 使用
data = ["apple", "banana", "cherry", "date"]

context = Context(ConcreteStrategyA())
print(context.execute_strategy(data))  # 按字母顺序排序

context.strategy = ConcreteStrategyB()
print(context.execute_strategy(data))  # 按字母顺序倒序排序

context.strategy = ConcreteStrategyC()
print(context.execute_strategy(data))  # 按长度排序
```

### 7.6 装饰器模式
装饰器模式动态地给对象添加新功能，不改变其结构。Python的装饰器语法(@)是这种模式的直接实现。

```python
from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def operation(self):
        pass

class ConcreteComponent(Component):
    def operation(self):
        return "ConcreteComponent"

class Decorator(Component):
    def __init__(self, component):
        self._component = component
    
    @abstractmethod
    def operation(self):
        pass

class ConcreteDecoratorA(Decorator):
    def operation(self):
        return f"ConcreteDecoratorA({self._component.operation()})"

class ConcreteDecoratorB(Decorator):
    def operation(self):
        return f"ConcreteDecoratorB({self._component.operation()})"

# 使用
simple = ConcreteComponent()
decorator_a = ConcreteDecoratorA(simple)
decorator_b = ConcreteDecoratorB(decorator_a)

print(decorator_b.operation())  # ConcreteDecoratorB(ConcreteDecoratorA(ConcreteComponent))
```

**使用Python的装饰器语法：**
```python
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_decorator
def add(a, b):
    return a + b

# 等同于 add = log_decorator(add)
print(add(3, 5))
```

### 7.7 适配器模式
适配器模式使接口不兼容的类能一起工作。

```python
class Target:
    def request(self):
        return "Target: The default target's behavior."

class Adaptee:
    def specific_request(self):
        return "Adaptee: Specific behavior."

class Adapter(Target):
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def request(self):
        return f"Adapter: {self.adaptee.specific_request()}"

# 使用
adaptee = Adaptee()
adapter = Adapter(adaptee)
print(adapter.request())
```

**常见面试问题：**
1. 什么是设计模式？为什么它们重要？
2. 工厂模式和抽象工厂模式的区别是什么？
3. 单例模式在多线程环境中可能有什么问题？如何解决？
4. 装饰器模式和Python装饰器的关系是什么？
5. 策略模式和工厂模式的主要区别是什么？
6. 在实际项目中，你使用过哪些设计模式？为什么选择它们？
7. 如何使用组合设计模式解决复杂问题？

## 8. 异常处理

### 8.1 异常处理机制
Python使用`try`、`except`、`else`、`finally`语句来处理异常。

```python
try:
    # 可能出错的代码
    result = 10 / 0
except ZeroDivisionError as e:
    # 处理特定类型的异常
    print(f"Error: {e}")
except Exception as e:
    # 处理其他类型的异常
    print(f"Unexpected error: {e}")
else:
    # 如果没有异常发生则执行
    print("No errors")
finally:
    # 无论是否发生异常都执行
    print("Always executed")
```

**异常层次结构：**
```
BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 ├── GeneratorExit
 └── Exception
      ├── StopIteration
      ├── ArithmeticError
      │    ├── FloatingPointError
      │    ├── OverflowError
      │    └── ZeroDivisionError
      ├── AssertionError
      ├── AttributeError
      ├── ImportError
      │    └── ModuleNotFoundError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── NameError
      │    └── UnboundLocalError
      ├── OSError
      │    ├── FileNotFoundError
      │    ├── PermissionError
      │    └── ... 其他OS错误
      ├── TypeError
      ├── ValueError
      └── ... 其他异常
```

**捕获多种异常：**
```python
try:
    # 可能引发不同类型的异常的代码
    x = int(input("Enter a number: "))
    y = 10 / x
except (ValueError, ZeroDivisionError) as e:
    print(f"Error: {e}")
```

### 8.2 自定义异常
自定义异常可以帮助更好地描述和处理程序中的特定错误情况。

```python
class MyError(Exception):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code
        super().__init__(self.message)
    
    def __str__(self):
        if self.code:
            return f"[Error {self.code}] {self.message}"
        return self.message

# 使用
try:
    raise MyError("Something went wrong", 500)
except MyError as e:
    print(e)  # [Error 500] Something went wrong
    print(e.code)  # 500
```

**创建异常层次结构：**
```python
class AppError(Exception):
    """Base exception for the application."""
    pass

class DatabaseError(AppError):
    """Exception raised for database errors."""
    pass

class NetworkError(AppError):
    """Exception raised for network errors."""
    pass

class ValidationError(AppError):
    """Exception raised for validation errors."""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"Validation error in {field}: {message}")
```

### 8.3 异常处理最佳实践

**1. 只捕获特定异常**
```python
# 不推荐
try:
    do_something()
except Exception:  # 捕获所有异常可能掩盖真正的问题
    pass

# 推荐
try:
    do_something()
except ValueError:  # 只捕获预期的异常
    handle_value_error()
```

**2. 处理异常，不忽略**
```python
# 不推荐
try:
    do_something()
except Exception:
    pass  # 忽略异常，难以调试

# 推荐
try:
    do_something()
except Exception as e:
    logger.error(f"Error: {e}")  # 记录错误信息
    # 可能的恢复逻辑
```

**3. 使用finally清理资源**
```python
file = None
try:
    file = open("data.txt", "r")
    # 处理文件
except IOError as e:
    print(f"Error: {e}")
finally:
    if file:
        file.close()  # 确保文件被关闭

# 更好的方式是使用上下文管理器
with open("data.txt", "r") as file:
    # 处理文件
```

**4. 使用else子句**
```python
try:
    data = json.loads(json_string)
except json.JSONDecodeError:
    print("Invalid JSON")
else:
    # 只有在没有异常时执行
    process_data(data)
```

**5. 异常链**
```python
try:
    do_something()
except SomeError as e:
    # Python 3的语法
    raise OtherError("Failed to do something") from e

    # 或者，如果不想保留原始异常信息
    # raise OtherError("Failed to do something") from None
```

### 8.4 上下文管理器与异常处理
上下文管理器可用于简化异常处理，尤其是在资源管理方面。

```python
# 基本上下文管理器
with open("file.txt", "r") as f:
    content = f.read()  # 即使发生异常，文件也会自动关闭

# 自定义上下文管理器处理异常
class ErrorHandler:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Caught an exception: {exc_val}")
            return True  # 表示异常已处理
        return False  # 表示没有异常或未处理异常

with ErrorHandler():
    # 即使这里发生异常，也会被ErrorHandler捕获和处理
    result = 10 / 0
```

### 8.5 调试技巧

**使用断言：**
```python
def calculate_average(numbers):
    assert len(numbers) > 0, "Cannot calculate average of empty list"
    return sum(numbers) / len(numbers)
```

**使用日志记录异常：**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    result = 10 / 0
except ZeroDivisionError as e:
    logger.exception("Division by zero error")  # 记录异常信息和堆栈跟踪
```

**使用traceback模块：**
```python
import traceback

try:
    result = 10 / 0
except ZeroDivisionError:
    # 获取并打印完整的堆栈跟踪
    traceback.print_exc()
    
    # 或获取堆栈跟踪信息为字符串
    error_message = traceback.format_exc()
    print(f"Error details: {error_message}")
```

**常见面试问题：**
1. Python中的异常处理机制与其他语言（如Java、C++）有什么不同？
2. `try`、`except`、`else`和`finally`块的执行顺序是什么？
3. 什么是异常链？为什么它很重要？
4. 如何在多线程环境中安全地处理异常？
   ```python
   import threading
   import traceback
   
   def worker():
       try:
           # 可能出错的代码
           result = 10 / 0
       except Exception:
           print(f"Exception in thread {threading.current_thread().name}:")
           traceback.print_exc()
   
   thread = threading.Thread(target=worker)
   thread.start()
   thread.join()
   ```
5. Python的`with`语句如何简化异常处理？
6. 如何设计一个好的自定义异常层次结构？
7. 为什么不应该捕获所有异常？有哪些例外情况？
   ```python
   # 示例：日志记录工具可能需要捕获所有异常
   def log_exceptions(func):
       def wrapper(*args, **kwargs):
           try:
               return func(*args, **kwargs)
           except Exception as e:
               logger.exception(f"Exception in {func.__name__}: {e}")
               raise  # 重新抛出异常
       return wrapper
   ```

## 9. 常用库

### 9.1 标准库
Python标准库是Python安装包自带的一组模块，提供了各种常用功能。

- **os**: 操作系统接口，提供与操作系统交互的功能
  ```python
  import os
  
  # 当前工作目录
  print(os.getcwd())
  
  # 列出目录内容
  print(os.listdir("."))
  
  # 创建目录
  os.makedirs("new_dir/sub_dir", exist_ok=True)
  
  # 环境变量
  print(os.environ.get("PATH"))
  
  # 连接路径组件
  path = os.path.join("dir", "subdir", "file.txt")
  ```

- **sys**: 系统特定参数和函数
  ```python
  import sys
  
  # 命令行参数
  print(sys.argv)
  
  # Python版本
  print(sys.version)
  
  # 模块搜索路径
  print(sys.path)
  
  # 标准输出/错误
  sys.stdout.write("Output\n")
  sys.stderr.write("Error\n")
  
  # 退出程序
  sys.exit(0)  # 成功退出
  ```

- **re**: 正则表达式
  ```python
  import re
  
  # 匹配模式
  pattern = r"\d+"
  text = "123 abc 456"
  print(re.findall(pattern, text))  # ['123', '456']
  
  # 替换
  new_text = re.sub(r"[aeiou]", "*", "hello world")
  print(new_text)  # h*ll* w*rld
  
  # 编译正则表达式（提高多次使用的效率）
  regex = re.compile(r"\d+")
  print(regex.findall("123 abc 456"))  # ['123', '456']
  
  # 分组
  match = re.search(r"(\d+)-(\d+)", "Number: 123-456")
  if match:
      print(match.group(0))  # 123-456
      print(match.group(1))  # 123
      print(match.group(2))  # 456
  ```

- **json**: JSON数据编码和解码
  ```python
  import json
  
  # Python对象转JSON字符串
  data = {"name": "John", "age": 30, "city": "New York"}
  json_str = json.dumps(data, indent=4)
  print(json_str)
  
  # JSON字符串转Python对象
  parsed_data = json.loads(json_str)
  print(parsed_data["name"])  # John
  
  # 写入JSON文件
  with open("data.json", "w") as f:
      json.dump(data, f, indent=4)
  
  # 读取JSON文件
  with open("data.json", "r") as f:
      loaded_data = json.load(f)
  ```

- **datetime**: 日期和时间处理
  ```python
  import datetime
  
  # 当前日期和时间
  now = datetime.datetime.now()
  print(now)
  
  # 创建日期
  date = datetime.date(2023, 1, 1)
  print(date)
  
  # 创建时间
  time = datetime.time(12, 30, 45)
  print(time)
  
  # 日期算术
  tomorrow = now + datetime.timedelta(days=1)
  print(tomorrow)
  
  # 格式化日期
  print(now.strftime("%Y-%m-%d %H:%M:%S"))
  
  # 解析日期字符串
  date_str = "2023-01-01 12:30:45"
  parsed_date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
  print(parsed_date)
  ```

- **collections**: 容器数据类型
  ```python
  from collections import Counter, defaultdict, namedtuple, deque, OrderedDict
  
  # Counter: 计数器
  c = Counter("hello world")
  print(c)  # Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})
  print(c.most_common(2))  # [('l', 3), ('o', 2)]
  
  # defaultdict: 带默认值的字典
  d = defaultdict(int)  # 默认值为0
  d["a"] += 1
  print(d)  # defaultdict(<class 'int'>, {'a': 1})
  
  # namedtuple: 命名元组
  Point = namedtuple("Point", ["x", "y"])
  p = Point(1, 2)
  print(p.x, p.y)  # 1 2
  
  # deque: 双端队列
  d = deque([1, 2, 3])
  d.append(4)        # 添加到右端
  d.appendleft(0)    # 添加到左端
  print(d)  # deque([0, 1, 2, 3, 4])
  
  # OrderedDict: 有序字典 (Python 3.7+中普通字典也保持插入顺序)
  od = OrderedDict()
  od["a"] = 1
  od["b"] = 2
  od["c"] = 3
  print(list(od.items()))  # [('a', 1), ('b', 2), ('c', 3)]
  ```

- **itertools**: 迭代器工具
  ```python
  import itertools
  
  # 无限迭代器
  counter = itertools.count(start=1, step=2)
  print([next(counter) for _ in range(5)])  # [1, 3, 5, 7, 9]
  
  # cycle: 循环迭代
  cycle = itertools.cycle([1, 2, 3])
  print([next(cycle) for _ in range(6)])  # [1, 2, 3, 1, 2, 3]
  
  # repeat: 重复
  repeat = itertools.repeat("A", 3)
  print(list(repeat))  # ['A', 'A', 'A']
  
  # 排列组合
  print(list(itertools.permutations([1, 2, 3], 2)))  # [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
  print(list(itertools.combinations([1, 2, 3], 2)))  # [(1, 2), (1, 3), (2, 3)]
  
  # 分组
  data = [("A", 1), ("A", 2), ("B", 1), ("B", 2)]
  for key, group in itertools.groupby(data, lambda x: x[0]):
      print(key, list(group))
  # A [('A', 1), ('A', 2)]
  # B [('B', 1), ('B', 2)]
  ```

- **random**: 生成伪随机数
  ```python
  import random
  
  # 随机整数
  print(random.randint(1, 10))  # 1到10之间的随机整数
  
  # 随机选择
  print(random.choice(["red", "green", "blue"]))
  
  # 随机样本
  print(random.sample(range(100), 5))
  
  # 随机打乱
  items = [1, 2, 3, 4, 5]
  random.shuffle(items)
  print(items)
  
  # 随机浮点数
  print(random.random())  # 0.0到1.0之间
  print(random.uniform(1.0, 10.0))  # 1.0到10.0之间
  ```

- **functools**: 高阶函数和操作可调用对象的工具
  ```python
  import functools
  
  # reduce: 累积计算
  print(functools.reduce(lambda x, y: x + y, [1, 2, 3, 4, 5]))  # 15
  
  # partial: 部分应用函数
  basetwo = functools.partial(int, base=2)
  print(basetwo("10010"))  # 18
  
  # lru_cache: 缓存函数结果
  @functools.lru_cache(maxsize=128)
  def fibonacci(n):
      if n <= 1:
          return n
      return fibonacci(n-1) + fibonacci(n-2)
  
  print(fibonacci(30))  # 快速计算，使用缓存
  
  # wraps: 保留被装饰函数的元数据
  def my_decorator(f):
      @functools.wraps(f)
      def wrapper(*args, **kwargs):
          return f(*args, **kwargs)
      return wrapper
  ```

### 9.2 第三方库
Python丰富的第三方库生态是其成功的关键之一。

- **requests**: HTTP客户端库
  ```python
  import requests
  
  # 基本GET请求
  response = requests.get("https://api.github.com")
  print(response.status_code)  # 200
  print(response.headers["content-type"])
  data = response.json()
  
  # 带参数的GET请求
  params = {"key1": "value1", "key2": "value2"}
  response = requests.get("https://httpbin.org/get", params=params)
  print(response.url)  # https://httpbin.org/get?key1=value1&key2=value2
  
  # POST请求
  data = {"username": "user", "password": "pass"}
  response = requests.post("https://httpbin.org/post", data=data)
  
  # 自定义头部
  headers = {"User-Agent": "Mozilla/5.0"}
  response = requests.get("https://httpbin.org/headers", headers=headers)
  
  # 处理cookies
  response = requests.get("https://httpbin.org/cookies/set?name=value")
  print(response.cookies["name"])  # value
  ```

- **numpy**: 科学计算库
  ```python
  import numpy as np
  
  # 创建数组
  a = np.array([1, 2, 3])
  b = np.array([[1, 2, 3], [4, 5, 6]])
  print(a.shape)  # (3,)
  print(b.shape)  # (2, 3)
  
  # 数组操作
  print(a + 1)  # [2 3 4]
  print(a * 2)  # [2 4 6]
  print(a + a)  # [2 4 6]
  
  # 矩阵操作
  x = np.array([[1, 2], [3, 4]])
  y = np.array([[5, 6], [7, 8]])
  print(np.dot(x, y))  # 矩阵乘法
  
  # 统计函数
  print(np.mean(a))  # 2.0
  print(np.std(a))   # 0.816...
  print(np.max(a))   # 3
  
  # 生成数组
  print(np.zeros((2, 3)))  # 全0数组
  print(np.ones((2, 3)))   # 全1数组
  print(np.eye(3))         # 单位矩阵
  print(np.linspace(0, 1, 5))  # 等间距数组
  ```

- **pandas**: 数据分析库
  ```python
  import pandas as pd
  
  # 创建数据结构
  # Series（一维数组）
  s = pd.Series([1, 3, 5, np.nan, 6, 8])
  print(s)
  
  # DataFrame（二维表格）
  df = pd.DataFrame({
      "A": [1, 2, 3, 4],
      "B": pd.date_range("20230101", periods=4),
      "C": pd.Series([1.0, 2.0, 3.0, 4.0]),
      "D": ["a", "b", "c", "d"]
  })
  print(df)
  
  # 读取文件
  # df = pd.read_csv("data.csv")
  # df = pd.read_excel("data.xlsx")
  
  # 数据操作
  print(df.head())  # 前几行
  print(df.describe())  # 统计摘要
  print(df.T)  # 转置
  
  # 选择数据
  print(df["A"])  # 选择单列
  print(df[0:2])  # 选择行
  print(df.loc[0, "A"])  # 按标签选择
  print(df.iloc[0, 0])  # 按位置选择
  
  # 过滤数据
  print(df[df["A"] > 2])
  
  # 分组和聚合
  # df.groupby("A").sum()
  ```

- **matplotlib**: 绘图库
  ```python
  import matplotlib.pyplot as plt
  import numpy as np
  
  # 线图
  x = np.linspace(0, 10, 100)
  y = np.sin(x)
  plt.figure(figsize=(8, 4))
  plt.plot(x, y, label="sin(x)")
  plt.title("Sine Wave")
  plt.xlabel("x")
  plt.ylabel("sin(x)")
  plt.legend()
  # plt.savefig("sine.png")
  # plt.show()
  
  # 散点图
  x = np.random.rand(50)
  y = np.random.rand(50)
  plt.figure()
  plt.scatter(x, y, c="blue", alpha=0.5)
  plt.title("Scatter Plot")
  # plt.show()
  
  # 直方图
  data = np.random.randn(1000)
  plt.figure()
  plt.hist(data, bins=30)
  plt.title("Histogram")
  # plt.show()
  ```

- **flask/django**: Web框架
  ```python
  # Flask示例
  from flask import Flask, request, jsonify
  
  app = Flask(__name__)
  
  @app.route("/")
  def hello():
      return "Hello, World!"
  
  @app.route("/api/data", methods=["GET"])
  def get_data():
      return jsonify({"data": [1, 2, 3, 4, 5]})
  
  @app.route("/api/user", methods=["POST"])
  def create_user():
      data = request.json
      # 处理数据
      return jsonify({"status": "success", "user": data})
  
  # if __name__ == "__main__":
  #     app.run(debug=True)
  ```

  ```python
  # Django示例 (简化版)
  # models.py
  from django.db import models
  
  class User(models.Model):
      name = models.CharField(max_length=100)
      email = models.EmailField(unique=True)
      created_at = models.DateTimeField(auto_now_add=True)
  
  # views.py
  from django.http import JsonResponse
  from .models import User
  
  def get_users(request):
      users = User.objects.all().values()
      return JsonResponse(list(users), safe=False)
  ```

- **sqlalchemy**: ORM库
  ```python
  from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
  from sqlalchemy.ext.declarative import declarative_base
  from sqlalchemy.orm import relationship, sessionmaker
  
  # 连接数据库
  engine = create_engine('sqlite:///example.db')
  Base = declarative_base()
  
  # 定义模型
  class User(Base):
      __tablename__ = 'users'
      id = Column(Integer, primary_key=True)
      name = Column(String)
      email = Column(String, unique=True)
      posts = relationship("Post", back_populates="author")
  
  class Post(Base):
      __tablename__ = 'posts'
      id = Column(Integer, primary_key=True)
      title = Column(String)
      content = Column(String)
      author_id = Column(Integer, ForeignKey('users.id'))
      author = relationship("User", back_populates="posts")
  
  # 创建表
  # Base.metadata.create_all(engine)
  
  # 使用会话
  Session = sessionmaker(bind=engine)
  session = Session()
  
  # 创建用户
  # new_user = User(name="John", email="john@example.com")
  # session.add(new_user)
  # session.commit()
  
  # 查询
  # users = session.query(User).all()
  # for user in users:
  #     print(user.name)
  ```

- **pytest**: 测试框架
  ```python
  # test_example.py
  def add(a, b):
      return a + b
  
  def test_add():
      assert add(1, 2) == 3
      assert add(-1, 1) == 0
      assert add(0, 0) == 0
  
  # 运行测试：pytest test_example.py
  
  # 使用参数化测试
  import pytest
  
  @pytest.mark.parametrize("a,b,expected", [
      (1, 2, 3),
      (-1, 1, 0),
      (0, 0, 0)
  ])
  def test_add_parametrized(a, b, expected):
      assert add(a, b) == expected
  
  # 使用fixture
  @pytest.fixture
  def sample_data():
      return {"key": "value"}
  
  def test_with_fixture(sample_data):
      assert sample_data["key"] == "value"
  ```

### 9.3 虚拟环境和包管理

**虚拟环境**：
```bash
# 创建虚拟环境
python -m venv myenv

# 激活虚拟环境
# Windows
myenv\Scripts\activate
# Unix/MacOS
source myenv/bin/activate

# 退出虚拟环境
deactivate
```

**pip包管理**：
```bash
# 安装包
pip install package_name

# 安装特定版本
pip install package_name==1.0.0

# 从requirements.txt安装
pip install -r requirements.txt

# 列出已安装的包
pip list

# 生成requirements.txt
pip freeze > requirements.txt

# 升级包
pip install --upgrade package_name

# 卸载包
pip uninstall package_name
```

**conda包管理**：
```bash
# 创建环境
conda create --name myenv python=3.9

# 激活环境
conda activate myenv

# 安装包
conda install package_name

# 从环境文件安装
conda env create -f environment.yml

# 导出环境
conda env export > environment.yml

# 列出环境
conda env list
```

**常见面试问题：**
1. 列举Python标准库中你常用的模块，并说明它们的用途。
2. requests库和Python内置的urllib有什么区别？为什么requests更受欢迎？
3. 如何处理JSON数据？演示json模块的基本用法。
4. 什么是ORM？SQLAlchemy的主要特点是什么？
5. 你如何管理Python项目的依赖？虚拟环境的作用是什么？
6. 如何选择Django和Flask之间的框架？它们各有什么优缺点？
7. NumPy和标准Python列表相比有什么优势？
8. Pandas中的DataFrame和Series是什么？如何使用它们进行数据操作？
9. Python的异步库（如asyncio）有什么用途？它解决了什么问题？
10. 如何使用pytest编写单元测试？它与unittest相比有什么优势？

## 10. 代码规范

### 10.1 PEP 8规范
PEP 8是Python官方的代码风格指南，它提供了编写可读性强的Python代码的约定。

**缩进和换行：**
- 缩进使用4个空格（不是制表符Tab）
- 行长度不超过79个字符（文档字符串/注释不超过72个字符）
- 使用反斜杠`\`或括号`()`, `[]`, `{}`来分割长行
- 函数和类之间空两行
- 类中的方法之间空一行
- 在二元运算符周围使用一个空格

```python
# 不推荐
def long_function_name(var_one,var_two,
    var_three,var_four):
    print(var_one)

# 推荐
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# 不推荐
x = 1+2

# 推荐
x = 1 + 2
```

**导入：**
- 导入总是放在文件顶部
- 每行一个导入
- 导入顺序：标准库导入 -> 相关第三方导入 -> 本地应用/库特定导入
- 避免使用通配符导入（`from module import *`）

```python
# 标准库导入
import os
import sys
from datetime import datetime

# 第三方库导入
import numpy as np
import pandas as pd

# 本地应用导入
from mymodule import MyClass
from mypackage.mymodule import function
```

**命名规范：**
- 变量、函数、方法、模块、包名：小写下划线（`snake_case`）
  ```python
  my_variable = 1
  def calculate_total(items):
      pass
  ```
- 类名：大写驼峰（`CamelCase`）
  ```python
  class UserProfile:
      pass
  ```
- 常量：大写下划线（`UPPER_SNAKE_CASE`）
  ```python
  MAX_SPEED = 100
  DEFAULT_CONFIG = {"timeout": 30}
  ```
- 受保护的属性：单下划线前缀（`_protected`）
  ```python
  class MyClass:
      def __init__(self):
          self._protected_attr = 10
  ```
- 私有属性：双下划线前缀（`__private`）
  ```python
  class MyClass:
      def __init__(self):
          self.__private_attr = 10  # 会被修改为_MyClass__private_attr
  ```
- 单下划线作为未使用变量名
  ```python
  for _ in range(5):
      print("Hello")
  ```

**注释：**
- 注释应该是完整的句子
- 使用英语注释，除非你确定代码永远不会被不懂你的语言的人阅读
- 代码更新时更新相关注释
- 代码应该是自解释的，注释应该解释为什么，而不是做什么
- 对于复杂的操作，写明做什么

```python
# 不推荐
# increment x by 1
x += 1

# 推荐（复杂逻辑需要说明）
# 补偿浮点误差，确保值总是正数
x = max(0.0, x + 0.1)
```

**文档字符串：**
- 使用三重双引号`"""`
- 函数文档包括简介、参数、返回值、异常等
- 类文档应该包括类的行为和公共属性

```python
def complex_function(param1, param2):
    """计算并返回两个参数的复杂函数结果。
    
    详细说明函数的计算方法和使用场景。
    
    Args:
        param1 (int): 第一个参数的描述。
        param2 (str): 第二个参数的描述。
        
    Returns:
        bool: 返回值的描述。
        
    Raises:
        ValueError: 抛出异常的条件描述。
    """
    # 函数实现
    pass
```

### 10.2 代码质量工具
Python提供了多种工具来帮助维护代码质量和规范。

- **pylint**：静态代码分析工具，检查代码错误和规范问题
  ```bash
  # 安装
  pip install pylint
  
  # 基本使用
  pylint mymodule.py
  
  # 使用配置文件
  pylint --rcfile=pylintrc mymodule.py
  ```
  
  在项目中添加`.pylintrc`配置文件：
  ```ini
  [MASTER]
  disable=C0111,C0103
  
  [FORMAT]
  max-line-length=100
  ```

- **black**：自动代码格式化工具，无需配置
  ```bash
  # 安装
  pip install black
  
  # 格式化单个文件
  black mymodule.py
  
  # 格式化整个项目
  black .
  
  # 只检查而不修改
  black --check mymodule.py
  ```

- **isort**：自动排序import语句
  ```bash
  # 安装
  pip install isort
  
  # 基本使用
  isort mymodule.py
  
  # 递归处理目录
  isort -rc .
  
  # 与black兼容
  isort --profile black mymodule.py
  ```

- **mypy**：静态类型检查工具
  ```bash
  # 安装
  pip install mypy
  
  # 检查单个文件
  mypy mymodule.py
  
  # 检查带有类型注解的代码
  ```python
  # typed_example.py
  def greeting(name: str) -> str:
      return 'Hello ' + name
  
  greeting(123)  # mypy会检测到类型错误
  ```

- **flake8**：组合了pycodestyle、pyflakes和McCabe复杂度检查工具
  ```bash
  # 安装
  pip install flake8
  
  # 基本使用
  flake8 mymodule.py
  
  # 忽略特定错误
  flake8 --ignore=E501,F401 mymodule.py
  ```

- **pre-commit**：Git钩子管理工具，可以在提交前运行检查
  ```bash
  # 安装
  pip install pre-commit
  
  # 创建配置文件.pre-commit-config.yaml
  repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.1
    hooks:
    - id: trailing-whitespace
    - id: end-of-file-fixer
  
  - repo: https://github.com/psf/black
    rev: 21.5b2
    hooks:
    - id: black
  
  - repo: https://github.com/pycqa/isort
    rev: 5.8.0
    hooks:
    - id: isort
  
  # 安装git钩子
  pre-commit install
  ```

### 10.3 类型注解
Python 3.5+支持类型注解，可以使代码更加清晰并支持静态类型检查。

**基本类型注解：**
```python
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> str:
    return f"Hello, {name}"

def process_items(items: list[int]) -> None:
    for item in items:
        print(item)
```

**复杂类型注解：**
```python
from typing import List, Dict, Tuple, Optional, Union, Callable, Any, TypeVar

# 列表、字典、元组
def process_data(numbers: List[int],
                 config: Dict[str, str],
                 point: Tuple[float, float]) -> List[float]:
    return [float(n) for n in numbers]

# 可选类型
def fetch_user(user_id: int) -> Optional[Dict[str, Any]]:
    if user_id > 0:
        return {"id": user_id, "name": "User"}
    return None

# 联合类型
def parse_value(value: Union[str, int, float]) -> float:
    return float(value)

# 函数类型
CalculatorFunc = Callable[[int, int], int]

def apply_operation(a: int, b: int, op: CalculatorFunc) -> int:
    return op(a, b)

# 泛型
T = TypeVar('T')

def first_element(items: List[T]) -> Optional[T]:
    if items:
        return items[0]
    return None
```

**类注解：**
```python
class User:
    def __init__(self, name: str, age: int) -> None:
        self.name: str = name
        self.age: int = age
    
    def greet(self) -> str:
        return f"Hello, {self.name}"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(data['name'], data['age'])
```

**类型别名：**
```python
from typing import Dict, List, Union

# 定义类型别名
UserId = int
UserData = Dict[str, Union[str, int]]
UserList = List[UserData]

def get_user(user_id: UserId) -> UserData:
    return {"id": user_id, "name": "User"}

def get_all_users() -> UserList:
    return [{"id": 1, "name": "User 1"}, {"id": 2, "name": "User 2"}]
```

### 10.4 文档编写
良好的文档对于代码的可维护性至关重要。

**内联文档（Docstrings）：**
```python
def calculate_discount(price: float, discount_rate: float) -> float:
    """计算折扣后的价格。
    
    Args:
        price: 原始价格。
        discount_rate: 折扣率，0到1之间的小数。
        
    Returns:
        折扣后的价格。
        
    Raises:
        ValueError: 如果折扣率不在0到1之间。
    """
    if not 0 <= discount_rate <= 1:
        raise ValueError("折扣率必须在0到1之间")
    return price * (1 - discount_rate)
```

**使用Sphinx生成文档：**
```bash
# 安装Sphinx
pip install sphinx

# 创建文档骨架
mkdir docs
cd docs
sphinx-quickstart

# 在源文件中使用Napoleon扩展来解析Google风格的docstrings
# 在conf.py中添加
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]

# 构建文档
sphinx-build -b html . _build
```

**使用ReadTheDocs托管文档**:
1. 在项目根目录创建`.readthedocs.yml`文件
2. 配置构建环境和依赖
3. 推送到GitHub并连接到ReadTheDocs

**README文件：**
```markdown
# 项目名称

简短描述项目的功能和目的。

## 安装

```bash
pip install mypackage
```

## 使用示例

```python
from mypackage import MyClass

obj = MyClass()
obj.do_something()
```

## 文档

完整文档请访问 [docs.example.com](https://docs.example.com).

## 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献代码。

## 许可证

该项目使用 MIT 许可证 - 详细信息请见 [LICENSE](LICENSE) 文件。
```

### 10.5 最佳实践

**变量命名的最佳实践：**
```python
# 不推荐
x = 5  # 含义不明确
tmp = get_user()  # 临时变量名不明确
l = [1, 2, 3]  # 使用了容易混淆的单字母

# 推荐
count = 5  # 明确表示计数
user_data = get_user()  # 清晰表明内容
numbers = [1, 2, 3]  # 明确表示内容
```

**函数设计的最佳实践：**
```python
# 不推荐：函数做太多事情
def process_user(user_id):
    user = get_user(user_id)
    if user:
        user['status'] = 'active'
        save_user(user)
        send_email(user['email'], 'Welcome!')
        return True
    return False

# 推荐：单一职责原则
def activate_user(user_id):
    user = get_user(user_id)
    if not user:
        return False
    
    user['status'] = 'active'
    save_user(user)
    return True

def send_welcome_email(user_id):
    user = get_user(user_id)
    if user:
        send_email(user['email'], 'Welcome!')
        return True
    return False
```

**异常处理的最佳实践：**
```python
# 不推荐：捕获所有异常并忽略
try:
    process_data()
except Exception:
    pass  # 忽略所有错误

# 推荐：只捕获预期的异常并处理
try:
    process_data()
except ValueError as e:
    logger.error(f"数据格式错误: {e}")
    # 处理错误
except IOError as e:
    logger.error(f"IO错误: {e}")
    # 处理错误
```

**代码组织的最佳实践：**
```python
# 模块级别的组织
"""模块描述。

这个模块提供了...
"""

# 标准库导入
import os
import sys

# 第三方库导入
import numpy as np

# 本地应用导入
from . import local_module

# 常量
MAX_SIZE = 100

# 类定义
class MyClass:
    """类描述。"""
    pass

# 函数定义
def my_function():
    """函数描述。"""
    pass

# 仅在作为脚本运行时执行的代码
if __name__ == "__main__":
    my_function()
```

**常见面试问题：**
1. 什么是PEP 8？为什么它对Python开发很重要？
2. 描述Python中的主要命名约定。
3. 如何在团队项目中确保代码质量和一致性？
4. Python的类型注解有什么好处？它们是必需的吗？
5. 你使用过哪些Python代码质量工具？它们如何帮助改进代码？
6. 如何在Python中组织大型项目的代码结构？
7. 什么是"Pythonic"代码？举例说明。
8. 解释Python中的"鸭子类型"及其相对于静态类型检查的优缺点。

## 11. 面试常见算法题

### 11.1 排序算法
排序算法是面试中常见的考点，了解它们的实现和复杂度是必要的。

**冒泡排序 (Bubble Sort)**：
- 时间复杂度：O(n²)
- 空间复杂度：O(1)
- 稳定性：稳定

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        # 最后i个元素已经就位
        for j in range(0, n-i-1):
            # 从头到尾遍历未排序部分
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```

**优化的冒泡排序**：
```python
def optimized_bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        
        # 如果内层循环没有交换元素，说明数组已经有序
        if not swapped:
            break
    return arr
```

**快速排序 (Quick Sort)**：
- 时间复杂度：平均 O(n log n)，最坏 O(n²)
- 空间复杂度：O(log n)
- 稳定性：不稳定

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]  # 选择中间元素作为基准
    left = [x for x in arr if x < pivot]  # 小于基准的元素
    middle = [x for x in arr if x == pivot]  # 等于基准的元素
    right = [x for x in arr if x > pivot]  # 大于基准的元素
    
    return quick_sort(left) + middle + quick_sort(right)
```

**原地快速排序**：
```python
def partition(arr, low, high):
    pivot = arr[high]  # 选择最右边的元素作为基准
    i = low - 1  # 小于基准的区域右边界
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1

def quick_sort_in_place(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)
        quick_sort_in_place(arr, low, pivot_index - 1)
        quick_sort_in_place(arr, pivot_index + 1, high)
    return arr

# 使用
def quick_sort_wrapper(arr):
    return quick_sort_in_place(arr, 0, len(arr) - 1)
```

**归并排序 (Merge Sort)**：
- 时间复杂度：O(n log n)
- 空间复杂度：O(n)
- 稳定性：稳定

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    # 分割数组
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    # 递归排序
    left = merge_sort(left)
    right = merge_sort(right)
    
    # 合并已排序的数组
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    # 比较左右数组元素并合并
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # 添加剩余元素
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**堆排序 (Heap Sort)**：
- 时间复杂度：O(n log n)
- 空间复杂度：O(1)
- 稳定性：不稳定

```python
def heapify(arr, n, i):
    largest = i  # 初始化最大值为根节点
    left = 2 * i + 1
    right = 2 * i + 2
    
    # 检查左子节点是否存在且大于根节点
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # 检查右子节点是否存在且大于当前最大值
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # 如果最大值不是根节点，交换并继续调整堆
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    
    # 构建最大堆
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # 依次提取堆顶元素
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # 交换
        heapify(arr, i, 0)  # 调整剩余堆
    
    return arr
```

**算法选择和性能比较**：

| 算法 | 最好时间 | 平均时间 | 最坏时间 | 空间 | 稳定性 | 适用场景 |
|------|----------|----------|----------|------|--------|----------|
| 冒泡排序 | O(n) | O(n²) | O(n²) | O(1) | 稳定 | 小数据集 |
| 快速排序 | O(n log n) | O(n log n) | O(n²) | O(log n) | 不稳定 | 大多数情况 |
| 归并排序 | O(n log n) | O(n log n) | O(n log n) | O(n) | 稳定 | 稳定性要求高 |
| 堆排序 | O(n log n) | O(n log n) | O(n log n) | O(1) | 不稳定 | 空间受限 |

### 11.2 查找算法
高效的查找算法对于处理大数据集至关重要。

**线性查找 (Linear Search)**：
- 时间复杂度：O(n)
- 空间复杂度：O(1)

```python
def linear_search(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i  # 返回索引
    return -1  # 未找到
```

**二分查找 (Binary Search)**：
- 时间复杂度：O(log n)
- 空间复杂度：O(1)（迭代版本）或 O(log n)（递归版本）
- 前提：数组必须有序

```python
# 迭代版本
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid  # 找到目标，返回索引
        elif arr[mid] < target:
            left = mid + 1  # 目标在右半部分
        else:
            right = mid - 1  # 目标在左半部分
    
    return -1  # 未找到目标

# 递归版本
def binary_search_recursive(arr, target, left, right):
    if left > right:
        return -1  # 基本情况：未找到
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid  # 找到目标
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)  # 右侧搜索
    else:
        return binary_search_recursive(arr, target, left, mid - 1)  # 左侧搜索
```

**哈希查找 (Hash Search)**：
- 时间复杂度：平均 O(1)，最坏 O(n)
- 空间复杂度：O(n)

```python
def hash_search(hash_table, key):
    if key in hash_table:
        return hash_table[key]
    return None

# 使用字典实现
def build_hash_table(arr):
    hash_table = {}
    for i, value in enumerate(arr):
        hash_table[value] = i
    return hash_table

# 使用例子
arr = [10, 20, 30, 40, 50]
hash_table = build_hash_table(arr)
print(hash_search(hash_table, 30))  # 输出: 2
```

**树查找 (Tree Search)**：
使用二叉搜索树进行查找：

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert_into_bst(root, value):
    if root is None:
        return TreeNode(value)
    
    if value < root.value:
        root.left = insert_into_bst(root.left, value)
    else:
        root.right = insert_into_bst(root.right, value)
    
    return root

def search_in_bst(root, value):
    if root is None or root.value == value:
        return root
    
    if value < root.value:
        return search_in_bst(root.left, value)
    return search_in_bst(root.right, value)

# 构建二叉搜索树
def build_bst(arr):
    root = None
    for value in arr:
        root = insert_into_bst(root, value)
    return root
```

### 11.3 动态规划
动态规划是一种通过将复杂问题分解为子问题并存储子问题的解来解决问题的方法。

**斐波那契数列**：
```python
# 递归解法（效率低）
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)

# 动态规划（自底向上）
def fib_dp(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

# 优化空间复杂度
def fib_optimized(n):
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b
```

**背包问题 (0-1 Knapsack Problem)**：
```python
def knapsack(weights, values, capacity):
    n = len(weights)
    # 创建DP表格
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # 填充DP表格
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # 如果当前物品重量大于容量，不选
            if weights[i-1] > w:
                dp[i][w] = dp[i-1][w]
            else:
                # 取最大值：不选当前物品 vs 选当前物品
                dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w - weights[i-1]])
    
    return dp[n][capacity]

# 优化空间复杂度
def knapsack_optimized(weights, values, capacity):
    n = len(weights)
    dp = [0 for _ in range(capacity + 1)]
    
    for i in range(n):
        # 逆序遍历防止重复计算
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    
    return dp[capacity]
```

**最长公共子序列 (Longest Common Subsequence)**：
```python
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

**最大子数组和 (Maximum Subarray)**：
```python
def max_subarray(nums):
    if not nums:
        return 0
    
    current_sum = max_sum = nums[0]
    
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**硬币找零问题 (Coin Change)**：
```python
def coin_change(coins, amount):
    # 初始化DP数组
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

### 11.4 常见面试算法题

**两数之和 (Two Sum)**：
```python
def two_sum(nums, target):
    # 使用字典存储已遍历过的数字及其索引
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    
    return []  # 没有找到符合条件的两个数
```

**字符串回文判断 (Palindrome Check)**：
```python
def is_palindrome(s):
    # 移除非字母数字字符并转为小写
    s = ''.join(c.lower() for c in s if c.isalnum())
    
    # 判断是否回文
    return s == s[::-1]

# 或者使用双指针
def is_palindrome_two_pointers(s):
    s = ''.join(c.lower() for c in s if c.isalnum())
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True
```

**有效的括号 (Valid Parentheses)**：
```python
def is_valid_parentheses(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:  # 是右括号
            top_element = stack.pop() if stack else '#'
            if top_element != mapping[char]:
                return False
        else:  # 是左括号
            stack.append(char)
    
    return not stack  # 栈为空表示所有括号都匹配
```

**反转链表 (Reverse Linked List)**：
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    prev = None
    current = head
    
    while current:
        next_temp = current.next  # 临时存储下一个节点
        current.next = prev       # 反转链接
        prev = current            # 移动prev
        current = next_temp       # 移动current
    
    return prev  # 新的头节点是原来的尾节点
```

**合并两个有序链表 (Merge Two Sorted Lists)**：
```python
def merge_two_sorted_lists(l1, l2):
    # 创建一个哑节点作为合并链表的头节点
    dummy = ListNode(-1)
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # 连接剩余部分
    current.next = l1 if l1 else l2
    
    return dummy.next
```

**二叉树深度优先遍历 (DFS)**：
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# 先序遍历（根-左-右）
def preorder_traversal(root):
    if not root:
        return []
    
    result = [root.val]
    result.extend(preorder_traversal(root.left))
    result.extend(preorder_traversal(root.right))
    
    return result

# 中序遍历（左-根-右）
def inorder_traversal(root):
    if not root:
        return []
    
    result = []
    result.extend(inorder_traversal(root.left))
    result.append(root.val)
    result.extend(inorder_traversal(root.right))
    
    return result

# 后序遍历（左-右-根）
def postorder_traversal(root):
    if not root:
        return []
    
    result = []
    result.extend(postorder_traversal(root.left))
    result.extend(postorder_traversal(root.right))
    result.append(root.val)
    
    return result
```

**二叉树宽度优先遍历 (BFS)**：
```python
from collections import deque

def level_order_traversal(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

**常见面试问题：**
1. 描述快速排序的基本原理，它的平均、最好和最坏情况下的时间复杂度是多少？
2. 什么情况下应该使用归并排序而不是快速排序？
3. 解释二分查找的工作原理和局限性。
4. 什么是动态规划？它与分治算法有什么区别？
5. 描述解决斐波那契数列问题的不同方法及其复杂度。
6. 如何优化递归算法以避免重复计算？
7. 解释回溯算法的基本思想及其应用场景。
8. 贪心算法与动态规划之间的区别是什么？它们各自适合解决什么类型的问题？

## 12. 项目经验

### 12.1 项目介绍要点
- 项目背景
- 技术栈选择
- 架构设计
- 难点和解决方案
- 性能优化
- 团队协作

### 12.2 常见问题
- 为什么选择这个技术栈？
- 遇到的最大挑战是什么？
- 如何解决性能问题？
- 如何保证代码质量？
- 如何进行团队协作？

## 13. 系统设计

### 13.1 设计原则
在软件开发中，遵循良好的设计原则可以提高代码质量、可维护性和可扩展性。

**SOLID原则**：
- **S：单一职责原则 (Single Responsibility Principle)**
  - 一个类应该只有一个引起它变化的原因
  ```python
  # 不好的设计：一个类负责多个职责
  class UserManager:
      def register_user(self, user):
          # 注册用户
          pass
      
      def send_email(self, user, message):
          # 发送邮件
          pass
      
      def generate_report(self, users):
          # 生成报告
          pass
  
  # 好的设计：分离职责
  class UserRegistration:
      def register_user(self, user):
          # 注册用户
          pass
  
  class EmailService:
      def send_email(self, user, message):
          # 发送邮件
          pass
  
  class ReportGenerator:
      def generate_report(self, users):
          # 生成报告
          pass
  ```

- **O：开放/封闭原则 (Open/Closed Principle)**
  - 软件实体应该对扩展开放，对修改封闭
  ```python
  # 不好的设计：需要修改类来添加新形状
  class AreaCalculator:
      def calculate_area(self, shape):
          if isinstance(shape, Rectangle):
              return shape.width * shape.height
          elif isinstance(shape, Circle):
              return 3.14 * shape.radius ** 2
          # 添加新形状需要修改这个类
  
  # 好的设计：使用多态
  class Shape:
      def area(self):
          pass
  
  class Rectangle(Shape):
      def __init__(self, width, height):
          self.width = width
          self.height = height
      
      def area(self):
          return self.width * self.height
  
  class Circle(Shape):
      def __init__(self, radius):
          self.radius = radius
      
      def area(self):
          return 3.14 * self.radius ** 2
  
  # 新的形状可以通过继承Shape来添加，无需修改AreaCalculator
  class AreaCalculator:
      def calculate_area(self, shape):
          return shape.area()
  ```

- **L：里氏替换原则 (Liskov Substitution Principle)**
  - 子类应该能够替换其基类使用
  ```python
  # 违反里氏替换原则
  class Bird:
      def fly(self):
          return "I can fly"
  
  class Penguin(Bird):  # 企鹅是鸟，但不能飞
      def fly(self):
          raise Exception("I can't fly")  # 违反了基类的行为
  
  # 符合里氏替换原则
  class Bird:
      def move(self):
          return "I can move"
  
  class FlyingBird(Bird):
      def move(self):
          return "I can fly"
  
  class NonFlyingBird(Bird):
      def move(self):
          return "I can walk"
  
  class Penguin(NonFlyingBird):
      pass
  ```

- **I：接口隔离原则 (Interface Segregation Principle)**
  - 客户端不应该被迫依赖它们不使用的方法
  ```python
  # 违反接口隔离原则
  class Worker:
      def work(self):
          pass
      
      def eat(self):
          pass
  
  # 符合接口隔离原则
  class Workable:
      def work(self):
          pass
  
  class Eatable:
      def eat(self):
          pass
  
  class Worker(Workable, Eatable):
      def work(self):
          # 实现工作逻辑
          pass
      
      def eat(self):
          # 实现吃饭逻辑
          pass
  
  class Robot(Workable):  # 机器人只需工作接口
      def work(self):
          # 实现工作逻辑
          pass
  ```

- **D：依赖反转原则 (Dependency Inversion Principle)**
  - 高层模块不应该依赖低层模块，两者都应该依赖抽象
  ```python
  # 违反依赖反转原则
  class MySQLDatabase:
      def connect(self):
          # 连接到MySQL
          pass
  
  class UserRepository:
      def __init__(self):
          self.database = MySQLDatabase()  # 直接依赖具体实现
      
      def save(self, user):
          self.database.connect()
          # 保存用户
  
  # 符合依赖反转原则
  class Database:
      def connect(self):
          pass
  
  class MySQLDatabase(Database):
      def connect(self):
          # 连接到MySQL
          pass
  
  class PostgreSQLDatabase(Database):
      def connect(self):
          # 连接到PostgreSQL
          pass
  
  class UserRepository:
      def __init__(self, database):
          self.database = database  # 依赖抽象
      
      def save(self, user):
          self.database.connect()
          # 保存用户
  ```

**DRY原则 (Don't Repeat Yourself)**：
- 避免代码重复
```python
# 违反DRY原则
def validate_email(email):
    # 验证邮箱
    if '@' in email and '.' in email:
        return True
    return False

def create_user(name, email):
    # 重复了验证逻辑
    if '@' in email and '.' in email:
        # 创建用户
        pass
    else:
        raise ValueError("Invalid email")

# 符合DRY原则
def validate_email(email):
    # 验证邮箱
    if '@' in email and '.' in email:
        return True
    return False

def create_user(name, email):
    if validate_email(email):
        # 创建用户
        pass
    else:
        raise ValueError("Invalid email")
```

**KISS原则 (Keep It Simple, Stupid)**：
- 保持简单，避免不必要的复杂性
```python
# 过于复杂
def is_even(num):
    return True if num % 2 == 0 else False

# 简单明了
def is_even(num):
    return num % 2 == 0
```

**YAGNI原则 (You Aren't Gonna Need It)**：
- 不要实现当前不需要的功能
```python
# 违反YAGNI
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.preferences = {}  # 未来可能需要
        self.activity_log = [] # 未来可能需要
        self.friends = []      # 未来可能需要

# 符合YAGNI
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

### 13.2 常见系统设计题
系统设计是面试中常见的高级主题，了解如何设计可扩展系统是很重要的。

**设计一个缓存系统**：
```python
class LRUCache:
    """
    基于LRU（最近最少使用）策略的缓存系统
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # 键值对存储
        self.order = []  # 访问顺序

    def get(self, key):
        if key in self.cache:
            # 更新访问顺序
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        if key in self.cache:
            # 更新已有键
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # 移除最久未使用的项
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        # 添加新项
        self.cache[key] = value
        self.order.append(key)
```

**更高效的LRU缓存实现（使用OrderedDict）**：
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        
        # 将访问的项移到末尾（最近使用）
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def put(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            # popitem(last=False) 移除最早添加的项
            self.cache.popitem(last=False)
        
        self.cache[key] = value
```

**设计一个消息队列**：
```python
import time
import threading
import queue

class MessageQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.running = False
        self.consumers = []

    def start(self):
        """启动消息队列"""
        self.running = True
        
    def stop(self):
        """停止消息队列"""
        self.running = False
        # 通知所有消费者停止
        for consumer in self.consumers:
            consumer.join()
        print("消息队列已停止")

    def enqueue(self, message):
        """生产者：将消息添加到队列"""
        if self.running:
            self.queue.put(message)
            print(f"生产消息: {message}")
        else:
            raise RuntimeError("消息队列未启动")

    def register_consumer(self, callback):
        """注册消费者"""
        consumer = threading.Thread(target=self._consumer_loop, args=(callback,))
        self.consumers.append(consumer)
        consumer.start()
        return consumer

    def _consumer_loop(self, callback):
        """消费者处理循环"""
        while self.running:
            try:
                # 非阻塞方式获取消息
                message = self.queue.get(block=True, timeout=1)
                print(f"消费消息: {message}")
                callback(message)
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"消费消息出错: {e}")

# 使用示例
def message_handler(message):
    print(f"处理消息: {message}")
    time.sleep(0.5)  # 模拟处理时间

message_queue = MessageQueue()
message_queue.start()

# 注册消费者
consumer = message_queue.register_consumer(message_handler)

# 生产消息
for i in range(5):
    message_queue.enqueue(f"消息 {i}")

# 等待所有消息处理完成
message_queue.queue.join()

# 停止消息队列
message_queue.stop()
```

**设计一个短链接系统**：
```python
import hashlib
import base64
import random
import string

class URLShortener:
    def __init__(self):
        self.url_mapping = {}  # 短URL到长URL的映射
        self.base_url = "http://short.url/"

    def shorten(self, long_url):
        """将长URL转换为短URL"""
        # 方法1：使用哈希
        # md5_hash = hashlib.md5(long_url.encode()).digest()
        # short_code = base64.b64encode(md5_hash)[:6].decode()
        
        # 方法2：随机生成
        chars = string.ascii_letters + string.digits
        short_code = ''.join(random.choice(chars) for _ in range(6))
        
        short_url = self.base_url + short_code
        self.url_mapping[short_code] = long_url
        return short_url

    def expand(self, short_url):
        """将短URL转换回长URL"""
        if not short_url.startswith(self.base_url):
            raise ValueError("无效的短URL")
        
        short_code = short_url[len(self.base_url):]
        if short_code not in self.url_mapping:
            raise ValueError("未找到对应的长URL")
        
        return self.url_mapping[short_code]

# 使用示例
shortener = URLShortener()
long_url = "https://www.example.com/very/long/url/that/needs/shortening"
short_url = shortener.shorten(long_url)
print(f"短URL: {short_url}")
expanded_url = shortener.expand(short_url)
print(f"长URL: {expanded_url}")
```

**设计一个秒杀系统**：
```python
import time
import threading
import queue
import redis
from datetime import datetime

class FlashSaleSystem:
    def __init__(self, product_id, stock, price, start_time, end_time):
        self.product_id = product_id
        self.stock = stock
        self.price = price
        self.start_time = start_time
        self.end_time = end_time
        self.order_queue = queue.Queue()
        self.lock = threading.Lock()
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
        # 初始化库存到Redis
        self.redis_client.set(f"product:{product_id}:stock", stock)
    
    def is_active(self):
        """检查秒杀是否处于活动时间内"""
        now = datetime.now()
        return self.start_time <= now <= self.end_time
    
    def place_order(self, user_id):
        """用户下单"""
        if not self.is_active():
            return {"success": False, "message": "秒杀活动未开始或已结束"}
        
        # 使用Redis进行原子减库存操作
        remaining = self.redis_client.decr(f"product:{self.product_id}:stock")
        
        if remaining < 0:
            # 库存不足，恢复库存计数
            self.redis_client.incr(f"product:{self.product_id}:stock")
            return {"success": False, "message": "商品已售罄"}
        
        # 将订单放入队列异步处理
        order = {
            "user_id": user_id,
            "product_id": self.product_id,
            "price": self.price,
            "timestamp": time.time()
        }
        self.order_queue.put(order)
        
        return {"success": True, "message": "下单成功，正在处理"}
    
    def process_orders(self):
        """异步处理订单队列"""
        while True:
            try:
                order = self.order_queue.get(timeout=1)
                # 这里应该是实际的订单处理逻辑
                # 例如：保存到数据库，扣减用户余额等
                print(f"处理订单: {order}")
                time.sleep(0.1)  # 模拟处理时间
                self.order_queue.task_done()
            except queue.Empty:
                if not self.is_active() and self.order_queue.empty():
                    break
    
    def start(self):
        """启动秒杀系统"""
        # 启动订单处理线程
        processor = threading.Thread(target=self.process_orders)
        processor.daemon = True
        processor.start()
        print(f"秒杀系统已启动，商品ID: {self.product_id}")

# 使用示例
start_time = datetime.now()  # 立即开始
end_time = datetime.fromtimestamp(time.time() + 3600)  # 一小时后结束

flash_sale = FlashSaleSystem(
    product_id="iphone13",
    stock=100,
    price=4999.00,
    start_time=start_time,
    end_time=end_time
)

flash_sale.start()

# 模拟多个用户同时下单
for user_id in range(1, 150):
    result = flash_sale.place_order(f"user_{user_id}")
    print(f"用户 {user_id} 下单结果: {result}")
```

### 13.3 微服务架构
微服务架构是一种将应用程序设计为小型、独立服务集合的方法。

**微服务的主要特点**：
- 单一职责：每个服务负责特定的业务功能
- 独立部署：服务可以独立开发、测试和部署
- 技术多样性：不同服务可以使用不同的技术栈
- 分布式：服务之间通过网络通信

**微服务示例架构**：
```python
# 用户服务
class UserService:
    def __init__(self, database):
        self.database = database
    
    def get_user(self, user_id):
        # 从数据库获取用户信息
        return {"id": user_id, "name": "用户名"}
    
    def create_user(self, user_data):
        # 在数据库中创建用户
        pass

# 订单服务
class OrderService:
    def __init__(self, database, user_service_url):
        self.database = database
        self.user_service_url = user_service_url
    
    def create_order(self, user_id, items):
        # 调用用户服务验证用户
        user = self._call_user_service(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        # 创建订单
        order_id = self._store_order(user_id, items)
        return {"order_id": order_id}
    
    def _call_user_service(self, user_id):
        # 实际应用中会使用HTTP请求调用用户服务
        import requests
        response = requests.get(f"{self.user_service_url}/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def _store_order(self, user_id, items):
        # 存储订单到数据库
        return "order_123"  # 返回订单ID

# API网关
class APIGateway:
    def __init__(self, user_service, order_service):
        self.user_service = user_service
        self.order_service = order_service
    
    def handle_request(self, path, method, data=None):
        # 路由请求到适当的服务
        if path.startswith("/users"):
            return self._handle_user_request(path, method, data)
        elif path.startswith("/orders"):
            return self._handle_order_request(path, method, data)
        else:
            return {"error": "Not Found"}, 404
    
    def _handle_user_request(self, path, method, data):
        # 处理用户相关请求
        pass
    
    def _handle_order_request(self, path, method, data):
        # 处理订单相关请求
        pass
```

**使用FastAPI实现微服务**：
```python
# user_service.py
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# 简化起见，使用内存存储
users_db = {}

class User(BaseModel):
    name: str
    email: str

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.post("/users/")
async def create_user(user: User):
    user_id = f"user_{len(users_db) + 1}"
    users_db[user_id] = {"id": user_id, **user.dict()}
    return users_db[user_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# order_service.py
from fastapi import FastAPI, HTTPException
import uvicorn
import requests
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 简化起见，使用内存存储
orders_db = {}

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]

@app.post("/orders/")
async def create_order(order: OrderCreate):
    # 调用用户服务验证用户
    try:
        response = requests.get(f"http://user-service:8000/users/{order.user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="User service unavailable")
    
    # 创建订单
    order_id = f"order_{len(orders_db) + 1}"
    orders_db[order_id] = {
        "id": order_id,
        "user_id": order.user_id,
        "items": [item.dict() for item in order.items],
        "status": "created"
    }
    return orders_db[order_id]

@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

### 13.4 设计模式与架构模式
架构模式是更高级别的设计模式，适用于整个系统架构。

**MVC模式 (Model-View-Controller)**：
```python
# Model
class UserModel:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
    
    @staticmethod
    def get_user(user_id):
        # 从数据库获取用户
        return UserModel(user_id, "John Doe", "john@example.com")
    
    def save(self):
        # 保存用户到数据库
        pass

# View
class UserView:
    def show_user_details(self, user):
        return f"User: {user.name}, Email: {user.email}"
    
    def show_error(self, message):
        return f"Error: {message}"

# Controller
class UserController:
    def __init__(self):
        self.view = UserView()
    
    def show_user(self, user_id):
        try:
            user = UserModel.get_user(user_id)
            return self.view.show_user_details(user)
        except Exception as e:
            return self.view.show_error(str(e))
    
    def create_user(self, name, email):
        try:
            # 生成用户ID
            user_id = "user_123"  # 简化示例
            user = UserModel(user_id, name, email)
            user.save()
            return self.view.show_user_details(user)
        except Exception as e:
            return self.view.show_error(str(e))
```

**MVVM模式 (Model-View-ViewModel)**：
```python
# Model
class UserModel:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
    
    @staticmethod
    def get_user(user_id):
        # 从数据库获取用户
        return UserModel(user_id, "John Doe", "john@example.com")

# ViewModel
class UserViewModel:
    def __init__(self):
        self.user = None
        self.error = None
        self._observers = []
    
    def add_observer(self, observer):
        self._observers.append(observer)
    
    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)
    
    def load_user(self, user_id):
        try:
            self.user = UserModel.get_user(user_id)
            self.error = None
        except Exception as e:
            self.user = None
            self.error = str(e)
        self.notify_observers()
    
    def get_display_name(self):
        if self.user:
            return f"{self.user.name} ({self.user.email})"
        return ""

# View (Observer)
class UserView:
    def __init__(self, view_model):
        self.view_model = view_model
        self.view_model.add_observer(self)
    
    def update(self, view_model):
        if view_model.error:
            self.show_error(view_model.error)
        else:
            self.show_user()
    
    def show_user(self):
        print(f"User: {self.view_model.get_display_name()}")
    
    def show_error(self, message):
        print(f"Error: {message}")
    
    def load_user(self, user_id):
        self.view_model.load_user(user_id)
```

**常见面试问题：**
1. 解释SOLID原则并举例说明每个原则。
2. 什么是微服务架构？它与单体架构相比有什么优缺点？
3. 如何设计一个高并发系统？有哪些关键考虑因素？
4. 解释CAP定理及其对分布式系统设计的影响。
5. 如何设计一个可扩展的API服务？
6. 什么是负载均衡？它在系统设计中的作用是什么？
7. 如何处理分布式系统中的数据一致性问题？
8. 设计一个简单的Twitter或社交媒体系统，考虑扩展性。
9. MVC和MVVM架构模式的区别是什么？
10. 如何设计一个具有高可用性的系统？

## 14. 数据库

### 14.1 数据库基础知识

#### SQL和NoSQL数据库比较

**SQL数据库**:
- 关系型数据库，如MySQL, PostgreSQL, SQLite, Oracle, SQL Server
- 使用结构化查询语言(SQL)
- 有预定义模式和表结构
- ACID特性保证

**NoSQL数据库**:
- 非关系型数据库，如MongoDB, Redis, Cassandra, DynamoDB
- 不要求固定模式
- 通常提供更高的可扩展性和性能
- 适合大数据和实时Web应用

**Python中使用SQL数据库**:
```python
import sqlite3

# 创建连接和游标
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 插入数据
def add_user(username, email):
    try:
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.rollback()
        return None

# 查询数据
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

def get_all_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# 更新数据
def update_email(user_id, new_email):
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )
    conn.commit()
    return cursor.rowcount

# 删除数据
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return cursor.rowcount

# 使用示例
user_id = add_user("johndoe", "john@example.com")
print(f"新增用户ID: {user_id}")
print(f"用户信息: {get_user(user_id)}")
update_email(user_id, "john.doe@example.com")
print(f"更新后: {get_user(user_id)}")
print(f"所有用户: {get_all_users()}")
delete_user(user_id)
print(f"删除后: {get_all_users()}")

# 关闭连接
conn.close()
```

**Python中使用NoSQL数据库 (MongoDB)**:
```python
import pymongo
from datetime import datetime

# 创建连接
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["example_db"]
users_collection = db["users"]

# 插入文档
def add_user(user_data):
    user_data["created_at"] = datetime.now()
    result = users_collection.insert_one(user_data)
    return result.inserted_id

# 查询文档
def get_user(user_id):
    from bson.objectid import ObjectId
    return users_collection.find_one({"_id": ObjectId(user_id)})

def get_users_by_criteria(criteria):
    return list(users_collection.find(criteria))

# 更新文档
def update_user(user_id, updates):
    from bson.objectid import ObjectId
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updates}
    )
    return result.modified_count

# 删除文档
def delete_user(user_id):
    from bson.objectid import ObjectId
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count

# 使用示例
user_id = add_user({
    "username": "johndoe",
    "email": "john@example.com",
    "profile": {
        "age": 30,
        "interests": ["programming", "music"]
    }
})
print(f"新增用户ID: {user_id}")
print(f"用户信息: {get_user(user_id)}")
update_user(user_id, {"email": "john.doe@example.com", "profile.age": 31})
print(f"更新后: {get_user(user_id)}")
print(f"编程爱好者: {get_users_by_criteria({'profile.interests': 'programming'})}")
delete_user(user_id)
print(f"MongoDB文档数: {users_collection.count_documents({})}")
```

#### ORM (对象关系映射)

ORM允许开发者使用面向对象的方式操作数据库，隐藏SQL细节。

**使用SQLAlchemy**:
```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# 创建引擎和基类
engine = create_engine('sqlite:///example.db', echo=True)
Base = declarative_base()

# 定义模型
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    author = relationship("User", back_populates="posts")
    
    def __repr__(self):
        return f"<Post(title='{self.title}')>"

# 创建表
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

# 增加用户和文章
def add_user_with_posts():
    user = User(username="johndoe", email="john@example.com")
    post1 = Post(title="First Post", content="Hello World!", author=user)
    post2 = Post(title="Second Post", content="More content", author=user)
    
    session.add(user)
    session.commit()
    return user.id

# 查询
def query_examples(user_id):
    # 获取单个用户
    user = session.query(User).filter_by(id=user_id).first()
    print(f"用户: {user}")
    
    # 用户的所有文章
    posts = session.query(Post).filter_by(user_id=user_id).all()
    print(f"文章数: {len(posts)}")
    
    # 连接查询
    user_posts = session.query(User, Post).join(Post).filter(User.id == user_id).all()
    for user, post in user_posts:
        print(f"{user.username} 写了 '{post.title}'")
    
    # 复杂过滤
    recent_posts = session.query(Post).filter(
        Post.user_id == user_id,
        Post.title.like('%Post%')
    ).order_by(Post.created_at.desc()).all()
    
    return recent_posts

# 更新
def update_example(user_id):
    user = session.query(User).get(user_id)
    if user:
        user.email = "new.email@example.com"
        session.commit()
        return True
    return False

# 删除
def delete_example(user_id):
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)  # 级联删除所有文章
        session.commit()
        return True
    return False

# 使用示例
user_id = add_user_with_posts()
print(f"添加了用户ID: {user_id}")
recent_posts = query_examples(user_id)
print(f"最近文章: {recent_posts}")
print(f"更新用户: {update_example(user_id)}")
print(f"删除用户: {delete_example(user_id)}")

# 关闭会话
session.close()
```

**使用Django ORM**:
```python
# 注意：这需要在Django项目中运行
# 在models.py中定义模型

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# 在视图或其他地方使用模型
# views.py 或 shell 中

# 创建
def create_example():
    user = User.objects.create(username="johndoe", email="john@example.com")
    Post.objects.create(title="First Post", content="Hello World!", author=user)
    Post.objects.create(title="Second Post", content="More content", author=user)
    return user.id

# 查询
def query_examples(user_id):
    # 获取单个用户
    user = User.objects.get(id=user_id)
    print(f"用户: {user}")
    
    # 获取用户的所有文章
    posts = user.posts.all()
    print(f"文章数: {posts.count()}")
    
    # 过滤查询
    posts_with_filter = Post.objects.filter(
        author_id=user_id,
        title__contains="Post"
    ).order_by('-created_at')
    
    # 聚合查询
    from django.db.models import Count, Avg
    post_stats = User.objects.annotate(
        post_count=Count('posts')
    ).values('username', 'post_count')
    
    return posts_with_filter

# 更新
def update_example(user_id):
    # 方式1：获取后更新
    user = User.objects.get(id=user_id)
    user.email = "new.email@example.com"
    user.save()
    
    # 方式2：直接更新
    User.objects.filter(id=user_id).update(email="another.email@example.com")
    
    return User.objects.get(id=user_id)

# 删除
def delete_example(user_id):
    # 方式1：获取后删除
    user = User.objects.get(id=user_id)
    user.delete()  # 级联删除所有文章
    
    # 方式2：直接删除
    # User.objects.filter(id=user_id).delete()
    
    return User.objects.filter(id=user_id).exists()
```

### 14.2 数据库索引

索引是提高数据库查询性能的重要工具，但也有相应的开销。

**索引基础**:
```python
# SQLite创建索引
import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 创建索引
cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_category ON products (category)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_price ON products (price)')
cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_products_name ON products (name)')

# 检查索引
cursor.execute("PRAGMA index_list(products)")
indexes = cursor.fetchall()
print("表的索引列表:", indexes)

for index in indexes:
    index_name = index[1]
    cursor.execute(f"PRAGMA index_info({index_name})")
    print(f"索引 {index_name} 的列:", cursor.fetchall())

conn.close()
```

**索引的优缺点**:
- 优点:
  - 加快查询速度
  - 唯一索引可强制数据唯一性
  - 可以优化排序和分组操作
- 缺点:
  - 占用额外存储空间
  - 减慢写操作(INSERT, UPDATE, DELETE)
  - 需要维护成本

**索引选择和优化**:
- 频繁查询的列应考虑建立索引
- 唯一性高的列作为索引效果更好
- 避免过多索引，权衡查询和写入性能
- 复合索引的列顺序很重要
- 定期分析和优化索引

### 14.3 数据库事务和ACID

数据库事务是一组作为单一逻辑工作单元执行的操作序列。

**ACID属性**:
- **原子性(Atomicity)**: 事务中的所有操作要么全部完成，要么全部不完成
- **一致性(Consistency)**: 事务将数据库从一个一致状态转变为另一个一致状态
- **隔离性(Isolation)**: 并发事务的执行相互隔离
- **持久性(Durability)**: 一旦事务提交，其结果将永久保存

**Python中的事务示例**:
```python
import sqlite3

conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# 创建账户表
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    balance REAL NOT NULL CHECK (balance >= 0)
)
''')

# 初始化一些账户
accounts = [
    (1, "Alice", 1000.0),
    (2, "Bob", 500.0)
]

cursor.executemany(
    "INSERT OR REPLACE INTO accounts VALUES (?, ?, ?)",
    accounts
)
conn.commit()

def transfer_money(from_id, to_id, amount):
    # 开始事务
    try:
        # 检查余额
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,))
        from_balance = cursor.fetchone()[0]
        
        if from_balance < amount:
            raise ValueError("余额不足")
        
        # 更新转出账户
        cursor.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, from_id)
        )
        
        # 可以在这里添加模拟错误来测试回滚
        # if True: raise Exception("模拟转账失败")
        
        # 更新转入账户
        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, to_id)
        )
        
        # 提交事务
        conn.commit()
        print("转账成功")
        return True
    except Exception as e:
        # 回滚事务
        conn.rollback()
        print(f"转账失败: {e}")
        return False

# 执行转账
print("转账前:")
cursor.execute("SELECT * FROM accounts")
print(cursor.fetchall())

transfer_money(1, 2, 200.0)

print("转账后:")
cursor.execute("SELECT * FROM accounts")
print(cursor.fetchall())

conn.close()
```

**事务隔离级别**:
- **读未提交(Read Uncommitted)**: 可能出现脏读
- **读已提交(Read Committed)**: 防止脏读，但可能出现不可重复读
- **可重复读(Repeatable Read)**: 防止脏读和不可重复读，但可能出现幻读
- **串行化(Serializable)**: 最高级别，防止所有并发问题，但性能最低

### 14.4 数据库优化技巧

**查询优化**:
```python
# 1. 使用EXPLAIN分析查询
import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# SQLite使用EXPLAIN QUERY PLAN
cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'john@example.com'")
explain_result = cursor.fetchall()
print("查询计划:", explain_result)

# 2. 避免SELECT *，只选择需要的列
def good_query():
    cursor.execute("SELECT id, username FROM users WHERE active = 1")
    return cursor.fetchall()

# 3. 使用参数化查询避免SQL注入并提高性能
def search_users(email):
    # 好的做法:
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    # 而不是:
    # cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
    return cursor.fetchall()

# 4. 批量操作提高效率
def bulk_insert(users):
    cursor.executemany(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        users  # 一个包含多个(username, email)元组的列表
    )
    conn.commit()

conn.close()
```

**数据库连接池**:
```python
import sqlite3
from contextlib import contextmanager
import queue
import threading

class ConnectionPool:
    def __init__(self, db_path, max_connections=5):
        self.db_path = db_path
        self.max_connections = max_connections
        self.connections = queue.Queue(maxsize=max_connections)
        self.created_connections = 0
        self.lock = threading.Lock()
    
    def _create_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 使结果可通过列名访问
        return conn
    
    def get_connection(self):
        try:
            # 尝试从池中获取连接
            return self.connections.get(block=False)
        except queue.Empty:
            # 池为空，创建新连接
            with self.lock:
                if self.created_connections < self.max_connections:
                    self.created_connections += 1
                    return self._create_connection()
                else:
                    # 已达到最大连接数，等待
                    return self.connections.get()
    
    def release_connection(self, conn):
        self.connections.put(conn)
    
    @contextmanager
    def connection(self):
        conn = self.get_connection()
        try:
            yield conn
        finally:
            self.release_connection(conn)
    
    def close_all(self):
        while not self.connections.empty():
            conn = self.connections.get()
            conn.close()

# 使用连接池
pool = ConnectionPool('example.db')

def user_exists(username):
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return cursor.fetchone() is not None

def add_user(username, email):
    with pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email)
        )
        conn.commit()
        return cursor.lastrowid

# 多线程测试
def worker(worker_id):
    print(f"Worker {worker_id} 开始工作")
    for i in range(3):
        username = f"user_{worker_id}_{i}"
        email = f"{username}@example.com"
        user_id = add_user(username, email)
        print(f"Worker {worker_id} 添加用户: {username} (ID: {user_id})")
    print(f"Worker {worker_id} 完成工作")

threads = []
for i in range(10):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

pool.close_all()
```

**最佳实践**:
1. 正确使用索引
2. 定期VACUUM和分析数据库
3. 使用合适的数据类型
4. 限制结果集大小(LIMIT)
5. 使用连接池管理连接
6. 避免在循环中执行查询
7. 合理规划数据库模式

### 14.5 常见面试问题

1. **关系型数据库和非关系型数据库有什么区别？各自适用于什么场景？**
   - 关系型数据库使用表和行，有固定模式，支持ACID；适合需要数据一致性的场景。
   - 非关系型数据库灵活多样，无固定模式；适合大数据量、高吞吐量或频繁模式变化的场景。

2. **什么是数据库事务？ACID属性是什么？**
   - 事务是一组作为单一逻辑单元执行的操作
   - A(原子性)、C(一致性)、I(隔离性)、D(持久性)

3. **如何优化SQL查询性能？**
   - 使用适当的索引
   - 只查询需要的列而非SELECT *
   - 限制结果集大小
   - 避免JOIN过多表
   - 参数化查询

4. **解释数据库规范化，并提供一个示例。**
   - 规范化是消除冗余和提高数据完整性的过程
   - 例如将用户地址信息拆分到单独的表中

5. **简述Python中几种常见的ORM工具及其特点。**
   - SQLAlchemy：功能全面，支持多种数据库，API灵活
   - Django ORM：与Django框架集成，易于使用
   - Peewee：轻量级ORM，简单易学
   - SQLObject：老牌ORM，对象关系映射简单明了

6. **什么是SQL注入？如何在Python中防止SQL注入？**
   - SQL注入是通过输入恶意SQL代码攻击数据库的方法
   - 使用参数化查询和预处理语句防止注入
   - 使用ORM工具自动处理参数化

7. **解释数据库连接池及其优点。**
   - 连接池管理和重用数据库连接
   - 减少连接建立的开销，提高性能
   - 控制并发连接数量，防止资源耗尽

8. **NoSQL数据库中的CAP定理是什么？**
   - 一致性(Consistency)：所有节点同时看到相同数据
   - 可用性(Availability)：每个请求都能收到响应
   - 分区容错性(Partition Tolerance)：即使网络分区，系统仍能运行
   - 理论上分布式系统只能同时满足三者中的两个

## 15. 网络编程

### 15.1 Socket编程

Socket是网络编程的基础，提供了在网络上进行通信的端点。Python的`socket`模块提供了对底层网络接口的访问。

**TCP服务器端**：
```python
import socket

def start_tcp_server(host='localhost', port=9999):
    # 创建socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 绑定地址和端口
    server_socket.bind((host, port))
    
    # 开始监听，参数表示最大连接数
    server_socket.listen(5)
    print(f"服务器启动，监听 {host}:{port}")
    
    try:
        while True:
            # 等待客户端连接
            client_socket, client_address = server_socket.accept()
            print(f"接受来自 {client_address} 的连接")
            
            try:
                # 接收数据
                data = client_socket.recv(1024)
                if data:
                    print(f"收到数据: {data.decode('utf-8')}")
                    # 发送响应
                    client_socket.send("数据已接收".encode('utf-8'))
            finally:
                # 关闭客户端连接
                client_socket.close()
    finally:
        # 关闭服务器socket
        server_socket.close()
```

**TCP客户端**：
```python
import socket

def tcp_client(host='localhost', port=9999, message="Hello, Server!"):
    # 创建socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 连接服务器
        client_socket.connect((host, port))
        print(f"已连接到 {host}:{port}")
        
        # 发送数据
        client_socket.send(message.encode('utf-8'))
        print(f"已发送: {message}")
        
        # 接收响应
        response = client_socket.recv(1024)
        print(f"接收到响应: {response.decode('utf-8')}")
    finally:
        # 关闭连接
        client_socket.close()
```

**UDP服务器端**：
```python
import socket

def start_udp_server(host='localhost', port=9999):
    # 创建UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 绑定地址和端口
    server_socket.bind((host, port))
    print(f"UDP服务器启动，监听 {host}:{port}")
    
    try:
        while True:
            # 接收数据和客户端地址
            data, client_address = server_socket.recvfrom(1024)
            print(f"收到来自 {client_address} 的数据: {data.decode('utf-8')}")
            
            # 发送响应
            server_socket.sendto("UDP数据已接收".encode('utf-8'), client_address)
    finally:
        server_socket.close()
```

**UDP客户端**：
```python
import socket

def udp_client(host='localhost', port=9999, message="Hello, UDP Server!"):
    # 创建UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # 发送数据
        client_socket.sendto(message.encode('utf-8'), (host, port))
        print(f"已发送: {message}")
        
        # 接收响应
        response, server_address = client_socket.recvfrom(1024)
        print(f"接收到来自 {server_address} 的响应: {response.decode('utf-8')}")
    finally:
        client_socket.close()
```

**使用非阻塞Socket**：
```python
import socket
import select

def non_blocking_server(host='localhost', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    # 设置为非阻塞模式
    server_socket.setblocking(False)
    
    # 要监听的socket列表
    inputs = [server_socket]
    outputs = []
    
    try:
        while inputs:
            # select监控多个socket，返回准备好的socket列表
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            
            for sock in readable:
                if sock is server_socket:
                    # 新的客户端连接
                    client_socket, client_address = sock.accept()
                    print(f"新连接: {client_address}")
                    client_socket.setblocking(False)
                    inputs.append(client_socket)
                else:
                    # 客户端发送数据
                    try:
                        data = sock.recv(1024)
                        if data:
                            print(f"收到数据: {data.decode('utf-8')}")
                            sock.send("数据已处理".encode('utf-8'))
                        else:
                            # 连接关闭
                            print(f"连接关闭")
                            inputs.remove(sock)
                            sock.close()
                    except ConnectionError:
                        inputs.remove(sock)
                        sock.close()
            
            for sock in exceptional:
                # 处理异常
                inputs.remove(sock)
                if sock in outputs:
                    outputs.remove(sock)
                sock.close()
    finally:
        server_socket.close()
```

### 15.2 HTTP编程

HTTP是应用层协议，用于Web浏览器和Web服务器之间的通信。Python提供了多种处理HTTP的库。

**使用requests库**：
```python
import requests

# 发送GET请求
def http_get_example():
    response = requests.get("https://api.github.com/users/python")
    
    # 检查状态码
    print(f"状态码: {response.status_code}")
    
    # 获取响应内容
    if response.status_code == 200:
        data = response.json()  # JSON解析
        print(f"用户名: {data.get('login')}")
        print(f"ID: {data.get('id')}")
    
    # 请求头部
    print(f"Content-Type: {response.headers.get('content-type')}")
    
    # 响应时间
    print(f"响应时间: {response.elapsed.total_seconds()}秒")

# 发送POST请求
def http_post_example():
    # POST表单数据
    data = {
        "name": "John Doe",
        "email": "john@example.com"
    }
    response = requests.post("https://httpbin.org/post", data=data)
    
    # POST JSON数据
    json_data = {
        "user": {
            "name": "John Doe",
            "email": "john@example.com"
        }
    }
    response_json = requests.post("https://httpbin.org/post", json=json_data)
    
    # 检查响应
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"响应: {response.json()}")

# 使用会话保持cookie
def session_example():
    # 创建会话对象
    session = requests.Session()
    
    # 设置会话级别的请求头
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    })
    
    # 发送请求
    response = session.get("https://httpbin.org/cookies/set/sessionid/123456")
    print(f"Cookies: {session.cookies}")
    
    # 使用同一会话发送另一请求
    response = session.get("https://httpbin.org/cookies")
    print(f"响应: {response.json()}")
    
    # 关闭会话
    session.close()

# 错误处理
def error_handling_example():
    try:
        response = requests.get("https://non-existent-url.org", timeout=3)
        response.raise_for_status()  # 抛出HTTP错误异常
    except requests.exceptions.Timeout:
        print("请求超时")
    except requests.exceptions.ConnectionError:
        print("连接错误")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
```

**使用http.server模块**：
```python
import http.server
import socketserver
import json

# 自定义HTTP处理器
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/info':
            # 返回JSON数据
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            data = {
                "status": "success",
                "message": "Hello from Python HTTP Server",
                "time": str(datetime.datetime.now())
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            # 默认行为：提供静态文件
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/echo':
            # 读取请求体长度
            content_length = int(self.headers['Content-Length'])
            
            # 读取请求体
            post_data = self.rfile.read(content_length)
            
            # 返回响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "success",
                "received": post_data.decode('utf-8')
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

# 启动HTTP服务器
def start_http_server(port=8000):
    handler = CustomHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"HTTP服务器启动于端口 {port}")
        httpd.serve_forever()
```

**使用aiohttp进行异步HTTP**：
```python
import aiohttp
import asyncio

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            return f"Error: {response.status}"

async def fetch_multiple_urls(urls):
    tasks = [fetch_url(url) for url in urls]
    return await asyncio.gather(*tasks)

async def async_http_example():
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent"
    ]
    
    results = await fetch_multiple_urls(urls)
    for url, result in zip(urls, results):
        print(f"URL: {url}")
        print(f"Result (first 100 chars): {result[:100]}...")
        print()

# 运行异步示例
# asyncio.run(async_http_example())
```

### 15.3 Web框架基础

**Flask框架简介**：
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Flask API"

@app.route('/api/hello')
def hello():
    name = request.args.get('name', 'World')
    return jsonify({"message": f"Hello, {name}!"})

@app.route('/api/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    
    user_data = request.get_json()
    
    # 这里应该有数据库存储逻辑
    # 简化示例仅返回接收的数据
    return jsonify({
        "status": "success",
        "user": user_data
    }), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # 模拟用户查询
    if user_id == 1:
        return jsonify({
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com"
        })
    return jsonify({"error": "User not found"}), 404

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "The requested resource was not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

# 启动服务器
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Django REST框架概述**：
```python
# models.py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# serializers.py
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at']

# views.py
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

**FastAPI示例**：
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Task API")

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class Task(TaskCreate):
    id: int
    completed: bool = False

# 模拟数据库
tasks_db = {}
task_counter = 0

@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    global task_counter
    task_counter += 1
    
    task_dict = task.dict()
    task_dict["id"] = task_counter
    task_dict["completed"] = False
    
    tasks_db[task_counter] = task_dict
    return task_dict

@app.get("/tasks/", response_model=List[Task])
def read_tasks(skip: int = 0, limit: int = 10):
    return list(tasks_db.values())[skip:skip+limit]

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_dict = task.dict()
    task_dict["id"] = task_id
    task_dict["completed"] = tasks_db[task_id]["completed"]
    
    tasks_db[task_id] = task_dict
    return task_dict

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks_db[task_id]
    return None

# 启动服务器
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 15.4 网络编程实践

**TCP聊天服务器**：
```python
import socket
import threading
import select

class ChatServer:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}  # 客户端socket和名称映射
        self.lock = threading.Lock()
    
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"聊天服务器启动于 {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"新连接: {address}")
                
                # 为新客户端创建线程
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("服务器关闭")
        finally:
            self.server_socket.close()
    
    def handle_client(self, client_socket, address):
        # 获取客户端名称
        client_socket.send("请输入你的名字: ".encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8').strip()
        
        with self.lock:
            self.clients[client_socket] = name
        
        # 广播新用户加入
        self.broadcast(f"{name} 加入了聊天室!", client_socket)
        
        try:
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break
                
                full_message = f"{name}: {message.decode('utf-8')}"
                self.broadcast(full_message, client_socket)
        except:
            pass  # 处理连接错误
        finally:
            # 客户端断开连接
            with self.lock:
                if client_socket in self.clients:
                    name = self.clients[client_socket]
                    del self.clients[client_socket]
            
            client_socket.close()
            self.broadcast(f"{name} 离开了聊天室", None)
    
    def broadcast(self, message, sender_socket):
        with self.lock:
            for client_socket in list(self.clients.keys()):
                if client_socket != sender_socket:
                    try:
                        client_socket.send(message.encode('utf-8'))
                    except:
                        # 如果发送失败，移除客户端
                        client_socket.close()
                        del self.clients[client_socket]

# 启动聊天服务器
# chat_server = ChatServer()
# chat_server.start()
```

**TCP聊天客户端**：
```python
import socket
import threading
import sys

class ChatClient:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
    
    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.running = True
            
            # 启动消息接收线程
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            return True
        except Exception as e:
            print(f"连接错误: {e}")
            return False
    
    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024)
                if not message:
                    break
                print(message.decode('utf-8'))
            except:
                break
        
        self.running = False
        print("与服务器的连接已关闭")
    
    def send_message(self, message):
        try:
            self.client_socket.send(message.encode('utf-8'))
            return True
        except:
            self.running = False
            return False
    
    def close(self):
        self.running = False
        self.client_socket.close()

# 使用聊天客户端
def run_chat_client():
    client = ChatClient()
    
    if not client.connect():
        return
    
    try:
        while client.running:
            message = input()
            if message.lower() == 'exit':
                break
            
            if not client.send_message(message):
                print("发送失败，连接已断开")
                break
    except KeyboardInterrupt:
        pass
    finally:
        client.close()

# 运行客户端
# run_chat_client()
```

**简单爬虫**：
```python
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin, urlparse

class WebCrawler:
    def __init__(self, start_url, max_pages=10, delay=1):
        self.start_url = start_url
        self.max_pages = max_pages
        self.delay = delay
        self.visited_urls = set()
        self.queue = [start_url]
        
        # 提取域名，仅爬取同一域名下的页面
        parsed_url = urlparse(start_url)
        self.domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    def crawl(self):
        count = 0
        
        while self.queue and count < self.max_pages:
            # 从队列获取URL
            url = self.queue.pop(0)
            
            # 已访问过则跳过
            if url in self.visited_urls:
                continue
            
            print(f"正在爬取: {url}")
            
            try:
                # 添加随机延迟以避免过快请求
                time.sleep(self.delay * (0.5 + random.random()))
                
                # 发送请求
                response = requests.get(
                    url, 
                    headers={
                        "User-Agent": "Mozilla/5.0 (compatible; MyCrawler/1.0)"
                    }
                )
                
                if response.status_code == 200:
                    # 标记为已访问
                    self.visited_urls.add(url)
                    count += 1
                    
                    # 解析页面
                    self.parse_page(url, response.text)
                else:
                    print(f"无法访问页面，状态码: {response.status_code}")
            
            except Exception as e:
                print(f"爬取错误: {e}")
        
        print(f"爬取完成，共访问 {len(self.visited_urls)} 个URL")
    
    def parse_page(self, base_url, html_content):
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取标题
        title = soup.title.string if soup.title else "无标题"
        print(f"页面标题: {title}")
        
        # 提取链接并添加到队列
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # 仅考虑同一域名下的页面且不包含锚点
            if full_url.startswith(self.domain) and '#' not in full_url:
                if full_url not in self.visited_urls and full_url not in self.queue:
                    self.queue.append(full_url)
        
        # 这里可以根据需要添加数据提取逻辑
        # 例如提取文章内容、图片URL等

# 使用爬虫示例
# crawler = WebCrawler("https://example.com", max_pages=5, delay=2)
# crawler.crawl()
```

### 15.5 常见网络编程面试题

1. **什么是Socket？在Python中如何创建TCP和UDP Socket？**
   - Socket是网络通信的端点，提供了网络层之上的抽象
   - TCP Socket: `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
   - UDP Socket: `socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`

2. **TCP和UDP的区别是什么？**
   - TCP是面向连接的可靠协议，有流量控制和拥塞控制
   - UDP是无连接的不可靠协议，速度更快但不保证数据送达
   - TCP适合要求可靠性的场景，UDP适合实时性要求高的场景

3. **在Python中如何实现多客户端的服务器？**
   - 使用多线程：为每个客户端创建一个处理线程
   - 使用select/poll/epoll：非阻塞I/O复用
   - 使用异步I/O库如asyncio

4. **解释HTTP的请求-响应模型及其在Python中的实现方式。**
   - HTTP是无状态的请求-响应协议
   - 客户端发送请求（方法、URL、头部、体），服务器返回响应（状态码、头部、体）
   - Python实现：requests库（客户端）、http.server模块（服务器）、Flask/Django（框架）

5. **什么是RESTful API？如何在Python中实现？**
   - REST是一种架构风格，使用HTTP方法表示操作
   - GET（读取）、POST（创建）、PUT（更新）、DELETE（删除）
   - Python实现：Flask、Django REST Framework、FastAPI

6. **描述WebSocket与HTTP的区别，以及它在Python中的实现。**
   - HTTP是无状态的短连接，WebSocket是持久的全双工连接
   - WebSocket适合实时通信如聊天、游戏、实时更新
   - Python实现：websockets库、Socket.IO

7. **如何在Python中处理网络请求超时和重试？**
   - 设置超时：`requests.get(url, timeout=5)`
   - 实现重试机制：使用循环和异常处理或使用第三方库如tenacity

8. **什么是异步网络编程？为什么它在Python中很重要？**
   - 异步编程允许在等待I/O操作时执行其他代码，提高并发性
   - Python的GIL限制了线程并发，异步I/O是提高I/O密集型应用性能的好方法
   - 使用asyncio、aiohttp等库实现   

9. **如何使用Python爬取网页并解析内容？**
   - 发送请求：requests库
   - 解析HTML：BeautifulSoup或lxml
   - 提取数据：CSS选择器或XPath
   - 处理动态内容：Selenium或Playwright

10. **如何处理网络编程中的安全问题？**
    - 输入验证：防止SQL注入和XSS
    - 使用HTTPS：确保传输安全
    - 实施速率限制：防止DoS攻击
    - 正确处理敏感数据：不明文存储密码

## 16. 测试

### 16.1 测试类型
- 单元测试
- 集成测试
- 功能测试
- 性能测试

### 16.2 测试框架
- unittest
- pytest
- nose


## 17. 部署和运维

### 17.1 部署方式

#### 传统部署

传统部署是指将Python应用程序直接部署到物理服务器或虚拟机上。

**使用Gunicorn和Nginx部署Flask应用**：

```python
# 安装依赖
# pip install gunicorn

# app.py - Flask应用
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run()

# wsgi.py - WSGI入口点
from app import app

if __name__ == "__main__":
    app.run()
```

**启动命令**：
```bash
# 启动Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

**Nginx配置**：
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**使用Supervisor管理进程**：
```ini
[program:myapp]
command=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
directory=/path/to/app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/myapp/error.log
stdout_logfile=/var/log/myapp/access.log
```

#### Docker容器

Docker容器可以打包应用程序及其依赖，确保在不同环境中一致运行。

**Dockerfile示例**：
```dockerfile
# 使用官方Python镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 运行应用
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

**构建和运行**：
```bash
# 构建镜像
docker build -t myapp:latest .

# 运行容器
docker run -d -p 5000:5000 --name myapp myapp:latest
```

**Docker Compose配置**：
```yaml
version: '3'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=production
    depends_on:
      - db
  
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=myapp
      - POSTGRES_PASSWORD=mypassword
      - POSTGRES_DB=myapp

volumes:
  postgres_data:
```

#### Kubernetes

Kubernetes是一个容器编排平台，可以自动化容器的部署、扩展和管理。

**部署配置示例(deployment.yaml)**：
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "100m"
            memory: "256Mi"
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
```

**服务配置(service.yaml)**：
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

**水平自动缩放(hpa.yaml)**：
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 17.2 监控和日志

#### Prometheus 监控

Prometheus是一个开源监控和告警系统，适用于容器化环境。

**Python应用集成Prometheus**：
```python
from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# 定义指标
REQUEST_COUNT = Counter('app_requests_total', 'Total request count of the app')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency in seconds')

@app.route('/')
@REQUEST_LATENCY.time()  # 自动记录请求耗时
def hello():
    REQUEST_COUNT.inc()  # 增加请求计数
    return "Hello, World!"

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
```

**Prometheus配置**：
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'myapp'
    scrape_interval: 5s
    static_configs:
      - targets: ['myapp:5000']
```

#### Grafana 可视化

Grafana是一个开源可视化和分析平台，可以连接到Prometheus等数据源。

**配置Grafana数据源**：
1. 添加Prometheus数据源
2. URL: http://prometheus:9090
3. 访问: Server (默认)

**创建仪表板示例查询**：
- 请求总数: `sum(app_requests_total)`
- 每秒请求数: `rate(app_requests_total[5m])`
- 请求延迟: `histogram_quantile(0.95, sum(rate(app_request_latency_seconds_bucket[5m])) by (le))`

#### ELK Stack

ELK Stack是Elasticsearch、Logstash和Kibana的组合，用于日志收集、存储和可视化。

**Python应用集成日志记录**：
```python
import logging
from flask import Flask
import json

app = Flask(__name__)

# 配置日志
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '{"timestamp":"%(asctime)s", "level":"%(levelname)s", "message":"%(message)s"}'
))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def hello():
    app.logger.info("访问了首页", extra={
        "user_agent": request.headers.get("User-Agent"),
        "ip": request.remote_addr
    })
    return "Hello, World!"
```

**Logstash配置**：
```
input {
  beats {
    port => 5044
  }
}

filter {
  json {
    source => "message"
  }
  
  date {
    match => [ "timestamp", "ISO8601" ]
    target => "@timestamp"
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "app-logs-%{+YYYY.MM.dd}"
  }
}
```

**Filebeat配置**：
```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/myapp/*.log
  json.keys_under_root: true
  json.add_error_key: true

output.logstash:
  hosts: ["logstash:5044"]
```

### 17.3 CI/CD 自动化部署

#### GitHub Actions

GitHub Actions可用于自动化构建、测试和部署Python应用。

**示例工作流配置(.github/workflows/deploy.yml)**：
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install pytest pytest-cov
    - name: Test with pytest
      run: |
        pytest --cov=./ --cov-report=xml
    - name: Upload coverage report
      uses: codecov/codecov-action@v1
  
  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t myapp:latest .
    
    - name: Login to Docker Hub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKER_HUB_USERNAME }}
        password: ${{ secrets.DOCKER_HUB_TOKEN }}
    
    - name: Push Docker image
      run: |
        docker tag myapp:latest username/myapp:latest
        docker push username/myapp:latest
    
    - name: Deploy to production
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /path/to/app
          docker-compose pull
          docker-compose up -d
```

#### Jenkins

Jenkins是一个开源自动化服务器，可用于构建、测试和部署代码。

**Jenkinsfile示例**：
```groovy
pipeline {
    agent {
        docker {
            image 'python:3.9'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest'
            }
            post {
                always {
                    junit 'test-reports/*.xml'
                }
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker build -t myapp:latest .'
                sh 'docker push myrepo/myapp:latest'
                
                sshagent(['deploy-key']) {
                    sh '''
                        ssh user@server "cd /path/to/app && docker-compose pull && docker-compose up -d"
                    '''
                }
            }
        }
    }
    post {
        failure {
            mail to: 'team@example.com',
                 subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
                 body: "Something is wrong with ${env.BUILD_URL}"
        }
    }
}
```

### 17.4 常见部署和运维问题

1. **如何确保Python应用在生产环境中的安全性？**
   - 使用HTTPS加密传输
   - 定期更新依赖包解决安全漏洞
   - 使用环境变量存储敏感信息
   - 实施适当的防火墙和网络策略

2. **如何优化Python Web应用的性能？**
   - 使用异步框架（如FastAPI、Quart）
   - 实施缓存策略（Redis、Memcached）
   - 优化数据库查询
   - 使用适当的工作进程数（通常是CPU核心数×2+1）

3. **Docker与虚拟机相比有什么优势？**
   - 资源效率更高（共享主机内核）
   - 启动速度更快
   - 可移植性更好
   - 版本控制和可重现性更强

4. **如何管理Python应用的配置？**
   - 使用环境变量
   - 使用配置文件（如YAML、JSON）
   - 使用专门的配置管理工具（如python-decouple）
   - 区分不同环境的配置

5. **如何进行零停机部署？**
   - 蓝绿部署：准备新版本，切换流量
   - 滚动更新：逐步替换实例
   - 使用负载均衡实现无缝切换
   - Kubernetes中使用滚动更新策略

6. **如何监控Python应用的健康状况？**
   - 实现健康检查端点
   - 监控关键指标（CPU、内存、响应时间）
   - 设置告警阈值
   - 使用APM工具（如New Relic、Datadog）

7. **容器编排工具（如Kubernetes）的主要优势是什么？**
   - 自动扩展和负载均衡
   - 自我修复能力
   - 滚动更新和回滚
   - 服务发现和配置管理

8. **如何处理Python应用的日志？**
   - 集中式日志收集（ELK Stack）
   - 结构化日志（JSON格式）
   - 日志轮转防止磁盘填满
   - 添加上下文信息（如请求ID）

9. **如何进行数据库迁移？**
   - 使用迁移工具（如Alembic、Django Migrations）
   - 制定回滚策略
   - 先在测试环境验证
   - 考虑停机时间和数据一致性

10. **如何确保应用的高可用性？**
    - 多实例部署
    - 负载均衡
    - 跨区域部署
    - 健康检查和自动恢复

## 18. 安全

### 18.1 常见安全问题

#### SQL注入

SQL注入是通过在用户提供的输入中插入恶意SQL代码，使应用程序执行非预期的SQL命令。

**易受攻击的代码**：
```python
# 危险的实现 - 易受SQL注入攻击
def get_user(username):
    cursor = db.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

# 如果username = "admin' OR '1'='1", 查询变为:
# SELECT * FROM users WHERE username = 'admin' OR '1'='1'
# 这将返回所有用户记录
```

**安全实现**：
```python
# 使用参数化查询
def get_user_safe(username):
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    return cursor.fetchone()

# 使用ORM (如SQLAlchemy)
from sqlalchemy import select
from sqlalchemy.orm import Session

def get_user_orm(username, session: Session):
    return session.query(User).filter(User.username == username).first()
```

#### XSS攻击

跨站脚本(XSS)攻击是将恶意JavaScript代码注入到网页中，当其他用户查看页面时执行。

**易受攻击的代码**：
```python
# Flask应用，未对用户输入进行转义
@app.route('/profile')
def profile():
    username = request.args.get('username', '')
    return f'<h1>欢迎, {username}!</h1>'

# 如果username = "<script>alert('XSS')</script>"
# 输出: <h1>欢迎, <script>alert('XSS')</script>!</h1>
# 脚本将在浏览器中执行
```

**安全实现**：
```python
from flask import escape

@app.route('/profile')
def profile_safe():
    username = request.args.get('username', '')
    return f'<h1>欢迎, {escape(username)}!</h1>'

# 使用模板引擎(Jinja2)自动转义
@app.route('/profile_template')
def profile_template():
    username = request.args.get('username', '')
    return render_template('profile.html', username=username)

# 在profile.html中:
# <h1>欢迎, {{ username }}!</h1>  <!-- Jinja2默认进行HTML转义 -->
```

#### CSRF攻击

跨站请求伪造(CSRF)攻击诱导用户执行非意愿的操作，利用用户已认证的会话。

**防护措施**：
```python
# Flask应用中使用CSRF保护
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard-to-guess-key'
csrf = CSRFProtect(app)

@app.route('/change_password', methods=['POST'])
def change_password():
    # 已受到CSRF保护
    new_password = request.form.get('new_password')
    # 更新密码...
    return redirect(url_for('profile'))

# 在HTML表单中:
'''
<form method="post" action="/change_password">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <input type="password" name="new_password">
    <button type="submit">更改密码</button>
</form>
'''
```

#### 文件上传漏洞

不安全的文件上传可能导致执行任意代码、服务器被滥用或敏感数据泄露。

**易受攻击的代码**：
```python
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join('uploads', filename))
    return f'文件 {filename} 上传成功!'

# 攻击者可能上传恶意PHP或Python文件，并尝试执行
```

**安全实现**：
```python
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file_safe():
    if 'file' not in request.files:
        return '没有文件部分', 400
    
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件', 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return f'文件 {filename} 上传成功!'
    
    return '不允许的文件类型', 400
```

### 18.2 安全措施

#### 输入验证

输入验证确保数据在进入应用程序前符合预期格式和约束。

```python
# 使用Pydantic进行数据验证
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    age: Optional[int] = None
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度至少为8个字符')
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not re.search(r'[0-9]', v):
            raise ValueError('密码必须包含至少一个数字')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('确认密码与密码不匹配')
        return v
    
    @validator('age')
    def age_valid(cls, v):
        if v is not None and (v < 18 or v > 120):
            raise ValueError('年龄必须在18到120之间')
        return v

# 使用示例
try:
    user = UserRegistration(
        username="john_doe",
        email="john@example.com",
        password="SecurePass123",
        confirm_password="SecurePass123",
        age=25
    )
    print("验证通过:", user.dict())
except ValueError as e:
    print("验证失败:", e)
```

#### 输出转义

输出转义防止数据被解释为代码或命令，从而预防XSS攻击。

```python
import html

def render_unsafe_content():
    user_content = "<script>alert('XSS')</script>"
    
    # 不安全的渲染
    unsafe_output = f"<div>{user_content}</div>"
    
    # 安全的渲染(HTML转义)
    safe_output = f"<div>{html.escape(user_content)}</div>"
    
    print("不安全:", unsafe_output)
    print("安全:", safe_output)

# 使用模板引擎的安全渲染(Jinja2)
from jinja2 import Template

def render_with_template():
    user_content = "<script>alert('XSS')</script>"
    
    template = Template("<div>{{ content }}</div>")
    output = template.render(content=user_content)
    
    print("模板渲染(自动转义):", output)
    
    # 有时需要显示原始HTML(受信任的内容)
    trusted_content = "<strong>安全HTML</strong>"
    template_raw = Template("<div>{{ content|safe }}</div>")
    output_raw = template_raw.render(content=trusted_content)
    
    print("模板渲染(原始HTML):", output_raw)
```

#### 密码加密

密码必须使用安全的哈希算法存储，而不是明文或弱加密。

```python
import hashlib
import os
import binascii
import bcrypt
from passlib.hash import pbkdf2_sha256

# 不安全的方法 - 永远不要使用!
def hash_password_unsafe(password):
    return hashlib.md5(password.encode()).hexdigest()

# 较好的方法 - 自定义盐值和SHA-256
def hash_password_better(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return binascii.hexlify(salt + key).decode()

def verify_password_better(stored_password, provided_password):
    binary = binascii.unhexlify(stored_password.encode())
    salt = binary[:32]
    stored_key = binary[32:]
    key = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return key == stored_key

# 推荐方法 - 使用bcrypt
def hash_password_bcrypt(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password_bcrypt(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password.encode())

# 推荐方法 - 使用passlib
def hash_password_passlib(password):
    return pbkdf2_sha256.hash(password)

def verify_password_passlib(stored_password, provided_password):
    return pbkdf2_sha256.verify(provided_password, stored_password)

# 示例使用
password = "SecurePassword123"

hashed_unsafe = hash_password_unsafe(password)
hashed_better = hash_password_better(password)
hashed_bcrypt = hash_password_bcrypt(password)
hashed_passlib = hash_password_passlib(password)

print(f"不安全哈希: {hashed_unsafe}")
print(f"改进哈希: {hashed_better}")
print(f"Bcrypt哈希: {hashed_bcrypt}")
print(f"Passlib哈希: {hashed_passlib}")

# 验证
print(f"验证bcrypt: {verify_password_bcrypt(hashed_bcrypt, password)}")
print(f"验证passlib: {verify_password_passlib(hashed_passlib, password)}")
```

#### 权限控制

权限控制限制用户对特定资源或操作的访问。

```python
# Flask应用中的基于角色的访问控制
from functools import wraps
from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 模拟用户数据库
users = {
    "admin": {"password": "admin_pass", "role": "admin"},
    "user1": {"password": "user1_pass", "role": "user"},
    "editor": {"password": "editor_pass", "role": "editor"}
}

# 角色所需权限
role_permissions = {
    "admin": ["read", "write", "delete", "admin"],
    "editor": ["read", "write"],
    "user": ["read"]
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            username = session.get('username')
            user_role = users.get(username, {}).get('role')
            
            if user_role and permission in role_permissions.get(user_role, []):
                return f(*args, **kwargs)
            else:
                return "权限不足", 403
        
        return decorated_function
    return decorator

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        
        return "登录失败"
    
    return "登录页面"

@app.route('/dashboard')
@login_required
def dashboard():
    return f"欢迎, {session.get('username')}!"

@app.route('/admin')
@permission_required('admin')
def admin_panel():
    return "管理员面板"

@app.route('/create')
@permission_required('write')
def create_content():
    return "创建内容页面"

@app.route('/view')
@permission_required('read')
def view_content():
    return "查看内容页面"
```

### 18.3 安全最佳实践

#### HTTPS和TLS

确保应用程序通过HTTPS安全传输数据。

```python
# 使用Flask启用HTTPS
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    # 在生产环境中，你可能会使用反向代理(如Nginx)来处理SSL
    app.run(ssl_context=('cert.pem', 'key.pem'))

# 强制重定向所有HTTP请求到HTTPS
@app.before_request
def force_https():
    if request.headers.get('X-Forwarded-Proto') == 'http':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
```

#### 安全Headers

设置适当的HTTP安全头部可以增强应用程序的安全性。

```python
# Flask应用中的安全头部
from flask import Flask

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    # 防止在frame中显示(防点击劫持)
    response.headers['X-Frame-Options'] = 'DENY'
    
    # 启用XSS保护
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # 防止MIME类型嗅探
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # 内容安全策略(CSP)
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    
    # 严格传输安全(HSTS)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # 引用策略
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    return response
```

#### 依赖安全

定期更新依赖项以解决已知漏洞。

```python
# 使用safety检查依赖漏洞
# pip install safety

import subprocess
import sys

def check_dependencies():
    print("检查依赖项安全...")
    result = subprocess.run(
        [sys.executable, "-m", "safety", "check", "--full-report"], 
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("所有依赖项安全!")
    else:
        print("发现安全问题:")
        print(result.stdout)
    
    return result.returncode

# 使用dependabot或renovate自动更新依赖
# GitHub配置文件: .github/dependabot.yml
'''
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
'''
```

### 18.4 常见安全问题

1. **如何防止SQL注入攻击？**
   - 使用参数化查询/预处理语句
   - 使用ORM框架
   - 避免直接拼接SQL字符串
   - 实施最小权限原则

2. **如何安全地存储用户密码？**
   - 使用强哈希算法(bcrypt, Argon2)
   - 添加随机盐值
   - 永不存储明文密码
   - 定期更新哈希算法

3. **如何防止跨站脚本(XSS)攻击？**
   - 转义用户输入
   - 使用内容安全策略(CSP)
   - 使用X-XSS-Protection头
   - 避免直接在JavaScript中使用用户输入

4. **什么是CSRF攻击，如何防止？**
   - 使用CSRF令牌
   - 检查Referer头
   - 使用SameSite Cookie
   - 使用POST请求进行状态更改

5. **如何处理敏感数据？**
   - 使用环境变量存储密钥
   - 实施适当的加密
   - 最小化数据收集和保留
   - 定期安全审计

6. **如何实施适当的会话管理？**
   - 使用安全Cookie属性(HttpOnly, Secure, SameSite)
   - 会话超时和轮换
   - 登录后重新生成会话ID
   - 在注销时销毁会话

7. **如何防止暴力破解攻击？**
   - 实施速率限制
   - 使用验证码
   - 实施账户锁定策略
   - 监控异常登录活动

8. **如何确保第三方库和依赖项的安全？**
   - 定期更新依赖项
   - 使用安全扫描工具(safety, snyk)
   - 审查重要依赖的源代码
   - 维护依赖清单

9. **如何保护API端点？**
   - 实施适当的认证(OAuth, JWT)
   - 使用API密钥或令牌
   - 实施速率限制
   - 验证所有输入参数

10. **如何处理文件上传安全？**
    - 验证文件类型和内容
    - 限制文件大小
    - 重命名上传的文件
    - 将上传内容存储在非可执行目录
```

## 19. 性能优化

### 19.1 代码优化

#### 算法优化

选择合适的算法对于提高程序性能至关重要。

**时间复杂度优化示例**：
```python
# 低效的查找算法 - O(n)
def find_element_linear(arr, target):
    for i, element in enumerate(arr):
        if element == target:
            return i
    return -1

# 高效的查找算法 - O(log n)，但要求数组已排序
def find_element_binary(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# 使用哈希表实现O(1)查找
def prepare_hash_lookup(arr):
    lookup = {}
    for i, element in enumerate(arr):
        lookup[element] = i
    return lookup

def find_element_hash(lookup, target):
    return lookup.get(target, -1)
```

**排序算法性能比较**：
```python
import time
import random

def measure_time(func, *args):
    start_time = time.time()
```

## 20. 最新技术趋势

### 20.1 Python 3.x新特性

#### 类型提示

自Python 3.5起，引入了类型提示（Type Hints），提高了代码可读性和可维护性。

```python
from typing import List, Dict, Tuple, Optional, Union, Any, Callable

# 基本类型注解
def greet(name: str) -> str:
    return f"Hello, {name}!"

# 复合类型
def process_items(items: List[int]) -> Dict[int, str]:
    return {item: str(item) for item in items}

# 可选类型
def find_user(user_id: int) -> Optional[Dict[str, Any]]:
    # 返回用户数据或None
    if user_id == 0:
        return None
    return {"id": user_id, "name": f"User {user_id}"}

# 联合类型
def parse_value(value: Union[str, int, float]) -> float:
    return float(value)

# 函数类型
def apply_function(func: Callable[[int], int], value: int) -> int:
    return func(value)

# 类型别名
Vector = List[float]

def normalize(vector: Vector) -> Vector:
    total = sum(vector)
    return [x / total for x in vector]

# 类型注释也适用于变量
names: List[str] = ["Alice", "Bob", "Charlie"]
user_data: Dict[str, Any] = {"name": "Alice", "age": 30}
```

**Python 3.8引入TypedDict**：
```python
from typing import TypedDict, List

class Movie(TypedDict):
    name: str
    year: int
    director: str
    actors: List[str]

def print_movie(movie: Movie) -> None:
    print(f"{movie['name']} ({movie['year']}), directed by {movie['director']}")

# 使用TypedDict
inception: Movie = {
    "name": "Inception",
    "year": 2010,
    "director": "Christopher Nolan",
    "actors": ["Leonardo DiCaprio", "Ellen Page"]
}

print_movie(inception)
```

**Python 3.10的模式匹配**:
```python
def analyze_data(data):
    match data:
        case {"type": "user", "id": id, "name": name}:
            return f"User {name} with ID {id}"
        
        case {"type": "product", "id": id, "price": price}:
            return f"Product with ID {id} costs ${price}"
        
        case [x, y]:
            return f"Point coordinates: ({x}, {y})"
        
        case [x, y, z]:
            return f"3D coordinates: ({x}, {y}, {z})"
        
        case str(value):
            return f"String: {value}"
        
        case _:
            return "Unknown data format"

# 使用示例
print(analyze_data({"type": "user", "id": 42, "name": "John"}))
print(analyze_data({"type": "product", "id": 101, "price": 99.99}))
print(analyze_data([10, 20]))
print(analyze_data([1, 2, 3]))
print(analyze_data("Hello"))
print(analyze_data(123))
```

#### 异步编程

Python 3.5引入了async/await语法，使异步编程更加直观和强大。

```python
import asyncio
import aiohttp
import time

# 基本异步函数
async def hello_world():
    print("Hello")
    await asyncio.sleep(1)  # 非阻塞暂停
    print("World")

# 异步HTTP请求
async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# 并发执行多个异步任务
async def fetch_multiple_urls(urls):
    tasks = [fetch_url(url) for url in urls]
    return await asyncio.gather(*tasks)

# 实际使用示例
async def main():
    start_time = time.time()
    
    urls = [
        "https://python.org",
        "https://pypi.org",
        "https://docs.python.org",
        "https://github.com",
        "https://stackoverflow.com"
    ]
    
    results = await fetch_multiple_urls(urls)
    
    for url, html in zip(urls, results):
        print(f"{url}: {len(html)} characters")
    
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds")

# 运行异步程序
# asyncio.run(main())  # Python 3.7+
```

**异步上下文管理器**：
```python
import asyncio

class AsyncResource:
    async def __aenter__(self):
        print("Acquiring resource")
        await asyncio.sleep(1)  # 模拟资源获取
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")
        await asyncio.sleep(0.5)  # 模拟资源释放
    
    async def process(self):
        print("Processing with resource")
        await asyncio.sleep(2)

async def use_async_resource():
    async with AsyncResource() as resource:
        await resource.process()
    print("Resource has been released")
```

**异步迭代器**：
```python
import asyncio
from random import random

class AsyncDataSource:
    def __init__(self, items):
        self.items = items
    
    def __aiter__(self):
        self.index = 0
        return self
    
    async def __anext__(self):
        if self.index >= len(self.items):
            raise StopAsyncIteration
        
        value = self.items[self.index]
        self.index += 1
        
        # 模拟异步获取数据
        await asyncio.sleep(random() * 0.5)
        return value

async def process_data_async():
    source = AsyncDataSource(["A", "B", "C", "D", "E"])
    
    async for item in source:
        print(f"Processing {item}")
    
    # 等效于:
    # async_iter = aiter(source)
    # while True:
    #     try:
    #         item = await anext(async_iter)
    #         print(f"Processing {item}")
    #     except StopAsyncIteration:
    #         break
```

#### 数据类

Python 3.7引入了数据类（dataclasses），简化了创建主要用于存储数据的类。

```python
from dataclasses import dataclass, field
from typing import List, Optional
import datetime

# 基本数据类
@dataclass
class Product:
    id: int
    name: str
    price: float
    quantity: int = 0
    tags: List[str] = field(default_factory=list)
    
    def total_value(self) -> float:
        return self.price * self.quantity

# 使用示例
laptop = Product(1, "Laptop", 999.99, 10, ["electronics", "computers"])
print(laptop)  # 自动生成__repr__
print(laptop.total_value())  # 调用方法

# 带默认值和计算字段的数据类
@dataclass
class Order:
    id: int
    products: List[Product]
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    processed: bool = False
    customer_name: Optional[str] = None
    total: float = field(init=False)
    
    def __post_init__(self):
        self.total = sum(product.total_value() for product in self.products)
    
    def process(self):
        self.processed = True
        print(f"Order {self.id} processed, total: ${self.total:.2f}")

# 数据类继承
@dataclass
class DiscountedProduct(Product):
    discount_percent: float = 0.0
    
    def total_value(self) -> float:
        original_value = super().total_value()
        discount = original_value * (self.discount_percent / 100)
        return original_value - discount
```

**不可变数据类**：
```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float
    
    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

# 尝试修改会引发异常
p = Point(3.0, 4.0)
# p.x = 10.0  # 会引发FrozenInstanceError
```

#### 路径操作

Python 3.4引入了pathlib模块，提供了面向对象的文件系统路径API。

```python
from pathlib import Path
import os
import shutil

# 创建路径对象
current_file = Path(__file__)  # 当前文件的路径
project_root = current_file.parent.parent  # 父目录的父目录

# 路径信息
print(f"当前文件: {current_file}")
print(f"父目录: {current_file.parent}")
print(f"文件名: {current_file.name}")
print(f"文件名(无扩展名): {current_file.stem}")
print(f"扩展名: {current_file.suffix}")

# 路径组合
data_dir = project_root / "data"  # 组合路径
config_file = project_root / "config" / "settings.json"

# 创建目录
if not data_dir.exists():
    data_dir.mkdir(parents=True)  # 递归创建目录

# 文件操作
example_file = data_dir / "example.txt"

# 写入文件
example_file.write_text("Hello, Pathlib!")

# 读取文件
content = example_file.read_text()
print(f"文件内容: {content}")

# 文件属性
print(f"文件大小: {example_file.stat().st_size} 字节")
print(f"是否是文件: {example_file.is_file()}")
print(f"是否是目录: {example_file.is_dir()}")

# 查找文件
python_files = list(project_root.glob("**/*.py"))  # 递归查找所有Python文件
print(f"Python文件数量: {len(python_files)}")

# 删除文件
example_file.unlink()  # 删除文件

# 临时目录操作
temp_dir = data_dir / "temp"
temp_dir.mkdir(exist_ok=True)

# 创建多个临时文件
for i in range(5):
    temp_file = temp_dir / f"temp_{i}.txt"
    temp_file.write_text(f"Temporary file {i}")

# 列出所有临时文件
temp_files = list(temp_dir.glob("*.txt"))
for file in temp_files:
    print(f"临时文件: {file.name}, 大小: {file.stat().st_size} 字节")

# 删除目录及其内容
shutil.rmtree(temp_dir)
```

#### 其他Python 3.x新特性

**f-strings (Python 3.6+)**:
```python
name = "Alice"
age = 30
print(f"Name: {name}, Age: {age}")

# Python 3.8+ 增加了=说明符
print(f"{name=}, {age=}")  # 输出: name='Alice', age=30

# 格式化表达式
import math
print(f"π值: {math.pi:.4f}")  # 保留4位小数
```

**赋值表达式 (Python 3.8+)**:
```python
# 海象运算符 :=
if (n := len([1, 2, 3])) > 2:
    print(f"长度为{n}，大于2")

# 在列表推导式中使用
[x for x in range(100) if (x_squared := x * x) < 100]

# 在正则表达式中使用
import re
if match := re.search(r'(\d+)', 'abc123def'):
    print(f"找到数字: {match.group(1)}")
```

**字典合并和更新运算符 (Python 3.9+)**:
```python
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}

# 合并两个字典 (Python 3.9+)
merged = dict1 | dict2  # {'a': 1, 'b': 3, 'c': 4}

# 更新字典 (Python 3.9+)
dict1 |= dict2  # dict1现在是 {'a': 1, 'b': 3, 'c': 4}
```

**更简单的类型注解 (Python 3.9+)**:
```python
# Python 3.9前
from typing import Dict, List, Tuple

points: List[Tuple[int, int]] = [(1, 2), (3, 4)]
counts: Dict[str, int] = {"apple": 10, "banana": 5}

# Python 3.9+
points: list[tuple[int, int]] = [(1, 2), (3, 4)]
counts: dict[str, int] = {"apple": 10, "banana": 5}
```