#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法 - 循环结构
========================

本文件演示Python的循环结构，并与Java进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""


def demonstrate_for_loop():
    """
    演示for循环
    Python与Java的巨大差异
    """
    print("=== for循环 ===\n")
    
    print("Java vs Python for循环:")
    print("Java (传统for):                Python (for-in):")
    print("for (int i = 0; i < 5; i++) {  for i in range(5):")
    print("    System.out.println(i);         print(i)")
    print("}")
    print()
    
    print("Java (增强for):                Python (for-in):")
    print("for (String item : list) {     for item in list:")
    print("    System.out.println(item);      print(item)")
    print("}")
    print()
    
    # 基本范围循环
    print("1. 基本范围循环")
    print("range(5):")
    for i in range(5):
        print(f"   {i}")
    print()
    
    print("range(2, 8):")
    for i in range(2, 8):
        print(f"   {i}")
    print()
    
    print("range(0, 10, 2):")
    for i in range(0, 10, 2):
        print(f"   {i}")
    print()
    
    # 遍历列表
    print("2. 遍历列表")
    fruits = ["苹果", "香蕉", "橙子", "葡萄"]
    print(f"水果列表: {fruits}")
    
    for fruit in fruits:
        print(f"   我喜欢{fruit}")
    print()
    
    # 带索引的遍历
    print("3. 带索引的遍历 (enumerate)")
    print("Java需要手动管理索引，Python使用enumerate:")
    
    for index, fruit in enumerate(fruits):
        print(f"   {index}: {fruit}")
    
    # 指定起始索引
    print("\n从索引1开始:")
    for index, fruit in enumerate(fruits, start=1):
        print(f"   第{index}个: {fruit}")
    print()


def demonstrate_while_loop():
    """
    演示while循环
    与Java基本相同
    """
    print("=== while循环 ===\n")
    
    print("Java vs Python while循环 (语法相似):")
    print("Java:                          Python:")
    print("while (condition) {            while condition:")
    print("    // 代码块                      # 代码块")
    print("}")
    print()
    
    # 基本while循环
    print("1. 基本while循环")
    count = 0
    print("计数到5:")
    while count < 5:
        print(f"   计数: {count}")
        count += 1
    print()
    
    # 用户输入循环 (模拟)
    print("2. 条件控制循环")
    numbers = [1, 3, 5, 7, 10, 12]
    index = 0
    
    print("寻找第一个偶数:")
    while index < len(numbers):
        current = numbers[index]
        print(f"   检查: {current}")
        if current % 2 == 0:
            print(f"   找到偶数: {current}")
            break
        index += 1
    print()
    
    # 无限循环控制
    print("3. 无限循环控制")
    print("处理任务队列:")
    
    task_queue = ["任务1", "任务2", "任务3"]
    
    while True:
        if not task_queue:
            print("   所有任务完成，退出循环")
            break
        
        task = task_queue.pop(0)
        print(f"   执行: {task}")
    print()


def demonstrate_loop_control():
    """
    演示循环控制语句
    break, continue, pass
    """
    print("=== 循环控制语句 ===\n")
    
    print("Java vs Python循环控制:")
    print("break:    跳出循环 (两者相同)")
    print("continue: 跳过当前迭代 (两者相同)")
    print("pass:     Python特有，空操作占位符")
    print()
    
    # break示例
    print("1. break - 跳出循环")
    print("寻找目标数字:")
    
    numbers = [1, 3, 7, 9, 12, 15, 18]
    target = 12
    
    for i, num in enumerate(numbers):
        print(f"   检查位置{i}: {num}")
        if num == target:
            print(f"   找到目标{target}，位置: {i}")
            break
    else:
        # for循环的else子句，当循环正常结束时执行
        print(f"   未找到目标{target}")
    print()
    
    # continue示例
    print("2. continue - 跳过当前迭代")
    print("只处理偶数:")
    
    for num in range(1, 11):
        if num % 2 != 0:
            continue  # 跳过奇数
        print(f"   处理偶数: {num}")
    print()
    
    # pass示例
    print("3. pass - 空操作占位符")
    print("暂未实现的功能:")
    
    for item in ["功能A", "功能B", "功能C"]:
        if item == "功能B":
            pass  # 暂未实现
            print(f"   {item}: 待实现")
        else:
            print(f"   {item}: 已实现")
    print()


