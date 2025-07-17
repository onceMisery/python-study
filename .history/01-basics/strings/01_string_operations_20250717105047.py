#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python基础语法 - 字符串操作
==========================

本文件演示Python的字符串操作，并与Java String进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

import re
import string
from typing import List, Optional


def demonstrate_string_creation():
    """
    演示字符串创建的各种方式
    与Java String对比
    """
    print("=== 字符串创建 ===\n")
    
    print("Java vs Python字符串创建:")
    print("Java:")
    print("   String str = \"hello\";")
    print("   String str = new String(\"hello\");")
    print("   String multiline = \"\"\"")
    print("       多行字符串")
    print("       \"\"\"; // Java 15+")
    print()
    
    print("Python:")
    print("   str = 'hello'")
    print("   str = \"hello\"")
    print("   str = '''多行字符串'''")
    print("   str = \"\"\"多行字符串\"\"\"")
    print()
    
    # 1. 基本字符串创建
    print("1. 基本字符串创建")
    
    single_quote = '单引号字符串'
    double_quote = "双引号字符串"
    mixed_content = "包含'单引号'的字符串"
    escaped_quote = "包含\"双引号\"的字符串"
    
    print(f"   单引号: {single_quote}")
    print(f"   双引号: {double_quote}")
    print(f"   混合引号: {mixed_content}")
    print(f"   转义引号: {escaped_quote}")
    print()
    
    # 2. 多行字符串
    print("2. 多行字符串")
    
    multiline_single = '''这是一个
    多行字符串
    使用三个单引号'''
    
    multiline_double = """这是另一个
    多行字符串
    使用三个双引号"""
    
    print(f"   三单引号: {repr(multiline_single)}")
    print(f"   三双引号: {repr(multiline_double)}")
    print()
    
    # 3. 原始字符串 (Raw String)
    print("3. 原始字符串 (r'' 或 R'')")
    print("   Java需要双重转义: \"C:\\\\Users\\\\name\"")
    print("   Python原始字符串: r'C:\\Users\\name'")
    
    normal_path = "C:\\Users\\name\\documents"
    raw_path = r"C:\Users\name\documents"
    regex_pattern = r"\d{3}-\d{2}-\d{4}"
    
    print(f"   普通字符串: {repr(normal_path)}")
    print(f"   原始字符串: {repr(raw_path)}")
    print(f"   正则表达式: {regex_pattern}")
    print()
    
    # 4. 字符串连接
    print("4. 字符串连接")
    
    # 简单连接
    hello = "Hello"
    world = "World"
    greeting = hello + " " + world
    
    print(f"   + 连接: {greeting}")
    
    # 多个字符串字面量自动连接
    auto_concat = "这是" "自动" "连接的" "字符串"
    print(f"   自动连接: {auto_concat}")
    
    # 重复
    repeated = "Python " * 3
    print(f"   重复: {repeated}")
    print()


