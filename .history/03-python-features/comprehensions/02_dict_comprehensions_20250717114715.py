#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
字典推导式详解 - Dictionary Comprehensions

本文件详细介绍Python字典推导式的语法和应用，
包括与Java Stream API的对比分析。

字典推导式是Python创建字典的简洁语法，
相当于Java中使用Stream API进行map操作后收集到Map中。

Author: Python学习项目
Date: 2024-01-16
"""

import time
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional


def main():
    """字典推导式示例主函数"""
    print("=== Python字典推导式详解 ===\n")
    
    # 1. 基础字典推导式语法
    basic_dict_comprehensions()
    
    # 2. 条件筛选字典推导式
    conditional_dict_comprehensions()
    
    # 3. 嵌套字典推导式
    nested_dict_comprehensions()
    
    # 4. 高级字典推导式技巧
    advanced_dict_comprehensions()
    
    # 5. 性能对比测试
    performance_comparison()
    
    # 6. 与Java Stream API对比
    java_comparison()
    
    # 7. 实际应用示例
    practical_examples()
    
    # 8. 常见陷阱和最佳实践
    pitfalls_and_best_practices()


def basic_dict_comprehensions():
    """基础字典推导式语法"""
    print("1. 基础字典推导式语法")
    print("-" * 40)
    
    # 基本语法：{key_expr: value_expr for item in iterable}
    
    # 示例1：数字平方字典
    squares = {x: x**2 for x in range(1, 6)}
    print(f"数字平方字典: {squares}")
    
    # 示例2：字符串长度字典
    words = ['apple', 'banana', 'cherry', 'date']
    word_lengths = {word: len(word) for word in words}
    print(f"单词长度字典: {word_lengths}")
    
    # 示例3：键值对互换
    original = {'a': 1, 'b': 2, 'c': 3}
    swapped = {v: k for k, v in original.items()}
    print(f"原字典: {original}")
    print(f"键值互换: {swapped}")
    
    # 示例4：从两个列表创建字典
    keys = ['name', 'age', 'city']
    values = ['张三', 25, '北京']
    person = {k: v for k, v in zip(keys, values)}
    print(f"人员信息: {person}")
    
    # 示例5：使用enumerate创建索引字典
    fruits = ['apple', 'banana', 'cherry']
    fruit_index = {fruit: idx for idx, fruit in enumerate(fruits)}
    print(f"水果索引: {fruit_index}")
    
    print()


def conditional_dict_comprehensions():
    """条件筛选字典推导式"""
    print("2. 条件筛选字典推导式")
    print("-" * 40)
    
    # 基本条件筛选语法：{key_expr: value_expr for item in iterable if condition}
    
    # 示例1：筛选偶数平方
    even_squares = {x: x**2 for x in range(1, 11) if x % 2 == 0}
    print(f"偶数平方: {even_squares}")
    
    # 示例2：筛选长单词
    words = ['cat', 'elephant', 'dog', 'hippopotamus', 'ant']
    long_words = {word: len(word) for word in words if len(word) > 3}
    print(f"长单词及长度: {long_words}")
    
    # 示例3：条件值表达式
    numbers = range(1, 11)
    number_types = {x: 'even' if x % 2 == 0 else 'odd' for x in numbers}
    print(f"数字类型: {number_types}")
    
    # 示例4：复杂条件筛选
    students = [
        {'name': '张三', 'age': 20, 'score': 85},
        {'name': '李四', 'age': 19, 'score': 92},
        {'name': '王五', 'age': 21, 'score': 78},
        {'name': '赵六', 'age': 20, 'score': 95}
    ]
    
    # 筛选优秀学生（分数>=90）
    excellent_students = {
        student['name']: student['score'] 
        for student in students 
        if student['score'] >= 90
    }
    print(f"优秀学生: {excellent_students}")
    
    # 示例5：多重条件
    young_excellent = {
        student['name']: student['score'] 
        for student in students 
        if student['age'] < 21 and student['score'] >= 85
    }
    print(f"年轻优秀学生: {young_excellent}")
    
    print()


def nested_dict_comprehensions():
    """嵌套字典推导式"""
    print("3. 嵌套字典推导式")
    print("-" * 40)
    
    # 示例1：二维表格数据
    # 创建乘法表
    multiplication_table = {
        i: {j: i * j for j in range(1, 6)} 
        for i in range(1, 6)
    }
    print("乘法表:")
    for i, row in multiplication_table.items():
        print(f"  {i}: {row}")
    
    # 示例2：矩阵转置
    matrix = {
        'row1': {'col1': 1, 'col2': 2, 'col3': 3},
        'row2': {'col1': 4, 'col2': 5, 'col3': 6},
        'row3': {'col1': 7, 'col2': 8, 'col3': 9}
    }
    
    # 转置矩阵
    transposed = {
        col: {row: matrix[row][col] for row in matrix} 
        for col in matrix['row1']
    }
    print(f"\n原矩阵: {matrix}")
    print(f"转置矩阵: {transposed}")
    
    # 示例3：多级分组
    products = [
        {'name': 'iPhone', 'category': 'Electronics', 'brand': 'Apple', 'price': 999},
        {'name': 'MacBook', 'category': 'Electronics', 'brand': 'Apple', 'price': 1299},
        {'name': 'Galaxy', 'category': 'Electronics', 'brand': 'Samsung', 'price': 899},
        {'name': 'T-Shirt', 'category': 'Clothing', 'brand': 'Nike', 'price': 29},
        {'name': 'Shoes', 'category': 'Clothing', 'brand': 'Nike', 'price': 89}
    ]
    
    # 按类别和品牌分组
    grouped_products = {
        category: {
            brand: [p for p in products 
                   if p['category'] == category and p['brand'] == brand]
            for brand in set(p['brand'] for p in products if p['category'] == category)
        }
        for category in set(p['category'] for p in products)
    }
    
    print(f"\n分组产品: {grouped_products}")
    
    print()


def advanced_dict_comprehensions():
    """高级字典推导式技巧"""
    print("4. 高级字典推导式技巧")
    print("-" * 40)
    
    # 示例1：使用函数作为值
    def get_letter_count(word):
        return Counter(word)
    
    words = ['hello', 'world', 'python']
    word_analysis = {word: get_letter_count(word) for word in words}
    print(f"单词字母统计: {word_analysis}")
    
    # 示例2：使用defaultdict模式
    # 创建按首字母分组的字典
    words = ['apple', 'ant', 'banana', 'cat', 'dog', 'elephant']
    grouped_by_first_letter = {}
    for word in words:
        first_letter = word[0]
        if first_letter not in grouped_by_first_letter:
            grouped_by_first_letter[first_letter] = []
        grouped_by_first_letter[first_letter].append(word)
    
    # 使用字典推导式的等价写法
    letters = set(word[0] for word in words)
    grouped_dict = {
        letter: [word for word in words if word[0] == letter] 
        for letter in letters
    }
    print(f"按首字母分组: {grouped_dict}")
    
    # 示例3：动态键名
    data = [
        ('temperature', 25, 'celsius'),
        ('pressure', 1013, 'hPa'),
        ('humidity', 60, 'percent')
    ]
    
    measurements = {
        f"{name}_{unit}": value 
        for name, value, unit in data
    }
    print(f"测量数据: {measurements}")
    
    # 示例4：条件键值对
    # 根据条件决定是否包含键值对
    numbers = range(1, 11)
    filtered_squares = {
        x: x**2 for x in numbers 
        if x % 2 == 0  # 只包含偶数
    }
    print(f"偶数平方: {filtered_squares}")
    
    # 示例5：复杂表达式
    employees = [
        {'name': '张三', 'salary': 5000, 'department': 'IT'},
        {'name': '李四', 'salary': 6000, 'department': 'Sales'},
        {'name': '王五', 'salary': 5500, 'department': 'IT'},
        {'name': '赵六', 'salary': 7000, 'department': 'Sales'}
    ]
    
    # 计算每个部门的平均工资
    departments = set(emp['department'] for emp in employees)
    dept_avg_salary = {
        dept: sum(emp['salary'] for emp in employees if emp['department'] == dept) / 
              len([emp for emp in employees if emp['department'] == dept])
        for dept in departments
    }
    print(f"部门平均工资: {dept_avg_salary}")
    
    print()


def performance_comparison():
    """性能对比测试"""
    print("5. 性能对比测试")
    print("-" * 40)
    
    # 测试数据
    data = list(range(10000))
    
    # 方法1：传统循环
    start_time = time.time()
    result1 = {}
    for x in data:
        if x % 2 == 0:
            result1[x] = x ** 2
    time1 = time.time() - start_time
    
    # 方法2：字典推导式
    start_time = time.time()
    result2 = {x: x**2 for x in data if x % 2 == 0}
    time2 = time.time() - start_time
    
    # 方法3：使用dict()和生成器表达式
    start_time = time.time()
    result3 = dict((x, x**2) for x in data if x % 2 == 0)
    time3 = time.time() - start_time
    
    print(f"传统循环方法: {time1:.4f}秒")
    print(f"字典推导式: {time2:.4f}秒")
    print(f"dict()构造器: {time3:.4f}秒")
    print(f"字典推导式比传统方法快: {time1/time2:.2f}倍")
    
    # 验证结果一致性
    print(f"结果一致性: {result1 == result2 == result3}")
    
    print()


def java_comparison():
    """与Java Stream API对比"""
    print("6. 与Java Stream API对比")
    print("-" * 40)
    
    # Python字典推导式示例
    words = ['apple', 'banana', 'cherry', 'date']
    
    # Python: 创建单词长度字典
    word_lengths = {word: len(word) for word in words}
    print("Python字典推导式:")
    print(f"  {word_lengths}")
    
    print("\nJava等价代码:")
    print("""
    // Java 8+ Stream API
    List<String> words = Arrays.asList("apple", "banana", "cherry", "date");
    
    Map<String, Integer> wordLengths = words.stream()
        .collect(Collectors.toMap(
            word -> word,           // key mapper
            word -> word.length()   // value mapper
        ));
    """)
    
    # 复杂示例：条件筛选
    numbers = range(1, 11)
    even_squares = {x: x**2 for x in numbers if x % 2 == 0}
    print(f"\nPython条件筛选: {even_squares}")
    
    print("Java等价代码:")
    print("""
    // Java 8+ Stream API with filtering
    Map<Integer, Integer> evenSquares = IntStream.rangeClosed(1, 10)
        .filter(x -> x % 2 == 0)
        .boxed()
        .collect(Collectors.toMap(
            x -> x,
            x -> x * x
        ));
    """)
    
    # 语法对比总结
    print("\n语法特点对比:")
    print("Python字典推导式:")
    print("  - 简洁的内联语法")
    print("  - 直观的条件筛选")
    print("  - 自然的键值表达")
    print("  - 无需导入额外模块")
    
    print("\nJava Stream API:")
    print("  - 函数式编程风格")
    print("  - 链式调用方法")
    print("  - 需要Collectors工具类")
    print("  - 类型安全但语法较冗长")
    
    print()


def practical_examples():
    """实际应用示例"""
    print("7. 实际应用示例")
    print("-" * 40)
    
    # 示例1：配置文件解析
    config_lines = [
        "database.host=localhost",
        "database.port=5432", 
        "database.name=myapp",
        "server.timeout=30",
        "server.max_connections=100"
    ]
    
    # 解析配置为字典
    config = {
        line.split('=')[0]: line.split('=')[1] 
        for line in config_lines 
        if '=' in line
    }
    print(f"配置解析: {config}")
    
    # 示例2：数据聚合
    sales_data = [
        {'product': 'iPhone', 'region': 'North', 'amount': 1000},
        {'product': 'iPhone', 'region': 'South', 'amount': 1500},
        {'product': 'iPad', 'region': 'North', 'amount': 800},
        {'product': 'iPhone', 'region': 'North', 'amount': 1200},
        {'product': 'iPad', 'region': 'South', 'amount': 900}
    ]
    
    # 按产品聚合销售额
    product_sales = {}
    for sale in sales_data:
        product = sale['product']
        if product not in product_sales:
            product_sales[product] = 0
        product_sales[product] += sale['amount']
    
    # 使用字典推导式的等价写法
    products = set(sale['product'] for sale in sales_data)
    product_sales_dict = {
        product: sum(sale['amount'] for sale in sales_data if sale['product'] == product)
        for product in products
    }
    print(f"产品销售汇总: {product_sales_dict}")
    
    # 示例3：API响应转换
    api_response = [
        {'id': 1, 'username': 'john_doe', 'email': 'john@example.com'},
        {'id': 2, 'username': 'jane_smith', 'email': 'jane@example.com'},
        {'id': 3, 'username': 'bob_wilson', 'email': 'bob@example.com'}
    ]
    
    # 创建ID到用户信息的映射
    user_lookup = {user['id']: user for user in api_response}
    print(f"用户查找表: {user_lookup}")
    
    # 创建用户名到邮箱的映射
    username_to_email = {
        user['username']: user['email'] 
        for user in api_response
    }
    print(f"用户名邮箱映射: {username_to_email}")
    
    # 示例4：数据清洗
    raw_data = {
        'name': '  张三  ',
        'age': '25',
        'city': '北京',
        'salary': '  5000  ',
        'department': None
    }
    
    # 清洗数据：去除空白，转换类型，过滤None值
    cleaned_data = {
        k: v.strip() if isinstance(v, str) else v
        for k, v in raw_data.items() 
        if v is not None
    }
    print(f"清洗后数据: {cleaned_data}")
    
    print()


def pitfalls_and_best_practices():
    """常见陷阱和最佳实践"""
    print("8. 常见陷阱和最佳实践")
    print("-" * 40)
    
    # 陷阱1：在推导式中修改可变对象
    print("陷阱1：可变对象共享问题")
    
    # 错误示例
    matrix = [[0] * 3 for _ in range(3)]  # 正确
    # matrix = [[0] * 3] * 3  # 错误！会共享同一个列表
    
    print("正确的矩阵创建:")
    for row in matrix:
        print(f"  {row}")
    
    # 陷阱2：复杂表达式可读性
    print("\n陷阱2：复杂表达式可读性")
    
    # 不好的示例（过于复杂）
    complex_dict = {
        k: {
            nested_k: nested_v * 2 if nested_v > 10 else nested_v 
            for nested_k, nested_v in v.items() if nested_v is not None
        }
        for k, v in {'a': {'x': 5, 'y': 15}, 'b': {'x': None, 'y': 20}}.items()
        if v
    }
    
    # 更好的写法：拆分为多步
    source_data = {'a': {'x': 5, 'y': 15}, 'b': {'x': None, 'y': 20}}
    
    def process_nested_dict(nested_dict):
        return {
            k: v * 2 if v > 10 else v 
            for k, v in nested_dict.items() 
            if v is not None
        }
    
    better_dict = {
        k: process_nested_dict(v) 
        for k, v in source_data.items() 
        if v
    }
    
    print(f"复杂处理结果: {better_dict}")
    
    # 最佳实践总结
    print("\n最佳实践总结:")
    print("1. 保持推导式简洁，复杂逻辑提取为函数")
    print("2. 使用有意义的变量名，避免单字母变量")
    print("3. 对于嵌套层级超过2层的，考虑使用传统循环")
    print("4. 注意内存使用，大数据集考虑生成器表达式")
    print("5. 添加适当的类型注解提高代码可读性")
    
    # 类型注解示例
    def create_user_mapping(users: List[Dict[str, Any]]) -> Dict[int, str]:
        """创建用户ID到姓名的映射"""
        return {user['id']: user['name'] for user in users}
    
    print("\n6. 性能考虑:")
    print("   - 字典推导式通常比循环快20-30%")
    print("   - 避免在推导式中进行复杂计算")
    print("   - 大数据集使用生成器表达式节省内存")
    
    print()


if __name__ == '__main__':
    main() 