def demonstrate_nested_loops():
    """
    演示嵌套循环
    二维数据处理
    """
    print("=== 嵌套循环 ===\n")
    
    print("Java vs Python嵌套循环 (语法类似):")
    print("Java:                          Python:")
    print("for (int i = 0; i < 3; i++) {  for i in range(3):")
    print("    for (int j = 0; j < 3; j++){   for j in range(3):")
    print("        // 处理 i, j                  # 处理 i, j")
    print("    }")
    print("}")
    print()
    
    # 二维表格
    print("1. 二维表格处理")
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    print("矩阵:")
    for row_idx, row in enumerate(matrix):
        for col_idx, value in enumerate(row):
            print(f"   [{row_idx}][{col_idx}] = {value}")
    print()
    
    # 九九乘法表
    print("2. 九九乘法表")
    for i in range(1, 4):  # 只显示前3行
        line = ""
        for j in range(1, 4):  # 只显示前3列
            product = i * j
            line += f"{i}×{j}={product:2d}  "
        print(f"   {line}")
    print()
    
    # 控制嵌套循环
    print("3. 嵌套循环控制")
    print("寻找目标组合:")
    
    found = False
    for x in range(1, 4):
        for y in range(1, 4):
            print(f"   检查组合: ({x}, {y})")
            if x * y == 6:
                print(f"   找到目标组合: ({x}, {y})")
                found = True
                break
        if found:
            break
    print()


def demonstrate_loop_else():
    """
    演示循环的else子句
    Python特有功能
    """
    print("=== 循环的else子句 ===\n")
    
    print("Python特有功能 - for/while的else子句:")
    print("- 当循环正常结束时执行else")
    print("- 当使用break跳出循环时不执行else")
    print("- Java没有类似功能")
    print()
    
    # for-else示例
    print("1. for-else示例")
    
    def find_even(numbers):
        print(f"   在{numbers}中寻找偶数:")
        for num in numbers:
            print(f"     检查: {num}")
            if num % 2 == 0:
                print(f"     找到偶数: {num}")
                break
        else:
            print("     没有找到偶数")
        print()
    
    find_even([1, 3, 5, 7])  # 没有偶数
    find_even([1, 3, 6, 7])  # 有偶数
    
    # while-else示例
    print("2. while-else示例")
    
    def countdown_with_interrupt(start, interrupt_at=None):
        print(f"   从{start}开始倒计时:")
        count = start
        while count > 0:
            print(f"     {count}")
            if count == interrupt_at:
                print("     倒计时被中断!")
                break
            count -= 1
        else:
            print("     倒计时完成!")
        print()
    
    countdown_with_interrupt(3)           # 正常完成
    countdown_with_interrupt(3, 2)        # 被中断


def demonstrate_comprehensions():
    """
    演示列表推导式
    Python的强大特性
    """
    print("=== 列表推导式 ===\n")
    
    print("Python列表推导式 vs Java Stream:")
    print("Python: [expr for item in iterable if condition]")
    print("Java: stream.filter(condition).map(expr).collect()")
    print()
    
    # 基本列表推导式
    print("1. 基本列表推导式")
    
    # 传统循环方式
    squares_traditional = []
    for x in range(5):
        squares_traditional.append(x ** 2)
    
    # 列表推导式方式
    squares_comprehension = [x ** 2 for x in range(5)]
    
    print(f"   传统方式: {squares_traditional}")
    print(f"   推导式:   {squares_comprehension}")
    print()
    
    # 带条件的推导式
    print("2. 带条件的推导式")
    
    numbers = range(10)
    
    # 偶数的平方
    even_squares = [x ** 2 for x in numbers if x % 2 == 0]
    print(f"   偶数的平方: {even_squares}")
    
    # 奇数的立方
    odd_cubes = [x ** 3 for x in numbers if x % 2 == 1]
    print(f"   奇数的立方: {odd_cubes}")
    print()
    
    # 嵌套推导式
    print("3. 嵌套推导式")
    
    # 二维列表展平
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [item for row in matrix for item in row]
    print(f"   原始矩阵: {matrix}")
    print(f"   展平结果: {flattened}")
    
    # 组合生成
    colors = ["红", "绿", "蓝"]
    sizes = ["S", "M", "L"]
    combinations = [f"{color}-{size}" for color in colors for size in sizes]
    print(f"   颜色: {colors}")
    print(f"   尺寸: {sizes}")
    print(f"   组合: {combinations}")
    print()


