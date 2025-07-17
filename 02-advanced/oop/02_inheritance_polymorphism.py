#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python高级特性 - 继承和多态
=========================

本文件演示Python的继承和多态机制，并与Java进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

from abc import ABC, abstractmethod
from typing import List, Protocol, Union
import math


def demonstrate_basic_inheritance():
    """
    演示基本继承
    Python vs Java
    """
    print("=== 基本继承 ===\n")
    
    print("Java vs Python继承语法:")
    print("Java:")
    print("   class Animal { ... }")
    print("   class Dog extends Animal { ... }")
    print("   super.method(); // 调用父类方法")
    print()
    
    print("Python:")
    print("   class Animal: ...")
    print("   class Dog(Animal): ...")
    print("   super().method()  # 调用父类方法")
    print()
    
    # 1. 基本继承示例
    print("1. 基本继承示例")
    
    class Animal:
        """动物基类"""
        
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age
            self.species = "未知"
        
        def speak(self) -> str:
            """动物叫声 - 基类方法"""
            return f"{self.name}发出声音"
        
        def sleep(self):
            """睡觉 - 通用行为"""
            print(f"{self.name}正在睡觉")
        
        def get_info(self) -> str:
            """获取动物信息"""
            return f"{self.species}: {self.name}, {self.age}岁"
    
    class Dog(Animal):
        """狗类 - 继承自Animal"""
        
        def __init__(self, name: str, age: int, breed: str):
            # 调用父类构造函数
            super().__init__(name, age)
            self.species = "狗"
            self.breed = breed
        
        def speak(self) -> str:
            """重写父类方法"""
            return f"{self.name}汪汪叫"
        
        def fetch(self, item: str):
            """狗特有的行为"""
            print(f"{self.name}去捡{item}")
        
        def get_info(self) -> str:
            """扩展父类方法"""
            base_info = super().get_info()
            return f"{base_info}, 品种: {self.breed}"
    
    class Cat(Animal):
        """猫类 - 继承自Animal"""
        
        def __init__(self, name: str, age: int, indoor: bool = True):
            super().__init__(name, age)
            self.species = "猫"
            self.indoor = indoor
        
        def speak(self) -> str:
            """重写父类方法"""
            return f"{self.name}喵喵叫"
        
        def climb(self):
            """猫特有的行为"""
            print(f"{self.name}爬到高处")
        
        def get_info(self) -> str:
            location = "室内" if self.indoor else "室外"
            base_info = super().get_info()
            return f"{base_info}, 位置: {location}"
    
    # 创建实例
    dog = Dog("旺财", 3, "金毛")
    cat = Cat("咪咪", 2, True)
    
    print(f"   狗的信息: {dog.get_info()}")
    print(f"   狗的叫声: {dog.speak()}")
    dog.fetch("球")
    dog.sleep()
    print()
    
    print(f"   猫的信息: {cat.get_info()}")
    print(f"   猫的叫声: {cat.speak()}")
    cat.climb()
    cat.sleep()
    print()


