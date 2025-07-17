#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试最佳实践详解
Testing Best Practices Guide

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习测试覆盖率、模拟技术、集成测试策略和企业级测试实践

学习目标:
1. 掌握测试覆盖率的监控和优化
2. 理解Mock和Stub的使用场景
3. 学会设计有效的集成测试策略
4. 了解企业级测试体系构建

注意：测试是保证代码质量的重要手段，需要系统性思考
"""

import pytest
import coverage
import unittest.mock as mock
from unittest.mock import Mock, MagicMock, patch, call
import requests
import asyncio
import json
import tempfile
import os
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging
import time
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
import docker
import psutil


def demo_test_coverage():
    """演示测试覆盖率最佳实践"""
    print("=== 1. 测试覆盖率最佳实践 ===")
    
    coverage_example = '''
# 测试覆盖率监控和优化

# 1. 使用coverage.py进行覆盖率测试
# 安装: pip install coverage pytest-cov

# 运行覆盖率测试的命令：
# pytest --cov=myproject --cov-report=html --cov-report=term-missing

# pytest.ini 配置文件
"""
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    --strict-markers
    --strict-config
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    smoke: marks tests as smoke tests
"""

# 2. .coveragerc 配置文件
"""
[run]
source = src
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */settings/*
    manage.py
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:

[html]
directory = htmlcov
"""

# 3. 覆盖率分析实用类
class CoverageAnalyzer:
    """覆盖率分析器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.cov = coverage.Coverage()
    
    def start_coverage(self):
        """开始覆盖率监控"""
        self.cov.start()
    
    def stop_coverage(self):
        """停止覆盖率监控"""
        self.cov.stop()
        self.cov.save()
    
    def generate_report(self):
        """生成覆盖率报告"""
        # 控制台报告
        print("\\n=== 覆盖率报告 ===")
        self.cov.report()
        
        # HTML报告
        self.cov.html_report(directory='htmlcov')
        print(f"HTML报告已生成到 htmlcov/ 目录")
        
        # JSON报告
        self.cov.json_report(outfile='coverage.json')
        
        return self.get_coverage_data()
    
    def get_coverage_data(self) -> Dict[str, Any]:
        """获取覆盖率数据"""
        with open('coverage.json', 'r') as f:
            data = json.load(f)
        
        return {
            'total_coverage': data['totals']['percent_covered'],
            'files': data['files'],
            'meta': data['meta']
        }
    
    def identify_uncovered_lines(self) -> Dict[str, List[int]]:
        """识别未覆盖的代码行"""
        uncovered = {}
        
        analysis = self.cov.analysis2
        for filename in self.cov.get_data().measured_files():
            _, _, missing_lines, _ = analysis(filename)
            if missing_lines:
                uncovered[filename] = missing_lines
        
        return uncovered
    
    def suggest_test_priorities(self) -> List[Dict[str, Any]]:
        """建议测试优先级"""
        coverage_data = self.get_coverage_data()
        suggestions = []
        
        for filename, file_data in coverage_data['files'].items():
            coverage_percent = file_data['summary']['percent_covered']
            
            if coverage_percent < 70:
                priority = "高"
            elif coverage_percent < 85:
                priority = "中"
            else:
                priority = "低"
            
            suggestions.append({
                'file': filename,
                'coverage': coverage_percent,
                'priority': priority,
                'missing_lines': len(file_data['missing_lines']),
                'reason': self._get_priority_reason(coverage_percent)
            })
        
        return sorted(suggestions, key=lambda x: x['coverage'])
    
    def _get_priority_reason(self, coverage: float) -> str:
        """获取优先级原因"""
        if coverage < 70:
            return "覆盖率过低，需要立即补充测试"
        elif coverage < 85:
            return "覆盖率中等，建议增加边界条件测试"
        else:
            return "覆盖率良好，可优化测试质量"

# 4. 覆盖率目标设定
class CoverageGoals:
    """覆盖率目标管理"""
    
    # 不同类型代码的覆盖率目标
    COVERAGE_TARGETS = {
        'business_logic': 95,    # 业务逻辑
        'api_endpoints': 90,     # API端点
        'data_access': 85,       # 数据访问层
        'utilities': 80,         # 工具函数
        'configuration': 70,     # 配置代码
        'ui_components': 75,     # UI组件
    }
    
    @classmethod
    def evaluate_coverage(cls, file_path: str, coverage: float) -> Dict[str, Any]:
        """评估文件覆盖率"""
        file_type = cls._classify_file(file_path)
        target = cls.COVERAGE_TARGETS.get(file_type, 80)
        
        return {
            'file': file_path,
            'type': file_type,
            'current_coverage': coverage,
            'target_coverage': target,
            'meets_target': coverage >= target,
            'gap': max(0, target - coverage),
            'status': cls._get_status(coverage, target)
        }
    
    @classmethod
    def _classify_file(cls, file_path: str) -> str:
        """分类文件类型"""
        path = Path(file_path)
        
        if 'service' in path.parts or 'business' in path.parts:
            return 'business_logic'
        elif 'api' in path.parts or 'endpoints' in path.parts:
            return 'api_endpoints'
        elif 'models' in path.parts or 'dao' in path.parts:
            return 'data_access'
        elif 'utils' in path.parts or 'helpers' in path.parts:
            return 'utilities'
        elif 'config' in path.parts or 'settings' in path.parts:
            return 'configuration'
        elif 'components' in path.parts or 'ui' in path.parts:
            return 'ui_components'
        else:
            return 'general'
    
    @classmethod
    def _get_status(cls, current: float, target: float) -> str:
        """获取覆盖率状态"""
        if current >= target:
            return "达标"
        elif current >= target * 0.9:
            return "接近"
        else:
            return "不足"

# 5. 覆盖率监控自动化
class CoverageMonitor:
    """覆盖率监控器"""
    
    def __init__(self):
        self.history = []
    
    def record_coverage(self, coverage_data: Dict[str, Any]):
        """记录覆盖率数据"""
        record = {
            'timestamp': time.time(),
            'total_coverage': coverage_data['total_coverage'],
            'file_count': len(coverage_data['files']),
            'files': coverage_data['files']
        }
        self.history.append(record)
    
    def analyze_trends(self) -> Dict[str, Any]:
        """分析覆盖率趋势"""
        if len(self.history) < 2:
            return {'trend': 'insufficient_data'}
        
        recent = self.history[-1]
        previous = self.history[-2]
        
        coverage_change = recent['total_coverage'] - previous['total_coverage']
        
        return {
            'trend': 'improving' if coverage_change > 0 else 'declining' if coverage_change < 0 else 'stable',
            'change': coverage_change,
            'current': recent['total_coverage'],
            'previous': previous['total_coverage'],
            'recommendation': self._get_trend_recommendation(coverage_change)
        }
    
    def _get_trend_recommendation(self, change: float) -> str:
        """获取趋势建议"""
        if change > 2:
            return "覆盖率显著提升，继续保持"
        elif change > 0:
            return "覆盖率有所提升，可进一步优化"
        elif change == 0:
            return "覆盖率保持稳定，关注测试质量"
        else:
            return "覆盖率下降，需要及时补充测试"
    
    def generate_coverage_dashboard(self) -> str:
        """生成覆盖率仪表板"""
        if not self.history:
            return "暂无覆盖率数据"
        
        latest = self.history[-1]
        trend = self.analyze_trends()
        
        dashboard = f"""
=== 覆盖率仪表板 ===
当前覆盖率: {latest['total_coverage']:.1f}%
文件数量: {latest['file_count']}
趋势: {trend.get('trend', 'unknown')}
变化: {trend.get('change', 0):+.1f}%
建议: {trend.get('recommendation', '无')}

=== 文件覆盖率分布 ===
"""
        
        # 文件覆盖率分布
        coverage_ranges = {
            '90-100%': 0, '80-89%': 0, '70-79%': 0, 
            '60-69%': 0, '50-59%': 0, '<50%': 0
        }
        
        for file_data in latest['files'].values():
            coverage = file_data['summary']['percent_covered']
            if coverage >= 90:
                coverage_ranges['90-100%'] += 1
            elif coverage >= 80:
                coverage_ranges['80-89%'] += 1
            elif coverage >= 70:
                coverage_ranges['70-79%'] += 1
            elif coverage >= 60:
                coverage_ranges['60-69%'] += 1
            elif coverage >= 50:
                coverage_ranges['50-59%'] += 1
            else:
                coverage_ranges['<50%'] += 1
        
        for range_name, count in coverage_ranges.items():
            dashboard += f"{range_name}: {count} 文件\\n"
        
        return dashboard

# 6. 使用示例
def coverage_example():
    """覆盖率使用示例"""
    analyzer = CoverageAnalyzer("./src")
    monitor = CoverageMonitor()
    
    # 开始覆盖率监控
    analyzer.start_coverage()
    
    try:
        # 运行被测试代码
        calculator = Calculator()
        result = calculator.add(2, 3)
        
    finally:
        # 停止监控并生成报告
        analyzer.stop_coverage()
        coverage_data = analyzer.generate_report()
        
        # 记录到监控器
        monitor.record_coverage(coverage_data)
        
        # 分析结果
        uncovered = analyzer.identify_uncovered_lines()
        priorities = analyzer.suggest_test_priorities()
        
        print(f"未覆盖代码行: {uncovered}")
        print(f"测试优先级建议: {priorities}")
        
        # 生成仪表板
        dashboard = monitor.generate_coverage_dashboard()
        print(dashboard)

class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b  # 这行可能未被测试覆盖
'''
    
    print("测试覆盖率最佳实践:")
    print("1. 设定合理的覆盖率目标（80-95%）")
    print("2. 关注行覆盖率、分支覆盖率和条件覆盖率")
    print("3. 定期监控覆盖率趋势变化")
    print("4. 优先测试业务核心逻辑")
    print("5. 覆盖率不是唯一指标，重视测试质量")
    
    # Java覆盖率对比
    java_coverage = '''
// Java测试覆盖率对比

// 1. JaCoCo配置（Maven）
/*
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.7</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
        <execution>
            <id>check</id>
            <goals>
                <goal>check</goal>
            </goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
*/

