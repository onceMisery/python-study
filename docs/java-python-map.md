# Java-Python 语法映射对比

## 概述

本文档详细对比Java和Python的语法特性，帮助Java开发者快速理解Python的语法差异和设计哲学。

---

## 基础语法对比

### 1. 变量声明

| 特性 | Java | Python |
|------|------|--------|
| 类型声明 | 必须显式声明 | 动态推导 |
| 变量作用域 | 块级作用域 | 函数级作用域 |
| 常量定义 | `final` 关键字 | 约定大写命名 |

```java
// Java - 静态类型
int age = 25;
String name = "Alice";
final double PI = 3.14159;
List<String> names = new ArrayList<>();
```

```python
# Python - 动态类型
age = 25
name = "Alice"
PI = 3.14159  # 约定：大写表示常量
names = []

# 类型提示（可选）
age: int = 25
name: str = "Alice"
names: List[str] = []
```

### 2. 控制结构

#### 条件判断

```java
// Java
if (score >= 90) {
    System.out.println("优秀");
} else if (score >= 80) {
    System.out.println("良好");
} else {
    System.out.println("及格");
}

// 三元运算符
String result = (score >= 60) ? "及格" : "不及格";
```

```python
# Python
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
else:
    print("及格")

# 三元运算符（条件表达式）
result = "及格" if score >= 60 else "不及格"
```

#### 循环结构

```java
// Java - for循环
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

// 增强for循环
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
for (String name : names) {
    System.out.println(name);
}

// while循环
int i = 0;
while (i < 10) {
    System.out.println(i);
    i++;
}
```

```python
# Python - for循环
for i in range(10):
    print(i)

# 遍历列表
names = ["Alice", "Bob", "Charlie"]
for name in names:
    print(name)

# 带索引遍历
for index, name in enumerate(names):
    print(f"{index}: {name}")

# while循环
i = 0
while i < 10:
    print(i)
    i += 1
```

### 3. 函数/方法定义

```java
// Java - 方法定义
public class Calculator {
    // 普通方法
    public int add(int a, int b) {
        return a + b;
    }
    
    // 重载方法
    public double add(double a, double b) {
        return a + b;
    }
    
    // 静态方法
    public static int multiply(int a, int b) {
        return a * b;
    }
    
    // 可变参数
    public int sum(int... numbers) {
        int total = 0;
        for (int num : numbers) {
            total += num;
        }
        return total;
    }
}
```

```python
# Python - 函数定义
def add(a, b):
    """基本函数"""
    return a + b

# 默认参数
def greet(name, message="Hello"):
    return f"{message}, {name}!"

# 可变参数
def sum_numbers(*args):
    """可变位置参数"""
    return sum(args)

# 关键字参数
def create_user(name, age, **kwargs):
    """可变关键字参数"""
    user = {"name": name, "age": age}
    user.update(kwargs)
    return user

# 类型提示
def calculate(a: int, b: int) -> int:
    return a + b

# 类方法和静态方法
class Calculator:
    @staticmethod
    def multiply(a, b):
        return a * b
    
    @classmethod
    def from_string(cls, calculation_str):
        # 解析字符串并创建实例
        pass
```

---

## 面向对象编程对比

### 1. 类定义

```java
// Java
public class Person {
    private String name;
    private int age;
    private static int count = 0;
    
    // 构造函数
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
        count++;
    }
    
    // Getter/Setter
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    // 实例方法
    public void introduce() {
        System.out.println("I'm " + name + ", " + age + " years old");
    }
    
    // 静态方法
    public static int getCount() { return count; }
}
```

```python
# Python
class Person:
    count = 0  # 类变量
    
    def __init__(self, name, age):
        """构造函数"""
        self.name = name  # 实例变量
        self.age = age
        Person.count += 1
    
    def introduce(self):
        """实例方法"""
        print(f"I'm {self.name}, {self.age} years old")
    
    @classmethod
    def get_count(cls):
        """类方法"""
        return cls.count
    
    @staticmethod
    def is_adult(age):
        """静态方法"""
        return age >= 18
    
    @property
    def display_name(self):
        """属性访问器"""
        return f"Mr./Ms. {self.name}"
    
    @display_name.setter
    def display_name(self, value):
        """属性设置器"""
        self.name = value.replace("Mr./Ms. ", "")
```