def demonstrate_method_resolution_order():
    """
    演示方法解析顺序(MRO)
    Python的多重继承
    """
    print("=== 方法解析顺序(MRO) ===\n")
    
    print("Java vs Python多重继承:")
    print("Java:")
    print("   只支持单继承")
    print("   通过接口实现多重继承效果")
    print()
    
    print("Python:")
    print("   支持多重继承")
    print("   使用C3线性化算法确定MRO")
    print("   可通过Class.__mro__查看继承链")
    print()
    
    # 1. 多重继承示例
    print("1. 多重继承示例")
    
    class Flyable:
        """可飞行的混入类"""
        
        def fly(self):
            print(f"   {self.__class__.__name__}在飞行")
        
        def get_abilities(self):
            abilities = getattr(super(), 'get_abilities', lambda: [])()
            return abilities + ["飞行"]
    
    class Swimmable:
        """可游泳的混入类"""
        
        def swim(self):
            print(f"   {self.__class__.__name__}在游泳")
        
        def get_abilities(self):
            abilities = getattr(super(), 'get_abilities', lambda: [])()
            return abilities + ["游泳"]
    
    class Animal:
        """动物基类"""
        
        def __init__(self, name: str):
            self.name = name
        
        def get_abilities(self):
            return ["基本生存"]
    
    class Bird(Animal, Flyable):
        """鸟类 - 继承自Animal和Flyable"""
        
        def __init__(self, name: str, wingspan: float):
            super().__init__(name)
            self.wingspan = wingspan
    
    class Duck(Bird, Swimmable):
        """鸭子 - 多重继承"""
        
        def __init__(self, name: str, wingspan: float):
            super().__init__(name, wingspan)
        
        def quack(self):
            print(f"   {self.name}嘎嘎叫")
    
    class Fish(Animal, Swimmable):
        """鱼类"""
        
        def __init__(self, name: str, depth: int):
            super().__init__(name)
            self.depth = depth
    
    # 创建实例并测试
    duck = Duck("唐老鸭", 0.8)
    bird = Bird("小鸟", 0.3)
    fish = Fish("小鱼", 10)
    
    print(f"   鸭子能力: {duck.get_abilities()}")
    duck.fly()
    duck.swim()
    duck.quack()
    print()
    
    print(f"   鸟类能力: {bird.get_abilities()}")
    bird.fly()
    print()
    
    print(f"   鱼类能力: {fish.get_abilities()}")
    fish.swim()
    print()
    
    # 2. 查看MRO
    print("2. 方法解析顺序(MRO)")
    
    print(f"   Duck的MRO:")
    for i, cls in enumerate(Duck.__mro__):
        print(f"     {i+1}. {cls.__name__}")
    print()
    
    print(f"   Bird的MRO:")
    for i, cls in enumerate(Bird.__mro__):
        print(f"     {i+1}. {cls.__name__}")
    print()


def demonstrate_abstract_classes():
    """
    演示抽象类
    Python的ABC模块
    """
    print("=== 抽象类 ===\n")
    
    print("Java vs Python抽象类:")
    print("Java:")
    print("   abstract class Shape {")
    print("       abstract double getArea();")
    print("   }")
    print()
    
    print("Python:")
    print("   from abc import ABC, abstractmethod")
    print("   class Shape(ABC):")
    print("       @abstractmethod")
    print("       def get_area(self): pass")
    print()
    
    # 1. 抽象基类示例
    print("1. 抽象基类示例")
    
    class Shape(ABC):
        """形状抽象基类"""
        
        def __init__(self, name: str):
            self.name = name
        
        @abstractmethod
        def get_area(self) -> float:
            """计算面积 - 抽象方法"""
            pass
        
        @abstractmethod
        def get_perimeter(self) -> float:
            """计算周长 - 抽象方法"""
            pass
        
        def describe(self) -> str:
            """描述形状 - 具体方法"""
            return f"{self.name}: 面积={self.get_area():.2f}, 周长={self.get_perimeter():.2f}"
    
    class Rectangle(Shape):
        """矩形类 - 实现抽象类"""
        
        def __init__(self, width: float, height: float):
            super().__init__("矩形")
            self.width = width
            self.height = height
        
        def get_area(self) -> float:
            """实现抽象方法"""
            return self.width * self.height
        
        def get_perimeter(self) -> float:
            """实现抽象方法"""
            return 2 * (self.width + self.height)
    
    class Circle(Shape):
        """圆形类 - 实现抽象类"""
        
        def __init__(self, radius: float):
            super().__init__("圆形")
            self.radius = radius
        
        def get_area(self) -> float:
            """实现抽象方法"""
            return math.pi * self.radius ** 2
        
        def get_perimeter(self) -> float:
            """实现抽象方法"""
            return 2 * math.pi * self.radius
    
    # 创建具体实例
    rectangle = Rectangle(5, 3)
    circle = Circle(4)
    
    print(f"   {rectangle.describe()}")
    print(f"   {circle.describe()}")
    
    # 尝试实例化抽象类会出错
    try:
        shape = Shape("测试")
    except TypeError as e:
        print(f"   无法实例化抽象类: {e}")
    print()
    
    # 2. 抽象属性
    print("2. 抽象属性示例")
    
    class Vehicle(ABC):
        """交通工具抽象类"""
        
        @property
        @abstractmethod
        def max_speed(self) -> int:
            """最大速度 - 抽象属性"""
            pass
        
        @abstractmethod
        def start_engine(self):
            """启动引擎 - 抽象方法"""
            pass
        
        def get_info(self):
            """获取信息 - 具体方法"""
            return f"最大速度: {self.max_speed} km/h"
    
    class Car(Vehicle):
        """汽车类"""
        
        def __init__(self, brand: str, max_speed: int):
            self.brand = brand
            self._max_speed = max_speed
        
        @property
        def max_speed(self) -> int:
            """实现抽象属性"""
            return self._max_speed
        
        def start_engine(self):
            """实现抽象方法"""
            print(f"   {self.brand}汽车启动引擎")
    
    car = Car("BMW", 250)
    print(f"   汽车信息: {car.get_info()}")
    car.start_engine()
    print()


