"""
Python vs Java 包机制全面对比
作者：Python学习项目  
日期：2024-01-16

本文件详细对比Python和Java的包机制差异
重点：帮助Java开发者理解Python包的设计理念
"""

import os
import sys
import importlib
import inspect
from pathlib import Path
from typing import List, Dict, Any


def package_concept_comparison():
    """
    包概念对比
    """
    print("=== 包概念对比 ===")
    
    print("Python包概念:")
    print("1. 包是包含__init__.py文件的目录")
    print("2. 包可以嵌套，形成包层次结构")
    print("3. 包既是命名空间也是模块")
    print("4. 可以包含可执行代码")
    print("5. 支持动态导入和修改")
    
    print("\nJava包概念:")
    java_concepts = """
1. 包是相关类和接口的集合
2. 通过package语句声明
3. 主要用于命名空间管理
4. 编译时确定包结构
5. 访问控制的基本单位
"""
    print(java_concepts)
    
    print("核心差异:")
    differences = [
        "Python包是运行时概念，Java包是编译时概念",
        "Python包可以包含执行代码，Java包主要是组织结构",
        "Python支持包级别的导入控制，Java依赖访问修饰符",
        "Python包可以动态修改，Java包结构相对固定",
        "Python包支持相对导入，Java包导入都是绝对的"
    ]
    
    for i, diff in enumerate(differences, 1):
        print(f"{i}. {diff}")


def directory_structure_comparison():
    """
    目录结构对比
    """
    print("\n=== 目录结构对比 ===")
    
    print("Python包结构示例:")
    python_structure = """
myproject/
├── __init__.py              # 包初始化文件
├── core/
│   ├── __init__.py          # 子包初始化
│   ├── processor.py         # 处理器模块
│   └── config.py           # 配置模块
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── validators.py
├── api/
│   ├── __init__.py
│   ├── client.py
│   └── exceptions.py
└── tests/
    ├── __init__.py
    ├── test_core.py
    └── test_utils.py
"""
    print(python_structure)
    
    print("Java包结构示例:")
    java_structure = """
src/main/java/
└── com/
    └── mycompany/
        └── myproject/
            ├── core/
            │   ├── Processor.java
            │   └── Config.java
            ├── utils/
            │   ├── Helpers.java
            │   └── Validators.java
            ├── api/
            │   ├── Client.java
            │   └── APIException.java
            └── Main.java

src/test/java/
└── com/
    └── mycompany/
        └── myproject/
            ├── core/
            │   └── ProcessorTest.java
            └── utils/
                └── HelpersTest.java
"""
    print(java_structure)
    
    print("结构差异分析:")
    structure_diffs = [
        "Python: __init__.py标识包，Java: 目录结构即包",
        "Python: 相对扁平，Java: 深层次域名结构",
        "Python: 测试可在同一目录，Java: 严格分离src/test",
        "Python: 包名即目录名，Java: 全限定包名路径",
        "Python: 灵活的文件组织，Java: 一个类一个文件"
    ]
    
    for diff in structure_diffs:
        print(f"- {diff}")


def import_system_comparison():
    """
    导入系统对比
    """
    print("\n=== 导入系统对比 ===")
    
    # Python导入示例
    print("Python导入语法:")
    python_imports = """
# 基本导入
import os
import sys
from datetime import datetime

# 包导入
import myproject.core.processor
from myproject.core import processor
from myproject.utils.helpers import retry_decorator

# 相对导入（包内使用）
from . import sibling_module
from ..parent import parent_module
from .submodule import function

# 重命名导入
import numpy as np
from collections import defaultdict as dd

# 条件导入
try:
    import optional_module
except ImportError:
    optional_module = None

# 动态导入
module_name = "json"
json_module = importlib.import_module(module_name)
"""
    print(python_imports)
    
    print("Java导入语法:")
    java_imports = """
// 基本导入
import java.util.*;
import java.io.File;
import java.time.LocalDateTime;

// 包导入
import com.mycompany.myproject.core.Processor;
import com.mycompany.myproject.utils.Helpers;

// 静态导入
import static java.lang.Math.*;
import static com.mycompany.utils.Constants.DEFAULT_SIZE;

// 通配符导入（不推荐）
import java.util.*;

// 完全限定名（无导入）
java.util.List<String> list = new java.util.ArrayList<>();

// 动态加载
Class<?> clazz = Class.forName("com.example.MyClass");
Object instance = clazz.getDeclaredConstructor().newInstance();
"""
    print(java_imports)
    
    # 对比导入特性
    print("导入特性对比:")
    import_features = [
        ("特性", "Python", "Java"),
        ("-" * 20, "-" * 30, "-" * 35),
        ("相对导入", "支持 (., ..)", "不支持"),
        ("重命名导入", "import module as name", "不支持直接重命名"),
        ("条件导入", "try/except ImportError", "Class.forName + 异常处理"),
        ("动态导入", "importlib.import_module", "Class.forName反射"),
        ("通配符导入", "from module import *", "import package.*"),
        ("导入时执行", "模块代码会执行", "类加载时静态块执行"),
        ("循环导入", "运行时可能出错", "编译时检查"),
        ("导入搜索", "sys.path动态搜索", "CLASSPATH静态路径"),
    ]
    
    for row in import_features:
        print(f"{row[0]:<20} | {row[1]:<30} | {row[2]:<35}")


