#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法 - 条件判断语句
===========================

本文件演示Python的条件判断语句，并与Java进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""


def demonstrate_basic_if():
    """
    演示基本的if语句
    与Java的语法对比
    """
    print("=== 基本if语句 ===\n")
    
    print("1. 基本语法对比")
    print("   Java:")
    print("   if (condition) {")
    print("       // 代码块")
    print("   }")
    print()
    
    print("   Python:")
    print("   if condition:")
    print("       # 代码块")
    print()
    
    # Python示例
    age = 18
    print(f"年龄: {age}")
    
    if age >= 18:
        print("   已成年，可以投票")
    
    print("\n关键差异:")
    print("   - Python使用冒号(:)而不是花括号")
    print("   - Python使用缩进表示代码块")
    print("   - Python条件表达式不需要括号(但可以使用)")
    print()


def demonstrate_if_else():
    """
    演示if-else语句
    """
    print("=== if-else语句 ===\n")
    
    print("Java vs Python语法:")
    print("Java:                          Python:")
    print("if (score >= 60) {             if score >= 60:")
    print("    System.out.println(\"及格\");     print(\"及格\")")
    print("} else {                       else:")
    print("    System.out.println(\"不及格\");   print(\"不及格\")")
    print("}")
    print()
    
    # Python示例
    score = 75
    print(f"考试成绩: {score}")
    
    if score >= 60:
        print("   结果: 及格")
        if score >= 90:
            print("   等级: 优秀")
        elif score >= 80:
            print("   等级: 良好")
        else:
            print("   等级: 一般")
    else:
        print("   结果: 不及格")
        print("   建议: 继续努力")
    print()


def demonstrate_elif():
    """
    演示elif语句(Python特有)
    与Java的else if对比
    """
    print("=== elif语句 ===\n")
    
    print("Java的else if vs Python的elif:")
    print("Java:                          Python:")
    print("if (grade >= 90) {             if grade >= 90:")
    print("    result = \"A\";                 result = \"A\"")
    print("} else if (grade >= 80) {      elif grade >= 80:")
    print("    result = \"B\";                 result = \"B\"")
    print("} else if (grade >= 70) {      elif grade >= 70:")
    print("    result = \"C\";                 result = \"C\"")
    print("} else {                       else:")
    print("    result = \"D\";                 result = \"D\"")
    print("}")
    print()
    
    # Python示例
    grade = 85
    print(f"成绩: {grade}")
    
    if grade >= 90:
        result = "A"
        comment = "优秀"
    elif grade >= 80:
        result = "B"
        comment = "良好"
    elif grade >= 70:
        result = "C"
        comment = "中等"
    elif grade >= 60:
        result = "D"
        comment = "及格"
    else:
        result = "F"
        comment = "不及格"
    
    print(f"   等级: {result}")
    print(f"   评价: {comment}")
    print()


def demonstrate_truth_values():
    """
    演示Python的真值判断
    与Java布尔表达式的差异
    """
    print("=== 真值判断 ===\n")
    
    print("Java vs Python的布尔值判断:")
    print("Java: 只有boolean类型的true/false")
    print("Python: 多种类型都可以用于布尔判断")
    print()
    
    # 测试各种值的真假性
    test_values = [
        (True, "布尔真值"),
        (False, "布尔假值"),
        (1, "非零整数"),
        (0, "零"),
        (-1, "负数"),
        ("hello", "非空字符串"),
        ("", "空字符串"),
        ([1, 2, 3], "非空列表"),
        ([], "空列表"),
        ({"key": "value"}, "非空字典"),
        ({}, "空字典"),
        (None, "None值")
    ]
    
    print("值的真假性测试:")
    for value, description in test_values:
        if value:
            truth = "True"
        else:
            truth = "False"
        print(f"   {description:12} {repr(value):15} -> {truth}")
    
    print("\nPython假值规则:")
    print("   - None")
    print("   - False")
    print("   - 数字零: 0, 0.0, 0j")
    print("   - 空序列: '', [], ()")
    print("   - 空映射: {}")
    print("   - 其他所有值都为真")
    print()


