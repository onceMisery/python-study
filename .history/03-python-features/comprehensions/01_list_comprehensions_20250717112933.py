"""
Python列表推导式详解
作者：Python学习项目
日期：2024-01-16

本文件演示Python列表推导式的各种用法和最佳实践
重点：列表推导式 vs Java Stream API的对比
"""

import time
import random
from typing import List, Any


def basic_list_comprehensions():
    """
    基础列表推导式
    
    Java对比：
    Python: [expression for item in iterable]
    Java: list.stream().map(function).collect(Collectors.toList())
    """
    print("=== 基础列表推导式 ===")
    
    # 1. 基本语法
    numbers = [1, 2, 3, 4, 5]
    
    # 传统方式
    squares_traditional = []
    for x in numbers:
        squares_traditional.append(x ** 2)
    print(f"传统方式: {squares_traditional}")
    
    # 列表推导式
    squares_comprehension = [x ** 2 for x in numbers]
    print(f"列表推导式: {squares_comprehension}")
    
    """
    Java对比：
    // 传统方式
    List<Integer> squares = new ArrayList<>();
    for (Integer x : numbers) {
        squares.add(x * x);
    }
    
    // Stream API
    List<Integer> squares = numbers.stream()
        .map(x -> x * x)
        .collect(Collectors.toList());
    """
    
    # 2. 字符串处理
    words = ["hello", "world", "python", "java"]
    
    # 转换为大写
    upper_words = [word.upper() for word in words]
    print(f"大写转换: {upper_words}")
    
    # 获取长度
    word_lengths = [len(word) for word in words]
    print(f"单词长度: {word_lengths}")
    
    # 首字母大写
    capitalized = [word.capitalize() for word in words]
    print(f"首字母大写: {capitalized}")
    
    """
    Java对比：
    List<String> upperWords = words.stream()
        .map(String::toUpperCase)
        .collect(Collectors.toList());
    
    List<Integer> lengths = words.stream()
        .map(String::length)
        .collect(Collectors.toList());
    """
    
    # 3. 数学运算
    print("\n数学运算示例:")
    
    # 平方根
    import math
    sqrt_values = [math.sqrt(x) for x in range(1, 11)]
    print(f"平方根: {[round(x, 2) for x in sqrt_values]}")
    
    # 三角函数
    angles = [0, 30, 45, 60, 90]
    sin_values = [math.sin(math.radians(angle)) for angle in angles]
    print(f"正弦值: {[round(x, 3) for x in sin_values]}")
    
    # 复杂表达式
    complex_calc = [x**2 + 2*x + 1 for x in range(5)]
    print(f"复杂计算 (x²+2x+1): {complex_calc}")


def conditional_comprehensions():
    """
    条件列表推导式
    """
    print("\n=== 条件列表推导式 ===")
    
    numbers = list(range(1, 21))
    
    # 1. 过滤条件 (if子句)
    # 偶数
    evens = [x for x in numbers if x % 2 == 0]
    print(f"偶数: {evens}")
    
    # 奇数且大于10
    odd_gt_10 = [x for x in numbers if x % 2 == 1 and x > 10]
    print(f"奇数且>10: {odd_gt_10}")
    
    # 能被3整除的数
    divisible_by_3 = [x for x in numbers if x % 3 == 0]
    print(f"能被3整除: {divisible_by_3}")
    
    """
    Java对比：
    List<Integer> evens = numbers.stream()
        .filter(x -> x % 2 == 0)
        .collect(Collectors.toList());
    
    List<Integer> oddGt10 = numbers.stream()
        .filter(x -> x % 2 == 1 && x > 10)
        .collect(Collectors.toList());
    """
    
    # 2. 条件表达式 (三元运算符)
    # 正数保留，负数变为0
    mixed_numbers = [-3, -1, 0, 2, 5, -2, 8]
    positive_or_zero = [x if x > 0 else 0 for x in mixed_numbers]
    print(f"正数或0: {positive_or_zero}")
    
    # 奇偶标记
    parity_labels = ["偶数" if x % 2 == 0 else "奇数" for x in numbers[:10]]
    print(f"奇偶标记: {parity_labels}")
    
    # 分级标记
    scores = [85, 92, 78, 96, 88, 71, 89, 94]
    grades = ["优秀" if score >= 90 else "良好" if score >= 80 else "及格" if score >= 60 else "不及格" 
              for score in scores]
    print(f"成绩分级: {grades}")
    
    """
    Java对比：
    List<Integer> positiveOrZero = mixedNumbers.stream()
        .map(x -> x > 0 ? x : 0)
        .collect(Collectors.toList());
    
    List<String> grades = scores.stream()
        .map(score -> score >= 90 ? "优秀" : 
                     score >= 80 ? "良好" : 
                     score >= 60 ? "及格" : "不及格")
        .collect(Collectors.toList());
    """
    
    # 3. 复杂条件
    # 字符串过滤和转换
    words = ["apple", "banana", "cat", "dog", "elephant", "fox"]
    
    # 长度大于3的单词转大写
    long_words_upper = [word.upper() for word in words if len(word) > 3]
    print(f"长单词大写: {long_words_upper}")
    
    # 包含特定字母的单词
    words_with_a = [word for word in words if 'a' in word]
    print(f"包含字母a: {words_with_a}")
    
    # 不以元音字母开头的单词
    consonant_start = [word for word in words if word[0].lower() not in 'aeiou']
    print(f"辅音开头: {consonant_start}")


