#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python学习第一课：Hello Python
=========================

这是你的第一个Python程序，我们将对比Java和Python的基本语法差异。

作者：Python学习项目
日期：2024年1月
"""

# ========================================
# 1. Python vs Java 基本语法对比
# ========================================

# Python - 简洁的打印语句
print("Hello, Python!")
print("欢迎开始Python学习之旅!")

"""
Java对比：
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
        System.out.println("欢迎使用Java!");
    }
}

关键差异：
1. Python不需要类和main方法
2. Python不需要分号结尾
3. Python使用缩进而不是大括号
4. Python的print函数更简洁
"""

# ========================================
# 2. 变量声明和类型
# ========================================

# Python - 动态类型，无需声明
name = "张三"           # 字符串 (相当于Java的String)
age = 25               # 整数 (相当于Java的int)
height = 175.5         # 浮点数 (相当于Java的double)
is_student = True      # 布尔值 (相当于Java的boolean)
score = None           # 空值 (相当于Java的null)

print(f"姓名: {name}")
print(f"年龄: {age}")
print(f"身高: {height}cm")
print(f"是否为学生: {is_student}")
print(f"分数: {score}")

"""
Java对比：
String name = "张三";
int age = 25;
double height = 175.5;
boolean isStudent = true;
Integer score = null;

System.out.println("姓名: " + name);
System.out.println("年龄: " + age);
System.out.println("身高: " + height + "cm");
System.out.println("是否为学生: " + isStudent);
System.out.println("分数: " + score);

关键差异：
1. Python变量无需类型声明
2. Python使用snake_case命名(is_student)，Java使用camelCase(isStudent)
3. Python的f-string格式化更简洁
4. Python使用None，Java使用null
"""

# ========================================
# 3. 类型检查和转换
# ========================================

print("\n=== 类型信息 ===")

# Python内置函数检查类型
print(f"name的类型: {type(name)}")
print(f"age的类型: {type(age)}")
print(f"height的类型: {type(height)}")
print(f"is_student的类型: {type(is_student)}")

# 类型转换
age_str = str(age)              # 转换为字符串
height_int = int(height)        # 转换为整数
age_float = float(age)          # 转换为浮点数

print(f"age转字符串: '{age_str}' (类型: {type(age_str)})")
print(f"height转整数: {height_int} (类型: {type(height_int)})")
print(f"age转浮点数: {age_float} (类型: {type(age_float)})")

"""
Java对比：
System.out.println("name的类型: " + name.getClass().getSimpleName());
System.out.println("age的类型: " + Integer.class.getSimpleName());

String ageStr = String.valueOf(age);
int heightInt = (int) height;
double ageFloat = (double) age;

关键差异：
1. Python的type()函数更直观
2. Python的类型转换使用构造函数风格
3. Java需要显式类型转换或方法调用
"""

# ========================================
# 4. Python特有的类型提示 (可选)
# ========================================

from typing import Optional

# Python 3.5+ 支持类型提示（可选，运行时不检查）
def greet_user(user_name: str, user_age: int, score: Optional[float] = None) -> str:
    """
    问候用户的函数
    
    Args:
        user_name: 用户姓名
        user_age: 用户年龄
        score: 可选的分数
    
    Returns:
        问候消息
    """
    if score is not None:
        return f"你好 {user_name}，{user_age}岁，分数：{score}"
    else:
        return f"你好 {user_name}，{user_age}岁"

# 调用函数
message1 = greet_user("李四", 30, 95.5)
message2 = greet_user("王五", 28)

print(f"\n=== 函数调用结果 ===")
print(message1)
print(message2)

"""
Java对比：
public static String greetUser(String userName, int userAge, Double score) {
    if (score != null) {
        return String.format("你好 %s，%d岁，分数：%.1f", userName, userAge, score);
    } else {
        return String.format("你好 %s，%d岁", userName, userAge);
    }
}

关键差异：
1. Python的类型提示是可选的，主要用于IDE和代码分析
2. Python的Optional[T]相当于Java的可空类型
3. Python的docstring提供了更好的文档化
4. Python的默认参数更灵活
"""

# ========================================
# 5. 常量定义（Python约定）
# ========================================

# Python使用全大写命名约定表示常量
PI = 3.14159
MAX_STUDENTS = 100
DEFAULT_TIMEOUT = 30
APP_NAME = "Python学习系统"

print(f"\n=== 常量使用 ===")
print(f"圆周率: {PI}")
print(f"最大学生数: {MAX_STUDENTS}")
print(f"默认超时: {DEFAULT_TIMEOUT}秒")
print(f"应用名称: {APP_NAME}")

"""
Java对比：
public static final double PI = 3.14159;
public static final int MAX_STUDENTS = 100;
public static final int DEFAULT_TIMEOUT = 30;
public static final String APP_NAME = "Java学习系统";

关键差异：
1. Python没有final关键字，使用约定（全大写）
2. Java有编译时常量检查，Python是运行时约定
3. Python的常量实际上是可变的（只是约定不修改）
"""

# ========================================
# 6. 实践练习
# ========================================

print("\n=== 实践练习 ===")

# 练习1：创建个人信息
print("练习1：创建你的个人信息")
my_name = "Python学习者"  # 修改为你的姓名
my_age = 25             # 修改为你的年龄  
my_city = "北京"         # 修改为你的城市
my_hobby = "编程"        # 修改为你的爱好

print(f"我叫{my_name}，今年{my_age}岁，来自{my_city}，喜欢{my_hobby}")

# 练习2：计算年龄相关信息
birth_year = 2024 - my_age
retirement_age = 65
years_to_retirement = retirement_age - my_age

print(f"出生年份: {birth_year}")
print(f"距离退休还有: {years_to_retirement}年")

# 练习3：字符串操作
full_intro = f"大家好，我是{my_name}，{my_age}岁，来自{my_city}。我的爱好是{my_hobby}。"
intro_length = len(full_intro)
intro_upper = full_intro.upper()

print(f"自我介绍: {full_intro}")
print(f"介绍长度: {intro_length}个字符")
print(f"大写版本: {intro_upper}")

"""
练习思考题：
1. 为什么Python不需要显式声明变量类型？
2. Python的f-string相比Java的String.format有什么优势？
3. 如何在Python中实现类似Java final关键字的效果？
4. Python的缩进规则和Java的大括号规则有什么优缺点？

下一步学习：
- 学习Python的集合类型（列表、字典、元组、集合）
- 了解Python的控制流结构（if/elif/else, for/while）
- 掌握Python的函数定义和调用
"""

if __name__ == "__main__":
    print("\n=== 程序执行完成 ===")
    print("恭喜！你已经完成了第一个Python程序的学习。")
    print("接下来可以继续学习其他模块的内容。")
    
    # 类似Java的主方法检查
    print("\n这个if __name__ == '__main__':")
    print("相当于Java的public static void main(String[] args)")
    print("只有直接运行这个文件时才会执行这部分代码") 