### 2. 继承

```java
// Java
public class Animal {
    protected String name;
    
    public Animal(String name) {
        this.name = name;
    }
    
    public void speak() {
        System.out.println(name + " makes a sound");
    }
}

public class Dog extends Animal {
    private String breed;
    
    public Dog(String name, String breed) {
        super(name);  // 调用父类构造函数
        this.breed = breed;
    }
    
    @Override
    public void speak() {
        System.out.println(name + " barks");
    }
    
    public void wagTail() {
        System.out.println(name + " wags tail");
    }
}
```

```python
# Python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        print(f"{self.name} makes a sound")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # 调用父类构造函数
        self.breed = breed
    
    def speak(self):
        """重写父类方法"""
        print(f"{self.name} barks")
    
    def wag_tail(self):
        print(f"{self.name} wags tail")

# 多重继承（Java不支持）
class Flyable:
    def fly(self):
        print("Flying...")

class Bird(Animal, Flyable):
    def __init__(self, name, wing_span):
        super().__init__(name)
        self.wing_span = wing_span
```

---

## 数据结构对比

### 1. 集合类型

| Java类型 | Python类型 | 特性对比 |
|----------|-------------|----------|
| `ArrayList<T>` | `list` | 动态数组，可变长度 |
| `LinkedList<T>` | `collections.deque` | 双端队列 |
| `HashMap<K,V>` | `dict` | 键值对映射 |
| `HashSet<T>` | `set` | 无重复元素集合 |
| `String` | `str` | 不可变字符串 |

```java
// Java
import java.util.*;

List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");

Map<String, Integer> ages = new HashMap<>();
ages.put("Alice", 25);
ages.put("Bob", 30);

Set<String> uniqueNames = new HashSet<>();
uniqueNames.add("Alice");
uniqueNames.add("Bob");
```

```python
# Python
# 列表（可变）
names = ["Alice", "Bob"]
names.append("Charlie")

# 元组（不可变）
coordinates = (10, 20)

# 字典
ages = {"Alice": 25, "Bob": 30}
ages["Charlie"] = 35

# 集合
unique_names = {"Alice", "Bob"}
unique_names.add("Charlie")

# 列表推导式（Java无对应语法）
squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

### 2. 字符串处理

```java
// Java
String name = "Alice";
String message = String.format("Hello, %s! You are %d years old.", name, 25);

// StringBuilder for efficiency
StringBuilder sb = new StringBuilder();
sb.append("Hello, ").append(name);

// 字符串方法
String text = "  Hello World  ";
String trimmed = text.trim();
String[] words = text.split(" ");
String joined = String.join("-", words);
```

```python
# Python
name = "Alice"

# 字符串格式化（多种方式）
message1 = "Hello, %s! You are %d years old." % (name, 25)
message2 = "Hello, {}! You are {} years old.".format(name, 25)
message3 = f"Hello, {name}! You are {25} years old."  # f-string (推荐)

# 字符串方法
text = "  Hello World  "
trimmed = text.strip()
words = text.split()
joined = "-".join(words)

# 字符串是不可变的（与Java相同）
# 但Python有更简洁的操作方式
```

---

## 异常处理对比

```java
// Java
try {
    int result = Integer.parseInt("abc");
} catch (NumberFormatException e) {
    System.err.println("Number format error: " + e.getMessage());
} catch (Exception e) {
    System.err.println("General error: " + e.getMessage());
} finally {
    System.out.println("Cleanup code");
}

// 自定义异常
public class CustomException extends Exception {
    public CustomException(String message) {
        super(message);
    }
}

// 声明抛出异常
public void riskyMethod() throws CustomException {
    throw new CustomException("Something went wrong");
}
```

```python
# Python
try:
    result = int("abc")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"General error: {e}")
