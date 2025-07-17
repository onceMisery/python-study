#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pytest测试框架详解
pytest Testing Framework Comprehensive Guide

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习pytest测试框架的测试编写、fixtures、参数化和与JUnit的对比

学习目标:
1. 掌握pytest的基本语法和测试编写
2. 理解fixtures的使用和依赖注入
3. 学会参数化测试和测试组织
4. 对比pytest与JUnit的设计差异

注意：pytest是Python生态中最强大的测试框架
"""

import pytest
import asyncio
import tempfile
import os
import json
import sqlite3
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import requests
import time


def demo_pytest_basics():
    """演示pytest基础语法"""
    print("=== 1. pytest基础语法 ===")
    
    basic_syntax = '''
# pytest基础测试示例

import pytest
from typing import List

# 1. 基本测试函数
def test_basic_assertion():
    """基本断言测试"""
    # 简单断言
    assert 1 + 1 == 2
    assert "hello" in "hello world"
    assert [1, 2, 3] == [1, 2, 3]
    
    # 布尔断言
    assert True
    assert not False
    
    # 比较断言
    assert 10 > 5
    assert "abc" < "def"

def test_exception_handling():
    """异常处理测试"""
    # 测试异常抛出
    with pytest.raises(ValueError):
        int("invalid")
    
    # 测试异常消息
    with pytest.raises(ValueError, match="invalid literal"):
        int("abc")
    
    # 捕获异常信息
    with pytest.raises(ZeroDivisionError) as exc_info:
        1 / 0
    
    assert "division by zero" in str(exc_info.value)

def test_approximate_comparison():
    """近似比较测试"""
    # 浮点数比较
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 0.1 + 0.2 == pytest.approx(0.3, rel=1e-9)
    assert 0.1 + 0.2 == pytest.approx(0.3, abs=1e-9)
    
    # 列表近似比较
    assert [0.1 + 0.2, 0.2 + 0.3] == pytest.approx([0.3, 0.5])

# 2. 测试类组织
class TestCalculator:
    """计算器测试类"""
    
    def test_addition(self):
        """加法测试"""
        calc = Calculator()
        assert calc.add(2, 3) == 5
        assert calc.add(-1, 1) == 0
        assert calc.add(0, 0) == 0
    
    def test_division(self):
        """除法测试"""
        calc = Calculator()
        assert calc.divide(10, 2) == 5
        assert calc.divide(7, 3) == pytest.approx(2.333, rel=1e-3)
        
        # 测试除零异常
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.divide(5, 0)
    
    def test_edge_cases(self):
        """边界条件测试"""
        calc = Calculator()
        
        # 大数处理
        large_num = 10**100
        assert calc.add(large_num, 1) == large_num + 1
        
        # 极小数处理
        tiny_num = 1e-10
        assert calc.multiply(tiny_num, 2) == pytest.approx(2e-10)

# 示例被测试类
class Calculator:
    """计算器类"""
    
    def add(self, a: float, b: float) -> float:
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# 3. 跳过和标记测试
@pytest.mark.skip(reason="功能尚未实现")
def test_future_feature():
    """未来功能测试"""
    pass

@pytest.mark.skipif(os.name == "nt", reason="不支持Windows")
def test_unix_specific():
    """Unix特定功能测试"""
    pass

@pytest.mark.slow
def test_slow_operation():
    """慢速测试"""
    time.sleep(0.1)  # 模拟慢速操作
    assert True

@pytest.mark.integration
def test_database_integration():
    """集成测试"""
    # 数据库集成测试代码
    pass

# 4. 自定义断言消息
def test_custom_assertion_message():
    """自定义断言消息"""
    expected = [1, 2, 3]
    actual = [1, 2, 4]
    
    # 虽然会失败，但提供了清晰的错误信息
    # assert actual == expected, f"Expected {expected}, but got {actual}"

# 5. 测试发现规则
# pytest会自动发现以下测试：
# - test_*.py 或 *_test.py 文件
# - Test* 类（不能有 __init__ 方法）
# - test_* 函数
# - test_* 方法

def test_pytest_discovery():
    """pytest测试发现示例"""
    assert True

class TestPytestDiscovery:
    """pytest测试发现类示例"""
    
    def test_method_discovery(self):
        """pytest方法发现示例"""
        assert True
'''
    
    print("pytest基础特点:")
    print("1. 简洁的assert语句，无需特殊断言方法")
    print("2. 自动测试发现，无需手动注册")
    print("3. 丰富的标记系统支持测试分类")
    print("4. 灵活的测试组织方式")
    print("5. 详细的失败信息和回溯")
    
    # JUnit基础对比
    junit_basics = '''
// JUnit基础语法对比

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.condition.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.*;

// 1. 基本测试类
public class CalculatorTest {
    
    private Calculator calculator;
    
    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }
    
    @Test
    @DisplayName("测试加法功能")
    void testAddition() {
        // 基本断言
        assertEquals(5, calculator.add(2, 3));
        assertEquals(0, calculator.add(-1, 1));
        assertEquals(0, calculator.add(0, 0));
        
        // 浮点数断言
        assertEquals(0.3, calculator.add(0.1, 0.2), 0.0001);
    }
    
    @Test
    void testDivision() {
        assertEquals(5.0, calculator.divide(10, 2));
        assertEquals(2.333, calculator.divide(7, 3), 0.001);
        
        // 异常测试
        Exception exception = assertThrows(
            IllegalArgumentException.class, 
            () -> calculator.divide(5, 0)
        );
        assertEquals("Cannot divide by zero", exception.getMessage());
    }
    
    @Test
    void testEdgeCases() {
        // 大数处理
        long largeNum = 1000000000000L;
        assertEquals(largeNum + 1, calculator.add(largeNum, 1));
        
        // 极小数处理
        double tinyNum = 1e-10;
        assertEquals(2e-10, calculator.multiply(tinyNum, 2), 1e-15);
    }
    
    // 2. 条件测试
    @Test
    @EnabledOnOs(OS.LINUX)
    @DisplayName("仅在Linux上运行")
    void testLinuxSpecific() {
        // Linux特定测试
    }
    
    @Test
    @DisabledOnOs(OS.WINDOWS)
    @DisplayName("在Windows上禁用")
    void testNonWindows() {
        // 非Windows测试
    }
    
    @Test
    @EnabledIfSystemProperty(named = "env", matches = "test")
    void testOnlyInTestEnvironment() {
        // 仅在测试环境运行
    }
    
    // 3. 参数化测试
    @ParameterizedTest
    @ValueSource(ints = {1, 2, 3, 5, 8, 13})
    @DisplayName("参数化测试示例")
    void testWithValueSource(int number) {
        assertTrue(number > 0);
        assertTrue(number < 20);
    }
    
    // 4. 分组测试
    @Nested
    @DisplayName("基本运算测试")
    class BasicOperationsTest {
        
        @Test
        void testAddition() {
            assertEquals(4, calculator.add(2, 2));
        }
        
        @Test
        void testSubtraction() {
            assertEquals(0, calculator.subtract(2, 2));
        }
    }
    
    @Nested
    @DisplayName("高级运算测试")
    class AdvancedOperationsTest {
        
        @Test
        void testPower() {
            assertEquals(8, calculator.power(2, 3));
        }
    }
    
    // 5. 生命周期管理
    @BeforeAll
    static void setUpClass() {
        // 类级别初始化
    }
    
    @AfterAll
    static void tearDownClass() {
        // 类级别清理
    }
    
    @BeforeEach
    void setUp() {
        // 每个测试前初始化
    }
    
    @AfterEach
    void tearDown() {
        // 每个测试后清理
    }
}

// 测试标签
@Tag("unit")
@Tag("fast")
public class UnitTest {
    
    @Test
    @Tag("smoke")
    void smokeTest() {
        assertTrue(true);
    }
}

@Tag("integration")
@Tag("slow")
public class IntegrationTest {
    
    @Test
    void integrationTest() {
        // 集成测试代码
    }
}
'''
    
    print(f"\n基础语法对比:")
    print("pytest:")
    print("- 简单的assert语句")
    print("- 函数式测试组织")
    print("- 标记装饰器")
    print("- 自动测试发现")
    
    print(f"\nJUnit 5:")
    print("- 丰富的断言方法")
    print("- 注解驱动测试")
    print("- 嵌套测试类")
    print("- 标签分类系统")
    print()


def demo_fixtures():
    """演示pytest fixtures"""
    print("=== 2. pytest Fixtures ===")
    
    fixtures_example = '''
# pytest fixtures详解

import pytest
import tempfile
import sqlite3
import json
from pathlib import Path
from typing import Generator, Dict, Any

# 1. 基本fixture
@pytest.fixture
def sample_data():
    """提供测试数据的fixture"""
    return {
        "users": [
            {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
            {"id": 2, "name": "李四", "email": "lisi@example.com"},
        ],
        "products": [
            {"id": 1, "name": "商品A", "price": 100.0},
            {"id": 2, "name": "商品B", "price": 200.0},
        ]
    }

def test_with_sample_data(sample_data):
    """使用sample_data fixture的测试"""
    assert len(sample_data["users"]) == 2
    assert sample_data["users"][0]["name"] == "张三"
    assert len(sample_data["products"]) == 2

# 2. Fixture作用域
@pytest.fixture(scope="function")  # 默认作用域，每个测试函数执行一次
def function_scoped_fixture():
    """函数作用域fixture"""
    print("\\n设置函数级fixture")
    yield "function_data"
    print("\\n清理函数级fixture")

@pytest.fixture(scope="class")  # 类作用域，每个测试类执行一次
def class_scoped_fixture():
    """类作用域fixture"""
    print("\\n设置类级fixture")
    yield "class_data"
    print("\\n清理类级fixture")

@pytest.fixture(scope="module")  # 模块作用域，每个模块执行一次
def module_scoped_fixture():
    """模块作用域fixture"""
    print("\\n设置模块级fixture")
    yield "module_data"
    print("\\n清理模块级fixture")

@pytest.fixture(scope="session")  # 会话作用域，整个测试会话执行一次
def session_scoped_fixture():
    """会话作用域fixture"""
    print("\\n设置会话级fixture")
    yield "session_data"
    print("\\n清理会话级fixture")

# 3. 自动使用fixture
@pytest.fixture(autouse=True)
def auto_fixture():
    """自动使用的fixture"""
    print("\\n自动执行的setup")
    yield
    print("\\n自动执行的teardown")

# 4. 参数化fixture
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_type(request):
    """参数化数据库类型fixture"""
    return request.param

@pytest.fixture
def database_connection(database_type):
    """基于数据库类型创建连接的fixture"""
    if database_type == "sqlite":
        conn = sqlite3.connect(":memory:")
    elif database_type == "postgresql":
        # 模拟PostgreSQL连接
        conn = MockConnection("postgresql")
    else:
        # 模拟MySQL连接
        conn = MockConnection("mysql")
    
    yield conn
    
    # 清理连接
    if hasattr(conn, 'close'):
        conn.close()

def test_database_operations(database_connection, database_type):
    """测试不同数据库操作"""
    print(f"\\n测试{database_type}数据库操作")
    assert database_connection is not None

# 5. 临时文件和目录fixture
@pytest.fixture
def temp_file():
    """临时文件fixture"""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as f:
        temp_path = Path(f.name)
        yield temp_path
    
    # 清理临时文件
    if temp_path.exists():
        temp_path.unlink()

@pytest.fixture
def temp_dir():
    """临时目录fixture"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

