#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法 - 字符串与Java对比
==============================

本文件详细对比Python字符串与Java String的差异
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

import sys
import time


def demonstrate_string_immutability():
    """
    演示字符串不可变性
    Python vs Java
    """
    print("=== 字符串不可变性 ===\n")
    
    print("Java vs Python字符串不可变性:")
    print("Java:")
    print("   String str = \"hello\";")
    print("   str += \"world\"; // 创建新的String对象")
    print("   StringBuilder/StringBuffer用于可变操作")
    print()
    
    print("Python:")
    print("   str = \"hello\"")
    print("   str += \"world\"  # 创建新的str对象")
    print("   list用于可变字符操作，然后join()")
    print()
    
    # 1. 验证不可变性
    print("1. 验证字符串不可变性")
    
    original = "hello"
    original_id = id(original)
    print(f"   原字符串: '{original}', id: {original_id}")
    
    # 尝试"修改"字符串
    modified = original + " world"
    modified_id = id(modified)
    print(f"   连接后: '{modified}', id: {modified_id}")
    print(f"   ID是否相同: {original_id == modified_id}")
    
    # 原字符串不变
    print(f"   原字符串仍然是: '{original}'")
    print()
    
    # 2. 字符串连接的性能影响
    print("2. 大量字符串连接的性能对比")
    
    def inefficient_concat(words, count=1000):
        """低效的字符串连接 (类似Java中直接用+)"""
        result = ""
        for i in range(count):
            result += words[i % len(words)]
        return result
    
    def efficient_concat(words, count=1000):
        """高效的字符串连接 (类似Java中用StringBuilder)"""
        parts = []
        for i in range(count):
            parts.append(words[i % len(words)])
        return "".join(parts)
    
    test_words = ["Python", "Java", "Hello", "World"]
    
    # 性能测试
    start_time = time.time()
    result1 = inefficient_concat(test_words)
    inefficient_time = time.time() - start_time
    
    start_time = time.time()
    result2 = efficient_concat(test_words)
    efficient_time = time.time() - start_time
    
    print(f"   低效连接 (+ 操作): {inefficient_time:.6f}秒")
    print(f"   高效连接 (join): {efficient_time:.6f}秒")
    print(f"   性能提升: {inefficient_time / efficient_time:.2f}倍")
    print()


def demonstrate_string_comparison():
    """
    演示字符串比较
    Python vs Java
    """
    print("=== 字符串比较 ===\n")
    
    print("Java vs Python字符串比较:")
    print("Java:")
    print("   str1.equals(str2)        // 内容比较")
    print("   str1 == str2             // 引用比较")
    print("   str1.compareTo(str2)     // 字典序比较")
    print()
    
    print("Python:")
    print("   str1 == str2             // 内容比较")
    print("   str1 is str2             // 引用比较")
    print("   str1 < str2              // 字典序比较")
    print()
    
    # 1. 内容比较
    print("1. 内容比较")
    
    str1 = "hello"
    str2 = "hello"
    str3 = "Hello"
    
    print(f"   str1 = '{str1}'")
    print(f"   str2 = '{str2}'")
    print(f"   str3 = '{str3}'")
    print()
    
    print(f"   str1 == str2: {str1 == str2}")  # True
    print(f"   str1 == str3: {str1 == str3}")  # False
    print(f"   str1.lower() == str3.lower(): {str1.lower() == str3.lower()}")  # True
    print()
    
    # 2. 引用比较
    print("2. 引用比较 (is vs ==)")
    
    # 字符串驻留 (String Interning)
    interned1 = "hello"
    interned2 = "hello"
    
    # 运行时创建的字符串
    runtime1 = "hel" + "lo"
    runtime2 = "".join(['h', 'e', 'l', 'l', 'o'])
    
    print(f"   字符串驻留:")
    print(f"     interned1 is interned2: {interned1 is interned2}")
    print(f"     id(interned1): {id(interned1)}")
    print(f"     id(interned2): {id(interned2)}")
    print()
    
    print(f"   运行时创建:")
    print(f"     runtime1 == runtime2: {runtime1 == runtime2}")
    print(f"     runtime1 is runtime2: {runtime1 is runtime2}")
    print(f"     id(runtime1): {id(runtime1)}")
    print(f"     id(runtime2): {id(runtime2)}")
    print()
    
    # 3. 字典序比较
    print("3. 字典序比较")
    
    words = ["apple", "banana", "cherry", "Apple", "Banana"]
    
    print("   原始顺序:", words)
    print("   排序后:", sorted(words))
    print("   忽略大小写排序:", sorted(words, key=str.lower))
    
    # 比较示例
    comparisons = [
        ("apple", "banana"),
        ("Apple", "apple"),
        ("banana", "Banana"),
        ("123", "abc")
    ]
    
    print("\n   字符串比较结果:")
    for s1, s2 in comparisons:
        print(f"     '{s1}' < '{s2}': {s1 < s2}")
        print(f"     '{s1}' > '{s2}': {s1 > s2}")
    print()


