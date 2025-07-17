"""
Python vs Java 文件API全面对比
作者：Python学习项目
日期：2024-01-16

本文件详细对比Python和Java在文件处理方面的差异
重点：帮助Java开发者快速理解Python的文件处理方式
"""

import os
import io
import json
import csv
import pickle
import pathlib
from pathlib import Path
import tempfile
import shutil
import time
from contextlib import contextmanager


def file_creation_comparison():
    """
    文件创建方式对比
    """
    print("=== 文件创建方式对比 ===")
    
    # Python方式
    print("Python文件创建:")
    
    # 方式1: 内置open()函数
    with open("data/python_test.txt", "w", encoding="utf-8") as f:
        f.write("Python文件内容")
    print("✓ 使用open()函数创建文件")
    
    # 方式2: pathlib.Path
    test_path = Path("data/pathlib_test.txt")
    test_path.write_text("使用pathlib创建", encoding="utf-8")
    print("✓ 使用pathlib.Path.write_text()创建文件")
    
    # 方式3: 确保目录存在
    nested_path = Path("data/nested/deep/file.txt")
    nested_path.parent.mkdir(parents=True, exist_ok=True)
    nested_path.write_text("嵌套目录文件")
    print("✓ 自动创建多级目录")
    
    print("\nJava对比:")
    print("""
    // Java方式1: 传统File API
    File file = new File("data/java_test.txt");
    file.getParentFile().mkdirs();
    FileWriter writer = new FileWriter(file, StandardCharsets.UTF_8);
    writer.write("Java文件内容");
    writer.close();
    
    // Java方式2: NIO.2 API (推荐)
    Path path = Paths.get("data/nio_test.txt");
    Files.createDirectories(path.getParent());
    Files.write(path, "使用NIO.2创建".getBytes(StandardCharsets.UTF_8));
    
    // Java方式3: try-with-resources
    try (BufferedWriter writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
        writer.write("安全的文件写入");
    }
    """)
    
    print("主要差异:")
    print("1. Python: with语句自动资源管理")
    print("2. Java: try-with-resources或手动close()")
    print("3. Python: pathlib更简洁的API")
    print("4. Java: 需要显式处理编码和异常")


