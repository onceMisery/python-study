# Python最佳实践指南 - Java开发者版

## 概述

本指南总结了Python开发的最佳实践，特别针对有Java背景的开发者，帮助建立Pythonic的编程思维。

---

## 代码风格和规范

### 1. PEP 8 代码规范

Python有官方的代码风格指南PEP 8，这与Java的代码规范有一些差异：

```python
# Python - PEP 8 风格
class UserService:  # 类名：大驼峰
    def __init__(self, db_connection):  # 方法名：蛇形命名
        self.db_connection = db_connection  # 变量名：蛇形命名
        self._cache = {}  # 受保护属性：单下划线
        self.__secret_key = "key"  # 私有属性：双下划线

    def get_user_by_id(self, user_id):  # 参数：蛇形命名
        """获取用户信息 - 文档字符串说明功能"""
        if user_id in self._cache:
            return self._cache[user_id]
        
        # 常量：全大写
        MAX_RETRY_COUNT = 3
        
        # 长行处理：在操作符前换行
        result = (self.db_connection
                 .select("users")
                 .where("id", user_id)
                 .first())
        
        return result
```

```java
// Java风格对比
public class UserService {  // 类名：大驼峰（相同）
    private DatabaseConnection dbConnection;  // 变量名：小驼峰
    private Map<String, User> cache;  // 私有变量：private关键字
    
    public User getUserById(String userId) {  // 方法名：小驼峰
        if (cache.containsKey(userId)) {
            return cache.get(userId);
        }
        
        final int MAX_RETRY_COUNT = 3;  // 常量：final关键字
        
        return dbConnection
            .select("users")
            .where("id", userId)
            .first();
    }
}
```

### 2. 导入规范

```python
# Python导入顺序（按PEP 8）
# 1. 标准库导入
import os
import sys
from datetime import datetime
from pathlib import Path

# 2. 第三方库导入
import requests
import pandas as pd
from flask import Flask, request

# 3. 本地应用导入
from myapp.models import User
from myapp.services import UserService
from . import config  # 相对导入

# 避免使用 import *
# from mymodule import *  # 不推荐

# 推荐明确导入
from mymodule import function1, function2, CLASS_NAME
```

### 3. 文档字符串规范

```python
def calculate_user_score(user_data, weights=None, include_bonus=True):
    """
    计算用户综合评分
    
    根据用户数据和权重计算综合评分，支持奖励分计算。
    这个函数实现了复杂的评分算法，考虑了多个维度的数据。
    
    Args:
        user_data (dict): 用户数据，包含各项评分指标
            - 'performance': 性能评分 (0-100)
            - 'attendance': 出勤评分 (0-100)
            - 'collaboration': 协作评分 (0-100)
        weights (dict, optional): 各指标权重。默认为None，使用标准权重
        include_bonus (bool): 是否包含奖励分。默认为True
    
    Returns:
        float: 综合评分 (0-100分制)
    
    Raises:
        ValueError: 当user_data格式不正确时
        KeyError: 当必要的评分指标缺失时
    
    Example:
        >>> user_data = {
        ...     'performance': 85,
        ...     'attendance': 95,
        ...     'collaboration': 78
        ... }
        >>> score = calculate_user_score(user_data)
        >>> print(f"用户评分: {score:.2f}")
        用户评分: 86.60
        
        >>> # 使用自定义权重
        >>> weights = {'performance': 0.5, 'attendance': 0.3, 'collaboration': 0.2}
        >>> score = calculate_user_score(user_data, weights=weights)
        >>> print(f"加权评分: {score:.2f}")
        加权评分: 84.40
    
    Note:
        该函数假设所有输入数据都在有效范围内。对于异常数据，
        建议在调用前进行数据清洗和验证。
    """
    if not isinstance(user_data, dict):
        raise ValueError("user_data必须是字典类型")
    
    required_keys = ['performance', 'attendance', 'collaboration']
    missing_keys = [key for key in required_keys if key not in user_data]
    if missing_keys:
        raise KeyError(f"缺少必要的评分指标: {missing_keys}")
    
    # 默认权重
    if weights is None:
        weights = {
            'performance': 0.4,
            'attendance': 0.3,
            'collaboration': 0.3
        }
    
    # 计算加权评分
    weighted_score = sum(
        user_data[key] * weights.get(key, 0) 
        for key in required_keys
    )
    
    # 添加奖励分
    if include_bonus and weighted_score >= 80:
        bonus = min(5, (weighted_score - 80) * 0.5)
        weighted_score += bonus
    
    return min(100, max(0, weighted_score))
```

