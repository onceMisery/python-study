#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python高级特性 - 自定义异常
==========================

本文件演示Python的自定义异常设计和实现
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

from typing import Dict, List, Optional, Any, Union
from enum import Enum
import json
import traceback
from datetime import datetime


def demonstrate_exception_design_patterns():
    """
    演示异常设计模式
    """
    print("=== 异常设计模式 ===\n")
    
    # 1. 分层异常设计
    print("1. 分层异常设计")
    
    class ApplicationError(Exception):
        """应用程序错误基类"""
        
        def __init__(self, message: str, error_code: Optional[str] = None):
            super().__init__(message)
            self.message = message
            self.error_code = error_code
            self.timestamp = datetime.now()
        
        def to_dict(self) -> Dict[str, Any]:
            """转换为字典格式"""
            return {
                'error_type': self.__class__.__name__,
                'message': self.message,
                'error_code': self.error_code,
                'timestamp': self.timestamp.isoformat()
            }
        
        def __str__(self) -> str:
            if self.error_code:
                return f"[{self.error_code}] {self.message}"
            return self.message
    
    class ValidationError(ApplicationError):
        """验证错误"""
        
        def __init__(self, message: str, field: Optional[str] = None, 
                     value: Any = None, error_code: str = "VALIDATION_ERROR"):
            super().__init__(message, error_code)
            self.field = field
            self.value = value
        
        def to_dict(self) -> Dict[str, Any]:
            data = super().to_dict()
            data.update({
                'field': self.field,
                'value': self.value
            })
            return data
    
    class BusinessLogicError(ApplicationError):
        """业务逻辑错误"""
        
        def __init__(self, message: str, operation: str, 
                     error_code: str = "BUSINESS_ERROR"):
            super().__init__(message, error_code)
            self.operation = operation
        
        def to_dict(self) -> Dict[str, Any]:
            data = super().to_dict()
            data['operation'] = self.operation
            return data
    
    class ExternalServiceError(ApplicationError):
        """外部服务错误"""
        
        def __init__(self, message: str, service_name: str, 
                     status_code: Optional[int] = None,
                     error_code: str = "EXTERNAL_SERVICE_ERROR"):
            super().__init__(message, error_code)
            self.service_name = service_name
            self.status_code = status_code
        
        def to_dict(self) -> Dict[str, Any]:
            data = super().to_dict()
            data.update({
                'service_name': self.service_name,
                'status_code': self.status_code
            })
            return data
    
    # 测试分层异常
    exceptions = [
        ValidationError("年龄必须大于0", field="age", value=-5),
        BusinessLogicError("余额不足", operation="withdraw"),
        ExternalServiceError("API调用失败", service_name="payment_service", status_code=500)
    ]
    
    for exc in exceptions:
        print(f"   异常: {exc}")
        print(f"   详情: {json.dumps(exc.to_dict(), indent=2, ensure_ascii=False)}")
        print()