def demonstrate_logical_operators():
    """
    演示逻辑运算符
    Python与Java的差异
    """
    print("=== 逻辑运算符 ===\n")
    
    print("Java vs Python逻辑运算符:")
    print("操作        Java    Python")
    print("逻辑与      &&      and")
    print("逻辑或      ||      or")
    print("逻辑非      !       not")
    print()
    
    # Python示例
    age = 25
    has_license = True
    has_car = False
    
    print(f"年龄: {age}, 有驾照: {has_license}, 有车: {has_car}")
    print()
    
    # and 运算符
    if age >= 18 and has_license:
        print("   可以开车 (年龄和驾照检查)")
    
    # or 运算符
    if has_car or age >= 25:
        print("   可以租车 (有车或年龄达到25岁)")
    
    # not 运算符
    if not has_car:
        print("   建议使用公共交通")
    
    # 复合条件
    if (age >= 21 and has_license) or (age >= 25 and not has_car):
        print("   符合特殊驾驶条件")
    
    print("\n短路求值演示:")
    
    def expensive_check():
        print("   执行了昂贵的检查函数")
        return True
    
    # 短路求值 - 如果第一个条件为False，不会执行第二个函数
    print("False and expensive_check():")
    if False and expensive_check():
        print("   不会到达这里")
    
    print("\nTrue or expensive_check():")
    if True or expensive_check():
        print("   到达这里，但expensive_check()没有执行")
    print()


def demonstrate_comparison_operators():
    """
    演示比较运算符
    Python的特殊功能
    """
    print("=== 比较运算符 ===\n")
    
    print("基本比较运算符 (与Java相同):")
    print("==  等于")
    print("!=  不等于")
    print("<   小于")
    print(">   大于")
    print("<=  小于等于")
    print(">=  大于等于")
    print()
    
    # 数字比较
    x, y, z = 10, 20, 10
    print(f"x={x}, y={y}, z={z}")
    print(f"x == z: {x == z}")
    print(f"x != y: {x != y}")
    print(f"x < y: {x < y}")
    print()
    
    print("Python特殊功能 - 链式比较:")
    print("Java: (x < y) && (y < z)")
    print("Python: x < y < z")
    print()
    
    # 链式比较示例
    a, b, c = 5, 10, 15
    print(f"a={a}, b={b}, c={c}")
    print(f"a < b < c: {a < b < c}")
    print(f"等价于: (a < b) and (b < c) = {(a < b) and (b < c)}")
    
    # 更复杂的链式比较
    score = 85
    print(f"\n成绩: {score}")
    if 80 <= score < 90:
        print("   良好等级 (80-89)")
    
    # 字符串比较
    print("\n字符串比较 (字典序):")
    str1, str2 = "apple", "banana"
    print(f"'{str1}' < '{str2}': {str1 < str2}")
    print(f"'{str1}' > '{str2}': {str1 > str2}")
    print()


def demonstrate_identity_operators():
    """
    演示身份运算符 is 和 is not
    与Java引用比较的对比
    """
    print("=== 身份运算符 ===\n")
    
    print("Java vs Python的引用比较:")
    print("Java: obj1 == obj2 (引用比较)")
    print("      obj1.equals(obj2) (内容比较)")
    print("Python: obj1 is obj2 (身份比较)")
    print("        obj1 == obj2 (值比较)")
    print()
    
    # 整数的身份比较
    a = 100
    b = 100
    c = 1000
    d = 1000
    
    print("小整数缓存:")
    print(f"a = {a}, b = {b}")
    print(f"a is b: {a is b} (小整数有缓存)")
    print(f"a == b: {a == b}")
    print()
    
    print("大整数:")
    print(f"c = {c}, d = {d}")
    print(f"c is d: {c is d} (大整数无缓存)")
    print(f"c == d: {c == d}")
    print()
    
    # 字符串的身份比较
    str1 = "hello"
    str2 = "hello"
    str3 = "hello" + " world"
    str4 = "hello world"
    
    print("字符串比较:")
    print(f"str1 = '{str1}', str2 = '{str2}'")
    print(f"str1 is str2: {str1 is str2}")
    print(f"str3 = '{str3}', str4 = '{str4}'")
    print(f"str3 is str4: {str3 is str4}")
    print()
    
    # None的比较
    print("None比较 (推荐使用is):")
    value = None
    print(f"value is None: {value is None} (推荐)")
    print(f"value == None: {value == None} (可行但不推荐)")
    print()


def demonstrate_membership_operators():
    """
    演示成员运算符 in 和 not in
    Java没有直接对应的运算符
    """
    print("=== 成员运算符 ===\n")
    
    print("Python的in运算符 (Java需要方法调用):")
    print("Python: item in collection")
    print("Java: collection.contains(item)")
    print()
    
    # 列表成员检查
    fruits = ["苹果", "香蕉", "橙子", "葡萄"]
    print(f"水果列表: {fruits}")
    
    if "苹果" in fruits:
        print("   列表中有苹果")
    
    if "芒果" not in fruits:
        print("   列表中没有芒果")
    
    # 字符串成员检查
    text = "Python编程很有趣"
    print(f"\n文本: '{text}'")
    
    if "Python" in text:
        print("   文本包含'Python'")
    
    if "Java" not in text:
        print("   文本不包含'Java'")
    
    # 字典成员检查 (检查键)
    student = {"name": "张三", "age": 20, "score": 95}
    print(f"\n学生信息: {student}")
    
    if "name" in student:
        print(f"   姓名: {student['name']}")
    
    if "phone" not in student:
        print("   没有电话信息")
    print()


