#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python高级特性 - 类和对象
=======================

本文件演示Python的面向对象编程，并与Java进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

from typing import List, Optional, ClassVar
from abc import ABC, abstractmethod
import weakref


def demonstrate_class_definition():
    """
    演示类定义的基础语法
    Python vs Java
    """
    print("=== 类定义基础 ===\n")
    
    print("Java vs Python类定义:")
    print("Java:")
    print("   public class Person {")
    print("       private String name;")
    print("       private int age;")
    print("       ")
    print("       public Person(String name, int age) {")
    print("           this.name = name;")
    print("           this.age = age;")
    print("       }")
    print("   }")
    print()
    
    print("Python:")
    print("   class Person:")
    print("       def __init__(self, name, age):")
    print("           self.name = name")
    print("           self.age = age")
    print()
    
    # 1. 基本类定义
    print("1. 基本类定义示例")
    
    class Person:
        """人员类 - 基本示例"""
        
        def __init__(self, name: str, age: int):
            """构造函数 (类似Java构造器)"""
            self.name = name
            self.age = age
        
        def introduce(self) -> str:
            """自我介绍方法"""
            return f"我是{self.name}，今年{self.age}岁"
        
        def celebrate_birthday(self):
            """过生日 - 修改对象状态"""
            self.age += 1
            print(f"{self.name}过生日了！现在{self.age}岁")
    
    # 创建对象
    person1 = Person("张三", 25)
    person2 = Person("李四", 30)
    
    print(f"   创建对象: {person1.name}, {person1.age}岁")
    print(f"   自我介绍: {person1.introduce()}")
    print()
    
    person1.celebrate_birthday()
    print(f"   生日后: {person1.introduce()}")
    print()
    
    # 2. 类属性 vs 实例属性
    print("2. 类属性 vs 实例属性")
    
    class Student:
        # 类属性 (类似Java static字段)
        school_name = "Python大学"
        student_count = 0
        
        def __init__(self, name: str, student_id: str):
            # 实例属性
            self.name = name
            self.student_id = student_id
            # 修改类属性
            Student.student_count += 1
        
        @classmethod
        def get_student_count(cls):
            """类方法 (类似Java static方法)"""
            return cls.student_count
        
        @staticmethod
        def is_valid_student_id(student_id: str) -> bool:
            """静态方法"""
            return len(student_id) == 8 and student_id.isdigit()
    
    print(f"   学校名称: {Student.school_name}")
    print(f"   初始学生数: {Student.get_student_count()}")
    
    student1 = Student("王五", "20240001")
    student2 = Student("赵六", "20240002")
    
    print(f"   创建学生后数量: {Student.get_student_count()}")
    print(f"   学号验证: {Student.is_valid_student_id('12345678')}")
    print(f"   无效学号: {Student.is_valid_student_id('abc')}")
    print()