def demonstrate_string_interning():
    """
    演示字符串驻留机制
    """
    print("=== 字符串驻留机制 ===\n")
    
    print("Java vs Python字符串驻留:")
    print("Java:")
    print("   String literal自动驻留到字符串池")
    print("   String.intern()手动驻留")
    print()
    
    print("Python:")
    print("   标识符样式的字符串自动驻留")
    print("   sys.intern()手动驻留")
    print()
    
    # 1. 自动驻留的情况
    print("1. 自动驻留的情况")
    
    # 标识符样式的字符串会被驻留
    auto1 = "hello_world"
    auto2 = "hello_world"
    
    # 包含特殊字符的短字符串也可能被驻留
    special1 = "hello"
    special2 = "hello"
    
    print(f"   标识符样式:")
    print(f"     'hello_world' is 'hello_world': {auto1 is auto2}")
    print(f"   简单字符串:")
    print(f"     'hello' is 'hello': {special1 is special2}")
    print()
    
    # 2. 不会自动驻留的情况
    print("2. 不会自动驻留的情况")
    
    # 包含空格或特殊字符的长字符串
    no_intern1 = "hello world with spaces"
    no_intern2 = "hello world with spaces"
    
    # 运行时动态创建的字符串
    dynamic1 = "hello" + " " + "world"
    dynamic2 = "hello" + " " + "world"
    
    print(f"   包含空格的字符串:")
    print(f"     == 比较: {no_intern1 == no_intern2}")
    print(f"     is 比较: {no_intern1 is no_intern2}")
    
    print(f"   动态创建的字符串:")
    print(f"     == 比较: {dynamic1 == dynamic2}")
    print(f"     is 比较: {dynamic1 is dynamic2}")
    print()
    
    # 3. 手动驻留
    print("3. 手动驻留 sys.intern()")
    
    manual1 = sys.intern("hello world manual")
    manual2 = sys.intern("hello world manual")
    
    print(f"   手动驻留的字符串:")
    print(f"     sys.intern('hello world manual') is sys.intern('hello world manual'): {manual1 is manual2}")
    
    # 与已存在字符串的驻留
    existing = "hello world manual"
    interned_existing = sys.intern(existing)
    
    print(f"     sys.intern(existing) is manual1: {interned_existing is manual1}")
    print()


def demonstrate_unicode_handling():
    """
    演示Unicode处理
    Python vs Java
    """
    print("=== Unicode处理 ===\n")
    
    print("Java vs Python Unicode处理:")
    print("Java:")
    print("   String内部使用UTF-16编码")
    print("   char是16位，可能需要代理对处理某些字符")
    print("   length()返回UTF-16代码单元数量")
    print()
    
    print("Python 3:")
    print("   str内部使用最优的Unicode表示")
    print("   len()返回Unicode字符数量")
    print("   完全的Unicode支持")
    print()
    
    # 1. 基本Unicode字符
    print("1. 基本Unicode字符")
    
    unicode_text = "Hello 世界 🌍 🐍"
    
    print(f"   文本: '{unicode_text}'")
    print(f"   字符数: {len(unicode_text)}")
    print(f"   字节数 (UTF-8): {len(unicode_text.encode('utf-8'))}")
    print(f"   字节数 (UTF-16): {len(unicode_text.encode('utf-16'))}")
    print()
    
    # 2. 逐字符分析
    print("2. 逐字符分析")
    
    for i, char in enumerate(unicode_text):
        if not char.isspace():
            print(f"   [{i}] '{char}' -> U+{ord(char):04X} ({char.encode('utf-8')})")
    print()
    
    # 3. Unicode规范化
    print("3. Unicode规范化")
    
    import unicodedata
    
    # 组合字符 vs 预组合字符
    composed = "café"  # é 是预组合字符
    decomposed = "cafe\u0301"  # e + 组合重音符
    
    print(f"   预组合: '{composed}' (长度: {len(composed)})")
    print(f"   分解式: '{decomposed}' (长度: {len(decomposed)})")
    print(f"   相等性: {composed == decomposed}")
    
    # 规范化比较
    nfc_composed = unicodedata.normalize('NFC', composed)
    nfc_decomposed = unicodedata.normalize('NFC', decomposed)
    
    print(f"   NFC规范化后相等: {nfc_composed == nfc_decomposed}")
    print()
    
    # 4. 字符分类
    print("4. Unicode字符分类")
    
    test_chars = ['A', '中', '🐍', '½', '\n', ' ']
    
    for char in test_chars:
        category = unicodedata.category(char)
        name = unicodedata.name(char, "无名称")
        print(f"   '{char}' -> 类别: {category}, 名称: {name}")
    print()