def demonstrate_string_formatting():
    """
    演示字符串格式化
    Python的多种格式化方式
    """
    print("=== 字符串格式化 ===\n")
    
    print("Java vs Python字符串格式化:")
    print("Java:")
    print("   String.format(\"Name: %s, Age: %d\", name, age)")
    print("   System.out.printf(\"Name: %s, Age: %d\", name, age)")
    print()
    
    print("Python:")
    print("   \"Name: %s, Age: %d\" % (name, age)")
    print("   \"Name: {}, Age: {}\".format(name, age)")
    print("   f\"Name: {name}, Age: {age}\"  # f-string")
    print()
    
    # 测试数据
    name = "张三"
    age = 25
    score = 98.5
    is_student = True
    
    # 1. % 格式化 (旧式)
    print("1. % 格式化 (printf风格)")
    
    percent_basic = "姓名: %s, 年龄: %d" % (name, age)
    percent_advanced = "姓名: %s, 年龄: %d, 成绩: %.2f" % (name, age, score)
    
    print(f"   基本格式: {percent_basic}")
    print(f"   高级格式: {percent_advanced}")
    
    # 命名参数
    percent_named = "姓名: %(name)s, 年龄: %(age)d" % {"name": name, "age": age}
    print(f"   命名参数: {percent_named}")
    print()
    
    # 2. str.format() 方法
    print("2. str.format() 方法")
    
    format_basic = "姓名: {}, 年龄: {}".format(name, age)
    format_indexed = "姓名: {0}, 年龄: {1}, 再次: {0}".format(name, age)
    format_named = "姓名: {name}, 年龄: {age}".format(name=name, age=age)
    
    print(f"   基本格式: {format_basic}")
    print(f"   索引格式: {format_indexed}")
    print(f"   命名格式: {format_named}")
    
    # 格式规范
    format_precision = "成绩: {:.2f}, 百分比: {:.1%}".format(score, score/100)
    format_padding = "姓名: {:>10}, 年龄: {:0>3}".format(name, age)
    
    print(f"   精度控制: {format_precision}")
    print(f"   填充对齐: {format_padding}")
    print()
    
    # 3. f-string (Python 3.6+, 推荐)
    print("3. f-string 格式化 (推荐)")
    
    fstring_basic = f"姓名: {name}, 年龄: {age}"
    fstring_expression = f"明年年龄: {age + 1}"
    fstring_format = f"成绩: {score:.2f}, 是否学生: {is_student}"
    
    print(f"   基本格式: {fstring_basic}")
    print(f"   表达式: {fstring_expression}")
    print(f"   格式控制: {fstring_format}")
    
    # f-string高级用法
    fstring_advanced = f"姓名: {name:>10}, 成绩: {score:8.2f}%"
    fstring_datetime = f"当前时间: {__import__('datetime').datetime.now():%Y-%m-%d %H:%M:%S}"
    
    print(f"   高级格式: {fstring_advanced}")
    print(f"   时间格式: {fstring_datetime}")
    print()
    
    # 4. Template 字符串 (较少使用)
    print("4. Template 字符串")
    
    from string import Template
    
    template = Template("姓名: $name, 年龄: $age")
    template_result = template.substitute(name=name, age=age)
    
    print(f"   Template: {template_result}")
    print()


def demonstrate_string_methods():
    """
    演示字符串的方法
    与Java String方法对比
    """
    print("=== 字符串方法 ===\n")
    
    # 测试字符串
    text = "  Hello, Python World!  "
    chinese_text = "你好，Python世界！"
    mixed_text = "Hello123World"
    
    print(f"测试字符串: '{text}'")
    print(f"中文字符串: '{chinese_text}'")
    print(f"混合字符串: '{mixed_text}'")
    print()
    
    # 1. 大小写转换
    print("1. 大小写转换")
    print("   Java: str.toLowerCase(), str.toUpperCase()")
    print("   Python: str.lower(), str.upper(), str.title(), str.capitalize()")
    
    sample = "hello WORLD"
    print(f"   原字符串: '{sample}'")
    print(f"   lower(): '{sample.lower()}'")
    print(f"   upper(): '{sample.upper()}'")
    print(f"   title(): '{sample.title()}'")
    print(f"   capitalize(): '{sample.capitalize()}'")
    print(f"   swapcase(): '{sample.swapcase()}'")
    print()
    
    # 2. 空白字符处理
    print("2. 空白字符处理")
    print("   Java: str.trim(), str.strip() (Java 11+)")
    print("   Python: str.strip(), str.lstrip(), str.rstrip()")
    
    print(f"   原字符串: '{text}'")
    print(f"   strip(): '{text.strip()}'")
    print(f"   lstrip(): '{text.lstrip()}'")
    print(f"   rstrip(): '{text.rstrip()}'")
    print()
    
    # 3. 查找和替换
    print("3. 查找和替换")
    print("   Java: str.indexOf(), str.contains(), str.replace()")
    print("   Python: str.find(), str.index(), str.replace(), in 运算符")
    
    search_text = "Python is great. Python is powerful."
    print(f"   搜索文本: '{search_text}'")
    
    # 查找
    print(f"   find('Python'): {search_text.find('Python')}")  # 第一次出现的位置
    print(f"   rfind('Python'): {search_text.rfind('Python')}")  # 最后一次出现的位置
    print(f"   count('Python'): {search_text.count('Python')}")  # 出现次数
    print(f"   'Python' in text: {'Python' in search_text}")  # 成员检查
    
    # 替换
    replaced = search_text.replace("Python", "Java")
    replaced_once = search_text.replace("Python", "Java", 1)  # 只替换第一个
    print(f"   replace('Python', 'Java'): '{replaced}'")
    print(f"   replace(..., 1): '{replaced_once}'")
    print()
    
    # 4. 分割和连接
    print("4. 分割和连接")
    print("   Java: str.split(), String.join() (Java 8+)")
    print("   Python: str.split(), str.join()")
    
    csv_data = "apple,banana,orange,grape"
    sentence = "Hello world Python programming"
    
    # 分割
    fruits = csv_data.split(",")
    words = sentence.split()  # 默认按空白字符分割
    words_limited = sentence.split(" ", 2)  # 限制分割次数
    
    print(f"   CSV数据: '{csv_data}'")
    print(f"   split(','): {fruits}")
    print(f"   句子: '{sentence}'")
    print(f"   split(): {words}")
    print(f"   split(' ', 2): {words_limited}")
    
    # 连接
    joined_fruits = " | ".join(fruits)
    joined_words = "-".join(words)
    
    print(f"   ' | '.join(fruits): '{joined_fruits}'")
    print(f"   '-'.join(words): '{joined_words}'")
    print()
    
    # 5. 字符串测试方法
    print("5. 字符串测试方法")
    
    test_strings = [
        "12345",
        "abc123",
        "ABC",
        "hello world",
        "Hello World",
        "   ",
        ""
    ]
    
    print("   字符串测试方法结果:")
    print("   {:15} {:8} {:8} {:8} {:8} {:8} {:8}".format(
        "字符串", "isdigit", "isalpha", "isalnum", "isupper", "islower", "isspace"))
    print("   " + "-" * 80)
    
    for s in test_strings:
        print("   {:15} {:8} {:8} {:8} {:8} {:8} {:8}".format(
            repr(s),
            str(s.isdigit()),
            str(s.isalpha()),
            str(s.isalnum()),
            str(s.isupper()),
            str(s.islower()),
            str(s.isspace())
        ))
    print()