def demonstrate_encapsulation():
    """
    演示封装
    Python的访问控制
    """
    print("=== 封装和访问控制 ===\n")
    
    print("Java vs Python访问控制:")
    print("Java:")
    print("   private   - 私有")
    print("   protected - 受保护")
    print("   public    - 公有")
    print("   package   - 包级别")
    print()
    
    print("Python:")
    print("   public     - 普通属性 (默认)")
    print("   _protected - 单下划线 (约定受保护)")
    print("   __private  - 双下划线 (名称改编)")
    print()
    
    # 1. Python的访问控制
    print("1. Python访问控制示例")
    
    class BankAccount:
        """银行账户类 - 展示封装"""
        
        def __init__(self, account_number: str, initial_balance: float = 0.0):
            self.account_number = account_number      # 公有属性
            self._balance = initial_balance           # 受保护属性 (约定)
            self.__pin = "1234"                      # 私有属性 (名称改编)
            self._transaction_history = []           # 受保护属性
        
        def get_balance(self) -> float:
            """获取余额 - 公有方法"""
            return self._balance
        
        def deposit(self, amount: float):
            """存款"""
            if amount > 0:
                self._balance += amount
                self._record_transaction(f"存款 {amount}")
                print(f"存款成功，余额: {self._balance}")
            else:
                raise ValueError("存款金额必须大于0")
        
        def withdraw(self, amount: float, pin: str):
            """取款"""
            if not self.__verify_pin(pin):
                raise ValueError("PIN码错误")
            
            if amount > self._balance:
                raise ValueError("余额不足")
            
            self._balance -= amount
            self._record_transaction(f"取款 {amount}")
            print(f"取款成功，余额: {self._balance}")
        
        def _record_transaction(self, description: str):
            """记录交易 - 受保护方法"""
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._transaction_history.append(f"{timestamp}: {description}")
        
        def __verify_pin(self, pin: str) -> bool:
            """验证PIN - 私有方法"""
            return pin == self.__pin
        
        def change_pin(self, old_pin: str, new_pin: str):
            """修改PIN码"""
            if self.__verify_pin(old_pin):
                self.__pin = new_pin
                print("PIN码修改成功")
            else:
                raise ValueError("原PIN码错误")
    
    account = BankAccount("123456789", 1000.0)
    
    print(f"   账户号: {account.account_number}")
    print(f"   余额: {account.get_balance()}")
    
    # 正常操作
    account.deposit(500.0)
    account.withdraw(200.0, "1234")
    
    # 访问控制演示
    print("\n   访问控制演示:")
    print(f"   公有属性: {account.account_number}")
    print(f"   受保护属性: {account._balance}")  # 可以访问但不推荐
    
    # 私有属性访问
    try:
        print(f"   私有属性: {account.__pin}")  # 会出错
    except AttributeError:
        print("   无法直接访问私有属性 __pin")
    
    # 名称改编后的访问 (不推荐)
    print(f"   名称改编后: {account._BankAccount__pin}")
    print()


def demonstrate_properties():
    """
    演示属性(Property)
    Python的getter/setter
    """
    print("=== 属性(Property) ===\n")
    
    print("Java vs Python属性访问:")
    print("Java:")
    print("   private int age;")
    print("   public int getAge() { return age; }")
    print("   public void setAge(int age) { this.age = age; }")
    print()
    
    print("Python:")
    print("   @property")
    print("   def age(self): return self._age")
    print("   @age.setter")
    print("   def age(self, value): self._age = value")
    print()
    
    # 1. 基本Property使用
    print("1. 基本Property示例")
    
    class Temperature:
        """温度类 - 展示Property"""
        
        def __init__(self, celsius: float = 0.0):
            self._celsius = celsius
        
        @property
        def celsius(self) -> float:
            """摄氏度getter"""
            return self._celsius
        
        @celsius.setter
        def celsius(self, value: float):
            """摄氏度setter"""
            if value < -273.15:
                raise ValueError("温度不能低于绝对零度")
            self._celsius = value
        
        @property
        def fahrenheit(self) -> float:
            """华氏度 (只读属性)"""
            return self._celsius * 9/5 + 32
        
        @property
        def kelvin(self) -> float:
            """开尔文 (只读属性)"""
            return self._celsius + 273.15
        
        def __str__(self) -> str:
            return f"{self._celsius}°C ({self.fahrenheit}°F, {self.kelvin}K)"
    
    temp = Temperature(25)
    print(f"   初始温度: {temp}")
    
    # 使用property
    temp.celsius = 100
    print(f"   设置为100°C: {temp}")
    
    print(f"   华氏度: {temp.fahrenheit}°F")
    print(f"   开尔文: {temp.kelvin}K")
    
    # 验证setter的验证逻辑
    try:
        temp.celsius = -300
    except ValueError as e:
        print(f"   温度验证: {e}")
    print()
    
    # 2. 复杂Property示例
    print("2. 复杂Property示例")
    
    class Rectangle:
        """矩形类 - 复杂属性计算"""
        
        def __init__(self, width: float, height: float):
            self._width = width
            self._height = height
        
        @property
        def width(self) -> float:
            return self._width
        
        @width.setter
        def width(self, value: float):
            if value <= 0:
                raise ValueError("宽度必须大于0")
            self._width = value
        
        @property
        def height(self) -> float:
            return self._height
        
        @height.setter
        def height(self, value: float):
            if value <= 0:
                raise ValueError("高度必须大于0")
            self._height = value
        
        @property
        def area(self) -> float:
            """面积 (计算属性)"""
            return self._width * self._height
        
        @property
        def perimeter(self) -> float:
            """周长 (计算属性)"""
            return 2 * (self._width + self._height)
        
        @property
        def diagonal(self) -> float:
            """对角线长度"""
            return (self._width ** 2 + self._height ** 2) ** 0.5
    
    rect = Rectangle(10, 5)
    print(f"   矩形: {rect.width} × {rect.height}")
    print(f"   面积: {rect.area}")
    print(f"   周长: {rect.perimeter}")
    print(f"   对角线: {rect.diagonal:.2f}")
    
    # 修改尺寸
    rect.width = 15
    print(f"   修改宽度后面积: {rect.area}")
    print()


