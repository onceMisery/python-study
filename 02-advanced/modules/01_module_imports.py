"""
Python模块导入详解
作者：Python学习项目
日期：2024-01-16

本文件演示Python中的模块导入机制，包含与Java的详细对比
重点：import机制 vs Java import和package系统
"""

# 标准库导入示例
import os
import sys
import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, namedtuple
from typing import List, Dict, Optional, Union

# 相对导入和绝对导入示例（在包内使用）
# from . import sibling_module      # 相对导入同级模块
# from ..parent import parent_module # 相对导入父级模块
# from mypackage.subpackage import module  # 绝对导入


def basic_import_examples():
    """
    基础导入示例
    
    Java对比：
    - Python: import module_name
    - Java: import package.ClassName;
    """
    print("=== 基础导入示例 ===")
    
    # 1. 整个模块导入
    # import os
    print(f"当前目录: {os.getcwd()}")
    print(f"操作系统: {os.name}")
    
    """
    Java对比：
    import java.io.File;
    File currentDir = new File(".");
    """
    
    # 2. 从模块导入特定内容
    # from datetime import datetime
    current_time = datetime.now()
    print(f"当前时间: {current_time}")
    
    """
    Java对比：
    import java.time.LocalDateTime;
    LocalDateTime now = LocalDateTime.now();
    """
    
    # 3. 导入时重命名
    import json as js
    data = {"name": "Python", "version": "3.9"}
    json_str = js.dumps(data)
    print(f"JSON字符串: {json_str}")
    
    """
    Java对比：
    // Java没有直接的重命名，但可以用全限定名
    com.fasterxml.jackson.databind.ObjectMapper mapper = 
        new com.fasterxml.jackson.databind.ObjectMapper();
    """
    
    # 4. 导入模块中的多个内容
    from math import sin, cos, pi, sqrt
    print(f"sin(π/2) = {sin(pi/2)}")
    print(f"cos(0) = {cos(0)}")
    print(f"√16 = {sqrt(16)}")
    
    """
    Java对比：
    import static java.lang.Math.*;
    double result = sin(PI/2);
    """


def advanced_import_patterns():
    """
    高级导入模式
    """
    print("\n=== 高级导入模式 ===")
    
    # 1. 条件导入
    try:
        import numpy as np
        has_numpy = True
        print("✓ NumPy可用")
    except ImportError:
        has_numpy = False
        print("✗ NumPy不可用，使用内置math模块")
    
    if has_numpy:
        # 使用NumPy
        arr = np.array([1, 2, 3, 4])
        print(f"NumPy数组: {arr}")
    else:
        # 使用内置功能
        arr = [1, 2, 3, 4]
        print(f"普通列表: {arr}")
    
    """
    Java对比：
    // Java通常在编译时确定依赖
    try {
        Class.forName("com.some.OptionalLibrary");
        // 使用可选库
    } catch (ClassNotFoundException e) {
        // 使用备选方案
    }
    """
    
    # 2. 延迟导入
    def process_data_with_pandas():
        """在函数内部导入，避免启动时开销"""
        try:
            import pandas as pd
            # 创建示例DataFrame
            data = {"A": [1, 2, 3], "B": [4, 5, 6]}
            df = pd.DataFrame(data)
            return f"Pandas DataFrame:\n{df}"
        except ImportError:
            return "Pandas不可用"
    
    print("延迟导入示例:")
    result = process_data_with_pandas()
    print(result)
    
    # 3. 动态导入
    module_name = "json"
    try:
        # 使用importlib动态导入
        import importlib
        dynamic_module = importlib.import_module(module_name)
        
        test_data = {"dynamic": True, "import": "successful"}
        json_result = dynamic_module.dumps(test_data)
        print(f"动态导入{module_name}模块成功: {json_result}")
    except ImportError as e:
        print(f"动态导入失败: {e}")
    
    """
    Java对比：
    // Java反射加载类
    Class<?> clazz = Class.forName("com.example.MyClass");
    Object instance = clazz.getDeclaredConstructor().newInstance();
    """
    
    # 4. 重新加载模块 (开发时使用)
    print("\n模块重新加载示例:")
    # importlib.reload(module_name)  # 重新加载已导入的模块
    print("注意：重新加载主要用于开发调试，生产环境不建议使用")


