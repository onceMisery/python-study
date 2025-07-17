#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python生成器表达式详解
Generator Expressions in Python

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习Python生成器表达式的语法、惰性求值特性、内存优化和与Java Stream的对比

学习目标:
1. 掌握生成器表达式的基本语法
2. 理解惰性求值的概念和优势
3. 学会内存优化的应用场景
4. 对比Java Stream API的惰性求值特性
"""

import time
import sys
import random
from typing import Iterator, Generator, Any
from memory_profiler import profile
import itertools


def demo_basic_syntax():
    """演示生成器表达式的基本语法"""
    print("=== 1. 基本语法演示 ===")
    
    # 基础语法: (expression for item in iterable)
    numbers = [1, 2, 3, 4, 5]
    
    # 列表推导式 vs 生成器表达式
    list_comp = [x**2 for x in numbers]  # 立即计算所有值
    gen_expr = (x**2 for x in numbers)   # 惰性求值，按需计算
    
    print(f"列表推导式: {list_comp}")
    print(f"生成器表达式: {gen_expr}")
    print(f"生成器类型: {type(gen_expr)}")
    
    # 从生成器获取值
    print("从生成器逐个获取值:")
    for value in gen_expr:
        print(f"  {value}")
    
    # 生成器只能遍历一次
    print("再次遍历生成器:")
    for value in gen_expr:
        print(f"  {value}")  # 不会输出任何内容
    print("  (生成器已耗尽)")
    
    """
    Java等价实现:
    List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
    
    // 立即求值 (类似列表推导式)
    List<Integer> listResult = numbers.stream()
                                     .map(x -> x * x)
                                     .collect(Collectors.toList());
    
    // 惰性求值 (类似生成器表达式)
    Stream<Integer> streamResult = numbers.stream()
                                         .map(x -> x * x);
    // 注意：Java Stream也是惰性的，只有在终端操作时才执行
    """
    
    print()


def demo_lazy_evaluation():
    """演示惰性求值的特性"""
    print("=== 2. 惰性求值特性 ===")
    
    def expensive_operation(x):
        """模拟昂贵的计算操作"""
        print(f"    正在处理 {x}...")
        time.sleep(0.1)  # 模拟耗时操作
        return x**2
    
    numbers = [1, 2, 3, 4, 5]
    
    print("创建列表推导式（立即求值）:")
    start_time = time.time()
    list_result = [expensive_operation(x) for x in numbers]
    list_time = time.time() - start_time
    print(f"列表推导式创建耗时: {list_time:.2f}秒")
    print(f"结果: {list_result}")
    
    print("\n创建生成器表达式（惰性求值）:")
    start_time = time.time()
    gen_result = (expensive_operation(x) for x in numbers)
    gen_creation_time = time.time() - start_time
    print(f"生成器表达式创建耗时: {gen_creation_time:.4f}秒")
    print(f"生成器对象: {gen_result}")
    
    print("\n从生成器获取前两个值:")
    start_time = time.time()
    first_two = [next(gen_result), next(gen_result)]
    partial_time = time.time() - start_time
    print(f"获取前两个值耗时: {partial_time:.2f}秒")
    print(f"前两个值: {first_two}")
    
    """
    Java Stream惰性求值示例:
    Stream<Integer> lazyStream = numbers.stream()
        .map(x -> expensiveOperation(x))  // 这里不会立即执行
        .filter(x -> x > 10);             // 这里也不会执行
    
    // 只有在终端操作时才会执行所有中间操作
    List<Integer> result = lazyStream.limit(2)
                                   .collect(Collectors.toList());
    """
    
    print()


def demo_memory_efficiency():
    """演示内存效率对比"""
    print("=== 3. 内存效率对比 ===")
    
    # 大数据集测试
    large_size = 1000000
    
    def measure_memory_usage(operation_name, operation):
        """测量内存使用"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        result = operation()
        end_time = time.time()
        
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = memory_after - memory_before
        
        print(f"{operation_name}:")
        print(f"  时间: {end_time - start_time:.4f}秒")
        print(f"  内存使用: {memory_used:.2f}MB")
        
        return result, memory_used
    
    print(f"处理 {large_size:,} 个元素:")
    
    # 列表推导式 - 立即创建所有元素
    def create_list():
        return [x**2 for x in range(large_size)]
    
    list_result, list_memory = measure_memory_usage("列表推导式", create_list)
    print(f"  列表长度: {len(list_result):,}")
    
    # 生成器表达式 - 按需生成
    def create_generator():
        return (x**2 for x in range(large_size))
    
    gen_result, gen_memory = measure_memory_usage("生成器表达式", create_generator)
    print(f"  生成器对象: {gen_result}")
    
    # 内存效率比较
    if list_memory > 0 and gen_memory >= 0:
        efficiency_ratio = list_memory / max(gen_memory, 0.1)
        print(f"\n内存效率提升: {efficiency_ratio:.1f}倍")
    
    # 演示生成器的实际使用
    print("\n使用生成器处理大数据集的前10个元素:")
    gen_sample = (x**2 for x in range(large_size))
    first_10 = [next(gen_sample) for _ in range(10)]
    print(f"前10个平方数: {first_10}")
    
    """
    Java Stream内存效率:
    // Java Stream也是惰性的，类似于Python生成器
    Stream<Integer> infiniteStream = Stream.iterate(0, x -> x + 1)
                                          .map(x -> x * x);
    
    // 只处理需要的元素，不会创建完整的集合
    List<Integer> first10 = infiniteStream.limit(10)
                                        .collect(Collectors.toList());
    
    // 并行处理大数据集
    List<Integer> parallelResult = IntStream.range(0, 1_000_000)
                                          .parallel()
                                          .map(x -> x * x)
                                          .filter(x -> x % 2 == 0)
                                          .limit(100)
                                          .boxed()
                                          .collect(Collectors.toList());
    """
    
    print()


