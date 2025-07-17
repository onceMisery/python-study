#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lambda函数详解 - Lambda Functions

本文件详细介绍Python Lambda函数的语法和应用，
包括与Java Lambda表达式的对比分析。

Lambda函数是Python函数式编程的重要组成部分，
提供了创建简短匿名函数的便捷方式。

Author: Python学习项目
Date: 2024-01-16
"""

import time
from functools import reduce, partial, wraps
from operator import add, mul, itemgetter, attrgetter
from typing import Callable, List, Any, Optional


def main():
    """Lambda函数示例主函数"""
    print("=== Python Lambda函数详解 ===\n")
    
    # 1. 基础Lambda语法
    basic_lambda_syntax()
    
    # 2. Lambda vs 普通函数
    lambda_vs_function()
    
    # 3. 与Java Lambda对比
    java_lambda_comparison()
    
    # 4. 常见使用场景
    common_use_cases()
    
    # 5. 高阶函数中的Lambda
    lambda_with_higher_order_functions()
    
    # 6. Lambda的局限性
    lambda_limitations()
    
    # 7. 函数式编程模式
    functional_programming_patterns()
    
    # 8. 实际应用示例
    practical_examples()
    
    # 9. 性能考虑
    performance_considerations()
    
    # 10. 最佳实践
    best_practices()


def basic_lambda_syntax():
    """基础Lambda语法"""
    print("1. 基础Lambda语法")
    print("-" * 40)
    
    # 基本语法：lambda 参数: 表达式
    
    # 示例1：简单计算
    square = lambda x: x ** 2
    print(f"平方函数: square(5) = {square(5)}")
    
    # 示例2：多个参数
    add_nums = lambda x, y: x + y
    print(f"加法函数: add_nums(3, 4) = {add_nums(3, 4)}")
    
    # 示例3：三个参数
    multiply_three = lambda x, y, z: x * y * z
    print(f"三数相乘: multiply_three(2, 3, 4) = {multiply_three(2, 3, 4)}")
    
    # 示例4：无参数Lambda
    get_greeting = lambda: "Hello, World!"
    print(f"问候函数: {get_greeting()}")
    
    # 示例5：条件表达式
    max_value = lambda x, y: x if x > y else y
    print(f"最大值函数: max_value(10, 15) = {max_value(10, 15)}")
    
    # 示例6：复杂表达式
    calculate = lambda x: x ** 2 + 2 * x + 1
    print(f"复杂计算: calculate(3) = {calculate(3)}")
    
    # 示例7：字符串操作
    format_name = lambda first, last: f"{first.title()} {last.title()}"
    print(f"格式化姓名: {format_name('john', 'doe')}")
    
    # 示例8：列表操作
    get_first = lambda lst: lst[0] if lst else None
    print(f"获取首元素: {get_first([1, 2, 3])}")
    print(f"空列表处理: {get_first([])}")
    
    print()


def lambda_vs_function():
    """Lambda vs 普通函数"""
    print("2. Lambda vs 普通函数")
    print("-" * 40)
    
    # 普通函数定义
    def normal_square(x):
        """计算平方的普通函数"""
        return x ** 2
    
    # Lambda函数定义
    lambda_square = lambda x: x ** 2
    
    print("功能比较:")
    print(f"  普通函数: normal_square(5) = {normal_square(5)}")
    print(f"  Lambda函数: lambda_square(5) = {lambda_square(5)}")
    
    # 特性对比
    print(f"\n特性对比:")
    print(f"  普通函数名称: {normal_square.__name__}")
    print(f"  Lambda函数名称: {lambda_square.__name__}")
    
    print(f"  普通函数文档: {normal_square.__doc__}")
    print(f"  Lambda函数文档: {lambda_square.__doc__}")
    
    # 性能对比
    print(f"\n性能对比 (100万次调用):")
    
    import time
    n = 1000000
    
    # 测试普通函数
    start = time.time()
    for _ in range(n):
        normal_square(5)
    normal_time = time.time() - start
    
    # 测试Lambda函数
    start = time.time()
    for _ in range(n):
        lambda_square(5)
    lambda_time = time.time() - start
    
    print(f"  普通函数: {normal_time:.4f}秒")
    print(f"  Lambda函数: {lambda_time:.4f}秒")
    print(f"  性能差异: {abs(normal_time - lambda_time) / min(normal_time, lambda_time) * 100:.1f}%")
    
    # 使用场景对比
    print(f"\n使用场景:")
    print("普通函数适用于:")
    print("  - 复杂逻辑实现")
    print("  - 需要文档字符串")
    print("  - 多次调用")
    print("  - 调试和测试")
    
    print("Lambda函数适用于:")
    print("  - 简单的一行表达式")
    print("  - 作为参数传递")
    print("  - 临时使用")
    print("  - 函数式编程")
    
    print()


def java_lambda_comparison():
    """与Java Lambda对比"""
    print("3. 与Java Lambda对比")
    print("-" * 40)
    
    # Python Lambda示例
    numbers = [1, 2, 3, 4, 5]
    
    # Python: 使用Lambda进行映射
    squares = list(map(lambda x: x ** 2, numbers))
    print("Python Lambda:")
    print(f"  numbers = {numbers}")
    print(f"  squares = list(map(lambda x: x ** 2, numbers))")
    print(f"  结果: {squares}")
    
    print("\nJava等价代码:")
    print("""
    // Java 8+ Lambda表达式
    List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
    
    List<Integer> squares = numbers.stream()
        .map(x -> x * x)
        .collect(Collectors.toList());
    """)
    
    # 筛选示例
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"\nPython筛选:")
    print(f"  even_numbers = list(filter(lambda x: x % 2 == 0, numbers))")
    print(f"  结果: {even_numbers}")
    
    print("\nJava等价代码:")
    print("""
    // Java 8+ 筛选
    List<Integer> evenNumbers = numbers.stream()
        .filter(x -> x % 2 == 0)
        .collect(Collectors.toList());
    """)
    
    # 聚合示例
    total = reduce(lambda x, y: x + y, numbers)
    print(f"\nPython聚合:")
    print(f"  total = reduce(lambda x, y: x + y, numbers)")
    print(f"  结果: {total}")
    
    print("\nJava等价代码:")
    print("""
    // Java 8+ 聚合
    int total = numbers.stream()
        .reduce(0, (x, y) -> x + y);
    """)
    
    # 语法特点对比
    print(f"\n语法特点对比:")
    
    print("Python Lambda:")
    print("  • 语法: lambda 参数: 表达式")
    print("  • 只能包含表达式，不能包含语句")
    print("  • 自动返回表达式结果")
    print("  • 可以直接赋值给变量")
    print("  • 支持默认参数和可变参数")
    
    print("\nJava Lambda:")
    print("  • 语法: (参数) -> 表达式 或 (参数) -> { 语句; }")
    print("  • 可以包含多条语句")
    print("  • 需要显式return（块形式）")
    print("  • 必须符合函数式接口")
    print("  • 强类型检查")
    
    # 函数接口对比
    print(f"\n函数接口使用:")
    
    # Python: 函数作为第一类对象
    def apply_operation(operation, x, y):
        return operation(x, y)
    
    result = apply_operation(lambda x, y: x + y, 10, 20)
    print(f"Python: apply_operation(lambda x, y: x + y, 10, 20) = {result}")
    
    print("\nJava等价代码:")
    print("""
    // Java 函数式接口
    @FunctionalInterface
    interface BinaryOperation {
        int apply(int x, int y);
    }
    
    public static int applyOperation(BinaryOperation op, int x, int y) {
        return op.apply(x, y);
    }
    
    // 使用
    int result = applyOperation((x, y) -> x + y, 10, 20);
    """)
    
    print()


def common_use_cases():
    """常见使用场景"""
    print("4. 常见使用场景")
    print("-" * 40)
    
    # 场景1：排序
    print("场景1：排序")
    
    students = [
        {'name': '张三', 'age': 20, 'score': 85},
        {'name': '李四', 'age': 19, 'score': 92},
        {'name': '王五', 'age': 21, 'score': 78},
        {'name': '赵六', 'age': 20, 'score': 95}
    ]
    
    # 按年龄排序
    by_age = sorted(students, key=lambda s: s['age'])
    print(f"  按年龄排序: {[s['name'] for s in by_age]}")
    
    # 按分数排序
    by_score = sorted(students, key=lambda s: s['score'], reverse=True)
    print(f"  按分数排序: {[s['name'] for s in by_score]}")
    
    # 复合排序：先按年龄，再按分数
    by_age_score = sorted(students, key=lambda s: (s['age'], s['score']))
    print(f"  按年龄和分数: {[(s['name'], s['age'], s['score']) for s in by_age_score]}")
    
    # 场景2：筛选
    print(f"\n场景2：筛选")
    
    numbers = list(range(1, 21))
    
    # 筛选偶数
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"  偶数: {evens}")
    
    # 筛选质数
    def is_prime(n):
        if n < 2:
            return False
        return all(n % i != 0 for i in range(2, int(n**0.5) + 1))
    
    primes = list(filter(lambda x: is_prime(x), numbers))
    print(f"  质数: {primes}")
    
    # 场景3：映射转换
    print(f"\n场景3：映射转换")
    
    words = ['hello', 'world', 'python', 'lambda']
    
    # 转换为大写
    upper_words = list(map(lambda w: w.upper(), words))
    print(f"  大写转换: {upper_words}")
    
    # 获取长度
    word_lengths = list(map(lambda w: len(w), words))
    print(f"  单词长度: {dict(zip(words, word_lengths))}")
    
    # 场景4：聚合计算
    print(f"\n场景4：聚合计算")
    
    numbers = [1, 2, 3, 4, 5]
    
    # 求和
    total = reduce(lambda x, y: x + y, numbers)
    print(f"  求和: {total}")
    
    # 求最大值
    maximum = reduce(lambda x, y: x if x > y else y, numbers)
    print(f"  最大值: {maximum}")
    
    # 连接字符串
    words = ['Python', 'is', 'awesome']
    sentence = reduce(lambda x, y: x + ' ' + y, words)
    print(f"  字符串连接: '{sentence}'")
    
    # 场景5：事件处理
    print(f"\n场景5：事件处理（模拟）")
    
    # 模拟按钮事件处理器
    def create_button_handler(action):
        return lambda: print(f"执行动作: {action}")
    
    # 创建多个处理器
    handlers = {
        'save': create_button_handler('保存文件'),
        'open': create_button_handler('打开文件'),
        'close': create_button_handler('关闭文件')
    }
    
    # 模拟事件触发
    print(f"  模拟按钮点击:")
    for action, handler in handlers.items():
        print(f"    {action}按钮: ", end='')
        handler()
    
    print()


def lambda_with_higher_order_functions():
    """高阶函数中的Lambda"""
    print("5. 高阶函数中的Lambda")
    print("-" * 40)
    
    # map函数
    print("map函数应用:")
    
    numbers = [1, 2, 3, 4, 5]
    
    # 平方映射
    squares = list(map(lambda x: x ** 2, numbers))
    print(f"  平方: {squares}")
    
    # 多个参数的map
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    sums = list(map(lambda x, y: x + y, list1, list2))
    print(f"  对应相加: {sums}")
    
    # filter函数
    print(f"\nfilter函数应用:")
    
    # 筛选条件
    data = range(1, 21)
    
    # 筛选大于10的数
    large_nums = list(filter(lambda x: x > 10, data))
    print(f"  大于10: {large_nums}")
    
    # 筛选能被3整除的数
    divisible_by_3 = list(filter(lambda x: x % 3 == 0, data))
    print(f"  能被3整除: {divisible_by_3}")
    
    # reduce函数
    print(f"\nreduce函数应用:")
    
    # 累积计算
    numbers = [1, 2, 3, 4, 5]
    
    # 累积乘法
    product = reduce(lambda x, y: x * y, numbers)
    print(f"  累积乘法: {product}")
    
    # 找最小值
    minimum = reduce(lambda x, y: x if x < y else y, numbers)
    print(f"  最小值: {minimum}")
    
    # sorted函数
    print(f"\nsorted函数应用:")
    
    # 复杂排序
    data = ['apple', 'Banana', 'cherry', 'Date']
    
    # 按长度排序
    by_length = sorted(data, key=lambda s: len(s))
    print(f"  按长度: {by_length}")
    
    # 忽略大小写排序
    case_insensitive = sorted(data, key=lambda s: s.lower())
    print(f"  忽略大小写: {case_insensitive}")
    
    # 自定义高阶函数
    print(f"\n自定义高阶函数:")
    
    def apply_twice(func, value):
        """应用函数两次"""
        return func(func(value))
    
    # 使用Lambda
    result = apply_twice(lambda x: x * 2, 5)
    print(f"  应用两次(乘2): apply_twice(lambda x: x * 2, 5) = {result}")
    
    result = apply_twice(lambda x: x + 3, 10)
    print(f"  应用两次(加3): apply_twice(lambda x: x + 3, 10) = {result}")
    
    # 函数组合器
    def compose(f, g):
        """函数组合"""
        return lambda x: f(g(x))
    
    # 组合函数
    add_then_square = compose(lambda x: x ** 2, lambda x: x + 1)
    result = add_then_square(5)
    print(f"  函数组合: (x+1)² where x=5 = {result}")
    
    print()


def lambda_limitations():
    """Lambda的局限性"""
    print("6. Lambda的局限性")
    print("-" * 40)
    
    # 局限性1：只能包含表达式
    print("局限性1：只能包含表达式，不能包含语句")
    
    # 这些不能在Lambda中使用：
    print("  不能使用的语句:")
    print("    - print语句")
    print("    - if语句（但可以用条件表达式）")
    print("    - for循环")
    print("    - try-except")
    print("    - with语句")
    print("    - def定义")
    
    # 可以使用条件表达式
    conditional_lambda = lambda x: "positive" if x > 0 else "non-positive"
    print(f"  条件表达式示例: {conditional_lambda(5)}, {conditional_lambda(-3)}")
    
    # 局限性2：调试困难
    print(f"\n局限性2：调试困难")
    
    def debug_function(x):
        """带调试信息的普通函数"""
        print(f"Debug: input is {x}")
        result = x ** 2
        print(f"Debug: result is {result}")
        return result
    
    debug_lambda = lambda x: x ** 2  # 难以调试
    
    print("  普通函数便于调试:")
    result = debug_function(5)
    
    print("  Lambda函数难以调试（无法添加print语句）")
    
    # 局限性3：可读性问题
    print(f"\n局限性3：复杂逻辑可读性差")
    
    # 过于复杂的Lambda
    complex_lambda = lambda x: x ** 2 + 2 * x + 1 if x > 0 else abs(x) * 2 if x < -10 else 0
    
    # 更好的普通函数版本
    def complex_function(x):
        """复杂逻辑的普通函数版本"""
        if x > 0:
            return x ** 2 + 2 * x + 1
        elif x < -10:
            return abs(x) * 2
        else:
            return 0
    
    print("  复杂Lambda（可读性差）:")
    print("    lambda x: x ** 2 + 2 * x + 1 if x > 0 else abs(x) * 2 if x < -10 else 0")
    
    print("  普通函数（可读性好）:")
    print("    def complex_function(x):")
    print("        if x > 0:")
    print("            return x ** 2 + 2 * x + 1")
    print("        elif x < -10:")
    print("            return abs(x) * 2")
    print("        else:")
    print("            return 0")
    
    # 局限性4：没有文档字符串
    print(f"\n局限性4：无法添加文档字符串")
    
    def documented_function(x):
        """
        计算数字的平方
        
        Args:
            x: 输入数字
            
        Returns:
            x的平方
        """
        return x ** 2
    
    undocumented_lambda = lambda x: x ** 2
    
    print(f"  普通函数文档: {documented_function.__doc__}")
    print(f"  Lambda函数文档: {undocumented_lambda.__doc__}")
    
    # 何时避免使用Lambda
    print(f"\n何时避免使用Lambda:")
    avoid_cases = [
        "复杂的逻辑（超过一行）",
        "需要调试的代码",
        "需要文档说明的函数",
        "多次重复使用的逻辑",
        "需要异常处理的场景",
        "团队代码规范不推荐的情况"
    ]
    
    for case in avoid_cases:
        print(f"  • {case}")
    
    print()


def functional_programming_patterns():
    """函数式编程模式"""
    print("7. 函数式编程模式")
    print("-" * 40)
    
    # 模式1：Currying（柯里化）
    print("模式1：Currying（柯里化）")
    
    # 普通多参数函数
    def add_three_params(x, y, z):
        return x + y + z
    
    # 柯里化版本
    def curried_add(x):
        return lambda y: lambda z: x + y + z
    
    # 使用柯里化
    add_5 = curried_add(5)
    add_5_10 = add_5(10)
    result = add_5_10(15)
    
    print(f"  普通函数: add_three_params(5, 10, 15) = {add_three_params(5, 10, 15)}")
    print(f"  柯里化: curried_add(5)(10)(15) = {curried_add(5)(10)(15)}")
    print(f"  部分应用: add_5_10(15) = {result}")
    
    # 模式2：偏函数应用
    print(f"\n模式2：偏函数应用")
    
    # 使用functools.partial
    multiply = lambda x, y, z: x * y * z
    
    # 创建偏函数
    double = partial(multiply, 2)  # 固定第一个参数为2
    triple = partial(multiply, 3)  # 固定第一个参数为3
    
    print(f"  原函数: multiply(2, 3, 4) = {multiply(2, 3, 4)}")
    print(f"  偏函数: double(3, 4) = {double(3, 4)}")
    print(f"  偏函数: triple(3, 4) = {triple(3, 4)}")
    
    # 模式3：函数组合
    print(f"\n模式3：函数组合")
    
    # 简单函数
    add_one = lambda x: x + 1
    multiply_by_two = lambda x: x * 2
    square = lambda x: x ** 2
    
    # 函数组合器
    def compose(*functions):
        """组合多个函数"""
        return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)
    
    # 组合函数
    complex_operation = compose(square, multiply_by_two, add_one)
    
    print(f"  单独操作: add_one(5) = {add_one(5)}")
    print(f"  单独操作: multiply_by_two(6) = {multiply_by_two(6)}")
    print(f"  单独操作: square(12) = {square(12)}")
    print(f"  组合操作: square(multiply_by_two(add_one(5))) = {complex_operation(5)}")
    
    # 模式4：闭包
    print(f"\n模式4：闭包")
    
    def create_multiplier(factor):
        """创建乘法器闭包"""
        return lambda x: x * factor
    
    # 创建不同的乘法器
    double_func = create_multiplier(2)
    triple_func = create_multiplier(3)
    
    print(f"  闭包乘法器: double_func(10) = {double_func(10)}")
    print(f"  闭包乘法器: triple_func(10) = {triple_func(10)}")
    
    # 带状态的闭包
    def create_counter():
        """创建计数器闭包"""
        count = 0
        def counter():
            nonlocal count
            count += 1
            return count
        return counter
    
    counter1 = create_counter()
    counter2 = create_counter()
    
    print(f"  计数器1: {counter1()}, {counter1()}, {counter1()}")
    print(f"  计数器2: {counter2()}, {counter2()}")
    
    # 模式5：高阶函数
    print(f"\n模式5：高阶函数")
    
    def apply_to_all(func, items):
        """对所有元素应用函数"""
        return [func(item) for item in items]
    
    def filter_and_map(predicate, transformer, items):
        """筛选并转换"""
        return [transformer(item) for item in items if predicate(item)]
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 使用高阶函数
    squares = apply_to_all(lambda x: x ** 2, numbers)
    even_squares = filter_and_map(
        lambda x: x % 2 == 0,  # 偶数筛选
        lambda x: x ** 2,      # 平方转换
        numbers
    )
    
    print(f"  所有平方: {squares}")
    print(f"  偶数平方: {even_squares}")
    
    print()


def practical_examples():
    """实际应用示例"""
    print("8. 实际应用示例")
    print("-" * 40)
    
    # 示例1：数据处理管道
    print("示例1：数据处理管道")
    
    # 销售数据
    sales_data = [
        {'product': 'iPhone', 'price': 999, 'quantity': 100, 'region': 'North'},
        {'product': 'iPad', 'price': 599, 'quantity': 150, 'region': 'South'},
        {'product': 'MacBook', 'price': 1299, 'quantity': 80, 'region': 'North'},
        {'product': 'iPhone', 'price': 999, 'quantity': 120, 'region': 'South'},
        {'product': 'iPad', 'price': 599, 'quantity': 90, 'region': 'North'}
    ]
    
    # 数据处理管道
    # 1. 计算总销售额
    sales_with_total = list(map(
        lambda item: {**item, 'total': item['price'] * item['quantity']},
        sales_data
    ))
    
    # 2. 筛选高价值销售（总额>50000）
    high_value_sales = list(filter(
        lambda item: item['total'] > 50000,
        sales_with_total
    ))
    
    # 3. 按总销售额排序
    sorted_sales = sorted(
        high_value_sales,
        key=lambda item: item['total'],
        reverse=True
    )
    
    print(f"  高价值销售（按总额排序）:")
    for sale in sorted_sales:
        print(f"    {sale['product']}: ${sale['total']:,}")
    
    # 示例2：配置处理
    print(f"\n示例2：配置处理")
    
    # 原始配置
    config = {
        'database_host': 'localhost',
        'database_port': '5432',
        'max_connections': '100',
        'timeout': '30',
        'debug': 'true'
    }
    
    # 类型转换器
    converters = {
        'port': lambda x: int(x),
        'connections': lambda x: int(x),
        'timeout': lambda x: int(x),
        'debug': lambda x: x.lower() == 'true'
    }
    
    # 处理配置
    processed_config = {}
    for key, value in config.items():
        # 查找对应的转换器
        converter_key = next((k for k in converters if k in key), None)
        if converter_key:
            processed_config[key] = converters[converter_key](value)
        else:
            processed_config[key] = value
    
    print(f"  原始配置: {config}")
    print(f"  处理后配置: {processed_config}")
    
    # 示例3：事件处理系统
    print(f"\n示例3：事件处理系统")
    
    # 事件处理器注册表
    event_handlers = {}
    
    def register_handler(event_type, handler):
        """注册事件处理器"""
        if event_type not in event_handlers:
            event_handlers[event_type] = []
        event_handlers[event_type].append(handler)
    
    def trigger_event(event_type, data):
        """触发事件"""
        if event_type in event_handlers:
            for handler in event_handlers[event_type]:
                handler(data)
    
    # 注册处理器（使用Lambda）
    register_handler('user_login', lambda data: print(f"用户登录: {data['username']}"))
    register_handler('user_logout', lambda data: print(f"用户登出: {data['username']}"))
    register_handler('error', lambda data: print(f"错误: {data['message']}"))
    
    # 触发事件
    print(f"  事件触发:")
    trigger_event('user_login', {'username': 'john_doe'})
    trigger_event('user_logout', {'username': 'john_doe'})
    trigger_event('error', {'message': '数据库连接失败'})
    
    # 示例4：动态计算器
    print(f"\n示例4：动态计算器")
    
    # 操作映射
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else float('inf'),
        '**': lambda x, y: x ** y,
        '%': lambda x, y: x % y if y != 0 else 0
    }
    
    def calculate(expression):
        """计算表达式"""
        try:
            # 简单解析（仅支持两个操作数）
            for op in operations:
                if op in expression:
                    parts = expression.split(op)
                    if len(parts) == 2:
                        x = float(parts[0].strip())
                        y = float(parts[1].strip())
                        return operations[op](x, y)
            return "无效表达式"
        except Exception as e:
            return f"错误: {e}"
    
    # 测试计算器
    expressions = ['10 + 5', '20 - 8', '6 * 7', '15 / 3', '2 ** 3']
    print(f"  动态计算:")
    for expr in expressions:
        result = calculate(expr)
        print(f"    {expr} = {result}")
    
    print()


def performance_considerations():
    """性能考虑"""
    print("9. 性能考虑")
    print("-" * 40)
    
    # 性能测试设置
    n = 100000
    
    # 测试1：Lambda vs 普通函数
    print("测试1：Lambda vs 普通函数性能")
    
    def normal_func(x):
        return x * 2
    
    lambda_func = lambda x: x * 2
    
    # 测试普通函数
    start = time.time()
    for i in range(n):
        normal_func(i)
    normal_time = time.time() - start
    
    # 测试Lambda函数
    start = time.time()
    for i in range(n):
        lambda_func(i)
    lambda_time = time.time() - start
    
    print(f"  普通函数 ({n:,}次): {normal_time:.4f}秒")
    print(f"  Lambda函数 ({n:,}次): {lambda_time:.4f}秒")
    print(f"  性能差异: {abs(normal_time - lambda_time) / min(normal_time, lambda_time) * 100:.1f}%")
    
    # 测试2：内置函数 vs Lambda
    print(f"\n测试2：内置函数 vs Lambda性能")
    
    data = list(range(1000))
    
    # 使用内置operator模块
    from operator import mul
    
    # 测试Lambda
    start = time.time()
    result1 = list(map(lambda x: x * 2, data))
    lambda_map_time = time.time() - start
    
    # 测试operator
    start = time.time()
    result2 = list(map(partial(mul, 2), data))
    operator_time = time.time() - start
    
    print(f"  Lambda map: {lambda_map_time:.4f}秒")
    print(f"  Operator map: {operator_time:.4f}秒")
    print(f"  内置函数快: {lambda_map_time / operator_time:.2f}倍")
    
    # 测试3：复杂Lambda vs 简单函数
    print(f"\n测试3：复杂表达式性能影响")
    
    # 简单Lambda
    simple_lambda = lambda x: x + 1
    
    # 复杂Lambda
    complex_lambda = lambda x: x ** 2 + 2 * x + 1 if x > 0 else abs(x)
    
    # 测试简单Lambda
    start = time.time()
    for i in range(n):
        simple_lambda(i)
    simple_time = time.time() - start
    
    # 测试复杂Lambda
    start = time.time()
    for i in range(n):
        complex_lambda(i)
    complex_time = time.time() - start
    
    print(f"  简单Lambda: {simple_time:.4f}秒")
    print(f"  复杂Lambda: {complex_time:.4f}秒")
    print(f"  复杂度影响: {complex_time / simple_time:.2f}倍")
    
    # 性能优化建议
    print(f"\n性能优化建议:")
    tips = [
        "对于简单操作，Lambda和普通函数性能相近",
        "频繁调用的Lambda考虑提取为普通函数",
        "使用operator模块代替简单Lambda操作",
        "避免在Lambda中进行复杂计算",
        "大数据处理时考虑使用生成器",
        "适当使用缓存避免重复计算"
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"  {i}. {tip}")
    
    print()


def best_practices():
    """最佳实践"""
    print("10. 最佳实践")
    print("-" * 40)
    
    # 实践1：保持简洁
    print("实践1：保持简洁")
    
    # 好的Lambda使用
    good_examples = [
        ("排序", "sorted(students, key=lambda s: s['score'])"),
        ("筛选", "filter(lambda x: x > 0, numbers)"),
        ("映射", "map(lambda x: x.upper(), words)"),
        ("聚合", "reduce(lambda x, y: x + y, numbers)")
    ]
    
    print("  好的使用示例:")
    for name, code in good_examples:
        print(f"    {name}: {code}")
    
    # 避免的Lambda使用
    print(f"\n  避免的复杂Lambda:")
    bad_example = """lambda x: x ** 2 + 2 * x + 1 if x > 0 else (
    abs(x) * 2 if x < -10 else 0
)"""
    print(f"    复杂逻辑: {bad_example}")
    
    # 实践2：有意义的上下文
    print(f"\n实践2：在有意义的上下文中使用")
    
    # 好的上下文
    print("  适合的上下文:")
    contexts = [
        "高阶函数参数 (map, filter, reduce)",
        "排序键函数 (sorted, list.sort)",
        "事件处理器",
        "配置和设置",
        "函数式编程模式"
    ]
    
    for context in contexts:
        print(f"    • {context}")
    
    # 实践3：类型注解
    print(f"\n实践3：使用类型注解（推荐）")
    
    # 带类型注解的Lambda使用
    from typing import Callable
    
    def process_numbers(
        numbers: List[int], 
        processor: Callable[[int], int]
    ) -> List[int]:
        """处理数字列表"""
        return [processor(num) for num in numbers]
    
    # 使用
    result = process_numbers([1, 2, 3, 4, 5], lambda x: x ** 2)
    print(f"  类型化处理: {result}")
    
    # 实践4：错误处理
    print(f"\n实践4：考虑错误处理")
    
    # 安全的Lambda使用
    def safe_divide(x, y):
        return x / y if y != 0 else 0
    
    # 在Lambda中使用安全函数
    numbers = [10, 20, 30]
    divisors = [2, 0, 5]  # 包含0
    
    safe_results = list(map(lambda pair: safe_divide(*pair), zip(numbers, divisors)))
    print(f"  安全除法: {safe_results}")
    
    # 实践5：文档化
    print(f"\n实践5：文档化复杂Lambda")
    
    # 使用注释说明复杂Lambda
    data = [
        {'name': 'Alice', 'scores': [85, 90, 92]},
        {'name': 'Bob', 'scores': [78, 85, 88]},
        {'name': 'Charlie', 'scores': [92, 95, 98]}
    ]
    
    # 计算平均分并排序
    sorted_by_avg = sorted(
        data,
        key=lambda student: sum(student['scores']) / len(student['scores']),  # 平均分
        reverse=True
    )
    
    print(f"  按平均分排序:")
    for student in sorted_by_avg:
        avg = sum(student['scores']) / len(student['scores'])
        print(f"    {student['name']}: {avg:.1f}")
    
    # 最佳实践总结
    print(f"\n最佳实践总结:")
    practices = [
        "1. 保持Lambda简洁（一行表达式）",
        "2. 避免复杂逻辑，提取为普通函数",
        "3. 使用有意义的变量名",
        "4. 在合适的上下文中使用",
        "5. 考虑使用operator模块替代简单操作",
        "6. 添加类型注解提高可读性",
        "7. 注意错误处理",
        "8. 适当添加注释说明",
        "9. 考虑代码可维护性",
        "10. 遵循团队编码规范"
    ]
    
    for practice in practices:
        print(f"  {practice}")
    
    print()


if __name__ == '__main__':
    main() 