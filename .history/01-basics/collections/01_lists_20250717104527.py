#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法 - 列表(List)
==========================

本文件演示Python的列表类型，并与Java ArrayList进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

from typing import List, Any
import copy
import time


def demonstrate_list_creation():
    """
    演示列表创建的各种方式
    与Java ArrayList对比
    """
    print("=== 列表创建 ===\n")
    
    print("Java ArrayList vs Python List:")
    print("Java:")
    print("   List<String> list = new ArrayList<>();")
    print("   List<String> list = Arrays.asList(\"a\", \"b\", \"c\");")
    print("   List<Integer> numbers = List.of(1, 2, 3); // Java 9+")
    print()
    
    print("Python:")
    print("   list = []")
    print("   list = [\"a\", \"b\", \"c\"]")
    print("   list = list(iterable)")
    print()
    
    # 1. 空列表
    print("1. 创建空列表")
    empty_list1 = []
    empty_list2 = list()
    
    print(f"   [] = {empty_list1}")
    print(f"   list() = {empty_list2}")
    print()
    
    # 2. 带初始值的列表
    print("2. 带初始值的列表")
    fruits = ["苹果", "香蕉", "橙子", "葡萄"]
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, "hello", 3.14, True, None]
    
    print(f"   字符串列表: {fruits}")
    print(f"   数字列表: {numbers}")
    print(f"   混合类型列表: {mixed}")
    print()
    
    # 3. 使用list()构造函数
    print("3. 使用list()构造函数")
    from_string = list("hello")
    from_range = list(range(5))
    from_tuple = list((1, 2, 3))
    
    print(f"   list('hello') = {from_string}")
    print(f"   list(range(5)) = {from_range}")
    print(f"   list((1, 2, 3)) = {from_tuple}")
    print()
    
    # 4. 列表推导式创建
    print("4. 列表推导式创建")
    squares = [x**2 for x in range(5)]
    even_numbers = [x for x in range(10) if x % 2 == 0]
    
    print(f"   平方数列表: {squares}")
    print(f"   偶数列表: {even_numbers}")
    print()
    
    # 5. 重复元素列表
    print("5. 重复元素列表")
    zeros = [0] * 5
    repeated = ["hi"] * 3
    
    print(f"   [0] * 5 = {zeros}")
    print(f"   ['hi'] * 3 = {repeated}")
    print()


def demonstrate_list_access():
    """
    演示列表访问和索引
    Python的负索引特性
    """
    print("=== 列表访问和索引 ===\n")
    
    print("Java vs Python索引访问:")
    print("Java: list.get(index), list.set(index, value)")
    print("Python: list[index], list[index] = value")
    print()
    
    fruits = ["苹果", "香蕉", "橙子", "葡萄", "芒果"]
    print(f"列表: {fruits}")
    print(f"长度: {len(fruits)}")
    print()
    
    # 1. 正向索引
    print("1. 正向索引 (从0开始)")
    for i in range(len(fruits)):
        print(f"   fruits[{i}] = {fruits[i]}")
    print()
    
    # 2. 负向索引（Python特有）
    print("2. 负向索引 (Python特有)")
    print("   Java需要: list.get(list.size() - 1)")
    print("   Python: list[-1]")
    
    for i in range(1, len(fruits) + 1):
        print(f"   fruits[-{i}] = {fruits[-i]}")
    print()
    
    # 3. 索引对应关系
    print("3. 索引对应关系")
    print("   正向索引: ", end="")
    for i in range(len(fruits)):
        print(f"{i:>6}", end="")
    print()
    
    print("   元素值:   ", end="")
    for fruit in fruits:
        print(f"{fruit:>6}", end="")
    print()
    
    print("   负向索引: ", end="")
    for i in range(-len(fruits), 0):
        print(f"{i:>6}", end="")
    print("\n")
    
    # 4. 修改元素
    print("4. 修改元素")
    original = fruits.copy()
    fruits[1] = "草莓"
    fruits[-1] = "柠檬"
    
    print(f"   原始列表: {original}")
    print(f"   修改后:   {fruits}")
    print()


