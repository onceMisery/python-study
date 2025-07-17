#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pip包管理详解
pip Package Management Guide

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习pip的基础使用、依赖管理、最佳实践和与Maven的对比

学习目标:
1. 掌握pip的基本命令和包管理操作
2. 理解依赖管理和版本控制策略
3. 学会pip的高级功能和配置优化
4. 对比pip与Maven的设计差异

注意：pip是Python生态系统的核心包管理工具
"""

import subprocess
import sys
import json
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional
import configparser
import requests
from datetime import datetime
import shutil


def demo_pip_basics():
    """演示pip基础操作"""
    print("=== 1. pip基础操作 ===")
    
    basic_commands = '''
# pip基础命令详解

# 1. 安装包
pip install package_name              # 安装最新版本
pip install package_name==1.2.3      # 安装指定版本
pip install package_name>=1.2.0      # 安装最低版本
pip install package_name~=1.2.0      # 兼容版本（1.2.x）
pip install package_name!=1.3.0      # 排除特定版本

# 版本约束符号说明
# ==  精确匹配版本
# >=  大于等于
# >   大于
# <=  小于等于
# <   小于
# ~=  兼容版本（相当于 >=1.2.0, <1.3.0）
# !=  不等于

# 2. 从不同源安装
pip install requests                                    # 从PyPI安装
pip install git+https://github.com/user/repo.git      # 从Git仓库安装
pip install git+https://github.com/user/repo.git@v1.0 # 安装特定标签
pip install git+https://github.com/user/repo.git@branch_name # 安装特定分支
pip install https://files.pythonhosted.org/packages/... # 从URL安装
pip install ./local_package                            # 安装本地包
pip install -e ./local_package                        # 可编辑模式安装

# 3. 批量安装
pip install -r requirements.txt      # 从文件安装
pip install package1 package2 package3  # 同时安装多个包

# 4. 升级和卸载
pip install --upgrade package_name   # 升级包
pip install -U package_name          # 升级包（简写）
pip uninstall package_name           # 卸载包
pip uninstall -r requirements.txt    # 批量卸载

# 5. 查看包信息
pip list                             # 列出已安装的包
pip list --outdated                  # 显示可升级的包
pip list --uptodate                  # 显示最新的包
pip show package_name                # 显示包详细信息
pip show -f package_name             # 显示包文件列表

# 6. 搜索包（注意：PyPI搜索API已禁用）
# pip search package_name            # 搜索包（已废弃）
# 替代方案：使用网站搜索 https://pypi.org/

# 7. 依赖关系
pip show package_name                # 查看包依赖
pip list --format=freeze            # 生成requirements格式
pip freeze                          # 导出当前环境包列表
pip freeze > requirements.txt       # 导出到文件

# 8. 缓存管理
pip cache list                      # 列出缓存
pip cache info                      # 显示缓存信息
pip cache dir                       # 显示缓存目录
pip cache purge                     # 清空缓存

# 9. 配置管理
pip config list                     # 列出配置
pip config get global.index-url     # 获取配置值
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/  # 设置镜像源
pip config unset global.index-url   # 删除配置

# 10. 高级选项
pip install --no-cache-dir package_name     # 不使用缓存
pip install --no-deps package_name          # 不安装依赖
pip install --force-reinstall package_name  # 强制重新安装
pip install --user package_name             # 安装到用户目录
pip install --target ./lib package_name     # 安装到指定目录
pip install --find-links ./wheels package_name # 从本地wheel查找
'''
    
    print("pip基础命令特点:")
    print("1. 简单直观的命令行界面")
    print("2. 灵活的版本约束语法")
    print("3. 多种安装源支持")
    print("4. 丰富的查询和管理功能")
    print("5. 配置和缓存优化")
    
    # Maven基础对比
    maven_basics = '''
<!-- Maven基础操作对比 -->

<!-- 1. 依赖声明 (pom.xml) -->
<dependencies>
    <!-- 精确版本 -->
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>5.3.21</version>
    </dependency>
    
    <!-- 版本范围 -->
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>[4.12,5.0)</version>  <!-- 4.12 <= version < 5.0 -->
        <scope>test</scope>
    </dependency>
    
    <!-- 最新版本 -->
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <version>LATEST</version>  <!-- 不推荐在生产环境使用 -->
    </dependency>
    
    <!-- 排除传递依赖 -->
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-web</artifactId>
        <version>5.3.21</version>
        <exclusions>
            <exclusion>
                <groupId>commons-logging</groupId>
                <artifactId>commons-logging</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
</dependencies>

<!-- 2. 仓库配置 -->
<repositories>
    <repository>
        <id>central</id>
        <url>https://repo1.maven.org/maven2</url>
    </repository>
    
    <repository>
        <id>aliyun</id>
        <url>https://maven.aliyun.com/repository/public</url>
    </repository>
    
    <repository>
        <id>spring-releases</id>
        <url>https://repo.spring.io/release</url>
    </repository>
</repositories>

<!-- 3. 依赖管理 -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>2.7.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<!-- Maven命令 -->
# 安装依赖
mvn clean install                    # 清理并安装
mvn dependency:resolve               # 解析依赖
mvn dependency:tree                  # 显示依赖树
mvn dependency:analyze               # 分析依赖

# 依赖管理
mvn dependency:copy-dependencies     # 复制依赖到target目录
mvn dependency:purge-local-repository # 清理本地仓库
mvn versions:display-dependency-updates # 显示可更新的依赖

# 项目管理
mvn archetype:generate               # 创建项目模板
mvn compile                         # 编译
mvn test                           # 运行测试
mvn package                        # 打包
mvn deploy                         # 部署到远程仓库
'''
    
    print(f"\n基础操作对比:")
    print("pip:")
    print("- 命令行直接操作")
    print("- requirements.txt管理依赖")
    print("- 简洁的版本语法")
    print("- 全局和用户级安装")
    
    print(f"\nMaven:")
    print("- XML配置驱动")
    print("- pom.xml声明式依赖")
    print("- 复杂的版本范围语法")
    print("- 项目级依赖管理")
    print()


def demo_dependency_management():
    """演示依赖管理策略"""
    print("=== 2. 依赖管理策略 ===")
    
    dependency_example = '''
# Python依赖管理详解

# 1. requirements.txt文件管理
"""
requirements.txt示例:

