#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python vs Java - 变量和类型差异详解
===============================

本文件详细对比Python和Java在变量和数据类型方面的差异
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""


def demonstrate_type_system_differences():
    """
    演示类型系统的根本差异
    """
    print("=== 类型系统差异 ===\n")
    
    print("1. 静态类型 vs 动态类型")
    print("   Java: 编译时确定类型，运行时不可改变")
    print("   int number = 42;        // 类型固定为int")
    print("   number = \"hello\";       // 编译错误")
    print()
    
    print("   Python: 运行时确定类型，可以动态改变")
    # Python示例
    number = 42
    print(f"   number = {number} (类型: {type(number).__name__})")
    
    number = "hello"
    print(f"   number = '{number}' (类型: {type(number).__name__})")
    
    number = [1, 2, 3]
    print(f"   number = {number} (类型: {type(number).__name__})")
    print()
    
    print("2. 类型声明")
    print("   Java: 必须显式声明变量类型")
    print("   String name = \"张三\";")
    print("   int age = 25;")
    print("   List<String> names = new ArrayList<>();")
    print()
    
    print("   Python: 可选的类型注解（仅作提示）")
    name: str = "张三"
    age: int = 25
    from typing import List
    names: List[str] = ["张三", "李四"]
    
    print(f"   name: str = '{name}'")
    print(f"   age: int = {age}")
    print(f"   names: List[str] = {names}")
    print()


def demonstrate_primitive_vs_object():
    """
    演示原始类型与对象类型的差异
    """
    print("=== 原始类型 vs 对象类型 ===\n")
    
    print("1. Java的原始类型和包装类")
    print("   原始类型: int, double, boolean, char")
    print("   包装类: Integer, Double, Boolean, Character")
    print("   int i = 42;           // 栈上存储")
    print("   Integer obj = 42;     // 堆上存储（自动装箱）")
    print()
    
    print("2. Python的统一对象模型")
    print("   所有值都是对象，没有原始类型")
    
    # Python中所有值都是对象
    num = 42
    text = "hello"
    flag = True
    
    print(f"   数字的方法: {num.__class__.__name__}")
    print(f"   数字的ID: {id(num)}")
    print(f"   字符串的方法: {len(text.__dir__())} 个方法")
    print(f"   布尔值的父类: {flag.__class__.__bases__}")
    print()
    
    print("3. 内存和性能影响")
    print("   Java: 原始类型性能更好，占用内存更少")
    print("   Python: 统一但有性能开销，小整数有缓存优化")
    
    # Python的小整数缓存
    a = 100
    b = 100
    c = 1000
    d = 1000
    
    print(f"   小整数缓存: {a} is {b} = {a is b}")
    print(f"   大整数: {c} is {d} = {c is d}")


def demonstrate_null_vs_none():
    """
    演示null vs None的差异
    """
    print("\n=== null vs None ===\n")
    
    print("1. 空值表示")
    print("   Java: null (小写关键字)")
    print("   String name = null;")
    print("   if (name == null) { ... }")
    print()
    
    print("   Python: None (首字母大写，单例对象)")
    name = None
    print(f"   name = {name}")
    print(f"   type(None) = {type(None)}")
    print(f"   None的ID: {id(None)}")
    
    # 检查None的方式
    if name is None:
        print("   正确的None检查: name is None")
    
    if name == None:  # 可以但不推荐
        print("   可行但不推荐: name == None")
    print()
    
    print("2. 空值检查最佳实践")
    print("   Java: obj == null 或 Objects.isNull(obj)")
    print("   Python: obj is None (推荐) 或 obj == None")
    
    # 演示差异
    class AlwaysEqual:
        def __eq__(self, other):
            return True
    
    weird_obj = AlwaysEqual()
    print(f"   特殊对象 == None: {weird_obj == None}")
    print(f"   特殊对象 is None: {weird_obj is None}")


def demonstrate_string_differences():
    """
    演示字符串处理的差异
    """
    print("\n=== 字符串差异 ===\n")
    
    print("1. 字符串不可变性")
    print("   Java: String不可变，StringBuilder可变")
    print("   String s = \"hello\";")
    print("   s += \" world\";  // 创建新对象")
    print()
    
    print("   Python: str不可变，列表可用于可变操作")
    s = "hello"
    original_id = id(s)
    s += " world"
    new_id = id(s)
    
    print(f"   原始字符串ID: {original_id}")
    print(f"   修改后ID: {new_id}")
    print(f"   是否为同一对象: {original_id == new_id}")
    print()
    
    print("2. 字符串字面量池")
    print("   Java: 字符串池在方法区")
    print("   Python: 字符串驻留机制")
    
    # Python字符串驻留
    a = "hello"
    b = "hello"
    c = "hello world"
    d = "hello world"
    
    print(f"   简单字符串: '{a}' is '{b}' = {a is b}")
    print(f"   复杂字符串: '{c}' is '{d}' = {c is d}")
    print()
    
    print("3. 字符串格式化")
    print("   Java: String.format(), MessageFormat, StringBuilder")
    print("   System.out.printf(\"Name: %s, Age: %d\", name, age);")
    print()
    
    print("   Python: 多种格式化方式")
    name = "张三"
    age = 25
    
    # % 格式化
    msg1 = "姓名: %s, 年龄: %d" % (name, age)
    print(f"   % 格式化: {msg1}")
    
    # str.format()
    msg2 = "姓名: {}, 年龄: {}".format(name, age)
    print(f"   format方法: {msg2}")
    
    # f-string (Python 3.6+)
    msg3 = f"姓名: {name}, 年龄: {age}"
    print(f"   f-string: {msg3}")


