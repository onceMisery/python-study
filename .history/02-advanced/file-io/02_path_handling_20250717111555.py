"""
Python文件路径处理详解
作者：Python学习项目
日期：2024-01-16

本文件演示Python中的路径处理操作，包含与Java的详细对比
重点：pathlib模块 vs Java java.nio.file.Path
"""

import os
import pathlib
from pathlib import Path, PurePath
import tempfile
import glob
import shutil
import stat
from datetime import datetime


def path_basics():
    """
    路径基础操作
    
    Java对比：
    - Python: os.path 或 pathlib.Path
    - Java: java.nio.file.Path, java.io.File
    """
    print("=== 路径基础操作 ===")
    
    # 1. 获取当前工作目录
    # Python方式1: os.getcwd()
    current_dir = os.getcwd()
    print(f"当前目录(os): {current_dir}")
    
    # Python方式2: pathlib.Path.cwd()
    current_path = Path.cwd()
    print(f"当前目录(pathlib): {current_path}")
    
    """
    Java对比：
    String currentDir = System.getProperty("user.dir");
    Path currentPath = Paths.get("").toAbsolutePath();
    """
    
    # 2. 路径拼接
    # Python方式1: os.path.join()
    old_style_path = os.path.join(current_dir, "data", "test.txt")
    print(f"路径拼接(os): {old_style_path}")
    
    # Python方式2: pathlib (推荐)
    modern_path = current_path / "data" / "test.txt"
    print(f"路径拼接(pathlib): {modern_path}")
    
    """
    Java对比：
    Path path = Paths.get("data", "test.txt");
    Path path2 = Paths.get("data").resolve("test.txt");
    """
    
    # 3. 路径分解
    example_path = Path("/home/user/documents/project/src/main.py")
    
    print(f"\n路径分解示例: {example_path}")
    print(f"父目录: {example_path.parent}")
    print(f"文件名: {example_path.name}")
    print(f"文件名(无扩展名): {example_path.stem}")
    print(f"扩展名: {example_path.suffix}")
    print(f"所有父目录: {list(example_path.parents)}")
    print(f"根目录: {example_path.root}")
    print(f"路径部分: {example_path.parts}")
    
    """
    Java对比：
    Path path = Paths.get("/home/user/documents/project/src/main.py");
    Path parent = path.getParent();
    String fileName = path.getFileName().toString();
    String extension = fileName.substring(fileName.lastIndexOf('.'));
    """


def path_operations():
    """
    路径操作和检查
    """
    print("\n=== 路径操作和检查 ===")
    
    # 创建测试路径
    test_path = Path("data/test_file.txt")
    test_dir = Path("data/test_dir")
    
    # 1. 路径类型检查
    print(f"路径存在: {test_path.exists()}")
    print(f"是文件: {test_path.is_file()}")
    print(f"是目录: {test_path.is_dir()}")
    print(f"是符号链接: {test_path.is_symlink()}")
    print(f"是绝对路径: {test_path.is_absolute()}")
    
    """
    Java对比：
    Files.exists(path)
    Files.isRegularFile(path)
    Files.isDirectory(path)
    Files.isSymbolicLink(path)
    path.isAbsolute()
    """
    
    # 2. 路径转换
    relative_path = Path("data/test.txt")
    absolute_path = relative_path.resolve()
    print(f"\n相对路径: {relative_path}")
    print(f"绝对路径: {absolute_path}")
    
    # 路径规范化
    messy_path = Path("./data/../data/./test.txt")
    clean_path = messy_path.resolve()
    print(f"混乱路径: {messy_path}")
    print(f"规范化后: {clean_path}")
    
    """
    Java对比：
    Path absolute = relative.toAbsolutePath();
    Path normalized = messy.normalize();
    Path resolved = messy.resolve();
    """
    
    # 3. 相对路径计算
    path1 = Path("/home/user/projects/python")
    path2 = Path("/home/user/documents")
    
    try:
        relative_to = path1.relative_to(path2.parent)
        print(f"\n{path1} 相对于 {path2.parent}: {relative_to}")
    except ValueError as e:
        print(f"无法计算相对路径: {e}")
    
    """
    Java对比：
    Path relativePath = path2.relativize(path1);
    """