def test_file_operations(temp_file, temp_dir):
    """测试文件操作"""
    # 测试临时文件
    test_data = {"test": "data"}
    with open(temp_file, 'w') as f:
        json.dump(test_data, f)
    
    with open(temp_file, 'r') as f:
        loaded_data = json.load(f)
    
    assert loaded_data == test_data
    
    # 测试临时目录
    sub_file = temp_dir / "subfile.txt"
    sub_file.write_text("测试内容")
    assert sub_file.read_text() == "测试内容"

# 6. 复杂fixture依赖
@pytest.fixture
def database_schema(database_connection):
    """数据库模式fixture"""
    # 创建表结构
    if hasattr(database_connection, 'execute'):
        database_connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        database_connection.commit()
    
    yield database_connection
    
    # 清理数据
    if hasattr(database_connection, 'execute'):
        database_connection.execute('DROP TABLE IF EXISTS users')
        database_connection.commit()

@pytest.fixture
def sample_users(database_schema):
    """示例用户数据fixture"""
    users_data = [
        (1, "张三", "zhangsan@example.com"),
        (2, "李四", "lisi@example.com"),
        (3, "王五", "wangwu@example.com"),
    ]
    
    if hasattr(database_schema, 'executemany'):
        database_schema.executemany(
            'INSERT INTO users (id, name, email) VALUES (?, ?, ?)',
            users_data
        )
        database_schema.commit()
    
    yield users_data

