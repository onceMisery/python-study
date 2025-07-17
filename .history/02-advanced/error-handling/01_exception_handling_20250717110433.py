#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python高级特性 - 异常处理机制
============================

本文件演示Python的异常处理机制，并与Java进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

import logging
import traceback
import sys
from typing import Optional, Union, Any
from contextlib import contextmanager


def demonstrate_basic_exception_handling():
    """
    演示基本异常处理
    Python vs Java
    """
    print("=== 基本异常处理 ===\n")
    
    print("Java vs Python异常处理语法:")
    print("Java:")
    print("   try {")
    print("       // 可能抛出异常的代码")
    print("   } catch (SpecificException e) {")
    print("       // 处理特定异常")
    print("   } catch (Exception e) {")
    print("       // 处理通用异常")
    print("   } finally {")
    print("       // 清理代码")
    print("   }")
    print()
    
    print("Python:")
    print("   try:")
    print("       # 可能抛出异常的代码")
    print("   except SpecificException as e:")
    print("       # 处理特定异常")
    print("   except Exception as e:")
    print("       # 处理通用异常")
    print("   else:")
    print("       # 没有异常时执行")
    print("   finally:")
    print("       # 清理代码")
    print()
    
    # 1. 基本try-except示例
    print("1. 基本try-except示例")
    
    def divide_numbers(a: float, b: float) -> float:
        """除法运算 - 可能抛出异常"""
        try:
            result = a / b
            print(f"   {a} ÷ {b} = {result}")
            return result
        except ZeroDivisionError as e:
            print(f"   除零错误: {e}")
            return float('inf')  # 返回无穷大
        except TypeError as e:
            print(f"   类型错误: {e}")
            return 0.0
        except Exception as e:
            print(f"   未知错误: {e}")
            return 0.0
    
    # 测试不同的异常情况
    test_cases = [
        (10, 2),      # 正常情况
        (10, 0),      # 除零异常
        (10, "abc"),  # 类型异常
    ]
    
    for a, b in test_cases:
        divide_numbers(a, b)
    print()
    
    # 2. try-except-else-finally示例
    print("2. try-except-else-finally示例")
    
    def read_file_content(filename: str) -> Optional[str]:
        """读取文件内容 - 完整异常处理"""
        file_handle = None
        try:
            print(f"   尝试打开文件: {filename}")
            file_handle = open(filename, 'r', encoding='utf-8')
            content = file_handle.read()
            print(f"   成功读取文件，内容长度: {len(content)}")
            return content
            
        except FileNotFoundError:
            print(f"   文件不存在: {filename}")
            return None
            
        except PermissionError:
            print(f"   没有权限访问文件: {filename}")
            return None
            
        except UnicodeDecodeError:
            print(f"   文件编码错误: {filename}")
            return None
            
        except Exception as e:
            print(f"   读取文件时发生未知错误: {e}")
            return None
            
        else:
            # 只有在没有异常时才执行
            print("   文件读取成功，没有发生异常")
            
        finally:
            # 无论是否有异常都会执行
            if file_handle and not file_handle.closed:
                file_handle.close()
                print("   文件已关闭")
            print("   清理工作完成")
    
    # 测试文件读取
    read_file_content("nonexistent.txt")
    print()
    
    # 3. 捕获多个异常
    print("3. 捕获多个异常")
    
    def process_user_input(user_input: str):
        """处理用户输入 - 多异常处理"""
        try:
            # 尝试将输入转换为数字
            number = int(user_input)
            
            # 尝试进行一些计算
            result = 100 / number
            
            # 尝试访问列表元素
            my_list = [1, 2, 3]
            element = my_list[number]
            
            print(f"   处理成功: {result}, 列表元素: {element}")
            
        except (ValueError, TypeError) as e:
            # 捕获多个异常类型
            print(f"   输入转换错误: {e}")
            
        except ZeroDivisionError:
            print("   不能除以零")
            
        except IndexError:
            print("   列表索引超出范围")
            
        except Exception as e:
            print(f"   处理过程中发生错误: {type(e).__name__}: {e}")
    
    # 测试不同输入
    test_inputs = ["2", "0", "10", "abc", "-1"]
    
    for user_input in test_inputs:
        print(f"   输入: '{user_input}'")
        process_user_input(user_input)
        print()


