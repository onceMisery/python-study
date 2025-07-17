#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python列表推导式详解
List Comprehensions in Python

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习Python列表推导式的语法、性能和与Java Stream API的对比

学习目标:
1. 掌握列表推导式的基本语法
2. 理解列表推导式的性能优势
3. 学会嵌套和条件列表推导式
4. 对比Java Stream API的实现方式
"""

import time
import random
from typing import List, Callable


def demo_basic_syntax():
    """演示列表推导式的基本语法"""
    print("=== 1. 基本语法演示 ===")
    
    # 基础语法: [expression for item in iterable]
    numbers = [1, 2, 3, 4, 5]
    
    # Python列表推导式
    squares = [x**2 for x in numbers]
    print(f"原始列表: {numbers}")
    print(f"平方列表: {squares}")
    
    # 等价的传统for循环写法
    squares_traditional = []
    for x in numbers:
        squares_traditional.append(x**2)
    print(f"传统方式: {squares_traditional}")
    
    """
    Java等价实现:
    List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
    List<Integer> squares = numbers.stream()
                                  .map(x -> x * x)
                                  .collect(Collectors.toList());
    """
    
    print()


def demo_conditional_comprehensions():
    """演示条件列表推导式"""
    print("=== 2. 条件推导式演示 ===")
    
    numbers = range(1, 11)
    
    # 带条件的列表推导式: [expression for item in iterable if condition]
    even_numbers = [x for x in numbers if x % 2 == 0]
    print(f"偶数列表: {even_numbers}")
    
    # 复杂条件
    even_squares = [x**2 for x in numbers if x % 2 == 0]
    print(f"偶数的平方: {even_squares}")
    
    # 条件表达式 (三元操作符)
    classified = [x if x % 2 == 0 else -x for x in numbers]
    print(f"偶数保持原值，奇数变负数: {classified}")
    
    """
    Java等价实现:
    List<Integer> evenNumbers = IntStream.rangeClosed(1, 10)
                                        .filter(x -> x % 2 == 0)
                                        .boxed()
                                        .collect(Collectors.toList());
    
    List<Integer> evenSquares = IntStream.rangeClosed(1, 10)
                                        .filter(x -> x % 2 == 0)
                                        .map(x -> x * x)
                                        .boxed()
                                        .collect(Collectors.toList());
    """
    
    print()


def demo_nested_comprehensions():
    """演示嵌套列表推导式"""
    print("=== 3. 嵌套推导式演示 ===")
    
    # 二维列表处理
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    # 扁平化二维列表
    flattened = [item for row in matrix for item in row]
    print(f"原始矩阵: {matrix}")
    print(f"扁平化后: {flattened}")
    
    # 等价的嵌套循环
    flattened_traditional = []
    for row in matrix:
        for item in row:
            flattened_traditional.append(item)
    print(f"传统方式: {flattened_traditional}")
    
    # 嵌套条件
    filtered_flattened = [item for row in matrix for item in row if item % 2 == 0]
    print(f"偶数扁平化: {filtered_flattened}")
    
    # 创建乘法表
    multiplication_table = [[i * j for j in range(1, 4)] for i in range(1, 4)]
    print(f"乘法表: {multiplication_table}")
    
    """
    Java等价实现:
    List<List<Integer>> matrix = Arrays.asList(
        Arrays.asList(1, 2, 3),
        Arrays.asList(4, 5, 6),
        Arrays.asList(7, 8, 9)
    );
    
    List<Integer> flattened = matrix.stream()
                                   .flatMap(Collection::stream)
                                   .collect(Collectors.toList());
    """
    
    print()


def demo_string_processing():
    """演示字符串处理的列表推导式"""
    print("=== 4. 字符串处理演示 ===")
    
    words = ["hello", "world", "python", "java"]
    
    # 字符串长度
    lengths = [len(word) for word in words]
    print(f"单词长度: {dict(zip(words, lengths))}")
    
    # 字符串转换
    upper_words = [word.upper() for word in words]
    print(f"大写转换: {upper_words}")
    
    # 首字母大写
    capitalized = [word.capitalize() for word in words]
    print(f"首字母大写: {capitalized}")
    
    # 过滤长度大于4的单词并转换
    long_words = [word.upper() for word in words if len(word) > 4]
    print(f"长单词大写: {long_words}")
    
    # 字符串分割和处理
    text = "Python is awesome and powerful"
    vowels = [char for char in text.lower() if char in 'aeiou']
    print(f"元音字母: {vowels}")
    
    """
    Java等价实现:
    List<String> words = Arrays.asList("hello", "world", "python", "java");
    
    List<Integer> lengths = words.stream()
                                .map(String::length)
                                .collect(Collectors.toList());
    
    List<String> upperWords = words.stream()
                                  .map(String::toUpperCase)
                                  .collect(Collectors.toList());
    """
    
    print()


def demo_performance_comparison():
    """性能对比：列表推导式 vs 传统循环 vs map()"""
    print("=== 5. 性能对比演示 ===")
    
    # 准备测试数据
    data = list(range(100000))
    
    def test_comprehension():
        return [x**2 for x in data]
    
    def test_traditional_loop():
        result = []
        for x in data:
            result.append(x**2)
        return result
    
    def test_map_function():
        return list(map(lambda x: x**2, data))
    
    # 性能测试函数
    def measure_time(func: Callable, description: str):
        start_time = time.time()
        result = func()
        end_time = time.time()
        print(f"{description}: {end_time - start_time:.4f}秒, 结果长度: {len(result)}")
        return end_time - start_time
    
    print("处理100,000个元素的平方运算:")
    time1 = measure_time(test_comprehension, "列表推导式")
    time2 = measure_time(test_traditional_loop, "传统for循环")
    time3 = measure_time(test_map_function, "map()函数")
    
    # 性能分析
    fastest = min(time1, time2, time3)
    print(f"\n性能分析:")
    print(f"列表推导式相对最快: {time1/fastest:.2f}x")
    print(f"传统循环相对最快: {time2/fastest:.2f}x")
    print(f"map函数相对最快: {time3/fastest:.2f}x")
    
    """
    Java性能对比参考:
    // 传统for循环
    List<Integer> result1 = new ArrayList<>();
    for (int x : data) {
        result1.add(x * x);
    }
    
    // Stream API
    List<Integer> result2 = data.stream()
                               .map(x -> x * x)
                               .collect(Collectors.toList());
    
    // 并行Stream
    List<Integer> result3 = data.parallelStream()
                               .map(x -> x * x)
                               .collect(Collectors.toList());
    
    通常性能: 传统循环 > Stream > 并行Stream (小数据量)
    """
    
    print()


def demo_advanced_patterns():
    """演示高级应用模式"""
    print("=== 6. 高级应用模式 ===")
    
    # 数据转换管道
    raw_data = ["1", "2", "3", "4", "5", "invalid", "6"]
    
    # 多步骤数据处理
    processed = [int(x)**2 for x in raw_data if x.isdigit() and int(x) % 2 == 0]
    print(f"原始数据: {raw_data}")
    print(f"处理结果 (数字->偶数->平方): {processed}")
    
    # 字典数据处理
    students = [
        {"name": "Alice", "score": 85},
        {"name": "Bob", "score": 92},
        {"name": "Charlie", "score": 78},
        {"name": "Diana", "score": 96}
    ]
    
    # 提取高分学生姓名
    high_scorers = [student["name"] for student in students if student["score"] >= 90]
    print(f"高分学生: {high_scorers}")
    
    # 成绩统计
    scores = [student["score"] for student in students]
    score_stats = {
        "平均分": sum(scores) / len(scores),
        "最高分": max(scores),
        "最低分": min(scores)
    }
    print(f"成绩统计: {score_stats}")
    
    # 文件路径处理示例
    file_paths = [
        "/home/user/document.txt",
        "/home/user/image.jpg", 
        "/home/user/script.py",
        "/home/user/data.csv"
    ]
    
    # 提取Python文件
    python_files = [path for path in file_paths if path.endswith('.py')]
    print(f"Python文件: {python_files}")
    
    # 提取文件名
    filenames = [path.split('/')[-1] for path in file_paths]
    print(f"文件名列表: {filenames}")
    
    """
    Java等价实现:
    List<Student> students = Arrays.asList(/*...*/);
    
    List<String> highScorers = students.stream()
                                      .filter(s -> s.getScore() >= 90)
                                      .map(Student::getName)
                                      .collect(Collectors.toList());
    
    OptionalDouble avgScore = students.stream()
                                     .mapToInt(Student::getScore)
                                     .average();
    """
    
    print()


def demo_common_pitfalls():
    """演示常见陷阱和最佳实践"""
    print("=== 7. 常见陷阱和最佳实践 ===")
    
    # 陷阱1: 过度复杂化
    print("陷阱1: 避免过度复杂的推导式")
    numbers = range(1, 6)
    
    # 不推荐: 过于复杂
    complex_bad = [x**2 if x % 2 == 0 else x**3 if x % 3 == 0 else x for x in numbers if x > 2]
    print(f"复杂推导式: {complex_bad}")
    
    # 推荐: 分步处理
    filtered = [x for x in numbers if x > 2]
    result_good = []
    for x in filtered:
        if x % 2 == 0:
            result_good.append(x**2)
        elif x % 3 == 0:
            result_good.append(x**3)
        else:
            result_good.append(x)
    print(f"分步处理: {result_good}")
    
    # 陷阱2: 副作用
    print("\n陷阱2: 避免在推导式中产生副作用")
    items = [1, 2, 3, 4, 5]
    
    # 不推荐: 有副作用的推导式
    # side_effects = [print(f"Processing {x}") or x**2 for x in items]  # 不推荐
    
    # 推荐: 分离副作用和数据处理
    processed = []
    for x in items:
        print(f"Processing {x}")  # 副作用
        processed.append(x**2)   # 数据处理
    
    # 陷阱3: 内存使用
    print("\n陷阱3: 大数据集内存考虑")
    
    # 对于大数据集，考虑使用生成器表达式
    large_range = range(1000000)
    
    # 列表推导式 - 立即创建所有元素
    # large_list = [x**2 for x in large_range]  # 占用大量内存
    
    # 生成器表达式 - 按需生成
    large_generator = (x**2 for x in large_range)  # 内存友好
    print(f"生成器对象: {large_generator}")
    print(f"第一个元素: {next(large_generator)}")
    
    # 最佳实践总结
    print("\n最佳实践:")
    print("1. 保持推导式简单易读")
    print("2. 复杂逻辑使用传统循环")
    print("3. 避免副作用")
    print("4. 大数据集考虑生成器")
    print("5. 适当使用变量名提高可读性")
    
    print()


def main():
    """主函数：运行所有演示"""
    print("Python列表推导式完整学习指南")
    print("=" * 50)
    
    demo_basic_syntax()
    demo_conditional_comprehensions()
    demo_nested_comprehensions()
    demo_string_processing()
    demo_performance_comparison()
    demo_advanced_patterns()
    demo_common_pitfalls()
    
    print("学习总结:")
    print("1. 列表推导式提供了简洁的语法来创建列表")
    print("2. 性能通常优于传统循环")
    print("3. 可读性是最重要的考虑因素")
    print("4. 复杂逻辑应该拆分或使用传统方法")
    print("5. Java Stream API提供了类似的函数式编程能力")


if __name__ == "__main__":
    main() 