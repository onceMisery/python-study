"""
Python包结构设计详解
作者：Python学习项目
日期：2024-01-16

本文件演示Python包结构的设计原则和最佳实践
重点：包设计模式、__init__.py文件、包管理
"""

import os
import sys
from pathlib import Path
import importlib
import pkgutil
from typing import List, Dict, Any


def create_sample_package():
    """
    创建示例包结构
    """
    print("=== 创建示例包结构 ===")
    
    # 定义包结构
    package_files = {
        # 主包
        "myproject/__init__.py": '''"""
MyProject - 示例Python项目包
版本: 1.0.0
作者: Python学习项目

这是一个演示Python包结构的示例项目
"""

# 版本信息
__version__ = "1.0.0"
__author__ = "Python学习项目"
__email__ = "example@python-study.com"
__description__ = "Python包结构示例"

# 包级别导入
from .core import DataProcessor, ConfigManager
from .utils import logger, validator
from .api import RESTClient, APIError

# 定义公共API
__all__ = [
    # 核心功能
    "DataProcessor",
    "ConfigManager",
    
    # 工具函数
    "logger",
    "validator",
    
    # API客户端
    "RESTClient",
    "APIError",
    
    # 版本信息
    "__version__",
]

# 包级别配置
DEFAULT_CONFIG = {
    "debug": False,
    "log_level": "INFO",
    "api_timeout": 30
}

def get_version():
    """获取版本信息"""
    return __version__

def configure(config_dict: dict):
    """配置包级别设置"""
    DEFAULT_CONFIG.update(config_dict)
''',
        
        # 核心模块包
        "myproject/core/__init__.py": '''"""
核心功能模块
包含项目的主要业务逻辑
"""

from .processor import DataProcessor
from .config import ConfigManager
from .exceptions import CoreError, ValidationError

__all__ = [
    "DataProcessor",
    "ConfigManager", 
    "CoreError",
    "ValidationError"
]
''',
        
        "myproject/core/processor.py": '''"""
数据处理器模块
"""

import json
from typing import Dict, List, Any, Optional
from ..utils.logger import get_logger
from .exceptions import ValidationError

logger = get_logger(__name__)


class DataProcessor:
    """主要的数据处理器类"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化数据处理器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        logger.info(f"初始化DataProcessor: {self.config}")
    
    def process_data(self, data: Any) -> Dict[str, Any]:
        """
        处理数据的主要方法
        
        Args:
            data: 待处理的数据
            
        Returns:
            处理结果字典
            
        Raises:
            ValidationError: 当数据验证失败时
        """
        logger.debug(f"开始处理数据: {type(data)}")
        
        try:
            # 数据验证
            if not self._validate_input(data):
                raise ValidationError("输入数据验证失败")
            
            # 数据处理逻辑
            result = self._transform_data(data)
            
            logger.info("数据处理完成")
            return {
                "status": "success",
                "data": result,
                "metadata": {
                    "processor": self.__class__.__name__,
                    "config": self.config
                }
            }
            
        except Exception as e:
            logger.error(f"数据处理失败: {e}")
            raise
    
    def _validate_input(self, data: Any) -> bool:
        """验证输入数据"""
        # 简单验证示例
        return data is not None
    
    def _transform_data(self, data: Any) -> Any:
        """转换数据"""
        # 数据转换逻辑
        if isinstance(data, dict):
            return {k: str(v).upper() for k, v in data.items()}
        elif isinstance(data, list):
            return [str(item).upper() for item in data]
        else:
            return str(data).upper()
    
    def get_stats(self) -> Dict[str, Any]:
        """获取处理器统计信息"""
        return {
            "class": self.__class__.__name__,
            "config": self.config,
            "version": "1.0.0"
        }
''',
        
        "myproject/core/config.py": '''"""
配置管理模块
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self._config = {}
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        # 默认配置
        self._config = {
            "app_name": "MyProject",
            "version": "1.0.0",
            "debug": False,
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "myproject_db"
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
        
        # 从文件加载配置
        if self.config_file and Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self._config.update(file_config)
                logger.info(f"配置从文件加载: {self.config_file}")
            except Exception as e:
                logger.warning(f"配置文件加载失败: {e}")
        
        # 从环境变量加载配置
        self._load_from_env()
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        env_mappings = {
            "MYPROJECT_DEBUG": ("debug", bool),
            "MYPROJECT_DB_HOST": ("database.host", str),
            "MYPROJECT_DB_PORT": ("database.port", int),
            "MYPROJECT_LOG_LEVEL": ("logging.level", str),
        }
        
        for env_var, (config_key, value_type) in env_mappings.items():
            env_value = os.environ.get(env_var)
            if env_value:
                try:
                    if value_type == bool:
                        value = env_value.lower() in ('true', '1', 'yes', 'on')
                    elif value_type == int:
                        value = int(env_value)
                    else:
                        value = env_value
                    
                    self._set_nested_config(config_key, value)
                    logger.debug(f"从环境变量设置配置: {config_key} = {value}")
                except ValueError as e:
                    logger.warning(f"环境变量{env_var}值无效: {e}")
    
    def _set_nested_config(self, key: str, value: Any):
        """设置嵌套配置"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        config = self._config
        try:
            for k in keys:
                config = config[k]
            return config
        except KeyError:
            return default
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        self._set_nested_config(key, value)
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config.copy()
    
    def save(self, file_path: Optional[str] = None):
        """保存配置到文件"""
        target_file = file_path or self.config_file
        if target_file:
            try:
                with open(target_file, 'w', encoding='utf-8') as f:
                    json.dump(self._config, f, indent=2, ensure_ascii=False)
                logger.info(f"配置已保存到: {target_file}")
            except Exception as e:
                logger.error(f"保存配置失败: {e}")
                raise
''',
        
        "myproject/core/exceptions.py": '''"""
核心异常模块
"""


class CoreError(Exception):
    """核心模块基础异常"""
    pass


class ValidationError(CoreError):
    """数据验证异常"""
    
    def __init__(self, message: str, field: str = None):
        super().__init__(message)
        self.field = field
        self.message = message
    
    def __str__(self):
        if self.field:
            return f"验证错误 [{self.field}]: {self.message}"
        return f"验证错误: {self.message}"


class ConfigurationError(CoreError):
    """配置异常"""
    pass


class ProcessingError(CoreError):
    """处理异常"""
    pass
''',
        
        # 工具模块包
        "myproject/utils/__init__.py": '''"""
工具模块包
包含各种辅助工具和实用函数
"""

from .logger import get_logger, configure_logging
from .validator import validate_email, validate_url, DataValidator
from .helpers import retry, timer, cache_result

__all__ = [
    # 日志工具
    "get_logger",
    "configure_logging",
    
    # 验证工具
    "validate_email", 
    "validate_url",
    "DataValidator",
    
    # 辅助工具
    "retry",
    "timer", 
    "cache_result"
]

# 模块级别的工具
logger = get_logger(__name__)
validator = DataValidator()
''',
        
        "myproject/utils/logger.py": '''"""
日志工具模块
"""

import logging
import sys
from typing import Optional


# 全局日志配置
_loggers = {}


def get_logger(name: str) -> logging.Logger:
    """
    获取或创建日志器
    
    Args:
        name: 日志器名称
        
    Returns:
        配置好的日志器
    """
    if name not in _loggers:
        logger = logging.getLogger(name)
        if not logger.handlers:
            # 设置默认处理器
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        
        _loggers[name] = logger
    
    return _loggers[name]


def configure_logging(level: str = "INFO", 
                     format_string: Optional[str] = None,
                     filename: Optional[str] = None):
    """
    配置全局日志设置
    
    Args:
        level: 日志级别
        format_string: 日志格式
        filename: 日志文件名
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # 清除现有处理器
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 配置新的日志设置
    logging.basicConfig(
        level=numeric_level,
        format=format_string or '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=filename
    )
    
    # 更新所有已存在的日志器
    for logger in _loggers.values():
        logger.setLevel(numeric_level)


# 创建默认日志器
default_logger = get_logger("myproject")
''',
        
        "myproject/utils/validator.py": '''"""
数据验证工具模块
"""

import re
from typing import Any, List, Dict, Optional
from urllib.parse import urlparse


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_url(url: str) -> bool:
    """验证URL格式"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


class DataValidator:
    """数据验证器类"""
    
    def __init__(self):
        self.errors = []
    
    def validate_required(self, value: Any, field_name: str) -> bool:
        """验证必填字段"""
        if value is None or (isinstance(value, str) and not value.strip()):
            self.errors.append(f"{field_name} 是必填字段")
            return False
        return True
    
    def validate_type(self, value: Any, expected_type: type, field_name: str) -> bool:
        """验证数据类型"""
        if not isinstance(value, expected_type):
            self.errors.append(f"{field_name} 必须是 {expected_type.__name__} 类型")
            return False
        return True
    
    def validate_range(self, value: int, min_val: int, max_val: int, field_name: str) -> bool:
        """验证数值范围"""
        if not (min_val <= value <= max_val):
            self.errors.append(f"{field_name} 必须在 {min_val} 到 {max_val} 之间")
            return False
        return True
    
    def validate_length(self, value: str, min_len: int, max_len: int, field_name: str) -> bool:
        """验证字符串长度"""
        if not (min_len <= len(value) <= max_len):
            self.errors.append(f"{field_name} 长度必须在 {min_len} 到 {max_len} 之间")
            return False
        return True
    
    def validate_dict(self, data: Dict[str, Any], schema: Dict[str, Dict]) -> bool:
        """根据模式验证字典数据"""
        self.errors = []
        valid = True
        
        for field_name, rules in schema.items():
            value = data.get(field_name)
            
            # 检查必填字段
            if rules.get('required', False):
                if not self.validate_required(value, field_name):
                    valid = False
                    continue
            
            # 如果值为空且非必填，跳过其他验证
            if value is None:
                continue
            
            # 类型验证
            if 'type' in rules:
                if not self.validate_type(value, rules['type'], field_name):
                    valid = False
                    continue
            
            # 范围验证（针对数字）
            if 'range' in rules and isinstance(value, (int, float)):
                min_val, max_val = rules['range']
                if not self.validate_range(value, min_val, max_val, field_name):
                    valid = False
            
            # 长度验证（针对字符串）
            if 'length' in rules and isinstance(value, str):
                min_len, max_len = rules['length']
                if not self.validate_length(value, min_len, max_len, field_name):
                    valid = False
        
        return valid
    
    def get_errors(self) -> List[str]:
        """获取验证错误列表"""
        return self.errors.copy()
    
    def clear_errors(self):
        """清除错误列表"""
        self.errors = []
''',
        
        "myproject/utils/helpers.py": '''"""
辅助工具函数模块
"""

import time
import functools
from typing import Any, Callable, Dict


def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    重试装饰器
    
    Args:
        max_attempts: 最大尝试次数
        delay: 重试间隔（秒）
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                        continue
                    break
            
            # 所有尝试都失败，抛出最后一个异常
            raise last_exception
        
        return wrapper
    return decorator


def timer(func: Callable) -> Callable:
    """
    计时装饰器
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"{func.__name__} 执行时间: {execution_time:.4f} 秒")
        
        return result
    
    return wrapper


def cache_result(max_size: int = 128):
    """
    简单的结果缓存装饰器
    
    Args:
        max_size: 缓存最大大小
    """
    def decorator(func: Callable) -> Callable:
        cache: Dict[str, Any] = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            cache_key = str(args) + str(sorted(kwargs.items()))
            
            # 检查缓存
            if cache_key in cache:
                return cache[cache_key]
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            
            # 如果缓存已满，移除最旧的条目
            if len(cache) >= max_size:
                oldest_key = next(iter(cache))
                del cache[oldest_key]
            
            cache[cache_key] = result
            return result
        
        # 添加缓存管理方法
        wrapper.cache_clear = lambda: cache.clear()
        wrapper.cache_info = lambda: {"size": len(cache), "max_size": max_size}
        
        return wrapper
    
    return decorator
''',
        
        # API模块包
        "myproject/api/__init__.py": '''"""
API模块包
包含REST客户端和API相关功能
"""

from .client import RESTClient
from .exceptions import APIError, HTTPError, TimeoutError

__all__ = [
    "RESTClient",
    "APIError", 
    "HTTPError",
    "TimeoutError"
]
''',
        
        "myproject/api/client.py": '''"""
REST API客户端模块
"""

import json
import time
from typing import Dict, Any, Optional
from urllib.parse import urljoin
from ..utils.logger import get_logger
from .exceptions import APIError, HTTPError, TimeoutError

logger = get_logger(__name__)


class RESTClient:
    """REST API客户端"""
    
    def __init__(self, base_url: str, timeout: int = 30, api_key: str = None):
        """
        初始化REST客户端
        
        Args:
            base_url: API基础URL
            timeout: 请求超时时间（秒）
            api_key: API密钥
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.api_key = api_key
        self.session_headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'MyProject-Client/1.0.0'
        }
        
        if api_key:
            self.session_headers['Authorization'] = f'Bearer {api_key}'
        
        logger.info(f"初始化REST客户端: {base_url}")
    
    def _make_request(self, method: str, endpoint: str, 
                     data: Optional[Dict] = None,
                     params: Optional[Dict] = None,
                     headers: Optional[Dict] = None) -> Dict[str, Any]:
        """
        发送HTTP请求（模拟实现）
        
        Args:
            method: HTTP方法
            endpoint: API端点
            data: 请求数据
            params: URL参数
            headers: 额外的请求头
            
        Returns:
            响应数据
            
        Raises:
            APIError: API请求失败
            HTTPError: HTTP错误
            TimeoutError: 请求超时
        """
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))
        
        # 合并请求头
        request_headers = self.session_headers.copy()
        if headers:
            request_headers.update(headers)
        
        logger.debug(f"发送{method}请求到: {url}")
        
        try:
            # 模拟网络请求延迟
            time.sleep(0.1)
            
            # 模拟请求处理
            if method.upper() == 'GET':
                # 模拟GET响应
                response_data = {
                    "status": "success",
                    "data": {"message": f"GET {endpoint} 成功"},
                    "timestamp": time.time()
                }
            elif method.upper() == 'POST':
                # 模拟POST响应
                response_data = {
                    "status": "created",
                    "data": {"id": 123, "created": True},
                    "input": data
                }
            elif method.upper() == 'PUT':
                # 模拟PUT响应
                response_data = {
                    "status": "updated",
                    "data": {"id": 123, "updated": True},
                    "input": data
                }
            elif method.upper() == 'DELETE':
                # 模拟DELETE响应
                response_data = {
                    "status": "deleted",
                    "data": {"deleted": True}
                }
            else:
                response_data = {
                    "status": "success",
                    "method": method,
                    "endpoint": endpoint
                }
            
            logger.debug(f"请求成功: {response_data.get('status')}")
            return response_data
            
        except Exception as e:
            logger.error(f"请求失败: {e}")
            raise APIError(f"请求失败: {e}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None, 
           headers: Optional[Dict] = None) -> Dict[str, Any]:
        """发送GET请求"""
        return self._make_request('GET', endpoint, params=params, headers=headers)
    
    def post(self, endpoint: str, data: Optional[Dict] = None,
            headers: Optional[Dict] = None) -> Dict[str, Any]:
        """发送POST请求"""
        return self._make_request('POST', endpoint, data=data, headers=headers)
    
    def put(self, endpoint: str, data: Optional[Dict] = None,
           headers: Optional[Dict] = None) -> Dict[str, Any]:
        """发送PUT请求"""
        return self._make_request('PUT', endpoint, data=data, headers=headers)
    
    def delete(self, endpoint: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """发送DELETE请求"""
        return self._make_request('DELETE', endpoint, headers=headers)
    
    def set_auth_token(self, token: str):
        """设置认证令牌"""
        self.session_headers['Authorization'] = f'Bearer {token}'
        logger.info("认证令牌已更新")
    
    def get_client_info(self) -> Dict[str, Any]:
        """获取客户端信息"""
        return {
            "base_url": self.base_url,
            "timeout": self.timeout,
            "has_auth": "Authorization" in self.session_headers,
            "headers": self.session_headers.copy()
        }
''',
        
        "myproject/api/exceptions.py": '''"""
API异常模块
"""


class APIError(Exception):
    """API基础异常"""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
    
    def __str__(self):
        if self.status_code:
            return f"API错误 [{self.status_code}]: {self.message}"
        return f"API错误: {self.message}"


class HTTPError(APIError):
    """HTTP错误异常"""
    pass


class TimeoutError(APIError):
    """请求超时异常"""
    
    def __init__(self, message: str = "请求超时", timeout: int = None):
        super().__init__(message)
        self.timeout = timeout
    
    def __str__(self):
        if self.timeout:
            return f"请求超时 ({self.timeout}秒): {self.message}"
        return f"请求超时: {self.message}"


class AuthenticationError(APIError):
    """认证错误异常"""
    pass


class AuthorizationError(APIError):
    """授权错误异常"""
    pass
'''
    }
    
    # 创建所有文件
    created_files = []
    try:
        for file_path, content in package_files.items():
            full_path = Path(file_path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            created_files.append(file_path)
        
        print(f"✓ 成功创建 {len(created_files)} 个文件")
        return created_files
        
    except Exception as e:
        print(f"创建包结构失败: {e}")
        return []


def analyze_package_structure():
    """
    分析包结构
    """
    print("\n=== 包结构分析 ===")
    
    # 检查包结构
    package_root = Path("myproject")
    if not package_root.exists():
        print("包不存在，请先创建包结构")
        return
    
    print("包结构:")
    
    def print_tree(path: Path, prefix="", is_last=True):
        """递归打印目录树"""
        if path.name.startswith('.'):
            return
        
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{path.name}")
        
        if path.is_dir():
            children = list(path.iterdir())
            children.sort(key=lambda x: (x.is_file(), x.name))
            
            for i, child in enumerate(children):
                is_last_child = i == len(children) - 1
                child_prefix = prefix + ("    " if is_last else "│   ")
                print_tree(child, child_prefix, is_last_child)
    
    print_tree(package_root)
    
    # 分析__init__.py文件
    print("\n__init__.py文件分析:")
    init_files = list(package_root.rglob("__init__.py"))
    for init_file in init_files:
        relative_path = init_file.relative_to(package_root.parent)
        print(f"  {relative_path}")
        
        # 读取并分析内容
        try:
            content = init_file.read_text(encoding="utf-8")
            lines = content.strip().split('\n')
            non_empty_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
            print(f"    行数: {len(lines)}, 代码行: {len(non_empty_lines)}")
            
            # 检查__all__定义
            if '__all__' in content:
                print("    ✓ 定义了__all__")
            else:
                print("    ⚠ 未定义__all__")
            
            # 检查导入语句
            import_lines = [line for line in non_empty_lines if 'import' in line]
            if import_lines:
                print(f"    导入语句: {len(import_lines)}个")
        
        except Exception as e:
            print(f"    错误: {e}")


def demonstrate_package_usage():
    """
    演示包的使用
    """
    print("\n=== 包使用演示 ===")
    
    # 添加包路径
    package_parent = Path.cwd()
    if str(package_parent) not in sys.path:
        sys.path.insert(0, str(package_parent))
    
    try:
        # 1. 导入整个包
        print("1. 导入包:")
        import myproject
        print(f"   包版本: {myproject.get_version()}")
        print(f"   包描述: {myproject.__description__}")
        
        # 2. 使用包级别的API
        print("\n2. 包级别API:")
        print(f"   默认配置: {list(myproject.DEFAULT_CONFIG.keys())}")
        
        # 3. 导入并使用核心模块
        print("\n3. 核心模块使用:")
        from myproject.core import DataProcessor, ConfigManager
        
        # 创建处理器
        processor = DataProcessor({"mode": "demo"})
        test_data = {"name": "python", "type": "language"}
        result = processor.process_data(test_data)
        print(f"   处理结果: {result['status']}")
        print(f"   处理后数据: {result['data']}")
        
        # 配置管理
        config = ConfigManager()
        app_name = config.get("app_name")
        print(f"   应用名称: {app_name}")
        
        # 4. 工具模块使用
        print("\n4. 工具模块使用:")
        from myproject.utils import validator, logger
        
        # 数据验证
        schema = {
            "name": {"required": True, "type": str, "length": (1, 50)},
            "age": {"required": True, "type": int, "range": (0, 120)}
        }
        
        test_user_data = {"name": "张三", "age": 30}
        is_valid = validator.validate_dict(test_user_data, schema)
        print(f"   数据验证结果: {'通过' if is_valid else '失败'}")
        
        if not is_valid:
            print(f"   验证错误: {validator.get_errors()}")
        
        # 日志使用
        log = logger("demo")
        log.info("演示日志消息")
        
        # 5. API客户端使用
        print("\n5. API客户端使用:")
        from myproject.api import RESTClient
        
        client = RESTClient("https://api.example.com", api_key="demo_key")
        client_info = client.get_client_info()
        print(f"   客户端基础URL: {client_info['base_url']}")
        print(f"   是否有认证: {client_info['has_auth']}")
        
        # 模拟API调用
        try:
            response = client.get("/users")
            print(f"   API响应状态: {response['status']}")
        except Exception as e:
            print(f"   API调用错误: {e}")
        
        print("\n✓ 包使用演示完成")
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保包结构正确创建")
    except Exception as e:
        print(f"使用错误: {e}")


def package_design_principles():
    """
    包设计原则
    """
    print("\n=== 包设计原则 ===")
    
    print("1. 单一职责原则:")
    print("   - 每个模块应该只有一个改变的理由")
    print("   - 核心功能与工具功能分离")
    print("   - API功能独立成包")
    
    print("\n2. 依赖倒置原则:")
    print("   - 高层模块不应依赖低层模块")
    print("   - 都应该依赖于抽象")
    print("   - 抽象不应依赖于细节")
    
    print("\n3. 开放封闭原则:")
    print("   - 对扩展开放，对修改封闭")
    print("   - 使用__all__控制公共API")
    print("   - 私有模块以_开头")
    
    print("\n4. 接口分离原则:")
    print("   - 不应强迫客户依赖它们不使用的接口")
    print("   - 通过__init__.py暴露精简的API")
    print("   - 避免过大的模块")
    
    print("\n5. 包结构最佳实践:")
    practices = [
        "使用清晰的目录层次结构",
        "每个包都要有__init__.py",
        "定义__all__控制导出内容",
        "使用相对导入进行包内导入",
        "文档字符串说明模块用途",
        "异常类集中定义",
        "配置和常量分离",
        "工具函数模块化",
        "测试代码与源码分离",
        "版本信息集中管理"
    ]
    
    for i, practice in enumerate(practices, 1):
        print(f"   {i:2d}. {practice}")


def compare_with_java():
    """
    与Java包机制对比
    """
    print("\n=== 与Java包机制对比 ===")
    
    print("Python包结构 vs Java包结构:")
    
    comparison_table = [
        ("特性", "Python", "Java"),
        ("-" * 15, "-" * 25, "-" * 30),
        ("包声明", "__init__.py文件", "package声明语句"),
        ("目录结构", "目录名即包名", "目录名对应包名"),
        ("导入语法", "import package.module", "import package.ClassName"),
        ("访问控制", "约定（_前缀）", "关键字（private/public）"),
        ("包初始化", "__init__.py执行", "静态初始化块"),
        ("动态导入", "importlib模块", "Class.forName()"),
        ("相对导入", ". 和 .. 语法", "不支持"),
        ("命名空间", "支持命名空间包", "通过包名隔离"),
        ("版本管理", "__version__属性", "Manifest文件"),
        ("依赖管理", "requirements.txt", "Maven/Gradle"),
    ]
    
    for row in comparison_table:
        print(f"{row[0]:<15} | {row[1]:<25} | {row[2]:<30}")
    
    print("\n主要差异:")
    print("1. Python包更灵活，支持动态特性")
    print("2. Java包在编译时确定，运行时性能更好")
    print("3. Python的相对导入更方便包内组织")
    print("4. Java的访问控制更严格和明确")
    print("5. Python包可以包含可执行代码")
    print("6. Java包主要是命名空间概念")
    
    print("\n迁移建议:")
    migration_tips = [
        "将Java包的概念映射到Python目录结构",
        "Java类对应Python模块或类",
        "Java接口可以用抽象基类替代",
        "使用类型注解增强代码可读性",
        "合理使用__all__控制API暴露",
        "遵循PEP 8命名规范",
        "使用工具（如mypy）进行类型检查"
    ]
    
    for i, tip in enumerate(migration_tips, 1):
        print(f"{i}. {tip}")


def package_maintenance():
    """
    包维护和管理
    """
    print("\n=== 包维护和管理 ===")
    
    print("1. 版本管理:")
    print("   - 在__init__.py中定义__version__")
    print("   - 遵循语义化版本控制（SemVer）")
    print("   - 使用版本控制工具管理代码")
    
    print("\n2. 文档管理:")
    print("   - 每个模块包含文档字符串")
    print("   - 使用Sphinx生成API文档")
    print("   - README文件说明使用方法")
    
    print("\n3. 测试策略:")
    print("   - tests/目录存放测试代码")
    print("   - 测试覆盖核心功能")
    print("   - 集成测试验证包协作")
    
    print("\n4. 依赖管理:")
    print("   - requirements.txt列出依赖")
    print("   - setup.py定义包信息")
    print("   - 使用虚拟环境隔离依赖")
    
    print("\n5. 性能优化:")
    print("   - 延迟导入减少启动时间")
    print("   - 避免循环导入")
    print("   - 合理使用__slots__")
    
    # 检查包的健康状态
    print("\n6. 包健康检查:")
    package_root = Path("myproject")
    if package_root.exists():
        # 统计文件数量
        py_files = list(package_root.rglob("*.py"))
        init_files = list(package_root.rglob("__init__.py"))
        
        print(f"   Python文件数量: {len(py_files)}")
        print(f"   __init__.py文件数量: {len(init_files)}")
        
        # 检查空的__init__.py
        empty_inits = []
        for init_file in init_files:
            content = init_file.read_text(encoding="utf-8").strip()
            if not content or content.startswith('"""') and content.endswith('"""'):
                empty_inits.append(init_file)
        
        if empty_inits:
            print(f"   ⚠ 发现 {len(empty_inits)} 个空的__init__.py文件")
        else:
            print("   ✓ 所有__init__.py文件都有内容")
        
        # 检查导入语句
        import_issues = []
        for py_file in py_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                if "from . import" in content or "from .. import" in content:
                    # 有相对导入
                    pass
            except Exception:
                import_issues.append(py_file)
        
        if import_issues:
            print(f"   ⚠ 发现 {len(import_issues)} 个文件可能有导入问题")
        else:
            print("   ✓ 导入语句看起来正常")


def main():
    """主函数：演示包结构设计"""
    print("Python包结构设计详解")
    print("=" * 50)
    
    try:
        # 创建示例包
        created_files = create_sample_package()
        if created_files:
            # 分析包结构
            analyze_package_structure()
            
            # 演示包使用
            demonstrate_package_usage()
        
        # 设计原则说明
        package_design_principles()
        
        # 与Java对比
        compare_with_java()
        
        # 包维护
        package_maintenance()
        
        print("\n总结:")
        print("1. 良好的包结构是可维护代码的基础")
        print("2. __init__.py文件是Python包的关键")
        print("3. 合理的模块划分提高代码复用性")
        print("4. 相对导入简化包内依赖管理")
        print("5. 文档和测试是包的重要组成部分")
        
    except Exception as e:
        print(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 