def access_control_comparison():
    """
    访问控制对比
    """
    print("\n=== 访问控制对比 ===")
    
    print("Python访问控制（约定）:")
    python_access = """
class MyClass:
    def __init__(self):
        self.public_attr = "公开属性"
        self._protected_attr = "受保护属性（约定）"
        self.__private_attr = "私有属性（名称改写）"
    
    def public_method(self):
        '''公开方法'''
        pass
    
    def _protected_method(self):
        '''受保护方法（约定）'''
        pass
    
    def __private_method(self):
        '''私有方法（名称改写）'''
        pass

# 模块级别访问控制
__all__ = ['MyClass', 'public_function']  # 控制from module import *

def public_function():
    '''公开函数'''
    pass

def _internal_function():
    '''内部函数（约定）'''
    pass
"""
    print(python_access)
    
    print("Java访问控制（关键字）:")
    java_access = """
package com.mycompany.myproject;

public class MyClass {
    public String publicField = "公开字段";
    protected String protectedField = "受保护字段";
    String packageField = "包私有字段";
    private String privateField = "私有字段";
    
    public void publicMethod() {
        // 公开方法
    }
    
    protected void protectedMethod() {
        // 受保护方法
    }
    
    void packageMethod() {
        // 包私有方法
    }
    
    private void privateMethod() {
        // 私有方法
    }
}

// 类级别访问控制
public class PublicClass { }        // 包外可访问
class PackageClass { }              // 包内可访问
"""
    print(java_access)
    
    print("访问控制对比:")
    access_comparison = [
        ("级别", "Python", "Java", "说明"),
        ("-" * 8, "-" * 25, "-" * 25, "-" * 30),
        ("公开", "无前缀", "public", "完全可访问"),
        ("受保护", "_前缀（约定）", "protected", "子类和包内访问"),
        ("包私有", "不支持", "无修饰符", "包内访问"),
        ("私有", "__前缀（名称改写）", "private", "类内访问"),
        ("模块控制", "__all__列表", "不适用", "控制导入内容"),
        ("编译检查", "运行时约定", "编译时强制", "检查时机"),
    ]
    
    for row in access_comparison:
        print(f"{row[0]:<8} | {row[1]:<25} | {row[2]:<25} | {row[3]:<30}")


def namespace_management():
    """
    命名空间管理对比
    """
    print("\n=== 命名空间管理对比 ===")
    
    print("Python命名空间:")
    print("1. 模块命名空间 - 每个.py文件")
    print("2. 类命名空间 - 每个类定义")
    print("3. 函数命名空间 - 每个函数调用")
    print("4. 内置命名空间 - Python内置名称")
    print("5. 全局命名空间 - 模块级别变量")
    print("6. 局部命名空间 - 函数内变量")
    
    # 演示Python命名空间
    print("\nPython命名空间示例:")
    
    # 全局变量
    global_var = "全局变量"
    
    def demo_namespace():
        # 局部变量
        local_var = "局部变量"
        
        # 查看命名空间
        print(f"  局部命名空间: {list(locals().keys())}")
        print(f"  全局命名空间示例: {list(globals().keys())[-5:]}")  # 显示最后5个
        
        # 嵌套函数
        def nested_function():
            nested_var = "嵌套变量"
            print(f"  嵌套函数局部变量: {nested_var}")
            print(f"  访问外层变量: {local_var}")
            print(f"  访问全局变量: {global_var}")
        
        nested_function()
    
    demo_namespace()
    
    print("\nJava命名空间:")
    java_namespace = """
// Java命名空间通过包和类管理
package com.mycompany.myproject;

import java.util.List;
import com.other.package.SomeClass;

public class MyClass {
    // 类级别变量
    private static final String CLASS_VAR = "类变量";
    private String instanceVar = "实例变量";
    
    public void myMethod() {
        // 方法级别变量
        String localVar = "局部变量";
        
        // 同名变量的处理
        String instanceVar = "局部变量覆盖实例变量";
        this.instanceVar = "通过this访问实例变量";
        MyClass.CLASS_VAR;  // 访问类变量
        
        // 完全限定名避免冲突
        java.util.Date date1 = new java.util.Date();
        java.sql.Date date2 = new java.sql.Date(0);
    }
}
"""
    print(java_namespace)
    
    print("命名空间管理差异:")
    namespace_diffs = [
        "Python: 运行时动态命名空间，Java: 编译时静态作用域",
        "Python: LEGB规则(Local/Enclosing/Global/Built-in)，Java: 就近原则",
        "Python: global/nonlocal关键字修改作用域，Java: this/super引用",
        "Python: 可以动态修改命名空间，Java: 编译时确定",
        "Python: 模块即命名空间，Java: 包+类组成命名空间"
    ]
    
    for i, diff in enumerate(namespace_diffs, 1):
        print(f"{i}. {diff}")


