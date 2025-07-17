#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python高级特性 - OOP与Java对比
=============================

本文件详细对比Python和Java的面向对象编程特性
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

from typing import List, Optional, Protocol, TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
import inspect


def demonstrate_class_definition_comparison():
    """
    演示类定义对比
    Python vs Java
    """
    print("=== 类定义对比 ===\n")
    
    print("语法对比:")
    print("Java:")
    print("   public class Person {")
    print("       private String name;")
    print("       private int age;")
    print("       ")
    print("       public Person(String name, int age) {")
    print("           this.name = name;")
    print("           this.age = age;")
    print("       }")
    print("       ")
    print("       public String getName() { return name; }")
    print("       public void setName(String name) { this.name = name; }")
    print("   }")
    print()
    
    print("Python (传统方式):")
    print("   class Person:")
    print("       def __init__(self, name, age):")
    print("           self._name = name")
    print("           self._age = age")
    print("       ")
    print("       @property")
    print("       def name(self): return self._name")
    print("       ")
    print("       @name.setter")
    print("       def name(self, value): self._name = value")
    print()
    
    print("Python (dataclass方式):")
    print("   @dataclass")
    print("   class Person:")
    print("       name: str")
    print("       age: int")
    print()
    
    # 1. 传统Python类
    print("1. 传统Python类定义")
    
    class Person:
        """传统Python类"""
        
        def __init__(self, name: str, age: int, email: Optional[str] = None):
            self._name = name
            self._age = age
            self._email = email
        
        @property
        def name(self) -> str:
            return self._name
        
        @name.setter
        def name(self, value: str):
            if not value.strip():
                raise ValueError("姓名不能为空")
            self._name = value
        
        @property
        def age(self) -> int:
            return self._age
        
        @age.setter
        def age(self, value: int):
            if value < 0:
                raise ValueError("年龄不能为负数")
            self._age = value
        
        def __str__(self) -> str:
            return f"Person(name='{self.name}', age={self.age})"
        
        def __repr__(self) -> str:
            return f"Person('{self.name}', {self.age}, '{self._email}')"
        
        def __eq__(self, other) -> bool:
            if not isinstance(other, Person):
                return False
            return self.name == other.name and self.age == other.age
    
    # 2. Dataclass方式
    print("2. Dataclass方式")
    
    @dataclass
    class PersonDC:
        """使用dataclass的Person类"""
        name: str
        age: int
        email: Optional[str] = None
        _private_data: str = field(default="", repr=False)
        
        def __post_init__(self):
            """初始化后处理"""
            if self.age < 0:
                raise ValueError("年龄不能为负数")
        
        def celebrate_birthday(self):
            """过生日"""
            self.age += 1
    
    # 创建实例对比
    person1 = Person("张三", 25, "zhang@example.com")
    person2 = PersonDC("李四", 30, "li@example.com")
    
    print(f"   传统类: {person1}")
    print(f"   Dataclass: {person2}")
    
    # 自动生成的方法
    person3 = PersonDC("李四", 30, "li@example.com")
    print(f"   相等比较: person2 == person3: {person2 == person3}")
    print()


