#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python高级特性 - 异常与Java对比
==============================

本文件详细对比Python和Java的异常处理机制
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

from typing import Optional, List, Dict, Any, Callable
from contextlib import contextmanager
import logging
import traceback
import sys
from functools import wraps


def demonstrate_exception_syntax_comparison():
    """
    演示异常语法对比
    """
    print("=== 异常语法对比 ===\n")
    
    print("Java vs Python异常处理语法对比:")
    print()
    
    print("1. 基本异常处理")
    print("Java:")
    print("   try {")
    print("       int result = 10 / 0;")
    print("   } catch (ArithmeticException e) {")
    print("       System.out.println(\"除零错误: \" + e.getMessage());")
    print("   } catch (Exception e) {")
    print("       System.out.println(\"通用错误: \" + e.getMessage());")
    print("   } finally {")
    print("       System.out.println(\"清理代码\");")
    print("   }")
    print()
    
    print("Python:")
    print("   try:")
    print("       result = 10 / 0")
    print("   except ZeroDivisionError as e:")
    print("       print(f\"除零错误: {e}\")")
    print("   except Exception as e:")
    print("       print(f\"通用错误: {e}\")")
    print("   else:")
    print("       print(\"没有异常时执行\")")
    print("   finally:")
    print("       print(\"清理代码\")")
    print()
    
    # 实际示例
    def demonstrate_basic_exception():
        """演示基本异常处理"""
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            print(f"   Python除零错误: {e}")
        except Exception as e:
            print(f"   Python通用错误: {e}")
        else:
            print("   没有异常")
        finally:
            print("   Python清理代码执行")
    
    demonstrate_basic_exception()
    print()
    
    print("2. 多异常捕获")
    print("Java:")
    print("   catch (IOException | SQLException e) {")
    print("       // 处理多种异常")
    print("   }")
    print()
    
    print("Python:")
    print("   except (IOError, ValueError) as e:")
    print("       # 处理多种异常")
    print()
    
    def demonstrate_multiple_exceptions():
        """演示多异常捕获"""
        test_inputs = ["abc", "0", "valid"]
        
        for input_val in test_inputs:
            try:
                if input_val == "abc":
                    int(input_val)  # ValueError
                elif input_val == "0":
                    10 / int(input_val)  # ZeroDivisionError
                else:
                    print(f"   处理成功: {input_val}")
            except (ValueError, ZeroDivisionError) as e:
                print(f"   捕获异常 {type(e).__name__}: {e}")
    
    demonstrate_multiple_exceptions()
    print()


def demonstrate_exception_hierarchy_comparison():
    """
    演示异常层次结构对比
    """
    print("=== 异常层次结构对比 ===\n")
    
    print("Java异常层次:")
    print("   Throwable")
    print("   ├── Error (系统级错误，不应捕获)")
    print("   │   ├── OutOfMemoryError")
    print("   │   ├── StackOverflowError")
    print("   │   └── VirtualMachineError")
    print("   └── Exception")
    print("       ├── RuntimeException (运行时异常，不强制处理)")
    print("       │   ├── NullPointerException")
    print("       │   ├── IndexOutOfBoundsException")
    print("       │   ├── IllegalArgumentException")
    print("       │   └── ClassCastException")
    print("       └── CheckedException (检查异常，强制处理)")
    print("           ├── IOException")
    print("           ├── SQLException")
    print("           └── ClassNotFoundException")
    print()
    
    print("Python异常层次:")
    print("   BaseException")
    print("   ├── SystemExit (系统退出)")
    print("   ├── KeyboardInterrupt (键盘中断)")
    print("   ├── GeneratorExit (生成器退出)")
    print("   └── Exception (所有异常的基类)")
    print("       ├── ArithmeticError")
    print("       │   ├── ZeroDivisionError")
    print("       │   ├── OverflowError")
    print("       │   └── FloatingPointError")
    print("       ├── LookupError")
    print("       │   ├── IndexError")
    print("       │   └── KeyError")
    print("       ├── ValueError")
    print("       ├── TypeError")
    print("       ├── NameError")
    print("       ├── AttributeError")
    print("       └── OSError")
    print("           ├── FileNotFoundError")
    print("           ├── PermissionError")
    print("           └── ConnectionError")
    print()
    
    # 异常层次检查
    def check_exception_hierarchy():
        """检查异常层次关系"""
        print("Python异常层次关系检查:")
        
        exceptions_to_check = [
            (ZeroDivisionError, ArithmeticError),
            (IndexError, LookupError),
            (FileNotFoundError, OSError),
            (ValueError, Exception),
            (Exception, BaseException),
        ]
        
        for child, parent in exceptions_to_check:
            is_subclass = issubclass(child, parent)
            print(f"   {child.__name__} 是 {parent.__name__} 的子类: {is_subclass}")
        print()
    
    check_exception_hierarchy()