def module_loading_comparison():
    """
    模块加载机制对比
    """
    print("\n=== 模块加载机制对比 ===")
    
    print("Python模块加载:")
    print("1. 搜索路径: sys.path")
    print("2. 导入缓存: sys.modules")
    print("3. 加载器: importlib机制")
    print("4. 执行时机: 首次导入时执行")
    print("5. 重新加载: importlib.reload()")
    
    # 演示Python模块加载
    print("\nPython模块加载演示:")
    
    # 显示搜索路径
    print(f"搜索路径数量: {len(sys.path)}")
    print(f"前3个搜索路径:")
    for i, path in enumerate(sys.path[:3]):
        print(f"  {i+1}. {path}")
    
    # 显示已加载模块
    print(f"\n已加载模块数量: {len(sys.modules)}")
    print("部分已加载模块:")
    for i, module_name in enumerate(list(sys.modules.keys())[:5]):
        print(f"  {module_name}")
    
    # 查看模块信息
    if 'os' in sys.modules:
        os_module = sys.modules['os']
        print(f"\nos模块信息:")
        print(f"  模块文件: {getattr(os_module, '__file__', '内置模块')}")
        print(f"  模块包: {getattr(os_module, '__package__', None)}")
    
    print("\nJava类加载:")
    java_loading = """
Java类加载机制:
1. Bootstrap ClassLoader - 核心类库
2. Extension ClassLoader - 扩展类库  
3. Application ClassLoader - 应用类路径
4. 双亲委派模型 - 向上委托，向下加载
5. 类初始化 - 静态块执行

类加载过程:
1. 加载(Loading) - 读取.class文件
2. 验证(Verification) - 字节码验证
3. 准备(Preparation) - 分配内存
4. 解析(Resolution) - 符号引用转直接引用
5. 初始化(Initialization) - 执行类初始化代码

示例代码:
public class LoadingDemo {
    static {
        System.out.println("类初始化块执行");
    }
    
    private static final String CONSTANT = "常量";
    
    public static void main(String[] args) {
        // 类加载演示
        ClassLoader loader = LoadingDemo.class.getClassLoader();
        System.out.println("类加载器: " + loader);
    }
}
"""
    print(java_loading)
    
    print("加载机制对比:")
    loading_comparison = [
        ("特性", "Python", "Java"),
        ("-" * 15, "-" * 30, "-" * 35),
        ("加载时机", "运行时动态加载", "首次使用时加载"),
        ("加载策略", "sys.path线性搜索", "双亲委派模型"),
        ("缓存机制", "sys.modules字典", "方法区类信息"),
        ("重新加载", "importlib.reload()", "需要自定义ClassLoader"),
        ("安全检查", "语法检查", "字节码验证"),
        ("初始化", "模块代码执行", "静态初始化块"),
        ("依赖处理", "运行时ImportError", "编译时检查"),
        ("版本控制", "模块路径控制", "ClassLoader隔离"),
    ]
    
    for row in loading_comparison:
        print(f"{row[0]:<15} | {row[1]:<30} | {row[2]:<35}")