def demo_conditional_generators():
    """演示条件生成器表达式"""
    print("=== 4. 条件生成器表达式 ===")
    
    # 大数据集中的筛选
    numbers = range(1, 1000000)
    
    # 筛选质数的生成器
    def is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    # 使用生成器表达式筛选质数
    prime_gen = (n for n in numbers if is_prime(n))
    
    print("前20个质数:")
    primes = []
    for _ in range(20):
        primes.append(next(prime_gen))
    print(f"{primes}")
    
    # 复杂条件筛选
    def fibonacci_generator(limit):
        """斐波那契数列生成器"""
        a, b = 0, 1
        while a < limit:
            yield a
            a, b = b, a + b
    
    # 筛选偶数斐波那契数
    fib_gen = fibonacci_generator(1000)
    even_fib = (n for n in fib_gen if n % 2 == 0)
    
    print("1000以内的偶数斐波那契数:")
    even_fib_list = list(even_fib)
    print(f"{even_fib_list}")
    
    # 多重条件筛选
    data_range = range(1, 10000)
    complex_filter = (
        x for x in data_range 
        if x % 7 == 0 and x % 11 != 0 and str(x)[-1] in '37'
    )
    
    print("复杂条件筛选结果（前10个）:")
    complex_results = [next(complex_filter) for _ in range(10)]
    print(f"{complex_results}")
    
    """
    Java Stream条件筛选:
    // 质数筛选
    Stream<Integer> primeStream = IntStream.range(1, 1_000_000)
                                         .filter(this::isPrime)
                                         .boxed();
    
    List<Integer> first20Primes = primeStream.limit(20)
                                           .collect(Collectors.toList());
    
    // 复杂条件筛选
    Stream<Integer> complexFilter = IntStream.range(1, 10_000)
                                           .filter(x -> x % 7 == 0)
                                           .filter(x -> x % 11 != 0)
                                           .filter(x -> String.valueOf(x).endsWith("3") || 
                                                       String.valueOf(x).endsWith("7"))
                                           .boxed();
    """
    
    print()