def demonstrate_access_control_comparison():
    """
    演示访问控制对比
    """
    print("=== 访问控制对比 ===\n")
    
    print("Java访问修饰符:")
    print("   private   - 只有本类可访问")
    print("   protected - 本类和子类可访问")
    print("   package   - 包内可访问")
    print("   public    - 所有类可访问")
    print()
    
    print("Python访问约定:")
    print("   attribute  - 公有 (public)")
    print("   _attribute - 受保护 (protected by convention)")
    print("   __attribute - 私有 (name mangling)")
    print()
    
    class JavaStyleClass:
        """Java风格的访问控制演示"""
        
        def __init__(self):
            self.public_attr = "公有属性"          # 相当于Java public
            self._protected_attr = "受保护属性"     # 相当于Java protected
            self.__private_attr = "私有属性"       # 相当于Java private
        
        def public_method(self):
            """公有方法"""
            return "公有方法被调用"
        
        def _protected_method(self):
            """受保护方法 (约定)"""
            return "受保护方法被调用"
        
        def __private_method(self):
            """私有方法 (名称改编)"""
            return "私有方法被调用"
        
        def access_demo(self):
            """演示内部访问"""
            print(f"   内部访问公有属性: {self.public_attr}")
            print(f"   内部访问受保护属性: {self._protected_attr}")
            print(f"   内部访问私有属性: {self.__private_attr}")
            print(f"   内部调用私有方法: {self.__private_method()}")
    
    class SubClass(JavaStyleClass):
        """子类"""
        
        def access_parent(self):
            """子类访问父类属性"""
            print(f"   子类访问公有属性: {self.public_attr}")
            print(f"   子类访问受保护属性: {self._protected_attr}")
            # print(f"   子类访问私有属性: {self.__private_attr}")  # 这会出错
            
            try:
                print(f"   子类访问私有属性: {self.__private_attr}")
            except AttributeError:
                print("   子类无法访问父类私有属性")
    
    # 测试访问控制
    obj = JavaStyleClass()
    sub_obj = SubClass()
    
    print("内部访问:")
    obj.access_demo()
    print()
    
    print("外部访问:")
    print(f"   外部访问公有属性: {obj.public_attr}")
    print(f"   外部访问受保护属性: {obj._protected_attr}")  # 可以访问但不推荐
    
    # 私有属性的名称改编
    print(f"   私有属性的真实名称: {obj._JavaStyleClass__private_attr}")
    print()
    
    print("子类访问:")
    sub_obj.access_parent()
    print()


def demonstrate_interface_comparison():
    """
    演示接口对比
    Java接口 vs Python Protocol/ABC
    """
    print("=== 接口对比 ===\n")
    
    print("Java接口:")
    print("   interface Drawable {")
    print("       void draw();")
    print("       default void highlight() { ... }")
    print("   }")
    print("   class Circle implements Drawable { ... }")
    print()
    
    print("Python Protocol (结构化子类型):")
    print("   class Drawable(Protocol):")
    print("       def draw(self) -> None: ...")
    print()
    
    print("Python ABC (名义子类型):")
    print("   class Drawable(ABC):")
    print("       @abstractmethod")
    print("       def draw(self) -> None: pass")
    print()
    
    # 1. Protocol方式 (鸭子类型)
    print("1. Protocol方式 (鸭子类型)")
    
    class Drawable(Protocol):
        """可绘制协议"""
        
        def draw(self) -> str:
            """绘制方法"""
            ...
        
        def get_bounds(self) -> tuple:
            """获取边界"""
            ...
    
    class Circle:
        """圆形 - 结构化实现Drawable"""
        
        def __init__(self, radius: float):
            self.radius = radius
        
        def draw(self) -> str:
            return f"绘制半径为{self.radius}的圆"
        
        def get_bounds(self) -> tuple:
            return (-self.radius, -self.radius, self.radius, self.radius)
    
    class Rectangle:
        """矩形 - 结构化实现Drawable"""
        
        def __init__(self, width: float, height: float):
            self.width = width
            self.height = height
        
        def draw(self) -> str:
            return f"绘制{self.width}x{self.height}的矩形"
        
        def get_bounds(self) -> tuple:
            return (0, 0, self.width, self.height)
    
    def render_shape(shape: Drawable):
        """渲染形状 - 使用Protocol"""
        print(f"   {shape.draw()}")
        print(f"   边界: {shape.get_bounds()}")
    
    circle = Circle(5)
    rectangle = Rectangle(10, 6)
    
    print("   Protocol方式 (无需显式继承):")
    render_shape(circle)
    render_shape(rectangle)
    print()
    
    # 2. ABC方式 (显式继承)
    print("2. ABC方式 (显式继承)")
    
    class Shape(ABC):
        """形状抽象基类"""
        
        @abstractmethod
        def calculate_area(self) -> float:
            """计算面积"""
            pass
        
        @abstractmethod
        def calculate_perimeter(self) -> float:
            """计算周长"""
            pass
        
        def describe(self) -> str:
            """描述形状 - 具体方法"""
            return f"面积: {self.calculate_area():.2f}, 周长: {self.calculate_perimeter():.2f}"
    
    class TriangleABC(Shape):
        """三角形 - 继承ABC"""
        
        def __init__(self, a: float, b: float, c: float):
            self.a, self.b, self.c = a, b, c
        
        def calculate_area(self) -> float:
            """海伦公式计算面积"""
            s = (self.a + self.b + self.c) / 2
            return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5
        
        def calculate_perimeter(self) -> float:
            return self.a + self.b + self.c
    
    triangle = TriangleABC(3, 4, 5)
    print(f"   ABC方式: {triangle.describe()}")
    print()