def demonstrate_special_methods():
    """
    演示特殊方法(Magic Methods)
    Python的运算符重载
    """
    print("=== 特殊方法(Magic Methods) ===\n")
    
    print("Java vs Python运算符重载:")
    print("Java:")
    print("   需要实现Comparable接口")
    print("   重写equals()和hashCode()")
    print("   无法重载+、-等运算符")
    print()
    
    print("Python:")
    print("   __str__、__repr__ - 字符串表示")
    print("   __eq__、__lt__ - 比较运算")
    print("   __add__、__sub__ - 算术运算")
    print("   __len__、__getitem__ - 容器操作")
    print()
    
    # 1. 基本特殊方法
    print("1. 基本特殊方法示例")
    
    class Point:
        """点类 - 展示特殊方法"""
        
        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y
        
        def __str__(self) -> str:
            """用户友好的字符串表示"""
            return f"Point({self.x}, {self.y})"
        
        def __repr__(self) -> str:
            """开发者友好的字符串表示"""
            return f"Point({self.x!r}, {self.y!r})"
        
        def __eq__(self, other) -> bool:
            """相等比较"""
            if not isinstance(other, Point):
                return False
            return self.x == other.x and self.y == other.y
        
        def __lt__(self, other) -> bool:
            """小于比较 (按距离原点)"""
            if not isinstance(other, Point):
                return NotImplemented
            return self.distance_from_origin() < other.distance_from_origin()
        
        def __add__(self, other):
            """向量加法"""
            if isinstance(other, Point):
                return Point(self.x + other.x, self.y + other.y)
            return NotImplemented
        
        def __sub__(self, other):
            """向量减法"""
            if isinstance(other, Point):
                return Point(self.x - other.x, self.y - other.y)
            return NotImplemented
        
        def __mul__(self, scalar):
            """标量乘法"""
            if isinstance(scalar, (int, float)):
                return Point(self.x * scalar, self.y * scalar)
            return NotImplemented
        
        def __hash__(self):
            """哈希值 (使对象可以用作字典键)"""
            return hash((self.x, self.y))
        
        def distance_from_origin(self) -> float:
            """距离原点的距离"""
            return (self.x ** 2 + self.y ** 2) ** 0.5
    
    p1 = Point(3, 4)
    p2 = Point(1, 2)
    p3 = Point(3, 4)
    
    print(f"   点p1: {p1}")
    print(f"   点p2: {p2}")
    print(f"   repr(p1): {repr(p1)}")
    
    # 比较操作
    print(f"   p1 == p3: {p1 == p3}")
    print(f"   p1 == p2: {p1 == p2}")
    print(f"   p1 < p2: {p1 < p2}")
    
    # 算术操作
    p4 = p1 + p2
    p5 = p1 - p2
    p6 = p1 * 2
    
    print(f"   p1 + p2: {p4}")
    print(f"   p1 - p2: {p5}")
    print(f"   p1 * 2: {p6}")
    
    # 哈希和集合操作
    points = {p1, p2, p3}  # 使用set
    print(f"   点的集合: {points}")
    print()
    
    # 2. 容器特殊方法
    print("2. 容器特殊方法示例")
    
    class Playlist:
        """播放列表 - 容器类"""
        
        def __init__(self, name: str):
            self.name = name
            self._songs = []
        
        def add_song(self, song: str):
            """添加歌曲"""
            self._songs.append(song)
        
        def __len__(self) -> int:
            """返回歌曲数量"""
            return len(self._songs)
        
        def __getitem__(self, index):
            """支持索引访问"""
            return self._songs[index]
        
        def __setitem__(self, index, value):
            """支持索引赋值"""
            self._songs[index] = value
        
        def __delitem__(self, index):
            """支持del操作"""
            del self._songs[index]
        
        def __iter__(self):
            """支持迭代"""
            return iter(self._songs)
        
        def __contains__(self, song) -> bool:
            """支持in操作"""
            return song in self._songs
        
        def __str__(self) -> str:
            return f"Playlist '{self.name}' with {len(self)} songs"
    
    playlist = Playlist("我的音乐")
    playlist.add_song("歌曲1")
    playlist.add_song("歌曲2")
    playlist.add_song("歌曲3")
    
    print(f"   播放列表: {playlist}")
    print(f"   歌曲数量: {len(playlist)}")
    print(f"   第一首歌: {playlist[0]}")
    print(f"   包含'歌曲2': {'歌曲2' in playlist}")
    
    # 迭代
    print("   所有歌曲:")
    for i, song in enumerate(playlist):
        print(f"     {i+1}. {song}")
    
    # 修改
    playlist[1] = "新歌曲2"
    print(f"   修改后第二首: {playlist[1]}")
    print()


