#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
装饰器基础详解 - Decorator Basics

本文件详细介绍Python装饰器的语法和应用，
包括与Java注解的对比分析。

装饰器是Python的强大特性，提供了AOP（面向切面编程）的能力，
类似于Java中的注解和AOP框架。

Author: Python学习项目
Date: 2024-01-16
"""

import time
import functools
from typing import Callable, Any, TypeVar, ParamSpec
from datetime import datetime


# 类型定义
F = TypeVar('F', bound=Callable[..., Any])
P = ParamSpec('P')
T = TypeVar('T')


def main():
    """装饰器示例主函数"""
    print("=== Python装饰器基础详解 ===\n")
    
    # 1. 装饰器基础概念
    decorator_concepts()
    
    # 2. 简单装饰器示例
    simple_decorators()
    
    # 3. 带参数的装饰器
    parameterized_decorators()
    
    # 4. 类装饰器
    class_decorators()
    
    # 5. 多个装饰器组合
    multiple_decorators()
    
    # 6. 与Java注解对比
    java_annotation_comparison()
    
    # 7. 常用内置装饰器
    builtin_decorators()
    
    # 8. 实际应用示例
    practical_examples()
    
    # 9. 高级装饰器模式
    advanced_patterns()
    
    # 10. 最佳实践
    best_practices()


def decorator_concepts():
    """装饰器基础概念"""
    print("1. 装饰器基础概念")
    print("-" * 40)
    
    # 概念演示：装饰器本质是函数
    print("装饰器本质 - 函数接受函数并返回函数:")
    
    def my_decorator(func):
        """简单装饰器示例"""
        def wrapper():
            print("在函数执行前做些事情")
            result = func()
            print("在函数执行后做些事情")
            return result
        return wrapper
    
    # 手动应用装饰器
    def hello():
        print("Hello, World!")
    
    print("\n手动应用装饰器:")
    print("原函数调用:")
    hello()
    
    print("\n装饰后调用:")
    decorated_hello = my_decorator(hello)
    decorated_hello()
    
    # 使用@语法糖
    print("\n使用@语法糖:")
    
    @my_decorator
    def greet():
        print("Greetings from Python!")
    
    greet()
    
    # 装饰器等价写法
    print("\n装饰器语法糖等价于:")
    print("  @my_decorator")
    print("  def greet():")
    print("      print('Greetings from Python!')")
    print("")
    print("  # 等价于:")
    print("  def greet():")
    print("      print('Greetings from Python!')")
    print("  greet = my_decorator(greet)")
    
    print()


def simple_decorators():
    """简单装饰器示例"""
    print("2. 简单装饰器示例")
    print("-" * 40)
    
    # 示例1：计时装饰器
    def timer(func):
        """计算函数执行时间"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} 执行时间: {end - start:.4f}秒")
            return result
        return wrapper
    
    @timer
    def slow_function():
        """模拟慢函数"""
        time.sleep(0.1)
        return "任务完成"
    
    print("计时装饰器示例:")
    result = slow_function()
    print(f"返回结果: {result}")
    
    # 示例2：日志装饰器
    def logger(func):
        """记录函数调用"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"调用函数: {func.__name__}")
            print(f"参数: args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                print(f"返回值: {result}")
                return result
            except Exception as e:
                print(f"异常: {e}")
                raise
        return wrapper
    
    @logger
    def calculate(x, y, operation="add"):
        """计算函数"""
        if operation == "add":
            return x + y
        elif operation == "multiply":
            return x * y
        else:
            raise ValueError(f"不支持的操作: {operation}")
    
    print(f"\n日志装饰器示例:")
    result1 = calculate(5, 3)
    result2 = calculate(4, 6, operation="multiply")
    
    # 示例3：缓存装饰器
    def simple_cache(func):
        """简单缓存装饰器"""
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args):
            if args in cache:
                print(f"缓存命中: {args}")
                return cache[args]
            else:
                print(f"计算结果: {args}")
                result = func(*args)
                cache[args] = result
                return result
        return wrapper
    
    @simple_cache
    def fibonacci(n):
        """计算斐波那契数"""
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print(f"\n缓存装饰器示例:")
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"fibonacci(10) = {fibonacci(10)}")  # 第二次调用，使用缓存
    
    print()


def parameterized_decorators():
    """带参数的装饰器"""
    print("3. 带参数的装饰器")
    print("-" * 40)
    
    # 示例1：重试装饰器
    def retry(max_attempts=3, delay=1):
        """重试装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if attempt < max_attempts - 1:
                            print(f"第{attempt + 1}次尝试失败，{delay}秒后重试...")
                            time.sleep(delay)
                        else:
                            print(f"所有{max_attempts}次尝试都失败了")
                raise last_exception
            return wrapper
        return decorator
    
    # 使用带参数的装饰器
    @retry(max_attempts=3, delay=0.5)
    def unreliable_function():
        """模拟不稳定的函数"""
        import random
        if random.random() < 0.7:  # 70%的概率失败
            raise Exception("随机失败")
        return "成功执行"
    
    print("重试装饰器示例:")
    try:
        result = unreliable_function()
        print(f"结果: {result}")
    except Exception as e:
        print(f"最终失败: {e}")
    
    # 示例2：权限检查装饰器
    def require_permission(permission):
        """权限检查装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 模拟权限检查
                user_permissions = {'read', 'write'}  # 模拟当前用户权限
                
                if permission not in user_permissions:
                    raise PermissionError(f"需要{permission}权限")
                
                print(f"权限检查通过: {permission}")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @require_permission('admin')
    def delete_user(user_id):
        """删除用户"""
        return f"用户{user_id}已删除"
    
    @require_permission('read')
    def get_user(user_id):
        """获取用户信息"""
        return f"用户{user_id}的信息"
    
    print(f"\n权限装饰器示例:")
    try:
        result = get_user(123)
        print(result)
    except PermissionError as e:
        print(f"权限错误: {e}")
    
    try:
        result = delete_user(123)
        print(result)
    except PermissionError as e:
        print(f"权限错误: {e}")
    
    # 示例3：限流装饰器
    def rate_limit(calls_per_second=1):
        """限流装饰器"""
        def decorator(func):
            last_called = [0]  # 使用列表保持可变性
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                now = time.time()
                time_since_last = now - last_called[0]
                min_interval = 1.0 / calls_per_second
                
                if time_since_last < min_interval:
                    sleep_time = min_interval - time_since_last
                    print(f"限流等待 {sleep_time:.2f}秒...")
                    time.sleep(sleep_time)
                
                last_called[0] = time.time()
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @rate_limit(calls_per_second=2)
    def api_call(data):
        """模拟API调用"""
        return f"处理数据: {data}"
    
    print(f"\n限流装饰器示例:")
    for i in range(3):
        result = api_call(f"数据{i}")
        print(f"  {result}")
    
    print()


def class_decorators():
    """类装饰器"""
    print("4. 类装饰器")
    print("-" * 40)
    
    # 示例1：可调用类作为装饰器
    class CountCalls:
        """统计函数调用次数的类装饰器"""
        
        def __init__(self, func):
            self.func = func
            self.count = 0
            functools.update_wrapper(self, func)
        
        def __call__(self, *args, **kwargs):
            self.count += 1
            print(f"{self.func.__name__} 被调用了 {self.count} 次")
            return self.func(*args, **kwargs)
        
        def get_count(self):
            return self.count
    
    @CountCalls
    def say_hello(name):
        return f"Hello, {name}!"
    
    print("类装饰器示例 - 调用计数:")
    print(say_hello("Alice"))
    print(say_hello("Bob"))
    print(say_hello("Charlie"))
    print(f"总调用次数: {say_hello.get_count()}")
    
    # 示例2：带参数的类装饰器
    class Validate:
        """参数验证类装饰器"""
        
        def __init__(self, *validators):
            self.validators = validators
        
        def __call__(self, func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 验证参数
                for i, validator in enumerate(self.validators):
                    if i < len(args):
                        if not validator(args[i]):
                            raise ValueError(f"参数{i}验证失败: {args[i]}")
                
                return func(*args, **kwargs)
            return wrapper
    
    # 验证函数
    def is_positive(x):
        return isinstance(x, (int, float)) and x > 0
    
    def is_string(x):
        return isinstance(x, str) and len(x) > 0
    
    @Validate(is_positive, is_string)
    def create_user(age, name):
        """创建用户"""
        return f"创建用户: {name}, 年龄: {age}"
    
    print(f"\n参数验证类装饰器:")
    try:
        result = create_user(25, "张三")
        print(result)
    except ValueError as e:
        print(f"验证错误: {e}")
    
    try:
        result = create_user(-5, "李四")  # 年龄为负数
        print(result)
    except ValueError as e:
        print(f"验证错误: {e}")
    
    # 示例3：装饰类的装饰器
    def add_methods(cls):
        """为类添加方法的装饰器"""
        def to_string(self):
            return f"{cls.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"
        
        def equals(self, other):
            return isinstance(other, cls) and self.__dict__ == other.__dict__
        
        cls.to_string = to_string
        cls.equals = equals
        return cls
    
    @add_methods
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
    
    print(f"\n类装饰器示例:")
    person1 = Person("张三", 25)
    person2 = Person("张三", 25)
    person3 = Person("李四", 30)
    
    print(f"person1: {person1.to_string()}")
    print(f"person1 == person2: {person1.equals(person2)}")
    print(f"person1 == person3: {person1.equals(person3)}")
    
    print()


def multiple_decorators():
    """多个装饰器组合"""
    print("5. 多个装饰器组合")
    print("-" * 40)
    
    # 定义多个装饰器
    def bold(func):
        """加粗装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"**{result}**"
        return wrapper
    
    def italic(func):
        """斜体装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"*{result}*"
        return wrapper
    
    def uppercase(func):
        """大写装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.upper()
        return wrapper
    
    # 多个装饰器组合
    @bold
    @italic
    @uppercase
    def format_text(text):
        """格式化文本"""
        return text
    
    print("多装饰器组合示例:")
    result = format_text("hello world")
    print(f"结果: {result}")
    
    # 装饰器执行顺序说明
    print(f"\n装饰器执行顺序:")
    print("  @bold")
    print("  @italic") 
    print("  @uppercase")
    print("  def format_text(text):")
    print("      return text")
    print("")
    print("  等价于:")
    print("  format_text = bold(italic(uppercase(format_text)))")
    print("  执行顺序: uppercase -> italic -> bold")
    
    # 带参数的多装饰器
    def prefix(text):
        """前缀装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                return f"{text}{result}"
            return wrapper
        return decorator
    
    def suffix(text):
        """后缀装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                return f"{result}{text}"
            return wrapper
        return decorator
    
    @prefix(">>> ")
    @suffix(" <<<")
    @timer
    def process_data(data):
        """处理数据"""
        time.sleep(0.01)  # 模拟处理时间
        return f"处理: {data}"
    
    print(f"\n带参数的多装饰器:")
    result = process_data("重要数据")
    print(f"结果: {result}")
    
    print()