---

## 错误处理最佳实践

### 1. 异常处理策略

```python
# 好的异常处理实践
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class UserNotFoundError(Exception):
    """用户未找到异常"""
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")

class DatabaseConnectionError(Exception):
    """数据库连接异常"""
    pass

def get_user_safely(user_id: str) -> Optional[dict]:
    """
    安全地获取用户信息
    
    Args:
        user_id: 用户ID
        
    Returns:
        用户信息字典，如果用户不存在返回None
        
    Raises:
        DatabaseConnectionError: 数据库连接失败时
    """
    try:
        # 具体的数据库操作
        user = database.get_user(user_id)
        if user is None:
            logger.warning(f"User not found: {user_id}")
            return None
        
        logger.info(f"Successfully retrieved user: {user_id}")
        return user
        
    except DatabaseTimeoutError as e:
        # 记录具体错误，但转换为业务异常
        logger.error(f"Database timeout while fetching user {user_id}: {e}")
        raise DatabaseConnectionError("Database is currently unavailable") from e
        
    except Exception as e:
        # 记录未预期的错误
        logger.exception(f"Unexpected error while fetching user {user_id}")
        # 不要吞掉异常，重新抛出或转换
        raise DatabaseConnectionError("An unexpected error occurred") from e

def process_user_request(user_id: str) -> dict:
    """处理用户请求的主函数"""
    try:
        user = get_user_safely(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        
        return {"status": "success", "user": user}
        
    except UserNotFoundError:
        # 业务异常，返回友好错误信息
        return {"status": "error", "message": "User not found"}
        
    except DatabaseConnectionError:
        # 系统异常，返回通用错误信息
        return {"status": "error", "message": "Service temporarily unavailable"}
```

### 2. 资源管理

```python
# 使用上下文管理器进行资源管理
import sqlite3
from contextlib import contextmanager
from typing import Generator

# 方式1：使用内置的with语句
def read_config_file(file_path: str) -> dict:
    """读取配置文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return json.loads(content)
    except FileNotFoundError:
        logger.error(f"Config file not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        return {}

# 方式2：自定义上下文管理器
@contextmanager
def database_transaction() -> Generator[sqlite3.Connection, None, None]:
    """数据库事务上下文管理器"""
    conn = sqlite3.connect('database.db')
    try:
        yield conn
        conn.commit()
        logger.info("Transaction committed successfully")
    except Exception as e:
        conn.rollback()
        logger.error(f"Transaction rolled back due to error: {e}")
        raise
    finally:
        conn.close()

# 使用自定义上下文管理器
def update_user_info(user_id: str, updates: dict) -> bool:
    """更新用户信息"""
    try:
        with database_transaction() as conn:
            cursor = conn.cursor()
            
            # 构建UPDATE语句
            set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
            query = f"UPDATE users SET {set_clause} WHERE id = ?"
            
            cursor.execute(query, list(updates.values()) + [user_id])
            
            if cursor.rowcount == 0:
                raise UserNotFoundError(user_id)
            
            return True
            
    except Exception as e:
        logger.error(f"Failed to update user {user_id}: {e}")
        return False
```

---

## 性能优化最佳实践

### 1. 列表和字典优化