def dependency_management():
    """
    依赖管理对比
    """
    print("\n=== 依赖管理对比 ===")
    
    print("Python依赖管理:")
    python_deps = """
1. pip - 包管理器
   pip install package_name
   pip install -r requirements.txt
   pip freeze > requirements.txt

2. requirements.txt - 依赖声明
   requests==2.28.1
   numpy>=1.21.0
   pandas~=1.4.0

3. setup.py - 包定义
   from setuptools import setup
   setup(
       name="myproject",
       version="1.0.0",
       install_requires=[
           "requests>=2.20.0",
           "numpy",
       ]
   )

4. 虚拟环境 - 依赖隔离
   python -m venv myenv
   source myenv/bin/activate  # Linux/Mac
   myenv\\Scripts\\activate   # Windows

5. poetry/pipenv - 现代工具
   poetry add requests
   poetry install
"""
    print(python_deps)
    
    print("Java依赖管理:")
    java_deps = """
1. Maven - 项目管理工具
   <dependency>
       <groupId>org.apache.commons</groupId>
       <artifactId>commons-lang3</artifactId>
       <version>3.12.0</version>
   </dependency>

2. Gradle - 构建工具
   dependencies {
       implementation 'org.apache.commons:commons-lang3:3.12.0'
       testImplementation 'junit:junit:4.13.2'
   }

3. pom.xml/build.gradle - 依赖声明
   - 传递依赖自动解析
   - 版本冲突处理
   - 作用域管理(compile/test/runtime)

4. 仓库管理
   - 中央仓库 Maven Central
   - 私有仓库 Nexus/Artifactory
   - 本地仓库 ~/.m2/repository

5. 模块化 (Java 9+)
   module com.example.myapp {
       requires java.base;
       requires org.apache.commons.lang3;
       exports com.example.api;
   }
"""
    print(java_deps)
    
    print("依赖管理对比:")
    dep_comparison = [
        ("方面", "Python", "Java"),
        ("-" * 12, "-" * 35, "-" * 40),
        ("包管理器", "pip, conda, poetry", "Maven, Gradle, SBT"),
        ("仓库", "PyPI, Anaconda", "Maven Central, JCenter"),
        ("依赖文件", "requirements.txt, pyproject.toml", "pom.xml, build.gradle"),
        ("版本管理", "语义化版本", "语义化版本 + SNAPSHOT"),
        ("传递依赖", "pip自动处理", "Maven/Gradle自动解析"),
        ("冲突解决", "pip-tools, poetry", "Maven dependency mediation"),
        ("环境隔离", "virtualenv, conda", "Maven profiles, Docker"),
        ("构建集成", "setup.py, wheel", "完整的构建生命周期"),
    ]
    
    for row in dep_comparison:
        print(f"{row[0]:<12} | {row[1]:<35} | {row[2]:<40}")


def performance_comparison():
    """
    性能对比
    """
    print("\n=== 性能对比 ===")
    
    print("Python包性能特点:")
    python_perf = [
        "解释执行，导入时编译成字节码",
        "首次导入较慢，后续从缓存读取",
        "动态特性带来灵活性，但影响性能",
        "GIL限制多线程CPU密集型任务",
        "内存占用相对较高",
        "适合原型开发和脚本任务"
    ]
    
    for i, perf in enumerate(python_perf, 1):
        print(f"{i}. {perf}")
    
    print("\nJava包性能特点:")
    java_perf = [
        "编译成字节码，JVM执行",
        "类加载开销较低，热点优化",
        "静态类型，编译时优化",
        "真正的多线程，适合并发处理",
        "内存管理自动，GC优化",
        "适合大型应用和高并发场景"
    ]
    
    for i, perf in enumerate(java_perf, 1):
        print(f"{i}. {perf}")
    
    # 简单性能测试示例
    print("\n性能测试示例:")
    
    import time
    
    # Python导入性能测试
    start_time = time.time()
    for i in range(100):
        # 重复导入已缓存的模块
        import json
    python_import_time = time.time() - start_time
    
    print(f"Python重复导入100次耗时: {python_import_time:.6f}秒")
    
    # 函数调用性能测试
    import math
    
    start_time = time.time()
    for i in range(100000):
        result = math.sqrt(16)
    python_call_time = time.time() - start_time
    
    print(f"Python函数调用100000次耗时: {python_call_time:.6f}秒")
    
    print("\nJava性能对比参考:")
    print("- Java类加载通常比Python模块导入快2-5倍")
    print("- Java方法调用比Python函数调用快5-10倍")
    print("- Java内存使用通常比Python少20-50%")
    print("- Java启动时间通常比Python长（JVM初始化）")