def test_user_operations(sample_users, database_schema):
    """测试用户操作"""
    if hasattr(database_schema, 'execute'):
        cursor = database_schema.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        assert count == 3

# 7. 条件fixture
@pytest.fixture
def expensive_resource(request):
    """昂贵资源fixture"""
    if request.config.getoption("--skip-expensive"):
        pytest.skip("跳过昂贵资源测试")
    
    print("\\n创建昂贵资源")
    resource = ExpensiveResource()
    yield resource
    print("\\n清理昂贵资源")
    resource.cleanup()

# 8. 错误处理fixture
@pytest.fixture
def resilient_fixture():
    """具有错误处理的fixture"""
    resource = None
    try:
        resource = create_resource()
        yield resource
    except Exception as e:
        pytest.fail(f"Fixture setup failed: {e}")
    finally:
        if resource:
            try:
                resource.cleanup()
            except Exception:
                pass  # 静默清理错误

# 9. conftest.py中的共享fixture
# 在conftest.py文件中定义的fixture可以在同一目录及子目录的所有测试中使用

# conftest.py 示例内容
'''
import pytest
from myapp import create_app, db

@pytest.fixture(scope="session")
def app():
    """应用实例fixture"""
    app = create_app(testing=True)
    
    with app.app_context():
        yield app

@pytest.fixture(scope="session")
def client(app):
    """测试客户端fixture"""
    return app.test_client()

@pytest.fixture(scope="function")
def db_session(app):
    """数据库会话fixture"""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()
        db.drop_all()
'''