def demonstrate_complex_exception_hierarchy():
    """
    演示复杂异常层次结构
    """
    print("=== 复杂异常层次结构 ===\n")
    
    # 1. HTTP异常体系
    print("1. HTTP异常体系")
    
    class HTTPError(Exception):
        """HTTP错误基类"""
        
        def __init__(self, message: str, status_code: int, 
                     headers: Optional[Dict[str, str]] = None):
            super().__init__(message)
            self.message = message
            self.status_code = status_code
            self.headers = headers or {}
        
        def __str__(self) -> str:
            return f"HTTP {self.status_code}: {self.message}"
    
    class ClientError(HTTPError):
        """4xx客户端错误"""
        pass
    
    class ServerError(HTTPError):
        """5xx服务器错误"""
        pass
    
    # 具体的4xx错误
    class BadRequestError(ClientError):
        """400错误"""
        
        def __init__(self, message: str = "Bad Request", 
                     validation_errors: Optional[List[str]] = None):
            super().__init__(message, 400)
            self.validation_errors = validation_errors or []
    
    class UnauthorizedError(ClientError):
        """401错误"""
        
        def __init__(self, message: str = "Unauthorized"):
            super().__init__(message, 401)
            self.headers = {'WWW-Authenticate': 'Bearer'}
    
    class ForbiddenError(ClientError):
        """403错误"""
        
        def __init__(self, message: str = "Forbidden", 
                     required_permission: Optional[str] = None):
            super().__init__(message, 403)
            self.required_permission = required_permission
    
    class NotFoundError(ClientError):
        """404错误"""
        
        def __init__(self, message: str = "Not Found", resource_type: str = "resource"):
            super().__init__(message, 404)
            self.resource_type = resource_type
    
    # 具体的5xx错误
    class InternalServerError(ServerError):
        """500错误"""
        
        def __init__(self, message: str = "Internal Server Error", 
                     original_exception: Optional[Exception] = None):
            super().__init__(message, 500)
            self.original_exception = original_exception
    
    class ServiceUnavailableError(ServerError):
        """503错误"""
        
        def __init__(self, message: str = "Service Unavailable", 
                     retry_after: Optional[int] = None):
            super().__init__(message, 503)
            if retry_after:
                self.headers['Retry-After'] = str(retry_after)
    
    # 2. 异常工厂
    print("2. 异常工厂")
    
    class HTTPExceptionFactory:
        """HTTP异常工厂"""
        
        _exception_map = {
            400: BadRequestError,
            401: UnauthorizedError,
            403: ForbiddenError,
            404: NotFoundError,
            500: InternalServerError,
            503: ServiceUnavailableError,
        }
        
        @classmethod
        def create_exception(cls, status_code: int, message: str, **kwargs) -> HTTPError:
            """根据状态码创建异常"""
            exception_class = cls._exception_map.get(status_code)
            
            if exception_class:
                return exception_class(message, **kwargs)
            elif 400 <= status_code < 500:
                return ClientError(message, status_code)
            elif 500 <= status_code < 600:
                return ServerError(message, status_code)
            else:
                return HTTPError(message, status_code)
    
    # 测试HTTP异常体系
    test_cases = [
        (400, "请求参数错误", {"validation_errors": ["age字段必填"]}),
        (401, "用户未认证"),
        (404, "用户不存在", {"resource_type": "user"}),
        (500, "数据库连接失败"),
        (503, "服务暂不可用", {"retry_after": 60}),
    ]
    
    for status_code, message, *args in test_cases:
        kwargs = args[0] if args else {}
        try:
            exception = HTTPExceptionFactory.create_exception(status_code, message, **kwargs)
            raise exception
        except HTTPError as e:
            print(f"   {e}")
            if hasattr(e, 'validation_errors') and e.validation_errors:
                print(f"   验证错误: {e.validation_errors}")
            if hasattr(e, 'required_permission') and e.required_permission:
                print(f"   需要权限: {e.required_permission}")
            if e.headers:
                print(f"   响应头: {e.headers}")
        print()