def demonstrate_exception_hierarchy():
    """
    演示异常层次结构
    Python vs Java异常体系
    """
    print("=== 异常层次结构 ===\n")
    
    print("Java异常层次:")
    print("   Throwable")
    print("   ├── Error (系统错误)")
    print("   └── Exception")
    print("       ├── RuntimeException (运行时异常)")
    print("       └── CheckedException (检查异常)")
    print()
    
    print("Python异常层次:")
    print("   BaseException")
    print("   ├── SystemExit")
    print("   ├── KeyboardInterrupt")
    print("   └── Exception")
    print("       ├── ArithmeticError")
    print("       ├── LookupError")
    print("       ├── ValueError")
    print("       ├── TypeError")
    print("       └── ...")
    print()
    
    # 1. 常见异常类型演示
    print("1. 常见异常类型演示")
    
    def demonstrate_common_exceptions():
        """演示常见异常类型"""
        
        exceptions_demo = [
            # (异常代码, 异常类型, 描述)
            ("int('abc')", ValueError, "值错误"),
            ("'hello'[10]", IndexError, "索引错误"),
            ("{'a': 1}['b']", KeyError, "键错误"),
            ("int(None)", TypeError, "类型错误"),
            ("open('nonexistent.txt')", FileNotFoundError, "文件未找到"),
            ("10 / 0", ZeroDivisionError, "除零错误"),
        ]
        
        for code, expected_exception, description in exceptions_demo:
            try:
                print(f"   执行: {code}")
                eval(code)
            except expected_exception as e:
                print(f"   捕获{description}: {type(e).__name__}: {e}")
            except Exception as e:
                print(f"   意外异常: {type(e).__name__}: {e}")
            print()
    
    demonstrate_common_exceptions()
    
    # 2. 异常继承关系
    print("2. 异常继承关系示例")
    
    def check_exception_inheritance():
        """检查异常继承关系"""
        
        # 创建一些异常实例
        exceptions = [
            ValueError("值错误"),
            TypeError("类型错误"),
            IndexError("索引错误"),
            KeyError("键错误"),
            ZeroDivisionError("除零错误"),
        ]
        
        print("   异常类型检查:")
        for exc in exceptions:
            exc_type = type(exc)
            print(f"   {exc_type.__name__}:")
            print(f"     是Exception子类: {issubclass(exc_type, Exception)}")
            print(f"     是BaseException子类: {issubclass(exc_type, BaseException)}")
            
            # 检查特定继承关系
            if issubclass(exc_type, ArithmeticError):
                print(f"     是ArithmeticError子类")
            if issubclass(exc_type, LookupError):
                print(f"     是LookupError子类")
            print()
    
    check_exception_inheritance()


def demonstrate_custom_exceptions():
    """
    演示自定义异常
    """
    print("=== 自定义异常 ===\n")
    
    print("Java vs Python自定义异常:")
    print("Java:")
    print("   class CustomException extends Exception {")
    print("       public CustomException(String message) {")
    print("           super(message);")
    print("       }")
    print("   }")
    print()
    
    print("Python:")
    print("   class CustomException(Exception):")
    print("       def __init__(self, message):")
    print("           super().__init__(message)")
    print()
    
    # 1. 基本自定义异常
    print("1. 基本自定义异常")
    
    class ValidationError(Exception):
        """验证错误 - 基本自定义异常"""
        
        def __init__(self, message: str, field_name: Optional[str] = None):
            super().__init__(message)
            self.field_name = field_name
            self.message = message
        
        def __str__(self):
            if self.field_name:
                return f"验证错误 [{self.field_name}]: {self.message}"
            return f"验证错误: {self.message}"
    
    class BusinessLogicError(Exception):
        """业务逻辑错误"""
        
        def __init__(self, message: str, error_code: int = 0):
            super().__init__(message)
            self.error_code = error_code
            self.message = message
        
        def __str__(self):
            return f"业务错误 [Code: {self.error_code}]: {self.message}"
    
    # 2. 复杂自定义异常
    print("2. 复杂自定义异常")
    
    class DatabaseError(Exception):
        """数据库操作异常基类"""
        
        def __init__(self, message: str, query: Optional[str] = None):
            super().__init__(message)
            self.message = message
            self.query = query
    
    class ConnectionError(DatabaseError):
        """数据库连接异常"""
        
        def __init__(self, message: str, host: str, port: int):
            super().__init__(message)
            self.host = host
            self.port = port
        
        def __str__(self):
            return f"数据库连接错误 [{self.host}:{self.port}]: {self.message}"
    
    class QueryError(DatabaseError):
        """查询执行异常"""
        
        def __init__(self, message: str, query: str, line_number: Optional[int] = None):
            super().__init__(message, query)
            self.line_number = line_number
        
        def __str__(self):
            base_msg = f"查询错误: {self.message}"
            if self.line_number:
                base_msg += f" (行号: {self.line_number})"
            if self.query:
                base_msg += f"\n查询语句: {self.query}"
            return base_msg
    
    # 3. 使用自定义异常
    print("3. 使用自定义异常")
    
    def validate_user_data(name: str, age: int, email: str):
        """用户数据验证 - 抛出自定义异常"""
        
        if not name or len(name.strip()) == 0:
            raise ValidationError("姓名不能为空", "name")
        
        if age < 0 or age > 150:
            raise ValidationError("年龄必须在0-150之间", "age")
        
        if "@" not in email:
            raise ValidationError("邮箱格式不正确", "email")
        
        print(f"   用户数据验证通过: {name}, {age}, {email}")
    
    def simulate_database_operation():
        """模拟数据库操作"""
        import random
        
        operation_type = random.choice(["connection", "query", "success"])
        
        if operation_type == "connection":
            raise ConnectionError("无法连接到数据库服务器", "localhost", 5432)
        elif operation_type == "query":
            raise QueryError(
                "SQL语法错误", 
                "SELECT * FROM users WHERE age = 'invalid'", 
                line_number=1
            )
        else:
            print("   数据库操作成功")
    
    # 测试自定义异常
    test_users = [
        ("张三", 25, "zhang@example.com"),  # 正常数据
        ("", 30, "test@example.com"),       # 姓名为空
        ("李四", -5, "li@example.com"),     # 年龄无效
        ("王五", 35, "invalid-email"),      # 邮箱无效
    ]
    
    for name, age, email in test_users:
        try:
            validate_user_data(name, age, email)
        except ValidationError as e:
            print(f"   {e}")
        print()
    
    # 测试数据库异常
    for i in range(3):
        try:
            simulate_database_operation()
        except DatabaseError as e:
            print(f"   {e}")
        print()


