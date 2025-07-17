#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法 - 变量和基本数据类型
=====================================

本文件演示Python的基本数据类型，并与Java进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

from typing import Union, Optional
import sys


def demonstrate_basic_types():
    """
    演示Python基本数据类型
    对应Java的基本类型和包装类
    """
    print("=== Python基本数据类型演示 ===\n")
    
    # 1. 整数类型 (int) - 对应Java的int/Integer
    print("1. 整数类型 (int)")
    print("   Java对比: int/Integer/long/Long")
    
    # Python的int可以处理任意大小的整数，无需区分int和long
    small_int = 42
    big_int = 12345678901234567890123456789
    
    print(f"   小整数: {small_int}, 类型: {type(small_int)}")
    print(f"   大整数: {big_int}, 类型: {type(big_int)}")
    print(f"   大整数位数: {len(str(big_int))}")
    print(f"   系统最大int值: {sys.maxsize}")
    print()
    
    # 2. 浮点数类型 (float) - 对应Java的double/Double
    print("2. 浮点数类型 (float)")
    print("   Java对比: double/Double (Python没有float原始类型)")
    
    pi = 3.14159
    scientific = 1.5e-10
    
    print(f"   普通浮点数: {pi}, 类型: {type(pi)}")
    print(f"   科学计数法: {scientific}, 类型: {type(scientific)}")
    print(f"   浮点数精度: {sys.float_info.dig} 位")
    print()
    
    # 3. 布尔类型 (bool) - 对应Java的boolean/Boolean
    print("3. 布尔类型 (bool)")
    print("   Java对比: boolean/Boolean")
    
    is_python_fun = True
    is_java_difficult = False
    
    print(f"   真值: {is_python_fun}, 类型: {type(is_python_fun)}")
    print(f"   假值: {is_java_difficult}, 类型: {type(is_java_difficult)}")
    
    # Python的布尔值实际上是int的子类
    print(f"   True的数值: {int(is_python_fun)}")
    print(f"   False的数值: {int(is_java_difficult)}")
    print(f"   bool是int的子类: {isinstance(True, int)}")
    print()
    
    # 4. 字符串类型 (str) - 对应Java的String
    print("4. 字符串类型 (str)")
    print("   Java对比: String")
    
    name = "Python学习者"
    multiline = """这是一个
    多行字符串
    类似Java的文本块"""
    
    print(f"   字符串: {name}, 类型: {type(name)}")
    print(f"   字符串长度: {len(name)}")
    print(f"   多行字符串: {repr(multiline)}")
    print()
    
    # 5. 空值类型 (NoneType) - 对应Java的null
    print("5. 空值类型 (NoneType)")
    print("   Java对比: null")
    
    empty_value = None
    print(f"   空值: {empty_value}, 类型: {type(empty_value)}")
    print(f"   空值检查: {empty_value is None}")
    print()


def demonstrate_type_properties():
    """
    演示Python类型的特殊属性
    与Java的重要差异
    """
    print("=== Python类型特性 ===\n")
    
    # 1. 动态类型系统
    print("1. 动态类型系统 (vs Java静态类型)")
    
    # 同一个变量可以存储不同类型的值
    dynamic_var = 42
    print(f"   整数阶段: {dynamic_var}, 类型: {type(dynamic_var)}")
    
    dynamic_var = "现在是字符串"
    print(f"   字符串阶段: {dynamic_var}, 类型: {type(dynamic_var)}")
    
    dynamic_var = [1, 2, 3]
    print(f"   列表阶段: {dynamic_var}, 类型: {type(dynamic_var)}")
    print()
    
    # 2. 类型注解 (Python 3.5+)
    print("2. 类型注解 (类似Java的类型声明)")
    
    def annotated_function(name: str, age: int) -> str:
        """带类型注解的函数，类似Java方法签名"""
        return f"{name}今年{age}岁"
    
    # 类型注解只是提示，不会强制检查
    result = annotated_function("张三", 25)
    print(f"   正常调用: {result}")
    
    # 即使传入错误类型，Python也不会报错（需要类型检查工具）
    result2 = annotated_function(123, "二十五")  # 类型不匹配但能运行
    print(f"   错误类型调用: {result2}")
    print()
    
    # 3. 类型检查函数
    print("3. 运行时类型检查")
    
    def check_types(value):
        """检查值的类型"""
        print(f"   值: {value}")
        print(f"   类型: {type(value)}")
        print(f"   类型名: {type(value).__name__}")
        print(f"   是否为整数: {isinstance(value, int)}")
        print(f"   是否为数字: {isinstance(value, (int, float))}")
        print()
    
    check_types(42)
    check_types(3.14)
    check_types("hello")
    check_types(True)  # 注意：bool是int的子类


