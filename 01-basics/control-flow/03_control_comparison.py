#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python vs Java - 控制流程对比总结
===============================

本文件总结Python和Java在控制流程方面的主要差异
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

import sys
from typing import List, Dict, Any


def syntax_comparison_summary():
    """
    语法对比总结
    """
    print("=== 语法对比总结 ===\n")
    
    comparisons = [
        {
            "feature": "代码块分隔",
            "java": "花括号 { }",
            "python": "冒号 : 和缩进",
            "example_java": "if (condition) {\n    statement;\n}",
            "example_python": "if condition:\n    statement"
        },
        {
            "feature": "条件表达式",
            "java": "必须用括号",
            "python": "括号可选",
            "example_java": "if (x > 0)",
            "example_python": "if x > 0:"
        },
        {
            "feature": "逻辑运算符",
            "java": "&& || !",
            "python": "and or not",
            "example_java": "if (a > 0 && b < 10)",
            "example_python": "if a > 0 and b < 10:"
        },
        {
            "feature": "多条件判断",
            "java": "else if",
            "python": "elif",
            "example_java": "} else if (condition) {",
            "example_python": "elif condition:"
        },
        {
            "feature": "空操作",
            "java": "空语句 ;",
            "python": "pass",
            "example_java": "if (condition);",
            "example_python": "if condition:\n    pass"
        }
    ]
    
    for comp in comparisons:
        print(f"功能: {comp['feature']}")
        print(f"   Java:   {comp['java']}")
        print(f"   Python: {comp['python']}")
        print(f"   Java示例:   {comp['example_java']}")
        print(f"   Python示例: {comp['example_python']}")
        print()


def unique_python_features():
    """
    Python独有特性
    """
    print("=== Python独有特性 ===\n")
    
    # 1. 链式比较
    print("1. 链式比较")
    print("   Java: (x > 0) && (x < 10)")
    print("   Python: 0 < x < 10")
    
    age = 25
    if 18 <= age < 60:
        print(f"   年龄{age}在工作年龄范围内")
    print()
    
    # 2. 循环的else子句
    print("2. 循环的else子句")
    print("   Java: 无此功能")
    print("   Python: for/while循环可以有else子句")
    
    def find_divisor(number, max_divisor=5):
        print(f"   寻找{number}的因子:")
        for i in range(2, max_divisor + 1):
            if number % i == 0:
                print(f"     找到因子: {i}")
                break
        else:
            print(f"     在1-{max_divisor}范围内没有找到因子")
    
    find_divisor(15)  # 有因子
    find_divisor(17)  # 没有因子
    print()
    
    # 3. 成员运算符
    print("3. 成员运算符 in/not in")
    print("   Java: list.contains(item)")
    print("   Python: item in list")
    
    fruits = ["苹果", "香蕉", "橙子"]
    if "苹果" in fruits:
        print("   列表包含苹果")
    
    if "芒果" not in fruits:
        print("   列表不包含芒果")
    print()
    
    # 4. 多重赋值和解包
    print("4. 多重赋值和解包")
    print("   Java: 需要分别赋值")
    print("   Python: a, b = 1, 2")
    
    # 交换变量
    x, y = 10, 20
    print(f"   交换前: x={x}, y={y}")
    x, y = y, x
    print(f"   交换后: x={x}, y={y}")
    print()
    
    # 5. 列表推导式
    print("5. 列表推导式")
    print("   Java: Stream API")
    print("   Python: [expression for item in iterable if condition]")
    
    numbers = range(10)
    even_squares = [x**2 for x in numbers if x % 2 == 0]
    print(f"   偶数的平方: {even_squares}")
    print()


def java_to_python_migration():
    """
    Java到Python的迁移指南
    """
    print("=== Java到Python迁移指南 ===\n")
    
    migration_tips = [
        {
            "category": "语法转换",
            "tips": [
                "将花括号{}替换为冒号:和缩进",
                "将&&、||、!替换为and、or、not",
                "将else if替换为elif",
                "移除条件表达式的括号(可选)",
                "将空语句;替换为pass"
            ]
        },
        {
            "category": "循环转换",
            "tips": [
                "将for(int i=0; i<n; i++)替换为for i in range(n)",
                "将增强for循环for(Type item : collection)替换为for item in collection",
                "考虑使用enumerate()获取索引",
                "利用循环的else子句简化逻辑",
                "使用列表推导式替代简单的循环"
            ]
        },
        {
            "category": "条件判断转换",
            "tips": [
                "利用链式比较简化复合条件",
                "使用in运算符检查成员资格",
                "利用Python的真值判断特性",
                "使用三元运算符value_if_true if condition else value_if_false",
                "考虑使用match语句(Python 3.10+)替代复杂的if-elif"
            ]
        }
    ]
    
    for section in migration_tips:
        print(f"{section['category']}:")
        for tip in section['tips']:
            print(f"   • {tip}")
        print()


