#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法 - 字符串格式化方法
================================

本文件演示Python的各种字符串格式化方法
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

import datetime
from decimal import Decimal


def demonstrate_percent_formatting():
    """
    演示%格式化 (printf风格)
    """
    print("=== % 格式化 (printf风格) ===\n")
    
    print("类似C/Java的printf格式化:")
    print("Java: String.format(\"%s is %d years old\", name, age)")
    print("Python: \"%s is %d years old\" % (name, age)")
    print()
    
    # 基本数据
    name = "张三"
    age = 25
    salary = 15000.5
    is_active = True
    
    # 1. 基本格式化
    print("1. 基本格式化")
    
    basic_string = "%s is %d years old" % (name, age)
    mixed_types = "Name: %s, Age: %d, Salary: %.2f, Active: %s" % (name, age, salary, is_active)
    
    print(f"   基本: {basic_string}")
    print(f"   混合: {mixed_types}")
    print()
    
    # 2. 格式说明符
    print("2. 常用格式说明符")
    
    number = 42
    float_num = 3.14159
    
    formats = [
        ("%s", "字符串", name),
        ("%d", "整数", number),
        ("%f", "浮点数", float_num),
        ("%.2f", "精度浮点", float_num),
        ("%e", "科学计数", float_num),
        ("%x", "十六进制", number),
        ("%o", "八进制", number),
        ("%%", "百分号", None)
    ]
    
    for fmt, desc, value in formats:
        if value is not None:
            result = fmt % value if fmt != "%%" else "%%"
            print(f"   {fmt:8} - {desc:8}: {result}")
        else:
            print(f"   {fmt:8} - {desc:8}: %")
    print()
    
    # 3. 字段宽度和对齐
    print("3. 字段宽度和对齐")
    
    names = ["张三", "李四", "王五"]
    scores = [85, 92, 78]
    
    print("   默认对齐:")
    for n, s in zip(names, scores):
        print("     %s: %d" % (n, s))
    
    print("   指定宽度:")
    for n, s in zip(names, scores):
        print("     %10s: %3d" % (n, s))
    
    print("   左对齐:")
    for n, s in zip(names, scores):
        print("     %-10s: %-3d" % (n, s))
    print()
    
    # 4. 命名参数
    print("4. 命名参数 (字典)")
    
    person = {"name": "张三", "age": 25, "city": "北京"}
    
    named_format = "%(name)s来自%(city)s，今年%(age)d岁" % person
    print(f"   命名格式: {named_format}")
    
    # 重复使用参数
    repeated = "%(name)s说：'我是%(name)s，来自%(city)s'" % person
    print(f"   重复使用: {repeated}")
    print()