def demonstrate_string_slicing():
    """
    演示字符串切片
    Python的强大特性
    """
    print("=== 字符串切片 ===\n")
    
    print("Java vs Python字符串截取:")
    print("Java: str.substring(start, end)")
    print("Python: str[start:end:step]")
    print()
    
    text = "Hello, Python World!"
    print(f"原字符串: '{text}'")
    print(f"长度: {len(text)}")
    print()
    
    # 1. 基本切片
    print("1. 基本切片")
    
    print(f"   text[0:5]: '{text[0:5]}'")      # 前5个字符
    print(f"   text[7:13]: '{text[7:13]}'")    # 从索引7到12
    print(f"   text[:5]: '{text[:5]}'")        # 从开始到索引4
    print(f"   text[7:]: '{text[7:]}'")        # 从索引7到结束
    print(f"   text[:]: '{text[:]}'")          # 完整字符串（复制）
    print()
    
    # 2. 负索引切片
    print("2. 负索引切片")
    
    print(f"   text[-6:]: '{text[-6:]}'")      # 最后6个字符
    print(f"   text[:-6]: '{text[:-6]}'")      # 除了最后6个字符
    print(f"   text[-13:-7]: '{text[-13:-7]}'")  # 中间部分
    print()
    
    # 3. 步长切片
    print("3. 步长切片")
    
    print(f"   text[::2]: '{text[::2]}'")      # 每隔一个字符
    print(f"   text[1::2]: '{text[1::2]}'")    # 从索引1开始，每隔一个
    print(f"   text[::-1]: '{text[::-1]}'")    # 反转字符串
    print(f"   text[::3]: '{text[::3]}'")      # 每隔两个字符
    print()
    
    # 4. 实用切片技巧
    print("4. 实用切片技巧")
    
    # 字符串反转
    reversed_text = text[::-1]
    print(f"   反转字符串: '{reversed_text}'")
    
    # 去除文件扩展名
    filename = "document.pdf"
    name_only = filename[:-4] if filename.endswith(".pdf") else filename
    print(f"   去除扩展名: '{filename}' -> '{name_only}'")
    
    # 提取中间部分
    email = "user@example.com"
    username = email[:email.find("@")]
    domain = email[email.find("@") + 1:]
    print(f"   邮箱分析: '{email}' -> 用户名: '{username}', 域名: '{domain}'")
    print()