def file_metadata():
    """
    文件元数据操作
    """
    print("\n=== 文件元数据操作 ===")
    
    # 确保有测试文件
    test_file = Path("data/metadata_test.txt")
    test_file.parent.mkdir(exist_ok=True)
    test_file.write_text("测试文件内容\n第二行内容")
    
    # 1. 基本文件信息
    if test_file.exists():
        stat_info = test_file.stat()
        print(f"文件大小: {stat_info.st_size} 字节")
        print(f"创建时间: {datetime.fromtimestamp(stat_info.st_ctime)}")
        print(f"修改时间: {datetime.fromtimestamp(stat_info.st_mtime)}")
        print(f"访问时间: {datetime.fromtimestamp(stat_info.st_atime)}")
        print(f"文件权限: {oct(stat_info.st_mode)}")
        print(f"用户ID: {stat_info.st_uid}")
        print(f"组ID: {stat_info.st_gid}")
    
    """
    Java对比：
    BasicFileAttributes attrs = Files.readAttributes(path, BasicFileAttributes.class);
    long size = attrs.size();
    FileTime created = attrs.creationTime();
    FileTime modified = attrs.lastModifiedTime();
    """
    
    # 2. 文件权限操作 (Unix/Linux)
    try:
        # 获取当前权限
        current_mode = test_file.stat().st_mode
        print(f"\n当前权限: {stat.filemode(current_mode)}")
        
        # 修改权限 (仅在Unix/Linux系统有效)
        if os.name != 'nt':  # 非Windows系统
            test_file.chmod(0o644)
            print("权限已修改为: rw-r--r--")
    except Exception as e:
        print(f"权限操作失败: {e}")
    
    """
    Java对比：
    Set<PosixFilePermission> permissions = Files.getPosixFilePermissions(path);
    Files.setPosixFilePermissions(path, permissions);
    """
    
    # 3. 文件系统信息
    try:
        # 获取磁盘空间信息 (Python 3.3+)
        if hasattr(shutil, 'disk_usage'):
            total, used, free = shutil.disk_usage(test_file.parent)
            print(f"\n磁盘空间信息:")
            print(f"总空间: {total // (1024**3)} GB")
            print(f"已用空间: {used // (1024**3)} GB")
            print(f"可用空间: {free // (1024**3)} GB")
    except Exception as e:
        print(f"磁盘空间信息获取失败: {e}")
    
    """
    Java对比：
    FileStore store = Files.getFileStore(path);
    long total = store.getTotalSpace();
    long usable = store.getUsableSpace();
    """


def directory_operations():
    """
    目录操作
    """
    print("\n=== 目录操作 ===")
    
    # 1. 创建目录
    test_dir = Path("data/test_directories/sub1/sub2")
    
    # 创建多级目录
    test_dir.mkdir(parents=True, exist_ok=True)
    print(f"创建目录: {test_dir}")
    
    """
    Java对比：
    Files.createDirectories(path);
    """
    
    # 2. 目录遍历
    print("\n目录遍历:")
    
    # 方式1: iterdir() - 直接子项
    data_dir = Path("data")
    if data_dir.exists():
        print("data目录直接子项:")
        for item in data_dir.iterdir():
            item_type = "目录" if item.is_dir() else "文件"
            print(f"  {item_type}: {item.name}")
    
    """
    Java对比：
    try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir)) {
        for (Path entry : stream) {
            System.out.println(entry.getFileName());
        }
    }
    """
    
    # 方式2: glob() - 模式匹配
    print("\n使用glob模式匹配:")
    for py_file in Path(".").glob("**/*.py"):
        print(f"  Python文件: {py_file}")
        if len(list(Path(".").glob("**/*.py"))) > 5:  # 限制输出数量
            print("  ... (更多文件)")
            break
    
    # 方式3: rglob() - 递归glob
    print("\n使用rglob递归搜索:")
    for md_file in Path(".").rglob("*.md"):
        print(f"  Markdown文件: {md_file}")
    
    """
    Java对比：
    Files.walk(start)
        .filter(path -> path.toString().endsWith(".py"))
        .forEach(System.out::println);
    """
    
    # 3. 目录复制和移动
    source_dir = Path("data/test_directories")
    backup_dir = Path("data/backup_directories")
    
    try:
        if source_dir.exists() and not backup_dir.exists():
            # 复制整个目录树
            shutil.copytree(source_dir, backup_dir)
            print(f"目录已复制: {source_dir} -> {backup_dir}")
    except Exception as e:
        print(f"目录复制失败: {e}")
    
    """
    Java对比：
    // Java需要自己实现目录复制，或使用第三方库
    Files.walkFileTree(source, new SimpleFileVisitor<Path>() {
        @Override
        public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) {
            Files.copy(file, target.resolve(source.relativize(file)));
            return FileVisitResult.CONTINUE;
        }
    });
    """