def demonstrate_exception_chaining():
    """
    演示异常链
    Python的raise from语法
    """
    print("=== 异常链 ===\n")
    
    print("Python异常链:")
    print("   try:")
    print("       # 可能失败的操作")
    print("   except LowLevelError as e:")
    print("       raise HighLevelError('高级错误') from e")
    print()
    
    print("   或者保留原始异常:")
    print("   except LowLevelError:")
    print("       raise HighLevelError('高级错误')")
    print()
    
    # 1. 异常链示例
    print("1. 异常链示例")
    
    class DataProcessingError(Exception):
        """数据处理错误"""
        pass
    
    class FileProcessingError(Exception):
        """文件处理错误"""
        pass
    
    def low_level_file_operation(filename: str):
        """底层文件操作 - 可能抛出异常"""
        if not filename.endswith('.txt'):
            raise ValueError(f"不支持的文件类型: {filename}")
        
        if 'missing' in filename:
            raise FileNotFoundError(f"文件不存在: {filename}")
        
        return f"文件内容: {filename}"
    
    def high_level_data_processing(filename: str):
        """高级数据处理 - 使用异常链"""
        try:
            content = low_level_file_operation(filename)
            # 模拟数据处理
            if 'error' in content:
                raise DataProcessingError("数据格式错误")
            return content.upper()
            
        except ValueError as e:
            # 明确的异常链
            raise FileProcessingError(f"文件格式不支持: {filename}") from e
            
        except FileNotFoundError as e:
            # 明确的异常链
            raise FileProcessingError(f"无法找到数据文件: {filename}") from e
            
        except DataProcessingError:
            # 重新抛出，保留原始异常链
            raise
    
    def process_multiple_files(filenames: list):
        """处理多个文件 - 隐式异常链"""
        results = []
        for filename in filenames:
            try:
                result = high_level_data_processing(filename)
                results.append(result)
            except FileProcessingError as e:
                # 包装异常但不破坏链
                raise Exception(f"批处理失败，文件: {filename}") from e
        return results
    
    # 测试异常链
    test_files = ["data.txt", "missing.txt", "data.pdf"]
    
    for filename in test_files:
        try:
            result = high_level_data_processing(filename)
            print(f"   处理成功: {result}")
        except Exception as e:
            print(f"   处理失败: {e}")
            # 打印异常链
            if e.__cause__:
                print(f"   原因: {e.__cause__}")
            if e.__context__ and e.__context__ is not e.__cause__:
                print(f"   上下文: {e.__context__}")
        print()