# 10. Fixture组合和工厂
@pytest.fixture
def user_factory():
    """用户工厂fixture"""
    created_users = []
    
    def create_user(name, email):
        user = User(name=name, email=email)
        created_users.append(user)
        return user
    
    yield create_user
    
    # 清理创建的用户
    for user in created_users:
        user.delete()

def test_multiple_users(user_factory):
    """测试多个用户"""
    user1 = user_factory("用户1", "user1@example.com")
    user2 = user_factory("用户2", "user2@example.com")
    
    assert user1.name == "用户1"
    assert user2.name == "用户2"

# 辅助类定义
class MockConnection:
    def __init__(self, db_type):
        self.db_type = db_type
    
    def close(self):
        pass

class ExpensiveResource:
    def cleanup(self):
        pass

def create_resource():
    return ExpensiveResource()

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def delete(self):
        pass
'''
    
    print("pytest fixtures特点:")
    print("1. 依赖注入式的测试数据准备")
    print("2. 多种作用域支持资源复用")
    print("3. 自动setup/teardown管理")
    print("4. 参数化fixture支持多场景测试")
    print("5. conftest.py实现fixture共享")
    print("6. 工厂模式支持动态资源创建")
    
    # JUnit fixtures对比
    junit_fixtures = '''
// JUnit fixture对比

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;

// 1. 基本生命周期
public class DatabaseTest {
    
    private static DatabaseConnection connection;
    private DatabaseTransaction transaction;
    
    @BeforeAll
    static void setUpClass() {
        // 类级别初始化（对应pytest session/module scope）
        connection = DatabaseConnection.create();
    }
    
    @AfterAll
    static void tearDownClass() {
        // 类级别清理
        if (connection != null) {
            connection.close();
        }
    }
    
    @BeforeEach
    void setUp() {
        // 每个测试前初始化（对应pytest function scope）
        transaction = connection.beginTransaction();
    }
    
    @AfterEach
    void tearDown() {
        // 每个测试后清理
        if (transaction != null) {
            transaction.rollback();
        }
    }
    
    @Test
    void testDatabaseOperation() {
        // 测试代码
        assertTrue(connection.isConnected());
    }
}

// 2. 参数化测试
@ParameterizedTest
@ValueSource(strings = {"postgresql", "mysql", "sqlite"})
void testWithDifferentDatabases(String databaseType) {
    DatabaseConnection conn = createConnection(databaseType);
    assertNotNull(conn);
    assertTrue(conn.isValid());
}

@ParameterizedTest
@CsvSource({
    "1, John, john@example.com",
    "2, Jane, jane@example.com",
    "3, Bob, bob@example.com"
})
void testUserCreation(int id, String name, String email) {
    User user = new User(id, name, email);
    assertEquals(id, user.getId());
    assertEquals(name, user.getName());
    assertEquals(email, user.getEmail());
}

// 3. 嵌套测试（类似pytest的测试类组织）
@Nested
@DisplayName("用户管理测试")
class UserManagementTest {
    
    private UserService userService;
    