def demonstrate_class_relationships():
    """
    演示类之间的关系
    组合、聚合等
    """
    print("=== 类之间的关系 ===\n")
    
    print("类关系类型:")
    print("   组合 (Composition) - 强关系，整体销毁时部分也销毁")
    print("   聚合 (Aggregation) - 弱关系，整体销毁时部分可独立存在")
    print("   关联 (Association) - 一般关系")
    print()
    
    # 1. 组合关系示例
    print("1. 组合关系示例")
    
    class Engine:
        """发动机类"""
        
        def __init__(self, power: int, fuel_type: str):
            self.power = power
            self.fuel_type = fuel_type
            self.is_running = False
        
        def start(self):
            self.is_running = True
            print(f"   发动机启动 ({self.power}马力, {self.fuel_type})")
        
        def stop(self):
            self.is_running = False
            print("   发动机停止")
    
    class Car:
        """汽车类 - 组合关系"""
        
        def __init__(self, brand: str, model: str, engine_power: int):
            self.brand = brand
            self.model = model
            # 组合关系：Car创建并拥有Engine
            self.engine = Engine(engine_power, "汽油")
            self.speed = 0
        
        def start(self):
            print(f"   启动 {self.brand} {self.model}")
            self.engine.start()
        
        def accelerate(self, delta_speed: int):
            if self.engine.is_running:
                self.speed += delta_speed
                print(f"   加速到 {self.speed} km/h")
            else:
                print("   请先启动发动机")
        
        def stop(self):
            self.speed = 0
            self.engine.stop()
            print(f"   {self.brand} {self.model} 停止")
    
    car = Car("Toyota", "Camry", 200)
    car.start()
    car.accelerate(50)
    car.stop()
    print()
    
    # 2. 聚合关系示例
    print("2. 聚合关系示例")
    
    class Student:
        """学生类"""
        
        def __init__(self, name: str, student_id: str):
            self.name = name
            self.student_id = student_id
        
        def __str__(self):
            return f"Student({self.name}, {self.student_id})"
    
    class Course:
        """课程类 - 聚合关系"""
        
        def __init__(self, name: str, code: str):
            self.name = name
            self.code = code
            self.students: List[Student] = []  # 聚合关系
        
        def enroll_student(self, student: Student):
            if student not in self.students:
                self.students.append(student)
                print(f"   {student.name} 选修了 {self.name}")
        
        def remove_student(self, student: Student):
            if student in self.students:
                self.students.remove(student)
                print(f"   {student.name} 退选了 {self.name}")
        
        def list_students(self):
            print(f"   {self.name} 的学生:")
            for student in self.students:
                print(f"     - {student.name}")
    
    # 创建学生（独立存在）
    student1 = Student("张三", "2024001")
    student2 = Student("李四", "2024002")
    
    # 创建课程
    python_course = Course("Python编程", "CS101")
    
    # 建立聚合关系
    python_course.enroll_student(student1)
    python_course.enroll_student(student2)
    python_course.list_students()
    
    # 学生可以独立存在
    python_course.remove_student(student1)
    print(f"   学生 {student1.name} 仍然存在")
    print()


