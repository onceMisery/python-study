#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法 - 元组(Tuple)
==========================

本文件演示Python的元组类型，并与Java不可变集合进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

from typing import Tuple, NamedTuple, Any
from collections import namedtuple
import time


def demonstrate_tuple_creation():
    """
    演示元组创建的各种方式
    与Java不可变集合对比
    """
    print("=== 元组创建 ===\n")
    
    print("Java不可变集合 vs Python Tuple:")
    print("Java:")
    print("   List<String> immutable = List.of(\"a\", \"b\", \"c\"); // Java 9+")
    print("   List<String> immutable = Collections.unmodifiableList(list);")
    print("   record Point(int x, int y) {} // Java 14+")
    print()
    
    print("Python:")
    print("   tuple = ()")
    print("   tuple = (1, 2, 3)")
    print("   tuple = 1, 2, 3  # 括号可选")
    print()
    
    # 1. 空元组
    print("1. 创建空元组")
    empty_tuple1 = ()
    empty_tuple2 = tuple()
    
    print(f"   () = {empty_tuple1}")
    print(f"   tuple() = {empty_tuple2}")
    print(f"   类型: {type(empty_tuple1)}")
    print()
    
    # 2. 单元素元组
    print("2. 单元素元组 (注意语法)")
    single_wrong = (42)      # 这不是元组，是整数
    single_correct = (42,)   # 正确的单元素元组
    single_no_paren = 42,    # 也是正确的
    
    print(f"   (42) = {single_wrong}, 类型: {type(single_wrong)}")
    print(f"   (42,) = {single_correct}, 类型: {type(single_correct)}")
    print(f"   42, = {single_no_paren}, 类型: {type(single_no_paren)}")
    print()
    
    # 3. 多元素元组
    print("3. 多元素元组")
    coordinates = (10, 20)
    rgb_color = (255, 128, 0)
    student_info = ("张三", 20, "计算机科学", 3.8)
    mixed_tuple = (1, "hello", 3.14, True, None)
    
    print(f"   坐标: {coordinates}")
    print(f"   RGB颜色: {rgb_color}")
    print(f"   学生信息: {student_info}")
    print(f"   混合类型: {mixed_tuple}")
    print()
    
    # 4. 使用tuple()构造函数
    print("4. 使用tuple()构造函数")
    from_list = tuple([1, 2, 3, 4])
    from_string = tuple("hello")
    from_range = tuple(range(5))
    
    print(f"   tuple([1,2,3,4]) = {from_list}")
    print(f"   tuple('hello') = {from_string}")
    print(f"   tuple(range(5)) = {from_range}")
    print()
    
    # 5. 嵌套元组
    print("5. 嵌套元组")
    nested = ((1, 2), (3, 4), (5, 6))
    complex_nested = (
        ("张三", (85, 92, 78)),
        ("李四", (90, 88, 95)),
        ("王五", (82, 79, 91))
    )
    
    print(f"   嵌套元组: {nested}")
    print(f"   复杂嵌套: {complex_nested}")
    print()


def demonstrate_tuple_access():
    """
    演示元组访问和特性
    不可变性的体现
    """
    print("=== 元组访问和特性 ===\n")
    
    print("元组的不可变特性:")
    print("   Java: 不可变集合一旦创建就不能修改")
    print("   Python: 元组是不可变的序列类型")
    print()
    
    colors = ("red", "green", "blue", "yellow", "purple")
    print(f"颜色元组: {colors}")
    print(f"长度: {len(colors)}")
    print()
    
    # 1. 索引访问
    print("1. 索引访问 (类似列表)")
    print(f"   colors[0] = {colors[0]}")
    print(f"   colors[-1] = {colors[-1]}")
    print(f"   colors[1:4] = {colors[1:4]}")
    print()
    
    # 2. 不可变性验证
    print("2. 不可变性验证")
    try:
        colors[0] = "orange"  # 尝试修改元组
    except TypeError as e:
        print(f"   尝试修改元组: {e}")
    
    try:
        colors.append("black")  # 元组没有append方法
    except AttributeError as e:
        print(f"   尝试添加元素: {e}")
    print()
    
    # 3. 元组解包
    print("3. 元组解包 (Python特有)")
    print("   Java需要通过索引逐个获取")
    print("   Python可以直接解包到变量")
    
    point = (10, 20)
    x, y = point  # 解包
    print(f"   point = {point}")
    print(f"   x, y = point -> x={x}, y={y}")
    
    # 多变量解包
    person = ("张三", 25, "工程师", "北京")
    name, age, job, city = person
    print(f"   name={name}, age={age}, job={job}, city={city}")
    
    # 部分解包
    first, *rest = colors
    print(f"   first={first}, rest={rest}")
    
    first, second, *middle, last = colors
    print(f"   first={first}, second={second}, middle={middle}, last={last}")
    print()
    
    # 4. 交换变量
    print("4. 交换变量 (利用元组)")
    print("   Java需要临时变量")
    print("   Python使用元组可以直接交换")
    
    a, b = 100, 200
    print(f"   交换前: a={a}, b={b}")
    a, b = b, a  # 直接交换
    print(f"   交换后: a={a}, b={b}")
    print()