def nested_comprehensions():
    """
    嵌套列表推导式
    """
    print("\n=== 嵌套列表推导式 ===")
    
    # 1. 二维列表处理
    matrix = [
        [1, 2, 3],
        [4, 5, 6], 
        [7, 8, 9]
    ]
    
    # 展平二维列表
    flattened = [element for row in matrix for element in row]
    print(f"展平矩阵: {flattened}")
    
    # 矩阵转置
    transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    print(f"转置矩阵: {transposed}")
    
    # 矩阵每个元素平方
    squared_matrix = [[element**2 for element in row] for row in matrix]
    print(f"平方矩阵: {squared_matrix}")
    
    """
    Java对比：
    // 展平二维列表
    List<Integer> flattened = matrix.stream()
        .flatMap(List::stream)
        .collect(Collectors.toList());
    
    // 矩阵每个元素平方  
    List<List<Integer>> squared = matrix.stream()
        .map(row -> row.stream()
            .map(x -> x * x)
            .collect(Collectors.toList()))
        .collect(Collectors.toList());
    """
    
    # 2. 笛卡尔积
    colors = ["red", "green", "blue"]
    sizes = ["S", "M", "L"]
    
    # 所有颜色和尺寸的组合
    combinations = [f"{color}-{size}" for color in colors for size in sizes]
    print(f"颜色尺寸组合: {combinations}")
    
    # 带条件的组合
    filtered_combinations = [f"{color}-{size}" for color in colors for size in sizes 
                           if not (color == "red" and size == "S")]
    print(f"过滤组合: {filtered_combinations}")
    
    # 3. 复杂嵌套
    # 九九乘法表
    multiplication_table = [f"{i}×{j}={i*j}" for i in range(1, 10) for j in range(1, i+1)]
    print("九九乘法表（部分）:")
    for i, item in enumerate(multiplication_table[:15]):
        print(f"  {item}", end="  ")
        if (i + 1) % 5 == 0:
            print()  # 每5个换行
    
    # 4. 三层嵌套
    # 生成三维坐标点
    coordinates = [(x, y, z) for x in range(2) for y in range(2) for z in range(2)]
    print(f"\n三维坐标点: {coordinates}")