def import_search_path():
    """
    导入搜索路径
    """
    print("\n=== 导入搜索路径 ===")
    
    print("Python模块搜索路径:")
    for i, path in enumerate(sys.path):
        print(f"  {i+1}. {path}")
    
    # 添加自定义路径
    custom_path = str(Path.cwd() / "custom_modules")
    if custom_path not in sys.path:
        sys.path.append(custom_path)
        print(f"\n添加自定义路径: {custom_path}")
    
    # 环境变量PYTHONPATH
    python_path = os.environ.get('PYTHONPATH', '无')
    print(f"PYTHONPATH环境变量: {python_path}")
    
    """
    Java对比：
    CLASSPATH环境变量:
    - 设置类搜索路径
    - java -cp /path/to/classes MyClass
    - Maven/Gradle管理依赖路径
    """
    
    print("\n搜索顺序:")
    print("1. 当前目录")
    print("2. PYTHONPATH环境变量指定的目录")
    print("3. 标准库目录")
    print("4. site-packages目录")


def package_structure_demo():
    """
    包结构演示
    """
    print("\n=== Python包结构 ===")
    
    # 创建示例包结构
    demo_package = Path("demo_package")
    
    # 创建包目录和__init__.py
    package_structure = {
        "demo_package/__init__.py": '''"""
示例包的初始化文件
"""

__version__ = "1.0.0"
__author__ = "Python学习项目"

# 包级别的导入
from .utils import helper_function
from .core.processor import DataProcessor

# 定义包的公共API
__all__ = [
    "helper_function",
    "DataProcessor",
    "PACKAGE_VERSION"
]

PACKAGE_VERSION = __version__
''',
        
        "demo_package/utils.py": '''"""
工具模块
"""

def helper_function(data):
    """辅助函数"""
    return f"处理数据: {data}"

def format_output(result):
    """格式化输出"""
    return f"结果: {result}"
''',
        
        "demo_package/core/__init__.py": '''"""
核心模块包
"""

from .processor import DataProcessor
from .validator import DataValidator

__all__ = ["DataProcessor", "DataValidator"]
''',
        
        "demo_package/core/processor.py": '''"""
数据处理器
"""

class DataProcessor:
    """数据处理器类"""
    
    def __init__(self, name="默认处理器"):
        self.name = name
    
    def process(self, data):
        """处理数据"""
        return f"{self.name}处理: {data}"
    
    def __repr__(self):
        return f"DataProcessor(name='{self.name}')"
''',
        
        "demo_package/core/validator.py": '''"""
数据验证器
"""

class DataValidator:
    """数据验证器"""
    
    @staticmethod
    def validate_string(value):
        """验证字符串"""
        return isinstance(value, str) and len(value) > 0
    
    @staticmethod
    def validate_number(value):
        """验证数字"""
        return isinstance(value, (int, float))
'''
    }
    
    # 创建包结构
    try:
        for file_path, content in package_structure.items():
            full_path = Path(file_path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
        
        print("✓ 创建示例包结构完成")
        
        # 显示包结构
        print("\n包结构:")
        for file_path in package_structure.keys():
            depth = file_path.count('/') - 1
            indent = "  " * depth
            filename = Path(file_path).name
            print(f"{indent}{filename}")
        
    except Exception as e:
        print(f"创建包结构失败: {e}")
    
    """
    Java对比：
    com/
    └── example/
        └── myproject/
            ├── Main.java
            ├── utils/
            │   └── Helper.java
            └── core/
                ├── Processor.java
                └── Validator.java
    
    Java包声明：
    package com.example.myproject.core;
    import com.example.myproject.utils.Helper;
    """


def import_best_practices():
    """
    导入最佳实践
    """
    print("\n=== 导入最佳实践 ===")
    
    print("1. 导入顺序 (PEP 8标准):")
    print("   a) 标准库导入")
    print("   b) 第三方库导入") 
    print("   c) 本地应用/库导入")
    print("   d) 每组之间用空行分隔")
    
    # 示例正确的导入顺序
    example_imports = '''
# 标准库
import os
import sys
from datetime import datetime
from pathlib import Path

# 第三方库
import requests
import numpy as np
import pandas as pd

# 本地导入
from myapp.core import processor
from myapp.utils import helpers
from . import local_module
'''
    print("示例导入顺序:")
    print(example_imports)
    
    print("2. 导入原则:")
    print("   ✓ 每行一个导入语句")
    print("   ✓ 使用绝对导入优于相对导入")
    print("   ✓ 避免使用 from module import *")
    print("   ✓ 长导入语句可以使用括号换行")
    
    # 好的例子
    print("\n✓ 推荐的导入方式:")
    print("import os")
    print("import sys")
    print("from collections import defaultdict, OrderedDict")
    print("from mypackage.submodule import (")
    print("    function1,")
    print("    function2,")
    print("    ClassName")
    print(")")
    
    # 不好的例子
    print("\n✗ 不推荐的导入方式:")
    print("import os, sys  # 多个模块在一行")
    print("from math import *  # 导入所有，可能命名冲突")
    print("import really.long.module.name.that.is.hard.to.read")
    
    """
    Java对比：
    // Java导入最佳实践
    import java.util.List;           // 标准库
    import java.util.ArrayList;
    
    import org.springframework.web.*; // 第三方库
    
    import com.mycompany.myapp.*;    // 本地包
    """


def circular_imports_demo():
    """
    循环导入问题演示
    """
    print("\n=== 循环导入问题 ===")
    
    print("循环导入是什么？")
    print("当两个或多个模块相互导入时发生的问题")
    
    # 创建循环导入示例
    module_a_content = '''
# module_a.py
print("正在导入 module_a")

from module_b import function_b

def function_a():
    return "来自A模块"

def call_b():
    return function_b()
'''
    
    module_b_content = '''
# module_b.py  
print("正在导入 module_b")

from module_a import function_a

def function_b():
    return "来自B模块"

def call_a():
    return function_a()
'''
    
    print("问题示例:")
    print("module_a.py:")
    print(module_a_content)
    print("module_b.py:")
    print(module_b_content)
    
    print("解决方案:")
    print("1. 重构代码，移除循环依赖")
    print("2. 将共同依赖提取到第三个模块")
    print("3. 使用函数内导入（延迟导入）")
    print("4. 使用importlib进行动态导入")
    
    # 解决方案示例
    solution_example = '''
# 解决方案1: 函数内导入
def call_b():
    from module_b import function_b
    return function_b()

# 解决方案2: 提取公共模块
# common.py
def shared_function():
    return "共享功能"

# module_a.py
from common import shared_function

# module_b.py  
from common import shared_function
'''
    print("解决方案代码:")
    print(solution_example)
    
    """
    Java对比：
    Java在编译时检查循环依赖，会直接报错：
    "Cyclic inheritance involving ClassName"
    
    Java解决方案：
    1. 接口分离
    2. 依赖注入
    3. 工厂模式
    4. 观察者模式
    """


def namespace_packages():
    """
    命名空间包
    """
    print("\n=== 命名空间包 ===")
    
    print("命名空间包允许将一个逻辑包分布在多个目录中")
    
    # PEP 420 命名空间包示例
    namespace_example = '''
# 目录结构
project/
├── path1/
│   └── namespace_package/
│       └── module1.py
└── path2/
    └── namespace_package/
        └── module2.py

# 注意：没有 __init__.py 文件

# 使用方式
import sys
sys.path.extend(['path1', 'path2'])

from namespace_package import module1
from namespace_package import module2
'''
    
    print("命名空间包示例:")
    print(namespace_example)
    
    print("特点:")
    print("1. 不需要 __init__.py 文件")
    print("2. 可以分布在不同的目录中")
    print("3. Python 3.3+ 支持")
    print("4. 主要用于大型项目和插件系统")
    
    """
    Java对比：
    Java包必须在连续的目录结构中：
    com/
    └── example/
        └── project/
            ├── module1/
            └── module2/
    
    但可以通过JAR文件分发：
    app.jar: com/example/project/module1/
    plugin.jar: com/example/project/module2/
    """


def import_performance():
    """
    导入性能考虑
    """
    print("\n=== 导入性能考虑 ===")
    
    import time
    
    # 测试导入时间
    start_time = time.time()
    import datetime
    import_time = time.time() - start_time
    print(f"导入datetime模块耗时: {import_time:.6f}秒")
    
    # 测试重复导入
    start_time = time.time()
    import datetime  # 再次导入
    reimport_time = time.time() - start_time
    print(f"重复导入datetime模块耗时: {reimport_time:.6f}秒")
    
    print("\n性能优化建议:")
    print("1. 避免在循环中导入模块")
    print("2. 使用 from module import function 减少属性查找")
    print("3. 考虑延迟导入重型模块")
    print("4. 使用 __all__ 控制 from module import * 的行为")
    
    # 性能对比示例
    def performance_test():
        # 完整模块导入
        import math
        
        start = time.time()
        for _ in range(10000):
            result = math.sqrt(16)
        full_import_time = time.time() - start
        
        # 直接导入函数
        from math import sqrt
        
        start = time.time()
        for _ in range(10000):
            result = sqrt(16)
        direct_import_time = time.time() - start
        
        print(f"\n性能测试结果 (10000次调用):")
        print(f"math.sqrt(): {full_import_time:.6f}秒")
        print(f"sqrt(): {direct_import_time:.6f}秒")
        print(f"性能提升: {full_import_time/direct_import_time:.2f}倍")
    
    performance_test()
    
    """
    Java对比：
    Java在编译时解析导入，运行时性能几乎无差异：
    import java.lang.Math;
    Math.sqrt(16);  // 编译时已解析
    
    import static java.lang.Math.sqrt;
    sqrt(16);  // 同样的性能
    """


def debugging_imports():
    """
    调试导入问题
    """
    print("\n=== 调试导入问题 ===")
    
    print("常见导入问题及解决方案:")
    
    # 1. 查看模块路径
    print("1. 查看模块搜索路径:")
    import sys
    print(f"   sys.path包含 {len(sys.path)} 个路径")
    
    # 2. 查看已导入的模块
    print(f"\n2. 已导入模块数量: {len(sys.modules)}")
    print("   部分已导入模块:")
    for i, module_name in enumerate(list(sys.modules.keys())[:5]):
        print(f"   - {module_name}")
    if len(sys.modules) > 5:
        print("   ...")
    
    # 3. 查看模块位置
    print("\n3. 查看模块位置:")
    modules_to_check = ['os', 'sys', 'json']
    for module_name in modules_to_check:
        if module_name in sys.modules:
            module = sys.modules[module_name]
            location = getattr(module, '__file__', '内置模块')
            print(f"   {module_name}: {location}")
    
    # 4. 导入调试技巧
    print("\n4. 调试技巧:")
    print("   - 使用 python -v 查看详细导入信息")
    print("   - 使用 importlib.util.find_spec() 查找模块")
    print("   - 检查 __name__ 和 __package__ 属性")
    print("   - 使用 sys.modules 查看已导入模块")
    
    # 5. 查找模块示例
    import importlib.util
    
    module_name = "json"
    spec = importlib.util.find_spec(module_name)
    if spec:
        print(f"\n5. 模块 {module_name} 信息:")
        print(f"   位置: {spec.origin}")
        print(f"   是否为包: {spec.submodule_search_locations is not None}")
    
    """
    Java对比：
    Java调试导入：
    1. java -verbose:class 查看类加载
    2. ClassLoader.getSystemResource() 查找资源
    3. 使用IDE的依赖分析工具
    4. Maven/Gradle的依赖树命令
    """


def main():
    """主函数：演示所有导入相关功能"""
    print("Python模块导入详解")
    print("=" * 50)
    
    try:
        basic_import_examples()
        advanced_import_patterns()
        import_search_path()
        package_structure_demo()
        import_best_practices()
        circular_imports_demo()
        namespace_packages()
        import_performance()
        debugging_imports()
        
        print("\n总结:")
        print("1. Python的导入机制灵活且强大")
        print("2. 合理的包结构设计很重要")
        print("3. 遵循PEP 8导入规范")
        print("4. 注意性能和循环导入问题")
        print("5. 善用调试工具解决导入问题")
        
        print("\nJava开发者迁移建议:")
        print("1. Python包 ≈ Java包，但更灵活")
        print("2. __init__.py ≈ package-info.java")
        print("3. 相对导入在Java中较少使用")
        print("4. Python的动态导入比Java反射更简单")
        
    except Exception as e:
        print(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 