def demonstrate_string_encoding():
    """
    演示字符串编码
    Unicode处理
    """
    print("=== 字符串编码 ===\n")
    
    print("Java vs Python字符串编码:")
    print("Java: String内部使用UTF-16")
    print("Python 3: str使用Unicode, bytes用于字节序列")
    print()
    
    # 1. Unicode字符串
    print("1. Unicode字符串")
    
    chinese = "你好世界"
    emoji = "Python 🐍 编程"
    mixed = "Hello 世界 🌍"
    
    print(f"   中文字符串: '{chinese}'")
    print(f"   包含emoji: '{emoji}'")
    print(f"   混合字符: '{mixed}'")
    
    # 字符串长度 vs 字节长度
    print(f"   中文字符数: {len(chinese)}")
    print(f"   UTF-8字节数: {len(chinese.encode('utf-8'))}")
    print()
    
    # 2. 编码和解码
    print("2. 编码和解码")
    
    text = "Hello 世界"
    
    # 编码为字节
    utf8_bytes = text.encode('utf-8')
    gbk_bytes = text.encode('gbk')
    
    print(f"   原始字符串: '{text}'")
    print(f"   UTF-8编码: {utf8_bytes}")
    print(f"   GBK编码: {gbk_bytes}")
    
    # 解码回字符串
    decoded_utf8 = utf8_bytes.decode('utf-8')
    decoded_gbk = gbk_bytes.decode('gbk')
    
    print(f"   UTF-8解码: '{decoded_utf8}'")
    print(f"   GBK解码: '{decoded_gbk}'")
    print()
    
    # 3. 编码错误处理
    print("3. 编码错误处理")
    
    problematic_text = "Hello 世界 💻"
    
    try:
        # ASCII不能编码中文和emoji
        ascii_bytes = problematic_text.encode('ascii')
    except UnicodeEncodeError as e:
        print(f"   ASCII编码错误: {e}")
    
    # 错误处理策略
    ascii_ignore = problematic_text.encode('ascii', errors='ignore')
    ascii_replace = problematic_text.encode('ascii', errors='replace')
    ascii_xmlcharrefreplace = problematic_text.encode('ascii', errors='xmlcharrefreplace')
    
    print(f"   ignore策略: {ascii_ignore}")
    print(f"   replace策略: {ascii_replace}")
    print(f"   xmlcharrefreplace策略: {ascii_xmlcharrefreplace}")
    print()
    
    # 4. 字符信息
    print("4. 字符信息")
    
    chars = "A中🐍"
    
    for char in chars:
        print(f"   字符: '{char}'")
        print(f"     Unicode码点: U+{ord(char):04X}")
        print(f"     UTF-8字节: {char.encode('utf-8')}")
        print(f"     是否为字母: {char.isalpha()}")
        print(f"     是否为数字: {char.isdigit()}")
        print()


def demonstrate_regular_expressions():
    """
    演示正则表达式
    文本模式匹配
    """
    print("=== 正则表达式 ===\n")
    
    print("Java vs Python正则表达式:")
    print("Java: Pattern.compile(), Matcher")
    print("Python: re模块")
    print()
    
    # 测试文本
    text = """
    联系信息:
    邮箱: zhang.san@example.com, li.si@company.org
    电话: 138-0013-8000, (010)12345678
    网址: https://www.example.com, http://blog.example.org
    日期: 2024-01-16, 2024/12/25
    """
    
    print(f"测试文本: {text}")
    print()
    
    # 1. 基本匹配
    print("1. 基本正则表达式匹配")
    
    # 邮箱匹配
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    print(f"   邮箱地址: {emails}")
    
    # 电话号码匹配
    phone_pattern = r'(\d{3}[-.]?\d{4}[-.]?\d{4}|\(\d{3}\)\d{8})'
    phones = re.findall(phone_pattern, text)
    print(f"   电话号码: {phones}")
    
    # URL匹配
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    print(f"   网址: {urls}")
    
    # 日期匹配
    date_pattern = r'\d{4}[-/]\d{1,2}[-/]\d{1,2}'
    dates = re.findall(date_pattern, text)
    print(f"   日期: {dates}")
    print()
    
    # 2. 编译正则表达式
    print("2. 编译正则表达式 (提高性能)")
    
    email_regex = re.compile(email_pattern)
    email_matches = email_regex.findall(text)
    print(f"   编译后匹配邮箱: {email_matches}")
    
    # 使用search和match
    first_email = email_regex.search(text)
    if first_email:
        print(f"   第一个邮箱: '{first_email.group()}'")
        print(f"   位置: {first_email.start()}-{first_email.end()}")
    print()
    
    # 3. 分组匹配
    print("3. 分组匹配")
    
    # 解析姓名和邮箱
    name_email_pattern = r'(\w+)\.(\w+)@([^,\s]+)'
    name_email_matches = re.findall(name_email_pattern, text)
    
    print("   姓名邮箱解析:")
    for match in name_email_matches:
        first_name, last_name, domain = match
        print(f"     姓: {first_name}, 名: {last_name}, 域名: {domain}")
    print()
    
    # 4. 替换操作
    print("4. 正则替换")
    
    # 隐藏邮箱
    hidden_email = re.sub(email_pattern, "[邮箱已隐藏]", text)
    print("   隐藏邮箱后的文本:")
    print(hidden_email)
    
    # 格式化电话号码
    def format_phone(match):
        phone = match.group()
        # 简单格式化
        digits = re.sub(r'\D', '', phone)
        if len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        return phone
    
    formatted_text = re.sub(phone_pattern, format_phone, text)
    print("   格式化电话号码后:")
    print(formatted_text)