def demonstrate_collection_initialization():
    """
    演示集合初始化的差异
    """
    print("\n=== 集合初始化差异 ===\n")
    
    print("1. 数组/列表初始化")
    print("   Java:")
    print("   int[] arr = {1, 2, 3};")
    print("   int[] arr2 = new int[]{1, 2, 3};")
    print("   List<String> list = Arrays.asList(\"a\", \"b\", \"c\");")
    print()
    
    print("   Python:")
    arr = [1, 2, 3]
    arr2 = list([1, 2, 3])
    arr3 = [i for i in range(1, 4)]  # 列表推导式
    
    print(f"   列表字面量: {arr}")
    print(f"   list()构造: {arr2}")
    print(f"   列表推导式: {arr3}")
    print()
    
    print("2. 字典/Map初始化")
    print("   Java:")
    print("   Map<String, Integer> map = new HashMap<>();")
    print("   map.put(\"age\", 25);")
    print("   // Java 9+: Map.of(\"age\", 25)")
    print()
    
    print("   Python:")
    map1 = {"age": 25, "score": 98.5}
    map2 = dict(age=25, score=98.5)
    map3 = {k: v for k, v in [("age", 25), ("score", 98.5)]}
    
    print(f"   字典字面量: {map1}")
    print(f"   dict()构造: {map2}")
    print(f"   字典推导式: {map3}")


def demonstrate_variable_scope():
    """
    演示变量作用域的差异
    """
    print("\n=== 变量作用域差异 ===\n")
    
    print("1. 块级作用域")
    print("   Java: 有块级作用域")
    print("   {")
    print("       int x = 10;  // 块内变量")
    print("   }")
    print("   // x在此处不可访问")
    print()
    
    print("   Python: 无块级作用域，只有函数作用域")
    if True:
        x = 10  # 在if块内定义
    print(f"   在if块外访问x: {x}")  # 仍然可以访问
    print()
    
    print("2. 变量提升")
    print("   Java: 无变量提升，必须先声明后使用")
    print("   Python: 有LEGB规则(Local->Enclosing->Global->Built-in)")
    
    def scope_demo():
        print(f"   访问全局变量y: {y}")  # 可以访问后面定义的全局变量
    
    y = 20
    scope_demo()
    print()
    
    print("3. 常量定义")
    print("   Java: final关键字定义常量")
    print("   final int MAX_SIZE = 100;")
    print()
    
    print("   Python: 约定使用大写，无强制不可变")
    MAX_SIZE = 100  # 约定为常量，但可以修改
    print(f"   MAX_SIZE = {MAX_SIZE}")
    MAX_SIZE = 200  # 可以修改，但违反约定
    print(f"   修改后: MAX_SIZE = {MAX_SIZE}")


def demonstrate_performance_considerations():
    """
    演示性能考虑
    """
    print("\n=== 性能考虑 ===\n")
    
    print("1. 类型检查开销")
    print("   Java: 编译时类型检查，运行时无开销")
    print("   Python: 运行时类型检查，有性能开销")
    print()
    
    print("2. 对象创建开销")
    print("   Java: 原始类型在栈上，对象在堆上")
    print("   Python: 所有值都是对象，在堆上分配")
    
    # 演示Python的对象开销
    import sys
    
    num = 42
    text = "hello"
    lst = [1, 2, 3]
    
    print(f"   整数占用内存: {sys.getsizeof(num)} 字节")
    print(f"   字符串占用内存: {sys.getsizeof(text)} 字节")
    print(f"   列表占用内存: {sys.getsizeof(lst)} 字节")
    print()
    
    print("3. 性能优化建议")
    print("   Java: 使用原始类型，避免自动装箱")
    print("   Python: 使用内置函数，避免频繁类型转换")
    
    # Python性能优化示例
    import time
    
    # 慢速方式：字符串拼接
    start = time.time()
    result = ""
    for i in range(1000):
        result += str(i)
    slow_time = time.time() - start
    
    # 快速方式：列表join
    start = time.time()
    result2 = "".join(str(i) for i in range(1000))
    fast_time = time.time() - start
    
    print(f"   字符串拼接耗时: {slow_time:.6f}秒")
    print(f"   列表join耗时: {fast_time:.6f}秒")
    print(f"   性能提升: {slow_time/fast_time:.1f}倍")


def main():
    """主函数 - 演示所有差异"""
    print("Python vs Java - 变量和类型差异详解")
    print("=" * 50)
    
    demonstrate_type_system_differences()
    demonstrate_primitive_vs_object()
    demonstrate_null_vs_none()
    demonstrate_string_differences()
    demonstrate_collection_initialization()
    demonstrate_variable_scope()
    demonstrate_performance_considerations()
    
    print("\n重要差异总结:")
    print("1. Python是动态类型，Java是静态类型")
    print("2. Python所有值都是对象，Java有原始类型和对象类型")
    print("3. Python使用None，Java使用null")
    print("4. Python无块级作用域，Java有块级作用域")
    print("5. Python字符串格式化更灵活")
    print("6. Python集合初始化语法更简洁")
    print("7. Python有性能开销，但开发效率更高")


if __name__ == "__main__":
    main() 