    @BeforeEach
    void setUp() {
        userService = new UserService();
    }
    
    @Nested
    @DisplayName("用户创建测试")
    class UserCreationTest {
        
        @Test
        void shouldCreateValidUser() {
            User user = userService.createUser("张三", "zhangsan@example.com");
            assertNotNull(user);
            assertEquals("张三", user.getName());
        }
        
        @Test
        void shouldThrowExceptionForInvalidEmail() {
            assertThrows(IllegalArgumentException.class, 
                () -> userService.createUser("张三", "invalid-email"));
        }
    }
    
    @Nested
    @DisplayName("用户查询测试")
    class UserQueryTest {
        
        @BeforeEach
        void setUpUsers() {
            userService.createUser("用户1", "user1@example.com");
            userService.createUser("用户2", "user2@example.com");
        }
        
        @Test
        void shouldFindUserByEmail() {
            User user = userService.findByEmail("user1@example.com");
            assertNotNull(user);
            assertEquals("用户1", user.getName());
        }
    }
}

// 4. Spring Boot测试集成
@SpringBootTest
@ExtendWith(SpringExtension.class)
public class IntegrationTest {
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private TestEntityManager entityManager;
    
    @Test
    @Transactional
    void testUserRepository() {
        // Spring自动管理事务和数据库状态
        User user = new User("测试用户", "test@example.com");
        User saved = userRepository.save(user);
        
        assertNotNull(saved.getId());
        assertEquals("测试用户", saved.getName());
    }
}

// 5. 自定义扩展（类似pytest fixture）
public class DatabaseExtension implements BeforeEachCallback, AfterEachCallback {
    
    @Override
    public void beforeEach(ExtensionContext context) throws Exception {
        // 测试前设置数据库状态
        DatabaseTestUtils.setupTestData();
    }
    
    @Override
    public void afterEach(ExtensionContext context) throws Exception {
        // 测试后清理数据库
        DatabaseTestUtils.cleanupTestData();
    }
}

@ExtendWith(DatabaseExtension.class)
public class MyDatabaseTest {
    
    @Test
    void testWithCleanDatabase() {
        // 测试代码，数据库状态由扩展管理
    }
}
'''
    
    print(f"\nFixtures对比:")
    print("pytest:")
    print("- 函数参数注入方式")
    print("- 灵活的作用域控制")
    print("- yield语法支持清理")
    print("- 参数化fixture支持")
    
    print(f"\nJUnit 5:")
    print("- 注解生命周期管理")
    print("- 嵌套测试类组织")
    print("- 扩展机制提供高级功能")
    print("- 框架集成（如Spring Boot）")
    print()


def demo_parametrized_tests():
    """演示参数化测试"""
    print("=== 3. 参数化测试 ===")
    
    parametrized_example = '''
# pytest参数化测试详解

import pytest
import requests
from unittest.mock import Mock, patch

# 1. 基本参数化测试
@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (4, 8),
    (-1, -2),
    (0, 0),
])
def test_double_function(input_value, expected):
    """测试双倍函数"""
    assert double(input_value) == expected

def double(x):
    return x * 2

# 2. 多参数参数化
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (1, 1, 2),
    (-1, 1, 0),
    (0, 0, 0),
    (10, -5, 5),
])
def test_addition(a, b, expected):
    """测试加法函数"""
    calc = Calculator()
    assert calc.add(a, b) == expected

# 3. 字符串参数化
@pytest.mark.parametrize("email", [
    "user@example.com",
    "test.email@domain.co.uk",
    "user+tag@example.org",
    "123@numeric-domain.com",
])
def test_valid_emails(email):
    """测试有效邮箱"""
    assert is_valid_email(email) == True

@pytest.mark.parametrize("invalid_email", [
    "invalid-email",
    "@example.com",
    "user@",
    "user..double.dot@example.com",
    "",
])
def test_invalid_emails(invalid_email):
    """测试无效邮箱"""
    assert is_valid_email(invalid_email) == False

# 4. 复杂数据结构参数化
@pytest.mark.parametrize("user_data,expected_valid", [
    ({"name": "张三", "age": 25, "email": "zhangsan@example.com"}, True),
    ({"name": "李四", "age": 17, "email": "lisi@example.com"}, False),  # 年龄不足
    ({"name": "", "age": 30, "email": "empty@example.com"}, False),     # 姓名为空
    ({"name": "王五", "age": 35, "email": "invalid-email"}, False),     # 邮箱无效
    ({"name": "赵六", "age": -5, "email": "zhaoliu@example.com"}, False), # 年龄负数
])
def test_user_validation(user_data, expected_valid):
    """测试用户数据验证"""
    validator = UserValidator()
    assert validator.is_valid(user_data) == expected_valid

