#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Poetry现代包管理详解
Poetry Modern Package Management Guide

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习Poetry的项目管理、依赖解析、发布流程和与Gradle的对比

学习目标:
1. 掌握Poetry的项目初始化和结构管理
2. 理解依赖解析和锁定机制
3. 学会构建和发布流程
4. 对比Poetry与Gradle的设计理念

注意：Poetry是Python生态中的现代化包管理和构建工具
"""

import subprocess
import sys
import json
import toml
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import os


def demo_poetry_basics():
    """演示Poetry基础操作"""
    print("=== 1. Poetry基础操作 ===")
    
    basic_operations = '''
# Poetry基础命令详解

# 1. 安装Poetry
curl -sSL https://install.python-poetry.org | python3 -
# 或者使用pip安装
pip install poetry

# 验证安装
poetry --version
poetry self show

# 2. 项目初始化
poetry new my-project                    # 创建新项目
poetry init                             # 在现有目录初始化
poetry init --no-interaction            # 非交互式初始化

# 创建的项目结构:
"""
my-project/
├── pyproject.toml                      # 项目配置文件
├── README.md                           # 项目说明
├── my_project/                         # 源代码目录
│   └── __init__.py
└── tests/                              # 测试目录
    └── __init__.py
"""

# 3. 依赖管理
poetry add requests                      # 添加生产依赖
poetry add pytest --group dev           # 添加开发依赖
poetry add "django>=4.0,<5.0"          # 添加版本约束依赖
poetry add git+https://github.com/user/repo.git  # 添加Git依赖
poetry add ./local-package              # 添加本地依赖
poetry add requests[security]           # 添加可选依赖

# 4. 依赖组管理
poetry add pytest black --group dev     # 添加到开发组
poetry add sphinx --group docs          # 添加到文档组
poetry install --with dev,docs          # 安装指定组依赖
poetry install --without dev            # 排除指定组
poetry install --only dev               # 只安装指定组

# 5. 依赖操作
poetry remove requests                   # 移除依赖
poetry update                           # 更新所有依赖
poetry update requests                  # 更新指定依赖
poetry show                             # 显示所有依赖
poetry show --tree                      # 显示依赖树
poetry show requests                    # 显示特定包信息

# 6. 虚拟环境管理
poetry env use python3.10               # 指定Python版本
poetry env use /usr/bin/python3         # 指定Python路径
poetry env info                         # 显示环境信息
poetry env list                         # 列出所有环境
poetry shell                            # 激活虚拟环境
poetry run python script.py             # 在环境中运行命令
poetry run pytest                       # 在环境中运行测试

# 7. 构建和发布
poetry build                            # 构建包（wheel和tar.gz）
poetry publish                          # 发布到PyPI
poetry publish --repository testpypi    # 发布到测试PyPI
poetry config repositories.my-repo http://my-repo.com/simple/  # 配置私有仓库
poetry publish --repository my-repo     # 发布到私有仓库

# 8. 锁定文件管理
poetry lock                             # 生成/更新锁定文件
poetry lock --no-update                 # 重新锁定而不更新
poetry install                          # 从锁定文件安装
poetry export -f requirements.txt --output requirements.txt  # 导出requirements.txt

# 9. 脚本和任务
poetry run python -m pytest             # 运行测试
poetry run black .                      # 代码格式化
poetry run mypy src/                     # 类型检查
poetry run python -m my_project         # 运行模块

# 10. 配置管理
poetry config --list                    # 列出所有配置
poetry config virtualenvs.create false  # 不创建虚拟环境
poetry config virtualenvs.in-project true  # 在项目内创建.venv
poetry config pypi-token.pypi YOUR_TOKEN    # 设置PyPI令牌
'''
    
    print("Poetry基础特点:")
    print("1. 统一的项目管理工具")
    print("2. 声明式依赖管理")
    print("3. 自动虚拟环境管理")
    print("4. 现代化的构建系统")
    print("5. 内置发布功能")
    
    # Gradle基础对比
    gradle_basics = '''
// Gradle基础操作对比

// 1. 项目初始化
gradle init --type java-application     // 创建Java应用项目
gradle init --type java-library         // 创建Java库项目
gradle init --type kotlin-application   // 创建Kotlin项目

// 项目结构 (Gradle)
/*
my-project/
├── build.gradle(.kts)                  // 构建脚本
├── settings.gradle(.kts)               // 设置文件
├── gradle.properties                   // 属性配置
├── gradlew                            // Gradle包装器
├── gradlew.bat                        // Windows包装器
├── gradle/                            // Gradle配置
│   └── wrapper/
├── src/
│   ├── main/
│   │   ├── java/                      // 源代码
│   │   └── resources/                 // 资源文件
│   └── test/
│       ├── java/                      // 测试代码
│       └── resources/                 // 测试资源
└── build/                             // 构建输出
*/

// 2. build.gradle依赖管理
plugins {
    id 'java'
    id 'application'
    id 'org.springframework.boot' version '2.7.0'
}

repositories {
    mavenCentral()
    maven {
        url 'https://maven.aliyun.com/repository/public'
    }
    gradlePluginPortal()
}

dependencies {
    // 生产依赖
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.postgresql:postgresql'
    
    // 编译时依赖
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
    
    // 运行时依赖
    runtimeOnly 'com.h2database:h2'
    
    // 测试依赖
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testImplementation 'org.testcontainers:junit-jupiter'
    testImplementation 'org.testcontainers:postgresql'
    
    // 开发工具
    developmentOnly 'org.springframework.boot:spring-boot-devtools'
}

// 3. 任务配置
tasks.named('test') {
    useJUnitPlatform()
    testLogging {
        events "passed", "skipped", "failed"
    }
}

application {
    mainClass = 'com.example.Application'
}

// 4. 自定义任务
task copyDependencies(type: Copy) {
    from configurations.runtimeClasspath
    into 'build/libs/dependencies'
}

task generateVersionFile {
    doLast {
        file('src/main/resources/version.txt').text = project.version
    }
}

// 5. Gradle命令
// ./gradlew build                        // 构建项目
// ./gradlew test                         // 运行测试
// ./gradlew bootRun                      // 运行Spring Boot应用
// ./gradlew dependencies                 // 显示依赖树
// ./gradlew dependencyInsight --dependency spring-core  // 依赖洞察
// ./gradlew clean                        // 清理构建
// ./gradlew publish                      // 发布到仓库

// 6. 多项目构建 (settings.gradle)
rootProject.name = 'multi-project'
include 'core', 'web', 'api'

project(':core').projectDir = file('modules/core')
project(':web').projectDir = file('modules/web')
project(':api').projectDir = file('modules/api')

// 7. Gradle Wrapper配置
// gradle/wrapper/gradle-wrapper.properties
/*
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-7.5-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
*/
'''
    
    print(f"\n基础操作对比:")
    print("Poetry:")
    print("- TOML配置文件")
    print("- 简化的命令语法")
    print("- 自动虚拟环境")
    print("- 内置依赖解析")
    
    print(f"\nGradle:")
    print("- Groovy/Kotlin DSL")
    print("- 灵活的任务系统")
    print("- 强大的多项目支持")
    print("- 丰富的插件生态")
    print()


def demo_pyproject_toml():
    """演示pyproject.toml配置详解"""
    print("=== 2. pyproject.toml配置详解 ===")
    
    pyproject_example = '''
# pyproject.toml完整配置示例

[tool.poetry]
# 项目基本信息
name = "my-awesome-project"
version = "1.0.0"
description = "一个出色的Python项目"
authors = ["张三 <zhangsan@example.com>"]
maintainers = ["李四 <lisi@example.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://github.com/user/my-awesome-project"
repository = "https://github.com/user/my-awesome-project"
documentation = "https://my-awesome-project.readthedocs.io"
keywords = ["python", "web", "api"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Framework :: Django",
    "Topic :: Internet :: WWW/HTTP",
]

# 包配置
packages = [{include = "my_project", from = "src"}]
include = [
    "CHANGELOG.md",
    "LICENSE",
    { path = "data/*.json", format = "wheel" },
]
exclude = ["tests", "docs", "*.pyc"]

# Python版本要求
python = "^3.8"

# 依赖管理
[tool.poetry.dependencies]
# 核心依赖
python = "^3.8"
django = "^4.1.0"
psycopg2-binary = "^2.9.0"
redis = "~4.3.0"
celery = {extras = ["redis"], version = "^5.2.0"}
requests = "^2.28.0"
pydantic = "^1.10.0"

# 可选依赖
uvicorn = {version = "^0.18.0", optional = true}
gunicorn = {version = "^20.1.0", optional = true}
sentry-sdk = {version = "^1.9.0", optional = true}

# Git依赖
my-private-lib = {git = "https://github.com/user/private-lib.git", branch = "main"}

# 本地依赖
local-utils = {path = "../utils", develop = true}

# URL依赖
special-package = {url = "https://files.pythonhosted.org/packages/.../package.whl"}

# 开发依赖组
[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
pytest-django = "^4.5.0"
pytest-cov = "^3.0.0"
pytest-mock = "^3.8.0"
black = "^22.6.0"
isort = "^5.10.0"
flake8 = "^5.0.0"
mypy = "^0.971"
pre-commit = "^2.20.0"

# 测试依赖组
[tool.poetry.group.test.dependencies]
pytest = "^7.0.0"
pytest-xdist = "^2.5.0"
coverage = "^6.4.0"
factory-boy = "^3.2.0"
faker = "^15.0.0"

# 文档依赖组
[tool.poetry.group.docs.dependencies]
sphinx = "^5.0.0"
sphinx-rtd-theme = "^1.0.0"
myst-parser = "^0.18.0"

# 可选功能
[tool.poetry.extras]
server = ["uvicorn", "gunicorn"]
monitoring = ["sentry-sdk"]
all = ["uvicorn", "gunicorn", "sentry-sdk"]

# 脚本定义
[tool.poetry.scripts]
my-cli = "my_project.cli:main"
start-server = "my_project.server:start"

# 插件入口点
[tool.poetry.plugins."my_project.plugins"]
json = "my_project.plugins.json:JsonPlugin"
yaml = "my_project.plugins.yaml:YamlPlugin"

# URL配置
[tool.poetry.urls]
"Bug Tracker" = "https://github.com/user/my-awesome-project/issues"
"Funding" = "https://github.com/sponsors/user"
"Say Thanks!" = "https://saythanks.io/to/user"

# 构建系统
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

# 工具配置
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\\.pyi?$'
extend-exclude = '''
/(
  # directories
  \\.eggs
  | \\.git
  | \\.hg
  | \\.mypy_cache
  | \\.tox
  | \\.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["my_project"]
known_third_party = ["django", "requests", "celery"]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
ignore_errors = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=my_project",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=85",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]

[tool.coverage.run]
source = ["my_project"]
omit = [
    "*/migrations/*",
    "*/venv/*",
    "*/tests/*",
    "manage.py",
    "*/settings/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
'''
    
    print("pyproject.toml配置特点:")
    print("1. 统一的项目配置文件")
    print("2. 声明式依赖管理")
    print("3. 依赖组织和分类")
    print("4. 丰富的元数据配置")
    print("5. 工具配置集中管理")


class PoetryProjectManager:
    """Poetry项目管理器"""
    
    def __init__(self, project_name: str, project_path: Optional[str] = None):
        self.project_name = project_name
        self.project_path = Path(project_path or tempfile.mkdtemp()) / project_name
        
    def create_project_structure(self):
        """创建项目结构"""
        # 创建项目目录
        self.project_path.mkdir(parents=True, exist_ok=True)
        
        # 创建pyproject.toml
        pyproject_content = self._generate_pyproject_toml()
        (self.project_path / "pyproject.toml").write_text(pyproject_content)
        
        # 创建源代码目录
        src_dir = self.project_path / "src" / self.project_name.replace("-", "_")
        src_dir.mkdir(parents=True, exist_ok=True)
        (src_dir / "__init__.py").write_text(f'"""\\n{self.project_name} package\\n"""\\n\\n__version__ = "0.1.0"\\n')
        
        # 创建测试目录
        tests_dir = self.project_path / "tests"
        tests_dir.mkdir(exist_ok=True)
        (tests_dir / "__init__.py").write_text("")
        (tests_dir / "test_basic.py").write_text(self._generate_basic_test())
        
        # 创建文档
        (self.project_path / "README.md").write_text(self._generate_readme())
        (self.project_path / "CHANGELOG.md").write_text("# Changelog\\n\\n## [Unreleased]\\n")
        
        # 创建配置文件
        (self.project_path / ".gitignore").write_text(self._generate_gitignore())
        (self.project_path / ".pre-commit-config.yaml").write_text(self._generate_precommit_config())
        
        print(f"项目结构已创建: {self.project_path}")
        
    def _generate_pyproject_toml(self) -> str:
        """生成pyproject.toml文件"""
        package_name = self.project_name.replace("-", "_")
        return f'''[tool.poetry]
name = "{self.project_name}"
version = "0.1.0"
description = "A modern Python project"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{{include = "{package_name}", from = "src"}}]

[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^22.6.0"
isort = "^5.10.0"
flake8 = "^5.0.0"
mypy = "^0.971"
pre-commit = "^2.20.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"

[tool.pytest.ini_options]
testpaths = ["tests"]
'''
        
    def _generate_basic_test(self) -> str:
        """生成基础测试"""
        package_name = self.project_name.replace("-", "_")
        return f'''import pytest
from {package_name} import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_basic_functionality():
    """测试基本功能"""
    assert True
'''
        
    def _generate_readme(self) -> str:
        """生成README"""
        return f'''# {self.project_name}

A modern Python project built with Poetry.

## Installation

```bash
poetry install
```

## Usage

```python
import {self.project_name.replace("-", "_")}
```

## Development

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Format code
poetry run black .
poetry run isort .

# Type checking
poetry run mypy src/
```

## License

MIT License
'''
        
    def _generate_gitignore(self) -> str:
        """生成.gitignore"""
        return '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
'''
        
    def _generate_precommit_config(self) -> str:
        """生成pre-commit配置"""
        return '''repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.3.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 22.6.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.971
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
'''

    def show_project_info(self):
        """显示项目信息"""
        if (self.project_path / "pyproject.toml").exists():
            with open(self.project_path / "pyproject.toml") as f:
                config = toml.load(f)
                
            print(f"项目信息:")
            print(f"  名称: {config['tool']['poetry']['name']}")
            print(f"  版本: {config['tool']['poetry']['version']}")
            print(f"  描述: {config['tool']['poetry']['description']}")
            print(f"  作者: {config['tool']['poetry']['authors']}")
            
            deps = config['tool']['poetry']['dependencies']
            print(f"  依赖数量: {len(deps)}")
            
            if 'group' in config['tool']['poetry']:
                dev_deps = config['tool']['poetry']['group']['dev']['dependencies']
                print(f"  开发依赖数量: {len(dev_deps)}")


def demo_dependency_resolution():
    """演示依赖解析机制"""
    print("=== 3. 依赖解析机制 ===")
    
    dependency_resolution = '''
# Poetry依赖解析详解

# 1. 语义化版本控制
"""
Poetry使用语义化版本（SemVer）进行依赖管理：

