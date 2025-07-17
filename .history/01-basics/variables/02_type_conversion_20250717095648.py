#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法 - 类型转换
========================

本文件演示Python的类型转换，并与Java进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

import decimal
from fractions import Fraction


def demonstrate_explicit_conversion():
    """
    演示显式类型转换
    对应Java的强制类型转换和包装类转换
    """
    print("=== 显式类型转换 ===\n")
    
    # 1. 数字类型转换
    print("1. 数字类型转换")
    
    # 整数转换
    float_num = 3.14
    int_from_float = int(float_num)  # 截断小数部分
    print(f"   浮点数转整数: {float_num} -> {int_from_float}")
    
    str_num = "123"
    int_from_str = int(str_num)
    print(f"   字符串转整数: '{str_num}' -> {int_from_str}")
    
    # 浮点数转换
    int_num = 42
    float_from_int = float(int_num)
    print(f"   整数转浮点数: {int_num} -> {float_from_int}")
    
    str_float = "3.14159"
    float_from_str = float(str_float)
    print(f"   字符串转浮点数: '{str_float}' -> {float_from_str}")
    
    # Java对比说明
    print("\n   Java对比:")
    print("   int i = (int)3.14;           // 强制转换")
    print("   int j = Integer.parseInt(\"123\");  // 包装类转换")
    print("   double d = Double.parseDouble(\"3.14\");")
    print()
    
    # 2. 字符串转换
    print("2. 字符串转换")
    
    # 各种类型转字符串
    num = 42
    pi = 3.14159
    flag = True
    none_val = None
    
    print(f"   整数转字符串: {num} -> '{str(num)}'")
    print(f"   浮点数转字符串: {pi} -> '{str(pi)}'")
    print(f"   布尔值转字符串: {flag} -> '{str(flag)}'")
    print(f"   None转字符串: {none_val} -> '{str(none_val)}'")
    
    # Java对比
    print("\n   Java对比:")
    print("   String s = String.valueOf(42);")
    print("   String s = Integer.toString(42);")
    print()
    
    # 3. 布尔值转换
    print("3. 布尔值转换")
    
    # 各种值转布尔值
    values = [0, 1, -1, "", "hello", [], [1, 2], {}, {"key": "value"}, None]
    
    for value in values:
        bool_val = bool(value)
        print(f"   {repr(value)} -> {bool_val}")
    
    print("\n   规则: 以下值为False，其他都为True")
    print("   - 数字0, 0.0")
    print("   - 空字符串 ''")
    print("   - 空集合 [], {}, ()")
    print("   - None")
    print()


def demonstrate_implicit_conversion():
    """
    演示隐式类型转换
    Python的类型提升规则
    """
    print("=== 隐式类型转换 ===\n")
    
    # 1. 数字运算中的类型提升
    print("1. 数字运算中的类型提升")
    
    int_val = 10
    float_val = 3.14
    
    # int + float -> float
    result = int_val + float_val
    print(f"   int + float: {int_val} + {float_val} = {result} (类型: {type(result)})")
    
    # int / int -> float (Python 3特性)
    division_result = 10 / 3
    print(f"   int / int: 10 / 3 = {division_result} (类型: {type(division_result)})")
    
    # 整数除法
    floor_division = 10 // 3
    print(f"   整数除法: 10 // 3 = {floor_division} (类型: {type(floor_division)})")
    
    print("\n   Java对比:")
    print("   Java中 10/3 = 3 (整数除法)")
    print("   Java中 10.0/3 = 3.333... (浮点除法)")
    print("   Python中 10/3 总是返回float")
    print()
    
    # 2. 字符串上下文中的转换
    print("2. 字符串格式化中的转换")
    
    name = "张三"
    age = 25
    score = 98.5
    
    # f-string自动转换
    message1 = f"{name}今年{age}岁，成绩是{score}分"
    print(f"   f-string: {message1}")
    
    # format方法
    message2 = "{}今年{}岁，成绩是{}分".format(name, age, score)
    print(f"   format: {message2}")
    
    # % 格式化
    message3 = "%s今年%d岁，成绩是%.1f分" % (name, age, score)
    print(f"   % 格式化: {message3}")
    print()