def demo_chaining_operations():
    """演示链式操作"""
    print("=== 5. 链式操作演示 ===")
    
    # 多层生成器表达式
    numbers = range(1, 100)
    
    # 链式过滤和转换
    step1 = (x for x in numbers if x % 2 == 0)          # 偶数
    step2 = (x * x for x in step1 if x % 4 == 0)        # 能被4整除的偶数的平方
    step3 = (x for x in step2 if x < 1000)              # 小于1000的结果
    
    print("链式操作结果:")
    result = list(step3)
    print(f"结果: {result}")
    
    # 使用itertools进行高级组合
    from itertools import chain, islice, takewhile, dropwhile
    
    # 组合多个生成器
    gen1 = (x for x in range(1, 6))
    gen2 = (x for x in range(10, 16))
    gen3 = (x for x in range(20, 26))
    
    combined = chain(gen1, gen2, gen3)
    print("组合生成器结果:")
    print(f"前10个元素: {list(islice(combined, 10))}")
    
    # 条件截取
    numbers_gen = (x for x in range(1, 50))
    
    # 取小于30的元素
    less_than_30 = takewhile(lambda x: x < 30, numbers_gen)
    print("小于30的元素（前15个）:")
    print(f"{list(islice(less_than_30, 15))}")
    
    # 跳过小于20的元素
    numbers_gen2 = (x for x in range(1, 50))
    greater_equal_20 = dropwhile(lambda x: x < 20, numbers_gen2)
    print("大于等于20的元素（前10个）:")
    print(f"{list(islice(greater_equal_20, 10))}")
    
    """
    Java Stream链式操作:
    List<Integer> result = IntStream.range(1, 100)
                                  .filter(x -> x % 2 == 0)     // 偶数
                                  .filter(x -> x % 4 == 0)     // 能被4整除
                                  .map(x -> x * x)             // 平方
                                  .filter(x -> x < 1000)       // 小于1000
                                  .boxed()
                                  .collect(Collectors.toList());
    
    // 组合多个Stream
    Stream<Integer> combined = Stream.concat(
        Stream.concat(stream1, stream2),
        stream3
    );
    
    // 条件截取
    List<Integer> lessThan30 = stream.takeWhile(x -> x < 30)
                                    .collect(Collectors.toList());
    """
    
    print()


def demo_practical_applications():
    """演示实际应用场景"""
    print("=== 6. 实际应用场景 ===")
    
    # 场景1: 大文件处理
    print("场景1: 大文件处理模拟")
    
    def simulate_large_file_lines():
        """模拟大文件的行生成器"""
        for i in range(1000000):
            yield f"Line {i}: Some data content with number {random.randint(1, 100)}"
    
    # 处理包含特定内容的行
    file_lines = simulate_large_file_lines()
    interesting_lines = (
        line for line in file_lines 
        if "data" in line and int(line.split()[-1]) > 90
    )
    
    print("包含'data'且数字>90的行（前5行）:")
    for i, line in enumerate(interesting_lines):
        if i >= 5:
            break
        print(f"  {line}")
    
    # 场景2: API数据流处理
    print("\n场景2: API数据流处理模拟")
    
    def simulate_api_responses():
        """模拟API响应数据流"""
        statuses = ["success", "error", "pending", "timeout"]
        for i in range(1000):
            yield {
                "id": i,
                "status": random.choice(statuses),
                "timestamp": f"2024-01-16T10:{i%60:02d}:00Z",
                "value": random.randint(1, 100)
            }
    
    # 处理成功的响应
    api_stream = simulate_api_responses()
    successful_responses = (
        response for response in api_stream 
        if response["status"] == "success" and response["value"] > 80
    )
    
    print("成功且值>80的响应（前3个）:")
    for i, response in enumerate(successful_responses):
        if i >= 3:
            break
        print(f"  ID: {response['id']}, Value: {response['value']}")
    
    # 场景3: 数据管道处理
    print("\n场景3: 数据管道处理")
    
    def data_pipeline(raw_data):
        """数据处理管道"""
        # 步骤1: 清理数据
        cleaned = (
            item.strip().lower() for item in raw_data 
            if item and item.strip()
        )
        
        # 步骤2: 过滤有效数据
        valid = (
            item for item in cleaned 
            if len(item) > 2 and item.isalpha()
        )
        
        # 步骤3: 转换数据
        transformed = (
            f"processed_{item}" for item in valid
        )
        
        return transformed
    
    # 模拟原始数据
    raw_data = [
        "  Hello  ", "", "World", "123", "  Python  ", 
        "AI", "x", "Programming", "  ", "Data"
    ]
    
    pipeline_result = data_pipeline(raw_data)
    print("数据管道处理结果:")
    for result in pipeline_result:
        print(f"  {result}")
    
    # 场景4: 无限数据流
    print("\n场景4: 无限数据流处理")
    
    def infinite_counter():
        """无限计数器"""
        count = 0
        while True:
            yield count
            count += 1
    
    # 从无限流中取出符合条件的元素
    counter = infinite_counter()
    perfect_squares = (
        x for x in counter 
        if int(x**0.5)**2 == x  # 完全平方数
    )
    
    print("前10个完全平方数:")
    squares = []
    for i, square in enumerate(perfect_squares):
        if i >= 10:
            break
        squares.append(square)
    print(f"  {squares}")
    
    """
    Java实际应用场景:
    
    // 大文件处理
    Stream<String> fileLines = Files.lines(Paths.get("large_file.txt"));
    Stream<String> interestingLines = fileLines
        .filter(line -> line.contains("data"))
        .filter(line -> extractNumber(line) > 90);
    
    // API数据流处理
    Stream<ApiResponse> apiStream = getApiResponseStream();
    Stream<ApiResponse> successfulResponses = apiStream
        .filter(response -> "success".equals(response.getStatus()))
        .filter(response -> response.getValue() > 80);
    
    // 无限数据流
    Stream<Integer> infiniteStream = Stream.iterate(0, x -> x + 1);
    List<Integer> perfectSquares = infiniteStream
        .filter(x -> isPerfectSquare(x))
        .limit(10)
        .collect(Collectors.toList());
    """
    
    print()