// 2. 覆盖率分析工具
@Component
public class CoverageAnalyzer {
    
    public CoverageReport analyzeCoverage(String reportPath) {
        // 解析JaCoCo报告
        File reportFile = new File(reportPath + "/jacoco.xml");
        
        try {
            DocumentBuilder builder = DocumentBuilderFactory.newInstance()
                    .newDocumentBuilder();
            Document doc = builder.parse(reportFile);
            
            NodeList packages = doc.getElementsByTagName("package");
            
            CoverageReport report = new CoverageReport();
            
            for (int i = 0; i < packages.getLength(); i++) {
                Element pkg = (Element) packages.item(i);
                String packageName = pkg.getAttribute("name");
                
                NodeList classes = pkg.getElementsByTagName("class");
                for (int j = 0; j < classes.getLength(); j++) {
                    Element cls = (Element) classes.item(j);
                    String className = cls.getAttribute("name");
                    
                    PackageCoverage pkgCov = report.getOrCreatePackage(packageName);
                    ClassCoverage clsCov = parseClassCoverage(cls);
                    pkgCov.addClass(clsCov);
                }
            }
            
            return report;
            
        } catch (Exception e) {
            throw new RuntimeException("Failed to parse coverage report", e);
        }
    }
    
    private ClassCoverage parseClassCoverage(Element classElement) {
        NodeList counters = classElement.getElementsByTagName("counter");
        
        ClassCoverage coverage = new ClassCoverage();
        coverage.setClassName(classElement.getAttribute("name"));
        
        for (int i = 0; i < counters.getLength(); i++) {
            Element counter = (Element) counters.item(i);
            String type = counter.getAttribute("type");
            int covered = Integer.parseInt(counter.getAttribute("covered"));
            int missed = Integer.parseInt(counter.getAttribute("missed"));
            
            switch (type) {
                case "LINE":
                    coverage.setLineCoverage(covered, missed);
                    break;
                case "BRANCH":
                    coverage.setBranchCoverage(covered, missed);
                    break;
                case "METHOD":
                    coverage.setMethodCoverage(covered, missed);
                    break;
            }
        }
        
        return coverage;
    }
}