```python
# 列表推导式 vs 传统循环
import time
from typing import List

def performance_comparison():
    """性能对比示例"""
    numbers = range(1000000)
    
    # 传统方式（较慢）
    start = time.time()
    result1 = []
    for n in numbers:
        if n % 2 == 0:
            result1.append(n * n)
    time1 = time.time() - start
    
    # 列表推导式（更快）
    start = time.time()
    result2 = [n * n for n in numbers if n % 2 == 0]
    time2 = time.time() - start
    
    # 生成器表达式（内存效率高）
    start = time.time()
    result3 = list(n * n for n in numbers if n % 2 == 0)
    time3 = time.time() - start
    
    print(f"传统循环: {time1:.3f}s")
    print(f"列表推导式: {time2:.3f}s")
    print(f"生成器表达式: {time3:.3f}s")

# 字典操作优化
def optimize_dictionary_operations():
    """字典操作优化示例"""
    # 使用get()方法替代键存在性检查
    user_scores = {'alice': 95, 'bob': 87}
    
    # 不推荐
    if 'charlie' in user_scores:
        score = user_scores['charlie']
    else:
        score = 0
    
    # 推荐
    score = user_scores.get('charlie', 0)
    
    # 使用setdefault()进行条件设置
    user_attempts = {}
    user_id = 'alice'
    
    # 不推荐
    if user_id not in user_attempts:
        user_attempts[user_id] = 0
    user_attempts[user_id] += 1
    
    # 推荐
    user_attempts.setdefault(user_id, 0)
    user_attempts[user_id] += 1
    
    # 或者使用defaultdict
    from collections import defaultdict
    user_attempts = defaultdict(int)
    user_attempts[user_id] += 1
```

### 2. 字符串操作优化

```python
# 字符串拼接优化
def string_concatenation_comparison():
    """字符串拼接性能对比"""
    words = ['hello', 'world', 'python', 'programming'] * 1000
    
    # 不推荐：使用+操作符（性能差）
    start = time.time()
    result1 = ''
    for word in words:
        result1 += word + ' '
    time1 = time.time() - start
    
    # 推荐：使用join()方法（性能好）
    start = time.time()
    result2 = ' '.join(words)
    time2 = time.time() - start
    
    # f-string格式化（推荐）
    name = "Alice"
    age = 25
    city = "Beijing"
    
    # 不推荐
    message1 = "Hello, " + name + "! You are " + str(age) + " years old and live in " + city
    
    # 推荐
    message2 = f"Hello, {name}! You are {age} years old and live in {city}"
    
    print(f"字符串拼接: {time1:.3f}s")
    print(f"join方法: {time2:.3f}s")
```

### 3. 函数和装饰器优化

```python
from functools import lru_cache, wraps
import time

# 使用缓存装饰器
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """使用缓存的斐波那契函数"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 自定义计时装饰器
def timing_decorator(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行时间: {end - start:.3f}s")
        return result
    return wrapper

# 条件装饰器
def conditional_decorator(condition):
    """条件装饰器"""
    def decorator(func):
        if condition:
            return timing_decorator(func)
        return func
    return decorator

# 使用示例
DEBUG = True

@conditional_decorator(DEBUG)
def complex_calculation(n: int) -> int:
    """复杂计算函数"""
    return sum(i**2 for i in range(n))
```

---

## 代码组织和架构最佳实践

### 1. 模块设计

```python
# 文件: models/user.py
"""
用户模型模块

本模块定义了用户相关的数据模型和业务逻辑。
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class UserStatus(Enum):
    """用户状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

@dataclass
class User:
    """
    用户数据模型
    
    使用dataclass装饰器自动生成__init__, __repr__, __eq__等方法
    """
    id: str
    username: str
    email: str
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = datetime.now()
    last_login: Optional[datetime] = None
    tags: List[str] = None
    
    def __post_init__(self):
        """初始化后处理"""
        if self.tags is None:
            self.tags = []
    
    @property
    def display_name(self) -> str:
        """显示名称"""
        return f"{self.username} ({self.email})"
    
    def is_active(self) -> bool:
        """检查用户是否活跃"""
        return self.status == UserStatus.ACTIVE
    
    def add_tag(self, tag: str) -> None:
        """添加标签"""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'tags': self.tags.copy()
        }
```