def demonstrate_list_slicing():
    """
    演示列表切片
    Python的强大特性
    """
    print("=== 列表切片 ===\n")
    
    print("Python切片 vs Java subList:")
    print("Java: list.subList(start, end)")
    print("Python: list[start:end:step]")
    print()
    
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"原始列表: {numbers}")
    print()
    
    # 1. 基本切片
    print("1. 基本切片 [start:end]")
    print(f"   numbers[2:6] = {numbers[2:6]}")
    print(f"   numbers[:5] = {numbers[:5]}")
    print(f"   numbers[3:] = {numbers[3:]}")
    print(f"   numbers[:] = {numbers[:]}")  # 复制整个列表
    print()
    
    # 2. 带步长的切片
    print("2. 带步长的切片 [start:end:step]")
    print(f"   numbers[::2] = {numbers[::2]}")      # 每隔一个
    print(f"   numbers[1::2] = {numbers[1::2]}")    # 从1开始每隔一个
    print(f"   numbers[::3] = {numbers[::3]}")      # 每隔两个
    print()
    
    # 3. 负索引切片
    print("3. 负索引切片")
    print(f"   numbers[-5:] = {numbers[-5:]}")      # 最后5个
    print(f"   numbers[:-3] = {numbers[:-3]}")      # 除了最后3个
    print(f"   numbers[-7:-2] = {numbers[-7:-2]}")  # 倒数第7到倒数第3
    print()
    
    # 4. 反向切片
    print("4. 反向切片")
    print(f"   numbers[::-1] = {numbers[::-1]}")    # 反转列表
    print(f"   numbers[8:2:-1] = {numbers[8:2:-1]}")# 反向选取
    print(f"   numbers[::2][::-1] = {numbers[::2][::-1]}")  # 组合操作
    print()
    
    # 5. 切片赋值
    print("5. 切片赋值")
    numbers_copy = numbers.copy()
    print(f"   原始: {numbers_copy}")
    
    numbers_copy[2:5] = [20, 30, 40]
    print(f"   numbers[2:5] = [20, 30, 40] -> {numbers_copy}")
    
    numbers_copy[1:4] = [100]  # 替换多个元素为一个
    print(f"   numbers[1:4] = [100] -> {numbers_copy}")
    
    numbers_copy[2:2] = [200, 300]  # 插入元素
    print(f"   numbers[2:2] = [200, 300] -> {numbers_copy}")
    print()


def demonstrate_list_methods():
    """
    演示列表的方法
    与Java ArrayList方法对比
    """
    print("=== 列表方法 ===\n")
    
    # 创建测试列表
    fruits = ["苹果", "香蕉"]
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    
    print("1. 添加元素")
    print("   Java: list.add(item), list.add(index, item)")
    print("   Python: list.append(item), list.insert(index, item)")
    
    print(f"   原始列表: {fruits}")
    fruits.append("橙子")
    print(f"   append('橙子'): {fruits}")
    
    fruits.insert(1, "草莓")
    print(f"   insert(1, '草莓'): {fruits}")
    
    fruits.extend(["葡萄", "芒果"])
    print(f"   extend(['葡萄', '芒果']): {fruits}")
    print()
    
    print("2. 删除元素")
    print("   Java: list.remove(item), list.remove(index)")
    print("   Python: list.remove(item), del list[index], list.pop(index)")
    
    test_fruits = fruits.copy()
    print(f"   原始列表: {test_fruits}")
    
    test_fruits.remove("草莓")
    print(f"   remove('草莓'): {test_fruits}")
    
    popped = test_fruits.pop()
    print(f"   pop(): {test_fruits}, 弹出的元素: {popped}")
    
    popped = test_fruits.pop(1)
    print(f"   pop(1): {test_fruits}, 弹出的元素: {popped}")
    
    del test_fruits[0]
    print(f"   del list[0]: {test_fruits}")
    print()
    
    print("3. 查找和统计")
    print("   Java: list.indexOf(item), list.contains(item)")
    print("   Python: list.index(item), item in list, list.count(item)")
    
    print(f"   数字列表: {numbers}")
    print(f"   index(1): {numbers.index(1)}")  # 第一个1的位置
    print(f"   count(1): {numbers.count(1)}")  # 1的个数
    print(f"   4 in numbers: {4 in numbers}")
    print(f"   10 in numbers: {10 in numbers}")
    print()
    
    print("4. 排序和反转")
    print("   Java: Collections.sort(list), Collections.reverse(list)")
    print("   Python: list.sort(), list.reverse(), sorted(list)")
    
    test_numbers = numbers.copy()
    print(f"   原始列表: {test_numbers}")
    
    test_numbers.sort()
    print(f"   sort(): {test_numbers}")
    
    test_numbers.reverse()
    print(f"   reverse(): {test_numbers}")
    
    # sorted()返回新列表，不修改原列表
    sorted_numbers = sorted(numbers)
    print(f"   sorted(原列表): {sorted_numbers}")
    print(f"   原列表不变: {numbers}")
    print()
    
    print("5. 清空和复制")
    print("   Java: list.clear(), new ArrayList<>(list)")
    print("   Python: list.clear(), list.copy(), list[:]")
    
    test_list = [1, 2, 3, 4, 5]
    print(f"   原始列表: {test_list}")
    
    copy1 = test_list.copy()
    copy2 = test_list[:]
    copy3 = list(test_list)
    
    print(f"   copy(): {copy1}")
    print(f"   [:]: {copy2}")
    print(f"   list(): {copy3}")
    
    test_list.clear()
    print(f"   clear()后: {test_list}")
    print(f"   副本不受影响: {copy1}")
    print()