// 3. 覆盖率质量门
@Component
public class CoverageQualityGate {
    
    private static final Map<String, Double> COVERAGE_THRESHOLDS = Map.of(
        "service", 0.90,
        "controller", 0.85, 
        "repository", 0.80,
        "util", 0.75,
        "config", 0.60
    );
    
    public QualityGateResult evaluate(CoverageReport report) {
        QualityGateResult result = new QualityGateResult();
        
        for (PackageCoverage pkg : report.getPackages()) {
            String packageType = classifyPackage(pkg.getName());
            double threshold = COVERAGE_THRESHOLDS.getOrDefault(packageType, 0.80);
            
            for (ClassCoverage cls : pkg.getClasses()) {
                double lineCoverage = cls.getLineCoverageRatio();
                
                if (lineCoverage < threshold) {
                    result.addViolation(new CoverageViolation(
                        cls.getClassName(),
                        lineCoverage,
                        threshold,
                        "Line coverage below threshold"
                    ));
                }
            }
        }
        
        result.setPassed(result.getViolations().isEmpty());
        return result;
    }
    
    private String classifyPackage(String packageName) {
        if (packageName.contains("service")) return "service";
        if (packageName.contains("controller")) return "controller";
        if (packageName.contains("repository")) return "repository";
        if (packageName.contains("util")) return "util";
        if (packageName.contains("config")) return "config";
        return "default";
    }
}

// 4. Gradle配置
/*
plugins {
    id 'jacoco'
}

jacoco {
    toolVersion = "0.8.7"
}

jacocoTestReport {
    reports {
        xml.enabled true
        html.enabled true
        csv.enabled false
    }
    
    afterEvaluate {
        classDirectories.setFrom(files(classDirectories.files.collect {
            fileTree(dir: it, exclude: [
                '**/*Application*',
                '**/*Config*',
                '**/dto/**',
                '**/entity/**'
            ])
        }))
    }
}

jacocoTestCoverageVerification {
    violationRules {
        rule {
            limit {
                counter = 'LINE'
                value = 'COVEREDRATIO'
                minimum = 0.80
            }
        }
        
        rule {
            limit {
                counter = 'BRANCH'
                value = 'COVEREDRATIO'
                minimum = 0.70
            }
        }
    }
}

check.dependsOn jacocoTestCoverageVerification
*/
'''
    
    print(f"\n覆盖率工具对比:")
    print("Python (coverage.py):")
    print("- 简单易用的配置")
    print("- 丰富的报告格式")
    print("- 灵活的排除规则")
    print("- pytest集成良好")
    
    print(f"\nJava (JaCoCo):")
    print("- 构建工具深度集成")
    print("- 多种覆盖率指标")
    print("- 质量门机制")
    print("- 企业级报告系统")
    print()


def demo_mocking_strategies():
    """演示Mock和测试替身策略"""
    print("=== 2. Mock和测试替身策略 ===")
    
    mocking_example = '''
# Mock和测试替身详解

from unittest.mock import Mock, MagicMock, patch, call, PropertyMock
from unittest.mock import AsyncMock, create_autospec, seal
import requests
import asyncio
from typing import Protocol

# 1. 基本Mock使用
def test_basic_mock():
    """基本Mock使用示例"""
    # 创建Mock对象
    mock_service = Mock()
    
    # 配置返回值
    mock_service.get_user.return_value = {"id": 1, "name": "张三"}
    
    # 使用Mock
    user = mock_service.get_user(1)
    assert user["name"] == "张三"
    
    # 验证调用
    mock_service.get_user.assert_called_once_with(1)
    mock_service.get_user.assert_called_with(1)

def test_magic_mock():
    """MagicMock使用示例"""
    # MagicMock支持魔法方法
    mock_obj = MagicMock()
    
    # 配置魔法方法
    mock_obj.__len__.return_value = 5
    mock_obj.__getitem__.return_value = "mocked_value"
    
    # 测试
    assert len(mock_obj) == 5
    assert mock_obj[0] == "mocked_value"
    
    # 验证调用
    mock_obj.__len__.assert_called_once()
    mock_obj.__getitem__.assert_called_with(0)

# 2. Mock配置和行为
class DatabaseService:
    """数据库服务（待测试）"""
    
    def __init__(self, connection):
        self.connection = connection
    
    def get_user_by_id(self, user_id: int) -> dict:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
    
    def create_user(self, user_data: dict) -> int:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user_data["name"], user_data["email"])
        )
        return cursor.lastrowid

def test_database_service_with_mock():
    """测试数据库服务Mock"""
    # 创建Mock连接
    mock_connection = Mock()
    mock_cursor = Mock()
    
    # 配置Mock行为
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {"id": 1, "name": "张三", "email": "zhangsan@example.com"}
    mock_cursor.lastrowid = 123
    
    # 测试服务
    service = DatabaseService(mock_connection)
    
    # 测试查询
    user = service.get_user_by_id(1)
    assert user["name"] == "张三"
    
    # 验证调用
    mock_connection.cursor.assert_called()
    mock_cursor.execute.assert_called_with("SELECT * FROM users WHERE id = ?", (1,))
    mock_cursor.fetchone.assert_called_once()
    
    # 测试创建
    user_data = {"name": "李四", "email": "lisi@example.com"}
    user_id = service.create_user(user_data)
    assert user_id == 123
    
    # 验证创建调用
    expected_call = call("INSERT INTO users (name, email) VALUES (?, ?)", ("李四", "lisi@example.com"))
    assert expected_call in mock_cursor.execute.call_args_list

# 3. 异常和边界情况Mock
def test_mock_exceptions():
    """测试Mock异常情况"""
    mock_service = Mock()
    
    # 配置抛出异常
    mock_service.risky_operation.side_effect = ValueError("模拟错误")
    
    # 测试异常处理
    with pytest.raises(ValueError, match="模拟错误"):
        mock_service.risky_operation()
    
    # 配置多次调用的不同返回值
    mock_service.unstable_operation.side_effect = [
        "success",
        ConnectionError("连接失败"),
        "success"
    ]
    
    # 第一次调用成功
    assert mock_service.unstable_operation() == "success"
    
    # 第二次调用抛异常
    with pytest.raises(ConnectionError):
        mock_service.unstable_operation()
    
    # 第三次调用又成功
    assert mock_service.unstable_operation() == "success"

