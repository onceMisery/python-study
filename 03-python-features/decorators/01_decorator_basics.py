#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python装饰器详解
Decorators in Python

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习Python装饰器的语法、原理和与Java注解/AOP的对比

学习目标:
1. 掌握装饰器的基本语法和工作原理
2. 理解函数装饰器和类装饰器的使用
3. 学会带参数的装饰器设计
4. 对比Java注解和AOP的实现方式
"""

import time
import functools
from typing import Callable, Any, Type
import logging
from datetime import datetime


def demo_basic_decorator_syntax():
    """演示装饰器的基本语法"""
    print("=== 1. 基本装饰器语法 ===")
    
    # 最简单的装饰器
    def simple_decorator(func):
        """简单装饰器：在函数执行前后打印信息"""
        def wrapper():
            print("函数执行前")
            result = func()
            print("函数执行后")
            return result
        return wrapper
    
    # 使用装饰器的两种方式
    
    # 方式1：使用@语法糖
    @simple_decorator
    def say_hello():
        print("Hello, World!")
        return "greeting"
    
    # 方式2：手动应用装饰器
    def say_goodbye():
        print("Goodbye, World!")
        return "farewell"
    
    say_goodbye_decorated = simple_decorator(say_goodbye)
    
    print("使用@语法糖的装饰器:")
    result1 = say_hello()
    print(f"返回值: {result1}")
    
    print("\n手动应用装饰器:")
    result2 = say_goodbye_decorated()
    print(f"返回值: {result2}")
    
    # 装饰器的本质：函数替换
    print(f"\n装饰器的本质:")
    print(f"say_hello实际上是: {say_hello.__name__}")
    print(f"say_hello的类型: {type(say_hello)}")
    
    """
    Java等价实现（使用注解+AOP）:
    
    @Component
    public class GreetingService {
        
        @LogExecution  // 自定义注解
        public String sayHello() {
            System.out.println("Hello, World!");
            return "greeting";
        }
    }
    
    // AOP切面
    @Aspect
    @Component
    public class LoggingAspect {
        
        @Around("@annotation(LogExecution)")
        public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
            System.out.println("函数执行前");
            Object result = joinPoint.proceed();
            System.out.println("函数执行后");
            return result;
        }
    }
    
    // 自定义注解
    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
    public @interface LogExecution {
    }
    """
    
    print()


def demo_decorator_with_arguments():
    """演示带参数的装饰器"""
    print("=== 2. 带参数的装饰器 ===")
    
    # 处理有参数函数的装饰器
    def log_calls(func):
        """记录函数调用的装饰器"""
        @functools.wraps(func)  # 保持原函数的元数据
        def wrapper(*args, **kwargs):
            print(f"调用函数: {func.__name__}")
            print(f"位置参数: {args}")
            print(f"关键字参数: {kwargs}")
            
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            print(f"执行时间: {end_time - start_time:.4f}秒")
            print(f"返回值: {result}")
            return result
        return wrapper
    
    @log_calls
    def add_numbers(a, b, operation="add"):
        """加法函数"""
        if operation == "add":
            return a + b
        elif operation == "multiply":
            return a * b
        else:
            return 0
    
    @log_calls
    def greet_person(name, age=None):
        """问候函数"""
        if age:
            return f"Hello {name}, you are {age} years old!"
        else:
            return f"Hello {name}!"
    
    print("调用带参数的函数:")
    result1 = add_numbers(5, 3)
    print()
    
    result2 = add_numbers(4, 6, operation="multiply")
    print()
    
    result3 = greet_person("Alice", age=25)
    print()
    
    result4 = greet_person("Bob")
    print()
    
    # 验证functools.wraps的作用
    print("函数元数据保持:")
    print(f"函数名: {add_numbers.__name__}")
    print(f"文档字符串: {add_numbers.__doc__}")
    
    """
    Java等价实现:
    
    @Service
    public class CalculatorService {
        
        @LogCalls
        public int addNumbers(int a, int b, String operation) {
            if ("add".equals(operation)) {
                return a + b;
            } else if ("multiply".equals(operation)) {
                return a * b;
            }
            return 0;
        }
    }
    
    @Around("@annotation(LogCalls)")
    public Object logCalls(ProceedingJoinPoint joinPoint) throws Throwable {
        String methodName = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();
        
        System.out.println("调用方法: " + methodName);
        System.out.println("参数: " + Arrays.toString(args));
        
        long startTime = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long endTime = System.currentTimeMillis();
        
        System.out.println("执行时间: " + (endTime - startTime) + "ms");
        System.out.println("返回值: " + result);
        
        return result;
    }
    """
    
    print()


def demo_parameterized_decorators():
    """演示参数化装饰器"""
    print("=== 3. 参数化装饰器 ===")
    
    # 可以接受参数的装饰器
    def repeat(times):
        """重复执行装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                results = []
                for i in range(times):
                    print(f"第{i+1}次执行:")
                    result = func(*args, **kwargs)
                    results.append(result)
                return results
            return wrapper
        return decorator
    
    def retry(max_attempts=3, delay=1.0):
        """重试装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                
                for attempt in range(max_attempts):
                    try:
                        print(f"尝试第{attempt + 1}次执行 {func.__name__}")
                        result = func(*args, **kwargs)
                        print(f"成功执行!")
                        return result
                    except Exception as e:
                        last_exception = e
                        print(f"执行失败: {e}")
                        if attempt < max_attempts - 1:
                            print(f"等待{delay}秒后重试...")
                            time.sleep(delay)
                
                print(f"所有重试都失败了")
                raise last_exception
            return wrapper
        return decorator
    
    def cache_result(ttl_seconds=60):
        """缓存结果装饰器"""
        def decorator(func):
            cache = {}
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 创建缓存键
                cache_key = str(args) + str(sorted(kwargs.items()))
                current_time = time.time()
                
                # 检查缓存
                if cache_key in cache:
                    result, timestamp = cache[cache_key]
                    if current_time - timestamp < ttl_seconds:
                        print(f"缓存命中: {func.__name__}")
                        return result
                    else:
                        print(f"缓存过期，重新计算")
                        del cache[cache_key]
                
                # 计算结果并缓存
                print(f"计算新结果: {func.__name__}")
                result = func(*args, **kwargs)
                cache[cache_key] = (result, current_time)
                return result
            return wrapper
        return decorator
    
    # 使用参数化装饰器
    @repeat(times=3)
    def say_number(num):
        print(f"  数字是: {num}")
        return num * 2
    
    @retry(max_attempts=3, delay=0.5)
    def unreliable_function(success_rate=0.3):
        """模拟不稳定的函数"""
        import random
        if random.random() < success_rate:
            return "成功执行!"
        else:
            raise Exception("随机失败")
    
    @cache_result(ttl_seconds=5)
    def expensive_calculation(x, y):
        """模拟昂贵的计算"""
        print(f"  执行昂贵计算: {x} + {y}")
        time.sleep(1)  # 模拟耗时操作
        return x + y
    
    print("重复执行装饰器:")
    results = say_number(5)
    print(f"所有结果: {results}")
    print()
    
    print("重试装饰器:")
    try:
        result = unreliable_function(success_rate=0.8)
        print(f"最终结果: {result}")
    except Exception as e:
        print(f"最终失败: {e}")
    print()
    
    print("缓存装饰器:")
    result1 = expensive_calculation(10, 20)
    print(f"第一次调用结果: {result1}")
    
    result2 = expensive_calculation(10, 20)  # 应该使用缓存
    print(f"第二次调用结果: {result2}")
    
    result3 = expensive_calculation(15, 25)  # 不同参数，重新计算
    print(f"不同参数结果: {result3}")
    
    """
    Java等价实现（使用注解参数）:
    
    @Retry(maxAttempts = 3, delay = 500)
    @Cacheable(value = "calculations", ttl = 60)
    public class CalculationService {
        
        public int expensiveCalculation(int x, int y) {
            // 模拟昂贵计算
            try { Thread.sleep(1000); } catch (InterruptedException e) {}
            return x + y;
        }
    }
    
    // 自定义重试注解
    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
    public @interface Retry {
        int maxAttempts() default 3;
        long delay() default 1000;
    }
    
    // AOP实现
    @Around("@annotation(retry)")
    public Object handleRetry(ProceedingJoinPoint joinPoint, Retry retry) throws Throwable {
        int maxAttempts = retry.maxAttempts();
        long delay = retry.delay();
        
        Throwable lastException = null;
        for (int attempt = 0; attempt < maxAttempts; attempt++) {
            try {
                return joinPoint.proceed();
            } catch (Exception e) {
                lastException = e;
                if (attempt < maxAttempts - 1) {
                    Thread.sleep(delay);
                }
            }
        }
        throw lastException;
    }
    """
    
    print()


def demo_class_decorators():
    """演示类装饰器"""
    print("=== 4. 类装饰器 ===")
    
    # 装饰器类
    class CountCalls:
        """计数器装饰器类"""
        
        def __init__(self, func):
            self.func = func
            self.count = 0
            functools.update_wrapper(self, func)
        
        def __call__(self, *args, **kwargs):
            self.count += 1
            print(f"函数 {self.func.__name__} 被调用了 {self.count} 次")
            return self.func(*args, **kwargs)
        
        def get_count(self):
            return self.count
    
    # 类装饰器装饰函数
    @CountCalls
    def calculate_square(x):
        """计算平方"""
        return x ** 2
    
    # 装饰类的装饰器
    def add_repr(cls):
        """为类添加repr方法的装饰器"""
        def __repr__(self):
            attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
            return f'{cls.__name__}({attrs})'
        
        cls.__repr__ = __repr__
        return cls
    
    def singleton(cls):
        """单例模式装饰器"""
        instances = {}
        
        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]
        
        return get_instance
    
    def add_method(method_name, method_impl):
        """动态添加方法的装饰器"""
        def decorator(cls):
            setattr(cls, method_name, method_impl)
            return cls
        return decorator
    
    # 使用类装饰器
    print("使用类装饰器:")
    result1 = calculate_square(4)
    print(f"结果: {result1}")
    
    result2 = calculate_square(5)
    print(f"结果: {result2}")
    
    result3 = calculate_square(6)
    print(f"结果: {result3}")
    
    print(f"总调用次数: {calculate_square.get_count()}")
    print()
    
    # 装饰类
    @add_repr
    @singleton
    class DatabaseConnection:
        """数据库连接类"""
        
        def __init__(self, host="localhost", port=5432):
            self.host = host
            self.port = port
            self.connected = False
            print(f"创建数据库连接: {host}:{port}")
        
        def connect(self):
            self.connected = True
            print("数据库连接已建立")
        
        def disconnect(self):
            self.connected = False
            print("数据库连接已断开")
    
    @add_method('get_status', lambda self: f"连接状态: {'已连接' if self.connected else '未连接'}")
    class ConfigurableService:
        """可配置服务类"""
        
        def __init__(self, name):
            self.name = name
    
    print("单例模式测试:")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"db1 is db2: {db1 is db2}")  # 应该是True
    print(f"db1: {db1}")
    print()
    
    print("动态添加方法:")
    service = ConfigurableService("MyService")
    print(f"服务状态: {service.get_status()}")
    
    """
    Java等价实现:
    
    // 单例模式（通过注解+DI容器）
    @Component
    @Scope("singleton")  // Spring默认就是单例
    public class DatabaseConnection {
        // ...
    }
    
    // 添加功能（通过接口+代理）
    @Component
    public class DatabaseConnectionProxy implements DatabaseConnection {
        
        private final DatabaseConnection target;
        private int callCount = 0;
        
        @Override
        public void connect() {
            callCount++;
            System.out.println("调用次数: " + callCount);
            target.connect();
        }
    }
    
    // 或者使用AOP
    @Aspect
    @Component
    public class CallCountAspect {
        
        private final Map<String, Integer> callCounts = new ConcurrentHashMap<>();
        
        @Around("execution(* com.example..*(..))")
        public Object countCalls(ProceedingJoinPoint joinPoint) throws Throwable {
            String methodName = joinPoint.getSignature().getName();
            callCounts.merge(methodName, 1, Integer::sum);
            System.out.println("方法 " + methodName + " 被调用了 " + callCounts.get(methodName) + " 次");
            return joinPoint.proceed();
        }
    }
    """
    
    print()


def demo_practical_decorators():
    """演示实用装饰器"""
    print("=== 5. 实用装饰器 ===")
    
    # 性能监控装饰器
    def performance_monitor(func):
        """性能监控装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = get_memory_usage()
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = get_memory_usage()
            
            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory
            
            print(f"性能监控 - {func.__name__}:")
            print(f"  执行时间: {execution_time:.4f}秒")
            print(f"  内存变化: {memory_delta:.2f}MB")
            
            return result
        return wrapper
    
    def get_memory_usage():
        """获取内存使用量（简化版）"""
        import psutil
        import os
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # MB
    
    # 权限检查装饰器
    def require_permission(permission):
        """权限检查装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 模拟获取当前用户
                current_user = getattr(wrapper, 'current_user', {'permissions': ['read', 'write']})
                
                if permission not in current_user.get('permissions', []):
                    raise PermissionError(f"需要权限: {permission}")
                
                print(f"权限检查通过: {permission}")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    # 输入验证装饰器
    def validate_types(**type_checks):
        """类型验证装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 获取函数参数名
                import inspect
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                
                # 验证类型
                for param_name, expected_type in type_checks.items():
                    if param_name in bound_args.arguments:
                        value = bound_args.arguments[param_name]
                        if not isinstance(value, expected_type):
                            raise TypeError(
                                f"参数 {param_name} 期望类型 {expected_type.__name__}, "
                                f"实际类型 {type(value).__name__}"
                            )
                
                print(f"类型验证通过: {func.__name__}")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    # 日志装饰器
    def log_to_file(log_file="app.log"):
        """文件日志装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                try:
                    result = func(*args, **kwargs)
                    log_entry = f"[{timestamp}] SUCCESS: {func.__name__}({args}, {kwargs}) -> {result}\n"
                    
                except Exception as e:
                    log_entry = f"[{timestamp}] ERROR: {func.__name__}({args}, {kwargs}) -> {str(e)}\n"
                    raise
                
                finally:
                    # 模拟写日志（实际应该写入文件）
                    print(f"日志记录: {log_entry.strip()}")
                
                return result
            return wrapper
        return decorator
    
    # 使用实用装饰器
    @performance_monitor
    @log_to_file("calculation.log")
    @validate_types(numbers=list, multiplier=int)
    def process_numbers(numbers, multiplier=2):
        """处理数字列表"""
        result = [num * multiplier for num in numbers]
        time.sleep(0.1)  # 模拟耗时操作
        return result
    
    @require_permission('admin')
    @log_to_file("admin.log")
    def delete_user(user_id):
        """删除用户（需要管理员权限）"""
        print(f"删除用户: {user_id}")
        return f"用户 {user_id} 已删除"
    
    # 设置当前用户权限
    delete_user.current_user = {'permissions': ['read', 'write', 'admin']}
    
    print("使用实用装饰器:")
    
    # 测试性能监控和类型验证
    try:
        result = process_numbers([1, 2, 3, 4, 5], multiplier=3)
        print(f"处理结果: {result}")
    except Exception as e:
        print(f"错误: {e}")
    print()
    
    # 测试类型验证失败
    try:
        result = process_numbers("not a list", multiplier=3)
    except TypeError as e:
        print(f"类型验证失败: {e}")
    print()
    
    # 测试权限检查
    try:
        result = delete_user("user123")
        print(f"删除结果: {result}")
    except PermissionError as e:
        print(f"权限错误: {e}")
    
    """
    Java等价实现:
    
    // 性能监控
    @PerformanceMonitor
    @Transactional
    @PreAuthorize("hasRole('ADMIN')")
    @Validated
    public class UserService {
        
        public List<Integer> processNumbers(@Valid @NotNull List<Integer> numbers, 
                                          @Min(1) Integer multiplier) {
            return numbers.stream()
                         .map(num -> num * multiplier)
                         .collect(Collectors.toList());
        }
        
        @PreAuthorize("hasPermission('user', 'delete')")
        public String deleteUser(@NotBlank String userId) {
            // 删除逻辑
            return "用户 " + userId + " 已删除";
        }
    }
    
    // AOP切面会按照优先级执行
    @Order(1)
    @Aspect
    public class ValidationAspect { ... }
    
    @Order(2) 
    @Aspect
    public class LoggingAspect { ... }
    
    @Order(3)
    @Aspect
    public class PerformanceAspect { ... }
    """
    
    print()


def demo_decorator_chaining():
    """演示装饰器链"""
    print("=== 6. 装饰器链 ===")
    
    # 多个装饰器的执行顺序
    def decorator_a(func):
        print("装饰器A: 装饰阶段")
        def wrapper(*args, **kwargs):
            print("装饰器A: 执行前")
            result = func(*args, **kwargs)
            print("装饰器A: 执行后")
            return result
        return wrapper
    
    def decorator_b(func):
        print("装饰器B: 装饰阶段")
        def wrapper(*args, **kwargs):
            print("装饰器B: 执行前")
            result = func(*args, **kwargs)
            print("装饰器B: 执行后")
            return result
        return wrapper
    
    def decorator_c(func):
        print("装饰器C: 装饰阶段")
        def wrapper(*args, **kwargs):
            print("装饰器C: 执行前")
            result = func(*args, **kwargs)
            print("装饰器C: 执行后")
            return result
        return wrapper
    
    # 装饰器链的执行顺序（从最靠近函数的开始）
    print("创建装饰器链:")
    
    @decorator_a
    @decorator_b  
    @decorator_c
    def test_function():
        print("原始函数执行")
        return "函数结果"
    
    print("\n执行装饰器链:")
    result = test_function()
    print(f"最终结果: {result}")
    
    # 实际的业务装饰器链示例
    print("\n实际业务装饰器链:")
    
    def timing(func):
        """计时装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"⏱️  执行时间: {end - start:.4f}秒")
            return result
        return wrapper
    
    def logging_decorator(func):
        """日志装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"📝 开始执行: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                print(f"✅ 成功完成: {func.__name__}")
                return result
            except Exception as e:
                print(f"❌ 执行失败: {func.__name__} - {e}")
                raise
        return wrapper
    
    def validate_input(func):
        """输入验证装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"🔍 验证输入参数...")
            # 简单验证示例
            if args and any(arg is None for arg in args):
                raise ValueError("参数不能为None")
            print(f"✅ 输入验证通过")
            return func(*args, **kwargs)
        return wrapper
    
    # 组合使用多个装饰器
    @timing
    @logging_decorator
    @validate_input
    def complex_calculation(x, y, z):
        """复杂计算函数"""
        print(f"🧮 执行计算: {x} + {y} * {z}")
        time.sleep(0.1)  # 模拟耗时计算
        result = x + y * z
        return result
    
    try:
        result = complex_calculation(10, 5, 3)
        print(f"🎯 计算结果: {result}")
    except Exception as e:
        print(f"💥 计算失败: {e}")
    
    print("\n装饰器链说明:")
    print("执行顺序: validate_input -> logging_decorator -> timing -> 原函数")
    print("装饰顺序: timing(logging_decorator(validate_input(complex_calculation)))")
    
    """
    Java装饰器链等价实现:
    
    // 使用多个注解
    @Component
    @Transactional
    @Cacheable("calculations")
    @PreAuthorize("hasRole('USER')")
    @Validated
    @PerformanceMonitor
    public class CalculationService {
        
        public Integer complexCalculation(@Valid @NotNull Integer x, 
                                        @Valid @NotNull Integer y, 
                                        @Valid @NotNull Integer z) {
            // 业务逻辑
            return x + y * z;
        }
    }
    
    // AOP切面会按照优先级执行
    @Order(1)
    @Aspect
    public class ValidationAspect { ... }
    
    @Order(2) 
    @Aspect
    public class LoggingAspect { ... }
    
    @Order(3)
    @Aspect
    public class PerformanceAspect { ... }
    """
    
    print()


def main():
    """主函数：运行所有演示"""
    print("Python装饰器完整学习指南")
    print("=" * 50)
    
    demo_basic_decorator_syntax()
    demo_decorator_with_arguments()
    demo_parameterized_decorators()
    demo_class_decorators()
    demo_practical_decorators()
    demo_decorator_chaining()
    
    print("学习总结:")
    print("1. 装饰器是Python中实现AOP（面向切面编程）的主要方式")
    print("2. 本质是函数替换，@语法糖让代码更简洁")
    print("3. 支持参数化装饰器，可以实现灵活的功能增强")
    print("4. 类装饰器提供了更强大的状态管理能力")
    print("5. 装饰器链的执行顺序需要特别注意")
    print("6. Java的注解+AOP提供类似功能但方式不同")
    print("7. Python装饰器更灵活，Java注解+AOP更规范")


if __name__ == "__main__":
    main() 