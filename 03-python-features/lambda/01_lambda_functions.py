#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python Lambda函数详解
Lambda Functions in Python

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习Python Lambda函数的语法、应用场景和与Java Lambda表达式的对比

学习目标:
1. 掌握Lambda函数的基本语法
2. 理解Lambda函数的应用场景
3. 学会函数式编程的思维方式
4. 对比Java Lambda表达式的使用
"""

import time
import random
from typing import Callable, List, Any, Tuple
from functools import reduce, partial
import operator


def demo_basic_syntax():
    """演示Lambda函数的基本语法"""
    print("=== 1. 基本语法演示 ===")
    
    # 基础语法: lambda arguments: expression
    
    # 普通函数定义
    def add_normal(x, y):
        return x + y
    
    # Lambda函数定义
    add_lambda = lambda x, y: x + y
    
    print("函数对比:")
    print(f"普通函数: add_normal(3, 5) = {add_normal(3, 5)}")
    print(f"Lambda函数: add_lambda(3, 5) = {add_lambda(3, 5)}")
    
    # 单参数Lambda
    square = lambda x: x**2
    print(f"平方函数: square(4) = {square(4)}")
    
    # 无参数Lambda
    get_pi = lambda: 3.14159
    print(f"常量函数: get_pi() = {get_pi()}")
    
    # 多参数Lambda
    multiply = lambda a, b, c: a * b * c
    print(f"三数相乘: multiply(2, 3, 4) = {multiply(2, 3, 4)}")
    
    # 条件表达式Lambda
    max_two = lambda a, b: a if a > b else b
    print(f"两数最大值: max_two(5, 8) = {max_two(5, 8)}")
    
    # Lambda函数的类型
    print(f"\nLambda函数类型: {type(add_lambda)}")
    print(f"Lambda函数名称: {add_lambda.__name__}")
    
    """
    Java等价实现:
    // 普通方法
    public static int addNormal(int x, int y) {
        return x + y;
    }
    
    // Lambda表达式
    BinaryOperator<Integer> addLambda = (x, y) -> x + y;
    Function<Integer, Integer> square = x -> x * x;
    Supplier<Double> getPi = () -> 3.14159;
    
    // 三参数Lambda
    @FunctionalInterface
    interface TriFunction<T, U, V, R> {
        R apply(T t, U u, V v);
    }
    TriFunction<Integer, Integer, Integer, Integer> multiply = (a, b, c) -> a * b * c;
    
    // 条件表达式
    BinaryOperator<Integer> maxTwo = (a, b) -> a > b ? a : b;
    """
    
    print()


def demo_lambda_with_builtin_functions():
    """演示Lambda与内置函数的结合使用"""
    print("=== 2. Lambda与内置函数结合 ===")
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # map() 函数 - 映射转换
    print("map() 函数:")
    squares = list(map(lambda x: x**2, numbers))
    print(f"原数组: {numbers}")
    print(f"平方后: {squares}")
    
    # 字符串转换
    words = ["hello", "world", "python", "lambda"]
    upper_words = list(map(lambda s: s.upper(), words))
    print(f"单词: {words}")
    print(f"大写: {upper_words}")
    
    # filter() 函数 - 过滤筛选
    print("\nfilter() 函数:")
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"偶数: {evens}")
    
    # 字符串过滤
    long_words = list(filter(lambda s: len(s) > 5, words))
    print(f"长单词: {long_words}")
    
    # reduce() 函数 - 归约计算
    print("\nreduce() 函数:")
    sum_all = reduce(lambda x, y: x + y, numbers)
    print(f"数组求和: {sum_all}")
    
    product_all = reduce(lambda x, y: x * y, numbers)
    print(f"数组求积: {product_all}")
    
    # 找最大值
    max_value = reduce(lambda x, y: x if x > y else y, numbers)
    print(f"最大值: {max_value}")
    
    # sorted() 函数 - 排序
    print("\nsorted() 函数:")
    
    # 按长度排序
    sorted_by_length = sorted(words, key=lambda s: len(s))
    print(f"按长度排序: {sorted_by_length}")
    
    # 按最后一个字符排序
    sorted_by_last_char = sorted(words, key=lambda s: s[-1])
    print(f"按最后字符排序: {sorted_by_last_char}")
    
    # 复杂对象排序
    students = [
        {"name": "Alice", "score": 85, "age": 20},
        {"name": "Bob", "score": 92, "age": 19},
        {"name": "Charlie", "score": 78, "age": 21},
        {"name": "Diana", "score": 96, "age": 20}
    ]
    
    # 按成绩排序
    sorted_by_score = sorted(students, key=lambda s: s["score"], reverse=True)
    print(f"\n按成绩排序:")
    for student in sorted_by_score:
        print(f"  {student['name']}: {student['score']}")
    
    # 多级排序：先按年龄，再按成绩
    sorted_multi = sorted(students, key=lambda s: (s["age"], -s["score"]))
    print(f"\n按年龄-成绩排序:")
    for student in sorted_multi:
        print(f"  {student['name']}: 年龄{student['age']}, 成绩{student['score']}")
    
    """
    Java等价实现:
    List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
    
    // map操作
    List<Integer> squares = numbers.stream()
                                  .map(x -> x * x)
                                  .collect(Collectors.toList());
    
    // filter操作
    List<Integer> evens = numbers.stream()
                                .filter(x -> x % 2 == 0)
                                .collect(Collectors.toList());
    
    // reduce操作
    int sum = numbers.stream()
                    .reduce(0, (x, y) -> x + y);
    
    Optional<Integer> max = numbers.stream()
                                  .reduce((x, y) -> x > y ? x : y);
    
    // sorted操作
    List<String> words = Arrays.asList("hello", "world", "python", "lambda");
    List<String> sortedByLength = words.stream()
                                      .sorted(Comparator.comparing(String::length))
                                      .collect(Collectors.toList());
    
    // 复杂对象排序
    List<Student> sortedStudents = students.stream()
                                          .sorted(Comparator.comparing(Student::getScore).reversed())
                                          .collect(Collectors.toList());
    """
    
    print()


def demo_lambda_in_data_processing():
    """演示Lambda在数据处理中的应用"""
    print("=== 3. 数据处理应用 ===")
    
    # 数据清洗和转换
    raw_data = [
        "  Alice, 25, Engineer  ",
        "Bob,30,Manager",
        "  Charlie, 35, Designer",
        "Diana,28,Developer  "
    ]
    
    print("数据清洗管道:")
    
    # 步骤1: 清理空白字符
    cleaned = list(map(lambda s: s.strip(), raw_data))
    print(f"清理空白: {cleaned}")
    
    # 步骤2: 分割字段
    split_data = list(map(lambda s: s.split(','), cleaned))
    print(f"分割字段: {split_data}")
    
    # 步骤3: 进一步清理每个字段
    cleaned_fields = list(map(lambda fields: [field.strip() for field in fields], split_data))
    print(f"清理字段: {cleaned_fields}")
    
    # 步骤4: 转换为字典
    person_dicts = list(map(
        lambda fields: {
            "name": fields[0],
            "age": int(fields[1]),
            "job": fields[2]
        },
        cleaned_fields
    ))
    
    print("转换为字典:")
    for person in person_dicts:
        print(f"  {person}")
    
    # 数据分析
    print("\n数据分析:")
    
    # 筛选年龄大于30的员工
    senior_employees = list(filter(lambda p: p["age"] > 30, person_dicts))
    print(f"资深员工: {[p['name'] for p in senior_employees]}")
    
    # 计算平均年龄
    total_age = reduce(lambda sum_age, person: sum_age + person["age"], person_dicts, 0)
    avg_age = total_age / len(person_dicts)
    print(f"平均年龄: {avg_age:.1f}")
    
    # 按职位分组
    jobs = set(map(lambda p: p["job"], person_dicts))
    job_groups = {
        job: list(filter(lambda p: p["job"] == job, person_dicts))
        for job in jobs
    }
    
    print("按职位分组:")
    for job, people in job_groups.items():
        names = list(map(lambda p: p["name"], people))
        print(f"  {job}: {names}")
    
    # 销售数据处理示例
    print("\n销售数据处理:")
    
    sales_data = [
        {"product": "iPhone", "quantity": 100, "price": 999},
        {"product": "iPad", "quantity": 50, "price": 599},
        {"product": "MacBook", "quantity": 30, "price": 1299},
        {"product": "AirPods", "quantity": 200, "price": 199}
    ]
    
    # 计算总收入
    revenues = list(map(lambda item: item["quantity"] * item["price"], sales_data))
    total_revenue = reduce(lambda x, y: x + y, revenues)
    
    print(f"各产品收入: {revenues}")
    print(f"总收入: ${total_revenue:,}")
    
    # 找出高价值产品（单价>500）
    high_value = list(filter(lambda item: item["price"] > 500, sales_data))
    high_value_names = list(map(lambda item: item["product"], high_value))
    print(f"高价值产品: {high_value_names}")
    
    # 按收入排序
    sorted_by_revenue = sorted(
        sales_data,
        key=lambda item: item["quantity"] * item["price"],
        reverse=True
    )
    
    print("按收入排序:")
    for item in sorted_by_revenue:
        revenue = item["quantity"] * item["price"]
        print(f"  {item['product']}: ${revenue:,}")
    
    """
    Java数据处理等价实现:
    // 数据清洗
    List<String> cleaned = rawData.stream()
                                 .map(String::trim)
                                 .collect(Collectors.toList());
    
    List<String[]> splitData = cleaned.stream()
                                     .map(s -> s.split(","))
                                     .collect(Collectors.toList());
    
    // 转换为对象
    List<Person> persons = splitData.stream()
                                   .map(fields -> new Person(
                                       fields[0].trim(),
                                       Integer.parseInt(fields[1].trim()),
                                       fields[2].trim()
                                   ))
                                   .collect(Collectors.toList());
    
    // 数据分析
    List<Person> seniorEmployees = persons.stream()
                                         .filter(p -> p.getAge() > 30)
                                         .collect(Collectors.toList());
    
    double avgAge = persons.stream()
                          .mapToInt(Person::getAge)
                          .average()
                          .orElse(0.0);
    
    // 分组
    Map<String, List<Person>> jobGroups = persons.stream()
                                                .collect(Collectors.groupingBy(Person::getJob));
    """
    
    print()


def demo_lambda_with_functional_programming():
    """演示Lambda与函数式编程模式"""
    print("=== 4. 函数式编程模式 ===")
    
    # 高阶函数：接受函数作为参数的函数
    def apply_operation(numbers: List[int], operation: Callable[[int], int]) -> List[int]:
        """对数组中每个元素应用操作"""
        return [operation(x) for x in numbers]
    
    def filter_and_transform(data: List[int], predicate: Callable[[int], bool], 
                           transformer: Callable[[int], int]) -> List[int]:
        """先过滤再转换"""
        return [transformer(x) for x in data if predicate(x)]
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("高阶函数应用:")
    
    # 应用不同的操作
    squares = apply_operation(numbers, lambda x: x**2)
    cubes = apply_operation(numbers, lambda x: x**3)
    doubled = apply_operation(numbers, lambda x: x * 2)
    
    print(f"原数组: {numbers}")
    print(f"平方: {squares}")
    print(f"立方: {cubes}")
    print(f"翻倍: {doubled}")
    
    # 组合操作
    even_squares = filter_and_transform(
        numbers,
        lambda x: x % 2 == 0,  # 筛选偶数
        lambda x: x**2         # 计算平方
    )
    print(f"偶数平方: {even_squares}")
    
    # 函数组合
    print("\n函数组合:")
    
    def compose(f, g):
        """函数组合：compose(f, g)(x) = f(g(x))"""
        return lambda x: f(g(x))
    
    # 创建组合函数
    square_then_double = compose(lambda x: x * 2, lambda x: x**2)
    double_then_square = compose(lambda x: x**2, lambda x: x * 2)
    
    x = 3
    print(f"x = {x}")
    print(f"先平方再翻倍: {square_then_double(x)}")  # (3^2) * 2 = 18
    print(f"先翻倍再平方: {double_then_square(x)}")  # (3 * 2)^2 = 36
    
    # 偏函数应用
    print("\n偏函数应用:")
    
    # 使用functools.partial
    multiply = lambda x, y: x * y
    double_partial = partial(multiply, 2)  # 固定第一个参数为2
    triple_partial = partial(multiply, 3)  # 固定第一个参数为3
    
    test_numbers = [1, 2, 3, 4, 5]
    doubled_list = list(map(double_partial, test_numbers))
    tripled_list = list(map(triple_partial, test_numbers))
    
    print(f"原数组: {test_numbers}")
    print(f"翻倍: {doubled_list}")
    print(f"三倍: {tripled_list}")
    
    # 柯里化（Currying）
    print("\n柯里化:")
    
    def curry_add(x):
        """柯里化的加法函数"""
        return lambda y: x + y
    
    add_5 = curry_add(5)  # 创建一个"加5"的函数
    add_10 = curry_add(10)  # 创建一个"加10"的函数
    
    print(f"add_5(3) = {add_5(3)}")
    print(f"add_10(7) = {add_10(7)}")
    
    # 应用到数组
    plus_5_list = list(map(add_5, test_numbers))
    print(f"数组加5: {plus_5_list}")
    
    # 函数流水线
    print("\n函数流水线:")
    
    def pipeline(*functions):
        """创建函数流水线"""
        return lambda x: reduce(lambda acc, func: func(acc), functions, x)
    
    # 创建数据处理流水线
    process_pipeline = pipeline(
        lambda x: x * 2,      # 翻倍
        lambda x: x + 1,      # 加1
        lambda x: x**2        # 平方
    )
    
    input_value = 3
    result = process_pipeline(input_value)
    print(f"流水线处理 {input_value}: 翻倍->加1->平方 = {result}")
    # ((3 * 2) + 1)^2 = 7^2 = 49
    
    """
    Java函数式编程等价实现:
    // 高阶函数
    public static <T, R> List<R> applyOperation(List<T> list, Function<T, R> operation) {
        return list.stream()
                  .map(operation)
                  .collect(Collectors.toList());
    }
    
    // 函数组合
    Function<Integer, Integer> squareThenDouble = 
        ((Function<Integer, Integer>) x -> x * x).andThen(x -> x * 2);
    
    Function<Integer, Integer> doubleThenSquare = 
        ((Function<Integer, Integer>) x -> x * 2).andThen(x -> x * x);
    
    // 柯里化
    Function<Integer, Function<Integer, Integer>> curryAdd = 
        x -> y -> x + y;
    
    Function<Integer, Integer> add5 = curryAdd.apply(5);
    
    // 流水线
    Function<Integer, Integer> pipeline = 
        ((Function<Integer, Integer>) x -> x * 2)
            .andThen(x -> x + 1)
            .andThen(x -> x * x);
    """
    
    print()


def demo_lambda_limitations_and_alternatives():
    """演示Lambda的限制和替代方案"""
    print("=== 5. Lambda限制和替代方案 ===")
    
    print("Lambda函数的限制:")
    
    # 限制1: 只能包含表达式，不能包含语句
    print("1. 只能包含表达式")
    
    # 这是可以的
    simple_lambda = lambda x: x * 2 if x > 0 else 0
    print(f"简单条件表达式: {simple_lambda(5)}")
    
    # 这是不可以的（会报语法错误）
    # complex_lambda = lambda x: 
    #     if x > 0:
    #         return x * 2
    #     else:
    #         return 0
    
    print("复杂逻辑需要使用普通函数:")
    
    def complex_function(x):
        if x > 10:
            result = x * 2
            print(f"大数处理: {x} -> {result}")
            return result
        elif x > 0:
            result = x + 1
            print(f"小数处理: {x} -> {result}")
            return result
        else:
            print(f"零或负数: {x}")
            return 0
    
    test_values = [-1, 5, 15]
    for val in test_values:
        result = complex_function(val)
        print(f"  complex_function({val}) = {result}")
    
    # 限制2: 可读性问题
    print("\n2. 复杂Lambda的可读性问题")
    
    # 不好的例子：过于复杂的Lambda
    complex_lambda_bad = lambda x: x**2 if x % 2 == 0 else x**3 if x % 3 == 0 else x + 1 if x > 5 else x - 1
    
    # 更好的替代方案
    def readable_function(x):
        """清晰可读的函数版本"""
        if x % 2 == 0:
            return x**2  # 偶数返回平方
        elif x % 3 == 0:
            return x**3  # 三的倍数返回立方
        elif x > 5:
            return x + 1  # 大于5的数加1
        else:
            return x - 1  # 其他情况减1
    
    test_numbers = [2, 3, 6, 7, 4]
    print("复杂逻辑对比:")
    for num in test_numbers:
        lambda_result = complex_lambda_bad(num)
        function_result = readable_function(num)
        print(f"  {num}: Lambda={lambda_result}, Function={function_result}")
    
    # 限制3: 调试困难
    print("\n3. 调试困难")
    
    # Lambda函数在错误信息中显示为 <lambda>
    try:
        problematic_lambda = lambda x: 10 / (x - 5)
        result = problematic_lambda(5)  # 会触发除零错误
    except ZeroDivisionError as e:
        print(f"Lambda错误（难以定位）: {e}")
    
    # 普通函数有明确的函数名
    def clear_division(x):
        """有明确名称的除法函数"""
        return 10 / (x - 5)
    
    try:
        result = clear_division(5)
    except ZeroDivisionError as e:
        print(f"函数错误（容易定位）: {e}")
    
    # 最佳实践建议
    print("\n最佳实践建议:")
    
    guidelines = [
        "1. 简单操作使用Lambda：map、filter、sort的key函数",
        "2. 复杂逻辑使用普通函数，提高可读性",
        "3. 需要文档说明的功能使用普通函数",
        "4. 调试时将Lambda替换为普通函数",
        "5. 团队协作中优先考虑代码可读性"
    ]
    
    for guideline in guidelines:
        print(f"  {guideline}")
    
    # 适合使用Lambda的场景
    print("\n适合使用Lambda的场景:")
    
    # 场景1: 简单的映射操作
    numbers = [1, 2, 3, 4, 5]
    squares = list(map(lambda x: x**2, numbers))
    print(f"简单映射: {squares}")
    
    # 场景2: 简单的过滤条件
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"简单过滤: {evens}")
    
    # 场景3: 简单的排序键
    words = ["apple", "pie", "a", "banana"]
    sorted_by_length = sorted(words, key=lambda s: len(s))
    print(f"按长度排序: {sorted_by_length}")
    
    # 场景4: 简单的事件处理（模拟）
    def simulate_button_click(callback):
        """模拟按钮点击事件"""
        print("按钮被点击了!")
        callback()
    
    # 使用Lambda作为回调
    simulate_button_click(lambda: print("Lambda回调被执行!"))
    
    """
    Java Lambda使用建议:
    // 适合的场景
    List<Integer> squares = numbers.stream()
                                  .map(x -> x * x)  // 简单映射
                                  .collect(Collectors.toList());
    
    List<String> sortedByLength = words.stream()
                                      .sorted(Comparator.comparing(s -> s.length()))  // 简单比较
                                      .collect(Collectors.toList());
    
    // 复杂逻辑应该提取为方法
    List<Integer> processed = numbers.stream()
                                    .map(this::complexProcessing)  // 方法引用
                                    .collect(Collectors.toList());
    
    private int complexProcessing(int x) {
        // 复杂逻辑
        if (x % 2 == 0) {
            return x * x;
        } else if (x % 3 == 0) {
            return x * x * x;
        } else {
            return x + 1;
        }
    }
    """
    
    print()


def demo_performance_considerations():
    """演示Lambda的性能考虑"""
    print("=== 6. 性能考虑 ===")
    
    # 性能测试数据
    test_data = list(range(100000))
    
    def measure_time(func, description):
        start_time = time.time()
        result = func()
        end_time = time.time()
        print(f"{description}: {end_time - start_time:.4f}秒")
        return result
    
    print("性能对比测试 (100,000个元素):")
    
    # 1. Lambda vs 普通函数
    def square_function(x):
        return x * x
    
    lambda_result = measure_time(
        lambda: list(map(lambda x: x * x, test_data)),
        "Lambda函数"
    )
    
    function_result = measure_time(
        lambda: list(map(square_function, test_data)),
        "普通函数"
    )
    
    builtin_result = measure_time(
        lambda: [x * x for x in test_data],
        "列表推导式"
    )
    
    # 验证结果一致性
    print(f"结果一致性: {lambda_result == function_result == builtin_result}")
    
    # 2. 复杂Lambda vs 函数
    print("\n复杂操作性能对比:")
    
    complex_lambda = lambda x: x**2 if x % 2 == 0 else x**3 if x % 3 == 0 else x + 1
    
    def complex_function(x):
        if x % 2 == 0:
            return x**2
        elif x % 3 == 0:
            return x**3
        else:
            return x + 1
    
    complex_lambda_result = measure_time(
        lambda: list(map(complex_lambda, test_data[:10000])),  # 减少数据量
        "复杂Lambda"
    )
    
    complex_function_result = measure_time(
        lambda: list(map(complex_function, test_data[:10000])),
        "复杂函数"
    )
    
    # 3. 内存使用对比
    print("\n内存使用对比:")
    
    import sys
    
    # Lambda对象大小
    simple_lambda = lambda x: x * 2
    print(f"Lambda对象大小: {sys.getsizeof(simple_lambda)} bytes")
    
    # 普通函数对象大小
    def simple_function(x):
        return x * 2
    
    print(f"普通函数对象大小: {sys.getsizeof(simple_function)} bytes")
    
    # 闭包的内存影响
    def create_multiplier(factor):
        return lambda x: x * factor  # 闭包
    
    multiplier_lambda = create_multiplier(5)
    print(f"闭包Lambda大小: {sys.getsizeof(multiplier_lambda)} bytes")
    
    # 4. 函数调用开销
    print("\n函数调用开销:")
    
    # 直接计算
    direct_result = measure_time(
        lambda: [x * x for x in test_data[:10000]],
        "直接计算"
    )
    
    # Lambda调用
    lambda_call_result = measure_time(
        lambda: [(lambda x: x * x)(x) for x in test_data[:10000]],
        "Lambda调用"
    )
    
    # 函数调用
    function_call_result = measure_time(
        lambda: [square_function(x) for x in test_data[:10000]],
        "函数调用"
    )
    
    # 性能建议
    print("\n性能建议:")
    
    performance_tips = [
        "1. 简单操作：列表推导式 > Lambda > 普通函数",
        "2. 复杂逻辑：普通函数性能更稳定",
        "3. 频繁调用：避免在循环中创建Lambda",
        "4. 内存敏感：注意闭包可能导致的内存泄漏",
        "5. 大数据处理：考虑使用生成器表达式",
        "6. 性能要求极高：考虑使用内置函数或operator模块"
    ]
    
    for tip in performance_tips:
        print(f"  {tip}")
    
    # operator模块示例
    print("\n使用operator模块优化:")
    
    import operator
    
    # 使用operator.mul代替lambda
    operator_result = measure_time(
        lambda: list(map(operator.mul, test_data[:10000], test_data[:10000])),
        "operator.mul"
    )
    
    lambda_mul_result = measure_time(
        lambda: list(map(lambda x, y: x * y, test_data[:10000], test_data[:10000])),
        "Lambda乘法"
    )
    
    """
    Java性能考虑:
    // Lambda vs 方法引用
    List<Integer> lambdaResult = numbers.stream()
                                       .map(x -> x * x)  // Lambda
                                       .collect(Collectors.toList());
    
    List<Integer> methodRefResult = numbers.stream()
                                          .map(this::square)  // 方法引用（通常更快）
                                          .collect(Collectors.toList());
    
    // 避免装箱/拆箱
    IntStream.range(0, 100000)
            .map(x -> x * x)  // 原始类型，避免装箱
            .sum();
    
    // 并行处理
    List<Integer> parallelResult = numbers.parallelStream()
                                         .map(x -> x * x)
                                         .collect(Collectors.toList());
    """
    
    print()


def main():
    """主函数：运行所有演示"""
    print("Python Lambda函数完整学习指南")
    print("=" * 50)
    
    demo_basic_syntax()
    demo_lambda_with_builtin_functions()
    demo_lambda_in_data_processing()
    demo_lambda_with_functional_programming()
    demo_lambda_limitations_and_alternatives()
    demo_performance_considerations()
    
    print("学习总结:")
    print("1. Lambda函数提供简洁的匿名函数语法")
    print("2. 适合与map、filter、sorted等函数配合使用")
    print("3. 函数式编程的重要工具，支持高阶函数操作")
    print("4. 复杂逻辑应使用普通函数以提高可读性")
    print("5. Java Lambda表达式提供类似功能但类型更严格")
    print("6. 性能考虑：简单操作优先，复杂逻辑用普通函数")


if __name__ == "__main__":
    main() 