# 4. 使用patch装饰器
@patch('requests.get')
def test_api_client_with_patch(mock_get):
    """使用patch测试API客户端"""
    # 配置Mock响应
    mock_response = Mock()
    mock_response.json.return_value = {"status": "success", "data": {"id": 1}}
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    # 测试API客户端
    client = ApiClient()
    result = client.get_user(1)
    
    assert result["status"] == "success"
    assert result["data"]["id"] == 1
    
    # 验证请求
    mock_get.assert_called_once_with("https://api.example.com/users/1")

class ApiClient:
    """API客户端"""
    
    def get_user(self, user_id: int) -> dict:
        response = requests.get(f"https://api.example.com/users/{user_id}")
        return response.json()

# 5. 上下文管理器patch
def test_with_patch_context():
    """使用patch上下文管理器"""
    with patch('builtins.open', mock.mock_open(read_data="file content")) as mock_file:
        # 测试文件操作
        with open("test.txt", "r") as f:
            content = f.read()
        
        assert content == "file content"
        mock_file.assert_called_once_with("test.txt", "r")

# 6. 属性Mock
def test_property_mock():
    """测试属性Mock"""
    mock_obj = Mock()
    
    # 使用PropertyMock
    type(mock_obj).status = PropertyMock(return_value="active")
    
    assert mock_obj.status == "active"
    
    # 验证属性访问
    type(mock_obj).status.assert_called_once()

# 7. 自动规范Mock (autospec)
class UserService:
    """用户服务接口"""
    
    def get_user(self, user_id: int) -> dict:
        pass
    
    def create_user(self, name: str, email: str) -> int:
        pass

def test_autospec_mock():
    """测试自动规范Mock"""
    # 创建符合规范的Mock
    mock_service = create_autospec(UserService)
    
    # 配置返回值
    mock_service.get_user.return_value = {"id": 1, "name": "张三"}
    
    # 正确的调用
    user = mock_service.get_user(1)
    assert user["name"] == "张三"
    
    # 错误的调用会被检测到
    try:
        mock_service.get_user("invalid_arg_type")  # 会在运行时报错
    except:
        pass

# 8. 异步Mock
async def test_async_mock():
    """测试异步Mock"""
    mock_async_service = AsyncMock()
    
    # 配置异步返回值
    mock_async_service.fetch_data.return_value = {"data": "async_result"}
    
    # 测试异步调用
    result = await mock_async_service.fetch_data()
    assert result["data"] == "async_result"
    
    # 验证异步调用
    mock_async_service.fetch_data.assert_called_once()

# 9. Mock封印 (sealing)
def test_sealed_mock():
    """测试封印Mock"""
    mock_obj = Mock()
    mock_obj.existing_method.return_value = "test"
    
    # 封印Mock，防止意外创建新属性
    seal(mock_obj)
    
    # 现有方法仍可使用
    assert mock_obj.existing_method() == "test"
    
    # 尝试访问新属性会报错
    try:
        _ = mock_obj.new_method  # 会抛出AttributeError
    except AttributeError:
        pass

# 10. 复杂Mock场景
class EmailService:
    """邮件服务"""
    
    def __init__(self, smtp_client):
        self.smtp_client = smtp_client
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        try:
            self.smtp_client.connect()
            self.smtp_client.send(to, subject, body)
            self.smtp_client.disconnect()
            return True
        except Exception:
            return False

def test_email_service_complex_mock():
    """复杂邮件服务Mock测试"""
    mock_smtp = Mock()
    
    # 测试成功场景
    email_service = EmailService(mock_smtp)
    result = email_service.send_email("test@example.com", "Test", "Body")
    
    assert result is True
    
    # 验证完整的调用序列
    expected_calls = [
        call.connect(),
        call.send("test@example.com", "Test", "Body"),
        call.disconnect()
    ]
    mock_smtp.assert_has_calls(expected_calls)
    
    # 重置Mock
    mock_smtp.reset_mock()
    
    # 测试失败场景
    mock_smtp.connect.side_effect = ConnectionError("SMTP连接失败")
    
    result = email_service.send_email("test@example.com", "Test", "Body")
    assert result is False
    
    # 只应该调用connect，不应该调用send和disconnect
    mock_smtp.connect.assert_called_once()
    mock_smtp.send.assert_not_called()
    mock_smtp.disconnect.assert_not_called()

# 11. Mock最佳实践
class MockBestPractices:
    """Mock最佳实践示例"""
    
    @staticmethod
    def create_user_mock(user_data: dict) -> Mock:
        """创建用户Mock的工厂方法"""
        mock_user = Mock()
        mock_user.id = user_data.get("id", 1)
        mock_user.name = user_data.get("name", "默认用户")
        mock_user.email = user_data.get("email", "default@example.com")
        mock_user.is_active = user_data.get("is_active", True)
        
        # 添加方法
        mock_user.get_full_name.return_value = f"{mock_user.name}"
        mock_user.is_admin.return_value = user_data.get("is_admin", False)
        
        return mock_user
    
    @staticmethod
    def create_database_mock() -> Mock:
        """创建数据库Mock的工厂方法"""
        mock_db = Mock()
        
        # 配置常用方法
        mock_db.connect.return_value = True
        mock_db.is_connected.return_value = True
        mock_db.close.return_value = None
        
        # 配置事务方法
        mock_db.begin_transaction.return_value = Mock()
        mock_db.commit.return_value = None
        mock_db.rollback.return_value = None
        
        return mock_db
    
    @staticmethod
    def verify_mock_interactions(mock_obj: Mock, expected_calls: list):
        """验证Mock交互的通用方法"""
        try:
            mock_obj.assert_has_calls(expected_calls)
            return True
        except AssertionError as e:
            print(f"Mock验证失败: {e}")
            return False