def advanced_comprehensions():
    """
    高级列表推导式技巧
    """
    print("\n=== 高级列表推导式技巧 ===")
    
    # 1. 使用函数
    def is_prime(n):
        """判断是否为质数"""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    # 找出100以内的质数
    primes = [n for n in range(2, 101) if is_prime(n)]
    print(f"100以内质数: {primes[:10]}...")  # 只显示前10个
    
    # 2. 使用enumerate
    fruits = ["apple", "banana", "cherry", "date"]
    indexed_fruits = [f"{i}: {fruit}" for i, fruit in enumerate(fruits)]
    print(f"带索引的水果: {indexed_fruits}")
    
    # 3. 使用zip
    names = ["Alice", "Bob", "Charlie"]
    ages = [25, 30, 35]
    people = [f"{name}({age}岁)" for name, age in zip(names, ages)]
    print(f"人员信息: {people}")
    
    # 4. 字典键值处理
    student_scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "David": 96}
    
    # 高分学生名单
    high_scorers = [name for name, score in student_scores.items() if score >= 90]
    print(f"高分学生: {high_scorers}")
    
    # 格式化输出
    score_reports = [f"{name}: {score}分" for name, score in student_scores.items()]
    print(f"成绩报告: {score_reports}")
    
    # 5. 使用多个可迭代对象
    subjects = ["数学", "英语", "物理"]
    alice_scores = [85, 90, 88]
    bob_scores = [92, 87, 91]
    
    # 比较两个学生的成绩
    comparisons = [f"{subject}: Alice {a_score} vs Bob {b_score}" 
                  for subject, a_score, b_score in zip(subjects, alice_scores, bob_scores)]
    print("成绩对比:")
    for comp in comparisons:
        print(f"  {comp}")
    
    # 6. 条件复杂化
    # 文件名处理
    files = ["document.txt", "image.jpg", "script.py", "data.csv", "archive.zip"]
    
    # 根据扩展名分类
    text_files = [f for f in files if f.endswith(('.txt', '.py', '.csv'))]
    image_files = [f for f in files if f.endswith(('.jpg', '.png', '.gif'))]
    
    print(f"文本文件: {text_files}")
    print(f"图片文件: {image_files}")


def performance_comparison():
    """
    性能对比测试
    """
    print("\n=== 性能对比测试 ===")
    
    # 准备测试数据
    large_numbers = list(range(100000))
    
    # 1. 传统for循环 vs 列表推导式
    print("测试：计算平方")
    
    # 传统for循环
    start_time = time.time()
    squares_for = []
    for x in large_numbers:
        squares_for.append(x ** 2)
    for_loop_time = time.time() - start_time
    
    # 列表推导式
    start_time = time.time()
    squares_comp = [x ** 2 for x in large_numbers]
    comprehension_time = time.time() - start_time
    
    print(f"for循环耗时: {for_loop_time:.4f}秒")
    print(f"列表推导式耗时: {comprehension_time:.4f}秒")
    print(f"性能提升: {for_loop_time/comprehension_time:.2f}倍")
    
    # 2. map() vs 列表推导式
    print("\n测试：字符串处理")
    
    words = ["hello"] * 50000
    
    # map函数
    start_time = time.time()
    upper_map = list(map(str.upper, words))
    map_time = time.time() - start_time
    
    # 列表推导式
    start_time = time.time()
    upper_comp = [word.upper() for word in words]
    comprehension_time = time.time() - start_time
    
    print(f"map()耗时: {map_time:.4f}秒")
    print(f"列表推导式耗时: {comprehension_time:.4f}秒")
    
    # 3. filter() vs 条件推导式
    print("\n测试：条件过滤")
    
    test_numbers = list(range(50000))
    
    # filter函数
    start_time = time.time()
    evens_filter = list(filter(lambda x: x % 2 == 0, test_numbers))
    filter_time = time.time() - start_time
    
    # 条件列表推导式
    start_time = time.time()
    evens_comp = [x for x in test_numbers if x % 2 == 0]
    comprehension_time = time.time() - start_time
    
    print(f"filter()耗时: {filter_time:.4f}秒")
    print(f"条件推导式耗时: {comprehension_time:.4f}秒")
    
    """
    Java Stream API性能特点：
    1. 延迟计算 - 只有终端操作时才执行
    2. 并行处理 - parallelStream()支持多线程
    3. 内存优化 - 不创建中间集合
    4. 优化器 - JVM可以优化Stream操作
    
    Python列表推导式特点：
    1. 立即执行 - 直接生成结果列表
    2. 内存占用 - 一次性创建完整列表
    3. 语法简洁 - 更直观易读
    4. 性能优异 - C级别优化
    """