def demonstrate_generics_comparison():
    """
    演示泛型对比
    Java泛型 vs Python类型变量
    """
    print("=== 泛型对比 ===\n")
    
    print("Java泛型:")
    print("   class Box<T> {")
    print("       private T value;")
    print("       public void set(T value) { this.value = value; }")
    print("       public T get() { return value; }")
    print("   }")
    print()
    
    print("Python类型变量:")
    print("   T = TypeVar('T')")
    print("   class Box(Generic[T]):")
    print("       def set(self, value: T) -> None: ...")
    print("       def get(self) -> T: ...")
    print()
    
    # Python泛型示例
    T = TypeVar('T')
    
    class Box(Generic[T]):
        """泛型容器"""
        
        def __init__(self, value: T):
            self._value = value
        
        def get(self) -> T:
            """获取值"""
            return self._value
        
        def set(self, value: T) -> None:
            """设置值"""
            self._value = value
        
        def __str__(self) -> str:
            return f"Box({self._value})"
    
    # 使用泛型
    int_box = Box[int](42)
    str_box = Box[str]("Hello")
    
    print(f"   整数容器: {int_box}")
    print(f"   字符串容器: {str_box}")
    
    # 更复杂的泛型示例
    class Repository(Generic[T]):
        """泛型仓库"""
        
        def __init__(self):
            self._items: List[T] = []
        
        def add(self, item: T) -> None:
            """添加项目"""
            self._items.append(item)
        
        def get_all(self) -> List[T]:
            """获取所有项目"""
            return self._items.copy()
        
        def find_by_predicate(self, predicate) -> Optional[T]:
            """根据条件查找"""
            for item in self._items:
                if predicate(item):
                    return item
            return None
    
    # 使用泛型仓库
    user_repo = Repository[Person]()
    person = Person("张三", 25)
    user_repo.add(person)
    
    found_user = user_repo.find_by_predicate(lambda p: p.name == "张三")
    print(f"   查找用户: {found_user}")
    print()


def demonstrate_enum_comparison():
    """
    演示枚举对比
    Java枚举 vs Python枚举
    """
    print("=== 枚举对比 ===\n")
    
    print("Java枚举:")
    print("   public enum Status {")
    print("       PENDING(\"待处理\"),")
    print("       APPROVED(\"已批准\"),")
    print("       REJECTED(\"已拒绝\");")
    print("       ")
    print("       private String description;")
    print("       Status(String desc) { this.description = desc; }")
    print("   }")
    print()
    
    print("Python枚举:")
    print("   class Status(Enum):")
    print("       PENDING = \"待处理\"")
    print("       APPROVED = \"已批准\"")
    print("       REJECTED = \"已拒绝\"")
    print()
    
    # Python枚举示例
    class Status(Enum):
        """状态枚举"""
        PENDING = "待处理"
        APPROVED = "已批准"
        REJECTED = "已拒绝"
        
        def __str__(self):
            return self.value
    
    class Priority(Enum):
        """优先级枚举 - 使用auto()"""
        LOW = auto()
        MEDIUM = auto()
        HIGH = auto()
        URGENT = auto()
        
        def __lt__(self, other):
            """支持比较"""
            if self.__class__ is other.__class__:
                return self.value < other.value
            return NotImplemented
    
    # 使用枚举
    current_status = Status.PENDING
    task_priority = Priority.HIGH
    
    print(f"   当前状态: {current_status}")
    print(f"   任务优先级: {task_priority}")
    print(f"   优先级比较: {Priority.LOW} < {Priority.HIGH} = {Priority.LOW < Priority.HIGH}")
    
    # 枚举迭代
    print("   所有状态:")
    for status in Status:
        print(f"     {status.name}: {status.value}")
    print()