# 5. 使用IDs美化测试输出
@pytest.mark.parametrize("operation,a,b,expected", [
    ("add", 2, 3, 5),
    ("subtract", 5, 3, 2),
    ("multiply", 4, 3, 12),
    ("divide", 8, 2, 4),
], ids=["加法", "减法", "乘法", "除法"])
def test_calculator_operations(operation, a, b, expected):
    """测试计算器各种操作"""
    calc = Calculator()
    result = getattr(calc, operation)(a, b)
    assert result == expected

# 6. 动态参数生成
def generate_fibonacci_test_cases():
    """生成斐波那契数列测试用例"""
    cases = []
    fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    
    for i, expected in enumerate(fibonacci):
        cases.append((i, expected))
    
    return cases

@pytest.mark.parametrize("n,expected", generate_fibonacci_test_cases())
def test_fibonacci(n, expected):
    """测试斐波那契数列"""
    assert fibonacci(n) == expected

def fibonacci(n):
    """斐波那契数列实现"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 7. 条件参数化
@pytest.mark.parametrize("database_url", [
    "sqlite:///test.db",
    pytest.param("postgresql://localhost/test", marks=pytest.mark.skipif(
        not has_postgresql(), reason="PostgreSQL not available"
    )),
    pytest.param("mysql://localhost/test", marks=pytest.mark.skipif(
        not has_mysql(), reason="MySQL not available"
    )),
])
def test_database_connection(database_url):
    """测试数据库连接"""
    conn = create_connection(database_url)
    assert conn.is_connected()

def has_postgresql():
    """检查是否有PostgreSQL"""
    return os.getenv("POSTGRES_AVAILABLE") == "true"

def has_mysql():
    """检查是否有MySQL"""
    return os.getenv("MYSQL_AVAILABLE") == "true"

# 8. 嵌套参数化
@pytest.mark.parametrize("format_type", ["json", "xml", "csv"])
@pytest.mark.parametrize("data_size", ["small", "medium", "large"])
def test_data_export(format_type, data_size):
    """测试数据导出（格式×大小的组合）"""
    exporter = DataExporter()
    data = generate_test_data(data_size)
    result = exporter.export(data, format_type)
    
    assert result is not None
    assert validate_format(result, format_type)

# 9. 参数化类测试
@pytest.mark.parametrize("config", [
    {"host": "localhost", "port": 5432, "db": "test1"},
    {"host": "127.0.0.1", "port": 3306, "db": "test2"},
    {"host": "remote.server.com", "port": 1433, "db": "test3"},
])
class TestDatabaseConfigurations:
    """数据库配置测试类"""
    
    def test_connection(self, config):
        """测试连接"""
        conn = DatabaseConnection(config)
        assert conn.test_connection()
    
    def test_query_execution(self, config):
        """测试查询执行"""
        conn = DatabaseConnection(config)
        result = conn.execute("SELECT 1")
        assert result is not None

# 10. fixture与参数化组合
@pytest.fixture(params=["development", "testing", "production"])
def environment_config(request):
    """环境配置fixture"""
    configs = {
        "development": {"debug": True, "db_pool_size": 5},
        "testing": {"debug": True, "db_pool_size": 2},
        "production": {"debug": False, "db_pool_size": 20},
    }
    return configs[request.param]

@pytest.mark.parametrize("feature_flag", [True, False])
def test_feature_behavior(environment_config, feature_flag):
    """测试功能在不同环境和开关状态下的行为"""
    app = create_app(environment_config)
    app.set_feature_flag("new_feature", feature_flag)
    
    if feature_flag and not environment_config["debug"]:
        # 生产环境下启用新功能
        assert app.has_feature("new_feature")
    else:
        # 其他情况
        assert app.get_feature_status("new_feature") == feature_flag

# 11. 参数化测试的错误处理
@pytest.mark.parametrize("invalid_input,expected_exception", [
    ("", ValueError),
    (None, TypeError),
    (-1, ValueError),
    ("invalid", ValueError),
])
def test_input_validation_errors(invalid_input, expected_exception):
    """测试输入验证错误"""
    processor = DataProcessor()
    
    with pytest.raises(expected_exception):
        processor.process(invalid_input)

# 12. 跨平台参数化
@pytest.mark.parametrize("path,expected", [
    pytest.param("/unix/path", "/unix/path", marks=pytest.mark.skipif(
        os.name == "nt", reason="Unix path on Windows"
    )),
    pytest.param("C:\\\\Windows\\\\path", "C:\\\\Windows\\\\path", marks=pytest.mark.skipif(
        os.name != "nt", reason="Windows path on Unix"
    )),
    ("relative/path", "relative/path"),  # 相对路径在所有平台都测试
])
def test_path_handling(path, expected):
    """测试路径处理"""
    handler = PathHandler()
    result = handler.normalize_path(path)
    assert result == expected

# 辅助函数和类
def is_valid_email(email):
    """邮箱验证函数"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