### 2. 服务层设计

```python
# 文件: services/user_service.py
"""
用户服务模块

提供用户相关的业务逻辑处理。
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from models.user import User, UserStatus
from repositories.user_repository import UserRepository
from utils.validators import EmailValidator, UsernameValidator
from utils.exceptions import ValidationError, UserNotFoundError

class UserServiceInterface(ABC):
    """用户服务接口"""
    
    @abstractmethod
    def create_user(self, username: str, email: str) -> User:
        """创建用户"""
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        """根据ID获取用户"""
        pass
    
    @abstractmethod
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> User:
        """更新用户信息"""
        pass

class UserService(UserServiceInterface):
    """用户服务实现"""
    
    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository
        self._email_validator = EmailValidator()
        self._username_validator = UsernameValidator()
    
    def create_user(self, username: str, email: str) -> User:
        """
        创建新用户
        
        Args:
            username: 用户名
            email: 邮箱地址
            
        Returns:
            创建的用户对象
            
        Raises:
            ValidationError: 输入数据验证失败
        """
        # 输入验证
        self._validate_user_input(username, email)
        
        # 检查用户名和邮箱唯一性
        if self._repository.exists_by_username(username):
            raise ValidationError(f"Username already exists: {username}")
        
        if self._repository.exists_by_email(email):
            raise ValidationError(f"Email already exists: {email}")
        
        # 创建用户
        user = User(
            id=self._generate_user_id(),
            username=username,
            email=email
        )
        
        # 保存到数据库
        saved_user = self._repository.save(user)
        
        # 记录日志
        logger.info(f"User created successfully: {saved_user.id}")
        
        return saved_user
    
    def get_user_by_id(self, user_id: str) -> User:
        """根据ID获取用户"""
        user = self._repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> User:
        """更新用户信息"""
        # 获取现有用户
        user = self.get_user_by_id(user_id)
        
        # 验证更新数据
        self._validate_updates(updates)
        
        # 应用更新
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        # 保存更新
        updated_user = self._repository.save(user)
        
        logger.info(f"User updated successfully: {user_id}")
        
        return updated_user
    
    def _validate_user_input(self, username: str, email: str) -> None:
        """验证用户输入"""
        if not self._username_validator.is_valid(username):
            raise ValidationError(f"Invalid username: {username}")
        
        if not self._email_validator.is_valid(email):
            raise ValidationError(f"Invalid email: {email}")
    
    def _validate_updates(self, updates: Dict[str, Any]) -> None:
        """验证更新数据"""
        allowed_fields = {'username', 'email', 'status', 'tags'}
        invalid_fields = set(updates.keys()) - allowed_fields
        
        if invalid_fields:
            raise ValidationError(f"Invalid update fields: {invalid_fields}")
    
    def _generate_user_id(self) -> str:
        """生成用户ID"""
        import uuid
        return str(uuid.uuid4())
```

### 3. 配置管理

```python
# 文件: config/settings.py
"""
应用配置管理

使用Pydantic进行配置验证和管理。
"""
from pydantic import BaseSettings, validator
from typing import List, Optional
import os

class DatabaseSettings(BaseSettings):
    """数据库配置"""
    host: str = "localhost"
    port: int = 5432
    username: str
    password: str
    database: str
    
    @validator('port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v
    
    @property
    def url(self) -> str:
        """数据库连接URL"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

class RedisSettings(BaseSettings):
    """Redis配置"""
    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None
    db: int = 0
    
    class Config:
        env_prefix = "REDIS_"

class AppSettings(BaseSettings):
    """应用主配置"""
    app_name: str = "Python Study App"
    debug: bool = False
    secret_key: str
    allowed_hosts: List[str] = ["localhost", "127.0.0.1"]
    
    # 子配置
    database: DatabaseSettings
    redis: RedisSettings
    
    # 日志配置
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError('Secret key must be at least 32 characters')
        return v
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"

# 配置实例
settings = AppSettings(
    database=DatabaseSettings(),
    redis=RedisSettings()
)

# 使用示例
def get_database_url() -> str:
    """获取数据库连接URL"""
    return settings.database.url

def is_debug_mode() -> bool:
    """检查是否为调试模式"""
    return settings.debug
```