def demonstrate_polymorphism():
    """
    演示多态
    鸭子类型和协议
    """
    print("=== 多态 ===\n")
    
    print("Java vs Python多态:")
    print("Java:")
    print("   通过继承和接口实现多态")
    print("   编译时类型检查")
    print("   需要显式声明实现接口")
    print()
    
    print("Python:")
    print("   鸭子类型 - 'If it walks like a duck...'")
    print("   运行时类型检查")
    print("   Protocol提供结构化类型")
    print()
    
    # 1. 传统多态示例
    print("1. 传统多态示例")
    
    class Animal:
        """动物基类"""
        
        def make_sound(self) -> str:
            return "动物叫声"
        
        def move(self) -> str:
            return "动物移动"
    
    class Dog(Animal):
        def make_sound(self) -> str:
            return "汪汪"
        
        def move(self) -> str:
            return "跑步"
    
    class Cat(Animal):
        def make_sound(self) -> str:
            return "喵喵"
        
        def move(self) -> str:
            return "轻步走"
    
    class Bird(Animal):
        def make_sound(self) -> str:
            return "啾啾"
        
        def move(self) -> str:
            return "飞行"
    
    def animal_behavior(animal: Animal):
        """多态函数 - 接受Animal类型"""
        print(f"   声音: {animal.make_sound()}")
        print(f"   移动: {animal.move()}")
    
    animals = [Dog(), Cat(), Bird()]
    
    for i, animal in enumerate(animals, 1):
        print(f"   动物{i}:")
        animal_behavior(animal)
        print()
    
    # 2. 鸭子类型示例
    print("2. 鸭子类型示例")
    
    class Duck:
        """鸭子类 - 不继承Animal"""
        
        def make_sound(self) -> str:
            return "嘎嘎"
        
        def move(self) -> str:
            return "游泳"
    
    class Robot:
        """机器人类 - 完全不相关的类"""
        
        def make_sound(self) -> str:
            return "哔哔"
        
        def move(self) -> str:
            return "机械行走"
    
    # 鸭子类型：只要有相同的方法，就可以被当作同一类型使用
    duck_like_objects = [Duck(), Robot()]
    
    print("   鸭子类型演示:")
    for obj in duck_like_objects:
        animal_behavior(obj)  # 即使不是Animal子类也能工作
        print()
    
    # 3. Protocol协议示例
    print("3. Protocol协议示例")
    
    class Drawable(Protocol):
        """可绘制协议"""
        
        def draw(self) -> str:
            """绘制方法"""
            ...
        
        def get_area(self) -> float:
            """获取面积方法"""
            ...
    
    class Circle:
        """圆形 - 实现Drawable协议（结构化子类型）"""
        
        def __init__(self, radius: float):
            self.radius = radius
        
        def draw(self) -> str:
            return f"绘制半径为{self.radius}的圆"
        
        def get_area(self) -> float:
            return math.pi * self.radius ** 2
    
    class Square:
        """正方形 - 实现Drawable协议"""
        
        def __init__(self, side: float):
            self.side = side
        
        def draw(self) -> str:
            return f"绘制边长为{self.side}的正方形"
        
        def get_area(self) -> float:
            return self.side ** 2
    
    def render_shape(shape: Drawable):
        """渲染形状 - 使用协议类型"""
        print(f"   {shape.draw()}")
        print(f"   面积: {shape.get_area():.2f}")
    
    shapes = [Circle(5), Square(4)]
    
    print("   Protocol协议演示:")
    for shape in shapes:
        render_shape(shape)
        print()