def demonstrate_list_operations():
    """
    演示列表运算操作
    Python的运算符重载
    """
    print("=== 列表运算操作 ===\n")
    
    print("Python列表运算符 (Java没有对应的运算符):")
    print("   + : 连接列表")
    print("   * : 重复列表")
    print("   == : 比较列表内容")
    print("   in : 成员检查")
    print()
    
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    
    print(f"list1 = {list1}")
    print(f"list2 = {list2}")
    print()
    
    # 1. 连接运算
    print("1. 连接运算 (+)")
    combined = list1 + list2
    print(f"   list1 + list2 = {combined}")
    
    list1 += [7, 8]  # 等价于 list1.extend([7, 8])
    print(f"   list1 += [7, 8] = {list1}")
    print()
    
    # 2. 重复运算
    print("2. 重复运算 (*)")
    repeated = [0] * 5
    print(f"   [0] * 5 = {repeated}")
    
    pattern = [1, 2] * 3
    print(f"   [1, 2] * 3 = {pattern}")
    print()
    
    # 3. 比较运算
    print("3. 比较运算")
    list_a = [1, 2, 3]
    list_b = [1, 2, 3]
    list_c = [1, 2, 4]
    
    print(f"   {list_a} == {list_b}: {list_a == list_b}")
    print(f"   {list_a} == {list_c}: {list_a == list_c}")
    print(f"   {list_a} < {list_c}: {list_a < list_c}")  # 字典序比较
    print()
    
    # 4. 成员检查
    print("4. 成员检查 (in/not in)")
    fruits = ["苹果", "香蕉", "橙子"]
    
    print(f"   水果列表: {fruits}")
    print(f"   '苹果' in fruits: {'苹果' in fruits}")
    print(f"   '葡萄' in fruits: {'葡萄' in fruits}")
    print(f"   '葡萄' not in fruits: {'葡萄' not in fruits}")
    print()


def demonstrate_list_comprehensions():
    """
    演示列表推导式
    Python的强大特性
    """
    print("=== 列表推导式 ===\n")
    
    print("Python列表推导式 vs Java Stream:")
    print("Java:")
    print("   list.stream().filter(x -> x > 0).map(x -> x * 2).collect(toList())")
    print()
    print("Python:")
    print("   [x * 2 for x in list if x > 0]")
    print()
    
    # 1. 基本推导式
    print("1. 基本推导式")
    numbers = range(10)
    
    # 传统方式
    squares_traditional = []
    for x in numbers:
        squares_traditional.append(x ** 2)
    
    # 推导式方式
    squares_comprehension = [x ** 2 for x in numbers]
    
    print(f"   传统方式: {squares_traditional}")
    print(f"   推导式:   {squares_comprehension}")
    print()
    
    # 2. 带条件的推导式
    print("2. 带条件的推导式")
    even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
    print(f"   偶数平方: {even_squares}")
    
    # 字符串处理
    words = ["hello", "world", "python", "java"]
    uppercase_long = [word.upper() for word in words if len(word) > 4]
    print(f"   长单词大写: {uppercase_long}")
    print()
    
    # 3. 嵌套推导式
    print("3. 嵌套推导式")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    # 展平矩阵
    flattened = [item for row in matrix for item in row]
    print(f"   矩阵: {matrix}")
    print(f"   展平: {flattened}")
    
    # 筛选矩阵中的偶数
    even_items = [item for row in matrix for item in row if item % 2 == 0]
    print(f"   偶数元素: {even_items}")
    print()
    
    # 4. 复杂推导式
    print("4. 复杂推导式")
    
    # 生成乘法表
    multiplication_table = [f"{i}x{j}={i*j}" for i in range(1, 4) for j in range(1, 4)]
    print("   乘法表:")
    for i, item in enumerate(multiplication_table):
        print(f"     {item}", end="  ")
        if (i + 1) % 3 == 0:
            print()
    
    # 条件表达式
    numbers = range(-5, 6)
    abs_or_zero = [x if x >= 0 else -x for x in numbers]
    print(f"\n   绝对值: {list(abs_or_zero)}")
    print()


