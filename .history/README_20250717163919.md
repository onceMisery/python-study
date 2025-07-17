# Python学习项目 - Java开发者的Python进阶之路

## 项目概述

本项目为资深Java开发工程师设计的Python3学习路径，通过对比Java和Python的语法特性，帮助快速掌握Python开发技能。

## 总体框架

### 技术选型

| 技术栈 | Python | Java对比 | 说明 |
|--------|--------|----------|------|
| 语言版本 | Python 3.9+ | JDK 17 | 主要开发语言 |
| 包管理 | pip/poetry | Maven/Gradle | 依赖管理工具 |
| Web框架 | Django/FastAPI | Spring Boot | 全栈/API开发 |
| 轻量框架 | Flask | Spring MVC | 微服务开发 |
| ORM框架 | SQLAlchemy | MyBatis | 数据库操作 |
| 测试框架 | Pytest | JUnit | 单元测试 |
| 异步任务 | Celery | Spring Task | 后台任务处理 |
| 数据库 | MySQL/PostgreSQL | MySQL | 关系型数据库 |

### 项目结构

```
python-study/
├── README.md                 # 项目总览
├── todo.md                   # 学习进度跟踪
├── data/                     # 学习过程数据
│   ├── notes/               # 学习笔记
│   ├── comparisons/         # Java vs Python对比
│   └── progress.json        # 学习进度记录
├── docs/                     # 文档目录
│   ├── learning-path.md     # 学习路线
│   ├── java-python-map.md   # Java-Python语法映射
│   └── best-practices.md    # 最佳实践
├── 01-basics/               # 基础语法
│   ├── variables/           # 变量和数据类型
│   ├── control-flow/        # 条件和循环
│   ├── functions/           # 函数
│   ├── collections/         # 集合类型
│   └── strings/             # 字符串处理
├── 02-advanced/             # 高级特性
│   ├── oop/                 # 面向对象编程
│   ├── error-handling/      # 错误处理
│   ├── file-io/             # 文件处理
│   ├── modules/             # 模块和包
│   └── decorators/          # 装饰器
├── 03-python-features/      # Python特有特性
│   ├── comprehensions/      # 推导式
│   ├── generators/          # 生成器
│   ├── lambda/              # Lambda函数
│   ├── concurrency/         # 并发处理
│   └── magic-methods/       # 魔术方法
├── 04-frameworks/           # 框架学习
│   ├── django/              # Django框架
│   ├── fastapi/             # FastAPI框架
│   ├── flask/               # Flask框架
│   └── sqlalchemy/          # SQLAlchemy ORM
├── 05-tools/                # 工具和环境
│   ├── package-management/  # 包管理
│   ├── virtual-env/         # 虚拟环境
│   ├── testing/             # 测试工具
│   └── deployment/          # 部署工具
└── examples/                # 综合示例项目
    ├── web-api/             # Web API项目
    ├── data-analysis/       # 数据分析项目
    └── microservice/        # 微服务项目
```

## 设计理念

### 代码质量原则

1. **性能优化**：关注Python特有的性能优化技巧
2. **可维护性**：使用类型提示、文档字符串
3. **可扩展性**：组合优于继承的设计模式
4. **边界条件**：完善的异常处理和参数验证
5. **监控告警**：日志记录和错误追踪

### 学习方法

1. **对比学习**：每个Python概念都与Java对比
2. **实践驱动**：每个概念都有可运行的示例
3. **渐进式学习**：从基础到高级逐步深入
4. **项目实战**：通过真实项目巩固知识

## 快速开始

### 环境准备

```bash
# 安装Python 3.9+
python --version

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 学习路径

1. **第一阶段**：基础语法 (1-2周)
2. **第二阶段**：高级特性 (2-3周)  
3. **第三阶段**：Python特色 (1-2周)
4. **第四阶段**：框架应用 (3-4周)

详细学习路线请查看 [docs/learning-path.md](docs/learning-path.md)

## 第六阶段：工具生态

本阶段目标是掌握 Python 生态下的主流开发工具，理解与 Java 生态的异同，形成高效、可维护的开发与部署流程。

### 6.1 包管理工具
- 掌握 pip、poetry、pipenv 的使用方法及适用场景
- 对比 Java 的 Maven/Gradle
- 形成依赖管理最佳实践
- 相关代码与文档：
  - 05-tools/package-management/
  - docs/best-practices.md
  - docs/java-python-map.md

### 6.2 开发环境
- 掌握虚拟环境（venv/virtualenv/pyenv）管理
- 熟悉主流 IDE（VSCode/PyCharm）配置
- 掌握 Python 调试技巧（pdb、IDE 调试）
- 相关代码与文档：
  - 05-tools/virtual-env/
  - docs/best-practices.md

### 6.3 部署工具
- 掌握 Docker 化部署流程
- 了解主流云平台部署方式
- 掌握性能监控工具的基本用法
- 相关代码与文档：
  - 05-tools/deployment/
  - docs/best-practices.md

## 贡献指南

本项目持续更新，欢迎提交学习心得和代码改进建议。

## 许可证

MIT License