def demonstrate_safe_conversion():
    """
    演示安全的类型转换
    异常处理和边界条件
    """
    print("=== 安全的类型转换 ===\n")
    
    # 1. 处理转换异常
    print("1. 处理转换异常")
    
    def safe_int_conversion(value):
        """安全的整数转换函数"""
        try:
            return int(value), None
        except ValueError as e:
            return None, str(e)
        except TypeError as e:
            return None, str(e)
    
    test_values = ["123", "3.14", "abc", "", None, [1, 2, 3]]
    
    for value in test_values:
        result, error = safe_int_conversion(value)
        if error:
            print(f"   {repr(value)} -> 转换失败: {error}")
        else:
            print(f"   {repr(value)} -> {result}")
    print()
    
    # 2. 使用默认值
    print("2. 使用默认值的转换")
    
    def int_with_default(value, default=0):
        """带默认值的整数转换"""
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    test_inputs = ["100", "abc", None, "3.7"]
    for inp in test_inputs:
        result = int_with_default(inp, -1)
        print(f"   {repr(inp)} -> {result}")
    print()
    
    # 3. 检查转换前的类型
    print("3. 转换前的类型检查")
    
    def smart_conversion(value):
        """智能类型转换"""
        if isinstance(value, int):
            return value, "已是整数"
        elif isinstance(value, float):
            return int(value), "浮点数转整数（截断）"
        elif isinstance(value, str):
            if value.isdigit():
                return int(value), "数字字符串转整数"
            else:
                return None, "非数字字符串"
        else:
            return None, f"不支持的类型: {type(value)}"
    
    test_cases = [42, 3.14, "123", "abc", True, None]
    for case in test_cases:
        result, message = smart_conversion(case)
        print(f"   {repr(case)} -> {result} ({message})")


def demonstrate_advanced_conversion():
    """
    演示高级类型转换
    包括数字系统、精度控制等
    """
    print("\n=== 高级类型转换 ===\n")
    
    # 1. 进制转换
    print("1. 进制转换")
    
    decimal_num = 255
    print(f"   十进制: {decimal_num}")
    print(f"   二进制: {bin(decimal_num)}")
    print(f"   八进制: {oct(decimal_num)}")
    print(f"   十六进制: {hex(decimal_num)}")
    
    # 从其他进制转换回来
    binary_str = "0b11111111"
    octal_str = "0o377"
    hex_str = "0xff"
    
    print(f"   从二进制: {binary_str} -> {int(binary_str, 0)}")
    print(f"   从八进制: {octal_str} -> {int(octal_str, 0)}")
    print(f"   从十六进制: {hex_str} -> {int(hex_str, 0)}")
    print()
    
    # 2. 精度控制
    print("2. 精度控制")
    
    # 使用Decimal进行精确计算
    from decimal import Decimal, getcontext
    
    # 设置精度
    getcontext().prec = 10
    
    d1 = Decimal('0.1')
    d2 = Decimal('0.2')
    d3 = d1 + d2
    
    print(f"   普通浮点数: 0.1 + 0.2 = {0.1 + 0.2}")
    print(f"   Decimal: 0.1 + 0.2 = {d3}")
    
    # 分数计算
    frac1 = Fraction(1, 3)
    frac2 = Fraction(1, 6)
    frac_sum = frac1 + frac2
    
    print(f"   分数计算: 1/3 + 1/6 = {frac_sum} = {float(frac_sum)}")
    print()
    
    # 3. 自定义对象转换
    print("3. 自定义对象转换")
    
    class Student:
        def __init__(self, name, age):
            self.name = name
            self.age = age
        
        def __str__(self):
            """定义str()转换"""
            return f"Student({self.name}, {self.age})"
        
        def __repr__(self):
            """定义repr()转换"""
            return f"Student(name='{self.name}', age={self.age})"
        
        def __int__(self):
            """定义int()转换"""
            return self.age
        
        def __float__(self):
            """定义float()转换"""
            return float(self.age)
        
        def __bool__(self):
            """定义bool()转换"""
            return self.age > 0
    
    student = Student("李四", 20)
    
    print(f"   str(student): {str(student)}")
    print(f"   repr(student): {repr(student)}")
    print(f"   int(student): {int(student)}")
    print(f"   float(student): {float(student)}")
    print(f"   bool(student): {bool(student)}")


def main():
    """主函数 - 演示所有类型转换功能"""
    print("Python基础语法学习 - 类型转换")
    print("=" * 50)
    
    demonstrate_explicit_conversion()
    demonstrate_implicit_conversion()
    demonstrate_safe_conversion()
    demonstrate_advanced_conversion()
    
    print("\n学习总结:")
    print("1. Python提供丰富的内置类型转换函数")
    print("2. 数字运算会自动进行类型提升")
    print("3. Python 3中整数除法总是返回float")
    print("4. 类型转换可能抛出异常，需要适当处理")
    print("5. 可以通过魔术方法自定义对象的类型转换")
    print("6. 使用Decimal和Fraction可以进行精确计算")


if __name__ == "__main__":
    main() 