def demonstrate_exception_context():
    """
    演示异常上下文信息
    """
    print("=== 异常上下文信息 ===\n")
    
    # 1. 带上下文的异常
    print("1. 带上下文的异常")
    
    class ContextualError(Exception):
        """带上下文信息的异常"""
        
        def __init__(self, message: str, context: Optional[Dict[str, Any]] = None,
                     cause: Optional[Exception] = None):
            super().__init__(message)
            self.message = message
            self.context = context or {}
            self.cause = cause
            self.traceback_info = self._capture_traceback()
        
        def _capture_traceback(self) -> Dict[str, Any]:
            """捕获调用栈信息"""
            tb_info = traceback.extract_stack()[:-1]  # 排除当前frame
            return {
                'filename': tb_info[-1].filename,
                'function': tb_info[-1].name,
                'line_number': tb_info[-1].lineno,
                'code': tb_info[-1].line
            }
        
        def add_context(self, key: str, value: Any):
            """添加上下文信息"""
            self.context[key] = value
        
        def get_full_context(self) -> Dict[str, Any]:
            """获取完整上下文"""
            return {
                'message': self.message,
                'context': self.context,
                'traceback': self.traceback_info,
                'cause': str(self.cause) if self.cause else None
            }
        
        def __str__(self) -> str:
            base_msg = self.message
            if self.context:
                context_str = ', '.join(f"{k}={v}" for k, v in self.context.items())
                base_msg += f" (Context: {context_str})"
            return base_msg
    
    class DataProcessingError(ContextualError):
        """数据处理错误"""
        
        def __init__(self, message: str, record_id: Optional[str] = None,
                     field_name: Optional[str] = None, **kwargs):
            context = kwargs.pop('context', {})
            if record_id:
                context['record_id'] = record_id
            if field_name:
                context['field_name'] = field_name
            super().__init__(message, context, **kwargs)
    
    # 2. 异常收集器
    print("2. 异常收集器")
    
    class ExceptionCollector:
        """异常收集器 - 收集多个异常"""
        
        def __init__(self):
            self.exceptions: List[Exception] = []
        
        def add_exception(self, exception: Exception):
            """添加异常"""
            self.exceptions.append(exception)
        
        def has_exceptions(self) -> bool:
            """是否有异常"""
            return len(self.exceptions) > 0
        
        def raise_if_any(self):
            """如果有异常则抛出"""
            if self.has_exceptions():
                if len(self.exceptions) == 1:
                    raise self.exceptions[0]
                else:
                    raise MultipleExceptionsError(self.exceptions)
        
        def get_summary(self) -> Dict[str, Any]:
            """获取异常摘要"""
            return {
                'total_count': len(self.exceptions),
                'exception_types': [type(e).__name__ for e in self.exceptions],
                'messages': [str(e) for e in self.exceptions]
            }
    
    class MultipleExceptionsError(Exception):
        """多重异常错误"""
        
        def __init__(self, exceptions: List[Exception]):
            self.exceptions = exceptions
            messages = [str(e) for e in exceptions]
            super().__init__(f"发生了 {len(exceptions)} 个异常: {'; '.join(messages[:3])}")
        
        def __str__(self) -> str:
            if len(self.exceptions) <= 3:
                return f"多重异常: {'; '.join(str(e) for e in self.exceptions)}"
            else:
                first_three = '; '.join(str(e) for e in self.exceptions[:3])
                return f"多重异常 ({len(self.exceptions)}个): {first_three}..."
    
    # 测试带上下文的异常
    def process_user_records(records: List[Dict[str, Any]]):
        """处理用户记录 - 演示上下文异常"""
        collector = ExceptionCollector()
        
        for i, record in enumerate(records):
            try:
                # 验证必填字段
                if 'name' not in record:
                    error = DataProcessingError(
                        "缺少必填字段",
                        record_id=record.get('id', f'record_{i}'),
                        field_name='name'
                    )
                    error.add_context('record_index', i)
                    raise error
                
                # 验证数据类型
                if not isinstance(record.get('age'), int):
                    error = DataProcessingError(
                        "字段类型错误",
                        record_id=record.get('id', f'record_{i}'),
                        field_name='age'
                    )
                    error.add_context('expected_type', 'int')
                    error.add_context('actual_type', type(record.get('age')).__name__)
                    raise error
                
                print(f"   处理成功: {record}")
                
            except DataProcessingError as e:
                collector.add_exception(e)
                print(f"   处理失败: {e}")
                print(f"   详细上下文: {json.dumps(e.get_full_context(), indent=2, ensure_ascii=False)}")
        
        # 如果有异常，抛出收集的异常
        collector.raise_if_any()
    
    # 测试数据
    test_records = [
        {'id': 'user1', 'name': '张三', 'age': 25},
        {'id': 'user2', 'age': 30},  # 缺少name
        {'id': 'user3', 'name': '李四', 'age': '不是数字'},  # age类型错误
        {'id': 'user4', 'name': '王五', 'age': 35}
    ]
    
    try:
        process_user_records(test_records)
    except MultipleExceptionsError as e:
        print(f"\n   批处理结果: {e}")
    print()