def demonstrate_format_method():
    """
    演示str.format()方法
    """
    print("=== str.format() 方法 ===\n")
    
    print("更现代的格式化方法:")
    print("优势: 更清晰的语法，更多功能")
    print()
    
    # 基本数据
    name = "李四"
    age = 30
    salary = 18000.75
    
    # 1. 位置参数
    print("1. 位置参数")
    
    positional = "{} is {} years old".format(name, age)
    indexed = "{0} is {1} years old. {0} works hard.".format(name, age)
    
    print(f"   位置参数: {positional}")
    print(f"   索引参数: {indexed}")
    print()
    
    # 2. 关键字参数
    print("2. 关键字参数")
    
    keyword = "{name} is {age} years old".format(name=name, age=age)
    mixed = "{0} ({name}) is {1} years old".format("李四", age, name="Li Si")
    
    print(f"   关键字: {keyword}")
    print(f"   混合方式: {mixed}")
    print()
    
    # 3. 格式规范
    print("3. 格式规范")
    
    pi = 3.14159265359
    large_number = 1234567890
    
    format_specs = [
        ("{:.2f}", "两位小数", pi),
        ("{:.4f}", "四位小数", pi),
        ("{:e}", "科学计数法", pi),
        ("{:,}", "千位分隔符", large_number),
        ("{:b}", "二进制", 42),
        ("{:x}", "十六进制", 255),
        ("{:o}", "八进制", 64)
    ]
    
    for fmt_template, desc, value in format_specs:
        result = fmt_template.format(value)
        print(f"   {fmt_template:10} - {desc:8}: {result}")
    print()
    
    # 4. 对齐和填充
    print("4. 对齐和填充")
    
    text = "Python"
    
    alignment_examples = [
        ("{:>10}", "右对齐", text),
        ("{:<10}", "左对齐", text),
        ("{:^10}", "居中对齐", text),
        ("{:*^10}", "居中填充*", text),
        ("{:0>8}", "右对齐填充0", text),
        ("{:-<10}", "左对齐填充-", text)
    ]
    
    for fmt_template, desc, value in alignment_examples:
        result = fmt_template.format(value)
        print(f"   {fmt_template:12} - {desc:10}: '{result}'")
    print()
    
    # 5. 数字格式化
    print("5. 数字格式化")
    
    price = 1234.5
    percentage = 0.755
    
    number_formats = [
        ("{:.2f}", "价格格式", price),
        ("{:,.2f}", "货币格式", price),
        ("{:.1%}", "百分比", percentage),
        ("{:+.2f}", "显示符号", price),
        ("{: .2f}", "正数前空格", price),
        ("{:8.2f}", "固定宽度", price)
    ]
    
    for fmt_template, desc, value in number_formats:
        result = fmt_template.format(value)
        print(f"   {fmt_template:12} - {desc:8}: '{result}'")
    print()
    
    # 6. 字典和对象格式化
    print("6. 字典和对象格式化")
    
    person = {"name": "王五", "age": 28, "salary": 20000}
    
    # 字典解包
    dict_format = "{name} (age {age}) earns {salary:,}".format(**person)
    print(f"   字典解包: {dict_format}")
    
    # 属性访问
    class Employee:
        def __init__(self, name, title):
            self.name = name
            self.title = title
    
    emp = Employee("赵六", "软件工程师")
    obj_format = "{0.name} is a {0.title}".format(emp)
    print(f"   对象属性: {obj_format}")
    print()


def demonstrate_fstring():
    """
    演示f-string格式化 (Python 3.6+)
    """
    print("=== f-string 格式化 (推荐) ===\n")
    
    print("f-string - 最现代的格式化方式:")
    print("优势: 简洁、高效、可读性强")
    print("语法: f'text {expression} text'")
    print()
    
    # 基本数据
    name = "赵六"
    age = 35
    salary = 25000.0
    
    # 1. 基本f-string
    print("1. 基本f-string")
    
    basic = f"{name} is {age} years old"
    expression = f"Next year {name} will be {age + 1}"
    
    print(f"   基本语法: {basic}")
    print(f"   表达式: {expression}")
    print()
    
    # 2. 格式规范
    print("2. 格式规范")
    
    pi = 3.14159265359
    large_num = 1234567890
    
    print(f"   两位小数: {pi:.2f}")
    print(f"   科学记数: {pi:e}")
    print(f"   千位分隔: {large_num:,}")
    print(f"   百分比: {0.456:.1%}")
    print(f"   十六进制: {255:x}")
    print()
    
    # 3. 对齐和填充
    print("3. 对齐和填充")
    
    text = "Python"
    
    print(f"   右对齐: '{text:>10}'")
    print(f"   左对齐: '{text:<10}'")
    print(f"   居中: '{text:^10}'")
    print(f"   填充字符: '{text:*^12}'")
    print()
    
    # 4. 复杂表达式
    print("4. 复杂表达式")
    
    numbers = [1, 2, 3, 4, 5]
    
    print(f"   列表长度: {len(numbers)}")
    print(f"   列表总和: {sum(numbers)}")
    print(f"   列表平均值: {sum(numbers) / len(numbers):.2f}")
    print(f"   最大值: {max(numbers)}")
    
    # 字典访问
    person = {"name": "张三", "age": 25}
    print(f"   字典访问: {person['name']} is {person['age']} years old")
    print()
    
    # 5. 方法调用
    print("5. 方法调用")
    
    text = "hello world"
    
    print(f"   大写: {text.upper()}")
    print(f"   标题: {text.title()}")
    print(f"   替换: {text.replace('world', 'Python')}")
    
    # 当前时间
    now = datetime.datetime.now()
    print(f"   当前时间: {now:%Y-%m-%d %H:%M:%S}")
    print()
    
    # 6. 条件表达式
    print("6. 条件表达式")
    
    score = 85
    
    print(f"   成绩评级: {score} ({'优秀' if score >= 90 else '良好' if score >= 80 else '一般'})")
    
    # 复杂条件
    status = "active" if age < 60 else "senior"
    print(f"   员工状态: {name} is {status}")
    print()
    
    # 7. 调试用法 (Python 3.8+)
    print("7. 调试用法 (Python 3.8+)")
    
    x = 10
    y = 20
    
    # = 符号会显示表达式和结果
    try:
        # 这在Python 3.8+中可用
        exec("print(f'{x=}, {y=}, {x+y=}')")
    except:
        print(f"   x={x}, y={y}, x+y={x+y}")
    print()