# 生产依赖
Django==4.1.0
psycopg2-binary>=2.9.0
redis~=4.3.0
celery[redis]>=5.2.0
gunicorn==20.1.0

# 开发依赖（通常放在dev-requirements.txt）
pytest>=7.0.0
pytest-django>=4.5.0
pytest-cov>=3.0.0
black==22.6.0
flake8>=5.0.0
mypy>=0.971

# 可选依赖组
# extras_require示例
requests[security,socks]>=2.28.0
"""

# 2. setup.py中的依赖声明
setup_py_example = '''
from setuptools import setup, find_packages

setup(
    name="myproject",
    version="1.0.0",
    packages=find_packages(),
    
    # 核心依赖
    install_requires=[
        "Django>=4.1.0,<5.0.0",
        "psycopg2-binary>=2.9.0",
        "redis~=4.3.0",
        "requests>=2.28.0",
    ],
    
    # 可选依赖
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black==22.6.0",
            "flake8>=5.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-django>=4.5.0",
            "factory-boy>=3.2.0",
        ],
        "deploy": [
            "gunicorn>=20.1.0",
            "supervisor>=4.2.0",
        ],
        "monitoring": [
            "sentry-sdk[django]>=1.9.0",
            "prometheus-client>=0.14.0",
        ]
    },
    
    # Python版本要求
    python_requires=">=3.8",
    
    # 包分类器
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
    ],
)
'''

# 3. 依赖锁定策略
class DependencyManager:
    """依赖管理器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.requirements_file = self.project_path / "requirements.txt"
        self.lock_file = self.project_path / "requirements-lock.txt"
    
    def generate_lock_file(self):
        """生成依赖锁定文件"""
        # 获取当前安装的包及其精确版本
        result = subprocess.run([
            sys.executable, "-m", "pip", "freeze"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            with open(self.lock_file, 'w') as f:
                f.write("# 依赖锁定文件\\n")
                f.write(f"# 生成时间: {datetime.now().isoformat()}\\n")
                f.write("# 此文件包含精确的包版本，用于确保环境一致性\\n\\n")
                f.write(result.stdout)
            
            print(f"依赖锁定文件已生成: {self.lock_file}")
        else:
            print(f"生成锁定文件失败: {result.stderr}")
    
    def install_from_lock(self):
        """从锁定文件安装依赖"""
        if self.lock_file.exists():
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "-r", str(self.lock_file)
            ])
            print("已从锁定文件安装依赖")
        else:
            print("锁定文件不存在")
    
    def update_dependencies(self):
        """更新依赖"""
        if self.requirements_file.exists():
            # 先升级所有包
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "-r", str(self.requirements_file), "--upgrade"
            ])
            
            # 重新生成锁定文件
            self.generate_lock_file()
            print("依赖已更新")
    
    def check_security_vulnerabilities(self):
        """检查安全漏洞"""
        try:
            # 使用safety库检查已知漏洞
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "safety"
            ], capture_output=True)
            
            if result.returncode == 0:
                safety_result = subprocess.run([
                    sys.executable, "-m", "safety", "check"
                ], capture_output=True, text=True)
                
                if safety_result.returncode == 0:
                    print("未发现安全漏洞")
                else:
                    print(f"发现安全漏洞:\\n{safety_result.stdout}")
            
        except Exception as e:
            print(f"安全检查失败: {e}")
    
    def analyze_dependency_tree(self):
        """分析依赖树"""
        try:
            # 使用pipdeptree分析依赖关系
            subprocess.run([
                sys.executable, "-m", "pip", "install", "pipdeptree"
            ], capture_output=True)
            
            result = subprocess.run([
                sys.executable, "-m", "pipdeptree"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("依赖树分析:")
                print(result.stdout)
                
                # 生成JSON格式
                json_result = subprocess.run([
                    sys.executable, "-m", "pipdeptree", "--json"
                ], capture_output=True, text=True)
                
                if json_result.returncode == 0:
                    deps = json.loads(json_result.stdout)
                    self._analyze_conflicts(deps)
            
        except Exception as e:
            print(f"依赖树分析失败: {e}")
    
    def _analyze_conflicts(self, deps: List[Dict]):
        """分析依赖冲突"""
        conflicts = []
        
        for package in deps:
            package_name = package['package']['package_name']
            for dep in package.get('dependencies', []):
                dep_name = dep['package_name']
                required_version = dep.get('required_version', '')
                installed_version = dep.get('installed_version', '')
                
                if required_version and installed_version:
                    if not self._version_matches(installed_version, required_version):
                        conflicts.append({
                            'package': package_name,
                            'dependency': dep_name,
                            'required': required_version,
                            'installed': installed_version
                        })
        
        if conflicts:
            print("\\n发现依赖冲突:")
            for conflict in conflicts:
                print(f"  {conflict['package']} 需要 {conflict['dependency']}{conflict['required']}，但安装的是 {conflict['installed']}")
        else:
            print("\\n未发现依赖冲突")
    
    def _version_matches(self, installed: str, required: str) -> bool:
        """检查版本是否匹配"""
        # 简化的版本匹配逻辑
        if required.startswith('=='):
            return installed == required[2:]
        elif required.startswith('>='):
            return True  # 简化处理
        # 更复杂的版本比较逻辑可以使用packaging库
        return True

# 4. 多环境依赖管理
class MultiEnvironmentManager:
    """多环境依赖管理"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def create_environment_files(self):
        """创建不同环境的依赖文件"""
        
        # 基础依赖
        base_requirements = '''
# 基础依赖 (requirements/base.txt)
Django>=4.1.0,<5.0.0
psycopg2-binary>=2.9.0
redis~=4.3.0
celery[redis]>=5.2.0
requests>=2.28.0
python-decouple>=3.6
'''
        
        # 开发环境依赖
        dev_requirements = '''
# 开发环境依赖 (requirements/dev.txt)
-r base.txt

# 测试工具
pytest>=7.0.0
pytest-django>=4.5.0
pytest-cov>=3.0.0
pytest-mock>=3.8.0
factory-boy>=3.2.0

# 代码质量
black==22.6.0
flake8>=5.0.0
isort>=5.10.0
mypy>=0.971
pre-commit>=2.20.0

# 开发工具
django-debug-toolbar>=3.5.0
django-extensions>=3.2.0
ipython>=8.4.0
jupyter>=1.0.0

# 文档
Sphinx>=5.0.0
sphinx-rtd-theme>=1.0.0
'''
        
        # 生产环境依赖
        prod_requirements = '''
# 生产环境依赖 (requirements/prod.txt)
-r base.txt

# 服务器
gunicorn>=20.1.0
whitenoise>=6.2.0

# 监控
sentry-sdk[django]>=1.9.0
prometheus-client>=0.14.0

# 性能
redis>=4.3.0
django-redis>=5.2.0
'''
        
        # 测试环境依赖
        test_requirements = '''
# 测试环境依赖 (requirements/test.txt)
-r base.txt

pytest>=7.0.0
pytest-django>=4.5.0
pytest-cov>=3.0.0
pytest-mock>=3.8.0
pytest-xdist>=2.5.0
coverage>=6.4.0
factory-boy>=3.2.0
'''
        
        # 创建目录和文件
        req_dir = self.project_path / "requirements"
        req_dir.mkdir(exist_ok=True)
        
        files = {
            "base.txt": base_requirements,
            "dev.txt": dev_requirements,
            "prod.txt": prod_requirements,
            "test.txt": test_requirements,
        }
        
        for filename, content in files.items():
            (req_dir / filename).write_text(content.strip())
        
        print(f"多环境依赖文件已创建在 {req_dir}")
    
    def install_environment(self, env: str):
        """安装指定环境的依赖"""
        req_file = self.project_path / "requirements" / f"{env}.txt"
        
        if req_file.exists():
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "-r", str(req_file)
            ])
            print(f"已安装 {env} 环境依赖")
        else:
            print(f"环境文件不存在: {req_file}")

# 5. 依赖安全管理
class SecurityManager:
    """依赖安全管理"""
    
    def __init__(self):
        self.known_vulnerabilities = []
    
    def audit_dependencies(self):
        """审计依赖安全性"""
        # 使用pip-audit进行安全审计
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "pip-audit"
            ], capture_output=True)
            
            result = subprocess.run([
                sys.executable, "-m", "pip-audit", "--format=json"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                audit_data = json.loads(result.stdout)
                self._process_audit_results(audit_data)
            else:
                print(f"安全审计失败: {result.stderr}")
                
        except Exception as e:
            print(f"安全审计错误: {e}")
    
    def _process_audit_results(self, audit_data: Dict):
        """处理审计结果"""
        vulnerabilities = audit_data.get('vulnerabilities', [])
        
        if vulnerabilities:
            print(f"发现 {len(vulnerabilities)} 个安全漏洞:")
            for vuln in vulnerabilities:
                package = vuln.get('package', 'Unknown')
                version = vuln.get('installed_version', 'Unknown')
                vuln_id = vuln.get('id', 'Unknown')
                description = vuln.get('description', 'No description')
                
                print(f"  {package} {version}: {vuln_id}")
                print(f"    {description}")
                
                # 建议修复版本
                fixed_versions = vuln.get('fixed_versions', [])
                if fixed_versions:
                    print(f"    建议升级到: {', '.join(fixed_versions)}")
        else:
            print("未发现安全漏洞")
    
    def generate_security_policy(self):
        """生成安全策略文件"""
        policy = {
            "security_policy": {
                "allowed_licenses": [
                    "MIT", "BSD", "Apache-2.0", "ISC", "LGPL"
                ],
                "blocked_packages": [
                    # 示例被阻止的包
                ],
                "vulnerability_threshold": "high",
                "auto_update_security_fixes": True,
                "scan_frequency": "daily"
            }
        }
        
        policy_file = Path("security-policy.json")
        with open(policy_file, 'w') as f:
            json.dump(policy, f, indent=2)
        
        print(f"安全策略文件已生成: {policy_file}")

# 6. 使用示例
def dependency_management_example():
    """依赖管理示例"""
    project_path = tempfile.mkdtemp()
    
    try:
        # 依赖管理
        manager = DependencyManager(project_path)
        manager.generate_lock_file()
        manager.analyze_dependency_tree()
        manager.check_security_vulnerabilities()
        
        # 多环境管理
        env_manager = MultiEnvironmentManager(project_path)
        env_manager.create_environment_files()
        
        # 安全管理
        security_manager = SecurityManager()
        security_manager.audit_dependencies()
        security_manager.generate_security_policy()
        
    finally:
        # 清理临时目录
        shutil.rmtree(project_path)
'''
    
    print("依赖管理策略特点:")
    print("1. requirements.txt文件管理")
    print("2. 依赖锁定确保一致性")
    print("3. 多环境依赖分离")
    print("4. 安全漏洞检测和审计")
    print("5. 依赖树分析和冲突检测")
    
    # Maven依赖管理对比
    maven_dependency = '''
<!-- Maven依赖管理对比 -->

<!-- 1. 多模块项目结构 -->
<project>
    <groupId>com.example</groupId>
    <artifactId>parent-project</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>
    
    <!-- 依赖版本统一管理 -->
    <properties>
        <spring.version>5.3.21</spring.version>
        <junit.version>5.8.2</junit.version>
        <slf4j.version>1.7.36</slf4j.version>
    </properties>
    
    <!-- 依赖管理 -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-framework-bom</artifactId>
                <version>${spring.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    
    <!-- 子模块 -->
    <modules>
        <module>core</module>
        <module>web</module>
        <module>service</module>
    </modules>
</project>

<!-- 2. Profile环境管理 -->
<profiles>
    <!-- 开发环境 -->
    <profile>
        <id>dev</id>
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
        <dependencies>
            <dependency>
                <groupId>com.h2database</groupId>
                <artifactId>h2</artifactId>
                <scope>runtime</scope>
            </dependency>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-devtools</artifactId>
                <scope>runtime</scope>
                <optional>true</optional>
            </dependency>
        </dependencies>
    </profile>
    
    <!-- 生产环境 -->
    <profile>
        <id>prod</id>
        <dependencies>
            <dependency>
                <groupId>org.postgresql</groupId>
                <artifactId>postgresql</artifactId>
                <scope>runtime</scope>
            </dependency>
        </dependencies>
    </profile>
    
    <!-- 测试环境 -->
    <profile>
        <id>test</id>
        <dependencies>
            <dependency>
                <groupId>org.testcontainers</groupId>
                <artifactId>junit-jupiter</artifactId>
                <scope>test</scope>
            </dependency>
        </dependencies>
    </profile>
</profiles>

<!-- 3. 依赖范围管理 -->
<dependencies>
    <!-- 编译时依赖 -->
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <scope>compile</scope>
    </dependency>
    
    <!-- 运行时依赖 -->
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>
    
    <!-- 测试依赖 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    
    <!-- 提供依赖（容器提供） -->
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>javax.servlet-api</artifactId>
        <scope>provided</scope>
    </dependency>
    
    <!-- 系统依赖 -->
    <dependency>
        <groupId>com.oracle</groupId>
        <artifactId>ojdbc8</artifactId>
        <scope>system</scope>
        <systemPath>${project.basedir}/lib/ojdbc8.jar</systemPath>
    </dependency>
</dependencies>

<!-- 4. 依赖分析插件 -->
<build>
    <plugins>
        <!-- 依赖分析 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-dependency-plugin</artifactId>
            <version>3.2.0</version>
            <executions>
                <execution>
                    <goals>
                        <goal>analyze</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
        
        <!-- 安全检查 -->
        <plugin>
            <groupId>org.owasp</groupId>
            <artifactId>dependency-check-maven</artifactId>
            <version>7.1.1</version>
            <executions>
                <execution>
                    <goals>
                        <goal>check</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
        
        <!-- 版本更新检查 -->
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>versions-maven-plugin</artifactId>
            <version>2.11.0</version>
        </plugin>
    </plugins>
</build>

<!-- Maven命令示例 -->
# 依赖管理命令
mvn dependency:tree                           # 显示依赖树
mvn dependency:analyze                        # 分析未使用的依赖
mvn dependency:resolve-sources                # 下载源码
mvn dependency:copy-dependencies              # 复制依赖

# 版本管理
mvn versions:display-dependency-updates       # 显示可更新的依赖
mvn versions:use-latest-releases              # 使用最新发布版本
mvn versions:update-properties                # 更新属性中的版本

# 安全检查
mvn org.owasp:dependency-check-maven:check    # 安全漏洞检查

# 环境构建
mvn clean install -Pdev                       # 开发环境构建
mvn clean package -Pprod                      # 生产环境打包
'''
    
    print(f"\n依赖管理对比:")
    print("pip:")
    print("- 文件驱动的依赖管理")
    print("- 简单的锁定机制")
    print("- 第三方工具增强功能")
    print("- 灵活的安装选项")
    
    print(f"\nMaven:")
    print("- XML声明式依赖管理")
    print("- 强大的依赖范围控制")
    print("- 内置依赖分析工具")
    print("- 多模块项目支持")
    print()


def demo_pip_configuration():
    """演示pip配置和优化"""
    print("=== 3. pip配置和优化 ===")
    
    configuration_example = '''
# pip配置和优化详解

# 1. pip配置文件位置
"""
配置文件优先级（从高到低）：
1. 命令行参数
2. 环境变量
3. 用户配置文件
4. 全局配置文件
5. 站点配置文件

配置文件路径：
- Linux/Mac用户配置: ~/.pip/pip.conf 或 ~/.config/pip/pip.conf
- Windows用户配置: %APPDATA%\\pip\\pip.ini
- Linux/Mac全局配置: /etc/pip.conf
- Windows全局配置: C:\\ProgramData\\pip\\pip.ini
"""

# 2. pip.conf配置示例
pip_conf_example = '''
[global]
# 镜像源配置
index-url = https://pypi.tuna.tsinghua.edu.cn/simple/
extra-index-url = https://pypi.org/simple/
                  https://pypi.douban.com/simple/

# 信任的主机
trusted-host = pypi.tuna.tsinghua.edu.cn
               pypi.douban.com

# 超时设置
timeout = 60
retries = 3

# 缓存配置
cache-dir = ~/.cache/pip
no-cache-dir = false

# 安装选项
user = false
no-deps = false
force-reinstall = false

# 日志级别
verbose = 1
quiet = 0

# 代理设置
# proxy = http://user:password@proxy.server:port

[install]
# 默认安装选项
no-warn-script-location = true
no-warn-conflicts = true

# 查找链接
find-links = file:///path/to/local/wheels
            https://download.pytorch.org/whl/torch_stable.html

[list]
# 列表格式
format = columns

[freeze]
# 冻结选项
all = false
'''

# 3. 环境变量配置
class PipConfigManager:
    """pip配置管理器"""
    
    def __init__(self):
        self.config_locations = self._get_config_locations()
    
    def _get_config_locations(self) -> Dict[str, Path]:
        """获取配置文件位置"""
        import platform
        
        if platform.system() == "Windows":
            user_config = Path(os.environ.get('APPDATA', '')) / 'pip' / 'pip.ini'
            global_config = Path('C:/') / 'ProgramData' / 'pip' / 'pip.ini'
        else:
            user_config = Path.home() / '.config' / 'pip' / 'pip.conf'
            global_config = Path('/etc/pip.conf')
        
        return {
            'user': user_config,
            'global': global_config
        }
    
    def create_optimized_config(self, scope: str = 'user'):
        """创建优化的配置文件"""
        config = configparser.ConfigParser()
        
        # 全局配置
        config.add_section('global')
        config.set('global', 'index-url', 'https://pypi.tuna.tsinghua.edu.cn/simple/')
        config.set('global', 'extra-index-url', '''
            https://pypi.org/simple/
            https://pypi.douban.com/simple/''')
        config.set('global', 'trusted-host', '''
            pypi.tuna.tsinghua.edu.cn
            pypi.douban.com''')
        config.set('global', 'timeout', '60')
        config.set('global', 'retries', '3')
        
        # 安装配置
        config.add_section('install')
        config.set('install', 'no-warn-script-location', 'true')
        
        # 写入配置文件
        config_file = self.config_locations[scope]
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            config.write(f)
        
        print(f"已创建优化配置文件: {config_file}")
    
    def show_current_config(self):
        """显示当前配置"""
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'config', 'list'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("当前pip配置:")
            print(result.stdout)
        else:
            print("无法获取配置信息")
    
    def benchmark_mirrors(self):
        """测试镜像源速度"""
        mirrors = [
            ('官方源', 'https://pypi.org/simple/'),
            ('清华源', 'https://pypi.tuna.tsinghua.edu.cn/simple/'),
            ('豆瓣源', 'https://pypi.douban.com/simple/'),
            ('阿里源', 'https://mirrors.aliyun.com/pypi/simple/'),
            ('腾讯源', 'https://mirrors.cloud.tencent.com/pypi/simple/'),
        ]
        
        results = []
        
        for name, url in mirrors:
            try:
                start_time = time.time()
                response = requests.get(url + 'requests/', timeout=10)
                end_time = time.time()
                
                if response.status_code == 200:
                    speed = end_time - start_time
                    results.append((name, url, speed, 'success'))
                else:
                    results.append((name, url, 0, f'HTTP {response.status_code}'))
                    
            except Exception as e:
                results.append((name, url, 0, str(e)))
        
        # 排序并显示结果
        results.sort(key=lambda x: x[2] if x[3] == 'success' else float('inf'))
        
        print("镜像源速度测试结果:")
        for name, url, speed, status in results:
            if status == 'success':
                print(f"  {name}: {speed:.2f}s - {url}")
            else:
                print(f"  {name}: 失败 ({status}) - {url}")
        
        # 推荐最快的镜像源
        if results and results[0][3] == 'success':
            fastest = results[0]
            print(f"\\n推荐使用最快的镜像源: {fastest[0]} ({fastest[2]:.2f}s)")
            print(f"配置命令: pip config set global.index-url {fastest[1]}")

# 4. pip性能优化
class PipPerformanceOptimizer:
    """pip性能优化器"""
    
    def __init__(self):
        self.cache_dir = Path.home() / '.cache' / 'pip'
    
    def optimize_cache(self):
        """优化缓存设置"""
        # 检查缓存目录大小
        cache_size = self._get_directory_size(self.cache_dir)
        print(f"当前缓存大小: {cache_size / (1024**2):.1f} MB")
        
        # 清理旧缓存
        self._cleanup_old_cache()
        
        # 设置缓存限制
        self._set_cache_limit()
    
    def _get_directory_size(self, path: Path) -> int:
        """获取目录大小"""
        total_size = 0
        if path.exists():
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        return total_size
    
    def _cleanup_old_cache(self):
        """清理旧缓存"""
        import time
        
        if not self.cache_dir.exists():
            return
        
        # 删除超过30天的缓存文件
        cutoff_time = time.time() - (30 * 24 * 60 * 60)
        cleaned_size = 0
        
        for file_path in self.cache_dir.rglob('*'):
            if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                size = file_path.stat().st_size
                file_path.unlink()
                cleaned_size += size
        
        if cleaned_size > 0:
            print(f"清理了 {cleaned_size / (1024**2):.1f} MB 的旧缓存")
    
    def _set_cache_limit(self):
        """设置缓存限制"""
        # 可以通过配置文件限制缓存大小
        print("建议在pip.conf中设置缓存限制")
    
    def parallel_install_setup(self):
        """并行安装设置"""
        print("pip并行安装优化建议:")
        print("1. 使用--parallel参数（实验性功能）")
        print("2. 预下载wheel文件")
        print("3. 使用本地缓存目录")
        print("4. 配置多个镜像源")
    
    def wheel_optimization(self):
        """wheel优化"""
        print("wheel使用优化:")
        print("1. 优先安装wheel格式包")
        print("2. 本地构建wheel缓存")
        print("3. 使用--find-links指定wheel目录")
        
        # 示例命令
        commands = [
            "pip install --only-binary=all package_name",  # 只安装二进制包
            "pip wheel -r requirements.txt -w ./wheels",   # 构建wheel
            "pip install --find-links ./wheels package_name",  # 从本地wheel安装
        ]
        
        for cmd in commands:
            print(f"  {cmd}")

# 5. pip安全配置
class PipSecurityManager:
    """pip安全管理器"""
    
    def __init__(self):
        self.security_config = {
            'verify_ssl': True,
            'trusted_hosts': [],
            'allow_unsafe_packages': False,
            'check_signatures': False  # PyPI不支持包签名
        }
    
    def configure_secure_installation(self):
        """配置安全安装"""
        secure_config = '''
[global]
# SSL验证
trusted-host = 
# 不要添加任何不受信任的主机

# 只从HTTPS源安装
index-url = https://pypi.org/simple/

# 启用所有安全检查
require-hashes = true

[install]
# 不安装不安全的包
no-allow-unsafe = true

# 只安装经过验证的包
only-binary = :all:
        '''
        
        print("安全配置建议:")
        print(secure_config)
    
    def hash_verification_example(self):
        """哈希验证示例"""
        requirements_with_hashes = '''
# requirements.txt with hashes
requests==2.28.1 \\
    --hash=sha256:7c5599b102feddaa661c826c56ab4fee28bfd17f5abca1ebbe3e7f19d7c97983 \\
    --hash=sha256:8fefa2a1a1365bf5520aac41836fbee479da67864514bdb821f31ce07ce65349

urllib3==1.26.12 \\
    --hash=sha256:3fa96cf423e6987997fc326ae8df396db2a8b7c667747d47ddd8ecba91f4a74e \\
    --hash=sha256:b930dd878d5a8afb066a637fbb35144fe7901e3b209d1cd4f524bd0e9deee997
        '''
        
        print("带哈希验证的requirements.txt:")
        print(requirements_with_hashes)
        print("\\n使用命令: pip install -r requirements.txt")
    
    def generate_hash_requirements(self, packages: List[str]):
        """生成带哈希的requirements文件"""
        print("生成带哈希的requirements.txt...")
        
        # 这里可以实现获取包哈希的逻辑
        # 实际应用中可以使用pip-tools的pip-compile --generate-hashes
        print("建议使用pip-tools: pip-compile --generate-hashes requirements.in")

# 6. 使用示例
def configuration_example():
    """配置示例"""
    
    # 配置管理
    config_manager = PipConfigManager()
    config_manager.show_current_config()
    config_manager.create_optimized_config()
    config_manager.benchmark_mirrors()
    
    # 性能优化
    optimizer = PipPerformanceOptimizer()
    optimizer.optimize_cache()
    optimizer.parallel_install_setup()
    optimizer.wheel_optimization()
    
    # 安全配置
    security_manager = PipSecurityManager()
    security_manager.configure_secure_installation()
    security_manager.hash_verification_example()
'''
    
    print("pip配置和优化特点:")
    print("1. 灵活的配置文件系统")
    print("2. 多镜像源支持和自动选择")
    print("3. 缓存优化提升安装速度")
    print("4. 安全配置防范供应链攻击")
    print("5. 性能调优适应不同网络环境")
    
    # Maven配置对比
    maven_config = '''
<!-- Maven配置对比 -->

<!-- 1. settings.xml全局配置 -->
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0">
    
    <!-- 本地仓库 -->
    <localRepository>/path/to/local/repo</localRepository>
    
    <!-- 镜像仓库 -->
    <mirrors>
        <mirror>
            <id>aliyun</id>
            <name>阿里云镜像</name>
            <url>https://maven.aliyun.com/repository/public</url>
            <mirrorOf>central</mirrorOf>
        </mirror>
        
        <mirror>
            <id>huawei</id>
            <name>华为云镜像</name>
            <url>https://mirrors.huaweicloud.com/repository/maven/</url>
            <mirrorOf>central</mirrorOf>
        </mirror>
    </mirrors>
    
    <!-- 服务器认证 -->
    <servers>
        <server>
            <id>my-repo</id>
            <username>deployment</username>
            <password>password123</password>
        </server>
        
        <server>
            <id>secure-repo</id>
            <username>user</username>
            <privateKey>/path/to/private/key</privateKey>
            <passphrase>optional-passphrase</passphrase>
        </server>
    </servers>
    
    <!-- 代理配置 -->
    <proxies>
        <proxy>
            <id>company-proxy</id>
            <active>true</active>
            <protocol>http</protocol>
            <host>proxy.company.com</host>
            <port>8080</port>
            <username>proxy-user</username>
            <password>proxy-pass</password>
            <nonProxyHosts>localhost|127.*|*.company.com</nonProxyHosts>
        </proxy>
    </proxies>
    
    <!-- Profile激活 -->
    <activeProfiles>
        <activeProfile>development</activeProfile>
    </activeProfiles>
    
    <!-- Profile定义 -->
    <profiles>
        <profile>
            <id>development</id>
            <repositories>
                <repository>
                    <id>dev-repo</id>
                    <url>https://dev.repository.com/maven2</url>
                    <releases>
                        <enabled>true</enabled>
                        <updatePolicy>always</updatePolicy>
                    </releases>
                    <snapshots>
                        <enabled>true</enabled>
                        <updatePolicy>daily</updatePolicy>
                    </snapshots>
                </repository>
            </repositories>
        </profile>
    </profiles>
</settings>

<!-- 2. .mvn/maven.config项目配置 -->
-Dmaven.repo.local=./.m2/repository
-Dmaven.test.skip=false
-Dmaven.javadoc.skip=true
-Dspring.profiles.active=dev
--batch-mode
--show-version

<!-- 3. Maven性能优化 -->
<!-- 并行构建 -->
mvn clean install -T 4              # 4线程并行构建
mvn clean install -T 1C             # 每CPU核心1线程

<!-- 离线模式 -->
mvn clean install -o                # 离线构建

<!-- 内存优化 -->
export MAVEN_OPTS="-Xmx4g -Xms1g -XX:ReservedCodeCacheSize=512m"

<!-- 增量构建 -->
mvn clean install -pl module1,module2   # 只构建指定模块
mvn clean install -am -pl web-module    # 构建依赖模块

<!-- 4. 企业级配置 -->
<build>
    <plugins>
        <!-- 编译器配置 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.10.1</version>
            <configuration>
                <source>17</source>
                <target>17</target>
                <encoding>UTF-8</encoding>
                <compilerArgs>
                    <arg>-parameters</arg>
                    <arg>-Xlint:all</arg>
                </compilerArgs>
            </configuration>
        </plugin>
        
        <!-- 资源插件 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-resources-plugin</artifactId>
            <version>3.2.0</version>
            <configuration>
                <encoding>UTF-8</encoding>
            </configuration>
        </plugin>
    </plugins>
</build>
'''
    
    print(f"\n配置管理对比:")
    print("pip:")
    print("- INI格式配置文件")
    print("- 环境变量覆盖")
    print("- 命令行参数优先")
    print("- 简单的镜像源配置")
    
    print(f"\nMaven:")
    print("- XML配置文件")
    print("- Profile环境切换")
    print("- 复杂的仓库管理")
    print("- 企业级认证和代理")
    print()


def main():
    """主函数：运行所有演示"""
    print("pip包管理完整学习指南")
    print("=" * 50)
    
    demo_pip_basics()
    demo_dependency_management()
    demo_pip_configuration()
    
    print("学习总结:")
    print("1. pip是Python包管理的核心工具")
    print("2. requirements.txt提供简单的依赖管理")
    print("3. 配置优化可显著提升使用体验")
    print("4. 安全配置防范供应链风险")
    print("5. 与Maven相比更轻量但功能相对简单")
    print("6. 需要第三方工具增强企业级功能")


if __name__ == "__main__":
    main() 