# 12. 测试替身类型总结
def test_doubles_summary():
    """测试替身类型总结"""
    
    # Dummy - 仅用于填充参数
    dummy_logger = Mock()
    service = SomeService(dummy_logger)  # logger不会被实际使用
    
    # Stub - 提供预设响应
    stub_repository = Mock()
    stub_repository.find_by_id.return_value = {"id": 1, "name": "测试用户"}
    
    # Mock - 验证交互
    mock_notifier = Mock()
    service.notify_user(1, "消息")
    mock_notifier.send.assert_called_with(1, "消息")
    
    # Spy - 部分Mock，保留部分真实行为
    real_service = RealService()
    spy_service = Mock(wraps=real_service)
    spy_service.process_data("test")  # 调用真实方法
    spy_service.process_data.assert_called_with("test")  # 同时可以验证调用

class SomeService:
    def __init__(self, logger):
        self.logger = logger
    
    def notify_user(self, user_id, message):
        pass

class RealService:
    def process_data(self, data):
        return f"processed_{data}"
'''
    
    print("Mock和测试替身特点:")
    print("1. Mock对象模拟外部依赖")
    print("2. patch装饰器临时替换模块")
    print("3. autospec确保Mock接口一致性")
    print("4. AsyncMock支持异步代码测试")
    print("5. 不同类型测试替身适用不同场景")
    
    # Java Mock对比
    java_mocking = '''
// Java Mock框架对比 (Mockito)

import static org.mockito.Mockito.*;
import static org.mockito.ArgumentMatchers.*;

public class MockitoExamples {
    
    // 1. 基本Mock
    @Test
    public void testBasicMocking() {
        // 创建Mock
        UserRepository mockRepo = mock(UserRepository.class);
        
        // 配置行为
        when(mockRepo.findById(1L)).thenReturn(
            Optional.of(new User(1L, "张三", "zhangsan@example.com"))
        );
        
        // 使用Mock
        UserService service = new UserService(mockRepo);
        User user = service.getUser(1L);
        
        // 验证
        assertEquals("张三", user.getName());
        verify(mockRepo).findById(1L);
    }
    
    // 2. 注解Mock
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserService userService;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }
    
    @Test
    public void testWithAnnotations() {
        when(userRepository.findById(anyLong()))
            .thenReturn(Optional.of(new User()));
            
        User result = userService.getUser(1L);
        assertNotNull(result);
        
        verify(userRepository, times(1)).findById(1L);
    }
    
    // 3. 异常Mock
    @Test
    public void testExceptionMocking() {
        when(userRepository.findById(999L))
            .thenThrow(new UserNotFoundException("User not found"));
            
        assertThrows(UserNotFoundException.class, 
                    () -> userService.getUser(999L));
    }
    
    // 4. Spy（部分Mock）
    @Test
    public void testSpying() {
        UserService realService = new UserService(userRepository);
        UserService spyService = spy(realService);
        
        // 部分Mock
        doReturn("mocked result").when(spyService).expensiveOperation();
        
        // 调用真实方法
        String result = spyService.normalOperation();
        
        // 验证
        verify(spyService).normalOperation();
    }
    
    // 5. 参数匹配器
    @Test
    public void testArgumentMatchers() {
        when(userRepository.findByEmail(anyString()))
            .thenReturn(Optional.of(new User()));
            
        when(userRepository.findByAgeRange(gt(18), lt(65)))
            .thenReturn(Arrays.asList(new User(), new User()));
            
        // 自定义匹配器
        when(userRepository.findByName(argThat(name -> name.startsWith("张"))))
            .thenReturn(Optional.of(new User()));
    }
    
    // 6. 验证交互
    @Test
    public void testVerification() {
        userService.processUsers();
        
        // 验证调用次数
        verify(userRepository, times(1)).findAll();
        verify(userRepository, atLeast(1)).save(any(User.class));
        verify(userRepository, never()).delete(any(User.class));
        
        // 验证调用顺序
        InOrder inOrder = inOrder(userRepository);
        inOrder.verify(userRepository).findAll();
        inOrder.verify(userRepository).save(any(User.class));
        
        // 验证没有更多交互
        verifyNoMoreInteractions(userRepository);
    }
    
    // 7. 复杂返回值
    @Test
    public void testComplexReturns() {
        // 连续返回不同值
        when(userRepository.count())
            .thenReturn(1L)
            .thenReturn(2L)
            .thenThrow(new RuntimeException());
            
        assertEquals(1L, userRepository.count());
        assertEquals(2L, userRepository.count());
        assertThrows(RuntimeException.class, () -> userRepository.count());
    }
    
    // 8. Mock静态方法（Mockito 3.4+）
    @Test
    public void testStaticMocking() {
        try (MockedStatic<UUID> mockedUUID = mockStatic(UUID.class)) {
            UUID fixedUUID = UUID.fromString("12345678-1234-1234-1234-123456789012");
            mockedUUID.when(UUID::randomUUID).thenReturn(fixedUUID);
            
            String result = userService.generateUserId();
            assertTrue(result.contains("12345678"));
            
            mockedUUID.verify(UUID::randomUUID);
        }
    }
}

// BDD风格测试 (Mockito-BDD)
public class BDDStyleTest {
    
    @Test
    public void shouldReturnUserWhenValidIdProvided() {
        // Given
        given(userRepository.findById(1L))
            .willReturn(Optional.of(new User()));
            
        // When
        User result = userService.getUser(1L);
        
        // Then
        then(userRepository).should().findById(1L);
        assertThat(result).isNotNull();
    }
}
'''
    
    print(f"\nMock框架对比:")
    print("Python (unittest.mock):")
    print("- 内置于标准库")
    print("- 动态类型友好")
    print("- patch装饰器灵活")
    print("- 异步支持完整")
    
    print(f"\nJava (Mockito):")
    print("- 类型安全的Mock")
    print("- 丰富的验证机制")
    print("- BDD风格支持")
    print("- 静态方法Mock")
    print()


def demo_integration_testing():
    """演示集成测试策略"""
    print("=== 3. 集成测试策略 ===")
    
    integration_example = '''
# 集成测试策略详解

import pytest
import docker
import requests
import time
import subprocess
import psutil
from pathlib import Path
from typing import Generator, Dict, Any
import tempfile
import json