def demonstrate_string_performance():
    """
    演示字符串性能考虑
    """
    print("\n=== 字符串性能考虑 ===\n")
    
    import time
    
    def time_operation(operation_name, operation_func, iterations=10000):
        start_time = time.time()
        for _ in range(iterations):
            result = operation_func()
        end_time = time.time()
        duration = end_time - start_time
        print(f"   {operation_name}: {duration:.6f}秒 ({iterations}次)")
        return result, duration
    
    print("性能测试:")
    
    # 1. 字符串连接性能
    print("\n1. 字符串连接性能对比:")
    
    words = ["Python", "is", "awesome", "and", "powerful"]
    
    def concat_with_plus():
        result = ""
        for word in words:
            result += word + " "
        return result.strip()
    
    def concat_with_join():
        return " ".join(words)
    
    def concat_with_format():
        return " {} {} {} {} {}".format(*words)
    
    def concat_with_fstring():
        return f"{words[0]} {words[1]} {words[2]} {words[3]} {words[4]}"
    
    time_operation("+ 连接", concat_with_plus)
    time_operation("join方法", concat_with_join)
    time_operation("format方法", concat_with_format)
    time_operation("f-string", concat_with_fstring)
    
    # 2. 字符串搜索性能
    print("\n2. 字符串搜索性能:")
    
    large_text = "Python " * 10000 + "target" + " text" * 10000
    
    def search_with_in():
        return "target" in large_text
    
    def search_with_find():
        return large_text.find("target") != -1
    
    def search_with_regex():
        return re.search("target", large_text) is not None
    
    time_operation("in 运算符", search_with_in, 1000)
    time_operation("find 方法", search_with_find, 1000)
    time_operation("正则表达式", search_with_regex, 1000)
    
    print("\n性能优化建议:")
    recommendations = [
        "使用join()而不是+连接大量字符串",
        "使用in运算符进行简单搜索",
        "编译正则表达式用于重复匹配",
        "使用f-string进行字符串格式化",
        "避免在循环中进行复杂的字符串操作",
        "使用str方法而不是正则表达式处理简单任务"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")


def main():
    """主函数 - 演示所有字符串功能"""
    print("Python基础语法学习 - 字符串操作")
    print("=" * 50)
    
    demonstrate_string_creation()
    demonstrate_string_formatting()
    demonstrate_string_methods()
    demonstrate_string_slicing()
    demonstrate_string_encoding()
    demonstrate_regular_expressions()
    demonstrate_string_performance()
    
    print("\n学习总结:")
    print("1. Python字符串是不可变的Unicode序列")
    print("2. 支持多种创建和格式化方式")
    print("3. 丰富的内置方法用于处理文本")
    print("4. 强大的切片功能")
    print("5. 完整的Unicode支持")
    print("6. 正则表达式提供高级文本处理")
    print("7. 注意性能优化，特别是字符串连接")


if __name__ == "__main__":
    main() 