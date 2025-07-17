#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法 - 函数定义
========================

本文件演示Python的函数定义，并与Java进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

from typing import List, Dict, Tuple, Optional, Union, Callable
import math


def demonstrate_basic_functions():
    """
    演示基本函数定义
    与Java方法的对比
    """
    print("=== 基本函数定义 ===\n")
    
    print("Java vs Python函数定义:")
    print("Java:")
    print("   public int add(int a, int b) {")
    print("       return a + b;")
    print("   }")
    print()
    
    print("Python:")
    print("   def add(a, b):")
    print("       return a + b")
    print()
    
    # Python函数示例
    def add(a, b):
        """加法函数 - 最简单的函数定义"""
        return a + b
    
    def multiply(a, b):
        """乘法函数"""
        result = a * b
        return result
    
    def greet(name):
        """问候函数 - 无返回值"""
        print(f"你好, {name}!")
    
    # 函数调用
    print("函数调用示例:")
    print(f"   add(3, 5) = {add(3, 5)}")
    print(f"   multiply(4, 6) = {multiply(4, 6)}")
    print("   greet('张三'):")
    greet('张三')
    print()
    
    print("关键差异:")
    print("   - Python使用def关键字定义函数")
    print("   - 不需要声明参数和返回值类型")
    print("   - 使用缩进表示函数体")
    print("   - 无返回值的函数返回None")
    print()


def demonstrate_parameters():
    """
    演示参数传递
    位置参数、关键字参数、默认参数
    """
    print("=== 参数传递 ===\n")
    
    print("1. 位置参数 (与Java类似)")
    
    def calculate_area(length, width):
        """计算矩形面积"""
        return length * width
    
    area = calculate_area(5, 3)
    print(f"   calculate_area(5, 3) = {area}")
    print()
    
    print("2. 关键字参数 (Python特有)")
    
    def create_person(name, age, city):
        """创建人员信息"""
        return f"{name}, {age}岁, 来自{city}"
    
    # 位置参数调用
    person1 = create_person("张三", 25, "北京")
    print(f"   位置参数: {person1}")
    
    # 关键字参数调用
    person2 = create_person(city="上海", name="李四", age=30)
    print(f"   关键字参数: {person2}")
    
    # 混合调用
    person3 = create_person("王五", age=28, city="广州")
    print(f"   混合调用: {person3}")
    print()
    
    print("3. 默认参数值")
    print("   Java: 需要方法重载")
    print("   Python: 直接在参数中指定默认值")
    
    def power(base, exponent=2):
        """计算幂，默认为平方"""
        return base ** exponent
    
    print(f"   power(3) = {power(3)}")        # 使用默认值
    print(f"   power(3, 3) = {power(3, 3)}")  # 指定指数
    print(f"   power(base=2, exponent=4) = {power(base=2, exponent=4)}")
    print()
    
    print("4. 多个默认参数")
    
    def connect_database(host, port=3306, username="admin", password="123456"):
        """数据库连接函数"""
        return f"连接到 {host}:{port}，用户: {username}"
    
    print(f"   connect_database('localhost')")
    print(f"   -> {connect_database('localhost')}")
    
    print(f"   connect_database('remote', username='user1')")
    print(f"   -> {connect_database('remote', username='user1')}")
    print()