class Calculator:
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b): return a / b

class UserValidator:
    def is_valid(self, user_data):
        return (user_data.get("name") and 
                user_data.get("age", 0) >= 18 and
                is_valid_email(user_data.get("email", "")))

class DataExporter:
    def export(self, data, format_type):
        return f"{format_type}_data"

def validate_format(result, format_type):
    return format_type in result

def generate_test_data(size):
    sizes = {"small": 10, "medium": 100, "large": 1000}
    return list(range(sizes.get(size, 10)))

def create_connection(url):
    return Mock(is_connected=lambda: True)

class DatabaseConnection:
    def __init__(self, config):
        self.config = config
    
    def test_connection(self):
        return True
    
    def execute(self, query):
        return "result"

def create_app(config):
    return Mock(
        has_feature=lambda x: True,
        set_feature_flag=lambda x, y: None,
        get_feature_status=lambda x: True
    )

class DataProcessor:
    def process(self, data):
        if data is None:
            raise TypeError("Data cannot be None")
        if not data:
            raise ValueError("Data cannot be empty")
        if isinstance(data, str) and data == "invalid":
            raise ValueError("Invalid data")
        if isinstance(data, int) and data < 0:
            raise ValueError("Data cannot be negative")
        return f"processed_{data}"

class PathHandler:
    def normalize_path(self, path):
        return path
'''
    
    print("参数化测试特点:")
    print("1. @pytest.mark.parametrize装饰器支持")
    print("2. 多种数据类型参数化")
    print("3. 动态参数生成")
    print("4. 条件参数化支持")
    print("5. 嵌套参数化实现组合测试")
    print("6. 与fixtures无缝结合")
    
    # JUnit参数化对比
    junit_parametrized = '''
// JUnit参数化测试对比

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;

public class ParameterizedTests {
    
    // 1. 简单值参数化
    @ParameterizedTest
    @ValueSource(ints = {1, 2, 3, 4, 5})
    void testWithValueSource(int number) {
        assertEquals(number * 2, double(number));
    }
    
    @ParameterizedTest
    @ValueSource(strings = {"user@example.com", "test@domain.org"})
    void testValidEmails(String email) {
        assertTrue(isValidEmail(email));
    }
    
    // 2. CSV参数化
    @ParameterizedTest
    @CsvSource({
        "2, 3, 5",
        "1, 1, 2", 
        "-1, 1, 0",
        "0, 0, 0"
    })
    void testAddition(int a, int b, int expected) {
        Calculator calc = new Calculator();
        assertEquals(expected, calc.add(a, b));
    }
    
    // 3. CSV文件参数化
    @ParameterizedTest
    @CsvFileSource(resources = "/test-data.csv", numLinesToSkip = 1)
    void testWithCsvFile(String name, int age, String email, boolean valid) {
        UserValidator validator = new UserValidator();
        User user = new User(name, age, email);
        assertEquals(valid, validator.isValid(user));
    }
    
    // 4. 方法源参数化
    @ParameterizedTest
    @MethodSource("provideCalculatorOperations")
    void testCalculatorOperations(String operation, int a, int b, int expected) {
        Calculator calc = new Calculator();
        int result = switch (operation) {
            case "add" -> calc.add(a, b);
            case "subtract" -> calc.subtract(a, b);
            case "multiply" -> calc.multiply(a, b);
            default -> throw new IllegalArgumentException("Unknown operation");
        };
        assertEquals(expected, result);
    }
    
    static Stream<Arguments> provideCalculatorOperations() {
        return Stream.of(
            Arguments.of("add", 2, 3, 5),
            Arguments.of("subtract", 5, 3, 2),
            Arguments.of("multiply", 4, 3, 12)
        );
    }
    