def common_patterns():
    """
    常用模式和最佳实践
    """
    print("\n=== 常用模式和最佳实践 ===")
    
    # 1. 数据清洗
    print("1. 数据清洗模式:")
    
    # 清理字符串数据
    raw_data = ["  Alice  ", "", "Bob\n", "  ", "Charlie\t", None]
    cleaned_data = [item.strip() for item in raw_data if item and item.strip()]
    print(f"  原始数据: {raw_data}")
    print(f"  清洗后: {cleaned_data}")
    
    # 转换数据类型
    string_numbers = ["1", "2", "abc", "4", "5.5", ""]
    valid_numbers = [float(s) for s in string_numbers if s and s.replace('.', '').replace('-', '').isdigit()]
    print(f"  有效数字: {valid_numbers}")
    
    # 2. 数据转换
    print("\n2. 数据转换模式:")
    
    # 字典转换
    users = [
        {"name": "Alice", "age": 25, "city": "Beijing"},
        {"name": "Bob", "age": 30, "city": "Shanghai"},
        {"name": "Charlie", "age": 35, "city": "Guangzhou"}
    ]
    
    # 提取特定字段
    names = [user["name"] for user in users]
    ages = [user["age"] for user in users]
    print(f"  姓名列表: {names}")
    print(f"  年龄列表: {ages}")
    
    # 格式化输出
    user_info = [f"{user['name']}({user['age']}) - {user['city']}" for user in users]
    print(f"  用户信息: {user_info}")
    
    # 3. 条件处理
    print("\n3. 条件处理模式:")
    
    # 成绩分级
    scores = [95, 87, 92, 78, 85, 91, 76, 88, 94, 82]
    
    def get_grade(score):
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        else:
            return "D"
    
    grades = [get_grade(score) for score in scores]
    grade_distribution = {grade: grades.count(grade) for grade in set(grades)}
    print(f"  分数: {scores}")
    print(f"  等级: {grades}")
    print(f"  分布: {grade_distribution}")
    
    # 4. 聚合操作
    print("\n4. 聚合操作模式:")
    
    # 按条件分组
    numbers = list(range(1, 21))
    evens = [x for x in numbers if x % 2 == 0]
    odds = [x for x in numbers if x % 2 == 1]
    
    print(f"  偶数: {evens}")
    print(f"  奇数: {odds}")
    
    # 统计计算
    temperatures = [23.5, 25.1, 22.8, 26.3, 24.7, 21.9, 27.2]
    above_25 = [temp for temp in temperatures if temp > 25]
    below_23 = [temp for temp in temperatures if temp < 23]
    
    print(f"  高温(>25°C): {len(above_25)}天, 平均{sum(above_25)/len(above_25):.1f}°C")
    print(f"  低温(<23°C): {len(below_23)}天, 平均{sum(below_23)/len(below_23):.1f}°C")


def best_practices_and_pitfalls():
    """
    最佳实践和常见陷阱
    """
    print("\n=== 最佳实践和常见陷阱 ===")
    
    print("✓ 最佳实践:")
    
    # 1. 简洁性
    print("1. 保持简洁性")
    print("   ✓ 好: [x*2 for x in range(10)]")
    print("   ✗ 避免: [complex_function(x, y, z) for x in items for y in other_items if condition1 and condition2]")
    
    # 2. 可读性
    print("\n2. 优先可读性")
    numbers = [1, 2, 3, 4, 5]
    
    # 好的例子
    squares = [x**2 for x in numbers]
    print(f"   清晰易读: {squares}")
    
    # 不好的例子（功能相同但可读性差）
    # result = [x**2 if x%2==0 else x**3 if x%3==0 else x for x in numbers if x>0]
    
    # 3. 性能考虑
    print("\n3. 性能考虑")
    print("   ✓ 对于小到中等数据集，列表推导式很好")
    print("   ✓ 对于大数据集，考虑生成器表达式")
    print("   ✓ 避免在推导式中调用复杂函数")
    
    # 4. 嵌套限制
    print("\n4. 避免过度嵌套")
    print("   ✓ 1-2层嵌套可接受")
    print("   ✗ 3层以上嵌套考虑重构")
    
    print("\n⚠ 常见陷阱:")
    
    # 陷阱1: 修改原列表
    print("1. 不要在推导式中修改原列表")
    original = [1, 2, 3, 4, 5]
    # 错误做法示例（不要这样做）
    print("   避免在推导式中修改被迭代的列表")
    
    # 陷阱2: 副作用
    print("\n2. 避免副作用")
    print("   推导式应该是纯函数式的，不产生副作用")
    
    # 陷阱3: 内存使用
    print("\n3. 注意内存使用")
    print("   大数据集考虑使用生成器表达式而不是列表推导式")
    
    # 生成器表达式示例
    big_data_gen = (x**2 for x in range(1000000))  # 生成器，延迟计算
    print(f"   生成器对象: {big_data_gen}")
    print(f"   前5个值: {[next(big_data_gen) for _ in range(5)]}")
    
    # 陷阱4: 变量作用域
    print("\n4. 理解变量作用域")
    # Python 3中推导式有自己的作用域
    x = "外部变量"
    result = [x for x in range(3)]  # 这里的x不会影响外部的x
    print(f"   外部变量x仍然是: '{x}'")
    print(f"   推导式结果: {result}")