def demonstrate_tuple_methods():
    """
    演示元组的方法
    有限但实用的方法集
    """
    print("=== 元组方法 ===\n")
    
    print("元组的方法 (相比列表很少):")
    print("   Java不可变集合: 只有查询方法")
    print("   Python元组: count(), index(), + 序列操作")
    print()
    
    numbers = (1, 2, 3, 2, 4, 2, 5)
    letters = ('a', 'b', 'c', 'd', 'e')
    
    print(f"数字元组: {numbers}")
    print(f"字母元组: {letters}")
    print()
    
    # 1. count方法
    print("1. count() - 统计元素出现次数")
    count_2 = numbers.count(2)
    count_missing = numbers.count(10)
    
    print(f"   numbers.count(2) = {count_2}")
    print(f"   numbers.count(10) = {count_missing}")
    print()
    
    # 2. index方法
    print("2. index() - 查找元素索引")
    index_2 = numbers.index(2)  # 第一个2的位置
    index_c = letters.index('c')
    
    print(f"   numbers.index(2) = {index_2}")
    print(f"   letters.index('c') = {index_c}")
    
    # 查找不存在的元素
    try:
        missing = numbers.index(10)
    except ValueError as e:
        print(f"   查找不存在元素: {e}")
    print()
    
    # 3. 成员检查
    print("3. 成员检查 (in/not in)")
    print(f"   2 in numbers: {2 in numbers}")
    print(f"   10 in numbers: {10 in numbers}")
    print(f"   'c' in letters: {'c' in letters}")
    print()
    
    # 4. 序列操作
    print("4. 序列操作")
    
    # 连接
    combined = numbers + letters
    print(f"   numbers + letters = {combined}")
    
    # 重复
    repeated = (1, 2) * 3
    print(f"   (1, 2) * 3 = {repeated}")
    
    # 切片
    slice_result = numbers[1:5]
    print(f"   numbers[1:5] = {slice_result}")
    print()


def demonstrate_tuple_use_cases():
    """
    演示元组的典型用例
    何时使用元组而不是列表
    """
    print("=== 元组的典型用例 ===\n")
    
    print("何时使用元组而不是列表:")
    print("   1. 数据不需要修改")
    print("   2. 作为字典的键")
    print("   3. 函数返回多个值")
    print("   4. 配置和常量")
    print("   5. 数据库记录")
    print()
    
    # 1. 坐标和点
    print("1. 坐标和几何数据")
    point_2d = (10, 20)
    point_3d = (10, 20, 30)
    rectangle = ((0, 0), (100, 50))  # 左上角和右下角
    
    print(f"   2D点: {point_2d}")
    print(f"   3D点: {point_3d}")
    print(f"   矩形: {rectangle}")
    print()
    
    # 2. RGB颜色
    print("2. 颜色定义")
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (128, 0, 128)
    
    def describe_color(color):
        r, g, b = color
        return f"RGB({r}, {g}, {b})"
    
    print(f"   红色: {describe_color(RED)}")
    print(f"   紫色: {describe_color(PURPLE)}")
    print()
    
    # 3. 作为字典键
    print("3. 作为字典键 (不可变性的优势)")
    
    # 游戏地图坐标
    game_map = {
        (0, 0): "起点",
        (5, 3): "宝箱",
        (10, 8): "怪物",
        (-2, 4): "陷阱"
    }
    
    print("   游戏地图:")
    for position, content in game_map.items():
        x, y = position
        print(f"     位置({x}, {y}): {content}")
    print()
    
    # 4. 函数返回多个值
    print("4. 函数返回多个值")
    
    def get_name_age_score():
        """返回学生的姓名、年龄和成绩"""
        return "张三", 20, 95.5  # 返回元组
    
    def calculate_stats(numbers):
        """计算统计信息"""
        if not numbers:
            return 0, 0, 0
        
        total = sum(numbers)
        avg = total / len(numbers)
        return len(numbers), total, avg  # 返回元组
    
    # 使用返回的元组
    name, age, score = get_name_age_score()
    print(f"   学生信息: {name}, {age}岁, {score}分")
    
    test_numbers = [85, 92, 78, 96, 88]
    count, total, average = calculate_stats(test_numbers)
    print(f"   统计结果: 数量={count}, 总和={total}, 平均={average:.2f}")
    print()
    
    # 5. 配置数据
    print("5. 配置和设置")
    
    # 数据库配置
    DB_CONFIG = ("localhost", 3306, "mydb", "user", "password")
    
    # 应用设置
    WINDOW_SIZE = (800, 600)
    DEFAULT_COLORS = (
        (255, 255, 255),  # 白色
        (0, 0, 0),        # 黑色
        (128, 128, 128)   # 灰色
    )
    
    def connect_database(config):
        host, port, database, username, password = config
        return f"连接到 {username}@{host}:{port}/{database}"
    
    print(f"   数据库连接: {connect_database(DB_CONFIG)}")
    print(f"   窗口大小: {WINDOW_SIZE}")
    print()