def demonstrate_list_performance():
    """
    演示列表性能考虑
    与Java ArrayList的性能对比
    """
    print("=== 列表性能考虑 ===\n")
    
    import time
    
    def time_operation(operation_name, operation_func):
        start_time = time.time()
        result = operation_func()
        end_time = time.time()
        duration = end_time - start_time
        print(f"   {operation_name}: {duration:.6f}秒")
        return result
    
    print("性能测试 (10万个元素):")
    
    # 1. 创建列表的性能
    print("\n1. 创建列表性能对比:")
    
    def create_with_append():
        lst = []
        for i in range(100000):
            lst.append(i)
        return lst
    
    def create_with_comprehension():
        return [i for i in range(100000)]
    
    def create_with_list():
        return list(range(100000))
    
    time_operation("append方式", create_with_append)
    time_operation("列表推导式", create_with_comprehension)
    time_operation("list()构造", create_with_list)
    
    # 2. 查找性能
    print("\n2. 查找性能 (查找最后一个元素):")
    test_list = list(range(100000))
    target = 99999
    
    def find_with_in():
        return target in test_list
    
    def find_with_index():
        try:
            test_list.index(target)
            return True
        except ValueError:
            return False
    
    time_operation("in运算符", find_with_in)
    time_operation("index方法", find_with_index)
    
    print("\n性能优化建议:")
    recommendations = [
        "使用列表推导式而不是循环append",
        "对于大量查找操作，考虑使用set",
        "避免在列表头部插入/删除元素",
        "使用slice而不是循环复制部分列表",
        "预分配列表大小可以提高性能",
        "使用deque处理队列操作"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    print()


def demonstrate_list_pitfalls():
    """
    演示列表的常见陷阱
    """
    print("=== 列表常见陷阱 ===\n")
    
    print("1. 浅复制 vs 深复制")
    
    # 浅复制陷阱
    original = [[1, 2], [3, 4]]
    shallow_copy = original.copy()  # 或 original[:]
    deep_copy = copy.deepcopy(original)
    
    print(f"   原始列表: {original}")
    print(f"   浅复制: {shallow_copy}")
    print(f"   深复制: {deep_copy}")
    
    # 修改内部列表
    original[0][0] = 999
    
    print("\n   修改原始列表内部元素后:")
    print(f"   原始列表: {original}")
    print(f"   浅复制: {shallow_copy}")  # 受到影响
    print(f"   深复制: {deep_copy}")     # 不受影响
    print()
    
    print("2. 默认参数陷阱")
    
    # 错误的方式
    def add_item_wrong(item, target_list=[]):
        target_list.append(item)
        return target_list
    
    # 正确的方式
    def add_item_correct(item, target_list=None):
        if target_list is None:
            target_list = []
        target_list.append(item)
        return target_list
    
    print("   错误的默认参数使用:")
    result1 = add_item_wrong("第一次")
    result2 = add_item_wrong("第二次")
    print(f"   第一次调用: {result1}")
    print(f"   第二次调用: {result2}")  # 包含了第一次的结果
    
    print("\n   正确的默认参数使用:")
    result3 = add_item_correct("第一次")
    result4 = add_item_correct("第二次")
    print(f"   第一次调用: {result3}")
    print(f"   第二次调用: {result4}")
    print()
    
    print("3. 循环中修改列表")
    
    # 错误的方式
    numbers = [1, 2, 3, 4, 5, 6]
    print(f"   原始列表: {numbers}")
    
    # 这样会跳过一些元素
    for num in numbers[:]:  # 使用副本避免问题
        if num % 2 == 0:
            numbers.remove(num)
    
    print(f"   删除偶数后: {numbers}")
    
    # 正确的方式 - 使用列表推导式
    numbers = [1, 2, 3, 4, 5, 6]
    numbers = [num for num in numbers if num % 2 != 0]
    print(f"   正确方式: {numbers}")
    print()


def main():
    """主函数 - 演示所有列表功能"""
    print("Python基础语法学习 - 列表(List)")
    print("=" * 50)
    
    demonstrate_list_creation()
    demonstrate_list_access()
    demonstrate_list_slicing()
    demonstrate_list_methods()
    demonstrate_list_operations()
    demonstrate_list_comprehensions()
    demonstrate_list_performance()
    demonstrate_list_pitfalls()
    
    print("学习总结:")
    print("1. Python列表是动态数组，类似Java ArrayList")
    print("2. 支持负索引和强大的切片操作")
    print("3. 列表推导式是Python的强大特性")
    print("4. 注意浅复制和深复制的区别")
    print("5. 合理使用列表方法提高代码效率")
    print("6. 避免在循环中修改正在遍历的列表")


if __name__ == "__main__":
    main() 