# 1. 数据库集成测试
class DatabaseIntegrationTest:
    """数据库集成测试基类"""
    
    @pytest.fixture(scope="class")
    def db_container(self) -> Generator[str, None, None]:
        """PostgreSQL测试容器"""
        client = docker.from_env()
        
        # 启动PostgreSQL容器
        container = client.containers.run(
            "postgres:13",
            environment={
                "POSTGRES_DB": "testdb",
                "POSTGRES_USER": "testuser", 
                "POSTGRES_PASSWORD": "testpass"
            },
            ports={"5432/tcp": None},  # 随机端口
            detach=True,
            remove=True
        )
        
        try:
            # 等待数据库启动
            container.reload()
            port = container.attrs['NetworkSettings']['Ports']['5432/tcp'][0]['HostPort']
            
            # 等待数据库就绪
            self._wait_for_db(f"postgresql://testuser:testpass@localhost:{port}/testdb")
            
            yield f"postgresql://testuser:testpass@localhost:{port}/testdb"
            
        finally:
            container.stop()
    
    def _wait_for_db(self, db_url: str, timeout: int = 30):
        """等待数据库就绪"""
        import sqlalchemy
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                engine = sqlalchemy.create_engine(db_url)
                engine.execute("SELECT 1")
                return
            except Exception:
                time.sleep(1)
        
        raise TimeoutError("数据库启动超时")
    
    @pytest.fixture
    def db_session(self, db_container):
        """数据库会话fixture"""
        import sqlalchemy
        from sqlalchemy.orm import sessionmaker
        
        engine = sqlalchemy.create_engine(db_container)
        
        # 创建表结构
        from myapp.models import Base
        Base.metadata.create_all(engine)
        
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        try:
            yield session
        finally:
            session.close()
            Base.metadata.drop_all(engine)

class TestUserRepository(DatabaseIntegrationTest):
    """用户仓库集成测试"""
    
    def test_create_and_find_user(self, db_session):
        """测试创建和查找用户"""
        from myapp.repositories import UserRepository
        from myapp.models import User
        
        repo = UserRepository(db_session)
        
        # 创建用户
        user_data = {
            "name": "张三",
            "email": "zhangsan@example.com",
            "age": 25
        }
        user = repo.create_user(user_data)
        
        assert user.id is not None
        assert user.name == "张三"
        
        # 查找用户
        found_user = repo.find_by_id(user.id)
        assert found_user is not None
        assert found_user.email == "zhangsan@example.com"
        
        # 按邮箱查找
        email_user = repo.find_by_email("zhangsan@example.com")
        assert email_user.id == user.id
    
    def test_user_relationships(self, db_session):
        """测试用户关系"""
        from myapp.repositories import UserRepository, OrderRepository
        
        user_repo = UserRepository(db_session)
        order_repo = OrderRepository(db_session)
        
        # 创建用户
        user = user_repo.create_user({
            "name": "李四",
            "email": "lisi@example.com"
        })
        
        # 创建订单
        order1 = order_repo.create_order({
            "user_id": user.id,
            "total_amount": 100.0,
            "status": "pending"
        })
        
        order2 = order_repo.create_order({
            "user_id": user.id, 
            "total_amount": 200.0,
            "status": "completed"
        })
        
        # 测试关系查询
        user_with_orders = user_repo.find_with_orders(user.id)
        assert len(user_with_orders.orders) == 2
        
        total_amount = sum(order.total_amount for order in user_with_orders.orders)
        assert total_amount == 300.0

# 2. API集成测试
class APIIntegrationTest:
    """API集成测试"""
    
    @pytest.fixture(scope="class")
    def test_app(self):
        """测试应用实例"""
        from myapp import create_app
        
        app = create_app(testing=True)
        app.config.update({
            "TESTING": True,
            "DATABASE_URL": "sqlite:///:memory:",
            "SECRET_KEY": "test-secret"
        })
        
        with app.app_context():
            from myapp.models import db
            db.create_all()
            yield app
            db.drop_all()
    
    @pytest.fixture
    def client(self, test_app):
        """测试客户端"""
        return test_app.test_client()
    
    @pytest.fixture
    def auth_headers(self, client):
        """认证头"""
        # 创建测试用户并登录
        response = client.post('/api/auth/register', json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        })
        
        login_response = client.post('/api/auth/login', json={
            "email": "test@example.com",
            "password": "testpass123"
        })
        
        token = login_response.get_json()['access_token']
        return {"Authorization": f"Bearer {token}"}
    
    def test_user_crud_flow(self, client, auth_headers):
        """测试用户CRUD流程"""
        # 创建用户
        create_response = client.post('/api/users', 
            json={
                "name": "新用户",
                "email": "newuser@example.com",
                "age": 30
            },
            headers=auth_headers
        )
        
        assert create_response.status_code == 201
        user_data = create_response.get_json()
        user_id = user_data['id']
        
        # 获取用户
        get_response = client.get(f'/api/users/{user_id}', headers=auth_headers)
        assert get_response.status_code == 200
        assert get_response.get_json()['name'] == "新用户"
        
        # 更新用户
        update_response = client.put(f'/api/users/{user_id}',
            json={"name": "更新用户", "age": 31},
            headers=auth_headers
        )
        assert update_response.status_code == 200
        assert update_response.get_json()['name'] == "更新用户"
        
        # 删除用户
        delete_response = client.delete(f'/api/users/{user_id}', headers=auth_headers)
        assert delete_response.status_code == 204
        
        # 验证删除
        get_deleted_response = client.get(f'/api/users/{user_id}', headers=auth_headers)
        assert get_deleted_response.status_code == 404
    
    def test_api_error_handling(self, client, auth_headers):
        """测试API错误处理"""
        # 测试参数验证
        response = client.post('/api/users',
            json={
                "name": "",  # 空名称
                "email": "invalid-email",  # 无效邮箱
                "age": -1  # 无效年龄
            },
            headers=auth_headers
        )
        
        assert response.status_code == 400
        error_data = response.get_json()
        assert 'validation_errors' in error_data
        
        # 测试未授权访问
        response = client.get('/api/users/1')  # 没有认证头
        assert response.status_code == 401
        
        # 测试权限不足
        response = client.delete('/api/admin/users/1', headers=auth_headers)
        assert response.status_code == 403