    // 5. 枚举参数化
    @ParameterizedTest
    @EnumSource(DatabaseType.class)
    void testDatabaseConnections(DatabaseType dbType) {
        DatabaseConnection conn = createConnection(dbType);
        assertNotNull(conn);
        assertTrue(conn.isConnected());
    }
    
    // 6. 条件参数化
    @ParameterizedTest
    @EnumSource(value = DatabaseType.class, 
                names = {"POSTGRESQL", "MYSQL"}, 
                mode = EnumSource.Mode.INCLUDE)
    void testSQLDatabases(DatabaseType dbType) {
        assertTrue(dbType.isSQL());
    }
    
    // 7. 复杂对象参数化
    @ParameterizedTest
    @MethodSource("provideUserTestCases")
    void testUserValidation(UserTestCase testCase) {
        UserValidator validator = new UserValidator();
        assertEquals(testCase.expectedValid, validator.isValid(testCase.user));
    }
    
    static Stream<UserTestCase> provideUserTestCases() {
        return Stream.of(
            new UserTestCase(new User("张三", 25, "zhangsan@example.com"), true),
            new UserTestCase(new User("李四", 17, "lisi@example.com"), false),
            new UserTestCase(new User("", 30, "empty@example.com"), false)
        );
    }
    
    // 8. 自定义参数源
    @ParameterizedTest
    @ArgumentsSource(FibonacciArgumentsProvider.class)
    void testFibonacci(int n, int expected) {
        assertEquals(expected, fibonacci(n));
    }
    
    static class FibonacciArgumentsProvider implements ArgumentsProvider {
        @Override
        public Stream<? extends Arguments> provideArguments(ExtensionContext context) {
            int[] fibonacci = {0, 1, 1, 2, 3, 5, 8, 13, 21, 34};
            return IntStream.range(0, fibonacci.length)
                          .mapToObj(i -> Arguments.of(i, fibonacci[i]));
        }
    }
    
    // 9. 动态测试（类似pytest的动态参数生成）
    @TestFactory
    Stream<DynamicTest> dynamicTestsForPrimeNumbers() {
        int[] primes = {2, 3, 5, 7, 11, 13, 17, 19, 23};
        
        return Arrays.stream(primes)
                    .mapToObj(prime -> 
                        DynamicTest.dynamicTest(
                            "Testing prime: " + prime,
                            () -> assertTrue(isPrime(prime))
                        )
                    );
    }
    
    // 10. 组合参数化（嵌套）
    @ParameterizedTest
    @CsvSource({
        "json, small",
        "json, large", 
        "xml, small",
        "xml, large",
        "csv, small",
        "csv, large"
    })
    void testDataExportCombinations(String format, String size) {
        DataExporter exporter = new DataExporter();
        TestData data = generateTestData(size);
        String result = exporter.export(data, format);
        
        assertNotNull(result);
        assertTrue(validateFormat(result, format));
    }
}

// 辅助类
record UserTestCase(User user, boolean expectedValid) {}

enum DatabaseType {
    POSTGRESQL(true), MYSQL(true), MONGODB(false), SQLITE(true);
    
    private final boolean isSQL;
    
    DatabaseType(boolean isSQL) {
        this.isSQL = isSQL;
    }
    
    public boolean isSQL() {
        return isSQL;
    }
}
'''
    
    print(f"\n参数化测试对比:")
    print("pytest:")
    print("- 装饰器式参数化")
    print("- Python数据结构直接支持")
    print("- 动态参数生成灵活")
    print("- 条件参数化简洁")
    
    print(f"\nJUnit 5:")
    print("- 多种参数源支持")
    print("- 类型安全的参数传递")
    print("- 自定义参数提供者")
    print("- 动态测试支持")
    print()


def main():
    """主函数：运行所有演示"""
    print("pytest测试框架完整学习指南")
    print("=" * 50)
    
    demo_pytest_basics()
    demo_fixtures()
    demo_parametrized_tests()
    
    print("学习总结:")
    print("1. pytest提供简洁直观的测试编写方式")
    print("2. fixtures机制支持灵活的测试资源管理")
    print("3. 参数化测试覆盖多种测试场景")
    print("4. 丰富的插件生态扩展测试能力")
    print("5. 与Python生态无缝集成")
    print("6. 相比JUnit更适合Python开发风格")


if __name__ == "__main__":
    main() 