def demonstrate_template_strings():
    """
    演示Template字符串
    """
    print("=== Template 字符串 ===\n")
    
    print("Template字符串 - 安全的替换:")
    print("优势: 避免代码注入，适合用户输入")
    print()
    
    from string import Template
    
    # 1. 基本Template
    print("1. 基本Template使用")
    
    tmpl = Template("Hello $name, welcome to $place!")
    result = tmpl.substitute(name="张三", place="Python世界")
    
    print(f"   模板: {tmpl.template}")
    print(f"   结果: {result}")
    print()
    
    # 2. 字典替换
    print("2. 字典替换")
    
    data = {
        "product": "Python课程",
        "price": 299,
        "discount": 0.8
    }
    
    price_tmpl = Template("$product 原价 ¥$price，折后价 ¥${price}")
    # 需要特殊处理计算
    data["final_price"] = int(data["price"] * data["discount"])
    
    price_tmpl2 = Template("$product 原价 ¥$price，折后价 ¥$final_price")
    result = price_tmpl2.substitute(data)
    
    print(f"   模板: {price_tmpl2.template}")
    print(f"   结果: {result}")
    print()
    
    # 3. safe_substitute
    print("3. safe_substitute - 安全替换")
    
    incomplete_tmpl = Template("Name: $name, Age: $age, City: $city")
    incomplete_data = {"name": "李四", "age": 30}
    
    try:
        # substitute会抛出异常
        normal_result = incomplete_tmpl.substitute(incomplete_data)
    except KeyError as e:
        print(f"   substitute错误: {e}")
    
    # safe_substitute不会抛出异常
    safe_result = incomplete_tmpl.safe_substitute(incomplete_data)
    print(f"   safe_substitute: {safe_result}")
    print()