def demonstrate_string_methods_comparison():
    """
    演示字符串方法对比
    Python vs Java
    """
    print("=== 字符串方法对比 ===\n")
    
    # 方法对照表
    method_comparison = [
        ("Python方法", "Java方法", "功能描述", "示例"),
        ("-" * 15, "-" * 15, "-" * 20, "-" * 30),
        ("len(str)", "str.length()", "获取长度", "len('hello') -> 5"),
        ("str.upper()", "str.toUpperCase()", "转大写", "'hello'.upper() -> 'HELLO'"),
        ("str.lower()", "str.toLowerCase()", "转小写", "'HELLO'.lower() -> 'hello'"),
        ("str.strip()", "str.trim()", "去除首尾空白", "' hello '.strip() -> 'hello'"),
        ("str.find()", "str.indexOf()", "查找子字符串", "'hello'.find('ll') -> 2"),
        ("str.replace()", "str.replace()", "替换子字符串", "'hello'.replace('l', 'L') -> 'heLLo'"),
        ("str.split()", "str.split()", "分割字符串", "'a,b,c'.split(',') -> ['a','b','c']"),
        ("''.join(list)", "String.join()", "连接字符串", "','.join(['a','b']) -> 'a,b'"),
        ("str.startswith()", "str.startsWith()", "检查前缀", "'hello'.startswith('he') -> True"),
        ("str.endswith()", "str.endsWith()", "检查后缀", "'hello'.endswith('lo') -> True"),
        ("str[start:end]", "str.substring()", "子字符串", "'hello'[1:4] -> 'ell'"),
        ("'text' in str", "str.contains()", "包含检查", "'ll' in 'hello' -> True"),
    ]
    
    print("Python vs Java字符串方法对照:")
    print()
    
    for row in method_comparison:
        print(f"   {row[0]:<15} | {row[1]:<20} | {row[2]:<15} | {row[3]}")
    print()
    
    # 实际示例
    print("实际示例对比:")
    
    test_string = "  Hello, Python World!  "
    print(f"   测试字符串: '{test_string}'")
    print()
    
    examples = [
        ("长度", f"len('{test_string.strip()}') = {len(test_string.strip())}"),
        ("大写", f"'{test_string.strip()}'.upper() = '{test_string.strip().upper()}'"),
        ("去空白", f"'{test_string}'.strip() = '{test_string.strip()}'"),
        ("查找", f"'{test_string.strip()}'.find('Python') = {test_string.strip().find('Python')}"),
        ("替换", f"'{test_string.strip()}'.replace('Python', 'Java') = '{test_string.strip().replace('Python', 'Java')}'"),
        ("分割", f"'{test_string.strip()}'.split(' ') = {test_string.strip().split(' ')}"),
        ("切片", f"'{test_string.strip()}'[7:13] = '{test_string.strip()[7:13]}'"),
        ("包含", f"'Python' in '{test_string.strip()}' = {'Python' in test_string.strip()}"),
    ]
    
    for desc, example in examples:
        print(f"   {desc}: {example}")
    print()


def demonstrate_performance_differences():
    """
    演示性能差异
    """
    print("=== 性能差异分析 ===\n")
    
    def time_operation(name, operation, iterations=10000):
        start_time = time.time()
        for _ in range(iterations):
            result = operation()
        end_time = time.time()
        duration = end_time - start_time
        print(f"   {name}: {duration:.6f}秒 ({iterations}次)")
        return duration
    
    # 1. 字符串连接性能
    print("1. 字符串连接性能 (Python vs Java概念对比)")
    
    words = ["Python", "is", "awesome", "and", "powerful"] * 100
    
    def concat_plus():
        """类似Java中用+连接 (低效)"""
        result = ""
        for word in words:
            result += word + " "
        return result
    
    def concat_join():
        """类似Java中用StringBuilder (高效)"""
        return " ".join(words)
    
    def concat_list():
        """使用列表累积再join"""
        parts = []
        for word in words:
            parts.append(word)
        return " ".join(parts)
    
    time_operation("+ 连接 (低效)", concat_plus, 100)
    time_operation("join 方法 (推荐)", concat_join, 1000)
    time_operation("列表累积+join", concat_list, 1000)
    print()
    
    # 2. 字符串查找性能
    print("2. 字符串查找性能")
    
    large_text = "Python " * 1000 + "target" + " text" * 1000
    
    def find_with_in():
        return "target" in large_text
    
    def find_with_find():
        return large_text.find("target") != -1
    
    def find_with_index():
        try:
            large_text.index("target")
            return True
        except ValueError:
            return False
    
    time_operation("in 运算符", find_with_in, 1000)
    time_operation("find 方法", find_with_find, 1000)
    time_operation("index 方法", find_with_index, 1000)
    print()
    
    # 3. 内存使用对比
    print("3. 内存使用分析")
    
    small_str = "hello"
    medium_str = "hello world " * 100
    large_str = "hello world " * 10000
    
    print(f"   小字符串 ('{small_str[:10]}...'): {sys.getsizeof(small_str)} 字节")
    print(f"   中等字符串 ({len(medium_str)} 字符): {sys.getsizeof(medium_str)} 字节")
    print(f"   大字符串 ({len(large_str)} 字符): {sys.getsizeof(large_str)} 字节")
    print()


