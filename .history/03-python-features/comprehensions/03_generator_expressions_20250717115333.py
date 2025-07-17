#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成器表达式详解 - Generator Expressions

本文件详细介绍Python生成器表达式的语法和应用，
包括与Java Stream的对比分析。

生成器表达式是Python中实现惰性求值的重要工具，
相当于Java中的Stream API，但语法更加简洁。

Author: Python学习项目
Date: 2024-01-16
"""

import sys
import time
import memory_profiler
from typing import Iterator, Iterable, Any, Generator
from itertools import islice, takewhile, dropwhile, chain


def main():
    """生成器表达式示例主函数"""
    print("=== Python生成器表达式详解 ===\n")
    
    # 1. 基础生成器表达式语法
    basic_generator_expressions()
    
    # 2. 生成器表达式vs列表推导式
    generator_vs_list_comprehension()
    
    # 3. 内存效率对比
    memory_efficiency_comparison()
    
    # 4. 惰性求值特性
    lazy_evaluation_demo()
    
    # 5. 链式操作
    chaining_operations()
    
    # 6. 与Java Stream API对比
    java_stream_comparison()
    
    # 7. 高级用法和模式
    advanced_patterns()
    
    # 8. 实际应用示例
    practical_examples()
    
    # 9. 性能优化技巧
    performance_optimization()
    
    # 10. 常见陷阱和最佳实践
    pitfalls_and_best_practices()


def basic_generator_expressions():
    """基础生成器表达式语法"""
    print("1. 基础生成器表达式语法")
    print("-" * 40)
    
    # 基本语法：(expression for item in iterable)
    # 注意：使用圆括号，不是方括号
    
    # 示例1：简单的数字生成器
    squares_gen = (x**2 for x in range(1, 6))
    print("数字平方生成器:")
    print(f"  生成器对象: {squares_gen}")
    print(f"  生成器类型: {type(squares_gen)}")
    
    # 消费生成器
    print("  生成的值:", list(squares_gen))
    
    # 注意：生成器只能消费一次
    print("  再次消费:", list(squares_gen))  # 空列表
    
    # 示例2：条件筛选
    even_squares = (x**2 for x in range(1, 11) if x % 2 == 0)
    print(f"\n偶数平方: {list(even_squares)}")
    
    # 示例3：字符串处理
    words = ['hello', 'world', 'python', 'generator']
    upper_words = (word.upper() for word in words if len(word) > 4)
    print(f"长单词大写: {list(upper_words)}")
    
    # 示例4：嵌套表达式
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = (item for row in matrix for item in row)
    print(f"矩阵展平: {list(flattened)}")
    
    # 示例5：函数调用
    def process_item(x):
        return x * 2 + 1
    
    processed = (process_item(x) for x in range(5))
    print(f"函数处理: {list(processed)}")
    
    print()


def generator_vs_list_comprehension():
    """生成器表达式vs列表推导式"""
    print("2. 生成器表达式vs列表推导式")
    print("-" * 40)
    
    # 语法对比
    print("语法对比:")
    
    # 列表推导式：立即创建整个列表
    list_comp = [x**2 for x in range(5)]
    print(f"列表推导式: {list_comp}")
    print(f"类型: {type(list_comp)}")
    print(f"大小: {sys.getsizeof(list_comp)} bytes")
    
    # 生成器表达式：创建生成器对象
    gen_expr = (x**2 for x in range(5))
    print(f"生成器表达式: {gen_expr}")
    print(f"类型: {type(gen_expr)}")
    print(f"大小: {sys.getsizeof(gen_expr)} bytes")
    
    # 内存使用对比
    print(f"\n内存使用对比 (1000个元素):")
    
    # 大数据集对比
    n = 1000
    large_list = [x**2 for x in range(n)]
    large_gen = (x**2 for x in range(n))
    
    print(f"列表推导式内存: {sys.getsizeof(large_list)} bytes")
    print(f"生成器表达式内存: {sys.getsizeof(large_gen)} bytes")
    print(f"内存节省: {sys.getsizeof(large_list) / sys.getsizeof(large_gen):.1f}倍")
    
    # 性能对比
    print(f"\n创建时间对比 (100万个元素):")
    n = 1000000
    
    # 列表推导式创建时间
    start_time = time.time()
    large_list = [x for x in range(n)]
    list_time = time.time() - start_time
    
    # 生成器表达式创建时间
    start_time = time.time()
    large_gen = (x for x in range(n))
    gen_time = time.time() - start_time
    
    print(f"列表推导式创建时间: {list_time:.4f}秒")
    print(f"生成器表达式创建时间: {gen_time:.6f}秒")
    print(f"生成器快: {list_time / gen_time:.1f}倍")
    
    # 使用场景建议
    print(f"\n使用场景建议:")
    print("列表推导式适用于:")
    print("  - 需要多次访问数据")
    print("  - 数据集较小")
    print("  - 需要随机访问元素")
    print("  - 需要len()、切片等列表操作")
    
    print("生成器表达式适用于:")
    print("  - 一次性遍历")
    print("  - 大数据集处理")
    print("  - 内存受限环境")
    print("  - 流式数据处理")
    
    print()


def memory_efficiency_comparison():
    """内存效率对比"""
    print("3. 内存效率对比")
    print("-" * 40)
    
    def measure_memory_usage(func, *args):
        """测量函数内存使用"""
        # 简化的内存测量
        import gc
        gc.collect()  # 强制垃圾回收
        before = memory_profiler.memory_usage()[0]
        result = func(*args)
        after = memory_profiler.memory_usage()[0]
        return result, after - before
    
    # 不同数据量的内存对比
    sizes = [1000, 10000, 100000]
    
    for size in sizes:
        print(f"\n数据量: {size:,} 个元素")
        
        # 列表推导式
        def create_list(n):
            return [x**2 for x in range(n)]
        
        # 生成器表达式
        def create_generator(n):
            return (x**2 for x in range(n))
        
        # 测量列表内存
        try:
            list_result, list_memory = measure_memory_usage(create_list, size)
            print(f"  列表推导式内存增长: {list_memory:.2f} MB")
            print(f"  列表大小: {sys.getsizeof(list_result):,} bytes")
        except Exception as e:
            print(f"  列表推导式: 内存不足 ({e})")
        
        # 测量生成器内存
        try:
            gen_result, gen_memory = measure_memory_usage(create_generator, size)
            print(f"  生成器表达式内存增长: {gen_memory:.2f} MB")
            print(f"  生成器大小: {sys.getsizeof(gen_result):,} bytes")
        except Exception as e:
            print(f"  生成器表达式: 内存不足 ({e})")
    
    # 实际内存使用示例
    print(f"\n实际内存使用对比:")
    
    # 创建大量数据
    def memory_intensive_operation():
        # 列表方式：一次性加载所有数据到内存
        data = [x**2 for x in range(1000000)]
        result = sum(x for x in data if x > 100000)
        return result
    
    def memory_efficient_operation():
        # 生成器方式：惰性计算，按需生成
        data = (x**2 for x in range(1000000))
        result = sum(x for x in data if x > 100000)
        return result
    
    print("内存密集操作对比:")
    print("  列表方式: 一次性加载100万个元素到内存")
    print("  生成器方式: 按需生成，内存使用恒定")
    
    print()


def lazy_evaluation_demo():
    """惰性求值特性"""
    print("4. 惰性求值特性")
    print("-" * 40)
    
    # 示例1：惰性求值演示
    def expensive_operation(x):
        """模拟耗时操作"""
        print(f"  正在处理 {x}...")
        time.sleep(0.01)  # 模拟耗时
        return x ** 2
    
    print("惰性求值演示:")
    print("创建生成器（注意：没有立即执行）")
    gen = (expensive_operation(x) for x in range(5))
    print("生成器已创建，但函数还未被调用")
    
    print("\n开始消费生成器:")
    for i, value in enumerate(gen):
        print(f"第{i+1}个值: {value}")
        if i == 2:  # 只取前3个值
            break
    
    print("只计算了需要的前3个值")
    
    # 示例2：无限序列
    print(f"\n无限序列示例:")
    
    def fibonacci_generator():
        """斐波那契数列生成器"""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    # 使用生成器表达式处理无限序列
    fib = fibonacci_generator()
    squares_of_fib = (x**2 for x in fib)
    
    # 只取前10个斐波那契数的平方
    first_10_squares = list(islice(squares_of_fib, 10))
    print(f"前10个斐波那契数的平方: {first_10_squares}")
    
    # 示例3：条件终止
    print(f"\n条件终止示例:")
    
    # 生成数字直到遇到第一个大于100的平方数
    numbers = (x for x in range(1, 20))
    squares = (x**2 for x in numbers)
    small_squares = list(takewhile(lambda x: x <= 100, squares))
    print(f"小于等于100的平方数: {small_squares}")
    
    # 示例4：跳过条件
    print(f"\n跳过条件示例:")
    
    # 跳过小于50的数，然后取后续的数
    numbers = (x for x in range(1, 20))
    squares = (x**2 for x in numbers)
    large_squares = list(dropwhile(lambda x: x < 50, squares))
    print(f"大于等于50的平方数: {large_squares}")
    
    print()


def chaining_operations():
    """链式操作"""
    print("5. 链式操作")
    print("-" * 40)
    
    # 示例1：多步数据处理
    data = range(1, 21)
    
    # 传统方式：多个中间列表
    step1 = [x for x in data if x % 2 == 0]     # 筛选偶数
    step2 = [x**2 for x in step1]               # 计算平方
    step3 = [x for x in step2 if x > 50]        # 筛选大于50的
    result_traditional = list(step3)
    
    # 生成器链式方式：内存高效
    result_generator = list(
        x for x in                              # 最终收集
        (x**2 for x in                         # 计算平方
         (x for x in data if x % 2 == 0))      # 筛选偶数
        if x > 50                              # 筛选大于50的
    )
    
    print("数据处理链:")
    print(f"  原数据: {list(data)}")
    print(f"  筛选偶数 -> 计算平方 -> 筛选>50")
    print(f"  传统方式结果: {result_traditional}")
    print(f"  生成器方式结果: {result_generator}")
    print(f"  结果一致: {result_traditional == result_generator}")
    
    # 示例2：使用itertools组合
    print(f"\n使用itertools组合:")
    
    from itertools import islice, chain, compress
    
    # 多个数据源
    source1 = (x for x in range(1, 6))
    source2 = (x for x in range(10, 16))
    source3 = (x for x in range(20, 26))
    
    # 链式组合多个生成器
    combined = chain(source1, source2, source3)
    squares = (x**2 for x in combined)
    limited = islice(squares, 10)  # 只取前10个
    
    print(f"组合多个源的前10个平方: {list(limited)}")
    
    # 示例3：条件筛选组合
    print(f"\n条件筛选组合:")
    
    # 复杂的数据处理管道
    data = range(1, 100)
    
    pipeline = (
        x * 3                                   # 乘以3
        for x in (
            x + 1                               # 加1
            for x in (
                x for x in data                 # 原数据
                if x % 2 == 0                   # 筛选偶数
            )
            if x < 20                           # 筛选小于20的
        )
        if x % 5 == 0                           # 筛选能被5整除的
    )
    
    result = list(pipeline)
    print(f"复杂管道处理结果: {result}")
    
    # 示例4：函数式风格
    print(f"\n函数式风格:")
    
    def is_even(x):
        return x % 2 == 0
    
    def square(x):
        return x ** 2
    
    def is_large(x):
        return x > 50
    
    # 函数组合
    functional_result = list(
        square(x) for x in data 
        if is_even(x) and is_large(square(x))
    )
    
    print(f"函数式处理结果: {functional_result[:10]}...")  # 显示前10个
    
    print()


def java_stream_comparison():
    """与Java Stream API对比"""
    print("6. 与Java Stream API对比")
    print("-" * 40)
    
    # Python生成器表达式示例
    data = range(1, 21)
    
    # Python: 筛选偶数，计算平方，取前5个
    result = list(islice(
        (x**2 for x in data if x % 2 == 0), 
        5
    ))
    
    print("Python生成器表达式:")
    print(f"  result = list(islice(")
    print(f"      (x**2 for x in data if x % 2 == 0),")
    print(f"      5")
    print(f"  ))")
    print(f"  结果: {result}")
    
    print("\nJava Stream等价代码:")
    print("""
    // Java 8+ Stream API
    List<Integer> data = IntStream.rangeClosed(1, 20)
        .boxed()
        .collect(Collectors.toList());
    
    List<Integer> result = data.stream()
        .filter(x -> x % 2 == 0)      // 筛选偶数
        .map(x -> x * x)              // 计算平方
        .limit(5)                     // 取前5个
        .collect(Collectors.toList());
    """)
    
    # 复杂示例
    print(f"\n复杂处理示例:")
    
    # Python
    words = ['hello', 'world', 'python', 'java', 'stream', 'generator']
    python_result = list(
        word.upper() 
        for word in words 
        if len(word) > 4 and 'o' in word
    )
    
    print("Python:")
    print(f"  words = {words}")
    print(f"  result = list(")
    print(f"      word.upper()")
    print(f"      for word in words")
    print(f"      if len(word) > 4 and 'o' in word")
    print(f"  )")
    print(f"  结果: {python_result}")
    
    print("\nJava等价代码:")
    print("""
    // Java 8+ Stream API
    List<String> words = Arrays.asList(
        "hello", "world", "python", "java", "stream", "generator");
    
    List<String> result = words.stream()
        .filter(word -> word.length() > 4)
        .filter(word -> word.contains("o"))
        .map(String::toUpperCase)
        .collect(Collectors.toList());
    """)
    
    # 特性对比
    print(f"\n特性对比:")
    print("Python生成器表达式:")
    print("  + 语法简洁直观")
    print("  + 内存效率高")
    print("  + 惰性求值")
    print("  + 可组合性强")
    print("  - 类型推断较弱")
    
    print("\nJava Stream API:")
    print("  + 类型安全")
    print("  + 并行处理支持")
    print("  + 丰富的收集器")
    print("  + IDE支持好")
    print("  - 语法较冗长")
    print("  - 装箱/拆箱开销")
    
    print()


def advanced_patterns():
    """高级用法和模式"""
    print("7. 高级用法和模式")
    print("-" * 40)
    
    # 模式1：生成器工厂
    def create_filtered_generator(data, condition):
        """生成器工厂函数"""
        return (item for item in data if condition(item))
    
    numbers = range(1, 11)
    even_gen = create_filtered_generator(numbers, lambda x: x % 2 == 0)
    large_gen = create_filtered_generator(numbers, lambda x: x > 5)
    
    print("生成器工厂模式:")
    print(f"  偶数: {list(even_gen)}")
    print(f"  大数: {list(large_gen)}")
    
    # 模式2：嵌套生成器
    def matrix_generator(rows, cols):
        """矩阵生成器"""
        return ((i * cols + j for j in range(cols)) for i in range(rows))
    
    matrix_gen = matrix_generator(3, 4)
    print(f"\n嵌套生成器模式 (3x4矩阵):")
    for i, row in enumerate(matrix_gen):
        print(f"  行{i}: {list(row)}")
    
    # 模式3：条件生成器
    def conditional_generator(data, *conditions):
        """多条件生成器"""
        return (
            item for item in data 
            if all(condition(item) for condition in conditions)
        )
    
    data = range(1, 21)
    conditions = [
        lambda x: x % 2 == 0,    # 偶数
        lambda x: x > 5,         # 大于5
        lambda x: x < 15         # 小于15
    ]
    
    filtered = conditional_generator(data, *conditions)
    print(f"\n多条件生成器: {list(filtered)}")
    
    # 模式4：管道模式
    class Pipeline:
        """数据处理管道"""
        
        def __init__(self, data):
            self.data = data
        
        def filter(self, condition):
            """筛选数据"""
            self.data = (item for item in self.data if condition(item))
            return self
        
        def map(self, transform):
            """转换数据"""
            self.data = (transform(item) for item in self.data)
            return self
        
        def take(self, n):
            """取前n个"""
            self.data = islice(self.data, n)
            return self
        
        def collect(self):
            """收集结果"""
            return list(self.data)
    
    # 使用管道
    result = (Pipeline(range(1, 21))
              .filter(lambda x: x % 2 == 0)  # 筛选偶数
              .map(lambda x: x ** 2)         # 计算平方
              .filter(lambda x: x > 50)      # 筛选大于50
              .take(5)                       # 取前5个
              .collect())                    # 收集结果
    
    print(f"\n管道模式结果: {result}")
    
    # 模式5：递归生成器
    def recursive_flatten(nested_list):
        """递归展平嵌套列表"""
        for item in nested_list:
            if isinstance(item, (list, tuple)):
                yield from recursive_flatten(item)
            else:
                yield item
    
    nested = [1, [2, 3], [4, [5, 6]], 7]
    flattened = list(recursive_flatten(nested))
    print(f"\n递归展平: {nested} -> {flattened}")
    
    print()


def practical_examples():
    """实际应用示例"""
    print("8. 实际应用示例")
    print("-" * 40)
    
    # 示例1：文件处理
    print("文件处理示例:")
    
    # 模拟文件行
    log_lines = [
        "2024-01-16 10:00:01 INFO User login: user123",
        "2024-01-16 10:00:02 ERROR Database connection failed",
        "2024-01-16 10:00:03 INFO User logout: user123",
        "2024-01-16 10:00:04 WARNING High memory usage",
        "2024-01-16 10:00:05 ERROR File not found",
        "2024-01-16 10:00:06 INFO User login: user456"
    ]
    
    # 筛选错误日志并提取时间
    error_times = (
        line.split()[1] 
        for line in log_lines 
        if 'ERROR' in line
    )
    
    print(f"  错误发生时间: {list(error_times)}")
    
    # 示例2：数据清洗
    print(f"\n数据清洗示例:")
    
    # 原始数据
    raw_data = [
        "  张三, 25, 工程师  ",
        "李四,30,经理",
        "  王五, , 程序员",  # 缺失年龄
        "赵六,35,设计师",
        ", 28, 测试员",      # 缺失姓名
    ]
    
    # 清洗和解析数据
    clean_data = (
        [field.strip() for field in line.split(',')]
        for line in raw_data
        if line.strip()  # 过滤空行
    )
    
    # 筛选有效记录（姓名和职位不为空）
    valid_records = (
        record for record in clean_data
        if len(record) == 3 and record[0] and record[2]
    )
    
    # 转换为字典
    person_records = (
        {
            'name': record[0],
            'age': int(record[1]) if record[1].isdigit() else None,
            'job': record[2]
        }
        for record in valid_records
    )
    
    print(f"  清洗后数据:")
    for person in person_records:
        print(f"    {person}")
    
    # 示例3：API数据处理
    print(f"\n API数据处理示例:")
    
    # 模拟API响应
    api_responses = [
        {'id': 1, 'name': 'Product A', 'price': 100, 'category': 'Electronics'},
        {'id': 2, 'name': 'Product B', 'price': 50, 'category': 'Books'},
        {'id': 3, 'name': 'Product C', 'price': 200, 'category': 'Electronics'},
        {'id': 4, 'name': 'Product D', 'price': 30, 'category': 'Books'},
        {'id': 5, 'name': 'Product E', 'price': 150, 'category': 'Clothing'}
    ]
    
    # 处理数据：筛选高价电子产品，添加折扣信息
    expensive_electronics = (
        {
            **product,
            'discounted_price': product['price'] * 0.9,
            'discount': '10%'
        }
        for product in api_responses
        if product['category'] == 'Electronics' and product['price'] > 80
    )
    
    print(f"  高价电子产品（含折扣）:")
    for product in expensive_electronics:
        print(f"    {product['name']}: ${product['price']} -> ${product['discounted_price']:.1f}")
    
    # 示例4：时间序列数据
    print(f"\n时间序列数据处理:")
    
    # 模拟股价数据
    stock_prices = [100, 102, 98, 105, 103, 107, 104, 108, 110, 106]
    
    # 计算移动平均（3日）
    def moving_average(prices, window=3):
        """计算移动平均"""
        return (
            sum(prices[i:i+window]) / window
            for i in range(len(prices) - window + 1)
        )
    
    ma_3 = list(moving_average(stock_prices, 3))
    print(f"  原价格: {stock_prices}")
    print(f"  3日移动平均: {ma_3}")
    
    # 找出价格上涨的日子
    price_changes = (
        (i+1, prices[i+1] - prices[i])
        for i, prices in enumerate(zip(stock_prices, stock_prices[1:]))
    )
    
    up_days = list(
        (day, change) 
        for day, change in price_changes 
        if change > 0
    )
    
    print(f"  上涨日期: {up_days}")
    
    print()


def performance_optimization():
    """性能优化技巧"""
    print("9. 性能优化技巧")
    print("-" * 40)
    
    # 技巧1：避免重复计算
    print("技巧1：避免重复计算")
    
    # 不好的做法
    def bad_expensive_func(x):
        # 模拟昂贵计算
        return sum(range(x * 1000))
    
    # 好的做法：缓存计算结果
    _cache = {}
    def good_expensive_func(x):
        if x not in _cache:
            _cache[x] = sum(range(x * 1000))
        return _cache[x]
    
    data = [1, 2, 1, 3, 2, 1]  # 有重复值
    
    # 使用缓存的生成器
    optimized_gen = (good_expensive_func(x) for x in data)
    print(f"  使用缓存避免重复计算")
    
    # 技巧2：使用内置函数
    print(f"\n技巧2：使用内置函数")
    
    # 慢速方式
    def slow_sum_squares(n):
        return sum(x**2 for x in range(n))
    
    # 快速方式：使用map
    def fast_sum_squares(n):
        return sum(map(lambda x: x*x, range(n)))
    
    n = 10000
    
    start = time.time()
    result1 = slow_sum_squares(n)
    time1 = time.time() - start
    
    start = time.time()
    result2 = fast_sum_squares(n)
    time2 = time.time() - start
    
    print(f"  生成器表达式: {time1:.4f}秒")
    print(f"  map函数: {time2:.4f}秒")
    print(f"  结果一致: {result1 == result2}")
    
    # 技巧3：适当使用islice
    print(f"\n技巧3：使用islice避免创建大列表")
    
    # 只需要前100个结果
    def process_large_dataset():
        # 模拟大数据集
        return (x**2 for x in range(1000000))
    
    # 高效方式：使用islice
    first_100 = list(islice(process_large_dataset(), 100))
    print(f"  前100个平方数: {first_100[:10]}...")
    
    # 技巧4：链式生成器
    print(f"\n技巧4：链式生成器避免中间列表")
    
    def chain_example(data):
        # 多步处理，每步都是生成器
        step1 = (x for x in data if x % 2 == 0)
        step2 = (x**2 for x in step1)
        step3 = (x for x in step2 if x > 100)
        return step3
    
    result = list(chain_example(range(1, 21)))
    print(f"  链式处理结果: {result}")
    
    # 技巧5：条件短路
    print(f"\n技巧5：条件短路优化")
    
    def expensive_check(x):
        # 模拟昂贵的检查
        time.sleep(0.001)
        return x > 50
    
    def cheap_check(x):
        # 便宜的检查
        return x % 2 == 0
    
    # 好的做法：先进行便宜的检查
    data = range(1, 101)
    optimized = (
        x for x in data 
        if cheap_check(x) and expensive_check(x)  # 短路求值
    )
    
    print(f"  使用短路求值优化")
    
    print()


def pitfalls_and_best_practices():
    """常见陷阱和最佳实践"""
    print("10. 常见陷阱和最佳实践")
    print("-" * 40)
    
    # 陷阱1：生成器只能消费一次
    print("陷阱1：生成器只能消费一次")
    
    gen = (x**2 for x in range(5))
    print(f"  第一次消费: {list(gen)}")
    print(f"  第二次消费: {list(gen)}")  # 空列表
    
    # 解决方案：重新创建或使用itertools.tee
    from itertools import tee
    
    def create_generator():
        return (x**2 for x in range(5))
    
    gen1, gen2 = tee(create_generator(), 2)
    print(f"  使用tee分割: {list(gen1)}, {list(gen2)}")
    
    # 陷阱2：闭包变量陷阱
    print(f"\n陷阱2：闭包变量陷阱")
    
    # 错误示例
    funcs = []
    for i in range(3):
        funcs.append(lambda x: x + i)  # i是闭包变量
    
    # 所有函数都引用同一个i（最终值2）
    results = [func(10) for func in funcs]
    print(f"  错误结果: {results}")  # [12, 12, 12]
    
    # 正确方式：使用默认参数
    funcs = []
    for i in range(3):
        funcs.append(lambda x, i=i: x + i)  # 捕获i的值
    
    results = [func(10) for func in funcs]
    print(f"  正确结果: {results}")  # [10, 11, 12]
    
    # 在生成器中的应用
    # 错误
    gens = []
    for i in range(3):
        gens.append((x + i for x in range(3)))
    
    # 正确
    gens = []
    for i in range(3):
        gens.append((x + i for x in range(3)) for i in [i])  # 立即求值
    
    # 陷阱3：内存泄漏
    print(f"\n陷阱3：避免内存泄漏")
    
    # 不好的做法：保持对大对象的引用
    def bad_generator():
        large_data = list(range(1000000))  # 大对象
        return (x for x in large_data)  # 生成器持有引用
    
    # 好的做法：不保持不必要的引用
    def good_generator():
        return (x for x in range(1000000))  # 直接生成
    
    print(f"  避免在生成器中保持大对象引用")
    
    # 最佳实践总结
    print(f"\n最佳实践总结:")
    
    practices = [
        "1. 优先使用生成器表达式处理大数据集",
        "2. 注意生成器只能消费一次的特性",
        "3. 使用islice限制生成器输出",
        "4. 避免在生成器中保持大对象引用",
        "5. 适当使用itertools模块增强功能",
        "6. 复杂逻辑提取为函数提高可读性",
        "7. 注意闭包变量的作用域问题",
        "8. 使用类型注解提高代码可维护性"
    ]
    
    for practice in practices:
        print(f"  {practice}")
    
    # 性能指南
    print(f"\n性能指南:")
    performance_tips = [
        "• 生成器表达式比列表推导式节省内存",
        "• map()通常比生成器表达式快一些",
        "• filter()比条件生成器表达式快",
        "• 避免在生成器中进行昂贵计算",
        "• 使用内置函数而不是自定义函数",
        "• 适当使用缓存避免重复计算"
    ]
    
    for tip in performance_tips:
        print(f"  {tip}")
    
    print()


if __name__ == '__main__':
    main() 