def advanced_path_operations():
    """
    高级路径操作
    """
    print("\n=== 高级路径操作 ===")
    
    # 1. 临时文件和目录
    print("临时文件操作:")
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write("临时文件内容")
        temp_path = Path(temp_file.name)
        print(f"临时文件: {temp_path}")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        print(f"临时目录: {temp_dir_path}")
        
        # 在临时目录中创建文件
        temp_file_in_dir = temp_dir_path / "test.txt"
        temp_file_in_dir.write_text("临时目录中的文件")
        print(f"临时目录中的文件: {temp_file_in_dir}")
    
    # 清理临时文件
    if temp_path.exists():
        temp_path.unlink()
        print("临时文件已删除")
    
    """
    Java对比：
    Path tempFile = Files.createTempFile("prefix", ".txt");
    Path tempDir = Files.createTempDirectory("prefix");
    Files.delete(tempFile);
    """
    
    # 2. 文件查找和过滤
    print("\n文件查找和过滤:")
    
    # 查找特定类型的文件
    python_files = []
    for file_path in Path(".").rglob("*.py"):
        if len(python_files) < 3:  # 限制输出
            python_files.append(file_path)
            print(f"Python文件: {file_path}")
    
    # 按大小过滤文件
    print("\n大文件查找:")
    for file_path in Path(".").rglob("*"):
        if file_path.is_file():
            try:
                size = file_path.stat().st_size
                if size > 1024:  # 大于1KB的文件
                    print(f"大文件: {file_path} ({size} 字节)")
                    break  # 只显示一个示例
            except (OSError, FileNotFoundError):
                pass
    
    # 3. 路径匹配
    print("\n路径匹配:")
    test_paths = [
        Path("data/test.txt"),
        Path("src/main.py"),
        Path("docs/readme.md"),
        Path("config/settings.json")
    ]
    
    for path in test_paths:
        # fnmatch风格的模式匹配
        if path.match("*.py"):
            print(f"Python文件匹配: {path}")
        elif path.match("data/*"):
            print(f"数据文件匹配: {path}")
    
    """
    Java对比：
    PathMatcher matcher = FileSystems.getDefault().getPathMatcher("glob:*.py");
    if (matcher.matches(path.getFileName())) {
        System.out.println("匹配: " + path);
    }
    """