def java_annotation_comparison():
    """与Java注解对比"""
    print("6. 与Java注解对比")
    print("-" * 40)
    
    # Python装饰器示例
    print("Python装饰器示例:")
    
    def transactional(func):
        """事务装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("开始事务")
            try:
                result = func(*args, **kwargs)
                print("提交事务")
                return result
            except Exception as e:
                print("回滚事务")
                raise
        return wrapper
    
    def cache_result(expire_time=3600):
        """缓存装饰器"""
        def decorator(func):
            cache = {}
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = str(args) + str(kwargs)
                if key in cache:
                    print(f"从缓存获取: {func.__name__}")
                    return cache[key]
                
                result = func(*args, **kwargs)
                cache[key] = result
                print(f"缓存结果: {func.__name__}")
                return result
            return wrapper
        return decorator
    
    @transactional
    @cache_result(expire_time=1800)
    def update_user_profile(user_id, profile_data):
        """更新用户配置"""
        print(f"更新用户{user_id}的配置: {profile_data}")
        return f"用户{user_id}配置已更新"
    
    # 调用示例
    print("Python调用:")
    result = update_user_profile(123, {'name': '张三', 'age': 25})
    print(f"返回: {result}\n")
    
    # Java等价代码
    print("Java等价代码:")
    print("""
    // Java Spring Boot 注解示例
    @Service
    @Transactional
    public class UserService {
        
        @Cacheable(value = "userProfiles", expire = 1800)
        @Transactional
        public String updateUserProfile(Long userId, Map<String, Object> profileData) {
            System.out.println("更新用户" + userId + "的配置: " + profileData);
            return "用户" + userId + "配置已更新";
        }
    }
    """)
    
    # 特性对比
    print("特性对比:")
    
    print("\nPython装饰器:")
    features_python = [
        "• 运行时动态应用",
        "• 可以修改函数行为",
        "• 支持参数化",
        "• 可以访问和修改参数",
        "• 灵活的组合方式",
        "• 函数式编程风格"
    ]
    
    for feature in features_python:
        print(f"  {feature}")
    
    print("\nJava注解:")
    features_java = [
        "• 编译时/运行时处理",
        "• 主要用于元数据标记",
        "• 需要反射或AOP框架",
        "• 类型安全",
        "• IDE支持更好",
        "• 框架集成度高"
    ]
    
    for feature in features_java:
        print(f"  {feature}")
    
    # 使用场景对比
    print(f"\n使用场景对比:")
    
    scenarios = [
        ("日志记录", "Python: @logger", "Java: @Slf4j + @LogExecutionTime"),
        ("缓存", "Python: @cache", "Java: @Cacheable"),
        ("事务", "Python: @transactional", "Java: @Transactional"),
        ("权限检查", "Python: @require_auth", "Java: @PreAuthorize"),
        ("参数验证", "Python: @validate", "Java: @Valid + @Validated"),
        ("重试机制", "Python: @retry", "Java: @Retryable")
    ]
    
    for scenario, python_example, java_example in scenarios:
        print(f"  {scenario}:")
        print(f"    {python_example}")
        print(f"    {java_example}")
    
    print()


def builtin_decorators():
    """常用内置装饰器"""
    print("7. 常用内置装饰器")
    print("-" * 40)
    
    # @property装饰器
    print("@property装饰器:")
    
    class Circle:
        """圆形类"""
        
        def __init__(self, radius):
            self._radius = radius
        
        @property
        def radius(self):
            """半径属性"""
            return self._radius
        
        @radius.setter
        def radius(self, value):
            """设置半径"""
            if value <= 0:
                raise ValueError("半径必须为正数")
            self._radius = value
        
        @property
        def area(self):
            """计算面积（只读属性）"""
            return 3.14159 * self._radius ** 2
        
        @property
        def diameter(self):
            """直径（只读属性）"""
            return 2 * self._radius
    
    circle = Circle(5)
    print(f"  半径: {circle.radius}")
    print(f"  面积: {circle.area:.2f}")
    print(f"  直径: {circle.diameter}")
    
    circle.radius = 10
    print(f"  新半径: {circle.radius}")
    print(f"  新面积: {circle.area:.2f}")
    
    # @staticmethod和@classmethod装饰器
    print(f"\n@staticmethod和@classmethod装饰器:")
    
    class MathUtils:
        """数学工具类"""
        
        class_name = "MathUtils"
        
        @staticmethod
        def add(x, y):
            """静态方法：加法"""
            return x + y
        
        @classmethod
        def get_class_info(cls):
            """类方法：获取类信息"""
            return f"这是{cls.class_name}类"
        
        @classmethod
        def create_from_string(cls, math_str):
            """类方法：工厂方法"""
            # 简单解析 "x+y" 格式
            parts = math_str.split('+')
            if len(parts) == 2:
                x, y = int(parts[0]), int(parts[1])
                return cls.add(x, y)
            return None
    
    print(f"  静态方法: MathUtils.add(5, 3) = {MathUtils.add(5, 3)}")
    print(f"  类方法: {MathUtils.get_class_info()}")
    print(f"  工厂方法: MathUtils.create_from_string('10+20') = {MathUtils.create_from_string('10+20')}")
    
    # @functools.lru_cache装饰器
    print(f"\n@functools.lru_cache装饰器:")
    
    @functools.lru_cache(maxsize=128)
    def expensive_computation(n):
        """昂贵的计算（带缓存）"""
        print(f"  正在计算 {n}...")
        time.sleep(0.01)  # 模拟耗时计算
        return n ** 2 + 2 * n + 1
    
    print("  第一次调用:")
    result1 = expensive_computation(10)
    print(f"  结果: {result1}")
    
    print("  第二次调用（使用缓存）:")
    result2 = expensive_computation(10)
    print(f"  结果: {result2}")
    
    # 查看缓存信息
    print(f"  缓存信息: {expensive_computation.cache_info()}")
    
    print()


def practical_examples():
    """实际应用示例"""
    print("8. 实际应用示例")
    print("-" * 40)
    
    # 示例1：Web框架路由装饰器
    print("示例1：Web框架路由装饰器")
    
    class SimpleRouter:
        """简单路由器"""
        
        def __init__(self):
            self.routes = {}
        
        def route(self, path, methods=['GET']):
            """路由装饰器"""
            def decorator(func):
                self.routes[path] = {
                    'handler': func,
                    'methods': methods
                }
                return func
            return decorator
        
        def handle_request(self, path, method='GET'):
            """处理请求"""
            if path in self.routes:
                route_info = self.routes[path]
                if method in route_info['methods']:
                    return route_info['handler']()
                else:
                    return f"方法 {method} 不被支持"
            else:
                return "404 Not Found"
    
    # 创建路由器
    app = SimpleRouter()
    
    @app.route('/', methods=['GET'])
    def home():
        return "欢迎访问首页"
    
    @app.route('/users', methods=['GET', 'POST'])
    def users():
        return "用户列表"
    
    @app.route('/api/data', methods=['GET'])
    def api_data():
        return "{'data': 'some data'}"
    
    # 测试路由
    print(f"  GET /: {app.handle_request('/')}")
    print(f"  GET /users: {app.handle_request('/users')}")
    print(f"  POST /users: {app.handle_request('/users', 'POST')}")
    print(f"  GET /api/data: {app.handle_request('/api/data')}")
    
    # 示例2：数据库连接装饰器
    print(f"\n示例2：数据库连接装饰器")
    
    class DatabaseConnection:
        """模拟数据库连接"""
        
        def __init__(self):
            self.connected = False
        
        def connect(self):
            print("    连接数据库...")
            self.connected = True
        
        def disconnect(self):
            print("    断开数据库连接")
            self.connected = False
        
        def execute(self, query):
            if not self.connected:
                raise Exception("数据库未连接")
            return f"执行查询: {query}"
    
    # 全局数据库连接
    db = DatabaseConnection()
    
    def with_database(func):
        """数据库连接装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            db.connect()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                db.disconnect()
        return wrapper
    
    @with_database
    def get_user_by_id(user_id):
        """根据ID获取用户"""
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return db.execute(query)
    
    @with_database
    def create_user(name, email):
        """创建用户"""
        query = f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')"
        return db.execute(query)
    
    print("  数据库操作:")
    result1 = get_user_by_id(123)
    print(f"    {result1}")
    
    result2 = create_user("张三", "zhangsan@example.com")
    print(f"    {result2}")
    
    # 示例3：API限流装饰器
    print(f"\n示例3：API限流装饰器")
    
    from collections import defaultdict, deque
    
    class RateLimiter:
        """速率限制器"""
        
        def __init__(self):
            self.requests = defaultdict(deque)
        
        def rate_limit(self, max_requests=5, time_window=60):
            """限流装饰器"""
            def decorator(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    # 模拟获取客户端IP
                    client_ip = kwargs.get('client_ip', 'default')
                    current_time = time.time()
                    
                    # 清理过期的请求记录
                    while (self.requests[client_ip] and 
                           current_time - self.requests[client_ip][0] > time_window):
                        self.requests[client_ip].popleft()
                    
                    # 检查是否超过限制
                    if len(self.requests[client_ip]) >= max_requests:
                        return {
                            'error': 'Rate limit exceeded',
                            'message': f'最多每{time_window}秒{max_requests}次请求'
                        }
                    
                    # 记录当前请求
                    self.requests[client_ip].append(current_time)
                    
                    # 执行原函数
                    return func(*args, **kwargs)
                return wrapper
            return decorator
    
    # 创建限流器
    limiter = RateLimiter()
    
    @limiter.rate_limit(max_requests=3, time_window=10)
    def api_endpoint(data, client_ip='127.0.0.1'):
        """API端点"""
        return {'success': True, 'data': f'处理数据: {data}'}
    
    print("  API限流测试:")
    for i in range(5):
        result = api_endpoint(f'request_{i}', client_ip='192.168.1.1')
        print(f"    请求{i+1}: {result}")
    
    print()


def advanced_patterns():
    """高级装饰器模式"""
    print("9. 高级装饰器模式")
    print("-" * 40)
    
    # 模式1：装饰器工厂
    print("模式1：装饰器工厂")
    
    def create_validator(**validators):
        """创建验证装饰器的工厂"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 验证参数
                import inspect
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                
                for param_name, validator in validators.items():
                    if param_name in bound_args.arguments:
                        value = bound_args.arguments[param_name]
                        if not validator(value):
                            raise ValueError(f"参数 {param_name} 验证失败: {value}")
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    # 使用装饰器工厂
    @create_validator(
        age=lambda x: isinstance(x, int) and 0 < x < 150,
        name=lambda x: isinstance(x, str) and len(x) > 0,
        email=lambda x: isinstance(x, str) and '@' in x
    )
    def register_user(name, age, email):
        """注册用户"""
        return f"用户注册成功: {name}, {age}岁, {email}"
    
    try:
        result = register_user("张三", 25, "zhangsan@example.com")
        print(f"  {result}")
    except ValueError as e:
        print(f"  验证失败: {e}")
    
    # 模式2：上下文装饰器
    print(f"\n模式2：上下文装饰器")
    
    def with_context(context_manager):
        """上下文管理装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with context_manager as ctx:
                    # 将上下文作为第一个参数传递
                    return func(ctx, *args, **kwargs)
            return wrapper
        return decorator
    
    class FileContext:
        """文件上下文管理器"""
        
        def __init__(self, filename, mode='r'):
            self.filename = filename
            self.mode = mode
            self.file = None
        
        def __enter__(self):
            print(f"    打开文件: {self.filename}")
            # 这里只是模拟，不实际打开文件
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            print(f"    关闭文件: {self.filename}")
        
        def read(self):
            return f"文件{self.filename}的内容"
        
        def write(self, data):
            return f"向文件{self.filename}写入: {data}"
    
    @with_context(FileContext("data.txt", "r"))
    def read_config(file_ctx):
        """读取配置文件"""
        content = file_ctx.read()
        return f"读取到配置: {content}"
    
    print("  上下文装饰器示例:")
    result = read_config()
    print(f"  {result}")
    
    # 模式3：异步装饰器（模拟）
    print(f"\n模式3：异步装饰器模拟")
    
    def async_timeout(timeout_seconds):
        """异步超时装饰器（简化版）"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError(f"函数执行超时 ({timeout_seconds}秒)")
                
                # 设置超时
                old_handler = signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(timeout_seconds)
                
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    # 恢复原来的信号处理器
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, old_handler)
            return wrapper
        return decorator
    
    # 注意：在Windows上SIGALRM不可用，这里只是演示概念
    def simulate_async_timeout(timeout_seconds):
        """模拟超时装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                if execution_time > timeout_seconds:
                    print(f"    警告: 函数执行时间({execution_time:.2f}s)超过预期({timeout_seconds}s)")
                else:
                    print(f"    函数执行时间: {execution_time:.2f}s")
                
                return result
            return wrapper
        return decorator
    
    @simulate_async_timeout(0.05)
    def slow_operation():
        """慢操作"""
        time.sleep(0.1)
        return "操作完成"
    
    print("  模拟异步超时:")
    result = slow_operation()
    print(f"  {result}")
    
    print()


def best_practices():
    """最佳实践"""
    print("10. 最佳实践")
    print("-" * 40)
    
    # 实践1：保持函数元信息
    print("实践1：使用functools.wraps保持函数元信息")
    
    def bad_decorator(func):
        """不保持元信息的装饰器"""
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    def good_decorator(func):
        """保持元信息的装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    def example_function():
        """示例函数"""
        pass
    
    bad_decorated = bad_decorator(example_function)
    good_decorated = good_decorator(example_function)
    
    print(f"  原函数名: {example_function.__name__}")
    print(f"  坏装饰器后: {bad_decorated.__name__}")
    print(f"  好装饰器后: {good_decorated.__name__}")
    print(f"  原函数文档: {example_function.__doc__}")
    print(f"  好装饰器文档: {good_decorated.__doc__}")
    
    # 实践2：参数处理
    print(f"\n实践2：正确处理*args和**kwargs")
    
    def flexible_decorator(func):
        """灵活的装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"  调用 {func.__name__}")
            print(f"  位置参数: {args}")
            print(f"  关键字参数: {kwargs}")
            return func(*args, **kwargs)
        return wrapper
    
    @flexible_decorator
    def flexible_function(a, b, c=None, *args, **kwargs):
        """灵活的函数"""
        return f"a={a}, b={b}, c={c}, args={args}, kwargs={kwargs}"
    
    print("  灵活参数处理:")
    result = flexible_function(1, 2, 3, 4, 5, extra="value")
    print(f"  返回: {result}")
    
    # 实践3：错误处理
    print(f"\n实践3：装饰器中的错误处理")
    
    def safe_decorator(func):
        """安全的装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print(f"  开始执行 {func.__name__}")
                result = func(*args, **kwargs)
                print(f"  成功完成 {func.__name__}")
                return result
            except Exception as e:
                print(f"  执行 {func.__name__} 时出错: {e}")
                # 可以选择重新抛出异常或返回默认值
                raise  # 重新抛出原异常
        return wrapper
    
    @safe_decorator
    def risky_function(x):
        """可能出错的函数"""
        if x < 0:
            raise ValueError("x不能为负数")
        return x ** 2
    
    print("  错误处理示例:")
    try:
        result = risky_function(5)
        print(f"  结果: {result}")
        result = risky_function(-1)
    except ValueError as e:
        print(f"  捕获异常: {e}")
    
    # 实践4：性能考虑
    print(f"\n实践4：性能考虑")
    
    # 避免每次调用都创建新对象
    def efficient_decorator(func):
        """高效的装饰器"""
        # 在装饰器定义时创建，而不是每次调用时创建
        start_message = f"开始执行 {func.__name__}"
        end_message = f"完成执行 {func.__name__}"
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"  {start_message}")
            result = func(*args, **kwargs)
            print(f"  {end_message}")
            return result
        return wrapper
    
    @efficient_decorator
    def some_function():
        """某个函数"""
        return "结果"
    
    print("  性能优化示例:")
    result = some_function()
    print(f"  返回: {result}")
    
    # 最佳实践总结
    print(f"\n最佳实践总结:")
    practices = [
        "1. 使用 @functools.wraps 保持函数元信息",
        "2. 正确处理 *args 和 **kwargs",
        "3. 适当的错误处理和异常传播",
        "4. 考虑装饰器的性能影响", 
        "5. 保持装饰器的单一职责",
        "6. 使用类型注解提高可读性",
        "7. 编写清晰的文档和示例",
        "8. 考虑装饰器的可测试性",
        "9. 避免过度使用装饰器",
        "10. 遵循项目的编码规范"
    ]
    
    for practice in practices:
        print(f"  {practice}")
    
    # 何时避免使用装饰器
    print(f"\n何时避免使用装饰器:")
    avoid_cases = [
        "• 逻辑过于复杂时",
        "• 调试困难时",
        "• 性能要求极高时",
        "• 团队成员不熟悉时",
        "• 可以用更简单方式实现时"
    ]
    
    for case in avoid_cases:
        print(f"  {case}")
    
    print()


if __name__ == '__main__':
    main() 