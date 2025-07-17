#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pipenv环境管理详解
Pipenv Environment Management Guide

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习Pipenv的虚拟环境管理、依赖锁定、开发流程和对比分析

学习目标:
1. 掌握Pipenv的环境管理和依赖安装
2. 理解Pipfile和Pipfile.lock的作用
3. 学会开发和生产环境的分离管理
4. 对比不同包管理工具的优劣

注意：Pipenv曾是Python官方推荐的包管理工具
"""

import subprocess
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import os
import time


def demo_pipenv_basics():
    """演示Pipenv基础操作"""
    print("=== 1. Pipenv基础操作 ===")
    
    basic_operations = '''
# Pipenv基础命令详解

# 1. 安装Pipenv
pip install pipenv
# 或者使用系统包管理器
# macOS: brew install pipenv
# Ubuntu: sudo apt install pipenv

# 验证安装
pipenv --version

# 2. 项目初始化
pipenv --python 3.10           # 创建指定Python版本的环境
pipenv --python python3        # 使用系统默认Python3
pipenv --python /usr/bin/python3.9  # 使用特定Python路径

# 在现有项目中初始化
cd my-project
pipenv install                  # 创建虚拟环境并安装依赖

# 3. 依赖管理
pipenv install requests         # 安装生产依赖
pipenv install pytest --dev    # 安装开发依赖
pipenv install django==4.1.0   # 安装指定版本
pipenv install -r requirements.txt  # 从requirements.txt安装

# 安装所有依赖
pipenv install                  # 只安装生产依赖
pipenv install --dev           # 安装所有依赖（包括开发依赖）

# 4. 环境激活和使用
pipenv shell                    # 激活虚拟环境
pipenv run python script.py    # 在环境中运行命令
pipenv run pip list            # 在环境中运行pip命令
pipenv run pytest              # 在环境中运行测试

# 5. 依赖操作
pipenv uninstall requests      # 卸载依赖
pipenv uninstall --all         # 卸载所有依赖
pipenv uninstall --all-dev     # 卸载所有开发依赖
pipenv clean                   # 清理未在Pipfile中列出的包

# 6. 环境信息
pipenv --where                 # 显示项目目录
pipenv --venv                  # 显示虚拟环境路径
pipenv --py                    # 显示Python解释器路径
pipenv graph                   # 显示依赖图
pipenv check                   # 检查安全漏洞

# 7. 锁定和同步
pipenv lock                    # 生成Pipfile.lock
pipenv sync                    # 从Pipfile.lock同步环境
pipenv sync --dev             # 同步包含开发依赖

# 8. 环境管理
pipenv --rm                    # 删除虚拟环境
pipenv --clear                 # 清除缓存

# 9. 导出依赖
pipenv requirements > requirements.txt        # 导出生产依赖
pipenv requirements --dev > dev-requirements.txt  # 导出开发依赖

# 10. 高级选项
pipenv install --skip-lock     # 跳过锁定文件生成
pipenv install --system        # 安装到系统而非虚拟环境
pipenv install --ignore-pipfile  # 忽略Pipfile，从锁定文件安装
'''
    
    print("Pipenv基础特点:")
    print("1. 自动管理虚拟环境")
    print("2. Pipfile替代requirements.txt")
    print("3. 依赖锁定确保一致性")
    print("4. 开发和生产依赖分离")
    print("5. 安全漏洞检查")
    
    # 包管理工具对比
    tools_comparison = '''
# Python包管理工具对比

## 1. pip + venv (传统方案)
# 优点：
- Python标准库内置
- 简单直接，学习成本低
- 与所有Python工具兼容

# 缺点：
- 需要手动管理虚拟环境
- requirements.txt功能有限
- 缺乏依赖锁定机制
- 无内置安全检查

## 2. Pipenv
# 优点：
- 自动虚拟环境管理
- Pipfile现代化依赖声明
- 确定性构建（Pipfile.lock）
- 内置安全漏洞检查
- 开发/生产依赖分离

# 缺点：
- 依赖解析较慢
- 与某些CI/CD工具集成复杂
- 社区维护不够活跃
- 不支持构建和发布

## 3. Poetry
# 优点：
- 现代化项目管理
- 快速依赖解析
- 内置构建和发布
- 优秀的文档和社区支持
- 灵活的依赖组管理

# 缺点：
- 学习曲线相对陡峭
- 配置文件格式独特（pyproject.toml）
- 可能与某些遗留项目不兼容

## 4. conda
# 优点：
- 跨语言包管理
- 科学计算生态支持好
- 二进制包分发
- 强大的环境隔离

# 缺点：
- 体积较大
- 主要面向数据科学
- 包更新可能较慢
- 与pip生态有时冲突

## 5. PDM
# 优点：
- 符合PEP 582标准
- 快速依赖解析
- 现代化设计
- 支持PEP 621

# 缺点：
- 相对较新，生态不够成熟
- 社区和文档相对较少
'''
    
    print(f"\n包管理工具特点对比:")
    print("pip + venv: 简单传统，适合初学者")
    print("Pipenv: 自动化环境管理，适合中小项目")
    print("Poetry: 现代化全功能，适合新项目")
    print("conda: 科学计算专用，适合数据科学")
    print("PDM: 未来标准，适合探索新技术")
    print()


def demo_pipfile_configuration():
    """演示Pipfile配置详解"""
    print("=== 2. Pipfile配置详解 ===")
    
    pipfile_example = '''
# Pipfile完整配置示例

[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[[source]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple/"
verify_ssl = true
name = "tsinghua"

[[source]]
url = "https://pypi.company.com/simple"
verify_ssl = true
name = "company"
username = "user"
password = "pass"

[packages]
# 基础依赖
requests = "*"                          # 任何版本
django = ">=4.0,<5.0"                  # 版本范围
psycopg2-binary = "~=2.9.0"            # 兼容版本
redis = "==4.3.4"                      # 精确版本

# Git依赖
my-private-lib = {git = "https://github.com/user/private-lib.git", ref = "main"}
feature-branch-lib = {git = "https://github.com/user/lib.git", ref = "feature-branch"}
tagged-lib = {git = "https://github.com/user/lib.git", ref = "v1.2.3"}

# 本地依赖
local-utils = {path = "../utils", editable = true}

# 可选依赖
celery = {extras = ["redis"], version = "*"}

# 条件依赖
pywin32 = {version = "*", markers = "sys_platform == 'win32'"}
uvloop = {version = "*", markers = "sys_platform != 'win32'"}

# 指定源
special-package = {version = "*", index = "company"}

[dev-packages]
# 测试工具
pytest = "*"
pytest-django = "*"
pytest-cov = "*"
pytest-mock = "*"
factory-boy = "*"

# 代码质量
black = "*"
isort = "*"
flake8 = "*"
mypy = "*"
bandit = "*"                           # 安全检查

# 开发工具
ipython = "*"
jupyter = "*"
django-debug-toolbar = "*"
django-extensions = "*"

# 文档工具
sphinx = "*"
sphinx-rtd-theme = "*"

[requires]
python_version = "3.10"

[scripts]
# 自定义脚本
start = "python manage.py runserver"
test = "pytest"
lint = "flake8 ."
format = "black ."
type-check = "mypy src/"
security = "bandit -r src/"
docs = "sphinx-build docs/ docs/_build/"

[pipenv]
# Pipenv特定配置
allow_prereleases = true               # 允许预发布版本
'''
    
    print("Pipfile配置特点:")
    print("1. TOML格式配置文件")
    print("2. 多源仓库支持")
    print("3. 生产和开发依赖分离")
    print("4. 丰富的依赖声明语法")
    print("5. 自定义脚本定义")


class PipenvProjectManager:
    """Pipenv项目管理器"""
    
    def __init__(self, project_name: str, project_path: Optional[str] = None):
        self.project_name = project_name
        self.project_path = Path(project_path or tempfile.mkdtemp()) / project_name
        
    def create_project_structure(self):
        """创建项目结构"""
        # 创建项目目录
        self.project_path.mkdir(parents=True, exist_ok=True)
        
        # 创建Pipfile
        pipfile_content = self._generate_pipfile()
        (self.project_path / "Pipfile").write_text(pipfile_content)
        
        # 创建源代码目录
        src_dir = self.project_path / "src" / self.project_name.replace("-", "_")
        src_dir.mkdir(parents=True, exist_ok=True)
        (src_dir / "__init__.py").write_text(f'"""\\n{self.project_name} package\\n"""\\n')
        
        # 创建测试目录
        tests_dir = self.project_path / "tests"
        tests_dir.mkdir(exist_ok=True)
        (tests_dir / "__init__.py").write_text("")
        (tests_dir / "test_basic.py").write_text(self._generate_basic_test())
        
        # 创建配置文件
        (self.project_path / ".env.example").write_text(self._generate_env_example())
        (self.project_path / ".gitignore").write_text(self._generate_gitignore())
        
        print(f"项目结构已创建: {self.project_path}")
        
    def _generate_pipfile(self) -> str:
        """生成Pipfile"""
        return '''[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"

[dev-packages]
pytest = "*"
black = "*"
flake8 = "*"

[requires]
python_version = "3.10"

[scripts]
test = "pytest"
lint = "flake8 src/"
format = "black src/ tests/"
'''
        
    def _generate_basic_test(self) -> str:
        """生成基础测试"""
        return '''import pytest


def test_basic():
    """基础测试"""
    assert True


def test_imports():
    """测试导入"""
    import requests
    assert hasattr(requests, 'get')
'''
        
    def _generate_env_example(self) -> str:
        """生成环境变量示例"""
        return '''# 环境变量示例文件
# 复制为.env并填入实际值

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis配置
REDIS_URL=redis://localhost:6379/0

# 密钥配置
SECRET_KEY=your-secret-key-here

# 调试模式
DEBUG=True

# 邮件配置
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
'''
        
    def _generate_gitignore(self) -> str:
        """生成.gitignore"""
        return '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Environment variables
.env

# Virtual environments
.venv/
venv/

# IDE
.vscode/
.idea/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Build
build/
dist/
*.egg-info/
'''

    def initialize_environment(self):
        """初始化Pipenv环境"""
        print("初始化Pipenv环境...")
        
        os.chdir(self.project_path)
        
        # 安装依赖
        result = subprocess.run([
            "pipenv", "install", "--dev"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("依赖安装成功")
            print(result.stdout)
        else:
            print(f"安装失败: {result.stderr}")
    
    def show_environment_info(self):
        """显示环境信息"""
        os.chdir(self.project_path)
        
        commands = [
            ("项目目录", ["pipenv", "--where"]),
            ("虚拟环境路径", ["pipenv", "--venv"]),
            ("Python路径", ["pipenv", "--py"]),
            ("依赖图", ["pipenv", "graph"]),
        ]
        
        for name, cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{name}: {result.stdout.strip()}")
            else:
                print(f"{name}: 获取失败")


def demo_dependency_locking():
    """演示依赖锁定机制"""
    print("=== 3. 依赖锁定机制 ===")
    
    locking_mechanism = '''
# Pipenv依赖锁定详解

# 1. Pipfile.lock结构分析
class PipfileLockAnalyzer:
    """Pipfile.lock分析器"""
    
    def __init__(self, lock_file_path: str):
        self.lock_file_path = Path(lock_file_path)
    
    def analyze_lock_file(self):
        """分析锁定文件"""
        if not self.lock_file_path.exists():
            print("Pipfile.lock不存在")
            return
        
        with open(self.lock_file_path, 'r') as f:
            lock_data = json.load(f)
        
        print("=== Pipfile.lock分析 ===")
        
        # 元数据分析
        meta = lock_data.get('_meta', {})
        print(f"生成工具: {meta.get('pipfile-spec', 'unknown')}")
        print(f"Python版本: {meta.get('requires', {}).get('python_version', 'unknown')}")
        print(f"Pipfile哈希: {meta.get('hash', {}).get('sha256', 'unknown')[:16]}...")
        
        # 源分析
        sources = meta.get('sources', [])
        print(f"\\n配置的源数量: {len(sources)}")
        for i, source in enumerate(sources):
            print(f"  源{i+1}: {source.get('name')} - {source.get('url')}")
        
        # 依赖分析
        default_deps = lock_data.get('default', {})
        develop_deps = lock_data.get('develop', {})
        
        print(f"\\n生产依赖: {len(default_deps)} 个")
        print(f"开发依赖: {len(develop_deps)} 个")
        print(f"总依赖数: {len(default_deps) + len(develop_deps)} 个")
        
        # 详细依赖信息
        self._analyze_dependencies("生产依赖", default_deps)
        self._analyze_dependencies("开发依赖", develop_deps)
        
        return lock_data
    
    def _analyze_dependencies(self, category: str, dependencies: Dict):
        """分析依赖详情"""
        if not dependencies:
            return
        
        print(f"\\n=== {category}详情 ===")
        
        # 按来源分类
        sources = {}
        hashed_count = 0
        
        for name, info in dependencies.items():
            source = info.get('index', 'pypi')
            if source not in sources:
                sources[source] = []
            sources[source].append(name)
            
            if 'hashes' in info:
                hashed_count += 1
        
        print(f"带哈希验证的包: {hashed_count}/{len(dependencies)}")
        
        for source, packages in sources.items():
            print(f"{source}源: {len(packages)} 个包")
            for pkg in sorted(packages)[:5]:  # 只显示前5个
                version = dependencies[pkg].get('version', 'unknown')
                print(f"  {pkg} {version}")
            if len(packages) > 5:
                print(f"  ... 还有 {len(packages) - 5} 个包")
    
    def check_integrity(self, pipfile_path: str):
        """检查完整性"""
        if not Path(pipfile_path).exists():
            print("Pipfile不存在")
            return False
        
        # 比较Pipfile和Pipfile.lock的一致性
        with open(pipfile_path, 'r') as f:
            pipfile_content = f.read()
        
        with open(self.lock_file_path, 'r') as f:
            lock_data = json.load(f)
        
        # 检查Pipfile哈希
        import hashlib
        pipfile_hash = hashlib.sha256(pipfile_content.encode()).hexdigest()
        lock_hash = lock_data.get('_meta', {}).get('hash', {}).get('sha256', '')
        
        if pipfile_hash == lock_hash:
            print("✓ Pipfile和Pipfile.lock一致")
            return True
        else:
            print("✗ Pipfile和Pipfile.lock不一致，需要重新锁定")
            return False
    
    def find_security_issues(self, dependencies: Dict):
        """查找安全问题（简化实现）"""
        print("\\n=== 安全问题检查 ===")
        
        # 模拟安全漏洞数据库
        vulnerable_packages = {
            'django': ['3.2.0', '3.2.1'],  # 示例漏洞版本
            'requests': ['2.25.0'],
            'pillow': ['8.0.0', '8.0.1'],
        }
        
        issues_found = []
        
        for pkg_name, pkg_info in dependencies.items():
            version = pkg_info.get('version', '').lstrip('==')
            
            if pkg_name in vulnerable_packages:
                if version in vulnerable_packages[pkg_name]:
                    issues_found.append({
                        'package': pkg_name,
                        'version': version,
                        'vulnerability': f'已知安全漏洞'
                    })
        
        if issues_found:
            print(f"发现 {len(issues_found)} 个安全问题:")
            for issue in issues_found:
                print(f"  {issue['package']} {issue['version']}: {issue['vulnerability']}")
        else:
            print("未发现已知安全问题")
        
        return issues_found

# 2. 锁定文件生成和管理
class LockFileManager:
    """锁定文件管理器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.pipfile = self.project_path / "Pipfile"
        self.lock_file = self.project_path / "Pipfile.lock"
    
    def generate_lock_file(self, dev: bool = True):
        """生成锁定文件"""
        print("生成Pipfile.lock...")
        
        os.chdir(self.project_path)
        
        cmd = ["pipenv", "lock"]
        if dev:
            cmd.append("--dev")
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        end_time = time.time()
        
        if result.returncode == 0:
            print(f"锁定文件生成成功 (耗时: {end_time - start_time:.1f}秒)")
            
            # 显示统计信息
            self._show_lock_stats()
        else:
            print(f"生成失败: {result.stderr}")
    
    def _show_lock_stats(self):
        """显示锁定统计"""
        if self.lock_file.exists():
            with open(self.lock_file, 'r') as f:
                lock_data = json.load(f)
            
            default_count = len(lock_data.get('default', {}))
            develop_count = len(lock_data.get('develop', {}))
            
            print(f"锁定依赖统计:")
            print(f"  生产依赖: {default_count}")
            print(f"  开发依赖: {develop_count}")
            print(f"  总计: {default_count + develop_count}")
    
    def update_lock_file(self, packages: List[str] = None):
        """更新锁定文件"""
        print("更新依赖锁定...")
        
        os.chdir(self.project_path)
        
        if packages:
            # 更新特定包
            for package in packages:
                cmd = ["pipenv", "update", package]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✓ {package} 更新成功")
                else:
                    print(f"✗ {package} 更新失败: {result.stderr}")
        else:
            # 更新所有依赖
            result = subprocess.run([
                "pipenv", "update"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("所有依赖更新成功")
            else:
                print(f"更新失败: {result.stderr}")
    
    def sync_from_lock(self, dev: bool = True):
        """从锁定文件同步环境"""
        print("从Pipfile.lock同步环境...")
        
        os.chdir(self.project_path)
        
        cmd = ["pipenv", "sync"]
        if dev:
            cmd.append("--dev")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("环境同步成功")
        else:
            print(f"同步失败: {result.stderr}")
    
    def verify_lock_integrity(self):
        """验证锁定文件完整性"""
        print("验证锁定文件完整性...")
        
        os.chdir(self.project_path)
        
        result = subprocess.run([
            "pipenv", "verify"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ 锁定文件完整性验证通过")
        else:
            print("✗ 锁定文件完整性验证失败")
            print(result.stderr)

# 3. 环境一致性保证
class EnvironmentConsistency:
    """环境一致性管理"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def create_reproducible_environment(self):
        """创建可重现环境"""
        print("创建可重现环境的最佳实践:")
        
        practices = [
            "1. 始终使用Pipfile.lock进行部署",
            "2. 定期更新依赖并测试兼容性",
            "3. 使用具体的Python版本约束",
            "4. 启用哈希验证确保包完整性",
            "5. 在CI/CD中使用pipenv sync",
            "6. 定期检查安全漏洞",
            "7. 文档化特殊依赖要求",
            "8. 使用.env文件管理环境变量"
        ]
        
        for practice in practices:
            print(f"  {practice}")
    
    def generate_deployment_script(self):
        """生成部署脚本"""
        script_content = '''#!/bin/bash
# Pipenv部署脚本

set -e  # 遇到错误立即退出

echo "开始部署..."

# 1. 检查Python版本
python_version=$(python3 --version | cut -d' ' -f2)
echo "Python版本: $python_version"

# 2. 安装pipenv（如果未安装）
if ! command -v pipenv &> /dev/null; then
    echo "安装pipenv..."
    pip install pipenv
fi

# 3. 设置环境变量
export PIPENV_VENV_IN_PROJECT=1  # 在项目目录创建.venv
export PIPENV_SKIP_LOCK=1        # 跳过锁定文件检查（生产环境）

# 4. 安装依赖
echo "安装依赖..."
pipenv sync  # 只安装生产依赖

# 5. 运行健康检查
echo "运行健康检查..."
pipenv run python -c "import django; print('Django版本:', django.get_version())"

# 6. 数据库迁移（如果是Django项目）
if [ -f "manage.py" ]; then
    echo "运行数据库迁移..."
    pipenv run python manage.py migrate --noinput
fi

# 7. 收集静态文件（如果是Django项目）
if [ -f "manage.py" ]; then
    echo "收集静态文件..."
    pipenv run python manage.py collectstatic --noinput
fi

echo "部署完成!"
'''
        
        script_file = self.project_path / "deploy.sh"
        script_file.write_text(script_content)
        script_file.chmod(0o755)
        
        print(f"部署脚本已生成: {script_file}")
    
    def generate_dockerfile(self):
        """生成Dockerfile"""
        dockerfile_content = '''FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# 安装pipenv
RUN pip install pipenv

# 复制依赖文件
COPY Pipfile Pipfile.lock ./

# 设置环境变量
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_DONT_LOAD_ENV=1

# 安装依赖
RUN pipenv sync

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
'''
        
        dockerfile = self.project_path / "Dockerfile"
        dockerfile.write_text(dockerfile_content)
        
        print(f"Dockerfile已生成: {dockerfile}")

# 4. 使用示例
def dependency_locking_example():
    """依赖锁定示例"""
    project_path = "/tmp/pipenv-example"
    
    # 锁定文件管理
    lock_manager = LockFileManager(project_path)
    lock_manager.generate_lock_file()
    lock_manager.verify_lock_integrity()
    
    # 环境一致性
    consistency = EnvironmentConsistency(project_path)
    consistency.create_reproducible_environment()
    consistency.generate_deployment_script()
    consistency.generate_dockerfile()
'''
    
    print("依赖锁定特点:")
    print("1. 确定性构建保证")
    print("2. 哈希验证确保完整性")
    print("3. 详细的依赖关系记录")
    print("4. 安全漏洞检查")
    print("5. 环境一致性保证")


def demo_development_workflow():
    """演示开发工作流程"""
    print("=== 4. 开发工作流程 ===")
    
    workflow_example = '''
# Pipenv开发工作流程详解

# 1. 项目开发生命周期
class DevelopmentWorkflow:
    """开发工作流程管理"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def setup_new_project(self):
        """新项目设置"""
        print("=== 新项目设置流程 ===")
        
        steps = [
            "1. 创建项目目录",
            "2. 初始化Git仓库",
            "3. 创建Pipfile（pipenv --python 3.10）",
            "4. 安装基础依赖（pipenv install requests django）",
            "5. 安装开发依赖（pipenv install pytest black --dev）",
            "6. 创建项目结构",
            "7. 生成配置文件（.env.example, .gitignore）",
            "8. 首次提交代码"
        ]
        
        for step in steps:
            print(f"  {step}")
    
    def daily_development_cycle(self):
        """日常开发循环"""
        print("\\n=== 日常开发循环 ===")
        
        cycle = [
            "1. 激活环境：pipenv shell",
            "2. 拉取最新代码：git pull",
            "3. 同步依赖：pipenv sync --dev",
            "4. 运行测试：pipenv run pytest",
            "5. 开发新功能",
            "6. 添加新依赖（如需要）：pipenv install package-name",
            "7. 运行代码检查：pipenv run flake8",
            "8. 格式化代码：pipenv run black .",
            "9. 运行测试确保无回归",
            "10. 提交代码：git commit",
            "11. 推送代码：git push"
        ]
        
        for step in cycle:
            print(f"  {step}")
    
    def dependency_management_workflow(self):
        """依赖管理工作流"""
        print("\\n=== 依赖管理工作流 ===")
        
        scenarios = {
            "添加新依赖": [
                "pipenv install package-name",
                "测试功能是否正常",
                "提交Pipfile和Pipfile.lock"
            ],
            "更新依赖": [
                "pipenv update package-name",
                "运行全量测试",
                "检查是否有破坏性变更",
                "更新文档（如需要）"
            ],
            "移除依赖": [
                "pipenv uninstall package-name",
                "检查代码中是否还有引用",
                "运行测试确保无错误",
                "清理未使用的依赖：pipenv clean"
            ],
            "安全更新": [
                "检查漏洞：pipenv check",
                "更新有漏洞的包",
                "验证修复效果",
                "重新运行安全检查"
            ]
        }
        
        for scenario, steps in scenarios.items():
            print(f"\\n{scenario}:")
            for step in steps:
                print(f"  • {step}")
    
    def environment_management_best_practices(self):
        """环境管理最佳实践"""
        print("\\n=== 环境管理最佳实践 ===")
        
        practices = {
            "开发环境": [
                "使用pipenv shell激活环境",
                "设置PIPENV_VENV_IN_PROJECT=1在项目内创建.venv",
                "配置IDE使用虚拟环境中的Python",
                "使用.env文件管理环境变量",
                "定期运行pipenv clean清理未使用的包"
            ],
            "测试环境": [
                "使用pipenv sync --dev安装所有依赖",
                "运行完整的测试套件",
                "验证环境一致性",
                "检查代码覆盖率",
                "进行安全扫描"
            ],
            "生产环境": [
                "使用pipenv sync只安装生产依赖",
                "设置PIPENV_DONT_LOAD_ENV=1避免加载.env",
                "使用pipenv verify验证依赖完整性",
                "监控应用性能",
                "定期更新依赖修复安全漏洞"
            ]
        }
        
        for env, practices_list in practices.items():
            print(f"\\n{env}:")
            for practice in practices_list:
                print(f"  • {practice}")

# 2. 多环境配置管理
class MultiEnvironmentConfig:
    """多环境配置管理"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def create_environment_configs(self):
        """创建环境配置文件"""
        
        # 开发环境配置
        dev_env = '''# 开发环境配置
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=DEBUG
ALLOWED_HOSTS=localhost,127.0.0.1
'''
        
        # 测试环境配置
        test_env = '''# 测试环境配置
DEBUG=False
DATABASE_URL=sqlite:///:memory:
REDIS_URL=redis://localhost:6379/1
LOG_LEVEL=INFO
ALLOWED_HOSTS=test.example.com
'''
        
        # 生产环境配置
        prod_env = '''# 生产环境配置
DEBUG=False
DATABASE_URL=postgresql://user:pass@prod-db:5432/myapp
REDIS_URL=redis://prod-redis:6379/0
LOG_LEVEL=WARNING
ALLOWED_HOSTS=myapp.com,www.myapp.com
'''
        
        configs = {
            ".env.dev": dev_env,
            ".env.test": test_env,
            ".env.prod": prod_env,
        }
        
        for filename, content in configs.items():
            config_file = self.project_path / filename
            config_file.write_text(content)
            print(f"已创建配置文件: {filename}")
    
    def create_environment_scripts(self):
        """创建环境脚本"""
        
        # 开发脚本
        dev_script = '''#!/bin/bash
# 开发环境启动脚本

export PIPENV_DOTENV_LOCATION=.env.dev

echo "启动开发环境..."
pipenv run python manage.py migrate
pipenv run python manage.py runserver
'''
        
        # 测试脚本
        test_script = '''#!/bin/bash
# 测试环境脚本

export PIPENV_DOTENV_LOCATION=.env.test

echo "运行测试..."
pipenv run pytest --cov=src --cov-report=html
pipenv run black --check .
pipenv run flake8 .
'''
        
        # 生产部署脚本
        prod_script = '''#!/bin/bash
# 生产环境部署脚本

export PIPENV_DOTENV_LOCATION=.env.prod

echo "生产环境部署..."
pipenv sync  # 只安装生产依赖
pipenv run python manage.py migrate
pipenv run python manage.py collectstatic --noinput
pipenv run gunicorn myapp.wsgi:application
'''
        
        scripts = {
            "dev.sh": dev_script,
            "test.sh": test_script,
            "prod.sh": prod_script,
        }
        
        for filename, content in scripts.items():
            script_file = self.project_path / filename
            script_file.write_text(content)
            script_file.chmod(0o755)
            print(f"已创建脚本文件: {filename}")

# 3. 团队协作工作流
class TeamCollaborationWorkflow:
    """团队协作工作流"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def setup_team_standards(self):
        """设置团队标准"""
        print("=== 团队协作标准 ===")
        
        standards = {
            "依赖管理": [
                "所有依赖必须通过Pipfile管理",
                "提交代码时必须包含Pipfile.lock",
                "添加新依赖前需要团队讨论",
                "定期更新依赖并测试兼容性",
                "生产环境只能从Pipfile.lock安装"
            ],
            "代码质量": [
                "使用black进行代码格式化",
                "使用flake8进行代码检查",
                "使用mypy进行类型检查",
                "保持测试覆盖率在80%以上",
                "所有公共方法必须有文档字符串"
            ],
            "环境管理": [
                "统一使用指定的Python版本",
                "本地开发使用pipenv shell",
                "CI/CD使用pipenv sync",
                "环境变量使用.env文件管理",
                "不要提交.env文件到版本控制"
            ]
        }
        
        for category, rules in standards.items():
            print(f"\\n{category}:")
            for rule in rules:
                print(f"  • {rule}")
    
    def create_pre_commit_hooks(self):
        """创建预提交钩子"""
        pre_commit_config = '''repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8

  - repo: local
    hooks:
      - id: pipenv-check
        name: pipenv check
        entry: pipenv check
        language: system
        pass_filenames: false
        always_run: true
'''
        
        config_file = self.project_path / ".pre-commit-config.yaml"
        config_file.write_text(pre_commit_config)
        
        print(f"预提交配置已创建: {config_file}")
        print("安装预提交钩子: pipenv run pre-commit install")
    
    def create_ci_pipeline(self):
        """创建CI流水线"""
        github_workflow = '''name: CI

on:
  push:
    branches: [ main, develop ]
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
    
    - name: Install pipenv
      run: |
        python -m pip install --upgrade pip
        pip install pipenv
    
    - name: Cache pipenv dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pipenv
        key: ${{ runner.os }}-pipenv-${{ hashFiles('Pipfile.lock') }}
        restore-keys: |
          ${{ runner.os }}-pipenv-
    
    - name: Install dependencies
      run: |
        pipenv sync --dev
    
    - name: Run linting
      run: |
        pipenv run flake8 .
        pipenv run black --check .
        pipenv run isort --check-only .
    
    - name: Run type checking
      run: |
        pipenv run mypy src/
    
    - name: Run tests
      run: |
        pipenv run pytest --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    
    - name: Security check
      run: |
        pipenv check
'''
        
        workflow_dir = self.project_path / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_file = workflow_dir / "ci.yml"
        workflow_file.write_text(github_workflow)
        
        print(f"CI流水线已创建: {workflow_file}")

# 4. 使用示例
def development_workflow_example():
    """开发工作流示例"""
    project_path = "/tmp/workflow-example"
    
    # 开发工作流
    workflow = DevelopmentWorkflow(project_path)
    workflow.setup_new_project()
    workflow.daily_development_cycle()
    workflow.dependency_management_workflow()
    workflow.environment_management_best_practices()
    
    # 多环境配置
    multi_env = MultiEnvironmentConfig(project_path)
    multi_env.create_environment_configs()
    multi_env.create_environment_scripts()
    
    # 团队协作
    team_workflow = TeamCollaborationWorkflow(project_path)
    team_workflow.setup_team_standards()
    team_workflow.create_pre_commit_hooks()
    team_workflow.create_ci_pipeline()
'''
    
    print("开发工作流特点:")
    print("1. 自动化环境管理")
    print("2. 明确的依赖管理流程")
    print("3. 多环境配置支持")
    print("4. 团队协作标准化")
    print("5. CI/CD集成")


def demo_tool_comparison():
    """演示工具对比分析"""
    print("=== 5. 包管理工具对比分析 ===")
    
    comparison_table = '''
# Python包管理工具详细对比

## 功能对比表

| 功能 | pip+venv | Pipenv | Poetry | conda | PDM |
|------|----------|--------|--------|--------|-----|
| 依赖管理 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 虚拟环境 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 依赖锁定 | ❌ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 构建发布 | ❌ | ❌ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 学习曲线 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 社区支持 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| 生态兼容性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 安全特性 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| CI/CD友好 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 适用场景分析

### pip + venv
**适用场景:**
- 学习Python和简单项目
- 遗留项目维护
- 对工具链有严格要求的环境
- 需要最大兼容性的场景

**优势:**
- Python标准库内置，无需额外安装
- 简单直接，学习成本最低
- 与所有Python工具和环境兼容
- 稳定可靠，不会有兼容性问题

**劣势:**
- 需要手动管理虚拟环境
- 缺乏现代化的依赖管理功能
- 无依赖锁定机制
- 配置分散，维护困难

### Pipenv
**适用场景:**
- 中小型Django/Flask项目
- 团队开发需要环境一致性
- 重视依赖安全性的项目
- 不需要发布包的应用项目

**优势:**
- 自动虚拟环境管理
- Pipfile现代化配置格式
- 确定性构建（Pipfile.lock）
- 内置安全漏洞检查
- 开发/生产依赖分离清晰

**劣势:**
- 依赖解析性能较差
- 社区维护活跃度下降
- 不支持包构建和发布
- 某些复杂依赖场景处理不佳

### Poetry
**适用场景:**
- 新项目开发
- 需要发布Python包的项目
- 现代化开发流程
- 复杂的依赖管理需求

**优势:**
- 现代化的项目管理工具
- 快速的依赖解析算法
- 内置构建和发布功能
- 优秀的文档和社区支持
- 统一的配置文件（pyproject.toml）

**劣势:**
- 学习曲线相对陡峭
- 与某些传统工具可能有冲突
- 配置文件格式相对复杂

### conda
**适用场景:**
- 数据科学和机器学习项目
- 需要非Python依赖的项目
- 跨平台科学计算环境
- 大型数据处理项目

**优势:**
- 跨语言包管理（Python、R、C++等）
- 二进制包分发，安装速度快
- 强大的环境隔离
- 科学计算生态支持完善

**劣势:**
- 安装包体积大
- 与纯Python生态可能有冲突
- 包更新频率相对较慢
- 主要面向科学计算领域

### PDM
**适用场景:**
- 追求最新标准的项目
- 需要高性能依赖解析的大型项目
- 实验性项目
- 对PEP标准兼容性要求高的项目

**优势:**
- 符合最新PEP标准
- 高性能依赖解析
- 现代化设计理念
- 支持PEP 621项目元数据

**劣势:**
- 相对较新，生态不够成熟
- 社区和文档相对较少
- 某些功能还在开发中

## 选择建议

### 项目类型
- **学习项目**: pip + venv
- **Web应用**: Pipenv 或 Poetry
- **Python包**: Poetry
- **数据科学**: conda
- **企业应用**: Poetry 或 Pipenv
- **实验项目**: PDM

### 团队规模
- **个人开发**: pip + venv 或 Poetry
- **小团队**: Pipenv
- **大团队**: Poetry
- **企业级**: Poetry 或 conda

### 技术栈
- **纯Python**: Poetry
- **Python + 系统依赖**: conda
- **多语言**: conda
- **容器化**: Poetry 或 Pipenv

## 迁移策略

### 从pip迁移到Poetry
1. 创建pyproject.toml
2. 使用poetry add逐步添加依赖
3. 删除requirements.txt
4. 更新CI/CD脚本

### 从Pipenv迁移到Poetry
1. 导出依赖：pipenv requirements > requirements.txt
2. 初始化Poetry项目：poetry init
3. 导入依赖：poetry add $(cat requirements.txt)
4. 删除Pipfile和Pipfile.lock

### 从conda迁移到Poetry
1. 导出环境：conda env export > environment.yml
2. 提取Python依赖
3. 使用Poetry重新管理Python依赖
4. 保留conda管理系统级依赖
'''
    
    print("包管理工具选择要点:")
    print("1. 根据项目类型和规模选择")
    print("2. 考虑团队技术栈和经验")
    print("3. 评估长期维护成本")
    print("4. 兼顾性能和功能需求")
    print("5. 重视社区支持和生态")
    
    # 决策矩阵
    decision_matrix = {
        "简单脚本": "pip + venv",
        "Web应用开发": "Poetry",
        "数据科学项目": "conda", 
        "Python包开发": "Poetry",
        "遗留项目维护": "pip + venv",
        "团队协作项目": "Poetry",
        "实验性项目": "PDM",
        "企业级应用": "Poetry"
    }
    
    print(f"\n快速决策参考:")
    for scenario, tool in decision_matrix.items():
        print(f"  {scenario}: 推荐 {tool}")


def main():
    """主函数：运行所有演示"""
    print("Pipenv环境管理完整学习指南")
    print("=" * 50)
    
    demo_pipenv_basics()
    demo_pipfile_configuration()
    demo_dependency_locking()
    demo_development_workflow()
    demo_tool_comparison()
    
    # 完成包管理工具部分
    print("\n=== 包管理工具学习完成 ===")
    print("✅ 6.1.1 pip包管理 - 基础使用、依赖管理、最佳实践")
    print("✅ 6.1.2 poetry现代包管理 - 项目管理、依赖解析、发布流程") 
    print("✅ 6.1.3 pipenv环境管理 - 虚拟环境、依赖锁定、开发流程")
    
    print("\n学习总结:")
    print("1. Pipenv提供自动化的环境管理")
    print("2. Pipfile/Pipfile.lock确保环境一致性")
    print("3. 适合中小型应用项目开发")
    print("4. 内置安全检查和依赖锁定")
    print("5. 在现代Python生态中地位有所下降")
    print("6. 选择工具需要考虑项目需求和团队情况")


if __name__ == "__main__":
    main() 