def demonstrate_method_types():
    """
    演示不同类型的方法
    实例方法、类方法、静态方法
    """
    print("=== 方法类型 ===\n")
    
    print("Java vs Python方法类型:")
    print("Java:")
    print("   实例方法 - 普通方法")
    print("   static方法 - 静态方法")
    print("   (无类方法概念)")
    print()
    
    print("Python:")
    print("   实例方法 - def method(self)")
    print("   类方法 - @classmethod def method(cls)")
    print("   静态方法 - @staticmethod def method()")
    print()
    
    class MathUtils:
        """数学工具类 - 展示不同方法类型"""
        
        # 类属性
        pi = 3.14159
        calculation_count = 0
        
        def __init__(self, precision: int = 2):
            # 实例属性
            self.precision = precision
        
        def round_number(self, number: float) -> float:
            """实例方法 - 使用实例属性"""
            MathUtils.calculation_count += 1
            return round(number, self.precision)
        
        @classmethod
        def create_high_precision(cls):
            """类方法 - 替代构造器"""
            return cls(precision=6)
        
        @classmethod
        def get_calculation_count(cls):
            """类方法 - 访问类属性"""
            return cls.calculation_count
        
        @classmethod
        def reset_counter(cls):
            """类方法 - 修改类属性"""
            cls.calculation_count = 0
        
        @staticmethod
        def add(a: float, b: float) -> float:
            """静态方法 - 纯函数，不访问类或实例"""
            return a + b
        
        @staticmethod
        def is_prime(n: int) -> bool:
            """静态方法 - 工具函数"""
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        @staticmethod
        def factorial(n: int) -> int:
            """静态方法 - 递归计算"""
            if n <= 1:
                return 1
            return n * MathUtils.factorial(n - 1)
    
    # 使用实例方法
    math1 = MathUtils(2)
    math2 = MathUtils(4)
    
    print(f"   实例方法调用:")
    print(f"     math1.round_number(3.14159): {math1.round_number(3.14159)}")
    print(f"     math2.round_number(2.71828): {math2.round_number(2.71828)}")
    
    # 使用类方法
    print(f"\n   类方法调用:")
    high_precision = MathUtils.create_high_precision()
    print(f"     高精度实例: {high_precision.precision}")
    print(f"     计算次数: {MathUtils.get_calculation_count()}")
    
    # 使用静态方法
    print(f"\n   静态方法调用:")
    print(f"     MathUtils.add(5, 3): {MathUtils.add(5, 3)}")
    print(f"     MathUtils.is_prime(17): {MathUtils.is_prime(17)}")
    print(f"     MathUtils.factorial(5): {MathUtils.factorial(5)}")
    
    # 重置计数器
    MathUtils.reset_counter()
    print(f"     重置后计算次数: {MathUtils.get_calculation_count()}")
    print()


def main():
    """主函数 - 演示所有面向对象特性"""
    print("Python高级特性学习 - 类和对象")
    print("=" * 50)
    
    demonstrate_class_definition()
    demonstrate_encapsulation()
    demonstrate_properties()
    demonstrate_special_methods()
    demonstrate_class_relationships()
    demonstrate_method_types()
    
    print("学习总结:")
    print("1. Python类定义语法简洁，使用__init__作为构造函数")
    print("2. 访问控制通过命名约定实现，而非关键字")
    print("3. Property提供了优雅的getter/setter机制")
    print("4. 特殊方法让类支持Python内置操作")
    print("5. 类方法和静态方法提供不同的调用方式")
    print("6. 类关系通过组合和聚合实现")
    print("7. Python的OOP更加灵活和动态")


if __name__ == "__main__":
    main() 