def demonstrate_itertools():
    """
    演示itertools模块
    高级迭代工具
    """
    print("=== itertools模块 ===\n")
    
    print("Python的itertools提供高级迭代工具")
    print("类似Java的Stream API，但更强大")
    print()
    
    import itertools
    
    # count - 无限计数器
    print("1. itertools.count - 无限计数器")
    counter = itertools.count(start=10, step=2)
    for i, value in enumerate(counter):
        if i >= 5:
            break
        print(f"   第{i}个值: {value}")
    print()
    
    # cycle - 循环迭代器
    print("2. itertools.cycle - 循环迭代器")
    colors = ["红", "绿", "蓝"]
    color_cycle = itertools.cycle(colors)
    
    print("   分配颜色给用户:")
    users = ["用户A", "用户B", "用户C", "用户D", "用户E"]
    for user in users:
        color = next(color_cycle)
        print(f"   {user}: {color}")
    print()
    
    # chain - 连接多个迭代器
    print("3. itertools.chain - 连接迭代器")
    list1 = [1, 2, 3]
    list2 = ["a", "b", "c"]
    list3 = [10, 20]
    
    chained = itertools.chain(list1, list2, list3)
    print(f"   连接结果: {list(chained)}")
    print()
    
    # combinations - 组合
    print("4. itertools.combinations - 组合")
    items = ["A", "B", "C", "D"]
    for r in range(2, 4):
        combos = list(itertools.combinations(items, r))
        print(f"   从{items}中选{r}个的组合: {combos}")
    print()


def demonstrate_performance_tips():
    """
    演示循环性能优化技巧
    """
    print("=== 循环性能优化 ===\n")
    
    import time
    
    print("性能优化技巧:")
    print("1. 使用内置函数而不是循环")
    print("2. 列表推导式通常比循环快")
    print("3. 避免在循环中重复计算")
    print("4. 使用生成器表达式节省内存")
    print()
    
    # 性能对比
    def time_function(func, name, *args):
        start = time.time()
        result = func(*args)
        end = time.time()
        print(f"   {name}: {end - start:.6f}秒")
        return result
    
    # 求和对比
    numbers = list(range(100000))
    
    def sum_with_loop(nums):
        total = 0
        for num in nums:
            total += num
        return total
    
    def sum_with_builtin(nums):
        return sum(nums)
    
    print("求和性能对比 (100,000个数字):")
    result1 = time_function(sum_with_loop, "循环求和", numbers)
    result2 = time_function(sum_with_builtin, "内置sum", numbers)
    print(f"   结果相同: {result1 == result2}")
    print()
    
    # 列表生成对比
    def create_with_loop():
        result = []
        for i in range(10000):
            result.append(i ** 2)
        return result
    
    def create_with_comprehension():
        return [i ** 2 for i in range(10000)]
    
    print("列表生成性能对比 (10,000个平方数):")
    time_function(create_with_loop, "循环创建", )
    time_function(create_with_comprehension, "列表推导式", )


def main():
    """主函数 - 演示所有循环功能"""
    print("Python基础语法学习 - 循环结构")
    print("=" * 50)
    
    demonstrate_for_loop()
    demonstrate_while_loop()
    demonstrate_loop_control()
    demonstrate_nested_loops()
    demonstrate_loop_else()
    demonstrate_comprehensions()
    demonstrate_itertools()
    demonstrate_performance_tips()
    
    print("\n学习总结:")
    print("1. Python的for循环是for-in循环，不是计数循环")
    print("2. range()函数生成数字序列")
    print("3. enumerate()为循环添加索引")
    print("4. Python有循环的else子句")
    print("5. 列表推导式是Python的强大特性")
    print("6. itertools模块提供高级迭代工具")
    print("7. 合理使用内置函数可以显著提高性能")


if __name__ == "__main__":
    main() 