def real_world_examples():
    """
    实际应用示例
    """
    print("\n=== 实际应用示例 ===")
    
    # 1. 文件处理
    print("1. 文件处理示例:")
    
    # 模拟文件名列表
    filenames = [
        "document1.txt", "image1.jpg", "script1.py", 
        "document2.pdf", "image2.png", "script2.js",
        "backup.zip", "config.json", "readme.md"
    ]
    
    # 按类型分类
    text_files = [f for f in filenames if f.endswith(('.txt', '.md', '.py', '.js'))]
    image_files = [f for f in filenames if f.endswith(('.jpg', '.png', '.gif'))]
    document_files = [f for f in filenames if f.endswith(('.pdf', '.doc', '.docx'))]
    
    print(f"   文本文件: {text_files}")
    print(f"   图片文件: {image_files}")
    print(f"   文档文件: {document_files}")
    
    # 2. 数据分析
    print("\n2. 数据分析示例:")
    
    # 模拟销售数据
    sales_data = [
        {"product": "iPhone", "price": 999, "quantity": 100},
        {"product": "iPad", "price": 599, "quantity": 150},
        {"product": "MacBook", "price": 1299, "quantity": 80},
        {"product": "AirPods", "price": 199, "quantity": 200},
    ]
    
    # 计算总收入
    revenues = [item["price"] * item["quantity"] for item in sales_data]
    total_revenue = sum(revenues)
    print(f"   各产品收入: {revenues}")
    print(f"   总收入: ${total_revenue:,}")
    
    # 高价值产品
    high_value_products = [item["product"] for item in sales_data if item["price"] > 500]
    print(f"   高价值产品: {high_value_products}")
    
    # 3. 字符串处理
    print("\n3. 字符串处理示例:")
    
    # 日志处理
    log_lines = [
        "2024-01-16 10:30:15 INFO User login successful",
        "2024-01-16 10:31:22 ERROR Database connection failed", 
        "2024-01-16 10:32:10 INFO Data processing completed",
        "2024-01-16 10:33:05 WARN Memory usage high",
        "2024-01-16 10:34:18 ERROR API request timeout"
    ]
    
    # 提取错误日志
    error_logs = [line for line in log_lines if "ERROR" in line]
    print(f"   错误日志: {len(error_logs)}条")
    for error in error_logs:
        print(f"     {error}")
    
    # 提取时间戳
    timestamps = [line.split()[1] for line in log_lines]
    print(f"   时间戳: {timestamps}")
    
    # 4. 配置处理
    print("\n4. 配置处理示例:")
    
    # 环境变量处理
    env_vars = {
        "DATABASE_URL": "postgresql://localhost:5432/mydb",
        "REDIS_URL": "redis://localhost:6379",
        "DEBUG": "true",
        "PORT": "8000",
        "SECRET_KEY": "your-secret-key"
    }
    
    # 提取URL配置
    url_configs = {key: value for key, value in env_vars.items() if key.endswith("_URL")}
    print(f"   URL配置: {url_configs}")
    
    # 布尔配置转换
    bool_configs = {key: value.lower() == "true" for key, value in env_vars.items() 
                   if value.lower() in ["true", "false"]}
    print(f"   布尔配置: {bool_configs}")


def main():
    """主函数：演示所有列表推导式功能"""
    print("Python列表推导式详解")
    print("=" * 50)
    
    try:
        basic_list_comprehensions()
        conditional_comprehensions()
        nested_comprehensions()
        advanced_comprehensions()
        performance_comparison()
        common_patterns()
        best_practices_and_pitfalls()
        real_world_examples()
        
        print("\n总结:")
        print("1. 列表推导式是Python的强大特性")
        print("2. 相比传统循环更简洁、性能更好")
        print("3. 适合数据转换和过滤操作")
        print("4. 保持简洁性和可读性很重要")
        print("5. 大数据集考虑使用生成器表达式")
        
        print("\nJava开发者学习建议:")
        print("1. 将Stream API的思维转换到推导式")
        print("2. 理解Python的duck typing特性")
        print("3. 掌握条件表达式的使用")
        print("4. 练习嵌套推导式的读写")
        print("5. 了解生成器表达式的内存优势")
        
    except Exception as e:
        print(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 