def demonstrate_exception_retry_patterns():
    """
    演示异常重试模式
    """
    print("=== 异常重试模式 ===\n")
    
    # 1. 可重试异常
    print("1. 可重试异常")
    
    class RetryableError(Exception):
        """可重试异常基类"""
        
        def __init__(self, message: str, max_retries: int = 3, 
                     retry_delay: float = 1.0):
            super().__init__(message)
            self.message = message
            self.max_retries = max_retries
            self.retry_delay = retry_delay
            self.retry_count = 0
        
        def should_retry(self) -> bool:
            """是否应该重试"""
            return self.retry_count < self.max_retries
        
        def increment_retry(self):
            """增加重试次数"""
            self.retry_count += 1
        
        def get_next_delay(self) -> float:
            """获取下次重试延迟"""
            # 指数退避策略
            return self.retry_delay * (2 ** self.retry_count)
    
    class NetworkError(RetryableError):
        """网络错误"""
        
        def __init__(self, message: str, status_code: Optional[int] = None):
            super().__init__(message, max_retries=3, retry_delay=1.0)
            self.status_code = status_code
        
        def should_retry(self) -> bool:
            """网络错误重试逻辑"""
            if not super().should_retry():
                return False
            
            # 某些状态码不应该重试
            non_retryable_codes = [400, 401, 403, 404]
            if self.status_code in non_retryable_codes:
                return False
            
            return True
    
    class DatabaseError(RetryableError):
        """数据库错误"""
        
        def __init__(self, message: str, error_code: Optional[str] = None):
            super().__init__(message, max_retries=2, retry_delay=0.5)
            self.error_code = error_code
        
        def should_retry(self) -> bool:
            """数据库错误重试逻辑"""
            if not super().should_retry():
                return False
            
            # 某些错误不应该重试
            non_retryable_errors = ['SYNTAX_ERROR', 'AUTH_FAILED']
            if self.error_code in non_retryable_errors:
                return False
            
            return True
    
    # 2. 重试装饰器
    print("2. 重试装饰器")
    
    import time
    import random
    from functools import wraps
    
    def retry_on_exception(exception_types: tuple = (Exception,), 
                          max_retries: int = 3, delay: float = 1.0):
        """重试装饰器"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                
                for attempt in range(max_retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except exception_types as e:
                        last_exception = e
                        
                        if isinstance(e, RetryableError):
                            if not e.should_retry():
                                print(f"   异常不可重试: {e}")
                                raise
                            
                            e.increment_retry()
                            current_delay = e.get_next_delay()
                        else:
                            if attempt == max_retries:
                                raise
                            current_delay = delay * (2 ** attempt)
                        
                        print(f"   尝试 {attempt + 1} 失败: {e}")
                        if attempt < max_retries:
                            print(f"   等待 {current_delay:.1f} 秒后重试...")
                            time.sleep(current_delay)
                
                raise last_exception
            return wrapper
        return decorator
    
    # 3. 模拟网络请求
    print("3. 模拟网络请求")
    
    @retry_on_exception((NetworkError, DatabaseError), max_retries=3, delay=0.1)
    def simulate_network_request(url: str) -> str:
        """模拟网络请求"""
        print(f"   发送请求到: {url}")
        
        # 模拟随机失败
        failure_rate = 0.7
        if random.random() < failure_rate:
            error_type = random.choice(['network', 'server', 'timeout'])
            
            if error_type == 'network':
                raise NetworkError("网络连接失败")
            elif error_type == 'server':
                status_code = random.choice([500, 502, 503])
                raise NetworkError(f"服务器错误", status_code=status_code)
            else:
                raise NetworkError("请求超时")
        
        return f"成功响应来自 {url}"
    
    @retry_on_exception((DatabaseError,), max_retries=2, delay=0.1)
    def simulate_database_query(query: str) -> str:
        """模拟数据库查询"""
        print(f"   执行查询: {query}")
        
        # 模拟随机失败
        failure_rate = 0.6
        if random.random() < failure_rate:
            error_type = random.choice(['connection', 'lock', 'syntax'])
            
            if error_type == 'connection':
                raise DatabaseError("数据库连接失败", "CONNECTION_ERROR")
            elif error_type == 'lock':
                raise DatabaseError("表被锁定", "LOCK_TIMEOUT")
            else:
                raise DatabaseError("SQL语法错误", "SYNTAX_ERROR")  # 不可重试
        
        return f"查询结果: {query}"
    
    # 测试重试机制
    test_urls = ["http://api.example.com/users", "http://api.example.com/orders"]
    test_queries = ["SELECT * FROM users", "SELECT * FROM products"]
    
    for url in test_urls:
        try:
            result = simulate_network_request(url)
            print(f"   请求成功: {result}")
        except NetworkError as e:
            print(f"   请求最终失败: {e}")
        print()
    
    for query in test_queries:
        try:
            result = simulate_database_query(query)
            print(f"   查询成功: {result}")
        except DatabaseError as e:
            print(f"   查询最终失败: {e}")
        print()


def main():
    """主函数 - 演示所有自定义异常特性"""
    print("Python高级特性学习 - 自定义异常")
    print("=" * 50)
    
    demonstrate_exception_design_patterns()
    demonstrate_complex_exception_hierarchy()
    demonstrate_exception_context()
    demonstrate_exception_retry_patterns()
    
    print("学习总结:")
    print("1. 分层异常设计提供清晰的错误分类")
    print("2. 异常工厂模式简化异常创建")
    print("3. 上下文信息有助于问题诊断")
    print("4. 异常收集器处理批量操作错误")
    print("5. 重试模式提高系统容错性")
    print("6. 合理的异常设计提升代码质量")
    print("7. 异常应该携带足够的诊断信息")


if __name__ == "__main__":
    main() 