def file_reading_comparison():
    """
    文件读取方式对比
    """
    print("\n=== 文件读取方式对比 ===")
    
    # 确保测试文件存在
    test_file = Path("data/read_test.txt")
    test_file.parent.mkdir(exist_ok=True)
    test_file.write_text("第一行\n第二行\n第三行", encoding="utf-8")
    
    print("Python文件读取:")
    
    # 方式1: 读取全部内容
    with open(test_file, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"✓ 全部内容: {repr(content)}")
    
    # 方式2: 按行读取
    with open(test_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        print(f"✓ 按行读取: {lines}")
    
    # 方式3: 迭代读取 (内存友好)
    print("✓ 迭代读取:")
    with open(test_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            print(f"  行{line_num}: {line.strip()}")
    
    # 方式4: pathlib简化方式
    content = test_file.read_text(encoding="utf-8")
    print(f"✓ pathlib读取: {repr(content)}")
    
    print("\nJava对比:")
    print("""
    // Java方式1: Files.readAllLines() (小文件)
    List<String> lines = Files.readAllLines(path, StandardCharsets.UTF_8);
    
    // Java方式2: Files.lines() (大文件，流式处理)
    try (Stream<String> lines = Files.lines(path, StandardCharsets.UTF_8)) {
        lines.forEach(System.out::println);
    }
    
    // Java方式3: BufferedReader
    try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
        String line;
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }
    }
    
    // Java方式4: 全部内容
    String content = Files.readString(path, StandardCharsets.UTF_8); // Java 11+
    """)
    
    print("主要差异:")
    print("1. Python: 默认字符串处理，需指定编码")
    print("2. Java: 字节数组为主，流式处理更强")
    print("3. Python: 迭代器语法更简洁")
    print("4. Java: 类型安全，编译时检查")


def binary_file_comparison():
    """
    二进制文件处理对比
    """
    print("\n=== 二进制文件处理对比 ===")
    
    print("Python二进制文件:")
    
    # 写入二进制数据
    binary_data = b'\x00\x01\x02\x03\xFF\xFE\xFD'
    binary_file = Path("data/binary_test.bin")
    
    # 方式1: open() with 'rb'/'wb'
    with open(binary_file, "wb") as f:
        f.write(binary_data)
    print("✓ 写入二进制数据")
    
    # 方式2: pathlib
    binary_file.write_bytes(binary_data)
    print("✓ pathlib写入二进制")
    
    # 读取二进制数据
    with open(binary_file, "rb") as f:
        read_data = f.read()
        print(f"✓ 读取二进制: {read_data.hex()}")
    
    # pathlib读取
    read_data2 = binary_file.read_bytes()
    print(f"✓ pathlib读取: {read_data2.hex()}")
    
    print("\nJava对比:")
    print("""
    // Java写入二进制
    byte[] data = {0x00, 0x01, 0x02, 0x03, (byte)0xFF, (byte)0xFE, (byte)0xFD};
    Files.write(path, data);
    
    // Java读取二进制
    byte[] readData = Files.readAllBytes(path);
    
    // 使用流处理大文件
    try (InputStream in = Files.newInputStream(path);
         OutputStream out = Files.newOutputStream(targetPath)) {
        byte[] buffer = new byte[8192];
        int bytesRead;
        while ((bytesRead = in.read(buffer)) != -1) {
            out.write(buffer, 0, bytesRead);
        }
    }
    """)
    
    print("主要差异:")
    print("1. Python: 文本/二进制模式由文件打开方式决定")
    print("2. Java: 字节数组和流的严格区分")
    print("3. Python: bytes类型自动处理")
    print("4. Java: 需要显式缓冲区管理")


def file_operations_comparison():
    """
    文件操作对比
    """
    print("\n=== 文件操作对比 ===")
    
    print("Python文件操作:")
    
    # 创建测试文件
    source_file = Path("data/source.txt")
    source_file.write_text("源文件内容")
    
    # 1. 复制文件
    target_file = Path("data/target.txt")
    shutil.copy2(source_file, target_file)  # 保留元数据
    print("✓ 文件复制 (shutil.copy2)")
    
    # 2. 移动文件
    moved_file = Path("data/moved.txt")
    shutil.move(str(target_file), str(moved_file))
    print("✓ 文件移动 (shutil.move)")
    
    # 3. 删除文件
    if moved_file.exists():
        moved_file.unlink()
        print("✓ 文件删除 (Path.unlink)")
    
    # 4. 文件信息
    if source_file.exists():
        stat_info = source_file.stat()
        print(f"✓ 文件大小: {stat_info.st_size} 字节")
        print(f"✓ 修改时间: {stat_info.st_mtime}")
    
    print("\nJava对比:")
    print("""
    // Java文件操作
    Path source = Paths.get("data/source.txt");
    Path target = Paths.get("data/target.txt");
    
    // 复制文件
    Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING,
               StandardCopyOption.COPY_ATTRIBUTES);
    
    // 移动文件
    Files.move(target, moved, StandardCopyOption.REPLACE_EXISTING);
    
    // 删除文件
    Files.delete(moved);
    // 或者安全删除
    Files.deleteIfExists(moved);
    
    // 文件信息
    BasicFileAttributes attrs = Files.readAttributes(source, BasicFileAttributes.class);
    long size = attrs.size();
    FileTime modified = attrs.lastModifiedTime();
    """)
    
    print("主要差异:")
    print("1. Python: shutil模块提供高级操作")
    print("2. Java: Files类提供原子操作")
    print("3. Python: 路径可以是字符串或Path对象")
    print("4. Java: 强类型Path参数")


def encoding_comparison():
    """
    编码处理对比
    """
    print("\n=== 编码处理对比 ===")
    
    print("Python编码处理:")
    
    # 测试各种编码
    test_content = "Hello 世界 🌍"
    encoding_file = Path("data/encoding_test.txt")
    
    # UTF-8编码
    encoding_file.write_text(test_content, encoding="utf-8")
    read_content = encoding_file.read_text(encoding="utf-8")
    print(f"✓ UTF-8: {read_content}")
    
    # GBK编码
    try:
        with open(encoding_file, "w", encoding="gbk") as f:
            f.write("简体中文测试")
        with open(encoding_file, "r", encoding="gbk") as f:
            content = f.read()
            print(f"✓ GBK: {content}")
    except UnicodeEncodeError as e:
        print(f"✗ GBK编码失败: {e}")
    
    # 错误处理策略
    problematic_content = "Hello \udcff World"  # 包含无效字符
    try:
        with open(encoding_file, "w", encoding="ascii", errors="ignore") as f:
            f.write(problematic_content)
        print("✓ ASCII编码 (忽略错误)")
    except Exception as e:
        print(f"编码错误: {e}")
    
    print("\nJava对比:")
    print("""
    // Java编码处理
    String content = "Hello 世界 🌍";
    
    // UTF-8编码
    Files.write(path, content.getBytes(StandardCharsets.UTF_8));
    String readContent = Files.readString(path, StandardCharsets.UTF_8);
    
    // GBK编码
    Charset gbk = Charset.forName("GBK");
    Files.write(path, content.getBytes(gbk));
    String gbkContent = Files.readString(path, gbk);
    
    // 错误处理
    CharsetEncoder encoder = StandardCharsets.US_ASCII.newEncoder();
    encoder.onMalformedInput(CodingErrorAction.IGNORE);
    encoder.onUnmappableCharacter(CodingErrorAction.IGNORE);
    """)
    
    print("主要差异:")
    print("1. Python: 字符串默认Unicode，需指定文件编码")
    print("2. Java: 需要显式字节数组转换")
    print("3. Python: errors参数简化错误处理")
    print("4. Java: CharsetEncoder提供细粒度控制")


def structured_data_comparison():
    """
    结构化数据处理对比
    """
    print("\n=== 结构化数据处理对比 ===")
    
    print("Python结构化数据:")
    
    # JSON处理
    data = {
        "name": "张三",
        "age": 30,
        "skills": ["Python", "Java", "Go"],
        "address": {
            "city": "北京",
            "district": "朝阳区"
        }
    }
    
    json_file = Path("data/test.json")
    
    # 写入JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✓ JSON写入")
    
    # 读取JSON
    with open(json_file, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    print(f"✓ JSON读取: {loaded_data['name']}")
    
    # CSV处理
    csv_file = Path("data/test.csv")
    csv_data = [
        ["姓名", "年龄", "城市"],
        ["张三", "30", "北京"],
        ["李四", "25", "上海"],
        ["王五", "35", "广州"]
    ]
    
    # 写入CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    print("✓ CSV写入")
    
    # 读取CSV
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            print(f"  CSV行: {row}")
    
    # Pickle处理 (Python特有)
    pickle_file = Path("data/test.pkl")
    pickle_data = {"complex": data, "function": lambda x: x * 2}
    
    with open(pickle_file, "wb") as f:
        pickle.dump(pickle_data, f)
    print("✓ Pickle序列化")
    
    print("\nJava对比:")
    print("""
    // Java JSON处理 (使用Jackson或Gson)
    ObjectMapper mapper = new ObjectMapper();
    
    // 写入JSON
    Person person = new Person("张三", 30, Arrays.asList("Python", "Java"));
    mapper.writeValue(new File("test.json"), person);
    
    // 读取JSON
    Person loaded = mapper.readValue(new File("test.json"), Person.class);
    
    // CSV处理 (使用OpenCSV)
    try (CSVWriter writer = new CSVWriter(new FileWriter("test.csv"))) {
        String[] header = {"姓名", "年龄", "城市"};
        writer.writeNext(header);
        writer.writeNext(new String[]{"张三", "30", "北京"});
    }
    
    // 对象序列化
    try (ObjectOutputStream oos = new ObjectOutputStream(
            new FileOutputStream("test.ser"))) {
        oos.writeObject(person);
    }
    """)
    
    print("主要差异:")
    print("1. Python: 内置json/csv模块，直接支持")
    print("2. Java: 需要第三方库处理JSON/CSV")
    print("3. Python: Pickle支持任意Python对象")
    print("4. Java: 对象需要实现Serializable接口")


def stream_processing_comparison():
    """
    流处理对比
    """
    print("\n=== 流处理对比 ===")
    
    print("Python流处理:")
    
    # 创建大文件模拟
    large_file = Path("data/large_file.txt")
    
    # 生成测试数据
    with open(large_file, "w", encoding="utf-8") as f:
        for i in range(1000):
            f.write(f"第{i+1}行数据\n")
    
    # 流式读取 (内存友好)
    line_count = 0
    with open(large_file, "r", encoding="utf-8") as f:
        for line in f:
            line_count += 1
            if line_count <= 3:  # 只显示前3行
                print(f"  {line.strip()}")
    print(f"✓ 流式处理完成，共{line_count}行")
    
    # 使用生成器处理
    def read_large_file(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                yield line.strip()
    
    # 生成器使用
    for i, line in enumerate(read_large_file(large_file)):
        if i >= 3:  # 只处理前3行
            break
        print(f"  生成器: {line}")
    
    print("\nJava对比:")
    print("""
    // Java流式处理
    
    // 方式1: BufferedReader逐行读取
    try (BufferedReader reader = Files.newBufferedReader(path)) {
        String line;
        while ((line = reader.readLine()) != null) {
            // 处理每一行
            processLine(line);
        }
    }
    
    // 方式2: Stream API (Java 8+)
    try (Stream<String> lines = Files.lines(path)) {
        lines.filter(line -> line.contains("关键词"))
             .map(String::toUpperCase)
             .forEach(System.out::println);
    }
    
    // 方式3: 大文件分块读取
    try (InputStream in = Files.newInputStream(path)) {
        byte[] buffer = new byte[8192];
        int bytesRead;
        while ((bytesRead = in.read(buffer)) != -1) {
            // 处理缓冲区数据
            processBuffer(buffer, bytesRead);
        }
    }
    """)
    
    print("主要差异:")
    print("1. Python: for循环自动处理文件迭代")
    print("2. Java: Stream API提供函数式处理")
    print("3. Python: 生成器语法简洁")
    print("4. Java: 更精细的缓冲区控制")


def performance_comparison():
    """
    性能对比
    """
    print("\n=== 性能对比 ===")
    
    print("Python性能测试:")
    
    test_file = Path("data/performance_test.txt")
    test_data = "测试数据" * 1000  # 重复数据
    
    # 测试写入性能
    start_time = time.time()
    with open(test_file, "w", encoding="utf-8") as f:
        for i in range(100):
            f.write(f"{i}: {test_data}\n")
    write_time = time.time() - start_time
    print(f"✓ 写入100行 (每行{len(test_data)}字符): {write_time:.4f}秒")
    
    # 测试读取性能
    start_time = time.time()
    line_count = 0
    with open(test_file, "r", encoding="utf-8") as f:
        for line in f:
            line_count += 1
    read_time = time.time() - start_time
    print(f"✓ 读取{line_count}行: {read_time:.4f}秒")
    
    # 测试pathlib vs open性能
    start_time = time.time()
    for i in range(100):
        test_file.read_text(encoding="utf-8")
    pathlib_time = time.time() - start_time
    
    start_time = time.time()
    for i in range(100):
        with open(test_file, "r", encoding="utf-8") as f:
            f.read()
    open_time = time.time() - start_time
    
    print(f"✓ pathlib读取100次: {pathlib_time:.4f}秒")
    print(f"✓ open()读取100次: {open_time:.4f}秒")
    
    print("\nJava性能特点:")
    print("""
    Java性能优势：
    1. 编译型语言，执行效率高
    2. JVM优化，热点代码加速
    3. 精确的内存管理
    4. NIO零拷贝技术
    
    Python性能特点：
    1. 解释型语言，开发效率高
    2. 简洁的语法，代码量少
    3. 丰富的标准库
    4. 适合原型开发和脚本任务
    """)
    
    print("性能优化建议:")
    print("1. Python: 使用适当的缓冲区大小")
    print("2. Python: 考虑使用Cython或PyPy")
    print("3. Java: 合理使用缓冲流")
    print("4. 都要: 避免频繁的小文件操作")


def error_handling_comparison():
    """
    错误处理对比
    """
    print("\n=== 错误处理对比 ===")
    
    print("Python错误处理:")
    
    # 常见文件错误处理
    try:
        # 文件不存在
        with open("nonexistent.txt", "r") as f:
            content = f.read()
    except FileNotFoundError:
        print("✓ 捕获文件不存在异常")
    
    try:
        # 权限错误 (模拟)
        restricted_file = Path("data/restricted.txt")
        restricted_file.write_text("测试")
        # 在Unix系统上移除读权限
        if os.name != 'nt':
            restricted_file.chmod(0o000)
        
        with open(restricted_file, "r") as f:
            content = f.read()
    except PermissionError:
        print("✓ 捕获权限错误")
    except Exception as e:
        print(f"✓ 其他错误: {type(e).__name__}")
    finally:
        # 恢复权限并清理
        if restricted_file.exists():
            try:
                if os.name != 'nt':
                    restricted_file.chmod(0o644)
                restricted_file.unlink()
            except:
                pass
    
    # 编码错误处理
    try:
        with open("data/encoding_test.txt", "w", encoding="ascii") as f:
            f.write("包含中文的内容")
    except UnicodeEncodeError as e:
        print(f"✓ 捕获编码错误: {e}")
    
    print("\nJava对比:")
    print("""
    // Java错误处理
    try {
        // 文件操作
        List<String> lines = Files.readAllLines(path);
    } catch (NoSuchFileException e) {
        System.out.println("文件不存在: " + e.getMessage());
    } catch (AccessDeniedException e) {
        System.out.println("权限不足: " + e.getMessage());
    } catch (IOException e) {
        System.out.println("IO错误: " + e.getMessage());
    } finally {
        // 清理资源
        cleanup();
    }
    
    // try-with-resources自动关闭
    try (BufferedReader reader = Files.newBufferedReader(path)) {
        return reader.lines().collect(Collectors.toList());
    } catch (IOException e) {
        throw new ServiceException("读取文件失败", e);
    }
    """)
    
    print("主要差异:")
    print("1. Python: with语句自动资源管理")
    print("2. Java: try-with-resources或finally块")
    print("3. Python: 异常类型更简单直观")
    print("4. Java: 检查异常强制处理")


@contextmanager
def file_context_manager(filename, mode="r", encoding="utf-8"):
    """
    自定义文件上下文管理器示例
    """
    print(f"打开文件: {filename}")
    f = None
    try:
        f = open(filename, mode, encoding=encoding)
        yield f
    except Exception as e:
        print(f"文件操作错误: {e}")
        raise
    finally:
        if f:
            f.close()
            print(f"关闭文件: {filename}")


def advanced_features_comparison():
    """
    高级特性对比
    """
    print("\n=== 高级特性对比 ===")
    
    print("Python高级特性:")
    
    # 1. 上下文管理器
    print("1. 自定义上下文管理器:")
    try:
        with file_context_manager("data/context_test.txt", "w") as f:
            f.write("上下文管理器测试")
        print("✓ 自定义上下文管理器")
    except Exception as e:
        print(f"错误: {e}")
    
    # 2. 文件对象作为迭代器
    print("\n2. 文件迭代器:")
    test_file = Path("data/iterator_test.txt")
    test_file.write_text("行1\n行2\n行3")
    
    with open(test_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            print(f"  第{i}行: {line.strip()}")
    
    # 3. 内存映射文件
    print("\n3. 内存映射文件 (mmap):")
    try:
        import mmap
        with open(test_file, "r+b") as f:
            with mmap.mmap(f.fileno(), 0) as mm:
                content = mm.read().decode('utf-8')
                print(f"  mmap内容: {repr(content[:20])}")
    except Exception as e:
        print(f"  mmap失败: {e}")
    
    print("\nJava对比:")
    print("""
    // Java高级特性
    
    // 1. try-with-resources多资源
    try (FileInputStream fis = new FileInputStream(source);
         FileOutputStream fos = new FileOutputStream(target);
         BufferedInputStream bis = new BufferedInputStream(fis);
         BufferedOutputStream bos = new BufferedOutputStream(fos)) {
        
        byte[] buffer = new byte[8192];
        int bytesRead;
        while ((bytesRead = bis.read(buffer)) != -1) {
            bos.write(buffer, 0, bytesRead);
        }
    }
    
    // 2. NIO Channel
    try (FileChannel sourceChannel = FileChannel.open(source, StandardOpenOption.READ);
         FileChannel targetChannel = FileChannel.open(target, 
             StandardOpenOption.WRITE, StandardOpenOption.CREATE)) {
        sourceChannel.transferTo(0, sourceChannel.size(), targetChannel);
    }
    
    // 3. 内存映射文件
    try (RandomAccessFile file = new RandomAccessFile("test.txt", "rw");
         FileChannel channel = file.getChannel()) {
        MappedByteBuffer buffer = channel.map(
            FileChannel.MapMode.READ_WRITE, 0, file.length());
        // 直接操作内存映射
    }
    """)


def migration_guide():
    """
    迁移指南
    """
    print("\n=== Java到Python迁移指南 ===")
    
    print("常用操作映射:")
    
    mapping_table = [
        ("Java", "Python", "说明"),
        ("-" * 20, "-" * 25, "-" * 20),
        ("new File(path)", "Path(path)", "路径对象创建"),
        ("Files.exists(path)", "path.exists()", "检查存在性"),
        ("Files.readAllLines()", "path.read_text().splitlines()", "读取所有行"),
        ("Files.write()", "path.write_text()", "写入文本"),
        ("Files.copy()", "shutil.copy2()", "复制文件"),
        ("Files.move()", "shutil.move()", "移动文件"),
        ("Files.delete()", "path.unlink()", "删除文件"),
        ("Files.createDirectories()", "path.mkdir(parents=True)", "创建目录"),
        ("try-with-resources", "with语句", "资源管理"),
        ("FileInputStream", "open(mode='rb')", "二进制读取"),
        ("FileOutputStream", "open(mode='wb')", "二进制写入"),
        ("BufferedReader", "open()迭代", "按行读取"),
        ("ObjectOutputStream", "pickle.dump()", "对象序列化"),
    ]
    
    for java_way, python_way, description in mapping_table:
        print(f"{java_way:<20} | {python_way:<25} | {description}")
    
    print("\n迁移建议:")
    print("1. 优先使用pathlib.Path而不是os.path")
    print("2. 使用with语句确保资源正确释放")
    print("3. 明确指定文件编码，避免编码问题")
    print("4. 利用Python的简洁语法减少代码量")
    print("5. 使用生成器处理大文件，节省内存")
    print("6. 合理使用异常处理，不要忽略错误")
    
    print("\n注意事项:")
    print("1. Python字符串默认Unicode，Java需要显式转换")
    print("2. Python的with自动管理资源，Java需要try-with-resources")
    print("3. Python路径操作更简洁，但性能可能略低")
    print("4. Python的duck typing vs Java的强类型检查")


def main():
    """主函数：演示所有对比内容"""
    print("Python vs Java 文件API全面对比")
    print("=" * 60)
    
    try:
        # 确保数据目录存在
        Path("data").mkdir(exist_ok=True)
        
        # 执行所有对比
        file_creation_comparison()
        file_reading_comparison()
        binary_file_comparison()
        file_operations_comparison()
        encoding_comparison()
        structured_data_comparison()
        stream_processing_comparison()
        performance_comparison()
        error_handling_comparison()
        advanced_features_comparison()
        migration_guide()
        
        print("\n学习建议:")
        print("1. 先掌握pathlib，它是Python文件处理的现代方式")
        print("2. 理解with语句的重要性，它能避免资源泄露")
        print("3. 熟悉Python的编码处理，避免中文乱码问题")
        print("4. 学会使用生成器处理大文件，这是Python的优势")
        print("5. 了解Python的序列化工具，简化数据存储")
        
    except Exception as e:
        print(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 