# 3. 微服务集成测试
class MicroservicesIntegrationTest:
    """微服务集成测试"""
    
    @pytest.fixture(scope="class")
    def services_env(self):
        """启动测试服务环境"""
        # 使用docker-compose启动测试环境
        compose_file = Path(__file__).parent / "docker-compose.test.yml"
        
        # 启动服务
        subprocess.run([
            "docker-compose", "-f", str(compose_file), 
            "up", "-d"
        ], check=True)
        
        # 等待服务就绪
        self._wait_for_services([
            "http://localhost:8001/health",  # 用户服务
            "http://localhost:8002/health",  # 订单服务
            "http://localhost:8003/health",  # 支付服务
        ])
        
        yield {
            "user_service": "http://localhost:8001",
            "order_service": "http://localhost:8002", 
            "payment_service": "http://localhost:8003"
        }
        
        # 清理环境
        subprocess.run([
            "docker-compose", "-f", str(compose_file),
            "down", "-v"
        ])
    
    def _wait_for_services(self, health_urls: list, timeout: int = 60):
        """等待服务就绪"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            all_ready = True
            
            for url in health_urls:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code != 200:
                        all_ready = False
                        break
                except requests.RequestException:
                    all_ready = False
                    break
            
            if all_ready:
                return
            
            time.sleep(2)
        
        raise TimeoutError("服务启动超时")
    
    def test_order_creation_flow(self, services_env):
        """测试订单创建流程"""
        user_service = services_env["user_service"]
        order_service = services_env["order_service"]
        payment_service = services_env["payment_service"]
        
        # 1. 创建用户
        user_response = requests.post(f"{user_service}/api/users", json={
            "name": "测试用户",
            "email": "test@example.com"
        })
        assert user_response.status_code == 201
        user_id = user_response.json()['id']
        
        # 2. 创建订单
        order_response = requests.post(f"{order_service}/api/orders", json={
            "user_id": user_id,
            "items": [
                {"product_id": 1, "quantity": 2, "price": 50.0},
                {"product_id": 2, "quantity": 1, "price": 30.0}
            ]
        })
        assert order_response.status_code == 201
        order_id = order_response.json()['id']
        
        # 3. 处理支付
        payment_response = requests.post(f"{payment_service}/api/payments", json={
            "order_id": order_id,
            "amount": 130.0,
            "payment_method": "credit_card",
            "card_token": "test_token_123"
        })
        assert payment_response.status_code == 201
        
        # 4. 验证订单状态更新
        order_status_response = requests.get(f"{order_service}/api/orders/{order_id}")
        assert order_status_response.status_code == 200
        assert order_status_response.json()['status'] == 'paid'
        
        # 5. 验证用户订单列表
        user_orders_response = requests.get(f"{user_service}/api/users/{user_id}/orders")
        assert user_orders_response.status_code == 200
        orders = user_orders_response.json()
        assert len(orders) == 1
        assert orders[0]['id'] == order_id

# 4. 性能集成测试
class PerformanceIntegrationTest:
    """性能集成测试"""
    
    def test_api_response_time(self, client):
        """测试API响应时间"""
        response_times = []
        
        for _ in range(100):
            start_time = time.time()
            response = client.get('/api/users')
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
        
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        
        # 性能断言
        assert avg_response_time < 0.1  # 平均响应时间小于100ms
        assert max_response_time < 0.5  # 最大响应时间小于500ms
        
        print(f"平均响应时间: {avg_response_time:.3f}s")
        print(f"最大响应时间: {max_response_time:.3f}s")
    
    def test_concurrent_requests(self, client):
        """测试并发请求"""
        import threading
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        results = []
        errors = []
        
        def make_request():
            try:
                response = client.get('/api/users')
                results.append({
                    'status_code': response.status_code,
                    'response_time': time.time()
                })
            except Exception as e:
                errors.append(str(e))
        
        # 并发50个请求
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            
            for future in as_completed(futures):
                future.result()  # 等待完成
        
        # 验证结果
        assert len(errors) == 0, f"发生错误: {errors}"
        assert len(results) == 50
        
        success_count = sum(1 for r in results if r['status_code'] == 200)
        assert success_count == 50, "并发请求成功率不达标"

# 5. 端到端测试
class EndToEndTest:
    """端到端测试"""
    
    @pytest.fixture(scope="class")
    def browser(self):
        """浏览器fixture (使用Selenium)"""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        yield driver
        driver.quit()
    
    def test_user_registration_flow(self, browser, test_app):
        """测试用户注册流程"""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        base_url = "http://localhost:5000"
        
        # 1. 访问注册页面
        browser.get(f"{base_url}/register")
        assert "注册" in browser.title
        
        # 2. 填写注册表单
        username_input = browser.find_element(By.NAME, "username")
        email_input = browser.find_element(By.NAME, "email")
        password_input = browser.find_element(By.NAME, "password")
        
        username_input.send_keys("testuser")
        email_input.send_keys("test@example.com")
        password_input.send_keys("testpass123")
        
        # 3. 提交表单
        submit_button = browser.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        
        # 4. 验证跳转到登录页面
        WebDriverWait(browser, 10).until(
            EC.url_contains("/login")
        )
        
        success_message = browser.find_element(By.CLASS_NAME, "success-message")
        assert "注册成功" in success_message.text
        
        # 5. 登录验证
        email_input = browser.find_element(By.NAME, "email")
        password_input = browser.find_element(By.NAME, "password")
        
        email_input.send_keys("test@example.com")
        password_input.send_keys("testpass123")
        
        login_button = browser.find_element(By.XPATH, "//input[@type='submit']")
        login_button.click()
        
        # 6. 验证登录成功
        WebDriverWait(browser, 10).until(
            EC.url_contains("/dashboard")
        )
        
        welcome_message = browser.find_element(By.CLASS_NAME, "welcome")
        assert "欢迎, testuser" in welcome_message.text

# 6. 集成测试配置
# conftest.py 示例
'''
import pytest
import tempfile
import os
from pathlib import Path

@pytest.fixture(scope="session")
def test_config():
    """测试配置"""
    return {
        "DATABASE_URL": "sqlite:///:memory:",
        "REDIS_URL": "redis://localhost:6379/1",
        "SECRET_KEY": "test-secret-key",
        "TESTING": True,
        "DEBUG": True
    }

@pytest.fixture(scope="session")
def temp_directory():
    """临时目录"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