def demonstrate_method_overriding():
    """
    演示方法重写
    super()的使用
    """
    print("=== 方法重写 ===\n")
    
    print("Java vs Python方法重写:")
    print("Java:")
    print("   @Override注解")
    print("   super.method()调用父类方法")
    print()
    
    print("Python:")
    print("   直接重新定义方法")
    print("   super().method()调用父类方法")
    print()
    
    # 1. 方法重写示例
    print("1. 方法重写示例")
    
    class Employee:
        """员工基类"""
        
        def __init__(self, name: str, base_salary: float):
            self.name = name
            self.base_salary = base_salary
        
        def calculate_salary(self) -> float:
            """计算薪资 - 基类实现"""
            return self.base_salary
        
        def get_description(self) -> str:
            """获取描述"""
            return f"员工: {self.name}"
        
        def work(self):
            """工作方法"""
            print(f"   {self.name}在工作")
    
    class Manager(Employee):
        """管理者 - 重写方法"""
        
        def __init__(self, name: str, base_salary: float, bonus_rate: float):
            super().__init__(name, base_salary)
            self.bonus_rate = bonus_rate
        
        def calculate_salary(self) -> float:
            """重写薪资计算"""
            base = super().calculate_salary()  # 调用父类方法
            return base * (1 + self.bonus_rate)
        
        def get_description(self) -> str:
            """重写描述方法"""
            base_desc = super().get_description()
            return f"{base_desc} (管理者)"
        
        def manage_team(self):
            """管理者特有方法"""
            print(f"   {self.name}在管理团队")
        
        def work(self):
            """重写工作方法"""
            super().work()  # 调用父类工作方法
            self.manage_team()  # 添加管理工作
    
    class Developer(Employee):
        """开发者 - 重写方法"""
        
        def __init__(self, name: str, base_salary: float, skill_bonus: float):
            super().__init__(name, base_salary)
            self.skill_bonus = skill_bonus
        
        def calculate_salary(self) -> float:
            """重写薪资计算"""
            base = super().calculate_salary()
            return base + self.skill_bonus
        
        def get_description(self) -> str:
            """重写描述方法"""
            base_desc = super().get_description()
            return f"{base_desc} (开发者)"
        
        def code(self):
            """开发者特有方法"""
            print(f"   {self.name}在编写代码")
        
        def work(self):
            """重写工作方法"""
            super().work()
            self.code()
    
    # 创建实例并测试
    employees = [
        Employee("张三", 5000),
        Manager("李四", 8000, 0.3),
        Developer("王五", 7000, 2000)
    ]
    
    print("   员工信息和工作方式:")
    for emp in employees:
        print(f"   {emp.get_description()}")
        print(f"   薪资: {emp.calculate_salary():.2f}")
        emp.work()
        print()