def common_patterns_comparison():
    """
    常见模式对比
    """
    print("=== 常见模式对比 ===\n")
    
    print("1. 遍历集合并处理")
    print("Java:")
    print("   for (String item : list) {")
    print("       if (item.length() > 3) {")
    print("           System.out.println(item.toUpperCase());")
    print("       }")
    print("   }")
    print()
    
    print("Python:")
    print("   for item in list:")
    print("       if len(item) > 3:")
    print("           print(item.upper())")
    print()
    
    # 实际示例
    items = ["cat", "elephant", "dog", "butterfly"]
    print("实际运行:")
    for item in items:
        if len(item) > 3:
            print(f"   {item.upper()}")
    print()
    
    print("2. 查找第一个匹配项")
    print("Java:")
    print("   String result = null;")
    print("   for (String item : list) {")
    print("       if (item.startsWith(\"a\")) {")
    print("           result = item;")
    print("           break;")
    print("       }")
    print("   }")
    print()
    
    print("Python (传统方式):")
    print("   result = None")
    print("   for item in list:")
    print("       if item.startswith('a'):")
    print("           result = item")
    print("           break")
    print()
    
    print("Python (推荐方式):")
    print("   result = next((item for item in list if item.startswith('a')), None)")
    print()
    
    # 实际示例
    words = ["hello", "apple", "world", "amazing"]
    result = next((word for word in words if word.startswith('a')), None)
    print(f"实际运行: 找到以'a'开头的单词: {result}")
    print()
    
    print("3. 统计条件匹配的项目数")
    print("Java:")
    print("   int count = 0;")
    print("   for (int num : numbers) {")
    print("       if (num % 2 == 0) {")
    print("           count++;")
    print("       }")
    print("   }")
    print()
    
    print("Python:")
    print("   count = sum(1 for num in numbers if num % 2 == 0)")
    print("   # 或者")
    print("   count = len([num for num in numbers if num % 2 == 0])")
    print()
    
    # 实际示例
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    count = sum(1 for num in numbers if num % 2 == 0)
    print(f"实际运行: 偶数个数: {count}")
    print()


def performance_considerations():
    """
    性能考虑
    """
    print("=== 性能考虑 ===\n")
    
    import time
    
    print("性能对比测试:")
    
    # 大数据集
    large_list = list(range(100000))
    
    def time_operation(operation_name, operation_func):
        start_time = time.time()
        result = operation_func()
        end_time = time.time()
        duration = end_time - start_time
        print(f"   {operation_name}: {duration:.6f}秒")
        return result
    
    print("\n1. 求和操作对比:")
    
    # 传统循环
    def sum_with_loop():
        total = 0
        for num in large_list:
            total += num
        return total
    
    # 内置函数
    def sum_with_builtin():
        return sum(large_list)
    
    # 列表推导式求和
    def sum_with_comprehension():
        return sum([num for num in large_list])
    
    result1 = time_operation("传统循环", sum_with_loop)
    result2 = time_operation("内置sum函数", sum_with_builtin)
    result3 = time_operation("推导式+sum", sum_with_comprehension)
    
    print(f"   结果验证: {result1 == result2 == result3}")
    print()
    
    print("2. 过滤操作对比:")
    
    # 传统循环过滤
    def filter_with_loop():
        result = []
        for num in large_list:
            if num % 2 == 0:
                result.append(num)
        return result
    
    # 列表推导式过滤
    def filter_with_comprehension():
        return [num for num in large_list if num % 2 == 0]
    
    # 内置filter函数
    def filter_with_builtin():
        return list(filter(lambda x: x % 2 == 0, large_list))
    
    time_operation("传统循环过滤", filter_with_loop)
    time_operation("列表推导式过滤", filter_with_comprehension)
    time_operation("内置filter函数", filter_with_builtin)
    print()
    
    print("性能优化建议:")
    recommendations = [
        "优先使用内置函数(sum, max, min, any, all等)",
        "列表推导式通常比传统循环快",
        "对于大数据集，考虑使用生成器表达式节省内存",
        "避免在循环中进行重复计算",
        "使用适当的数据结构(set用于成员检查，dict用于键值映射)",
        "考虑使用NumPy处理数值计算密集型任务"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")


def best_practices():
    """
    最佳实践建议
    """
    print("\n=== 最佳实践建议 ===\n")
    
    practices = {
        "代码风格": [
            "使用4个空格缩进，不要使用Tab",
            "条件表达式不需要括号，除非提高可读性",
            "使用有意义的变量名",
            "避免深度嵌套，考虑提前返回或continue",
            "遵循PEP 8编码规范"
        ],
        "性能优化": [
            "优先使用内置函数和标准库",
            "合理使用列表推导式和生成器表达式",
            "避免在循环中创建新对象",
            "使用集合(set)进行快速成员检查",
            "考虑使用缓存减少重复计算"
        ],
        "错误处理": [
            "使用具体的异常类型而不是通用Exception",
            "在循环中适当处理异常",
            "使用try-except-else-finally结构",
            "考虑使用断言检查前置条件",
            "记录错误信息用于调试"
        ],
        "可读性": [
            "使用描述性的函数和变量名",
            "添加适当的注释和文档字符串",
            "将复杂逻辑分解为小函数",
            "使用类型注解提高代码可读性",
            "保持函数和类的职责单一"
        ]
    }
    
    for category, tips in practices.items():
        print(f"{category}:")
        for tip in tips:
            print(f"   • {tip}")
        print()


def main():
    """主函数 - 展示所有对比内容"""
    print("Python vs Java - 控制流程对比总结")
    print("=" * 50)
    
    syntax_comparison_summary()
    unique_python_features()
    java_to_python_migration()
    common_patterns_comparison()
    performance_considerations()
    best_practices()
    
    print("\n总结:")
    print("1. Python的语法更简洁，可读性更好")
    print("2. Python提供了许多Java没有的便利特性")
    print("3. 从Java迁移到Python需要改变编程思维")
    print("4. Python在很多情况下性能足够，且开发效率更高")
    print("5. 合理使用Python特性可以大大简化代码")


if __name__ == "__main__":
    main() 