def migration_guide():
    """
    迁移指南
    """
    print("\n=== Java到Python包迁移指南 ===")
    
    print("1. 概念映射:")
    concept_mapping = [
        ("Java概念", "Python对应概念", "说明"),
        ("-" * 15, "-" * 20, "-" * 30),
        ("package", "package/module", "目录结构组织代码"),
        ("import语句", "import语句", "语法略有不同"),
        ("类文件.java", "模块文件.py", "一个文件多个类vs一个文件一个模块"),
        ("类加载器", "import机制", "动态加载vs静态加载"),
        ("CLASSPATH", "sys.path", "搜索路径概念"),
        ("jar文件", "wheel/egg文件", "打包分发格式"),
        ("Maven/Gradle", "pip/poetry", "依赖管理工具"),
        ("interface", "ABC/Protocol", "接口定义方式"),
    ]
    
    for row in concept_mapping:
        print(f"{row[0]:<15} | {row[1]:<20} | {row[2]:<30}")
    
    print("\n2. 迁移步骤:")
    migration_steps = [
        "分析Java包结构，确定Python包组织方式",
        "创建对应的目录结构和__init__.py文件",
        "将Java类转换为Python类或模块",
        "调整导入语句，使用Python语法",
        "处理访问控制，使用Python约定",
        "设置依赖管理，创建requirements.txt",
        "编写测试代码，验证功能正确性",
        "优化性能，处理Python特有问题"
    ]
    
    for i, step in enumerate(migration_steps, 1):
        print(f"{i}. {step}")
    
    print("\n3. 常见陷阱:")
    common_pitfalls = [
        "循环导入问题 - Java编译时检查，Python运行时出错",
        "命名空间污染 - 避免使用from module import *",
        "可变默认参数 - Python特有的陷阱",
        "模块级别代码执行 - 导入时会执行顶级代码",
        "相对导入路径 - 注意包内导入的正确方式",
        "编码问题 - Python 3默认UTF-8，注意文件编码"
    ]
    
    for i, pitfall in enumerate(common_pitfalls, 1):
        print(f"{i}. {pitfall}")
    
    print("\n4. 最佳实践:")
    best_practices = [
        "使用__all__明确定义模块公共API",
        "遵循PEP 8命名规范和代码风格",
        "合理使用类型注解增强代码可读性",
        "编写完整的文档字符串",
        "使用虚拟环境隔离项目依赖",
        "设置合适的日志记录",
        "编写单元测试和集成测试",
        "使用工具检查代码质量（pylint, mypy）"
    ]
    
    for i, practice in enumerate(best_practices, 1):
        print(f"{i}. {practice}")


def advanced_features():
    """
    高级特性对比
    """
    print("\n=== 高级特性对比 ===")
    
    print("Python高级包特性:")
    python_advanced = [
        "命名空间包 - 分布式包定义",
        "包资源访问 - importlib.resources",
        "插件系统 - 动态发现和加载",
        "元类编程 - 动态创建类",
        "装饰器 - AOP式编程",
        "上下文管理器 - 资源管理",
        "生成器和协程 - 异步编程支持",
        "多重继承 - MRO算法"
    ]
    
    for i, feature in enumerate(python_advanced, 1):
        print(f"{i}. {feature}")
    
    print("\nJava高级包特性:")
    java_advanced = [
        "模块系统 (Java 9+) - 强封装",
        "服务加载器 - ServiceLoader机制",
        "注解处理器 - 编译时代码生成",
        "反射API - 运行时类型信息",
        "动态代理 - AOP实现",
        "类加载器 - 自定义加载策略",
        "并发工具 - java.util.concurrent",
        "泛型系统 - 类型安全"
    ]
    
    for i, feature in enumerate(java_advanced, 1):
        print(f"{i}. {feature}")
    
    print("\n特性对比总结:")
    print("Python: 更灵活，动态特性丰富，适合快速开发")
    print("Java: 更严格，静态类型安全，适合大型系统")
    print("选择依据: 项目规模、性能要求、团队技能、维护成本")


def main():
    """主函数：演示所有对比内容"""
    print("Python vs Java 包机制全面对比")
    print("=" * 60)
    
    try:
        package_concept_comparison()
        directory_structure_comparison()
        import_system_comparison()
        access_control_comparison()
        namespace_management()
        module_loading_comparison()
        dependency_management()
        performance_comparison()
        migration_guide()
        advanced_features()
        
        print("\n总结:")
        print("1. Python包更灵活，支持动态特性和运行时修改")
        print("2. Java包更严格，提供编译时安全和更好的性能")
        print("3. Python适合快速原型和脚本开发")
        print("4. Java适合大型企业应用和高并发系统")
        print("5. 理解两者差异有助于更好地进行技术选型")
        
        print("\n学习建议:")
        print("1. 从Java的静态思维转向Python的动态思维")
        print("2. 理解Python的duck typing和动态特性")
        print("3. 学会使用Python的包管理工具")
        print("4. 掌握Python的异常处理和资源管理")
        print("5. 实践中逐步熟悉Python的最佳实践")
        
    except Exception as e:
        print(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 