else:
    print("No exception occurred")  # Java没有else子句
finally:
    print("Cleanup code")

# 自定义异常
class CustomException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

# 抛出异常（不需要声明）
def risky_function():
    raise CustomException("Something went wrong")

# 异常链
try:
    risky_function()
except CustomException as e:
    raise RuntimeError("Failed to process") from e
```

---

## 模块和包系统对比

### Java包系统

```java
// 文件: com/example/utils/StringUtil.java
package com.example.utils;

public class StringUtil {
    public static String capitalize(String str) {
        return str.substring(0, 1).toUpperCase() + str.substring(1);
    }
}

// 使用
import com.example.utils.StringUtil;
// 或
import com.example.utils.*;

public class Main {
    public static void main(String[] args) {
        String result = StringUtil.capitalize("hello");
    }
}
```

### Python模块系统

```python
# 文件: utils/string_util.py
def capitalize(text):
    """首字母大写"""
    return text.capitalize() if text else text

def snake_to_camel(snake_str):
    """蛇形命名转驼峰命名"""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

# 文件: utils/__init__.py
from .string_util import capitalize, snake_to_camel

# 使用（多种导入方式）
import utils.string_util
from utils.string_util import capitalize
from utils import capitalize
import utils.string_util as str_util

# 使用
result1 = utils.string_util.capitalize("hello")
result2 = capitalize("hello")
result3 = str_util.capitalize("hello")
```

---

## 高级特性对比

### 1. Lambda表达式和函数式编程

```java
// Java 8+
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

// Lambda表达式
List<Integer> doubled = numbers.stream()
    .map(x -> x * 2)
    .collect(Collectors.toList());

// 方法引用
List<String> strings = numbers.stream()
    .map(String::valueOf)
    .collect(Collectors.toList());

// 函数式接口
Function<Integer, Integer> square = x -> x * x;
Predicate<Integer> isEven = x -> x % 2 == 0;
```

```python
# Python
numbers = [1, 2, 3, 4, 5]

# Lambda表达式
doubled = list(map(lambda x: x * 2, numbers))

# 列表推导式（更Pythonic）
doubled = [x * 2 for x in numbers]

# 高阶函数
square = lambda x: x * x
is_even = lambda x: x % 2 == 0

# filter和map
evens = list(filter(is_even, numbers))
squares = list(map(square, numbers))

# 更Pythonic的写法
evens = [x for x in numbers if x % 2 == 0]
squares = [x**2 for x in numbers]
```

### 2. 装饰器模式

```java
// Java - 需要设计模式或框架支持
public interface Component {
    void operation();
}

public class ConcreteComponent implements Component {
    public void operation() {
        System.out.println("Basic operation");
    }
}

public class Decorator implements Component {
    private Component component;
    
    public Decorator(Component component) {
        this.component = component;
    }
    
    public void operation() {
        System.out.println("Before operation");
        component.operation();
        System.out.println("After operation");
    }
}
```

```python
# Python - 内置装饰器语法
import time
from functools import wraps