def demonstrate_named_tuples():
    """
    演示命名元组
    更好的结构化数据
    """
    print("=== 命名元组 ===\n")
    
    print("命名元组 vs 普通元组:")
    print("   普通元组: 通过索引访问，不够直观")
    print("   命名元组: 通过名称访问，更清晰")
    print("   Java对比: 类似record类 (Java 14+)")
    print()
    
    # 1. 创建命名元组类
    print("1. 创建命名元组类")
    
    # 使用namedtuple工厂函数
    Point = namedtuple('Point', ['x', 'y'])
    Person = namedtuple('Person', 'name age city')  # 也可以用字符串
    
    # 使用typing.NamedTuple (推荐，支持类型注解)
    class Student(NamedTuple):
        name: str
        age: int
        grade: str
        gpa: float
    
    print("   Point = namedtuple('Point', ['x', 'y'])")
    print("   class Student(NamedTuple): ...")
    print()
    
    # 2. 创建实例
    print("2. 创建和使用命名元组实例")
    
    p1 = Point(10, 20)
    p2 = Point(x=30, y=40)  # 关键字参数
    
    person = Person("张三", 25, "北京")
    student = Student("李四", 20, "大二", 3.8)
    
    print(f"   Point实例: {p1}")
    print(f"   Person实例: {person}")
    print(f"   Student实例: {student}")
    print()
    
    # 3. 访问字段
    print("3. 访问字段")
    print("   索引访问:")
    print(f"     p1[0] = {p1[0]}, p1[1] = {p1[1]}")
    
    print("   名称访问:")
    print(f"     p1.x = {p1.x}, p1.y = {p1.y}")
    print(f"     person.name = {person.name}")
    print(f"     student.gpa = {student.gpa}")
    print()
    
    # 4. 命名元组方法
    print("4. 命名元组的特殊方法")
    
    # _asdict() - 转换为字典
    person_dict = person._asdict()
    print(f"   person._asdict() = {person_dict}")
    
    # _replace() - 创建修改后的副本
    older_person = person._replace(age=26)
    print(f"   person._replace(age=26) = {older_person}")
    
    # _fields - 字段名称
    print(f"   Person._fields = {Person._fields}")
    print(f"   Student._fields = {Student._fields}")
    print()
    
    # 5. 实际应用示例
    print("5. 实际应用示例")
    
    # 数据库记录
    Employee = namedtuple('Employee', 'id name department salary')
    
    employees = [
        Employee(1, "张三", "开发部", 15000),
        Employee(2, "李四", "销售部", 12000),
        Employee(3, "王五", "开发部", 18000)
    ]
    
    print("   员工记录:")
    for emp in employees:
        print(f"     {emp.name} ({emp.department}): ￥{emp.salary}")
    
    # 计算开发部平均工资
    dev_salaries = [emp.salary for emp in employees if emp.department == "开发部"]
    avg_salary = sum(dev_salaries) / len(dev_salaries)
    print(f"   开发部平均工资: ￥{avg_salary:.0f}")
    print()