def pytest_configure(config):
    """pytest配置"""
    config.addinivalue_line("markers", "slow: 标记慢速测试")
    config.addinivalue_line("markers", "integration: 标记集成测试")
    config.addinivalue_line("markers", "e2e: 标记端到端测试")

def pytest_collection_modifyitems(config, items):
    """修改测试收集"""
    if config.getoption("--runslow"):
        return
    
    skip_slow = pytest.mark.skip(reason="需要 --runslow 选项来运行")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
'''

# docker-compose.test.yml 示例
'''
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: testdb
      POSTGRES_USER: testuser
      POSTGRES_PASSWORD: testpass
    ports:
      - "5432:5432"
    
  redis:
    image: redis:6
    ports:
      - "6379:6379"
    
  user-service:
    build: ./services/user
    environment:
      DATABASE_URL: postgresql://testuser:testpass@postgres:5432/testdb
      REDIS_URL: redis://redis:6379
    ports:
      - "8001:8000"
    depends_on:
      - postgres
      - redis
    
  order-service:
    build: ./services/order
    environment:
      DATABASE_URL: postgresql://testuser:testpass@postgres:5432/testdb
      USER_SERVICE_URL: http://user-service:8000
    ports:
      - "8002:8000"
    depends_on:
      - postgres
      - user-service
'''
'''
    
    print("集成测试策略特点:")
    print("1. 测试真实组件间的交互")
    print("2. 使用容器化测试环境")
    print("3. 包含数据库、API、微服务测试")
    print("4. 性能和端到端测试覆盖")
    print("5. 自动化环境搭建和清理")
    
    # Java集成测试对比
    java_integration = '''
// Java集成测试对比 (Spring Boot)

// 1. 数据库集成测试
@SpringBootTest
@Testcontainers
@Transactional
public class UserRepositoryIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:13")
            .withDatabaseName("testdb")
            .withUsername("testuser")
            .withPassword("testpass");
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private TestEntityManager entityManager;
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
    
    @Test
    public void shouldCreateAndFindUser() {
        User user = new User("张三", "zhangsan@example.com");
        User saved = userRepository.save(user);
        
        assertThat(saved.getId()).isNotNull();
        
        Optional<User> found = userRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("张三");
    }
}

// 2. Web层集成测试
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class UserControllerIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    public void shouldCreateUserThroughAPI() {
        UserCreateRequest request = new UserCreateRequest("李四", "lisi@example.com");
        
        ResponseEntity<UserResponse> response = restTemplate.postForEntity(
            "/api/users", request, UserResponse.class);
        
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody().getName()).isEqualTo("李四");
        
        // 验证数据库中的数据
        Optional<User> saved = userRepository.findByEmail("lisi@example.com");
        assertThat(saved).isPresent();
    }
}

// 3. 微服务集成测试
@SpringBootTest
@TestMethodOrder(OrderAnnotation.class)
public class OrderProcessingIntegrationTest {
    
    @MockBean
    private PaymentService paymentService;
    
    @Autowired
    private OrderService orderService;
    
    @Autowired
    private UserService userService;
    
    @Test
    @Order(1)
    public void shouldProcessOrderSuccessfully() {
        // Given
        User user = userService.createUser(new User("王五", "wangwu@example.com"));
        
        when(paymentService.processPayment(any(PaymentRequest.class)))
            .thenReturn(new PaymentResult(true, "SUCCESS"));
        
        // When
        OrderRequest request = new OrderRequest(user.getId(), 
            Arrays.asList(new OrderItem(1L, 2), new OrderItem(2L, 1)));
        Order order = orderService.createOrder(request);
        
        // Then
        assertThat(order.getStatus()).isEqualTo(OrderStatus.PAID);
        verify(paymentService).processPayment(any(PaymentRequest.class));
    }
}

// 4. 测试片段
@DataJpaTest
public class UserRepositoryTest {
    @Autowired
    private TestEntityManager entityManager;
    
    @Autowired
    private UserRepository userRepository;
    
    // 只测试JPA层
}

@WebMvcTest(UserController.class)
public class UserControllerTest {
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private UserService userService;
    
    // 只测试Web层
}

// 5. 测试配置
@TestConfiguration
public class TestConfig {
    
    @Bean
    @Primary
    public Clock testClock() {
        return Clock.fixed(Instant.parse("2023-01-01T00:00:00Z"), ZoneId.systemDefault());
    }
    
    @Bean
    @Primary
    public EmailService mockEmailService() {
        return Mockito.mock(EmailService.class);
    }
}
'''
    
    print(f"\n集成测试对比:")
    print("Python:")
    print("- 灵活的容器化测试环境")
    print("- pytest fixtures管理测试资源")
    print("- 直接的HTTP客户端测试")
    print("- Selenium端到端测试")
    
    print(f"\nJava (Spring Boot):")
    print("- Testcontainers无缝集成")
    print("- 测试片段隔离测试层")
    print("- 丰富的测试注解")
    print("- 企业级测试配置")
    print()


def main():
    """主函数：运行所有演示"""
    print("测试最佳实践完整学习指南")
    print("=" * 50)
    
    demo_test_coverage()
    demo_mocking_strategies()
    demo_integration_testing()
    
    # 完成第五阶段所有任务
    print("\n=== 第五阶段完成总结 ===")
    print("✅ 5.1 Web框架对比 - Django、FastAPI、Flask")
    print("✅ 5.2 数据库操作 - SQLAlchemy ORM、连接池")
    print("✅ 5.3 测试框架 - pytest、最佳实践")
    
    print("\n学习总结:")
    print("1. 测试覆盖率监控确保代码质量")
    print("2. Mock技术隔离测试环境")
    print("3. 集成测试验证组件交互")
    print("4. 测试策略需要分层设计")
    print("5. Python测试生态系统完整成熟")
    print("6. 企业级测试需要自动化和监控")


if __name__ == "__main__":
    main() 