def demo_performance_comparison():
    """演示性能对比"""
    print("=== 7. 性能对比分析 ===")
    
    data_size = 1000000
    
    def measure_performance(name, operation):
        start_time = time.time()
        result = operation()
        end_time = time.time()
        
        # 获取结果的类型和大小信息
        if hasattr(result, '__len__'):
            size_info = f"长度: {len(result)}"
        else:
            size_info = f"类型: {type(result).__name__}"
        
        print(f"{name}:")
        print(f"  时间: {end_time - start_time:.4f}秒")
        print(f"  结果: {size_info}")
        
        return result, end_time - start_time
    
    print(f"处理 {data_size:,} 个元素的性能对比:")
    
    # 1. 列表推导式 - 全量计算
    def list_comprehension_full():
        return [x**2 for x in range(data_size) if x % 2 == 0]
    
    list_result, list_time = measure_performance(
        "列表推导式（全量计算）", list_comprehension_full
    )
    
    # 2. 生成器表达式 - 创建对象
    def generator_creation():
        return (x**2 for x in range(data_size) if x % 2 == 0)
    
    gen_result, gen_time = measure_performance(
        "生成器表达式（创建对象）", generator_creation
    )
    
    # 3. 生成器表达式 - 部分消费
    def generator_partial():
        gen = (x**2 for x in range(data_size) if x % 2 == 0)
        return [next(gen) for _ in range(100)]  # 只取前100个
    
    partial_result, partial_time = measure_performance(
        "生成器表达式（取前100个）", generator_partial
    )
    
    # 4. 内置函数优化
    def builtin_optimized():
        return list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(data_size))))
    
    builtin_result, builtin_time = measure_performance(
        "内置函数（map+filter）", builtin_optimized
    )
    
    # 性能分析
    print("\n性能分析:")
    print(f"生成器创建比列表推导式快: {list_time/gen_time:.0f}倍")
    print(f"部分消费的实际优势: {list_time/partial_time:.0f}倍")
    
    # 内存使用对比
    print("\n内存使用分析:")
    print(f"列表推导式结果大小: {sys.getsizeof(list_result[:1000]):,} bytes (前1000个)")
    print(f"生成器对象大小: {sys.getsizeof(gen_result):,} bytes")
    print(f"内存效率提升: {sys.getsizeof(list_result[:1000])/sys.getsizeof(gen_result):.0f}倍")
    
    """
    Java性能对比:
    // 立即求值
    List<Integer> listResult = IntStream.range(0, 1_000_000)
                                      .filter(x -> x % 2 == 0)
                                      .map(x -> x * x)
                                      .boxed()
                                      .collect(Collectors.toList());
    
    // 惰性求值 + 部分消费
    List<Integer> partialResult = IntStream.range(0, 1_000_000)
                                         .filter(x -> x % 2 == 0)
                                         .map(x -> x * x)
                                         .limit(100)
                                         .boxed()
                                         .collect(Collectors.toList());
    
    // 并行处理
    List<Integer> parallelResult = IntStream.range(0, 1_000_000)
                                          .parallel()
                                          .filter(x -> x % 2 == 0)
                                          .map(x -> x * x)
                                          .boxed()
                                          .collect(Collectors.toList());
    """
    
    print()