def demonstrate_tuple_performance():
    """
    演示元组的性能特点
    """
    print("=== 元组性能特点 ===\n")
    
    import time
    
    def time_operation(operation_name, operation_func, iterations=1000000):
        start_time = time.time()
        for _ in range(iterations):
            operation_func()
        end_time = time.time()
        duration = end_time - start_time
        print(f"   {operation_name}: {duration:.6f}秒 ({iterations}次)")
        return duration
    
    print("性能测试:")
    
    # 1. 创建性能对比
    print("\n1. 创建性能对比:")
    
    data = [1, 2, 3, 4, 5]
    
    def create_list():
        return [1, 2, 3, 4, 5]
    
    def create_tuple():
        return (1, 2, 3, 4, 5)
    
    def create_list_from_data():
        return list(data)
    
    def create_tuple_from_data():
        return tuple(data)
    
    time_operation("创建列表", create_list)
    time_operation("创建元组", create_tuple)
    time_operation("list(data)", create_list_from_data)
    time_operation("tuple(data)", create_tuple_from_data)
    
    # 2. 访问性能对比
    print("\n2. 访问性能对比:")
    
    test_list = [i for i in range(1000)]
    test_tuple = tuple(test_list)
    
    def access_list():
        return test_list[500]
    
    def access_tuple():
        return test_tuple[500]
    
    time_operation("列表访问", access_list)
    time_operation("元组访问", access_tuple)
    
    # 3. 内存使用对比
    print("\n3. 内存使用对比:")
    
    import sys
    
    small_list = [1, 2, 3, 4, 5]
    small_tuple = (1, 2, 3, 4, 5)
    
    large_list = list(range(10000))
    large_tuple = tuple(range(10000))
    
    print(f"   小列表内存: {sys.getsizeof(small_list)} 字节")
    print(f"   小元组内存: {sys.getsizeof(small_tuple)} 字节")
    print(f"   大列表内存: {sys.getsizeof(large_list)} 字节")
    print(f"   大元组内存: {sys.getsizeof(large_tuple)} 字节")
    
    print("\n性能特点总结:")
    print("   1. 元组创建比列表快")
    print("   2. 元组访问速度与列表相当")
    print("   3. 元组内存占用通常更少")
    print("   4. 元组的不可变性提供更好的哈希性能")
    print("   5. 元组适合作为字典键")
    print()


def demonstrate_tuple_pitfalls():
    """
    演示元组的常见陷阱
    """
    print("=== 元组常见陷阱 ===\n")
    
    print("1. 单元素元组的括号陷阱")
    
    # 错误的单元素"元组"
    not_tuple = (42)
    correct_tuple = (42,)
    
    print(f"   (42) 的类型: {type(not_tuple)}")
    print(f"   (42,) 的类型: {type(correct_tuple)}")
    print("   记住：单元素元组需要末尾逗号")
    print()
    
    print("2. 嵌套可变对象的陷阱")
    
    # 元组本身不可变，但内容可以是可变的
    nested_tuple = ([1, 2], [3, 4])
    print(f"   原始元组: {nested_tuple}")
    
    # 修改内部列表
    nested_tuple[0].append(3)
    print(f"   修改后: {nested_tuple}")
    print("   元组不可变，但内部可变对象可以修改")
    print()
    
    print("3. 解包时的变量数量陷阱")
    
    point_3d = (10, 20, 30)
    
    try:
        x, y = point_3d  # 变量数量不匹配
    except ValueError as e:
        print(f"   解包错误: {e}")
    
    # 正确的解包方式
    x, y, z = point_3d
    print(f"   正确解包: x={x}, y={y}, z={z}")
    
    # 使用*收集多余元素
    x, y, *rest = point_3d
    print(f"   使用*解包: x={x}, y={y}, rest={rest}")
    print()
    
    print("4. 作为字典键时的注意事项")
    
    # 包含可变对象的元组不能作为字典键
    try:
        bad_key = ([1, 2], 3)
        test_dict = {bad_key: "value"}
    except TypeError as e:
        print(f"   可变内容元组作键: {e}")
    
    # 只有完全不可变的元组才能作为键
    good_key = ((1, 2), 3)
    test_dict = {good_key: "value"}
    print(f"   不可变元组作键: 成功创建字典")
    print()


def main():
    """主函数 - 演示所有元组功能"""
    print("Python基础语法学习 - 元组(Tuple)")
    print("=" * 50)
    
    demonstrate_tuple_creation()
    demonstrate_tuple_access()
    demonstrate_tuple_methods()
    demonstrate_tuple_use_cases()
    demonstrate_named_tuples()
    demonstrate_tuple_performance()
    demonstrate_tuple_pitfalls()
    
    print("学习总结:")
    print("1. 元组是不可变的有序序列")
    print("2. 适用于不需要修改的数据")
    print("3. 可以作为字典键 (如果完全不可变)")
    print("4. 支持序列操作但不支持修改操作")
    print("5. 命名元组提供更好的可读性")
    print("6. 性能通常比列表稍好")
    print("7. 注意单元素元组的语法")


if __name__ == "__main__":
    main() 