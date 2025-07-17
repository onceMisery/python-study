#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法 - 字典(Dict)
==========================

本文件演示Python的字典类型，并与Java HashMap进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

from typing import Dict, Any, Optional, Union
from collections import defaultdict, OrderedDict, Counter
import json


def demonstrate_dict_creation():
    """
    演示字典创建的各种方式
    与Java HashMap对比
    """
    print("=== 字典创建 ===\n")
    
    print("Java HashMap vs Python Dict:")
    print("Java:")
    print("   Map<String, Integer> map = new HashMap<>();")
    print("   map.put(\"key\", value);")
    print("   Map<String, Integer> map = Map.of(\"a\", 1, \"b\", 2); // Java 9+")
    print()
    
    print("Python:")
    print("   dict = {}")
    print("   dict = {'key': value}")
    print("   dict = dict(key=value)")
    print()
    
    # 1. 空字典
    print("1. 创建空字典")
    empty_dict1 = {}
    empty_dict2 = dict()
    
    print(f"   {{}} = {empty_dict1}")
    print(f"   dict() = {empty_dict2}")
    print()
    
    # 2. 字面量创建
    print("2. 字面量创建")
    student = {
        "name": "张三",
        "age": 20,
        "grade": "大二",
        "scores": [85, 92, 78]
    }
    
    colors = {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF"}
    
    print(f"   学生信息: {student}")
    print(f"   颜色映射: {colors}")
    print()
    
    # 3. dict()构造函数
    print("3. dict()构造函数")
    
    # 关键字参数方式
    person1 = dict(name="李四", age=25, city="北京")
    
    # 键值对列表方式
    person2 = dict([("name", "王五"), ("age", 30), ("city", "上海")])
    
    # 从其他字典创建
    person3 = dict(person1)
    
    print(f"   关键字参数: {person1}")
    print(f"   键值对列表: {person2}")
    print(f"   从字典复制: {person3}")
    print()
    
    # 4. 字典推导式
    print("4. 字典推导式")
    
    # 数字平方映射
    squares = {x: x**2 for x in range(5)}
    
    # 字符串长度映射
    words = ["apple", "banana", "cherry"]
    lengths = {word: len(word) for word in words}
    
    # 带条件的推导式
    even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
    
    print(f"   数字平方: {squares}")
    print(f"   字符串长度: {lengths}")
    print(f"   偶数平方: {even_squares}")
    print()
    
    # 5. 从序列创建
    print("5. 从序列创建")
    
    keys = ["a", "b", "c"]
    values = [1, 2, 3]
    zipped_dict = dict(zip(keys, values))
    
    # 使用fromkeys创建具有相同值的字典
    default_dict = dict.fromkeys(keys, 0)
    
    print(f"   zip创建: {zipped_dict}")
    print(f"   fromkeys创建: {default_dict}")
    print()


def demonstrate_dict_access():
    """
    演示字典访问和修改
    Python的灵活语法
    """
    print("=== 字典访问和修改 ===\n")
    
    print("Java vs Python字典操作:")
    print("Java: map.get(key), map.put(key, value)")
    print("Python: dict[key], dict[key] = value")
    print()
    
    student = {
        "name": "张三",
        "age": 20,
        "grade": "大二",
        "scores": {"math": 85, "english": 92, "physics": 78}
    }
    
    print(f"学生信息: {student}")
    print()
    
    # 1. 访问元素
    print("1. 访问元素")
    
    print(f"   student['name'] = {student['name']}")
    print(f"   student['age'] = {student['age']}")
    print(f"   student['scores']['math'] = {student['scores']['math']}")
    print()
    
    # 2. 安全访问 - get方法
    print("2. 安全访问 - get方法")
    print("   Java: map.getOrDefault(key, defaultValue)")
    print("   Python: dict.get(key, default)")
    
    # 不存在的键
    phone = student.get("phone")
    phone_with_default = student.get("phone", "未提供")
    
    print(f"   student.get('phone') = {phone}")
    print(f"   student.get('phone', '未提供') = {phone_with_default}")
    print()
    
    # 3. 修改元素
    print("3. 修改元素")
    original_age = student["age"]
    student["age"] = 21
    student["phone"] = "13800138000"  # 添加新键
    
    print(f"   修改年龄: {original_age} -> {student['age']}")
    print(f"   添加电话: {student['phone']}")
    print(f"   修改后: {student}")
    print()
    
    # 4. 检查键是否存在
    print("4. 检查键是否存在")
    print("   Java: map.containsKey(key)")
    print("   Python: key in dict")
    
    keys_to_check = ["name", "email", "phone"]
    for key in keys_to_check:
        exists = key in student
        print(f"   '{key}' in student: {exists}")
    print()


def demonstrate_dict_methods():
    """
    演示字典的方法
    与Java HashMap方法对比
    """
    print("=== 字典方法 ===\n")
    
    # 测试字典
    inventory = {
        "apple": 50,
        "banana": 30,
        "orange": 25,
        "grape": 40
    }
    
    print(f"库存字典: {inventory}")
    print()
    
    # 1. 获取键、值、项
    print("1. 获取键、值、项")
    print("   Java: map.keySet(), map.values(), map.entrySet()")
    print("   Python: dict.keys(), dict.values(), dict.items()")
    
    print(f"   keys(): {list(inventory.keys())}")
    print(f"   values(): {list(inventory.values())}")
    print(f"   items(): {list(inventory.items())}")
    print()
    
    # 2. 更新字典
    print("2. 更新字典")
    print("   Java: map.putAll(otherMap)")
    print("   Python: dict.update(other)")
    
    new_items = {"mango": 15, "kiwi": 20}
    original_inventory = inventory.copy()
    
    inventory.update(new_items)
    inventory.update(apple=60)  # 关键字参数方式
    
    print(f"   原始库存: {original_inventory}")
    print(f"   新增项目: {new_items}")
    print(f"   更新后: {inventory}")
    print()
    
    # 3. 删除元素
    print("3. 删除元素")
    print("   Java: map.remove(key)")
    print("   Python: del dict[key], dict.pop(key), dict.popitem()")
    
    test_inventory = inventory.copy()
    
    # pop方法 - 删除并返回值
    popped_value = test_inventory.pop("kiwi")
    print(f"   pop('kiwi'): 删除的值 = {popped_value}")
    
    # pop方法带默认值
    popped_default = test_inventory.pop("watermelon", 0)
    print(f"   pop('watermelon', 0): {popped_default}")
    
    # popitem方法 - 删除并返回最后一个键值对
    last_item = test_inventory.popitem()
    print(f"   popitem(): {last_item}")
    
    # del语句
    del test_inventory["banana"]
    print(f"   del删除后: {test_inventory}")
    print()
    
    # 4. 清空和复制
    print("4. 清空和复制")
    print("   Java: map.clear(), new HashMap<>(map)")
    print("   Python: dict.clear(), dict.copy()")
    
    test_dict = {"a": 1, "b": 2, "c": 3}
    copy_dict = test_dict.copy()
    
    print(f"   原始字典: {test_dict}")
    print(f"   复制字典: {copy_dict}")
    
    test_dict.clear()
    print(f"   清空后: {test_dict}")
    print(f"   副本不受影响: {copy_dict}")
    print()
    
    # 5. setdefault方法
    print("5. setdefault方法 (Java没有直接对应)")
    print("   如果键不存在则设置默认值，存在则返回现有值")
    
    user_prefs = {"theme": "dark", "language": "zh"}
    
    # 设置默认值
    font_size = user_prefs.setdefault("font_size", 12)
    theme = user_prefs.setdefault("theme", "light")  # 已存在，不会修改
    
    print(f"   setdefault('font_size', 12): {font_size}")
    print(f"   setdefault('theme', 'light'): {theme}")
    print(f"   最终字典: {user_prefs}")
    print()


def demonstrate_dict_iteration():
    """
    演示字典遍历
    各种遍历方式
    """
    print("=== 字典遍历 ===\n")
    
    scores = {"语文": 85, "数学": 92, "英语": 78, "物理": 88}
    
    print(f"成绩字典: {scores}")
    print()
    
    # 1. 遍历键
    print("1. 遍历键")
    print("   Java: for (String key : map.keySet())")
    print("   Python: for key in dict:")
    
    print("   科目列表:")
    for subject in scores:  # 默认遍历键
        print(f"     {subject}")
    
    # 明确遍历键
    print("   使用keys():")
    for subject in scores.keys():
        print(f"     {subject}: {scores[subject]}分")
    print()
    
    # 2. 遍历值
    print("2. 遍历值")
    print("   Java: for (Integer value : map.values())")
    print("   Python: for value in dict.values()")
    
    total_score = 0
    for score in scores.values():
        total_score += score
        print(f"     {score}分")
    
    print(f"   总分: {total_score}")
    print()
    
    # 3. 遍历键值对
    print("3. 遍历键值对")
    print("   Java: for (Map.Entry<String, Integer> entry : map.entrySet())")
    print("   Python: for key, value in dict.items()")
    
    print("   成绩详情:")
    for subject, score in scores.items():
        grade = "优秀" if score >= 90 else "良好" if score >= 80 else "一般"
        print(f"     {subject}: {score}分 ({grade})")
    print()
    
    # 4. 带索引的遍历
    print("4. 带索引的遍历")
    print("   使用enumerate():")
    
    for i, (subject, score) in enumerate(scores.items(), 1):
        print(f"     {i}. {subject}: {score}分")
    print()
    
    # 5. 条件遍历
    print("5. 条件遍历")
    
    print("   高分科目 (>= 85分):")
    high_scores = {subject: score for subject, score in scores.items() if score >= 85}
    for subject, score in high_scores.items():
        print(f"     {subject}: {score}分")
    print()


def demonstrate_nested_dicts():
    """
    演示嵌套字典
    复杂数据结构
    """
    print("=== 嵌套字典 ===\n")
    
    # 复杂的嵌套字典结构
    company = {
        "name": "科技公司",
        "departments": {
            "开发部": {
                "manager": "张经理",
                "employees": [
                    {"name": "程序员A", "level": "高级", "salary": 15000},
                    {"name": "程序员B", "level": "中级", "salary": 12000}
                ],
                "projects": {
                    "项目1": {"status": "进行中", "deadline": "2024-03-01"},
                    "项目2": {"status": "已完成", "deadline": "2024-01-15"}
                }
            },
            "销售部": {
                "manager": "李经理", 
                "employees": [
                    {"name": "销售员A", "level": "资深", "salary": 10000},
                    {"name": "销售员B", "level": "初级", "salary": 8000}
                ]
            }
        }
    }
    
    print("1. 复杂嵌套字典结构")
    print(f"   公司名称: {company['name']}")
    print()
    
    # 访问嵌套数据
    print("2. 访问嵌套数据")
    dev_manager = company["departments"]["开发部"]["manager"]
    first_employee = company["departments"]["开发部"]["employees"][0]
    project1_status = company["departments"]["开发部"]["projects"]["项目1"]["status"]
    
    print(f"   开发部经理: {dev_manager}")
    print(f"   第一个员工: {first_employee['name']} ({first_employee['level']})")
    print(f"   项目1状态: {project1_status}")
    print()
    
    # 安全访问嵌套数据
    print("3. 安全访问嵌套数据")
    
    def safe_get(dictionary, *keys, default=None):
        """安全获取嵌套字典的值"""
        for key in keys:
            if isinstance(dictionary, dict) and key in dictionary:
                dictionary = dictionary[key]
            else:
                return default
        return dictionary
    
    # 使用安全访问函数
    hr_manager = safe_get(company, "departments", "人事部", "manager", default="未设置")
    dev_budget = safe_get(company, "departments", "开发部", "budget", default=0)
    
    print(f"   人事部经理: {hr_manager}")
    print(f"   开发部预算: {dev_budget}")
    print()
    
    # 遍历嵌套字典
    print("4. 遍历嵌套字典")
    print("   各部门员工信息:")
    
    for dept_name, dept_info in company["departments"].items():
        print(f"   {dept_name}:")
        print(f"     经理: {dept_info['manager']}")
        print(f"     员工数: {len(dept_info['employees'])}")
        
        for employee in dept_info["employees"]:
            print(f"       - {employee['name']}: {employee['level']} (￥{employee['salary']})")
        print()


def demonstrate_dict_special_types():
    """
    演示特殊字典类型
    collections模块的字典变体
    """
    print("=== 特殊字典类型 ===\n")
    
    # 1. defaultdict - 默认字典
    print("1. defaultdict - 自动创建默认值")
    print("   Java: 需要手动检查键是否存在")
    print("   Python: 自动为新键创建默认值")
    
    # 普通字典的问题
    normal_dict = {}
    try:
        normal_dict["new_key"].append("value")  # 会报错
    except KeyError as e:
        print(f"   普通字典错误: {e}")
    
    # defaultdict解决方案
    list_dict = defaultdict(list)  # 默认值为空列表
    count_dict = defaultdict(int)  # 默认值为0
    
    # 自动创建列表
    list_dict["fruits"].append("apple")
    list_dict["fruits"].append("banana")
    list_dict["colors"].append("red")
    
    # 自动创建计数器
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    for word in words:
        count_dict[word] += 1
    
    print(f"   list_dict: {dict(list_dict)}")
    print(f"   count_dict: {dict(count_dict)}")
    print()
    
    # 2. OrderedDict - 有序字典 (Python 3.7+普通dict也保持插入顺序)
    print("2. OrderedDict - 保持插入顺序")
    
    ordered = OrderedDict([("first", 1), ("second", 2), ("third", 3)])
    ordered["fourth"] = 4
    
    print(f"   有序字典: {ordered}")
    
    # 移动到末尾
    ordered.move_to_end("first")
    print(f"   移动first到末尾: {ordered}")
    print()
    
    # 3. Counter - 计数器
    print("3. Counter - 专门用于计数")
    
    text = "hello world"
    char_count = Counter(text)
    
    word_list = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    word_count = Counter(word_list)
    
    print(f"   字符计数: {char_count}")
    print(f"   单词计数: {word_count}")
    
    # Counter的特殊方法
    print(f"   最常见的2个字符: {char_count.most_common(2)}")
    print(f"   apple出现次数: {word_count['apple']}")
    
    # Counter运算
    more_words = Counter(["apple", "grape", "banana"])
    combined = word_count + more_words
    print(f"   合并计数: {combined}")
    print()


def demonstrate_dict_performance():
    """
    演示字典性能特点
    """
    print("=== 字典性能特点 ===\n")
    
    import time
    import random
    
    def time_operation(operation_name, operation_func):
        start_time = time.time()
        result = operation_func()
        end_time = time.time()
        duration = end_time - start_time
        print(f"   {operation_name}: {duration:.6f}秒")
        return result
    
    # 创建测试数据
    keys = [f"key_{i}" for i in range(100000)]
    values = list(range(100000))
    
    print("性能测试 (10万个键值对):")
    
    # 1. 创建字典性能
    print("\n1. 创建字典性能:")
    
    def create_with_loop():
        d = {}
        for k, v in zip(keys, values):
            d[k] = v
        return d
    
    def create_with_comprehension():
        return {k: v for k, v in zip(keys, values)}
    
    def create_with_dict():
        return dict(zip(keys, values))
    
    time_operation("循环创建", create_with_loop)
    time_operation("字典推导式", create_with_comprehension)
    time_operation("dict()构造", create_with_dict)
    
    # 2. 查找性能
    print("\n2. 查找性能 (vs 列表):")
    
    test_dict = dict(zip(keys, values))
    test_list = list(zip(keys, values))
    
    search_keys = random.sample(keys, 1000)
    
    def dict_lookup():
        count = 0
        for key in search_keys:
            if key in test_dict:
                count += 1
        return count
    
    def list_lookup():
        count = 0
        for key in search_keys:
            for k, v in test_list:
                if k == key:
                    count += 1
                    break
        return count
    
    time_operation("字典查找", dict_lookup)
    time_operation("列表查找", list_lookup)
    
    print("\n性能特点:")
    print("   1. 字典查找是O(1)平均时间复杂度")
    print("   2. 列表查找是O(n)时间复杂度")
    print("   3. 字典推导式通常比循环快")
    print("   4. 字典占用更多内存，但查找更快")
    print("   5. 键必须是可哈希的类型")
    print()


def demonstrate_dict_pitfalls():
    """
    演示字典常见陷阱
    """
    print("=== 字典常见陷阱 ===\n")
    
    print("1. 遍历时修改字典")
    
    # 错误的方式
    scores = {"语文": 85, "数学": 92, "英语": 65, "物理": 88}
    print(f"   原始成绩: {scores}")
    
    # 正确的方式 - 创建副本
    for subject, score in scores.copy().items():
        if score < 70:
            scores[subject] = 70  # 补考后最低70分
    
    print(f"   补考后: {scores}")
    print()
    
    print("2. 键的可变性问题")
    
    # 不能使用可变对象作为键
    try:
        bad_dict = {[1, 2]: "value"}  # 列表不能作为键
    except TypeError as e:
        print(f"   列表作为键: {e}")
    
    # 可以使用不可变对象
    good_dict = {(1, 2): "value", "string": "value", 42: "value"}
    print(f"   有效的键类型: {good_dict}")
    print()
    
    print("3. 默认值陷阱")
    
    # 使用可变对象作为默认值的问题
    def create_user_wrong(name, groups=[]):
        """错误的默认参数使用"""
        groups.append("默认组")
        return {"name": name, "groups": groups}
    
    def create_user_correct(name, groups=None):
        """正确的默认参数使用"""
        if groups is None:
            groups = []
        groups = groups.copy()  # 创建副本
        groups.append("默认组")
        return {"name": name, "groups": groups}
    
    user1 = create_user_wrong("张三")
    user2 = create_user_wrong("李四")
    print(f"   错误方式 - 用户1: {user1}")
    print(f"   错误方式 - 用户2: {user2}")  # 包含了用户1的组
    
    user3 = create_user_correct("王五")
    user4 = create_user_correct("赵六")
    print(f"   正确方式 - 用户3: {user3}")
    print(f"   正确方式 - 用户4: {user4}")
    print()


def main():
    """主函数 - 演示所有字典功能"""
    print("Python基础语法学习 - 字典(Dict)")
    print("=" * 50)
    
    demonstrate_dict_creation()
    demonstrate_dict_access()
    demonstrate_dict_methods()
    demonstrate_dict_iteration()
    demonstrate_nested_dicts()
    demonstrate_dict_special_types()
    demonstrate_dict_performance()
    demonstrate_dict_pitfalls()
    
    print("学习总结:")
    print("1. Python字典类似Java HashMap，但语法更简洁")
    print("2. 支持字典推导式，类似列表推导式")
    print("3. 字典是可变的，键必须是不可变类型")
    print("4. collections模块提供特殊字典类型")
    print("5. 字典查找是O(1)平均时间复杂度")
    print("6. Python 3.7+字典保持插入顺序")
    print("7. 避免在遍历时修改字典结构")


if __name__ == "__main__":
    main() 