def demonstrate_advanced_formatting():
    """
    演示高级格式化技巧
    """
    print("=== 高级格式化技巧 ===\n")
    
    # 1. 动态格式规范
    print("1. 动态格式规范")
    
    precision = 3
    width = 10
    value = 3.14159
    
    # 使用嵌套的{}
    dynamic_format = "{value:{width}.{precision}f}".format(
        value=value, width=width, precision=precision
    )
    
    # f-string版本
    f_dynamic = f"{value:{width}.{precision}f}"
    
    print(f"   动态格式 (format): '{dynamic_format}'")
    print(f"   动态格式 (f-string): '{f_dynamic}'")
    print()
    
    # 2. 自定义格式化类
    print("2. 自定义格式化类")
    
    class Money:
        def __init__(self, amount, currency="CNY"):
            self.amount = amount
            self.currency = currency
        
        def __format__(self, format_spec):
            if format_spec == "":
                return f"{self.amount:.2f} {self.currency}"
            elif format_spec == "c":
                return f"¥{self.amount:,.2f}"
            elif format_spec == "s":
                return f"{self.amount:.2f}"
            else:
                return f"{self.amount:{format_spec}} {self.currency}"
    
    price = Money(1234.567)
    
    print(f"   默认格式: {price}")
    print(f"   货币格式: {price:c}")
    print(f"   数字格式: {price:s}")
    print(f"   自定义格式: {price:.1f}")
    print()
    
    # 3. 表格格式化
    print("3. 表格格式化")
    
    data = [
        ("姓名", "年龄", "薪资"),
        ("张三", 25, 15000),
        ("李四", 30, 18000),
        ("王五", 28, 16500)
    ]
    
    # 计算列宽
    col_widths = [max(len(str(row[i])) for row in data) for i in range(3)]
    
    print("   表格数据:")
    for row in data:
        formatted_row = " | ".join(f"{str(item):{col_widths[i]}}" for i, item in enumerate(row))
        print(f"   {formatted_row}")
        
        # 在标题行后添加分隔线
        if row == data[0]:
            separator = " | ".join("-" * col_widths[i] for i in range(3))
            print(f"   {separator}")
    print()
    
    # 4. 多行字符串格式化
    print("4. 多行字符串格式化")
    
    person = {
        "name": "张三",
        "age": 25,
        "email": "zhangsan@example.com",
        "address": "北京市朝阳区"
    }
    
    # 使用三引号字符串
    card = f"""
    ╭─────────────────────────╮
    │  个人信息卡片           │
    ├─────────────────────────┤
    │  姓名: {person['name']:<15} │
    │  年龄: {person['age']:<15} │
    │  邮箱: {person['email']:<15} │
    │  地址: {person['address']:<15} │
    ╰─────────────────────────╯
    """
    
    print(card)


def demonstrate_performance_comparison():
    """
    演示不同格式化方法的性能对比
    """
    print("=== 格式化性能对比 ===\n")
    
    import time
    
    def time_formatting(method_name, format_func, iterations=100000):
        start_time = time.time()
        for _ in range(iterations):
            result = format_func()
        end_time = time.time()
        duration = end_time - start_time
        print(f"   {method_name}: {duration:.6f}秒 ({iterations}次)")
        return duration
    
    # 测试数据
    name = "张三"
    age = 25
    salary = 15000.5
    
    print("性能测试 (10万次格式化):")
    
    # 不同格式化方法
    def percent_format():
        return "%s is %d years old, salary: %.2f" % (name, age, salary)
    
    def str_format():
        return "{} is {} years old, salary: {:.2f}".format(name, age, salary)
    
    def fstring_format():
        return f"{name} is {age} years old, salary: {salary:.2f}"
    
    def concat_format():
        return name + " is " + str(age) + " years old, salary: " + str(round(salary, 2))
    
    # 性能测试
    time_formatting("% 格式化", percent_format)
    time_formatting("str.format()", str_format)
    time_formatting("f-string", fstring_format)
    time_formatting("字符串连接", concat_format)
    
    print("\n性能结论:")
    print("   1. f-string 通常是最快的")
    print("   2. % 格式化 也很快")
    print("   3. str.format() 稍慢但功能强大")
    print("   4. 字符串连接 对于复杂格式最慢")
    print("\n推荐:")
    print("   - 日常使用: f-string")
    print("   - 模板需求: str.format() 或 Template")
    print("   - 国际化: % 格式化")


def main():
    """主函数 - 演示所有格式化方法"""
    print("Python基础语法学习 - 字符串格式化方法")
    print("=" * 60)
    
    demonstrate_percent_formatting()
    demonstrate_format_method()
    demonstrate_fstring()
    demonstrate_template_strings()
    demonstrate_advanced_formatting()
    demonstrate_performance_comparison()
    
    print("\n学习总结:")
    print("1. Python提供多种字符串格式化方法")
    print("2. f-string是最现代和推荐的方式")
    print("3. str.format()功能最全面")
    print("4. % 格式化兼容性好")
    print("5. Template适合处理用户输入")
    print("6. 选择格式化方法要考虑性能和需求")


if __name__ == "__main__":
    main() 