def demonstrate_best_practices():
    """
    演示最佳实践
    从Java到Python的迁移建议
    """
    print("=== 最佳实践和迁移建议 ===\n")
    
    print("从Java String到Python str的迁移建议:")
    print()
    
    practices = [
        ("字符串比较", 
         "Java: str1.equals(str2)", 
         "Python: str1 == str2",
         "✓ Python中直接用==比较内容"),
        
        ("空字符串检查", 
         "Java: str.isEmpty() 或 str.length() == 0", 
         "Python: not str 或 len(str) == 0",
         "✓ Python中空字符串是falsy"),
        
        ("字符串连接", 
         "Java: StringBuilder.append()", 
         "Python: ''.join(list) 或 f-string",
         "✓ 避免在循环中使用+连接"),
        
        ("字符串格式化", 
         "Java: String.format() 或 printf", 
         "Python: f-string (推荐)",
         "✓ f-string性能最好，语法最清晰"),
        
        ("子字符串", 
         "Java: str.substring(start, end)", 
         "Python: str[start:end]",
         "✓ Python切片语法更灵活"),
        
        ("字符串分割", 
         "Java: str.split(regex)", 
         "Python: str.split(delimiter)",
         "⚠ Python的split默认不是正则表达式"),
        
        ("大小写转换", 
         "Java: str.toUpperCase()", 
         "Python: str.upper()",
         "✓ 方法名更简洁"),
        
        ("去除空白", 
         "Java: str.trim()", 
         "Python: str.strip()",
         "✓ Python还有lstrip()和rstrip()"),
    ]
    
    for topic, java_way, python_way, note in practices:
        print(f"   {topic}:")
        print(f"     Java:   {java_way}")
        print(f"     Python: {python_way}")
        print(f"     {note}")
        print()
    
    print("Python字符串的独特优势:")
    advantages = [
        "切片语法：str[start:end:step] 比Java更灵活",
        "多种引号：单引号、双引号、三引号支持",
        "原始字符串：r'string' 避免转义问题",
        "链式操作：str.strip().lower().split()",
        "成员检查：'sub' in string 比Java更直观",
        "负索引：str[-1] 获取最后一个字符",
        "f-string：直接在字符串中嵌入表达式",
        "Unicode：内置完整Unicode支持"
    ]
    
    for i, advantage in enumerate(advantages, 1):
        print(f"   {i}. {advantage}")
    print()
    
    print("需要注意的差异:")
    differences = [
        "Python字符串是不可变的，修改操作会创建新对象",
        "Python的split()默认不支持正则表达式，需要用re.split()",
        "Python字符串比较是按Unicode码点顺序，不是本地化排序",
        "Python的字符串驻留机制与Java略有不同",
        "Python字符串索引越界会抛出IndexError，不像Java返回异常"
    ]
    
    for i, diff in enumerate(differences, 1):
        print(f"   {i}. {diff}")


def main():
    """主函数 - 演示所有对比内容"""
    print("Python基础语法学习 - 字符串与Java对比")
    print("=" * 60)
    
    demonstrate_string_immutability()
    demonstrate_string_comparison()
    demonstrate_string_interning()
    demonstrate_unicode_handling()
    demonstrate_string_methods_comparison()
    demonstrate_performance_differences()
    demonstrate_best_practices()
    
    print("\n学习总结:")
    print("1. Python字符串与Java String都是不可变的")
    print("2. Python使用==进行内容比较，更直观")
    print("3. Python有更灵活的切片语法")
    print("4. Python的f-string是最佳格式化方式")
    print("5. Python内置完整的Unicode支持")
    print("6. 注意字符串连接的性能影响")
    print("7. 掌握Python独有的字符串特性")


if __name__ == "__main__":
    main() 