def demo_best_practices():
    """演示最佳实践和注意事项"""
    print("=== 8. 最佳实践和注意事项 ===")
    
    # 最佳实践1: 生成器只能使用一次
    print("注意事项1: 生成器只能使用一次")
    
    gen = (x**2 for x in range(5))
    print(f"第一次遍历: {list(gen)}")
    print(f"第二次遍历: {list(gen)}")  # 空列表
    
    # 解决方案：重新创建或使用函数
    def create_generator():
        return (x**2 for x in range(5))
    
    print(f"重新创建生成器: {list(create_generator())}")
    
    # 最佳实践2: 合理使用生成器vs列表
    print("\n最佳实践2: 何时使用生成器vs列表")
    
    data = range(1000)
    
    # 场景1: 需要多次访问 - 使用列表
    squares_list = [x**2 for x in data]
    print(f"列表长度: {len(squares_list)}")
    print(f"列表切片: {squares_list[10:15]}")
    print(f"随机访问: {squares_list[500]}")
    
    # 场景2: 单次遍历，大数据集 - 使用生成器
    squares_gen = (x**2 for x in data)
    first_10 = [next(squares_gen) for _ in range(10)]
    print(f"生成器前10个: {first_10}")
    
    # 最佳实践3: 避免在生成器中使用可变对象
    print("\n最佳实践3: 避免闭包变量问题")
    
    # 问题示例
    multipliers = []
    for i in range(3):
        multipliers.append((x * i for x in range(3)))
    
    print("闭包问题结果:")
    for gen in multipliers:
        print(f"  {list(gen)}")  # 都是[0, 0, 0]
    
    # 正确做法
    def create_multiplier(factor):
        return (x * factor for x in range(3))
    
    multipliers_correct = [create_multiplier(i) for i in range(3)]
    print("正确做法结果:")
    for gen in multipliers_correct:
        print(f"  {list(gen)}")
    
    # 最佳实践4: 错误处理
    print("\n最佳实践4: 生成器中的错误处理")
    
    def safe_division_generator(numbers, divisor):
        for num in numbers:
            try:
                yield num / divisor
            except ZeroDivisionError:
                yield float('inf')
    
    numbers = [10, 20, 30, 40]
    safe_gen = safe_division_generator(numbers, 0)
    print(f"安全除法结果: {list(safe_gen)}")
    
    # 最佳实践5: 生成器链式操作的调试
    print("\n最佳实践5: 调试技巧")
    
    def debug_generator(gen, name):
        """调试生成器的包装器"""
        for item in gen:
            print(f"DEBUG {name}: {item}")
            yield item
    
    # 调试链式操作
    numbers = range(10)
    step1 = debug_generator((x for x in numbers if x % 2 == 0), "偶数过滤")
    step2 = debug_generator((x**2 for x in step1), "平方计算")
    
    print("调试输出:")
    result = list(step2)
    print(f"最终结果: {result}")
    
    print("\n最佳实践总结:")
    print("1. 生成器只能遍历一次，需要多次使用时重新创建")
    print("2. 大数据集或单次遍历使用生成器，需要随机访问使用列表")
    print("3. 注意闭包变量问题，使用函数封装避免")
    print("4. 在生成器内部处理异常，保证数据流稳定")
    print("5. 使用调试包装器帮助排查问题")
    print("6. 生成器适合数据管道、流处理等场景")
    
    print()


def main():
    """主函数：运行所有演示"""
    print("Python生成器表达式完整学习指南")
    print("=" * 50)
    
    demo_basic_syntax()
    demo_lazy_evaluation()
    demo_memory_efficiency()
    demo_conditional_generators()
    demo_chaining_operations()
    demo_practical_applications()
    demo_performance_comparison()
    demo_best_practices()
    
    print("学习总结:")
    print("1. 生成器表达式提供惰性求值，节省内存")
    print("2. 适合处理大数据集和无限数据流")
    print("3. 只能遍历一次，需要重复使用时重新创建")
    print("4. 性能优势在于内存效率和部分消费场景")
    print("5. Java Stream API提供类似的惰性求值特性")
    print("6. 最适合数据管道、流处理等应用场景")


if __name__ == "__main__":
    main() 