def timer(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

def log(func):
    """日志装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

# 使用装饰器
@timer
@log
def slow_function(n):
    time.sleep(n)
    return f"Slept for {n} seconds"

# 等价于：
# slow_function = timer(log(slow_function))
```

### 3. 并发编程

```java
// Java
import java.util.concurrent.*;

// 线程池
ExecutorService executor = Executors.newFixedThreadPool(4);

// 提交任务
Future<String> future = executor.submit(() -> {
    Thread.sleep(1000);
    return "Task completed";
});

// 获取结果
try {
    String result = future.get();
    System.out.println(result);
} catch (InterruptedException | ExecutionException e) {
    e.printStackTrace();
}

executor.shutdown();

// CompletableFuture (Java 8+)
CompletableFuture<String> future2 = CompletableFuture
    .supplyAsync(() -> "Hello")
    .thenCompose(s -> CompletableFuture.supplyAsync(() -> s + " World"))
    .thenApply(s -> s + "!");
```

```python
# Python
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# 多线程
def worker(name):
    time.sleep(1)
    return f"Worker {name} completed"

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(worker, i) for i in range(4)]
    results = [future.result() for future in as_completed(futures)]

# 异步编程（Python独有的简洁语法）
async def async_worker(name):
    await asyncio.sleep(1)
    return f"Async worker {name} completed"

async def main():
    tasks = [async_worker(i) for i in range(4)]
    results = await asyncio.gather(*tasks)
    print(results)

# 运行异步函数
asyncio.run(main())
```

---

## 开发环境和工具对比

### 项目结构

```
Java项目结构:
src/
├── main/
│   ├── java/
│   │   └── com/example/myapp/
│   │       ├── Main.java
│   │       ├── model/
│   │       ├── service/
│   │       └── controller/
│   └── resources/
│       ├── application.properties
│       └── static/
├── test/
│   └── java/
│       └── com/example/myapp/
└── pom.xml (Maven) 或 build.gradle (Gradle)
```

```
Python项目结构:
myapp/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       │   └── __init__.py
│       ├── services/
│       │   └── __init__.py
│       └── controllers/
│           └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt 或 pyproject.toml
├── setup.py
└── README.md
```

### 依赖管理

```xml
<!-- Java - Maven (pom.xml) -->
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <version>2.7.0</version>
    </dependency>
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.13.2</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

```python
# Python - requirements.txt
flask==2.3.0
requests==2.28.0
pytest==7.1.0

# 或者 pyproject.toml (Poetry)
[tool.poetry.dependencies]
python = "^3.9"
flask = "^2.3.0"
requests = "^2.28.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.1.0"
```

---

## 性能和最佳实践对比

### 1. 性能考虑

| 方面 | Java | Python |
|------|------|--------|
| 执行速度 | 编译型，更快 | 解释型，相对较慢 |
| 内存管理 | JVM垃圾回收 | 引用计数 + 循环垃圾回收 |
| 并发模型 | 真正的多线程 | GIL限制（但有multiprocessing） |
| 启动时间 | JVM启动较慢 | 快速启动 |

### 2. 编码风格

```java
// Java - 驼峰命名，详细的类型声明
public class UserService {
    private UserRepository userRepository;
    
    public User getUserById(Long userId) throws UserNotFoundException {
        Optional<User> userOptional = userRepository.findById(userId);
        return userOptional.orElseThrow(() -> 
            new UserNotFoundException("User not found: " + userId));
    }
}
```

```python
# Python - 蛇形命名，简洁的语法
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository
    
    def get_user_by_id(self, user_id):
        """获取用户，如果不存在则抛出异常"""
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundException(f"User not found: {user_id}")
        return user
```

---

## 学习建议

### 1. 思维转换

- **从静态到动态**：适应Python的动态类型系统
- **从冗长到简洁**：学会欣赏Python的简洁语法
- **从严格到灵活**：理解Python的"成人语言"哲学
- **从单一到多样**：Python支持多种编程范式

### 2. 常见陷阱

```python
# 陷阱1：可变默认参数
def bad_function(items=[]):  # 危险！
    items.append(1)
    return items

def good_function(items=None):  # 正确
    if items is None:
        items = []
    items.append(1)
    return items

# 陷阱2：闭包中的变量绑定
functions = []
for i in range(3):
    functions.append(lambda: i)  # 都会返回2

# 正确方式
functions = []
for i in range(3):
    functions.append(lambda x=i: x)

# 陷阱3：is vs ==
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # True，值相等
print(a is b)  # False，不是同一个对象

# 但是对于小整数和字符串
x = 100
y = 100
print(x is y)  # True，Python优化
```

### 3. Python之禅

```python
import this
# 会显示Python之禅，体现Python的设计哲学
```

核心理念：
- 优美胜于丑陋
- 明确胜于晦涩
- 简单胜于复杂
- 扁平胜于嵌套
- 可读性很重要

---

这个映射表应该能帮助你快速理解Python与Java的主要差异。建议在学习每个新概念时都参考这个对比，逐步建立Python的思维模式。 