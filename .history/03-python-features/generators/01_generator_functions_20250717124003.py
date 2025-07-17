#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成器函数详解 - Generator Functions

本文件详细介绍Python生成器函数的语法和应用，
包括与Java Iterator的对比分析。

生成器函数是Python实现迭代器模式的优雅方式，
通过yield关键字实现惰性求值和内存高效的序列处理。

Author: Python学习项目
Date: 2024-01-16
"""

import sys
import time
import random
from typing import Generator, Iterator, Iterable
from collections.abc import Iterator as AbcIterator


def main():
    """生成器函数示例主函数"""
    print("=== Python生成器函数详解 ===\n")
    
    # 1. 基础生成器函数
    basic_generator_functions()
    
    # 2. yield关键字详解
    yield_keyword_details()
    
    # 3. 生成器状态和协议
    generator_state_and_protocol()
    
    # 4. 与Java Iterator对比
    java_iterator_comparison()
    
    # 5. 高级生成器特性
    advanced_generator_features()
    
    # 6. 生成器协作
    generator_cooperation()
    
    # 7. 实际应用示例
    practical_examples()
    
    # 8. 性能优化
    performance_optimization()
    
    # 9. 常见陷阱
    common_pitfalls()
    
    # 10. 最佳实践
    best_practices()


def basic_generator_functions():
    """基础生成器函数"""
    print("1. 基础生成器函数")
    print("-" * 40)
    
    # 示例1：简单生成器
    def simple_generator():
        """最简单的生成器"""
        print("  生成器开始")
        yield 1
        print("  生成第二个值")
        yield 2
        print("  生成第三个值")
        yield 3
        print("  生成器结束")
    
    print("简单生成器示例:")
    gen = simple_generator()
    print(f"  生成器对象: {gen}")
    print(f"  类型: {type(gen)}")
    
    print("  遍历生成器:")
    for value in gen:
        print(f"    收到值: {value}")
    
    # 示例2：数字序列生成器
    def number_sequence(start, end, step=1):
        """生成数字序列"""
        current = start
        while current < end:
            yield current
            current += step
    
    print(f"\n数字序列生成器:")
    numbers = number_sequence(1, 10, 2)
    print(f"  序列: {list(numbers)}")
    
    # 示例3：斐波那契数列生成器
    def fibonacci_generator(n):
        """生成前n个斐波那契数"""
        a, b = 0, 1
        count = 0
        while count < n:
            yield a
            a, b = b, a + b
            count += 1
    
    print(f"\n斐波那契数列生成器:")
    fib = fibonacci_generator(10)
    print(f"  前10个斐波那契数: {list(fib)}")
    
    # 示例4：无限生成器
    def infinite_counter(start=0):
        """无限计数器"""
        current = start
        while True:
            yield current
            current += 1
    
    print(f"\n无限生成器示例:")
    counter = infinite_counter(100)
    print("  前5个值:", end=" ")
    for i, value in enumerate(counter):
        if i >= 5:
            break
        print(value, end=" ")
    print()
    
    # 示例5：条件生成器
    def even_numbers(max_value):
        """生成偶数"""
        for i in range(0, max_value + 1, 2):
            yield i
    
    print(f"\n条件生成器:")
    evens = even_numbers(20)
    print(f"  0-20的偶数: {list(evens)}")
    
    print()


def yield_keyword_details():
    """yield关键字详解"""
    print("2. yield关键字详解")
    print("-" * 40)
    
    # yield的基本行为
    print("yield的基本行为:")
    
    def yield_demo():
        """演示yield的行为"""
        print("    函数开始执行")
        result1 = yield "第一个值"
        print(f"    yield返回了: {result1}")
        
        result2 = yield "第二个值"  
        print(f"    yield返回了: {result2}")
        
        return "函数结束"
    
    gen = yield_demo()
    print(f"  创建生成器: {gen}")
    
    # 使用next()逐步执行
    print(f"  第一次next(): {next(gen)}")
    print(f"  第二次next(): {next(gen)}")
    
    try:
        print(f"  第三次next(): {next(gen)}")
    except StopIteration as e:
        print(f"  StopIteration异常，返回值: {e.value}")
    
    # yield表达式
    print(f"\nyield表达式:")
    
    def accumulator():
        """累加器生成器"""
        total = 0
        while True:
            value = yield total
            if value is not None:
                total += value
    
    acc = accumulator()
    next(acc)  # 启动生成器
    
    print(f"  初始值: {acc.send(10)}")
    print(f"  加5: {acc.send(5)}")
    print(f"  加20: {acc.send(20)}")
    print(f"  当前总和: {acc.send(0)}")
    
    # yield from语法
    print(f"\nyield from语法:")
    
    def sub_generator():
        """子生成器"""
        yield 1
        yield 2
        yield 3
    
    def main_generator():
        """主生成器"""
        yield "开始"
        yield from sub_generator()  # 委托给子生成器
        yield "结束"
    
    gen = main_generator()
    print(f"  yield from结果: {list(gen)}")
    
    # 等价的手动实现
    def manual_delegation():
        """手动委托实现"""
        yield "开始"
        for value in sub_generator():
            yield value
        yield "结束"
    
    gen2 = manual_delegation()
    print(f"  手动委托结果: {list(gen2)}")
    
    # yield的返回值处理
    print(f"\nyield的返回值处理:")
    
    def generator_with_return():
        """带返回值的生成器"""
        yield 1
        yield 2
        return "完成"  # 生成器的返回值
    
    def delegating_generator():
        """委托生成器"""
        result = yield from generator_with_return()
        yield f"收到返回值: {result}"
    
    gen = delegating_generator()
    print(f"  委托结果: {list(gen)}")
    
    print()


def generator_state_and_protocol():
    """生成器状态和协议"""
    print("3. 生成器状态和协议")
    print("-" * 40)
    
    # 生成器状态
    print("生成器状态:")
    
    def stateful_generator():
        """有状态的生成器"""
        print("    GEN_CREATED: 生成器已创建")
        try:
            value = yield "第一个值"
            print("    GEN_RUNNING: 生成器运行中")
            yield f"收到: {value}"
        except GeneratorExit:
            print("    GEN_CLOSED: 生成器被关闭")
        finally:
            print("    GEN_SUSPENDED: 生成器挂起")
    
    gen = stateful_generator()
    print(f"  状态: {gen.gi_frame}")  # None表示未启动
    
    print(f"  第一次next: {next(gen)}")
    print(f"  状态: {gen.gi_frame is not None}")  # 有frame表示挂起
    
    print(f"  send值: {gen.send('测试数据')}")
    
    gen.close()  # 关闭生成器
    print("  生成器已关闭")
    
    # 生成器方法
    print(f"\n生成器方法:")
    
    def interactive_generator():
        """交互式生成器"""
        try:
            while True:
                try:
                    value = yield "等待输入"
                    if value == "error":
                        raise ValueError("模拟错误")
                    yield f"处理: {value}"
                except ValueError as e:
                    yield f"错误处理: {e}"
        except GeneratorExit:
            yield "清理资源"
    
    gen = interactive_generator()
    print(f"  启动: {next(gen)}")
    print(f"  send: {gen.send('正常数据')}")
    print(f"  next: {next(gen)}")
    
    # 使用throw发送异常
    try:
        result = gen.throw(ValueError, "外部异常")
        print(f"  throw: {result}")
    except StopIteration:
        pass
    
    # 生成器协议实现
    print(f"\n生成器协议实现:")
    
    class CustomIterator:
        """自定义迭代器类"""
        
        def __init__(self, max_value):
            self.max_value = max_value
            self.current = 0
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.current >= self.max_value:
                raise StopIteration
            self.current += 1
            return self.current ** 2
    
    def generator_equivalent(max_value):
        """等价的生成器实现"""
        for i in range(1, max_value + 1):
            yield i ** 2
    
    # 比较两种实现
    print("  自定义迭代器:", list(CustomIterator(5)))
    print("  生成器函数:", list(generator_equivalent(5)))
    print("  代码行数对比: 类(15行) vs 生成器(3行)")
    
    print()


def java_iterator_comparison():
    """与Java Iterator对比"""
    print("4. 与Java Iterator对比")
    print("-" * 40)
    
    # Python生成器示例
    def python_generator(data):
        """Python生成器"""
        for item in data:
            if item % 2 == 0:
                yield item * 2
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    gen = python_generator(data)
    
    print("Python生成器:")
    print(f"  def python_generator(data):")
    print(f"      for item in data:")
    print(f"          if item % 2 == 0:")
    print(f"              yield item * 2")
    print(f"")
    print(f"  结果: {list(gen)}")
    
    print("\nJava等价代码:")
    print("""
    // Java 8+ Iterator实现
    public class EvenDoubleIterator implements Iterator<Integer> {
        private List<Integer> data;
        private int index = 0;
        private Integer nextValue = null;
        
        public EvenDoubleIterator(List<Integer> data) {
            this.data = data;
            findNext();
        }
        
        private void findNext() {
            while (index < data.size()) {
                int current = data.get(index++);
                if (current % 2 == 0) {
                    nextValue = current * 2;
                    return;
                }
            }
            nextValue = null;
        }
        
        @Override
        public boolean hasNext() {
            return nextValue != null;
        }
        
        @Override
        public Integer next() {
            if (!hasNext()) {
                throw new NoSuchElementException();
            }
            Integer result = nextValue;
            findNext();
            return result;
        }
    }
    
    // 使用
    List<Integer> data = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
    Iterator<Integer> iter = new EvenDoubleIterator(data);
    List<Integer> result = new ArrayList<>();
    while (iter.hasNext()) {
        result.add(iter.next());
    }
    """)
    
    # 使用Stream API的简化版本
    print("\nJava Stream API等价:")
    print("""
    // Java 8+ Stream API
    List<Integer> data = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
    List<Integer> result = data.stream()
        .filter(item -> item % 2 == 0)
        .map(item -> item * 2)
        .collect(Collectors.toList());
    """)
    
    # 特性对比
    print(f"\n特性对比:")
    
    features = [
        ("代码简洁性", "Python: 3行", "Java Iterator: 30+行", "Java Stream: 4行"),
        ("内存效率", "惰性求值", "手动状态管理", "惰性求值"),
        ("错误处理", "异常自然传播", "手动异常处理", "异常自然传播"),
        ("可读性", "非常直观", "状态复杂", "相对直观"),
        ("性能", "解释器开销", "编译优化", "JVM优化"),
        ("调试", "容易调试", "状态调试复杂", "流式调试"),
    ]
    
    for feature, python_val, java_iter, java_stream in features:
        print(f"  {feature}:")
        print(f"    Python生成器: {python_val}")
        print(f"    Java Iterator: {java_iter}")
        print(f"    Java Stream: {java_stream}")
    
    # 使用场景对比
    print(f"\n使用场景对比:")
    
    scenarios = [
        "大数据处理 - Python生成器内存友好",
        "复杂状态管理 - Java Iterator控制精确",
        "函数式编程 - Java Stream功能丰富",
        "快速原型 - Python生成器开发速度快",
        "性能敏感 - Java Iterator编译优化好",
        "团队协作 - 取决于团队技能栈"
    ]
    
    for scenario in scenarios:
        print(f"  • {scenario}")
    
    print()


def advanced_generator_features():
    """高级生成器特性"""
    print("5. 高级生成器特性")
    print("-" * 40)
    
    # 双向通信
    print("双向通信:")
    
    def coroutine_demo():
        """协程演示"""
        print("    协程启动")
        total = 0
        count = 0
        
        try:
            while True:
                value = yield f"当前平均值: {total/count if count > 0 else 0}"
                if value is not None:
                    total += value
                    count += 1
                    print(f"    收到值: {value}, 总计: {total}")
        except GeneratorExit:
            print(f"    协程结束，最终平均值: {total/count if count > 0 else 0}")
    
    coro = coroutine_demo()
    next(coro)  # 启动协程
    
    print(f"  发送10: {coro.send(10)}")
    print(f"  发送20: {coro.send(20)}")
    print(f"  发送30: {coro.send(30)}")
    coro.close()
    
    # 生成器管道
    print(f"\n生成器管道:")
    
    def numbers(max_num):
        """数字源"""
        for i in range(1, max_num + 1):
            print(f"    生成: {i}")
            yield i
    
    def filter_even(source):
        """过滤偶数"""
        for num in source:
            if num % 2 == 0:
                print(f"    过滤: {num}")
                yield num
    
    def multiply_by_2(source):
        """乘以2"""
        for num in source:
            result = num * 2
            print(f"    乘2: {num} -> {result}")
            yield result
    
    # 构建管道
    print("  构建管道: 数字 -> 过滤偶数 -> 乘以2")
    pipeline = multiply_by_2(filter_even(numbers(10)))
    
    # 只取前3个结果
    results = []
    for i, value in enumerate(pipeline):
        results.append(value)
        if i >= 2:
            break
    
    print(f"  管道结果: {results}")
    
    # 生成器表达式vs生成器函数
    print(f"\n生成器表达式vs生成器函数:")
    
    # 简单情况用生成器表达式
    simple_squares = (x**2 for x in range(10) if x % 2 == 0)
    print(f"  生成器表达式: {list(simple_squares)}")
    
    # 复杂情况用生成器函数
    def complex_generator(n):
        """复杂生成器函数"""
        for i in range(n):
            if i % 2 == 0:
                # 复杂计算
                result = i ** 2
                if result > 10:
                    yield result
                else:
                    yield result * 2
    
    complex_gen = complex_generator(10)
    print(f"  生成器函数: {list(complex_gen)}")
    
    # 递归生成器
    print(f"\n递归生成器:")
    
    def tree_traverse(node):
        """递归遍历树结构"""
        yield node['value']
        for child in node.get('children', []):
            yield from tree_traverse(child)
    
    # 树结构
    tree = {
        'value': 'root',
        'children': [
            {
                'value': 'child1',
                'children': [
                    {'value': 'grandchild1'},
                    {'value': 'grandchild2'}
                ]
            },
            {
                'value': 'child2',
                'children': [
                    {'value': 'grandchild3'}
                ]
            }
        ]
    }
    
    print(f"  树遍历: {list(tree_traverse(tree))}")
    
    print()


def generator_cooperation():
    """生成器协作"""
    print("6. 生成器协作")
    print("-" * 40)
    
    # 生产者-消费者模式
    print("生产者-消费者模式:")
    
    def producer(queue_size=5):
        """生产者"""
        queue = []
        item_id = 1
        
        while True:
            # 生产物品
            if len(queue) < queue_size:
                item = f"item_{item_id}"
                queue.append(item)
                print(f"    生产: {item}")
                item_id += 1
            
            # 发送队列状态
            consumed_item = yield queue[:]
            
            # 处理消费
            if consumed_item and queue:
                removed = queue.pop(0)
                print(f"    消费: {removed}")
    
    def consumer(producer_gen):
        """消费者"""
        queue = next(producer_gen)  # 启动生产者
        
        while queue or len(queue) > 0:
            if queue:
                # 消费一个物品
                item_to_consume = queue[0]
                queue = producer_gen.send(item_to_consume)
                yield f"消费了: {item_to_consume}"
            else:
                queue = producer_gen.send(None)
                yield "等待生产"
    
    prod = producer()
    cons = consumer(prod)
    
    print("  生产者-消费者协作:")
    for i, status in enumerate(cons):
        print(f"    {status}")
        if i >= 7:  # 限制输出
            break
    
    # 协程链
    print(f"\n协程链:")
    
    def input_processor():
        """输入处理器"""
        while True:
            data = yield
            if data:
                processed = data.upper()
                print(f"    输入处理: {data} -> {processed}")
                yield processed
    
    def filter_processor():
        """过滤处理器"""
        while True:
            data = yield
            if data and len(data) > 3:
                filtered = f"[FILTERED]{data}"
                print(f"    过滤处理: {data} -> {filtered}")
                yield filtered
    
    def output_processor():
        """输出处理器"""
        while True:
            data = yield
            if data:
                output = f"OUTPUT: {data}"
                print(f"    输出处理: {output}")
                yield output
    
    # 手动协程链（简化版）
    input_proc = input_processor()
    filter_proc = filter_processor()
    output_proc = output_processor()
    
    # 启动协程
    next(input_proc)
    next(filter_proc)
    next(output_proc)
    
    print("  协程链处理:")
    
    test_data = ["hello", "hi", "python", "ok"]
    for data in test_data:
        step1 = input_proc.send(data)
        next(input_proc)  # 重置
        
        if step1:
            step2 = filter_proc.send(step1)
            next(filter_proc)  # 重置
            
            if step2:
                step3 = output_proc.send(step2)
                next(output_proc)  # 重置
    
    print()


def practical_examples():
    """实际应用示例"""
    print("7. 实际应用示例")
    print("-" * 40)
    
    # 示例1：文件逐行读取
    print("示例1：大文件逐行处理")
    
    def read_large_file(filename):
        """逐行读取大文件"""
        # 模拟文件内容
        file_content = [
            "第1行：用户登录 user123",
            "第2行：数据库查询 SELECT * FROM users",
            "第3行：ERROR 数据库连接失败",
            "第4行：用户注销 user123",
            "第5行：系统维护开始",
            "第6行：ERROR 磁盘空间不足",
            "第7行：系统维护结束"
        ]
        
        for line_num, line in enumerate(file_content, 1):
            # 模拟逐行处理
            yield (line_num, line)
    
    def process_log_file(filename):
        """处理日志文件"""
        error_count = 0
        for line_num, line in read_large_file(filename):
            if "ERROR" in line:
                error_count += 1
                yield f"错误 #{error_count} 在第{line_num}行: {line}"
    
    print("  日志文件错误分析:")
    for error in process_log_file("large_log.txt"):
        print(f"    {error}")
    
    # 示例2：数据分页
    print(f"\n示例2：数据分页处理")
    
    def paginated_data(total_items, page_size=10):
        """分页数据生成器"""
        for start in range(0, total_items, page_size):
            end = min(start + page_size, total_items)
            # 模拟数据库查询
            page_data = [f"item_{i}" for i in range(start, end)]
            yield {
                'page': start // page_size + 1,
                'data': page_data,
                'total': total_items,
                'has_next': end < total_items
            }
    
    print("  分页数据处理:")
    for page_info in paginated_data(25, 7):
        print(f"    页面{page_info['page']}: {len(page_info['data'])}项 "
              f"{'(有下页)' if page_info['has_next'] else '(最后页)'}")
        if page_info['page'] >= 3:  # 只显示前3页
            break
    
    # 示例3：实时数据流
    print(f"\n示例3：实时数据流处理")
    
    def sensor_data_stream():
        """模拟传感器数据流"""
        import random
        sensor_id = 1
        
        while True:
            # 模拟传感器数据
            temperature = random.uniform(20.0, 35.0)
            humidity = random.uniform(40.0, 80.0)
            timestamp = time.time()
            
            yield {
                'sensor_id': sensor_id,
                'temperature': round(temperature, 2),
                'humidity': round(humidity, 2),
                'timestamp': timestamp,
                'alert': temperature > 30 or humidity > 70
            }
            
            time.sleep(0.01)  # 模拟数据间隔
    
    def alert_processor(data_stream):
        """告警处理器"""
        alert_count = 0
        for data in data_stream:
            if data['alert']:
                alert_count += 1
                yield f"告警 #{alert_count}: 传感器{data['sensor_id']} - "
                     f"温度:{data['temperature']}°C, 湿度:{data['humidity']}%"
    
    print("  实时数据流告警:")
    stream = sensor_data_stream()
    alerts = alert_processor(stream)
    
    # 只处理前5个告警
    for i, alert in enumerate(alerts):
        print(f"    {alert}")
        if i >= 4:
            break
    
    # 示例4：任务队列
    print(f"\n示例4：任务队列处理")
    
    class TaskQueue:
        """任务队列生成器"""
        
        def __init__(self):
            self.tasks = []
            self.completed = []
        
        def add_task(self, task):
            """添加任务"""
            self.tasks.append(task)
        
        def process_tasks(self):
            """处理任务生成器"""
            while self.tasks:
                task = self.tasks.pop(0)
                print(f"    处理任务: {task}")
                
                # 模拟任务处理
                time.sleep(0.01)
                result = f"完成_{task}"
                self.completed.append(result)
                
                yield result
    
    # 使用任务队列
    queue = TaskQueue()
    
    # 添加任务
    for i in range(5):
        queue.add_task(f"task_{i}")
    
    print("  任务队列处理:")
    for result in queue.process_tasks():
        print(f"    结果: {result}")
    
    print()


def performance_optimization():
    """性能优化"""
    print("8. 性能优化")
    print("-" * 40)
    
    # 内存效率对比
    print("内存效率对比:")
    
    def memory_test_list(n):
        """列表方式"""
        return [x**2 for x in range(n)]
    
    def memory_test_generator(n):
        """生成器方式"""
        for x in range(n):
            yield x**2
    
    n = 10000
    
    # 测试列表内存使用
    list_result = memory_test_list(n)
    list_size = sys.getsizeof(list_result)
    
    # 测试生成器内存使用
    gen_result = memory_test_generator(n)
    gen_size = sys.getsizeof(gen_result)
    
    print(f"  数据量: {n:,} 个元素")
    print(f"  列表内存: {list_size:,} bytes")
    print(f"  生成器内存: {gen_size:,} bytes")
    print(f"  内存节省: {list_size / gen_size:.1f}倍")
    
    # 惰性求值优势
    print(f"\n惰性求值优势:")
    
    def expensive_computation(x):
        """昂贵的计算"""
        time.sleep(0.001)  # 模拟耗时
        return x ** 3
    
    def eager_processing(data):
        """立即处理"""
        return [expensive_computation(x) for x in data]
    
    def lazy_processing(data):
        """惰性处理"""
        for x in data:
            yield expensive_computation(x)
    
    data = range(100)
    
    # 测试立即处理
    start_time = time.time()
    eager_result = eager_processing(data)
    eager_time = time.time() - start_time
    
    # 测试惰性处理（只取前10个）
    start_time = time.time()
    lazy_gen = lazy_processing(data)
    lazy_result = []
    for i, value in enumerate(lazy_gen):
        lazy_result.append(value)
        if i >= 9:  # 只取前10个
            break
    lazy_time = time.time() - start_time
    
    print(f"  立即处理100个: {eager_time:.3f}秒")
    print(f"  惰性处理10个: {lazy_time:.3f}秒")
    print(f"  惰性处理优势: {eager_time / lazy_time:.1f}倍")
    
    # 生成器链式优化
    print(f"\n生成器链式优化:")
    
    def optimized_pipeline(data):
        """优化的管道"""
        # 将多个操作合并到一个生成器中
        for x in data:
            if x % 2 == 0:  # 筛选
                squared = x ** 2  # 转换
                if squared > 10:  # 二次筛选
                    yield squared * 2  # 最终转换
    
    def separate_pipeline(data):
        """分离的管道"""
        def filter_even(items):
            for x in items:
                if x % 2 == 0:
                    yield x
        
        def square(items):
            for x in items:
                yield x ** 2
        
        def filter_large(items):
            for x in items:
                if x > 10:
                    yield x
        
        def double(items):
            for x in items:
                yield x * 2
        
        return double(filter_large(square(filter_even(data))))
    
    test_data = range(20)
    
    # 测试优化版本
    start_time = time.time()
    opt_result = list(optimized_pipeline(test_data))
    opt_time = time.time() - start_time
    
    # 测试分离版本
    start_time = time.time()
    sep_result = list(separate_pipeline(test_data))
    sep_time = time.time() - start_time
    
    print(f"  优化管道: {opt_time:.6f}秒")
    print(f"  分离管道: {sep_time:.6f}秒")
    print(f"  结果一致: {opt_result == sep_result}")
    print(f"  性能提升: {sep_time / opt_time:.1f}倍")
    
    print()


def common_pitfalls():
    """常见陷阱"""
    print("9. 常见陷阱")
    print("-" * 40)
    
    # 陷阱1：生成器只能消费一次
    print("陷阱1：生成器只能消费一次")
    
    def one_time_generator():
        """一次性生成器"""
        for i in range(3):
            yield i
    
    gen = one_time_generator()
    print(f"  第一次消费: {list(gen)}")
    print(f"  第二次消费: {list(gen)}")  # 空列表
    
    # 解决方案：生成器工厂
    def generator_factory():
        """生成器工厂"""
        def generator():
            for i in range(3):
                yield i
        return generator
    
    gen_factory = generator_factory()
    print(f"  工厂第一次: {list(gen_factory())}")
    print(f"  工厂第二次: {list(gen_factory())}")
    
    # 陷阱2：生成器中的闭包问题
    print(f"\n陷阱2：闭包变量陷阱")
    
    # 错误示例
    generators = []
    for i in range(3):
        generators.append((x + i for x in range(3)))
    
    print("  错误的闭包:")
    for gen in generators:
        print(f"    {list(gen)}")  # 所有生成器都使用最后的i值
    
    # 正确示例
    def create_generator(offset):
        """创建带偏移的生成器"""
        return (x + offset for x in range(3))
    
    correct_generators = [create_generator(i) for i in range(3)]
    print("  正确的闭包:")
    for gen in correct_generators:
        print(f"    {list(gen)}")
    
    # 陷阱3：生成器中的异常处理
    print(f"\n陷阱3：异常处理陷阱")
    
    def problematic_generator():
        """有问题的生成器"""
        try:
            for i in range(5):
                if i == 3:
                    raise ValueError("测试异常")
                yield i
        except ValueError as e:
            print(f"    生成器内部捕获: {e}")
            yield "错误恢复"
    
    print("  异常处理:")
    try:
        for value in problematic_generator():
            print(f"    收到: {value}")
    except Exception as e:
        print(f"    外部捕获: {e}")
    
    # 陷阱4：生成器的过早终止
    print(f"\n陷阱4：生成器过早终止")
    
    def resource_generator():
        """资源管理生成器"""
        print("    获取资源")
        try:
            for i in range(5):
                yield f"资源_{i}"
        finally:
            print("    释放资源")
    
    print("  正常完成:")
    for item in resource_generator():
        print(f"    使用: {item}")
    
    print("  过早终止:")
    gen = resource_generator()
    print(f"    第一个: {next(gen)}")
    print(f"    第二个: {next(gen)}")
    # 生成器被垃圾回收，finally可能不会执行
    del gen
    
    print()


def best_practices():
    """最佳实践"""
    print("10. 最佳实践")
    print("-" * 40)
    
    # 实践1：合适的使用场景
    print("实践1：合适的使用场景")
    
    # 适合使用生成器的情况
    suitable_cases = [
        "处理大数据集（内存受限）",
        "实现无限序列",
        "流式数据处理",
        "需要惰性求值的计算",
        "实现状态机",
        "协程和异步编程",
        "数据管道处理"
    ]
    
    print("  适合使用生成器:")
    for case in suitable_cases:
        print(f"    • {case}")
    
    # 不适合使用生成器的情况
    unsuitable_cases = [
        "需要随机访问元素",
        "需要多次遍历同一数据",
        "需要len()操作",
        "简单的一次性列表操作",
        "性能要求极高的场景"
    ]
    
    print("  不适合使用生成器:")
    for case in unsuitable_cases:
        print(f"    • {case}")
    
    # 实践2：资源管理
    print(f"\n实践2：资源管理最佳实践")
    
    def safe_file_reader(filename):
        """安全的文件读取生成器"""
        file_handle = None
        try:
            # 模拟文件打开
            print(f"    打开文件: {filename}")
            file_handle = f"handle_for_{filename}"
            
            # 模拟文件内容
            content = [f"line_{i}" for i in range(5)]
            for line in content:
                yield line
        
        except Exception as e:
            print(f"    文件读取错误: {e}")
            raise
        finally:
            if file_handle:
                print(f"    关闭文件: {filename}")
    
    print("  安全文件读取:")
    for line in safe_file_reader("example.txt"):
        print(f"    读取: {line}")
    
    # 实践3：错误处理
    print(f"\n实践3：错误处理最佳实践")
    
    def robust_generator(data):
        """健壮的生成器"""
        for item in data:
            try:
                # 可能出错的处理
                if item < 0:
                    raise ValueError(f"负数: {item}")
                
                result = item ** 2
                yield result
                
            except ValueError as e:
                # 记录错误但继续处理
                print(f"    跳过错误项: {e}")
                continue
            except Exception as e:
                # 严重错误，停止处理
                print(f"    严重错误: {e}")
                break
    
    test_data = [1, 2, -1, 4, -2, 5]
    print("  健壮错误处理:")
    results = list(robust_generator(test_data))
    print(f"    处理结果: {results}")
    
    # 实践4：类型注解
    print(f"\n实践4：类型注解最佳实践")
    
    def typed_generator(data: Iterable[int]) -> Generator[int, None, None]:
        """带类型注解的生成器"""
        for item in data:
            yield item * 2
    
    def typed_coroutine() -> Generator[str, int, str]:
        """带类型注解的协程"""
        total = 0
        while True:
            value = yield f"当前总计: {total}"
            if value is None:
                break
            total += value
        return f"最终总计: {total}"
    
    print("  类型注解示例:")
    print("    def typed_generator(data: Iterable[int]) -> Generator[int, None, None]:")
    print("    def typed_coroutine() -> Generator[str, int, str]:")
    
    # 实践5：文档化
    print(f"\n实践5：文档化最佳实践")
    
    def documented_generator(data):
        """
        处理数据的生成器
        
        Args:
            data: 输入数据序列
            
        Yields:
            int: 处理后的数据
            
        Raises:
            ValueError: 当输入包含无效数据时
            
        Example:
            >>> gen = documented_generator([1, 2, 3])
            >>> list(gen)
            [2, 4, 6]
        """
        for item in data:
            if not isinstance(item, (int, float)):
                raise ValueError(f"无效数据类型: {type(item)}")
            yield item * 2
    
    print("  文档化生成器:")
    print("    包含参数说明、返回值、异常和使用示例")
    
    # 最佳实践总结
    print(f"\n最佳实践总结:")
    practices = [
        "1. 在合适的场景使用生成器",
        "2. 注意资源管理和清理",
        "3. 实现健壮的错误处理",
        "4. 使用类型注解提高可读性",
        "5. 编写清晰的文档和示例",
        "6. 避免生成器中的副作用",
        "7. 考虑生成器的生命周期",
        "8. 适当使用yield from",
        "9. 测试边界条件",
        "10. 监控内存和性能"
    ]
    
    for practice in practices:
        print(f"  {practice}")
    
    print()


if __name__ == '__main__':
    main() 