def demonstrate_composition_vs_inheritance():
    """
    演示组合 vs 继承
    """
    print("=== 组合 vs 继承 ===\n")
    
    print("设计原则:")
    print("   继承: 'is-a' 关系")
    print("   组合: 'has-a' 关系")
    print("   优先使用组合而非继承")
    print()
    
    # 1. 继承方式 (有问题的设计)
    print("1. 继承方式 (问题示例)")
    
    class FlyingCar_Inheritance:
        """飞行汽车 - 继承方式 (有问题)"""
        # 这种设计有问题：飞行汽车既要继承Car又要继承Plane
        # 在单继承语言中无法实现，即使多继承也会很复杂
        pass
    
    print("   问题: 飞行汽车既是汽车又是飞机，继承关系复杂")
    print()
    
    # 2. 组合方式 (推荐)
    print("2. 组合方式 (推荐)")
    
    class Engine:
        """引擎组件"""
        
        def __init__(self, power: int, fuel_type: str):
            self.power = power
            self.fuel_type = fuel_type
        
        def start(self):
            print(f"   启动{self.power}马力{self.fuel_type}引擎")
        
        def stop(self):
            print(f"   停止引擎")
    
    class Wings:
        """机翼组件"""
        
        def __init__(self, wingspan: float):
            self.wingspan = wingspan
        
        def extend(self):
            print(f"   展开{self.wingspan}米机翼")
        
        def retract(self):
            print(f"   收起机翼")
    
    class Wheels:
        """轮子组件"""
        
        def __init__(self, count: int):
            self.count = count
        
        def deploy(self):
            print(f"   放下{self.count}个轮子")
        
        def retract(self):
            print(f"   收起轮子")
    
    class FlyingCar_Composition:
        """飞行汽车 - 组合方式"""
        
        def __init__(self):
            # 组合不同的组件
            self.engine = Engine(300, "混合动力")
            self.wings = Wings(8.0)
            self.wheels = Wheels(4)
            self.mode = "ground"  # ground 或 air
        
        def switch_to_flight_mode(self):
            """切换到飞行模式"""
            if self.mode == "ground":
                print("   切换到飞行模式:")
                self.wheels.retract()
                self.wings.extend()
                self.mode = "air"
                print("   现在可以飞行了!")
        
        def switch_to_ground_mode(self):
            """切换到地面模式"""
            if self.mode == "air":
                print("   切换到地面模式:")
                self.wings.retract()
                self.wheels.deploy()
                self.mode = "ground"
                print("   现在可以在地面行驶了!")
        
        def start(self):
            """启动"""
            self.engine.start()
            print(f"   飞行汽车启动 (当前模式: {self.mode})")
        
        def stop(self):
            """停止"""
            self.engine.stop()
            print("   飞行汽车停止")
    
    # 测试组合方式
    flying_car = FlyingCar_Composition()
    
    flying_car.start()
    flying_car.switch_to_flight_mode()
    flying_car.switch_to_ground_mode()
    flying_car.stop()
    print()
    
    print("   组合的优势:")
    print("   - 更灵活，可以动态改变行为")
    print("   - 避免复杂的继承层次")
    print("   - 更容易测试和维护")
    print("   - 符合'开闭原则'")


def main():
    """主函数 - 演示所有继承和多态特性"""
    print("Python高级特性学习 - 继承和多态")
    print("=" * 50)
    
    demonstrate_basic_inheritance()
    demonstrate_method_resolution_order()
    demonstrate_abstract_classes()
    demonstrate_polymorphism()
    demonstrate_method_overriding()
    demonstrate_composition_vs_inheritance()
    
    print("学习总结:")
    print("1. Python支持单继承和多重继承")
    print("2. MRO确保方法解析的一致性")
    print("3. ABC模块提供抽象类功能")
    print("4. 鸭子类型实现灵活的多态")
    print("5. Protocol提供结构化子类型")
    print("6. super()用于调用父类方法")
    print("7. 组合通常比继承更灵活")


if __name__ == "__main__":
    main() 