---

## 测试最佳实践

### 1. 单元测试

```python
# 文件: tests/test_user_service.py
"""
用户服务测试

使用pytest进行单元测试。
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from services.user_service import UserService
from models.user import User, UserStatus
from utils.exceptions import ValidationError, UserNotFoundError

class TestUserService:
    """用户服务测试类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.mock_repository = Mock()
        self.user_service = UserService(self.mock_repository)
    
    def test_create_user_success(self):
        """测试成功创建用户"""
        # 准备测试数据
        username = "testuser"
        email = "test@example.com"
        
        # 配置mock
        self.mock_repository.exists_by_username.return_value = False
        self.mock_repository.exists_by_email.return_value = False
        self.mock_repository.save.return_value = User(
            id="test-id",
            username=username,
            email=email
        )
        
        # 执行测试
        result = self.user_service.create_user(username, email)
        
        # 验证结果
        assert result.username == username
        assert result.email == email
        assert result.status == UserStatus.ACTIVE
        
        # 验证调用
        self.mock_repository.exists_by_username.assert_called_once_with(username)
        self.mock_repository.exists_by_email.assert_called_once_with(email)
        self.mock_repository.save.assert_called_once()
    
    def test_create_user_duplicate_username(self):
        """测试创建重复用户名的用户"""
        # 配置mock
        self.mock_repository.exists_by_username.return_value = True
        
        # 执行测试并验证异常
        with pytest.raises(ValidationError, match="Username already exists"):
            self.user_service.create_user("existing_user", "test@example.com")
    
    def test_get_user_by_id_success(self):
        """测试成功获取用户"""
        user_id = "test-id"
        expected_user = User(id=user_id, username="test", email="test@example.com")
        
        self.mock_repository.find_by_id.return_value = expected_user
        
        result = self.user_service.get_user_by_id(user_id)
        
        assert result == expected_user
        self.mock_repository.find_by_id.assert_called_once_with(user_id)
    
    def test_get_user_by_id_not_found(self):
        """测试获取不存在的用户"""
        user_id = "nonexistent-id"
        self.mock_repository.find_by_id.return_value = None
        
        with pytest.raises(UserNotFoundError):
            self.user_service.get_user_by_id(user_id)
    
    @pytest.mark.parametrize("username,email,expected_error", [
        ("", "test@example.com", "Invalid username"),
        ("test", "invalid-email", "Invalid email"),
        ("a" * 51, "test@example.com", "Invalid username"),  # 假设用户名最大50字符
    ])
    def test_create_user_validation_errors(self, username, email, expected_error):
        """参数化测试：验证各种输入错误"""
        with pytest.raises(ValidationError, match=expected_error):
            self.user_service.create_user(username, email)

# 集成测试示例
class TestUserServiceIntegration:
    """用户服务集成测试"""
    
    @pytest.fixture
    def real_user_service(self, test_database):
        """真实的用户服务实例"""
        from repositories.user_repository import UserRepository
        repository = UserRepository(test_database)
        return UserService(repository)
    
    def test_full_user_lifecycle(self, real_user_service):
        """测试完整的用户生命周期"""
        # 创建用户
        user = real_user_service.create_user("integration_test", "test@integration.com")
        assert user.id is not None
        
        # 获取用户
        retrieved_user = real_user_service.get_user_by_id(user.id)
        assert retrieved_user.username == "integration_test"
        
        # 更新用户
        updates = {"username": "updated_user"}
        updated_user = real_user_service.update_user(user.id, updates)
        assert updated_user.username == "updated_user"
```