def demonstrate_exception_handling_best_practices():
    """
    演示异常处理最佳实践
    """
    print("=== 异常处理最佳实践 ===\n")
    
    # 1. 具体异常 vs 通用异常
    print("1. 具体异常 vs 通用异常")
    
    def bad_exception_handling(data: dict):
        """不好的异常处理 - 过于宽泛"""
        try:
            value = data['key']
            result = int(value) / 10
            return result
        except Exception:  # 太宽泛
            return None  # 丢失了错误信息
    
    def good_exception_handling(data: dict):
        """好的异常处理 - 具体明确"""
        try:
            value = data['key']
            result = int(value) / 10
            return result
        except KeyError:
            print("   错误: 缺少必需的键 'key'")
            return None
        except ValueError:
            print("   错误: 无法将值转换为整数")
            return None
        except ZeroDivisionError:
            print("   错误: 除零操作")
            return None
    
    test_data = [
        {'key': '20'},      # 正常情况
        {'other': '10'},    # 缺少键
        {'key': 'abc'},     # 值错误
        {'key': '0'},       # 除零错误
    ]
    
    for data in test_data:
        print(f"   测试数据: {data}")
        result = good_exception_handling(data)
        print(f"   结果: {result}")
        print()
    
    # 2. 资源管理和异常处理
    print("2. 资源管理和异常处理")
    
    class DatabaseConnection:
        """模拟数据库连接"""
        
        def __init__(self, db_name: str):
            self.db_name = db_name
            self.is_connected = False
        
        def connect(self):
            print(f"   连接到数据库: {self.db_name}")
            self.is_connected = True
        
        def execute_query(self, query: str):
            if not self.is_connected:
                raise RuntimeError("数据库未连接")
            
            if 'error' in query.lower():
                raise Exception("SQL执行错误")
            
            return f"查询结果: {query}"
        
        def close(self):
            if self.is_connected:
                print(f"   关闭数据库连接: {self.db_name}")
                self.is_connected = False
    
    # 不好的资源管理
    def bad_resource_management():
        """不好的资源管理"""
        db = DatabaseConnection("test_db")
        db.connect()
        try:
            result = db.execute_query("SELECT * FROM users")
            return result
        except Exception as e:
            print(f"   查询失败: {e}")
            return None
        # 如果异常发生，资源可能不会被释放
        db.close()
    
    # 好的资源管理 - 使用finally
    def good_resource_management_finally():
        """好的资源管理 - 使用finally"""
        db = DatabaseConnection("test_db")
        try:
            db.connect()
            result = db.execute_query("SELECT * FROM users")
            return result
        except Exception as e:
            print(f"   查询失败: {e}")
            return None
        finally:
            db.close()  # 确保资源被释放
    
    # 最好的资源管理 - 使用上下文管理器
    @contextmanager
    def database_connection(db_name: str):
        """数据库连接上下文管理器"""
        db = DatabaseConnection(db_name)
        try:
            db.connect()
            yield db
        finally:
            db.close()
    
    def best_resource_management():
        """最好的资源管理 - 使用上下文管理器"""
        try:
            with database_connection("test_db") as db:
                result = db.execute_query("SELECT * FROM users")
                return result
        except Exception as e:
            print(f"   查询失败: {e}")
            return None
    
    print("   测试资源管理:")
    result = best_resource_management()
    print(f"   查询结果: {result}")
    print()
    
    # 3. 日志记录和异常处理
    print("3. 日志记录和异常处理")
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    def process_data_with_logging(data: Any):
        """带日志记录的数据处理"""
        try:
            logger.info(f"开始处理数据: {type(data).__name__}")
            
            if not isinstance(data, (int, float)):
                raise TypeError(f"期望数字类型，得到 {type(data).__name__}")
            
            if data < 0:
                raise ValueError("数据不能为负数")
            
            result = data ** 2
            logger.info(f"数据处理成功: {data} -> {result}")
            return result
            
        except TypeError as e:
            logger.error(f"类型错误: {e}")
            raise
        except ValueError as e:
            logger.warning(f"值错误: {e}")
            raise
        except Exception as e:
            logger.critical(f"未知错误: {e}")
            # 记录详细的异常信息
            logger.debug("异常详情:", exc_info=True)
            raise
    
    # 测试带日志的异常处理
    test_values = [4, -2, "abc", 3.14]
    
    for value in test_values:
        try:
            result = process_data_with_logging(value)
            print(f"   处理结果: {result}")
        except Exception as e:
            print(f"   处理失败: {e}")
        print()


def main():
    """主函数 - 演示所有异常处理特性"""
    print("Python高级特性学习 - 异常处理机制")
    print("=" * 60)
    
    demonstrate_basic_exception_handling()
    demonstrate_exception_hierarchy()
    demonstrate_custom_exceptions()
    demonstrate_exception_chaining()
    demonstrate_exception_handling_best_practices()
    
    print("学习总结:")
    print("1. Python异常处理语法简洁，支持else和finally")
    print("2. 异常层次结构清晰，便于分类处理")
    print("3. 自定义异常提供业务相关的错误信息")
    print("4. 异常链帮助追踪错误根源")
    print("5. 合理的异常处理提高代码健壮性")
    print("6. 使用上下文管理器确保资源释放")
    print("7. 日志记录帮助问题诊断和调试")


if __name__ == "__main__":
    main() 