def demonstrate_variable_arguments():
    """
    演示可变参数
    *args 和 **kwargs
    """
    print("=== 可变参数 ===\n")
    
    print("Java vs Python可变参数:")
    print("Java: public void method(String... args)")
    print("Python: def method(*args, **kwargs)")
    print()
    
    print("1. *args - 可变位置参数")
    
    def sum_all(*numbers):
        """求所有数字的和"""
        total = 0
        for num in numbers:
            total += num
        return total
    
    print(f"   sum_all() = {sum_all()}")
    print(f"   sum_all(1) = {sum_all(1)}")
    print(f"   sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
    print(f"   sum_all(1, 2, 3, 4, 5) = {sum_all(1, 2, 3, 4, 5)}")
    print()
    
    print("2. **kwargs - 可变关键字参数")
    
    def create_user(**user_info):
        """创建用户信息"""
        print("   用户信息:")
        for key, value in user_info.items():
            print(f"     {key}: {value}")
        return user_info
    
    print("   create_user(name='张三', age=25, city='北京'):")
    create_user(name='张三', age=25, city='北京')
    
    print("\n   create_user(name='李四', job='工程师', salary=8000, married=True):")
    create_user(name='李四', job='工程师', salary=8000, married=True)
    print()
    
    print("3. 混合使用")
    
    def flexible_function(required_param, *args, default_param="默认值", **kwargs):
        """灵活的函数参数示例"""
        print(f"   必需参数: {required_param}")
        print(f"   位置参数: {args}")
        print(f"   默认参数: {default_param}")
        print(f"   关键字参数: {kwargs}")
        print()
    
    print("   调用示例:")
    flexible_function("必需的", 1, 2, 3, default_param="自定义", extra1="额外1", extra2="额外2")
    
    print("4. 参数解包")
    
    def divide(dividend, divisor):
        """除法函数"""
        return dividend / divisor
    
    numbers = [10, 2]
    result = divide(*numbers)  # 解包列表
    print(f"   divide(*[10, 2]) = {result}")
    
    params = {"dividend": 20, "divisor": 4}
    result = divide(**params)  # 解包字典
    print(f"   divide(**{{'dividend': 20, 'divisor': 4}}) = {result}")
    print()


def demonstrate_return_values():
    """
    演示返回值
    多返回值、None返回值
    """
    print("=== 返回值 ===\n")
    
    print("1. 单个返回值 (与Java相同)")
    
    def get_square(num):
        """返回平方值"""
        return num * num
    
    print(f"   get_square(5) = {get_square(5)}")
    print()
    
    print("2. 多个返回值 (Python特有)")
    print("   Java需要创建对象或使用数组")
    print("   Python可以直接返回多个值")
    
    def get_name_age():
        """返回姓名和年龄"""
        return "张三", 25
    
    def divide_with_remainder(dividend, divisor):
        """返回商和余数"""
        quotient = dividend // divisor
        remainder = dividend % divisor
        return quotient, remainder
    
    # 多返回值接收
    name, age = get_name_age()
    print(f"   name, age = get_name_age()")
    print(f"   name = {name}, age = {age}")
    
    q, r = divide_with_remainder(17, 5)
    print(f"   q, r = divide_with_remainder(17, 5)")
    print(f"   商 = {q}, 余数 = {r}")
    print()
    
    print("3. 返回不同类型")
    
    def analyze_text(text):
        """分析文本，返回多种统计信息"""
        length = len(text)
        words = text.split()
        word_count = len(words)
        is_long = length > 50
        
        return length, word_count, is_long
    
    text = "Python是一种高级编程语言，具有简洁的语法和强大的功能"
    length, word_count, is_long = analyze_text(text)
    
    print(f"   文本: {text}")
    print(f"   字符数: {length}")
    print(f"   单词数: {word_count}")
    print(f"   是否长文本: {is_long}")
    print()
    
    print("4. 无返回值 (返回None)")
    
    def print_info(name, age):
        """打印信息，无返回值"""
        print(f"   姓名: {name}, 年龄: {age}")
        # 隐式返回None
    
    def explicit_none():
        """显式返回None"""
        print("   执行一些操作...")
        return None
    
    result1 = print_info("李四", 30)
    result2 = explicit_none()
    
    print(f"   print_info的返回值: {result1}")
    print(f"   explicit_none的返回值: {result2}")
    print()


def demonstrate_type_hints():
    """
    演示类型注解
    Python 3.5+的特性
    """
    print("=== 类型注解 ===\n")
    
    print("Python类型注解 vs Java类型声明:")
    print("Java:")
    print("   public int add(int a, int b) {")
    print("       return a + b;")
    print("   }")
    print()
    
    print("Python (类型注解):")
    print("   def add(a: int, b: int) -> int:")
    print("       return a + b")
    print()
    
    # 基本类型注解
    def add_numbers(a: int, b: int) -> int:
        """带类型注解的加法函数"""
        return a + b
    
    def format_name(first: str, last: str) -> str:
        """格式化姓名"""
        return f"{last}, {first}"
    
    def is_positive(num: float) -> bool:
        """检查是否为正数"""
        return num > 0
    
    print("基本类型注解示例:")
    print(f"   add_numbers(3, 5) = {add_numbers(3, 5)}")
    print(f"   format_name('三', '张') = {format_name('三', '张')}")
    print(f"   is_positive(-2.5) = {is_positive(-2.5)}")
    print()
    
    # 复杂类型注解
    def process_scores(scores: List[int]) -> Dict[str, float]:
        """处理分数列表，返回统计信息"""
        if not scores:
            return {"average": 0.0, "max": 0.0, "min": 0.0}
        
        return {
            "average": sum(scores) / len(scores),
            "max": float(max(scores)),
            "min": float(min(scores))
        }
    
    def get_user_info(user_id: int) -> Optional[Dict[str, Union[str, int]]]:
        """获取用户信息，可能返回None"""
        if user_id > 0:
            return {"name": "用户" + str(user_id), "age": 25}
        return None
    
    print("复杂类型注解示例:")
    scores = [85, 92, 78, 96, 88]
    stats = process_scores(scores)
    print(f"   process_scores({scores})")
    print(f"   -> {stats}")
    
    user = get_user_info(1)
    print(f"   get_user_info(1) = {user}")
    
    user = get_user_info(-1)
    print(f"   get_user_info(-1) = {user}")
    print()
    
    # 函数类型注解
    def apply_operation(numbers: List[int], operation: Callable[[int, int], int]) -> int:
        """应用操作到数字列表"""
        result = numbers[0]
        for num in numbers[1:]:
            result = operation(result, num)
        return result
    
    def multiply(a: int, b: int) -> int:
        return a * b
    
    numbers = [2, 3, 4]
    result = apply_operation(numbers, multiply)
    print(f"连续乘法 {numbers} = {result}")
    print()


def demonstrate_docstrings():
    """
    演示文档字符串
    Python的文档化方式
    """
    print("=== 文档字符串 ===\n")
    
    print("Java vs Python文档:")
    print("Java: /** Javadoc注释 */")
    print("Python: \"\"\"文档字符串\"\"\"")
    print()
    
    def calculate_bmi(weight: float, height: float) -> float:
        """
        计算身体质量指数(BMI)
        
        Args:
            weight (float): 体重，单位为千克
            height (float): 身高，单位为米
            
        Returns:
            float: BMI值
            
        Raises:
            ValueError: 当身高为0或负数时
            
        Examples:
            >>> calculate_bmi(70, 1.75)
            22.86
        """
        if height <= 0:
            raise ValueError("身高必须大于0")
        
        bmi = weight / (height ** 2)
        return round(bmi, 2)
    
    def get_bmi_category(bmi: float) -> str:
        """
        根据BMI值获取体重分类
        
        参数:
            bmi: BMI值
            
        返回:
            体重分类字符串
        """
        if bmi < 18.5:
            return "偏瘦"
        elif bmi < 24:
            return "正常"
        elif bmi < 28:
            return "偏胖"
        else:
            return "肥胖"
    
    # 使用文档化的函数
    weight, height = 70, 1.75
    bmi = calculate_bmi(weight, height)
    category = get_bmi_category(bmi)
    
    print(f"体重: {weight}kg, 身高: {height}m")
    print(f"BMI: {bmi}")
    print(f"分类: {category}")
    print()
    
    # 查看文档字符串
    print("查看函数文档:")
    print(f"calculate_bmi.__doc__:")
    print(calculate_bmi.__doc__)


def demonstrate_lambda_functions():
    """
    演示Lambda函数
    匿名函数
    """
    print("\n=== Lambda函数 ===\n")
    
    print("Java vs Python匿名函数:")
    print("Java 8+: (x, y) -> x + y")
    print("Python: lambda x, y: x + y")
    print()
    
    # 基本Lambda函数
    print("1. 基本Lambda函数")
    
    # 传统函数定义
    def square_func(x):
        return x ** 2
    
    # Lambda函数
    square_lambda = lambda x: x ** 2
    
    print(f"   传统函数: square_func(5) = {square_func(5)}")
    print(f"   Lambda函数: square_lambda(5) = {square_lambda(5)}")
    print()
    
    # 在高阶函数中使用Lambda
    print("2. 在高阶函数中使用")
    
    numbers = [1, 2, 3, 4, 5]
    
    # map函数
    squares = list(map(lambda x: x ** 2, numbers))
    print(f"   map(lambda x: x**2, {numbers}) = {squares}")
    
    # filter函数
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"   filter(lambda x: x%2==0, {numbers}) = {evens}")
    
    # sorted函数
    students = [("张三", 85), ("李四", 92), ("王五", 78)]
    sorted_by_score = sorted(students, key=lambda student: student[1])
    print(f"   按成绩排序: {sorted_by_score}")
    print()
    
    # Lambda的限制
    print("3. Lambda函数的限制")
    print("   - 只能包含表达式，不能有语句")
    print("   - 不能有return语句")
    print("   - 不能有文档字符串")
    print("   - 复杂逻辑应该使用普通函数")
    
    # 适合Lambda的场景
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else 0
    }
    
    a, b = 10, 3
    for op_name, op_func in operations.items():
        result = op_func(a, b)
        print(f"   {op_name}({a}, {b}) = {result}")


def main():
    """主函数 - 演示所有函数功能"""
    print("Python基础语法学习 - 函数定义")
    print("=" * 50)
    
    demonstrate_basic_functions()
    demonstrate_parameters()
    demonstrate_variable_arguments()
    demonstrate_return_values()
    demonstrate_type_hints()
    demonstrate_docstrings()
    demonstrate_lambda_functions()
    
    print("\n学习总结:")
    print("1. Python使用def关键字定义函数")
    print("2. 支持位置参数、关键字参数、默认参数")
    print("3. *args和**kwargs支持可变参数")
    print("4. 可以返回多个值")
    print("5. 类型注解提高代码可读性")
    print("6. 文档字符串用于函数文档化")
    print("7. Lambda函数适用于简单的匿名函数")


if __name__ == "__main__":
    main() 