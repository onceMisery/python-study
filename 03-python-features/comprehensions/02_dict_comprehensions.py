#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python字典推导式详解
Dictionary Comprehensions in Python

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习Python字典推导式的语法、应用场景和与Java Map操作的对比

学习目标:
1. 掌握字典推导式的基本语法
2. 理解字典推导式的应用场景
3. 学会复杂的字典数据处理
4. 对比Java Map操作的实现方式
"""

import time
import random
from typing import Dict, List, Any
from collections import defaultdict, Counter


def demo_basic_syntax():
    """演示字典推导式的基本语法"""
    print("=== 1. 基本语法演示 ===")
    
    # 基础语法: {key_expression: value_expression for item in iterable}
    numbers = [1, 2, 3, 4, 5]
    
    # Python字典推导式 - 数字和其平方
    squares_dict = {x: x**2 for x in numbers}
    print(f"数字平方字典: {squares_dict}")
    
    # 等价的传统for循环写法
    squares_traditional = {}
    for x in numbers:
        squares_traditional[x] = x**2
    print(f"传统方式: {squares_traditional}")
    
    # 字符串键的示例
    fruits = ["apple", "banana", "cherry"]
    fruit_lengths = {fruit: len(fruit) for fruit in fruits}
    print(f"水果长度字典: {fruit_lengths}")
    
    """
    Java等价实现:
    List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
    Map<Integer, Integer> squaresMap = numbers.stream()
                                             .collect(Collectors.toMap(
                                                 Function.identity(),
                                                 x -> x * x
                                             ));
    
    List<String> fruits = Arrays.asList("apple", "banana", "cherry");
    Map<String, Integer> fruitLengths = fruits.stream()
                                             .collect(Collectors.toMap(
                                                 Function.identity(),
                                                 String::length
                                             ));
    """
    
    print()


def demo_conditional_dict_comprehensions():
    """演示条件字典推导式"""
    print("=== 2. 条件字典推导式 ===")
    
    numbers = range(1, 11)
    
    # 带条件的字典推导式 - 只包含偶数
    even_squares = {x: x**2 for x in numbers if x % 2 == 0}
    print(f"偶数平方字典: {even_squares}")
    
    # 条件值表达式 - 根据条件设置不同的值
    number_types = {x: "偶数" if x % 2 == 0 else "奇数" for x in numbers}
    print(f"数字类型: {number_types}")
    
    # 复杂条件 - 质数判断
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    prime_status = {x: "质数" if is_prime(x) else "合数" for x in range(2, 21)}
    print(f"质数状态: {prime_status}")
    
    """
    Java等价实现:
    Map<Integer, Integer> evenSquares = IntStream.rangeClosed(1, 10)
                                                .filter(x -> x % 2 == 0)
                                                .boxed()
                                                .collect(Collectors.toMap(
                                                    Function.identity(),
                                                    x -> x * x
                                                ));
    
    Map<Integer, String> numberTypes = IntStream.rangeClosed(1, 10)
                                               .boxed()
                                               .collect(Collectors.toMap(
                                                   Function.identity(),
                                                   x -> x % 2 == 0 ? "偶数" : "奇数"
                                               ));
    """
    
    print()


def demo_data_transformation():
    """演示数据转换应用"""
    print("=== 3. 数据转换应用 ===")
    
    # 列表到字典的转换
    students = ["Alice", "Bob", "Charlie", "Diana"]
    scores = [85, 92, 78, 96]
    
    # 使用zip创建字典
    student_scores = {name: score for name, score in zip(students, scores)}
    print(f"学生成绩: {student_scores}")
    
    # 字典的逆转（值变键，键变值）
    score_to_student = {score: name for name, score in student_scores.items()}
    print(f"成绩对应学生: {score_to_student}")
    
    # 字典过滤 - 高分学生
    high_scorers = {name: score for name, score in student_scores.items() if score >= 90}
    print(f"高分学生: {high_scorers}")
    
    # 字典值转换 - 成绩等级
    def get_grade(score):
        if score >= 90: return "A"
        elif score >= 80: return "B" 
        elif score >= 70: return "C"
        else: return "D"
    
    student_grades = {name: get_grade(score) for name, score in student_scores.items()}
    print(f"学生等级: {student_grades}")
    
    """
    Java等价实现:
    List<String> students = Arrays.asList("Alice", "Bob", "Charlie", "Diana");
    List<Integer> scores = Arrays.asList(85, 92, 78, 96);
    
    Map<String, Integer> studentScores = IntStream.range(0, students.size())
                                                 .boxed()
                                                 .collect(Collectors.toMap(
                                                     i -> students.get(i),
                                                     i -> scores.get(i)
                                                 ));
    
    Map<String, Integer> highScorers = studentScores.entrySet().stream()
                                                   .filter(entry -> entry.getValue() >= 90)
                                                   .collect(Collectors.toMap(
                                                       Map.Entry::getKey,
                                                       Map.Entry::getValue
                                                   ));
    """
    
    print()


def demo_nested_data_processing():
    """演示嵌套数据处理"""
    print("=== 4. 嵌套数据处理 ===")
    
    # 二维数据处理
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    # 创建坐标到值的映射
    coordinate_map = {(i, j): matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix[0]))}
    print(f"坐标映射: {coordinate_map}")
    
    # 行索引到行和的映射
    row_sums = {i: sum(row) for i, row in enumerate(matrix)}
    print(f"行和: {row_sums}")
    
    # 列索引到列和的映射
    col_sums = {j: sum(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0]))}
    print(f"列和: {col_sums}")
    
    # 嵌套字典结构
    sales_data = [
        {"region": "北京", "product": "iPhone", "sales": 100},
        {"region": "北京", "product": "iPad", "sales": 80},
        {"region": "上海", "product": "iPhone", "sales": 120},
        {"region": "上海", "product": "iPad", "sales": 90},
        {"region": "广州", "product": "iPhone", "sales": 110},
    ]
    
    # 按地区分组销售数据
    region_sales = {}
    for item in sales_data:
        region = item["region"]
        if region not in region_sales:
            region_sales[region] = {}
        region_sales[region][item["product"]] = item["sales"]
    
    print(f"地区销售数据: {region_sales}")
    
    # 使用字典推导式计算总销售额
    region_totals = {region: sum(products.values()) for region, products in region_sales.items()}
    print(f"地区总销售额: {region_totals}")
    
    """
    Java等价实现:
    Map<String, Map<String, Integer>> regionSales = salesData.stream()
        .collect(Collectors.groupingBy(
            item -> item.get("region"),
            Collectors.toMap(
                item -> item.get("product"),
                item -> item.get("sales")
            )
        ));
    
    Map<String, Integer> regionTotals = regionSales.entrySet().stream()
        .collect(Collectors.toMap(
            Map.Entry::getKey,
            entry -> entry.getValue().values().stream()
                          .mapToInt(Integer::intValue)
                          .sum()
        ));
    """
    
    print()


def demo_string_processing():
    """演示字符串处理应用"""
    print("=== 5. 字符串处理应用 ===")
    
    # 字符频率统计
    text = "Hello World Python Programming"
    char_count = {char: text.count(char) for char in set(text.lower()) if char.isalpha()}
    print(f"字符频率: {sorted(char_count.items())}")
    
    # 单词长度统计
    words = text.split()
    word_lengths = {word.lower(): len(word) for word in words}
    print(f"单词长度: {word_lengths}")
    
    # 首字母分组
    word_groups = {}
    for word in words:
        first_letter = word[0].upper()
        if first_letter not in word_groups:
            word_groups[first_letter] = []
        word_groups[first_letter].append(word.lower())
    
    print(f"首字母分组: {word_groups}")
    
    # 使用字典推导式重写首字母分组
    from collections import defaultdict
    grouped_words = defaultdict(list)
    for word in words:
        grouped_words[word[0].upper()].append(word.lower())
    
    # 转换为普通字典
    word_groups_comp = {letter: word_list for letter, word_list in grouped_words.items()}
    print(f"推导式分组: {word_groups_comp}")
    
    # URL参数解析示例
    url_params = "name=Alice&age=25&city=Beijing&hobby=coding"
    params_dict = {pair.split('=')[0]: pair.split('=')[1] for pair in url_params.split('&')}
    print(f"URL参数: {params_dict}")
    
    """
    Java等价实现:
    String text = "Hello World Python Programming";
    Map<Character, Long> charCount = text.toLowerCase().chars()
        .filter(Character::isLetter)
        .mapToObj(c -> (char) c)
        .collect(Collectors.groupingBy(
            Function.identity(),
            Collectors.counting()
        ));
    
    Map<String, Integer> wordLengths = Arrays.stream(text.split(" "))
        .collect(Collectors.toMap(
            word -> word.toLowerCase(),
            String::length,
            (existing, replacement) -> existing
        ));
    """
    
    print()


def demo_advanced_patterns():
    """演示高级应用模式"""
    print("=== 6. 高级应用模式 ===")
    
    # 配置文件处理
    config_lines = [
        "database_host=localhost",
        "database_port=5432",
        "redis_host=127.0.0.1",
        "redis_port=6379",
        "debug=true",
        "max_connections=100"
    ]
    
    # 解析配置
    config = {line.split('=')[0]: line.split('=')[1] for line in config_lines}
    print(f"配置字典: {config}")
    
    # 类型转换配置
    def convert_value(value):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.isdigit():
            return int(value)
        else:
            return value
    
    typed_config = {key: convert_value(value) for key, value in config.items()}
    print(f"类型转换后: {typed_config}")
    
    # 数据聚合 - 按条件分组
    products = [
        {"name": "iPhone 13", "category": "手机", "price": 6999},
        {"name": "iPhone 14", "category": "手机", "price": 7999},
        {"name": "iPad Air", "category": "平板", "price": 4599},
        {"name": "iPad Pro", "category": "平板", "price": 8599},
        {"name": "MacBook Air", "category": "笔记本", "price": 9999},
        {"name": "MacBook Pro", "category": "笔记本", "price": 14999},
    ]
    
    # 按类别统计平均价格
    category_prices = {}
    for product in products:
        category = product["category"]
        if category not in category_prices:
            category_prices[category] = []
        category_prices[category].append(product["price"])
    
    category_avg_price = {category: sum(prices) / len(prices) 
                         for category, prices in category_prices.items()}
    print(f"类别平均价格: {category_avg_price}")
    
    # 价格区间分析
    price_ranges = {
        "低价": [p["name"] for p in products if p["price"] < 5000],
        "中价": [p["name"] for p in products if 5000 <= p["price"] < 10000],
        "高价": [p["name"] for p in products if p["price"] >= 10000]
    }
    print(f"价格区间分析: {price_ranges}")
    
    # 多维数据索引
    students_data = [
        {"name": "Alice", "grade": 10, "subject": "数学", "score": 95},
        {"name": "Alice", "grade": 10, "subject": "英语", "score": 87},
        {"name": "Bob", "grade": 10, "subject": "数学", "score": 92},
        {"name": "Bob", "grade": 10, "subject": "英语", "score": 89},
    ]
    
    # 创建学生-科目成绩索引
    score_index = {(item["name"], item["subject"]): item["score"] for item in students_data}
    print(f"成绩索引: {score_index}")
    print(f"Alice的数学成绩: {score_index[('Alice', '数学')]}")
    
    """
    Java等价实现:
    Map<String, List<Integer>> categoryPrices = products.stream()
        .collect(Collectors.groupingBy(
            product -> product.get("category"),
            Collectors.mapping(
                product -> product.get("price"),
                Collectors.toList()
            )
        ));
    
    Map<String, Double> categoryAvgPrice = categoryPrices.entrySet().stream()
        .collect(Collectors.toMap(
            Map.Entry::getKey,
            entry -> entry.getValue().stream()
                          .mapToInt(Integer::intValue)
                          .average()
                          .orElse(0.0)
        ));
    """
    
    print()


def demo_performance_comparison():
    """演示性能对比"""
    print("=== 7. 性能对比 ===")
    
    # 准备测试数据
    data = list(range(100000))
    
    def test_dict_comprehension():
        return {x: x**2 for x in data}
    
    def test_traditional_loop():
        result = {}
        for x in data:
            result[x] = x**2
        return result
    
    def test_dict_constructor():
        return dict((x, x**2) for x in data)
    
    # 性能测试函数
    def measure_time(func, description):
        start_time = time.time()
        result = func()
        end_time = time.time()
        print(f"{description}: {end_time - start_time:.4f}秒, 字典大小: {len(result)}")
        return end_time - start_time
    
    print("处理100,000个元素创建字典:")
    time1 = measure_time(test_dict_comprehension, "字典推导式")
    time2 = measure_time(test_traditional_loop, "传统for循环")
    time3 = measure_time(test_dict_constructor, "dict()构造器")
    
    # 性能分析
    fastest = min(time1, time2, time3)
    print(f"\n性能分析:")
    print(f"字典推导式相对最快: {time1/fastest:.2f}x")
    print(f"传统循环相对最快: {time2/fastest:.2f}x")
    print(f"dict构造器相对最快: {time3/fastest:.2f}x")
    
    print()


def demo_common_pitfalls():
    """演示常见陷阱和最佳实践"""
    print("=== 8. 常见陷阱和最佳实践 ===")
    
    # 陷阱1: 重复键问题
    print("陷阱1: 重复键处理")
    words = ["apple", "banana", "apple", "cherry", "banana"]
    
    # 这会丢失重复的键值
    word_dict_bad = {word: len(word) for word in words}
    print(f"重复键被覆盖: {word_dict_bad}")
    
    # 正确处理重复键 - 计数
    from collections import Counter
    word_count = Counter(words)
    word_count_dict = {word: count for word, count in word_count.items()}
    print(f"正确的计数: {word_count_dict}")
    
    # 陷阱2: 键的可哈希性
    print("\n陷阱2: 键必须是可哈希的")
    
    # 正确: 使用不可变类型作为键
    good_keys = {(1, 2): "点1", (3, 4): "点2"}
    print(f"元组键: {good_keys}")
    
    # 错误示例（注释掉避免错误）
    # bad_keys = {[1, 2]: "点1"}  # TypeError: unhashable type: 'list'
    print("列表不能作为字典键（会报错）")
    
    # 陷阱3: 内存使用考虑
    print("\n陷阱3: 大数据集内存考虑")
    
    # 对于大数据集，考虑按需生成
    large_range = range(1000000)
    
    # 字典推导式 - 立即创建所有键值对
    # large_dict = {x: x**2 for x in large_range}  # 占用大量内存
    
    # 生成器字典（实际是生成器表达式）
    large_dict_gen = ((x, x**2) for x in large_range)
    print(f"字典生成器: {large_dict_gen}")
    print(f"第一个键值对: {next(large_dict_gen)}")
    
    # 最佳实践总结
    print("\n最佳实践:")
    print("1. 注意重复键的处理")
    print("2. 确保键是可哈希的")
    print("3. 大数据集考虑内存使用")
    print("4. 保持推导式简洁易读")
    print("5. 复杂逻辑考虑分步处理")
    
    print()


def demo_real_world_examples():
    """演示实际应用示例"""
    print("=== 9. 实际应用示例 ===")
    
    # 示例1: API响应数据处理
    print("示例1: API响应数据处理")
    
    api_response = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com", "active": True},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "active": False},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com", "active": True},
        ]
    }
    
    # 创建ID到用户的映射
    user_by_id = {user["id"]: user for user in api_response["users"]}
    print(f"用户ID映射: {user_by_id}")
    
    # 活跃用户邮箱列表
    active_emails = {user["name"]: user["email"] for user in api_response["users"] if user["active"]}
    print(f"活跃用户邮箱: {active_emails}")
    
    # 示例2: 数据库查询结果处理
    print("\n示例2: 数据库查询结果处理")
    
    # 模拟数据库查询结果
    query_results = [
        (1, "订单A", "2024-01-15", 1500.00),
        (2, "订单B", "2024-01-16", 2300.50),
        (3, "订单C", "2024-01-16", 890.00),
        (4, "订单D", "2024-01-17", 3200.00),
    ]
    
    # 转换为字典格式
    orders = {row[0]: {
        "name": row[1],
        "date": row[2], 
        "amount": row[3]
    } for row in query_results}
    print(f"订单字典: {orders}")
    
    # 按日期分组订单金额
    daily_totals = {}
    for order in orders.values():
        date = order["date"]
        amount = order["amount"]
        daily_totals[date] = daily_totals.get(date, 0) + amount
    
    print(f"每日订单总额: {daily_totals}")
    
    # 示例3: 配置管理
    print("\n示例3: 配置管理")
    
    # 环境变量配置
    env_config = {
        "DATABASE_URL": "postgresql://localhost:5432/mydb",
        "REDIS_URL": "redis://localhost:6379/0",
        "SECRET_KEY": "your-secret-key-here",
        "DEBUG": "true",
        "PORT": "8000",
        "WORKERS": "4"
    }
    
    # 按前缀分组配置
    config_groups = {}
    for key, value in env_config.items():
        if "_" in key:
            prefix = key.split("_")[0]
            if prefix not in config_groups:
                config_groups[prefix] = {}
            config_groups[prefix][key] = value
        else:
            if "GENERAL" not in config_groups:
                config_groups["GENERAL"] = {}
            config_groups["GENERAL"][key] = value
    
    print(f"配置分组: {config_groups}")
    
    # 类型转换配置
    def parse_config_value(value):
        if value.lower() in ['true', 'false']:
            return value.lower() == 'true'
        elif value.isdigit():
            return int(value)
        elif value.replace('.', '').isdigit():
            return float(value)
        return value
    
    parsed_config = {key: parse_config_value(value) for key, value in env_config.items()}
    print(f"解析后配置: {parsed_config}")
    
    """
    Java等价实现参考:
    
    // API响应处理
    Map<Integer, User> userById = apiResponse.getUsers().stream()
        .collect(Collectors.toMap(User::getId, Function.identity()));
    
    Map<String, String> activeEmails = apiResponse.getUsers().stream()
        .filter(User::isActive)
        .collect(Collectors.toMap(User::getName, User::getEmail));
    
    // 配置分组
    Map<String, Map<String, String>> configGroups = envConfig.entrySet().stream()
        .collect(Collectors.groupingBy(
            entry -> entry.getKey().contains("_") ? 
                     entry.getKey().split("_")[0] : "GENERAL",
            Collectors.toMap(
                Map.Entry::getKey,
                Map.Entry::getValue
            )
        ));
    """
    
    print()


def main():
    """主函数：运行所有演示"""
    print("Python字典推导式完整学习指南")
    print("=" * 50)
    
    demo_basic_syntax()
    demo_conditional_dict_comprehensions()
    demo_data_transformation()
    demo_nested_data_processing()
    demo_string_processing()
    demo_advanced_patterns()
    demo_performance_comparison()
    demo_common_pitfalls()
    demo_real_world_examples()
    
    print("学习总结:")
    print("1. 字典推导式提供了创建字典的简洁语法")
    print("2. 适合键值对的转换、过滤和聚合操作")
    print("3. 性能通常优于传统循环方式")
    print("4. 注意键的唯一性和可哈希性")
    print("5. Java的Stream API + Collectors提供类似功能")
    print("6. 复杂逻辑建议分步处理以保持可读性")


if __name__ == "__main__":
    main() 