版本约束语法：
- ^1.2.3   相当于 >=1.2.3, <2.0.0 (兼容更新)
- ~1.2.3   相当于 >=1.2.3, <1.3.0 (补丁更新)
- >=1.2.3  大于等于1.2.3
- >1.2.3   大于1.2.3
- <=1.2.3  小于等于1.2.3
- <1.2.3   小于1.2.3
- ==1.2.3  精确等于1.2.3
- !=1.2.3  不等于1.2.3
- *        任何版本
"""

# 2. 依赖解析过程
class DependencyResolver:
    """依赖解析器演示"""
    
    def __init__(self):
        self.dependency_graph = {}
        self.resolved_versions = {}
        self.conflicts = []
    
    def resolve_dependencies(self, requirements: Dict[str, str]):
        """解析依赖"""
        print("开始依赖解析...")
        
        for package, version_spec in requirements.items():
            print(f"解析 {package} {version_spec}")
            
            # 获取包的所有可用版本
            available_versions = self._get_available_versions(package)
            print(f"  可用版本: {available_versions}")
            
            # 找到满足约束的版本
            compatible_versions = self._find_compatible_versions(
                available_versions, version_spec
            )
            print(f"  兼容版本: {compatible_versions}")
            
            if compatible_versions:
                # 选择最高的兼容版本
                selected_version = max(compatible_versions)
                self.resolved_versions[package] = selected_version
                print(f"  选定版本: {selected_version}")
                
                # 递归解析子依赖
                sub_deps = self._get_package_dependencies(package, selected_version)
                if sub_deps:
                    print(f"  子依赖: {sub_deps}")
                    self.resolve_dependencies(sub_deps)
            else:
                self.conflicts.append(f"无法找到满足 {package} {version_spec} 的版本")
    
    def _get_available_versions(self, package: str) -> List[str]:
        """获取包的可用版本（模拟）"""
        # 模拟从PyPI获取版本信息
        mock_versions = {
            "requests": ["2.25.1", "2.26.0", "2.27.0", "2.28.0", "2.28.1"],
            "urllib3": ["1.26.8", "1.26.9", "1.26.10", "1.26.11", "1.26.12"],
            "certifi": ["2021.10.8", "2022.5.18", "2022.6.15", "2022.9.24"],
        }
        return mock_versions.get(package, ["1.0.0"])
    
    def _find_compatible_versions(self, versions: List[str], spec: str) -> List[str]:
        """找到兼容的版本（简化实现）"""
        # 这里简化处理，实际Poetry使用复杂的版本解析算法
        if spec.startswith("^"):
            # 兼容更新：主版本相同，次版本和补丁版本可以更高
            base_version = spec[1:]
            return [v for v in versions if v >= base_version and v.split('.')[0] == base_version.split('.')[0]]
        elif spec.startswith("~"):
            # 补丁更新：主版本和次版本相同，补丁版本可以更高
            base_version = spec[1:]
            base_parts = base_version.split('.')
            return [v for v in versions if v >= base_version and v.split('.')[0:2] == base_parts[0:2]]
        else:
            # 其他情况简化处理
            return versions
    
    def _get_package_dependencies(self, package: str, version: str) -> Dict[str, str]:
        """获取包的依赖（模拟）"""
        mock_dependencies = {
            "requests": {
                "urllib3": "^1.26.0",
                "certifi": "^2022.0.0",
                "charset-normalizer": "^2.0.0",
            },
            "urllib3": {},
            "certifi": {},
        }
        return mock_dependencies.get(package, {})
    
    def show_resolution_result(self):
        """显示解析结果"""
        print("\\n=== 依赖解析结果 ===")
        if self.resolved_versions:
            print("已解析的依赖:")
            for package, version in self.resolved_versions.items():
                print(f"  {package} == {version}")
        
        if self.conflicts:
            print("\\n冲突:")
            for conflict in self.conflicts:
                print(f"  {conflict}")

# 3. poetry.lock文件分析
class LockFileAnalyzer:
    """锁定文件分析器"""
    
    def __init__(self, lock_file_path: str):
        self.lock_file_path = Path(lock_file_path)
    
    def analyze_lock_file(self):
        """分析锁定文件"""
        if not self.lock_file_path.exists():
            print("poetry.lock文件不存在")
            return
        
        with open(self.lock_file_path, 'r') as f:
            lock_data = toml.load(f)
        
        packages = lock_data.get('package', [])
        metadata = lock_data.get('metadata', {})
        
        print(f"锁定文件分析:")
        print(f"  包数量: {len(packages)}")
        print(f"  Python版本约束: {metadata.get('python-versions', 'N/A')}")
        print(f"  内容哈希: {metadata.get('content-hash', 'N/A')}")
        
        # 分析包类型分布
        package_types = {}
        for package in packages:
            category = package.get('category', 'main')
            package_types[category] = package_types.get(category, 0) + 1
        
        print(f"  包类型分布:")
        for category, count in package_types.items():
            print(f"    {category}: {count}")
        
        # 检查是否有开发依赖
        dev_packages = [p for p in packages if p.get('category') == 'dev']
        if dev_packages:
            print(f"  开发依赖: {len(dev_packages)} 个")
        
        return packages, metadata
    
    def check_outdated_packages(self, packages: List[Dict]):
        """检查过时的包"""
        print("\\n检查过时的包:")
        # 这里可以实现与PyPI API的集成
        # 检查每个包是否有更新版本
        for package in packages[:5]:  # 只检查前5个包作为示例
            name = package['name']
            version = package['version']
            print(f"  {name} {version} - 检查更新...")
    
    def generate_dependency_graph(self, packages: List[Dict]):
        """生成依赖关系图"""
        print("\\n依赖关系图:")
        
        # 构建依赖图
        dep_graph = {}
        for package in packages:
            name = package['name']
            dependencies = package.get('dependencies', {})
            dep_graph[name] = list(dependencies.keys())
        
        # 显示顶级依赖（没有被其他包依赖的包）
        all_deps = set()
        for deps in dep_graph.values():
            all_deps.update(deps)
        
        top_level = [pkg for pkg in dep_graph.keys() if pkg not in all_deps]
        print(f"  顶级依赖: {top_level}")
        
        # 显示依赖最多的包
        dep_counts = [(pkg, len(deps)) for pkg, deps in dep_graph.items()]
        dep_counts.sort(key=lambda x: x[1], reverse=True)
        
        print("  依赖最多的包:")
        for pkg, count in dep_counts[:5]:
            print(f"    {pkg}: {count} 个依赖")

# 4. 依赖冲突解决
class ConflictResolver:
    """依赖冲突解决器"""
    
    def __init__(self):
        self.constraints = {}
        self.conflicts = []
    
    def add_constraint(self, package: str, constraint: str, source: str):
        """添加约束"""
        if package not in self.constraints:
            self.constraints[package] = []
        
        self.constraints[package].append({
            'constraint': constraint,
            'source': source
        })
    
    def detect_conflicts(self):
        """检测冲突"""
        print("检测依赖冲突...")
        
        for package, constraints in self.constraints.items():
            if len(constraints) > 1:
                # 检查约束是否兼容
                constraint_values = [c['constraint'] for c in constraints]
                if not self._are_constraints_compatible(constraint_values):
                    self.conflicts.append({
                        'package': package,
                        'constraints': constraints
                    })
                    print(f"发现冲突: {package}")
                    for constraint in constraints:
                        print(f"  {constraint['source']}: {constraint['constraint']}")
    
    def _are_constraints_compatible(self, constraints: List[str]) -> bool:
        """检查约束是否兼容（简化实现）"""
        # 实际实现需要复杂的版本约束解析
        return len(set(constraints)) == 1  # 简化：只有相同约束才兼容
    
    def suggest_resolutions(self):
        """建议解决方案"""
        if not self.conflicts:
            print("未发现冲突")
            return
        
        print("\\n冲突解决建议:")
        for conflict in self.conflicts:
            package = conflict['package']
            print(f"\\n{package}:")
            print("  可能的解决方案:")
            print("  1. 更新依赖到兼容版本")
            print("  2. 使用dependency groups隔离冲突依赖")
            print("  3. 寻找替代包")
            print("  4. 使用extras避免不必要的依赖")

# 5. 使用示例
def dependency_resolution_example():
    """依赖解析示例"""
    
    # 依赖解析
    resolver = DependencyResolver()
    requirements = {
        "requests": "^2.28.0",
        "urllib3": "^1.26.0",
    }
    resolver.resolve_dependencies(requirements)
    resolver.show_resolution_result()
    
    # 冲突检测
    conflict_resolver = ConflictResolver()
    conflict_resolver.add_constraint("urllib3", "^1.26.0", "requests")
    conflict_resolver.add_constraint("urllib3", "~1.25.0", "another-package")
    conflict_resolver.detect_conflicts()
    conflict_resolver.suggest_resolutions()
'''
    
    print("依赖解析特点:")
    print("1. 基于SAT求解器的智能解析")
    print("2. 语义化版本约束支持")
    print("3. 详细的锁定文件记录")
    print("4. 冲突检测和解决建议")
    print("5. 依赖图分析和优化")
    
    # Gradle依赖解析对比
    gradle_resolution = '''
// Gradle依赖解析对比

// 1. 版本冲突解决策略
configurations.all {
    resolutionStrategy {
        // 失败策略
        failOnVersionConflict()
        
        // 强制特定版本
        force 'org.slf4j:slf4j-api:1.7.36'
        
        // 版本选择规则
        eachDependency { DependencyResolveDetails details ->
            if (details.requested.group == 'org.slf4j') {
                details.useVersion '1.7.36'
                details.because 'Align SLF4J versions'
            }
        }
        
        // 缓存策略
        cacheDynamicVersionsFor 10, 'minutes'
        cacheChangingModulesFor 4, 'hours'
    }
}

// 2. 依赖约束
dependencies {
    constraints {
        implementation 'org.springframework:spring-core:5.3.21'
        implementation 'org.springframework:spring-web:5.3.21'
    }
    
    implementation 'org.springframework:spring-webmvc' // 会使用约束的版本
}

// 3. BOM导入
dependencies {
    implementation platform('org.springframework.boot:spring-boot-dependencies:2.7.0')
    implementation 'org.springframework.boot:spring-boot-starter-web' // 版本由BOM管理
}

// 4. 依赖分析任务
task dependencyInsight(type: DependencyInsightReportTask) {
    doLast {
        println "Dependency insight for ${dependency}"
    }
}

// 查看依赖冲突
./gradlew dependencyInsight --dependency slf4j-api
./gradlew dependencies --configuration compileClasspath

// 5. 版本目录（Gradle 7+）
// gradle/libs.versions.toml
/*
[versions]
spring = "5.3.21"
junit = "5.8.2"

[libraries]
spring-core = { module = "org.springframework:spring-core", version.ref = "spring" }
spring-web = { module = "org.springframework:spring-web", version.ref = "spring" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }

[bundles]
spring = ["spring-core", "spring-web"]

[plugins]
spring-boot = { id = "org.springframework.boot", version = "2.7.0" }
*/

// build.gradle中使用
dependencies {
    implementation libs.spring.core
    implementation libs.bundles.spring
    testImplementation libs.junit.jupiter
}
'''
    
    print(f"\n依赖解析对比:")
    print("Poetry:")
    print("- SAT求解器智能解析")
    print("- 自动冲突检测")
    print("- 详细的锁定文件")
    print("- 语义化版本约束")
    
    print(f"\nGradle:")
    print("- 灵活的解析策略")
    print("- 强大的冲突解决机制")
    print("- BOM/Platform依赖管理")
    print("- 版本目录集中管理")
    print()


def demo_build_and_publish():
    """演示构建和发布流程"""
    print("=== 4. 构建和发布流程 ===")
    
    build_publish_example = '''
# Poetry构建和发布详解

# 1. 构建配置
class BuildManager:
    """构建管理器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.pyproject_file = self.project_path / "pyproject.toml"
    
    def configure_build(self):
        """配置构建"""
        build_config = {
            "tool": {
                "poetry": {
                    "name": "my-package",
                    "version": "1.0.0",
                    "description": "My awesome package",
                    "authors": ["Author <author@example.com>"],
                    "license": "MIT",
                    "readme": "README.md",
                    "homepage": "https://github.com/user/my-package",
                    "repository": "https://github.com/user/my-package",
                    "documentation": "https://my-package.readthedocs.io",
                    "keywords": ["python", "package"],
                    "classifiers": [
                        "Development Status :: 4 - Beta",
                        "Intended Audience :: Developers",
                        "License :: OSI Approved :: MIT License",
                        "Programming Language :: Python :: 3",
                        "Programming Language :: Python :: 3.8",
                        "Programming Language :: Python :: 3.9",
                        "Programming Language :: Python :: 3.10",
                    ],
                    
                    # 包含文件配置
                    "packages": [
                        {"include": "my_package", "from": "src"}
                    ],
                    "include": [
                        "CHANGELOG.md",
                        "LICENSE",
                        {"path": "data/*.json", "format": "wheel"},
                    ],
                    "exclude": [
                        "tests",
                        "docs",
                        "*.pyc",
                        "__pycache__",
                    ],
                    
                    # 脚本和入口点
                    "scripts": {
                        "my-cli": "my_package.cli:main"
                    },
                    "plugins": {
                        "my_package.plugins": {
                            "json": "my_package.plugins.json:JsonPlugin",
                            "yaml": "my_package.plugins.yaml:YamlPlugin",
                        }
                    }
                }
            },
            "build-system": {
                "requires": ["poetry-core>=1.0.0"],
                "build-backend": "poetry.core.masonry.api"
            }
        }
        
        with open(self.pyproject_file, 'w') as f:
            toml.dump(build_config, f)
        
        print("构建配置已更新")
    
    def build_package(self):
        """构建包"""
        print("开始构建包...")
        
        # 清理之前的构建
        dist_dir = self.project_path / "dist"
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        
        # 执行构建
        result = subprocess.run([
            "poetry", "build"
        ], cwd=self.project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("构建成功!")
            print(result.stdout)
            
            # 显示构建产物
            if dist_dir.exists():
                artifacts = list(dist_dir.glob("*"))
                print(f"构建产物:")
                for artifact in artifacts:
                    size = artifact.stat().st_size
                    print(f"  {artifact.name} ({size} bytes)")
        else:
            print(f"构建失败: {result.stderr}")
    
    def validate_package(self):
        """验证包"""
        print("验证包...")
        
        # 使用twine检查包
        dist_dir = self.project_path / "dist"
        if dist_dir.exists():
            result = subprocess.run([
                "twine", "check", str(dist_dir / "*")
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("包验证通过")
                print(result.stdout)
            else:
                print(f"包验证失败: {result.stderr}")

# 2. 发布配置
class PublishManager:
    """发布管理器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def configure_repositories(self):
        """配置仓库"""
        repositories = {
            "testpypi": {
                "url": "https://test.pypi.org/simple/",
                "username": "__token__",
                "password": "pypi-test-token"
            },
            "pypi": {
                "url": "https://pypi.org/simple/",
                "username": "__token__",
                "password": "pypi-prod-token"
            },
            "private": {
                "url": "https://pypi.company.com/simple/",
                "username": "company-user",
                "password": "company-pass"
            }
        }
        
        for name, config in repositories.items():
            # 配置仓库
            subprocess.run([
                "poetry", "config", f"repositories.{name}", config["url"]
            ])
            
            # 配置认证（实际使用中应该通过环境变量或keyring）
            print(f"配置仓库: {name}")
            print(f"  URL: {config['url']}")
            print(f"  用户名: {config['username']}")
    
    def publish_to_test(self):
        """发布到测试PyPI"""
        print("发布到测试PyPI...")
        
        result = subprocess.run([
            "poetry", "publish", "--repository", "testpypi"
        ], cwd=self.project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("发布到测试PyPI成功!")
            print(result.stdout)
        else:
            print(f"发布失败: {result.stderr}")
    
    def publish_to_pypi(self):
        """发布到PyPI"""
        print("发布到生产PyPI...")
        
        # 确认发布
        confirm = input("确认发布到生产环境? (y/N): ")
        if confirm.lower() != 'y':
            print("发布取消")
            return
        
        result = subprocess.run([
            "poetry", "publish"
        ], cwd=self.project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("发布成功!")
            print(result.stdout)
        else:
            print(f"发布失败: {result.stderr}")
    
    def publish_to_private(self, repository: str):
        """发布到私有仓库"""
        print(f"发布到私有仓库: {repository}")
        
        result = subprocess.run([
            "poetry", "publish", "--repository", repository
        ], cwd=self.project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("发布成功!")
        else:
            print(f"发布失败: {result.stderr}")

# 3. 版本管理
class VersionManager:
    """版本管理器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.pyproject_file = self.project_path / "pyproject.toml"
    
    def get_current_version(self) -> str:
        """获取当前版本"""
        with open(self.pyproject_file, 'r') as f:
            config = toml.load(f)
        
        return config['tool']['poetry']['version']
    
    def bump_version(self, bump_type: str):
        """版本升级"""
        valid_types = ['patch', 'minor', 'major', 'prepatch', 'preminor', 'premajor', 'prerelease']
        
        if bump_type not in valid_types:
            print(f"无效的版本类型: {bump_type}")
            print(f"有效类型: {', '.join(valid_types)}")
            return
        
        current_version = self.get_current_version()
        print(f"当前版本: {current_version}")
        
        result = subprocess.run([
            "poetry", "version", bump_type
        ], cwd=self.project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            new_version = self.get_current_version()
            print(f"版本已更新: {current_version} -> {new_version}")
            
            # 创建Git标签（如果是Git仓库）
            self._create_git_tag(new_version)
        else:
            print(f"版本更新失败: {result.stderr}")
    
    def _create_git_tag(self, version: str):
        """创建Git标签"""
        try:
            # 检查是否是Git仓库
            result = subprocess.run([
                "git", "rev-parse", "--git-dir"
            ], cwd=self.project_path, capture_output=True)
            
            if result.returncode == 0:
                # 创建标签
                subprocess.run([
                    "git", "tag", f"v{version}"
                ], cwd=self.project_path)
                print(f"已创建Git标签: v{version}")
        except Exception as e:
            print(f"创建Git标签失败: {e}")
    
    def set_version(self, version: str):
        """设置特定版本"""
        result = subprocess.run([
            "poetry", "version", version
        ], cwd=self.project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"版本已设置为: {version}")
        else:
            print(f"设置版本失败: {result.stderr}")

# 4. CI/CD集成
class CICDIntegration:
    """CI/CD集成"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def generate_github_workflow(self):
        """生成GitHub Actions工作流"""
        workflow_content = '''name: Build and Publish

on:
  push:
    branches: [ main ]
    tags: [ v* ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        virtualenvs-create: true
        virtualenvs-in-project: true
    
    - name: Load cached venv
      id: cached-poetry-dependencies
      uses: actions/cache@v3
      with:
        path: .venv
        key: venv-${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}
    
    - name: Install dependencies
      if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'
      run: poetry install --no-interaction --no-root
    
    - name: Install project
      run: poetry install --no-interaction
    
    - name: Run tests
      run: |
        poetry run pytest
        poetry run black --check .
        poetry run isort --check-only .
        poetry run flake8 .
        poetry run mypy src/
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
    
    - name: Build package
      run: poetry build
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/
  
  publish:
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
    
    - name: Download artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist
        path: dist/
    
    - name: Publish to PyPI
      env:
        POETRY_PYPI_TOKEN_PYPI: ${{ secrets.PYPI_TOKEN }}
      run: poetry publish
'''
        
        workflow_dir = self.project_path / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_file = workflow_dir / "build-and-publish.yml"
        workflow_file.write_text(workflow_content)
        
        print(f"GitHub Actions工作流已生成: {workflow_file}")
    
    def generate_gitlab_ci(self):
        """生成GitLab CI配置"""
        gitlab_ci_content = '''stages:
  - test
  - build
  - publish

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - .venv/

before_script:
  - apt-get update -qy
  - apt-get install -y python3-dev python3-pip
  - pip install poetry
  - poetry config virtualenvs.in-project true
  - poetry install

test:
  stage: test
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.8", "3.9", "3.10", "3.11"]
  image: python:${PYTHON_VERSION}
  script:
    - poetry run pytest
    - poetry run black --check .
    - poetry run isort --check-only .
    - poetry run flake8 .
    - poetry run mypy src/
  coverage: '/TOTAL.*\\s+(\\d+%)$/'

build:
  stage: build
  image: python:3.10
  script:
    - poetry build
  artifacts:
    paths:
      - dist/
  only:
    - tags

publish:
  stage: publish
  image: python:3.10
  script:
    - poetry config pypi-token.pypi $PYPI_TOKEN
    - poetry publish
  only:
    - tags
  when: manual
'''
        
        gitlab_ci_file = self.project_path / ".gitlab-ci.yml"
        gitlab_ci_file.write_text(gitlab_ci_content)
        
        print(f"GitLab CI配置已生成: {gitlab_ci_file}")

# 5. 使用示例
def build_publish_example():
    """构建发布示例"""
    project_path = "/tmp/example-project"
    
    # 构建管理
    build_manager = BuildManager(project_path)
    build_manager.configure_build()
    build_manager.build_package()
    build_manager.validate_package()
    
    # 版本管理
    version_manager = VersionManager(project_path)
    current = version_manager.get_current_version()
    print(f"当前版本: {current}")
    
    # 发布管理
    publish_manager = PublishManager(project_path)
    publish_manager.configure_repositories()
    
    # CI/CD集成
    cicd = CICDIntegration(project_path)
    cicd.generate_github_workflow()
    cicd.generate_gitlab_ci()
'''
    
    print("构建和发布特点:")
    print("1. 自动化的构建流程")
    print("2. 多仓库发布支持")
    print("3. 版本管理集成")
    print("4. CI/CD流水线自动化")
    print("5. 包验证和质量检查")
    
    # Gradle构建发布对比
    gradle_build_publish = '''
// Gradle构建发布对比

// 1. 发布配置
publishing {
    publications {
        maven(MavenPublication) {
            from components.java
            
            // 自定义Artifact ID
            artifactId = 'my-awesome-library'
            
            // 添加源码和文档
            artifact sourcesJar
            artifact javadocJar
            
            // POM配置
            pom {
                name = 'My Awesome Library'
                description = 'A concise description of my library'
                url = 'https://github.com/user/my-awesome-library'
                
                licenses {
                    license {
                        name = 'The Apache License, Version 2.0'
                        url = 'http://www.apache.org/licenses/LICENSE-2.0.txt'
                    }
                }
                
                developers {
                    developer {
                        id = 'user'
                        name = 'John Doe'
                        email = 'john@example.com'
                    }
                }
                
                scm {
                    connection = 'scm:git:git://github.com/user/my-awesome-library.git'
                    developerConnection = 'scm:git:ssh://github.com/user/my-awesome-library.git'
                    url = 'https://github.com/user/my-awesome-library'
                }
            }
        }
    }
    
    repositories {
        maven {
            name = "OSSRH"
            url = version.endsWith('SNAPSHOT') ? 
                'https://oss.sonatype.org/content/repositories/snapshots/' : 
                'https://oss.sonatype.org/service/local/staging/deploy/maven2/'
            
            credentials {
                username = project.findProperty("ossrhUsername") ?: ""
                password = project.findProperty("ossrhPassword") ?: ""
            }
        }
        
        maven {
            name = "GitHubPackages"
            url = "https://maven.pkg.github.com/user/my-awesome-library"
            credentials {
                username = project.findProperty("gpr.user") ?: System.getenv("USERNAME")
                password = project.findProperty("gpr.key") ?: System.getenv("TOKEN")
            }
        }
    }
}

// 2. 签名配置
signing {
    required { gradle.taskGraph.hasTask("publish") }
    sign publishing.publications.maven
}

// 3. 源码和文档JAR
java {
    withSourcesJar()
    withJavadocJar()
}

// 4. 版本管理插件
plugins {
    id 'net.researchgate.release' version '3.0.2'
}

release {
    tagTemplate = 'v$version'
    git {
        requireBranch = 'main'
        pushToRemote = 'origin'
    }
}

// 5. 质量检查
task qualityGate {
    dependsOn test, jacocoTestReport, spotbugsMain, checkstyleMain
    
    doLast {
        def coverageReport = file("$buildDir/reports/jacoco/test/jacocoTestReport.xml")
        if (coverageReport.exists()) {
            def coverage = new XmlSlurper().parse(coverageReport)
            def lineCoverage = coverage.counter.find { it.@type == 'LINE' }
            def ratio = lineCoverage.@covered.toFloat() / lineCoverage.@missed.toFloat()
            
            if (ratio < 0.8) {
                throw new GradleException("Code coverage below 80%: ${ratio * 100}%")
            }
        }
    }
}

// 6. 多环境构建
task buildForStaging {
    group = 'build'
    description = 'Build for staging environment'
    
    doFirst {
        project.version = "${project.version}-staging-${new Date().format('yyyyMMddHHmm')}"
    }
    
    finalizedBy build
}

// 7. Docker集成
task buildDockerImage(type: Exec) {
    dependsOn build
    commandLine 'docker', 'build', '-t', "${project.name}:${project.version}", '.'
}

task pushDockerImage(type: Exec) {
    dependsOn buildDockerImage
    commandLine 'docker', 'push', "${project.name}:${project.version}"
}

// 8. 发布任务
task publishToStaging {
    dependsOn build, buildDockerImage
    group = 'publishing'
    description = 'Publish to staging environment'
    
    doLast {
        println "Publishing ${project.name}:${project.version} to staging"
    }
}

task publishToProduction {
    dependsOn qualityGate, buildDockerImage
    group = 'publishing'
    description = 'Publish to production environment'
    
    doLast {
        println "Publishing ${project.name}:${project.version} to production"
    }
}

// Gradle命令示例
// ./gradlew build                     // 构建项目
// ./gradlew publish                   // 发布到配置的仓库
// ./gradlew publishToMavenLocal       // 发布到本地Maven仓库
// ./gradlew release                   // 版本发布（自动打标签）
// ./gradlew qualityGate               // 质量检查
// ./gradlew buildDockerImage          // 构建Docker镜像
'''
    
    print(f"\n构建发布对比:")
    print("Poetry:")
    print("- 统一的构建和发布工具")
    print("- 简化的配置和命令")
    print("- 自动依赖管理")
    print("- Python生态特化")
    
    print(f"\nGradle:")
    print("- 强大的构建自动化")
    print("- 丰富的插件生态")
    print("- 多项目支持")
    print("- 企业级发布流程")
    print()


def main():
    """主函数：运行所有演示"""
    print("Poetry现代包管理完整学习指南")
    print("=" * 50)
    
    demo_poetry_basics()
    demo_pyproject_toml()
    demo_dependency_resolution()
    demo_build_and_publish()
    
    print("学习总结:")
    print("1. Poetry提供现代化的Python包管理体验")
    print("2. pyproject.toml统一项目配置")
    print("3. 智能依赖解析和锁定机制")
    print("4. 简化的构建和发布流程")
    print("5. 与现代开发工具链无缝集成")
    print("6. 相比Gradle更专注于Python生态")


if __name__ == "__main__":
    main() 