def demonstrate_checked_vs_unchecked():
    """
    演示检查异常 vs 非检查异常
    """
    print("=== 检查异常 vs 非检查异常 ===\n")
    
    print("Java异常分类:")
    print("1. CheckedException (检查异常)")
    print("   - 编译时必须处理")
    print("   - 方法签名中必须声明throws")
    print("   - 如: IOException, SQLException")
    print()
    
    print("2. RuntimeException (运行时异常)")
    print("   - 编译时可以不处理")
    print("   - 如: NullPointerException, IllegalArgumentException")
    print()
    
    print("Java示例:")
    print("   // 必须处理检查异常")
    print("   public void readFile() throws IOException {")
    print("       FileReader file = new FileReader(\"file.txt\");")
    print("   }")
    print()
    print("   // 可以不处理运行时异常")
    print("   public void divide(int a, int b) {")
    print("       int result = a / b; // 可能抛出ArithmeticException")
    print("   }")
    print()
    
    print("Python的方式:")
    print("   - 所有异常都是非检查异常")
    print("   - 不强制在方法签名中声明")
    print("   - 依赖文档和类型注解说明可能的异常")
    print()
    
    # Python异常声明示例
    def python_file_operation(filename: str) -> str:
        """
        读取文件内容
        
        Args:
            filename: 文件名
            
        Returns:
            文件内容
            
        Raises:
            FileNotFoundError: 文件不存在
            PermissionError: 没有读取权限
            UnicodeDecodeError: 文件编码错误
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"   文件不存在: {filename}")
            raise
        except PermissionError:
            print(f"   没有读取权限: {filename}")
            raise
        except UnicodeDecodeError:
            print(f"   文件编码错误: {filename}")
            raise
    
    def python_divide(a: int, b: int) -> float:
        """
        除法运算
        
        Args:
            a: 被除数
            b: 除数
            
        Returns:
            运算结果
            
        Raises:
            ZeroDivisionError: 除数为零
            TypeError: 参数类型错误
        """
        return a / b
    
    print("Python异常文档示例:")
    print(f"   文件操作函数文档:\n{python_file_operation.__doc__}")
    print(f"   除法函数文档:\n{python_divide.__doc__}")


def demonstrate_resource_management():
    """
    演示资源管理对比
    """
    print("=== 资源管理对比 ===\n")
    
    print("Java资源管理:")
    print("1. try-finally模式 (Java 6及以前):")
    print("   FileInputStream fis = null;")
    print("   try {")
    print("       fis = new FileInputStream(\"file.txt\");")
    print("       // 使用资源")
    print("   } finally {")
    print("       if (fis != null) {")
    print("           fis.close();")
    print("       }")
    print("   }")
    print()
    
    print("2. try-with-resources (Java 7+):")
    print("   try (FileInputStream fis = new FileInputStream(\"file.txt\")) {")
    print("       // 使用资源，自动关闭")
    print("   }")
    print()
    
    print("Python资源管理:")
    print("1. try-finally模式:")
    print("   f = None")
    print("   try:")
    print("       f = open('file.txt')")
    print("       # 使用资源")
    print("   finally:")
    print("       if f:")
    print("           f.close()")
    print()
    
    print("2. with语句 (推荐):")
    print("   with open('file.txt') as f:")
    print("       # 使用资源，自动关闭")
    print()
    
    # 1. 模拟资源类
    class Resource:
        """模拟资源类"""
        
        def __init__(self, name: str):
            self.name = name
            self.is_open = False
        
        def open(self):
            """打开资源"""
            print(f"   打开资源: {self.name}")
            self.is_open = True
        
        def use(self):
            """使用资源"""
            if not self.is_open:
                raise RuntimeError("资源未打开")
            print(f"   使用资源: {self.name}")
        
        def close(self):
            """关闭资源"""
            if self.is_open:
                print(f"   关闭资源: {self.name}")
                self.is_open = False
        
        def __enter__(self):
            """上下文管理器入口"""
            self.open()
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            """上下文管理器出口"""
            self.close()
            # 返回False表示不抑制异常
            return False
    
    # 2. try-finally模式
    print("Python try-finally模式示例:")
    resource = None
    try:
        resource = Resource("database_connection")
        resource.open()
        resource.use()
        # 模拟异常
        # raise ValueError("模拟错误")
    except Exception as e:
        print(f"   处理异常: {e}")
    finally:
        if resource:
            resource.close()
    print()
    
    # 3. with语句模式
    print("Python with语句模式示例:")
    try:
        with Resource("file_handle") as resource:
            resource.use()
            # 模拟异常
            # raise ValueError("模拟错误")
    except Exception as e:
        print(f"   处理异常: {e}")
    print()
    
    # 4. 上下文管理器装饰器
    @contextmanager
    def managed_resource(name: str):
        """上下文管理器装饰器示例"""
        resource = Resource(name)
        try:
            resource.open()
            yield resource
        finally:
            resource.close()
    
    print("contextmanager装饰器示例:")
    try:
        with managed_resource("network_connection") as resource:
            resource.use()
    except Exception as e:
        print(f"   处理异常: {e}")
    print()


def demonstrate_exception_chaining_comparison():
    """
    演示异常链对比
    """
    print("=== 异常链对比 ===\n")
    
    print("Java异常链:")
    print("   try {")
    print("       // 底层操作")
    print("   } catch (SQLException e) {")
    print("       throw new DataAccessException(\"数据访问失败\", e);")
    print("   }")
    print()
    
    print("Python异常链:")
    print("   try:")
    print("       # 底层操作")
    print("   except SQLException as e:")
    print("       raise DataAccessException('数据访问失败') from e")
    print()
    
    # 1. 自定义异常类
    class DataAccessException(Exception):
        """数据访问异常"""
        pass
    
    class BusinessLogicException(Exception):
        """业务逻辑异常"""
        pass
    
    # 2. 异常链示例
    def low_level_database_operation():
        """底层数据库操作"""
        raise ValueError("数据库连接失败")
    
    def mid_level_data_access():
        """中层数据访问"""
        try:
            low_level_database_operation()
        except ValueError as e:
            # 明确的异常链
            raise DataAccessException("数据访问层错误") from e
    
    def high_level_business_logic():
        """高层业务逻辑"""
        try:
            mid_level_data_access()
        except DataAccessException as e:
            # 隐式异常链
            raise BusinessLogicException("业务逻辑执行失败")
    
    print("Python异常链示例:")
    try:
        high_level_business_logic()
    except BusinessLogicException as e:
        print(f"   业务异常: {e}")
        print(f"   直接原因: {e.__cause__}")
        print(f"   上下文: {e.__context__}")
        
        # 打印完整的异常链
        print("   完整异常链:")
        current = e
        level = 0
        while current:
            print(f"     {'  ' * level}{type(current).__name__}: {current}")
            current = current.__cause__ or current.__context__
            level += 1
            if level > 10:  # 防止无限循环
                break
    print()


def demonstrate_exception_performance():
    """
    演示异常性能对比
    """
    print("=== 异常性能考虑 ===\n")
    
    print("Java异常性能:")
    print("   - 异常创建成本高 (需要填充堆栈跟踪)")
    print("   - 异常抛出/捕获影响JVM优化")
    print("   - 建议: 不要用异常控制正常流程")
    print()
    
    print("Python异常性能:")
    print("   - 异常相对轻量")
    print("   - 在某些情况下比条件检查更快")
    print("   - EAFP (Easier to Ask for Forgiveness than Permission)")
    print()
    
    import time
    
    # 1. LBYL vs EAFP 性能对比
    def lbyl_approach(data: Dict[str, Any], key: str):
        """Look Before You Leap 方式"""
        if key in data:
            return data[key]
        else:
            return None
    
    def eafp_approach(data: Dict[str, Any], key: str):
        """Easier to Ask for Forgiveness than Permission 方式"""
        try:
            return data[key]
        except KeyError:
            return None
    
    # 性能测试
    test_data = {'a': 1, 'b': 2, 'c': 3}
    test_keys = ['a', 'b', 'c', 'd', 'e'] * 1000  # 60% 命中率
    
    # LBYL测试
    start_time = time.time()
    for key in test_keys:
        lbyl_approach(test_data, key)
    lbyl_time = time.time() - start_time
    
    # EAFP测试
    start_time = time.time()
    for key in test_keys:
        eafp_approach(test_data, key)
    eafp_time = time.time() - start_time
    
    print(f"   LBYL方式耗时: {lbyl_time:.4f} 秒")
    print(f"   EAFP方式耗时: {eafp_time:.4f} 秒")
    print(f"   性能比较: EAFP是LBYL的 {eafp_time/lbyl_time:.2f} 倍")
    print()
    
    # 2. 异常vs返回码性能
    def error_by_exception(value: int):
        """使用异常处理错误"""
        if value < 0:
            raise ValueError("值不能为负数")
        return value * 2
    
    def error_by_return_code(value: int):
        """使用返回码处理错误"""
        if value < 0:
            return None, "值不能为负数"
        return value * 2, None
    
    test_values = list(range(-100, 101))  # 50% 错误率
    
    # 异常方式测试
    start_time = time.time()
    for value in test_values:
        try:
            result = error_by_exception(value)
        except ValueError:
            pass
    exception_time = time.time() - start_time
    
    # 返回码方式测试
    start_time = time.time()
    for value in test_values:
        result, error = error_by_return_code(value)
        if error:
            pass
    return_code_time = time.time() - start_time
    
    print(f"   异常方式耗时: {exception_time:.4f} 秒")
    print(f"   返回码方式耗时: {return_code_time:.4f} 秒")
    print(f"   性能比较: 异常是返回码的 {exception_time/return_code_time:.2f} 倍")
    print()


def demonstrate_logging_and_debugging():
    """
    演示日志和调试对比
    """
    print("=== 日志和调试对比 ===\n")
    
    print("Java异常日志:")
    print("   logger.error(\"操作失败\", e);")
    print("   e.printStackTrace();")
    print()
    
    print("Python异常日志:")
    print("   logging.exception(\"操作失败\")")
    print("   traceback.print_exc()")
    print()
    
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    def demonstrate_exception_logging():
        """演示异常日志记录"""
        
        def risky_operation(value: int):
            """可能出错的操作"""
            if value == 0:
                raise ZeroDivisionError("除零错误")
            elif value < 0:
                raise ValueError("负数错误")
            return 100 / value
        
        test_values = [10, 0, -5]
        
        for value in test_values:
            try:
                result = risky_operation(value)
                logger.info(f"操作成功: {value} -> {result}")
            except ZeroDivisionError:
                logger.exception(f"除零错误，输入值: {value}")
            except ValueError:
                logger.error(f"值错误，输入值: {value}", exc_info=True)
            except Exception as e:
                logger.critical(f"未知错误: {e}", exc_info=True)
    
    print("异常日志记录示例:")
    demonstrate_exception_logging()
    print()
    
    # 异常信息提取
    def extract_exception_info():
        """提取异常信息"""
        try:
            1 / 0
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            
            print("异常信息提取:")
            print(f"   异常类型: {exc_type.__name__}")
            print(f"   异常值: {exc_value}")
            print(f"   异常发生位置: {exc_traceback.tb_frame.f_code.co_filename}:{exc_traceback.tb_lineno}")
            
            # 格式化堆栈跟踪
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print("   堆栈跟踪:")
            for line in tb_lines:
                print(f"     {line.strip()}")
    
    extract_exception_info()


def main():
    """主函数 - 演示所有异常对比"""
    print("Python高级特性学习 - 异常与Java对比")
    print("=" * 60)
    
    demonstrate_exception_syntax_comparison()
    demonstrate_exception_hierarchy_comparison()
    demonstrate_checked_vs_unchecked()
    demonstrate_resource_management()
    demonstrate_exception_chaining_comparison()
    demonstrate_exception_performance()
    demonstrate_logging_and_debugging()
    
    print("学习总结:")
    print("1. Python异常语法更简洁，支持else子句")
    print("2. Python没有检查异常，所有异常都是运行时异常")
    print("3. Python的with语句类似Java的try-with-resources")
    print("4. Python异常链提供更清晰的错误追踪")
    print("5. Python的EAFP原则在某些场景下性能更好")
    print("6. Python的异常处理更加灵活和动态")
    print("7. Python的日志系统与异常处理结合更紧密")


if __name__ == "__main__":
    main() 