### 2. 测试配置

```python
# 文件: tests/conftest.py
"""
Pytest配置文件

定义测试的fixture和全局配置。
"""
import pytest
import tempfile
import os
from unittest.mock import Mock
import sqlite3

@pytest.fixture(scope="session")
def test_database():
    """测试数据库fixture"""
    # 创建临时数据库文件
    db_fd, db_path = tempfile.mkstemp()
    
    # 初始化数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建测试表
    cursor.execute('''
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    
    yield db_path
    
    # 清理
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def mock_logger():
    """模拟日志器"""
    return Mock()

@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """自动设置测试环境"""
    # 设置测试环境变量
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    
    # 禁用外部服务调用
    monkeypatch.setattr("requests.get", Mock())
    monkeypatch.setattr("requests.post", Mock())

# 自定义pytest标记
def pytest_configure(config):
    """配置自定义标记"""
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
```

---

## 安全最佳实践

### 1. 输入验证和清理

```python
import re
import html
from typing import Any, Dict
from utils.exceptions import ValidationError

class InputValidator:
    """输入验证器"""
    
    # 正则表达式模式
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,30}$')
    
    @classmethod
    def validate_email(cls, email: str) -> str:
        """验证邮箱格式"""
        if not email or not cls.EMAIL_PATTERN.match(email):
            raise ValidationError("Invalid email format")
        return email.lower().strip()
    
    @classmethod
    def validate_username(cls, username: str) -> str:
        """验证用户名格式"""
        if not username or not cls.USERNAME_PATTERN.match(username):
            raise ValidationError("Username must be 3-30 characters, alphanumeric and underscore only")
        return username.strip()
    
    @classmethod
    def sanitize_html(cls, text: str) -> str:
        """清理HTML内容"""
        if not text:
            return ""
        return html.escape(text.strip())
    
    @classmethod
    def validate_dict(cls, data: Dict[str, Any], required_fields: set, optional_fields: set = None) -> Dict[str, Any]:
        """验证字典数据"""
        if optional_fields is None:
            optional_fields = set()
        
        # 检查必需字段
        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            raise ValidationError(f"Missing required fields: {missing_fields}")
        
        # 检查额外字段
        allowed_fields = required_fields | optional_fields
        extra_fields = set(data.keys()) - allowed_fields
        if extra_fields:
            raise ValidationError(f"Unexpected fields: {extra_fields}")
        
        return data

# 密码安全
import bcrypt
import secrets

class PasswordManager:
    """密码管理器"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """哈希密码"""
        # 验证密码强度
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit")
        
        # 生成盐值并哈希
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """验证密码"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """生成安全令牌"""
        return secrets.token_urlsafe(length)
```

### 2. API安全

```python
from functools import wraps
from flask import request, jsonify, g
import jwt
from datetime import datetime, timedelta

class SecurityMiddleware:
    """安全中间件"""
    
    def __init__(self, app, secret_key: str):
        self.app = app
        self.secret_key = secret_key
        self.setup_middleware()
    
    def setup_middleware(self):
        """设置中间件"""
        @self.app.before_request
        def security_headers():
            """添加安全响应头"""
            pass
        
        @self.app.after_request
        def add_security_headers(response):
            """添加安全响应头"""
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            return response

def require_auth(f):
    """认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Missing authorization header'}), 401
        
        try:
            # 移除 "Bearer " 前缀
            if token.startswith('Bearer '):
                token = token[7:]
            
            # 验证JWT
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            g.current_user_id = payload['user_id']
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def rate_limit(max_requests: int = 100, window_seconds: int = 3600):
    """速率限制装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 实现速率限制逻辑
            client_ip = request.remote_addr
            # 使用Redis或内存缓存实现限制逻辑
            # ...
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

---

这个最佳实践指南涵盖了Python开发的核心方面，特别关注了与Java的差异。建议在实际开发中逐步采用这些实践，并根据项目需求进行调整。 