def demonstrate_annotations_comparison():
    """
    演示注解对比
    Java注解 vs Python装饰器
    """
    print("=== 注解/装饰器对比 ===\n")
    
    print("Java注解:")
    print("   @Override")
    print("   @Deprecated")
    print("   @SuppressWarnings(\"unchecked\")")
    print("   @Entity")
    print("   @Table(name=\"users\")")
    print()
    
    print("Python装饰器:")
    print("   @property")
    print("   @staticmethod")
    print("   @classmethod")
    print("   @dataclass")
    print("   @deprecated")
    print()
    
    # 自定义装饰器示例
    def deprecated(func):
        """标记函数为已弃用"""
        def wrapper(*args, **kwargs):
            print(f"警告: {func.__name__} 已弃用")
            return func(*args, **kwargs)
        return wrapper
    
    def validate_types(**types):
        """类型验证装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                # 简单的类型检查
                for arg_name, expected_type in types.items():
                    if arg_name in kwargs:
                        value = kwargs[arg_name]
                        if not isinstance(value, expected_type):
                            raise TypeError(f"{arg_name} 应该是 {expected_type.__name__}")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    class Calculator:
        """计算器类 - 展示装饰器使用"""
        
        @staticmethod
        @validate_types(a=int, b=int)
        def add(a: int, b: int) -> int:
            """加法"""
            return a + b
        
        @staticmethod
        @deprecated
        def old_multiply(a: int, b: int) -> int:
            """旧的乘法方法"""
            return a * b
        
        @staticmethod
        def multiply(a: int, b: int) -> int:
            """新的乘法方法"""
            return a * b
    
    # 使用装饰器
    print("   装饰器演示:")
    result1 = Calculator.add(a=5, b=3)
    print(f"   加法结果: {result1}")
    
    result2 = Calculator.old_multiply(4, 5)
    print(f"   旧乘法结果: {result2}")
    print()


def demonstrate_reflection_comparison():
    """
    演示反射对比
    Java反射 vs Python内省
    """
    print("=== 反射/内省对比 ===\n")
    
    print("Java反射:")
    print("   Class.forName(\"className\")")
    print("   obj.getClass().getMethods()")
    print("   field.get(obj)")
    print()
    
    print("Python内省:")
    print("   type(obj)")
    print("   dir(obj)")
    print("   getattr(obj, 'attr')")
    print("   hasattr(obj, 'attr')")
    print()
    
    class SampleClass:
        """示例类用于内省"""
        
        class_var = "类变量"
        
        def __init__(self, name: str):
            self.name = name
            self._private = "私有属性"
        
        def public_method(self):
            """公有方法"""
            return "公有方法被调用"
        
        def _protected_method(self):
            """受保护方法"""
            return "受保护方法被调用"
        
        @staticmethod
        def static_method():
            """静态方法"""
            return "静态方法被调用"
        
        @classmethod
        def class_method(cls):
            """类方法"""
            return f"类方法被调用: {cls.__name__}"
    
    obj = SampleClass("测试对象")
    
    print("   Python内省演示:")
    print(f"   对象类型: {type(obj)}")
    print(f"   类名: {obj.__class__.__name__}")
    print(f"   模块: {obj.__class__.__module__}")
    
    # 获取所有属性和方法
    print("\n   所有属性和方法:")
    for attr_name in dir(obj):
        if not attr_name.startswith('__'):
            attr_value = getattr(obj, attr_name)
            attr_type = type(attr_value).__name__
            print(f"     {attr_name}: {attr_type}")
    
    # 动态调用方法
    print("\n   动态方法调用:")
    if hasattr(obj, 'public_method'):
        result = getattr(obj, 'public_method')()
        print(f"     {result}")
    
    # 检查方法签名
    print("\n   方法签名:")
    sig = inspect.signature(obj.public_method)
    print(f"     public_method{sig}")
    
    # 获取类的MRO
    print(f"\n   方法解析顺序: {[cls.__name__ for cls in SampleClass.__mro__]}")
    print()


def main():
    """主函数 - 演示所有OOP对比"""
    print("Python高级特性学习 - OOP与Java对比")
    print("=" * 60)
    
    demonstrate_class_definition_comparison()
    demonstrate_access_control_comparison()
    demonstrate_interface_comparison()
    demonstrate_generics_comparison()
    demonstrate_enum_comparison()
    demonstrate_annotations_comparison()
    demonstrate_reflection_comparison()
    
    print("学习总结:")
    print("1. Python类定义更简洁，dataclass进一步简化")
    print("2. Python访问控制基于约定，而非关键字")
    print("3. Protocol提供结构化子类型，ABC提供名义子类型")
    print("4. Python类型系统更灵活，支持渐进式类型")
    print("5. Python装饰器比Java注解更强大")
    print("6. Python内省功能强大且易用")
    print("7. Python的OOP更加动态和灵活")


if __name__ == "__main__":
    main() 