def demonstrate_ternary_operator():
    """
    演示三元运算符
    Python与Java的语法差异
    """
    print("=== 三元运算符 ===\n")
    
    print("Java vs Python三元运算符:")
    print("Java: condition ? value_if_true : value_if_false")
    print("Python: value_if_true if condition else value_if_false")
    print()
    
    # Python三元运算符示例
    age = 20
    status = "成年人" if age >= 18 else "未成年人"
    print(f"年龄: {age}")
    print(f"状态: {status}")
    print()
    
    # 嵌套三元运算符
    score = 85
    grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D"
    print(f"成绩: {score}")
    print(f"等级: {grade}")
    print()
    
    # 与if-else的对比
    print("等价的if-else语句:")
    if score >= 90:
        grade_verbose = "A"
    elif score >= 80:
        grade_verbose = "B"
    elif score >= 70:
        grade_verbose = "C"
    else:
        grade_verbose = "D"
    
    print(f"详细等级: {grade_verbose}")
    print()


def demonstrate_match_statement():
    """
    演示match语句 (Python 3.10+)
    与Java的switch语句对比
    """
    print("=== match语句 (Python 3.10+) ===\n")
    
    print("Java switch vs Python match:")
    print("Java:                          Python:")
    print("switch (day) {                 match day:")
    print("    case 1:                        case 1:")
    print("        return \"周一\";                return \"周一\"")
    print("    case 2:                        case 2:")
    print("        return \"周二\";                return \"周二\"")
    print("    default:                       case _:")
    print("        return \"其他\";                return \"其他\"")
    print("}")
    print()
    
    # Python 3.10+的match语句
    try:
        def get_day_name(day):
            match day:
                case 1:
                    return "周一"
                case 2:
                    return "周二"
                case 3:
                    return "周三"
                case 4:
                    return "周四"
                case 5:
                    return "周五"
                case 6 | 7:  # 多个值匹配
                    return "周末"
                case _:  # 默认情况
                    return "无效的日期"
        
        print("match语句示例:")
        for day in [1, 3, 6, 8]:
            result = get_day_name(day)
            print(f"   day={day} -> {result}")
        
        print("\nmatch的高级模式匹配:")
        
        def process_data(data):
            match data:
                case int() if data > 0:
                    return f"正整数: {data}"
                case int() if data < 0:
                    return f"负整数: {data}"
                case 0:
                    return "零"
                case str() if len(data) > 0:
                    return f"非空字符串: {data}"
                case []:
                    return "空列表"
                case [x] if isinstance(x, int):
                    return f"单元素整数列表: {x}"
                case [x, y]:
                    return f"双元素列表: {x}, {y}"
                case _:
                    return f"其他类型: {type(data)}"
        
        test_data = [42, -10, 0, "hello", "", [], [5], [1, 2], {"key": "value"}]
        for data in test_data:
            result = process_data(data)
            print(f"   {repr(data)} -> {result}")
    
    except SyntaxError:
        print("注意: match语句需要Python 3.10+版本")
        print("当前版本不支持match语句")
    
    print()


def main():
    """主函数 - 演示所有条件判断功能"""
    print("Python基础语法学习 - 条件判断语句")
    print("=" * 50)
    
    demonstrate_basic_if()
    demonstrate_if_else()
    demonstrate_elif()
    demonstrate_truth_values()
    demonstrate_logical_operators()
    demonstrate_comparison_operators()
    demonstrate_identity_operators()
    demonstrate_membership_operators()
    demonstrate_ternary_operator()
    demonstrate_match_statement()
    
    print("学习总结:")
    print("1. Python使用缩进而不是花括号表示代码块")
    print("2. Python的elif比Java的else if更简洁")
    print("3. Python支持链式比较操作")
    print("4. Python的逻辑运算符是and/or/not而不是&&/||/!")
    print("5. Python使用is进行身份比较，==进行值比较")
    print("6. Python的in运算符非常方便进行成员检查")
    print("7. Python的三元运算符语法与Java不同")
    print("8. Python 3.10+的match语句比Java的switch更强大")


if __name__ == "__main__":
    main() 