def cross_platform_considerations():
    """
    跨平台考虑
    """
    print("\n=== 跨平台考虑 ===")
    
    # 1. 平台检测
    print(f"操作系统: {os.name}")
    print(f"平台详细: {os.sys.platform}")
    print(f"路径分隔符: '{os.sep}'")
    print(f"路径列表分隔符: '{os.pathsep}'")
    
    # 2. 路径分隔符处理
    # pathlib自动处理平台差异
    cross_platform_path = Path("data") / "subdir" / "file.txt"
    print(f"跨平台路径: {cross_platform_path}")
    
    # 转换为平台特定格式
    print(f"平台特定格式: {cross_platform_path.as_posix()}")  # 总是使用/
    
    """
    Java对比：
    String separator = File.separator;
    Path path = Paths.get("data", "subdir", "file.txt");
    """
    
    # 3. 用户目录处理
    home_dir = Path.home()
    print(f"用户主目录: {home_dir}")
    
    # 配置目录 (示例)
    if os.name == 'nt':  # Windows
        config_dir = Path.home() / "AppData" / "Local" / "MyApp"
    else:  # Unix/Linux/macOS
        config_dir = Path.home() / ".config" / "myapp"
    
    print(f"配置目录: {config_dir}")
    
    """
    Java对比：
    String userHome = System.getProperty("user.home");
    Path homePath = Paths.get(userHome);
    """


def path_best_practices():
    """
    路径处理最佳实践
    """
    print("\n=== 路径处理最佳实践 ===")
    
    print("1. 使用pathlib而不是os.path")
    print("   ✓ 推荐: Path('data') / 'file.txt'")
    print("   ✗ 避免: os.path.join('data', 'file.txt')")
    
    print("\n2. 使用resolve()获取绝对路径")
    relative = Path("../data/file.txt")
    absolute = relative.resolve()
    print(f"   相对路径: {relative}")
    print(f"   绝对路径: {absolute}")
    
    print("\n3. 检查路径存在性")
    print("   ✓ 推荐: path.exists() 和 path.is_file()")
    print("   ✗ 避免: 直接操作可能不存在的路径")
    
    print("\n4. 使用with语句处理文件")
    print("   ✓ 推荐: with open(path) as f:")
    print("   ✗ 避免: f = open(path) 不关闭")
    
    print("\n5. 异常处理")
    test_path = Path("nonexistent/file.txt")
    try:
        content = test_path.read_text()
    except FileNotFoundError:
        print(f"   文件不存在异常处理示例: {test_path}")
    except PermissionError:
        print("   权限错误处理")
    except Exception as e:
        print(f"   其他异常: {e}")
    
    """
    Java最佳实践对比：
    1. 使用java.nio.file.Path而不是java.io.File
    2. 使用Files.exists()检查存在性
    3. 使用try-with-resources处理文件
    4. 适当的异常处理
    """


def performance_considerations():
    """
    性能考虑
    """
    print("\n=== 性能考虑 ===")
    
    print("1. 大目录遍历优化:")
    print("   - 使用iterdir()而不是listdir()")
    print("   - 使用glob()进行模式匹配")
    print("   - 避免递归遍历大目录")
    
    print("\n2. 文件操作优化:")
    print("   - 批量操作文件")
    print("   - 使用缓冲I/O")
    print("   - 避免频繁的stat()调用")
    
    print("\n3. 路径操作优化:")
    print("   - 缓存resolve()结果")
    print("   - 避免重复的路径规范化")
    print("   - 使用Path对象而不是字符串")
    
    # 简单性能测试示例
    import time
    
    # 测试路径拼接性能
    start_time = time.time()
    for i in range(1000):
        path = Path("data") / f"file_{i}.txt"
    pathlib_time = time.time() - start_time
    
    start_time = time.time()
    for i in range(1000):
        path = os.path.join("data", f"file_{i}.txt")
    os_path_time = time.time() - start_time
    
    print(f"\n性能测试 (1000次路径拼接):")
    print(f"pathlib: {pathlib_time:.4f}秒")
    print(f"os.path: {os_path_time:.4f}秒")


def main():
    """主函数：演示所有路径处理功能"""
    print("Python文件路径处理详解")
    print("=" * 50)
    
    try:
        # 确保数据目录存在
        Path("data").mkdir(exist_ok=True)
        
        # 执行各种路径处理示例
        path_basics()
        path_operations()
        file_metadata()
        directory_operations()
        advanced_path_operations()
        cross_platform_considerations()
        path_best_practices()
        performance_considerations()
        
    except Exception as e:
        print(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 