def demonstrate_variable_assignment():
    """
    演示Python变量赋值的特性
    与Java的重要差异
    """
    print("=== Python变量赋值特性 ===\n")
    
    # 1. 多重赋值
    print("1. 多重赋值 (Java需要分别赋值)")
    
    a = b = c = 100
    print(f"   a={a}, b={b}, c={c}")
    
    # 序列解包赋值
    x, y, z = 1, 2, 3
    print(f"   序列解包: x={x}, y={y}, z={z}")
    
    # 交换变量（Java需要临时变量）
    x, y = y, x
    print(f"   交换后: x={x}, y={y}")
    print()
    
    # 2. 变量命名规则
    print("2. 变量命名规则 (与Java的差异)")
    
    # Python推荐蛇形命名法，Java推荐驼峰命名法
    student_name = "张三"  # Python风格
    studentAge = 20       # Java风格（在Python中不推荐）
    
    print(f"   Python风格: {student_name}")
    print(f"   Java风格: {studentAge}")
    
    # 特殊变量
    _private_var = "私有变量（约定）"
    __magic_var__ = "魔术变量"
    
    print(f"   私有变量: {_private_var}")
    print(f"   魔术变量: {__magic_var__}")
    print()
    
    # 3. 变量作用域
    print("3. 变量作用域")
    
    global_var = "全局变量"
    
    def scope_demo():
        local_var = "局部变量"
        global global_var  # 声明使用全局变量
        global_var = "修改后的全局变量"
        
        print(f"   函数内 - 局部变量: {local_var}")
        print(f"   函数内 - 全局变量: {global_var}")
    
    print(f"   函数外 - 全局变量: {global_var}")
    scope_demo()
    print(f"   函数调用后 - 全局变量: {global_var}")


def demonstrate_constants():
    """
    演示Python中的常量约定
    与Java final关键字的对比
    """
    print("\n=== Python常量约定 ===\n")
    
    # Python没有真正的常量，只有约定
    print("1. 常量约定 (vs Java final)")
    
    # 约定：全大写表示常量
    PI = 3.14159
    MAX_CONNECTIONS = 100
    DATABASE_URL = "mysql://localhost:3306/test"
    
    print(f"   数学常量: {PI}")
    print(f"   配置常量: {MAX_CONNECTIONS}")
    print(f"   字符串常量: {DATABASE_URL}")
    
    # 注意：这些"常量"实际上可以被修改（与Java final不同）
    PI = 3.0  # 可以修改，但不推荐
    print(f"   修改后的PI: {PI} (不推荐这样做)")
    print()
    
    # 2. 真正的不可变对象
    print("2. 不可变对象 (类似Java final对象)")
    
    from typing import Final
    
    # Python 3.8+ 支持Final注解（需要类型检查工具）
    FINAL_VALUE: Final = 42
    
    # 元组是不可变的
    IMMUTABLE_TUPLE = (1, 2, 3)
    print(f"   不可变元组: {IMMUTABLE_TUPLE}")
    
    # 字符串也是不可变的
    IMMUTABLE_STRING = "不可变字符串"
    print(f"   不可变字符串: {IMMUTABLE_STRING}")


def main():
    """主函数 - 演示所有基本类型功能"""
    print("Python基础语法学习 - 变量和数据类型")
    print("=" * 50)
    
    demonstrate_basic_types()
    demonstrate_type_properties()
    demonstrate_variable_assignment()
    demonstrate_constants()
    
    print("\n学习总结:")
    print("1. Python是动态类型语言，变量无需声明类型")
    print("2. Python的int可以处理任意大小的整数")
    print("3. Python支持类型注解，但不强制类型检查")
    print("4. Python使用蛇形命名法，Java使用驼峰命名法")
    print("5. Python没有真正的常量，只有命名约定")
    print("6. Python支持多重赋值和序列解包")


if __name__ == "__main__":
    main() 