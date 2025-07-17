#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python高级特性 - 文件I/O操作
===========================

本文件演示Python的文件操作，并与Java进行对比说明
面向Java开发者的Python学习教程

作者: Python学习项目
创建时间: 2024年1月16日
"""

import os
import shutil
import json
import csv
import pickle
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Iterator
from contextlib import contextmanager
import io


def demonstrate_basic_file_operations():
    """
    演示基本文件操作
    Python vs Java
    """
    print("=== 基本文件操作 ===\n")
    
    print("Java vs Python文件操作语法:")
    print("Java:")
    print("   // 读取文件")
    print("   try (BufferedReader reader = Files.newBufferedReader(path)) {")
    print("       String content = reader.lines().collect(Collectors.joining());")
    print("   }")
    print("   ")
    print("   // 写入文件")
    print("   try (BufferedWriter writer = Files.newBufferedWriter(path)) {")
    print("       writer.write(\"Hello World\");")
    print("   }")
    print()
    
    print("Python:")
    print("   # 读取文件")
    print("   with open('file.txt', 'r') as f:")
    print("       content = f.read()")
    print("   ")
    print("   # 写入文件")
    print("   with open('file.txt', 'w') as f:")
    print("       f.write('Hello World')")
    print()
    
    # 1. 创建临时目录进行演示
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        demo_file = temp_path / "demo.txt"
        
        print("1. 基本文件写入和读取")
        
        # 写入文件
        content_to_write = "Hello Python!\n这是第二行\n这是第三行"
        
        with open(demo_file, 'w', encoding='utf-8') as f:
            f.write(content_to_write)
        
        print(f"   写入文件: {demo_file}")
        print(f"   内容: {repr(content_to_write)}")
        
        # 读取整个文件
        with open(demo_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"   读取内容: {repr(content)}")
        print()
        
        # 2. 不同的读取方式
        print("2. 不同的读取方式")
        
        # 按行读取
        with open(demo_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print("   按行读取 (readlines()):")
        for i, line in enumerate(lines):
            print(f"     行{i+1}: {repr(line)}")
        
        # 逐行迭代
        print("   逐行迭代:")
        with open(demo_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                print(f"     行{i}: {line.strip()}")
        print()
        
        # 3. 不同的写入方式
        print("3. 不同的写入方式")
        
        # 追加写入
        append_file = temp_path / "append.txt"
        
        # 首次写入
        with open(append_file, 'w', encoding='utf-8') as f:
            f.write("第一次写入\n")
        
        # 追加写入
        with open(append_file, 'a', encoding='utf-8') as f:
            f.write("追加的内容\n")
        
        # 读取查看结果
        with open(append_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"   追加写入结果: {repr(content)}")
        
        # 写入多行
        multi_line_file = temp_path / "multiline.txt"
        lines_to_write = ["第一行", "第二行", "第三行"]
        
        with open(multi_line_file, 'w', encoding='utf-8') as f:
            f.writelines(line + '\n' for line in lines_to_write)
        
        print(f"   多行写入完成: {multi_line_file}")
        print()


def demonstrate_file_modes_and_encoding():
    """
    演示文件模式和编码
    """
    print("=== 文件模式和编码 ===\n")
    
    print("Python文件模式:")
    print("   'r'  - 只读模式 (默认)")
    print("   'w'  - 写入模式 (覆盖)")
    print("   'a'  - 追加模式")
    print("   'x'  - 独占创建模式")
    print("   'b'  - 二进制模式")
    print("   't'  - 文本模式 (默认)")
    print("   '+'  - 读写模式")
    print()
    
    print("Java对比:")
    print("   Files.newBufferedReader() - 类似'r'")
    print("   Files.newBufferedWriter() - 类似'w'")
    print("   StandardOpenOption.APPEND - 类似'a'")
    print("   StandardOpenOption.CREATE_NEW - 类似'x'")
    print()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 1. 文本模式 vs 二进制模式
        print("1. 文本模式 vs 二进制模式")
        
        text_file = temp_path / "text.txt"
        binary_file = temp_path / "binary.bin"
        
        # 文本模式写入
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("Hello 世界! 🌍")
        
        # 二进制模式写入
        with open(binary_file, 'wb') as f:
            f.write("Hello 世界! 🌍".encode('utf-8'))
        
        # 文本模式读取
        with open(text_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        # 二进制模式读取
        with open(binary_file, 'rb') as f:
            binary_content = f.read()
        
        print(f"   文本模式读取: {text_content}")
        print(f"   二进制模式读取: {binary_content}")
        print(f"   解码二进制: {binary_content.decode('utf-8')}")
        print()
        
        # 2. 不同编码演示
        print("2. 不同编码演示")
        
        encodings = ['utf-8', 'gbk', 'ascii']
        test_text = "Hello 世界!"
        
        for encoding in encodings:
            try:
                encoded_file = temp_path / f"encoded_{encoding}.txt"
                
                # 写入特定编码
                with open(encoded_file, 'w', encoding=encoding) as f:
                    f.write(test_text)
                
                # 读取并验证
                with open(encoded_file, 'r', encoding=encoding) as f:
                    content = f.read()
                
                print(f"   {encoding:8} 编码: {content}")
                
            except UnicodeEncodeError as e:
                print(f"   {encoding:8} 编码失败: {e}")
        print()
        
        # 3. 读写模式组合
        print("3. 读写模式组合")
        
        rw_file = temp_path / "readwrite.txt"
        
        # 'w+' 模式：读写，先清空文件
        with open(rw_file, 'w+', encoding='utf-8') as f:
            f.write("初始内容\n")
            f.seek(0)  # 回到文件开头
            content = f.read()
            print(f"   'w+' 模式读取: {repr(content)}")
        
        # 'r+' 模式：读写，不清空文件
        with open(rw_file, 'r+', encoding='utf-8') as f:
            content = f.read()
            print(f"   'r+' 模式读取: {repr(content)}")
            f.write("追加内容\n")
        
        # 验证追加结果
        with open(rw_file, 'r', encoding='utf-8') as f:
            final_content = f.read()
            print(f"   最终内容: {repr(final_content)}")
        print()


def demonstrate_file_positioning():
    """
    演示文件定位操作
    """
    print("=== 文件定位操作 ===\n")
    
    print("Python vs Java文件定位:")
    print("Python:")
    print("   f.seek(offset, whence)  # 设置文件指针位置")
    print("   f.tell()               # 获取当前位置")
    print("   whence: 0(开头), 1(当前), 2(末尾)")
    print()
    
    print("Java:")
    print("   channel.position(position)  # 设置位置")
    print("   channel.position()          # 获取位置")
    print("   RandomAccessFile.seek()     # 设置位置")
    print()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        seek_file = temp_path / "seek_demo.txt"
        
        # 创建测试文件
        content = "0123456789ABCDEFGHIJ"
        with open(seek_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("1. 文件定位演示")
        print(f"   文件内容: {content}")
        
        with open(seek_file, 'r', encoding='utf-8') as f:
            # 初始位置
            print(f"   初始位置: {f.tell()}")
            
            # 读取前5个字符
            data = f.read(5)
            print(f"   读取5个字符: '{data}', 当前位置: {f.tell()}")
            
            # 移动到位置10
            f.seek(10)
            data = f.read(3)
            print(f"   移动到位置10，读取3个字符: '{data}', 当前位置: {f.tell()}")
            
            # 从当前位置向前移动2个位置
            f.seek(-2, 1)  # 相对当前位置
            data = f.read(2)
            print(f"   向前移动2位，读取2个字符: '{data}', 当前位置: {f.tell()}")
            
            # 移动到文件末尾
            f.seek(0, 2)  # 相对文件末尾
            print(f"   移动到文件末尾，位置: {f.tell()}")
        print()
        
        # 2. 二进制文件定位（更精确）
        print("2. 二进制文件定位")
        
        binary_file = temp_path / "binary_seek.bin"
        binary_data = bytes(range(256))  # 0-255的字节
        
        with open(binary_file, 'wb') as f:
            f.write(binary_data)
        
        with open(binary_file, 'rb') as f:
            # 读取特定位置的字节
            positions = [0, 50, 100, 200, 255]
            
            for pos in positions:
                f.seek(pos)
                byte_value = f.read(1)[0] if f.read(1) else None
                f.seek(pos)  # 重新定位因为read移动了指针
                actual_byte = f.read(1)[0]
                print(f"   位置 {pos:3d}: 字节值 {actual_byte:3d}")
        print()


def demonstrate_directory_operations():
    """
    演示目录操作
    """
    print("=== 目录操作 ===\n")
    
    print("Python vs Java目录操作:")
    print("Python:")
    print("   os.mkdir()           # 创建目录")
    print("   os.makedirs()        # 创建多级目录")
    print("   os.listdir()         # 列出目录内容")
    print("   shutil.rmtree()      # 删除目录树")
    print("   Path.mkdir()         # pathlib方式")
    print()
    
    print("Java:")
    print("   Files.createDirectory()      # 创建目录")
    print("   Files.createDirectories()    # 创建多级目录")
    print("   Files.list()                 # 列出目录")
    print("   Files.walkFileTree()         # 遍历目录树")
    print()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 1. 创建目录结构
        print("1. 创建目录结构")
        
        # 使用pathlib创建目录
        project_dir = temp_path / "project"
        src_dir = project_dir / "src"
        test_dir = project_dir / "test"
        docs_dir = project_dir / "docs"
        
        # 创建多级目录
        src_dir.mkdir(parents=True)  # parents=True 类似 makedirs
        test_dir.mkdir()
        docs_dir.mkdir()
        
        print(f"   创建项目目录: {project_dir}")
        print(f"   创建子目录: {src_dir}, {test_dir}, {docs_dir}")
        
        # 创建一些文件
        (src_dir / "main.py").write_text("print('Hello')", encoding='utf-8')
        (src_dir / "utils.py").write_text("def helper(): pass", encoding='utf-8')
        (test_dir / "test_main.py").write_text("import unittest", encoding='utf-8')
        (docs_dir / "README.md").write_text("# 项目文档", encoding='utf-8')
        
        # 2. 遍历目录
        print("\n2. 遍历目录")
        
        print("   使用os.listdir():")
        for item in os.listdir(project_dir):
            item_path = project_dir / item
            item_type = "目录" if item_path.is_dir() else "文件"
            print(f"     {item} ({item_type})")
        
        print("\n   使用pathlib遍历:")
        for item in project_dir.iterdir():
            item_type = "目录" if item.is_dir() else "文件"
            print(f"     {item.name} ({item_type})")
        
        print("\n   递归遍历所有文件:")
        for item in project_dir.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(project_dir)
                print(f"     {relative_path}")
        print()
        
        # 3. 目录信息
        print("3. 目录信息")
        
        def print_path_info(path: Path):
            """打印路径信息"""
            print(f"   路径: {path}")
            print(f"   存在: {path.exists()}")
            print(f"   是文件: {path.is_file()}")
            print(f"   是目录: {path.is_dir()}")
            
            if path.exists():
                stat = path.stat()
                print(f"   大小: {stat.st_size} 字节")
                print(f"   修改时间: {stat.st_mtime}")
            print()
        
        print_path_info(src_dir)
        print_path_info(src_dir / "main.py")
        
        # 4. 复制和移动
        print("4. 复制和移动操作")
        
        # 复制文件
        backup_dir = temp_path / "backup"
        backup_dir.mkdir()
        
        src_file = src_dir / "main.py"
        backup_file = backup_dir / "main_backup.py"
        
        shutil.copy2(src_file, backup_file)  # copy2保留元数据
        print(f"   复制文件: {src_file} -> {backup_file}")
        
        # 复制整个目录
        project_backup = temp_path / "project_backup"
        shutil.copytree(project_dir, project_backup)
        print(f"   复制目录: {project_dir} -> {project_backup}")
        
        # 移动文件
        temp_file = backup_dir / "temp.txt"
        temp_file.write_text("临时文件", encoding='utf-8')
        
        moved_file = backup_dir / "moved.txt"
        shutil.move(str(temp_file), str(moved_file))
        print(f"   移动文件: {temp_file} -> {moved_file}")
        print()


def demonstrate_advanced_file_operations():
    """
    演示高级文件操作
    """
    print("=== 高级文件操作 ===\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 1. 临时文件和目录
        print("1. 临时文件和目录")
        
        # 临时文件
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
            temp_file.write("这是临时文件内容")
            temp_file_path = temp_file.name
            print(f"   创建临时文件: {temp_file_path}")
        
        # 读取临时文件
        with open(temp_file_path, 'r') as f:
            content = f.read()
            print(f"   临时文件内容: {content}")
        
        # 清理临时文件
        os.unlink(temp_file_path)
        print("   删除临时文件")
        
        # 临时目录
        with tempfile.TemporaryDirectory() as temp_subdir:
            print(f"   创建临时目录: {temp_subdir}")
            
            # 在临时目录中创建文件
            temp_file_in_dir = Path(temp_subdir) / "test.txt"
            temp_file_in_dir.write_text("临时目录中的文件", encoding='utf-8')
            print(f"   在临时目录中创建文件: {temp_file_in_dir}")
        
        print("   临时目录自动清理")
        print()
        
        # 2. 内存文件操作
        print("2. 内存文件操作")
        
        # StringIO - 内存中的文本文件
        text_buffer = io.StringIO()
        text_buffer.write("第一行\n")
        text_buffer.write("第二行\n")
        text_buffer.write("第三行\n")
        
        # 读取内存文件
        text_buffer.seek(0)
        content = text_buffer.read()
        print(f"   StringIO内容: {repr(content)}")
        
        # BytesIO - 内存中的二进制文件
        bytes_buffer = io.BytesIO()
        bytes_buffer.write(b"Hello World")
        bytes_buffer.write(b"\x00\x01\x02\x03")
        
        bytes_buffer.seek(0)
        binary_content = bytes_buffer.read()
        print(f"   BytesIO内容: {binary_content}")
        print()
        
        # 3. 文件锁定（跨平台困难，演示概念）
        print("3. 文件锁定概念")
        
        lock_file = temp_path / "lockfile.txt"
        
        # 模拟文件锁定
        try:
            with open(lock_file, 'x') as f:  # 'x' 模式确保文件不存在时才创建
                f.write("这个文件被锁定")
                print(f"   成功创建并锁定文件: {lock_file}")
                
                # 尝试再次创建（应该失败）
                try:
                    with open(lock_file, 'x') as f2:
                        f2.write("不应该成功")
                except FileExistsError:
                    print("   文件已存在，锁定有效")
        
        except FileExistsError:
            print("   文件已被锁定")
        finally:
            if lock_file.exists():
                lock_file.unlink()
                print("   释放文件锁定")
        print()


def demonstrate_structured_file_formats():
    """
    演示结构化文件格式
    """
    print("=== 结构化文件格式 ===\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 1. JSON文件操作
        print("1. JSON文件操作")
        
        # 准备数据
        data = {
            "name": "张三",
            "age": 30,
            "skills": ["Python", "Java", "JavaScript"],
            "address": {
                "city": "北京",
                "zipcode": "100000"
            },
            "active": True
        }
        
        json_file = temp_path / "data.json"
        
        # 写入JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"   写入JSON文件: {json_file}")
        
        # 读取JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        print(f"   读取JSON数据: {loaded_data}")
        print()
        
        # 2. CSV文件操作
        print("2. CSV文件操作")
        
        csv_file = temp_path / "employees.csv"
        
        # 准备CSV数据
        employees = [
            {"name": "张三", "age": 30, "department": "开发部", "salary": 8000},
            {"name": "李四", "age": 25, "department": "测试部", "salary": 6000},
            {"name": "王五", "age": 35, "department": "产品部", "salary": 7000},
        ]
        
        # 写入CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "age", "department", "salary"])
            writer.writeheader()
            writer.writerows(employees)
        
        print(f"   写入CSV文件: {csv_file}")
        
        # 读取CSV
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            print("   读取CSV数据:")
            for row in reader:
                print(f"     {row}")
        print()
        
        # 3. Pickle文件操作（Python特有）
        print("3. Pickle文件操作（Python序列化）")
        
        pickle_file = temp_path / "data.pkl"
        
        # 复杂Python对象
        complex_data = {
            "numbers": [1, 2, 3, 4, 5],
            "function": lambda x: x * 2,  # 函数也可以序列化
            "set": {1, 2, 3},
            "tuple": (1, "hello", [1, 2, 3])
        }
        
        # 写入Pickle
        with open(pickle_file, 'wb') as f:
            pickle.dump(complex_data, f)
        
        print(f"   写入Pickle文件: {pickle_file}")
        
        # 读取Pickle
        with open(pickle_file, 'rb') as f:
            loaded_complex_data = pickle.load(f)
        
        print("   读取Pickle数据:")
        print(f"     numbers: {loaded_complex_data['numbers']}")
        print(f"     function(5): {loaded_complex_data['function'](5)}")
        print(f"     set: {loaded_complex_data['set']}")
        print(f"     tuple: {loaded_complex_data['tuple']}")
        print()


def demonstrate_file_monitoring():
    """
    演示文件监控和观察
    """
    print("=== 文件监控概念 ===\n")
    
    print("Python文件监控:")
    print("   watchdog库 - 跨平台文件系统监控")
    print("   os.stat() - 获取文件状态信息")
    print("   pathlib.Path.stat() - 面向对象的文件状态")
    print()
    
    print("Java对比:")
    print("   WatchService - Java 7+ 的文件监控API")
    print("   Files.getLastModifiedTime() - 获取修改时间")
    print("   Files.size() - 获取文件大小")
    print()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        monitor_file = temp_path / "monitor.txt"
        
        # 创建文件
        monitor_file.write_text("初始内容", encoding='utf-8')
        
        # 获取初始状态
        initial_stat = monitor_file.stat()
        print(f"   文件: {monitor_file}")
        print(f"   初始大小: {initial_stat.st_size} 字节")
        print(f"   初始修改时间: {initial_stat.st_mtime}")
        
        # 修改文件
        import time
        time.sleep(1)  # 确保时间戳不同
        
        monitor_file.write_text("修改后的内容，更长一些", encoding='utf-8')
        
        # 获取修改后状态
        modified_stat = monitor_file.stat()
        print(f"   修改后大小: {modified_stat.st_size} 字节")
        print(f"   修改后时间: {modified_stat.st_mtime}")
        print(f"   大小变化: {modified_stat.st_size - initial_stat.st_size} 字节")
        print(f"   时间变化: {modified_stat.st_mtime - initial_stat.st_mtime:.2f} 秒")
        print()


@contextmanager
def managed_file(filename: Union[str, Path], mode: str = 'r', **kwargs):
    """
    文件上下文管理器示例
    """
    print(f"   打开文件: {filename} (模式: {mode})")
    try:
        f = open(filename, mode, **kwargs)
        yield f
    except Exception as e:
        print(f"   文件操作异常: {e}")
        raise
    finally:
        if 'f' in locals() and not f.closed:
            f.close()
            print(f"   关闭文件: {filename}")


def main():
    """主函数 - 演示所有文件I/O特性"""
    print("Python高级特性学习 - 文件I/O操作")
    print("=" * 50)
    
    demonstrate_basic_file_operations()
    demonstrate_file_modes_and_encoding()
    demonstrate_file_positioning()
    demonstrate_directory_operations()
    demonstrate_advanced_file_operations()
    demonstrate_structured_file_formats()
    demonstrate_file_monitoring()
    
    # 演示自定义上下文管理器
    print("=== 自定义文件上下文管理器 ===\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "context_demo.txt"
        
        with managed_file(temp_file, 'w', encoding='utf-8') as f:
            f.write("使用自定义上下文管理器")
        
        with managed_file(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"   读取内容: {content}")
    
    print()
    print("学习总结:")
    print("1. Python文件操作语法简洁，with语句确保资源释放")
    print("2. pathlib提供面向对象的路径操作")
    print("3. 支持多种编码和文件模式")
    print("4. 内置支持JSON、CSV等结构化格式")
    print("5. Pickle提供Python特有的对象序列化")
    print("6. 临时文件和内存文件操作便捷")
    print("7. 文件定位和状态监控功能完善")


if __name__ == "__main__":
    main() 