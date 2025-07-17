#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python生成器函数详解
Generator Functions in Python

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习Python生成器函数的语法、yield关键字、协程基础和内存优化应用

学习目标:
1. 掌握生成器函数和yield关键字的使用
2. 理解生成器的状态管理和协程基础
3. 学会内存优化和无限序列处理
4. 对比Java中的类似概念和实现方式
"""

import time
import random
import sys
from typing import Generator, Iterator, Any
from collections import deque


def demo_basic_generator_syntax():
    """演示生成器函数的基本语法"""
    print("=== 1. 生成器函数基本语法 ===")
    
    # 简单的生成器函数
    def count_to_n(n):
        """计数到n的生成器"""
        print(f"开始生成数字...")
        for i in range(1, n + 1):
            print(f"  生成数字: {i}")
            yield i
        print(f"生成完成!")
    
    # 普通函数 vs 生成器函数
    def normal_function(n):
        """普通函数返回列表"""
        print("普通函数：立即生成所有数字")
        return [i for i in range(1, n + 1)]
    
    print("普通函数调用:")
    normal_result = normal_function(5)
    print(f"结果: {normal_result}")
    print(f"类型: {type(normal_result)}")
    print()
    
    print("生成器函数调用:")
    generator = count_to_n(5)
    print(f"生成器对象: {generator}")
    print(f"类型: {type(generator)}")
    
    print("\n手动获取生成器的值:")
    try:
        while True:
            value = next(generator)
            print(f"获得值: {value}")
    except StopIteration:
        print("生成器已耗尽")
    
    print("\n使用for循环遍历生成器:")
    generator2 = count_to_n(3)
    for value in generator2:
        print(f"循环获得: {value}")
    
    # yield的不同用法
    def multiple_yields():
        """多个yield的生成器"""
        yield "第一个值"
        yield "第二个值"
        yield "第三个值"
    
    print("\n多个yield:")
    for item in multiple_yields():
        print(f"  {item}")
    
    # 带条件的yield
    def even_numbers(max_num):
        """生成偶数的生成器"""
        for i in range(max_num):
            if i % 2 == 0:
                yield i
    
    print("\n条件yield - 偶数:")
    evens = list(even_numbers(10))
    print(f"偶数列表: {evens}")
    
    """
    Java等价实现:
    
    // Java没有直接的生成器语法，需要实现Iterator接口
    public class CountToN implements Iterator<Integer> {
        private int current = 1;
        private final int max;
        
        public CountToN(int n) {
            this.max = n;
        }
        
        @Override
        public boolean hasNext() {
            return current <= max;
        }
        
        @Override
        public Integer next() {
            if (!hasNext()) {
                throw new NoSuchElementException();
            }
            System.out.println("生成数字: " + current);
            return current++;
        }
    }
    
    // 使用Stream API的替代方案
    Stream<Integer> countStream = IntStream.rangeClosed(1, 5)
                                          .peek(i -> System.out.println("生成数字: " + i))
                                          .boxed();
    
    // 或者使用自定义Supplier
    public class NumberGenerator implements Supplier<Integer> {
        private int current = 1;
        private final int max;
        
        public NumberGenerator(int max) { this.max = max; }
        
        @Override
        public Integer get() {
            return current <= max ? current++ : null;
        }
    }
    """
    
    print()


def demo_generator_state_management():
    """演示生成器的状态管理"""
    print("=== 2. 生成器状态管理 ===")
    
    # 生成器维持状态
    def fibonacci_generator():
        """斐波那契数列生成器"""
        print("初始化斐波那契生成器")
        a, b = 0, 1
        while True:
            print(f"  当前状态: a={a}, b={b}")
            yield a
            a, b = b, a + b
    
    print("斐波那契数列生成器:")
    fib = fibonacci_generator()
    
    # 获取前10个斐波那契数
    fib_numbers = []
    for _ in range(10):
        fib_numbers.append(next(fib))
    
    print(f"前10个斐波那契数: {fib_numbers}")
    
    # 生成器的状态保持
    print("\n生成器状态保持演示:")
    
    def stateful_generator():
        """有状态的生成器"""
        count = 0
        while True:
            count += 1
            received = yield f"第{count}次调用"
            if received:
                print(f"  收到消息: {received}")
                count += 10  # 收到消息时跳跃计数
    
    gen = stateful_generator()
    
    # 启动生成器
    print(next(gen))  # 第1次调用
    print(next(gen))  # 第2次调用
    
    # 发送值到生成器
    print(gen.send("跳跃!"))  # 第13次调用（2+10+1）
    print(next(gen))  # 第14次调用
    
    # 生成器的方法
    print("\n生成器对象的方法:")
    
    def demo_generator():
        try:
            yield "开始"
            yield "中间"
            yield "结束"
        except GeneratorExit:
            print("  生成器被关闭")
        except Exception as e:
            print(f"  生成器收到异常: {e}")
            yield "异常处理"
    
    gen = demo_generator()
    print(f"1. {next(gen)}")
    
    # 发送异常到生成器
    try:
        gen.throw(ValueError, "测试异常")
    except StopIteration:
        pass
    
    # 重新创建生成器测试关闭
    gen = demo_generator()
    print(f"2. {next(gen)}")
    gen.close()  # 关闭生成器
    
    try:
        next(gen)  # 尝试继续使用已关闭的生成器
    except StopIteration:
        print("  生成器已关闭，无法继续使用")
    
    """
    Java状态管理等价实现:
    
    public class FibonacciIterator implements Iterator<Integer> {
        private int a = 0, b = 1;
        
        @Override
        public boolean hasNext() {
            return true; // 无限序列
        }
        
        @Override
        public Integer next() {
            int current = a;
            int temp = a + b;
            a = b;
            b = temp;
            return current;
        }
    }
    
    // 使用Stream生成无限序列
    Stream<Integer> fibonacciStream = Stream.iterate(
        new int[]{0, 1},
        t -> new int[]{t[1], t[0] + t[1]}
    ).map(t -> t[0]);
    
    List<Integer> first10 = fibonacciStream.limit(10)
                                         .collect(Collectors.toList());
    """
    
    print()


def demo_yield_from():
    """演示yield from语法"""
    print("=== 3. yield from语法 ===")
    
    # 基本的yield from用法
    def sub_generator():
        """子生成器"""
        yield "子生成器: 1"
        yield "子生成器: 2"
        yield "子生成器: 3"
    
    def main_generator():
        """主生成器使用yield from"""
        yield "主生成器: 开始"
        yield from sub_generator()  # 委托给子生成器
        yield "主生成器: 结束"
    
    print("yield from基本用法:")
    for item in main_generator():
        print(f"  {item}")
    
    # yield from 与 迭代器
    def number_generator():
        """数字生成器"""
        yield from range(1, 4)      # 委托给range对象
        yield from [10, 20, 30]     # 委托给列表
        yield from "ABC"            # 委托给字符串
    
    print("\nyield from 与不同迭代器:")
    numbers = list(number_generator())
    print(f"结果: {numbers}")
    
    # 复杂的yield from示例
    def read_file_lines(filename):
        """模拟读取文件行的生成器"""
        # 模拟文件内容
        lines = [
            "第一行内容",
            "第二行内容", 
            "第三行内容"
        ]
        yield from lines
    
    def process_multiple_files(filenames):
        """处理多个文件的生成器"""
        for filename in filenames:
            print(f"处理文件: {filename}")
            yield f"=== {filename} ==="
            yield from read_file_lines(filename)
            yield "--- 文件结束 ---"
    
    print("\n处理多个文件:")
    files = ["file1.txt", "file2.txt"]
    for content in process_multiple_files(files):
        print(f"  {content}")
    
    # yield from 的返回值
    def sub_generator_with_return():
        """带返回值的子生成器"""
        yield "子: 1"
        yield "子: 2"
        return "子生成器完成"  # 返回值
    
    def main_generator_with_result():
        """接收子生成器返回值的主生成器"""
        yield "主: 开始"
        result = yield from sub_generator_with_return()
        yield f"主: 收到结果 - {result}"
        yield "主: 结束"
    
    print("\nyield from 返回值:")
    for item in main_generator_with_result():
        print(f"  {item}")
    
    # 递归生成器
    def tree_traversal(node):
        """树遍历生成器"""
        yield node["value"]
        for child in node.get("children", []):
            yield from tree_traversal(child)
    
    # 构建示例树
    tree = {
        "value": "根节点",
        "children": [
            {
                "value": "子节点1",
                "children": [
                    {"value": "叶节点1"},
                    {"value": "叶节点2"}
                ]
            },
            {
                "value": "子节点2",
                "children": [
                    {"value": "叶节点3"}
                ]
            }
        ]
    }
    
    print("\n树遍历:")
    for node_value in tree_traversal(tree):
        print(f"  访问: {node_value}")
    
    """
    Java递归遍历等价实现:
    
    public class TreeNode {
        private String value;
        private List<TreeNode> children;
        
        // 递归遍历
        public Stream<String> traverse() {
            Stream<String> currentNode = Stream.of(this.value);
            
            Stream<String> childrenNodes = children.stream()
                                                  .flatMap(TreeNode::traverse);
            
            return Stream.concat(currentNode, childrenNodes);
        }
    }
    
    // 使用
    List<String> allNodes = rootNode.traverse()
                                   .collect(Collectors.toList());
    """
    
    print()


def demo_generator_performance():
    """演示生成器的性能优势"""
    print("=== 4. 生成器性能优势 ===")
    
    # 内存使用对比
    def measure_memory_and_time(func, description):
        """测量内存和时间"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        start_time = time.time()
        
        result = func()
        
        end_time = time.time()
        end_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"{description}:")
        print(f"  时间: {end_time - start_time:.4f}秒")
        print(f"  内存变化: {end_memory - start_memory:.2f}MB")
        
        return result
    
    # 大数据集处理对比
    size = 1000000
    
    def list_approach():
        """列表方式 - 立即生成所有数据"""
        return [x**2 for x in range(size)]
    
    def generator_approach():
        """生成器方式 - 按需生成"""
        def square_generator():
            for x in range(size):
                yield x**2
        return square_generator()
    
    print(f"处理 {size:,} 个元素:")
    
    # 比较创建时间和内存
    list_result = measure_memory_and_time(list_approach, "列表方式")
    gen_result = measure_memory_and_time(generator_approach, "生成器方式")
    
    print(f"列表大小: {len(list_result):,} 元素")
    print(f"生成器对象: {gen_result}")
    
    # 部分消费的优势
    print(f"\n部分消费优势 (只需要前100个元素):")
    
    def consume_first_100_from_list():
        data = [x**2 for x in range(size)]  # 生成全部
        return data[:100]  # 只使用前100个
    
    def consume_first_100_from_generator():
        def square_gen():
            for x in range(size):
                yield x**2
        
        gen = square_gen()
        return [next(gen) for _ in range(100)]  # 只生成前100个
    
    list_partial = measure_memory_and_time(consume_first_100_from_list, "列表方式(部分消费)")
    gen_partial = measure_memory_and_time(consume_first_100_from_generator, "生成器方式(部分消费)")
    
    print(f"结果验证: {list_partial[:5]} == {gen_partial[:5]}")
    
    # 无限序列
    print(f"\n无限序列处理:")
    
    def infinite_primes():
        """无限质数生成器"""
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        candidate = 2
        while True:
            if is_prime(candidate):
                yield candidate
            candidate += 1
    
    def get_first_n_primes(n):
        """获取前n个质数"""
        primes = infinite_primes()
        return [next(primes) for _ in range(n)]
    
    first_20_primes = get_first_n_primes(20)
    print(f"前20个质数: {first_20_primes}")
    
    # 流水线处理
    print(f"\n流水线处理:")
    
    def data_source():
        """数据源生成器"""
        for i in range(10):
            print(f"  生成原始数据: {i}")
            yield i
    
    def transform_stage1(data_gen):
        """第一阶段转换"""
        for item in data_gen:
            transformed = item * 2
            print(f"  阶段1转换: {item} -> {transformed}")
            yield transformed
    
    def transform_stage2(data_gen):
        """第二阶段转换"""
        for item in data_gen:
            transformed = item + 1
            print(f"  阶段2转换: {item} -> {transformed}")
            yield transformed
    
    def filter_stage(data_gen):
        """过滤阶段"""
        for item in data_gen:
            if item > 10:
                print(f"  过滤通过: {item}")
                yield item
            else:
                print(f"  过滤拒绝: {item}")
    
    # 构建处理流水线
    pipeline = filter_stage(transform_stage2(transform_stage1(data_source())))
    
    print("流水线处理结果:")
    results = list(pipeline)
    print(f"最终结果: {results}")
    
    """
    Java流水线处理等价实现:
    
    // 使用Stream API构建处理流水线
    List<Integer> results = IntStream.range(0, 10)
                                   .peek(i -> System.out.println("生成原始数据: " + i))
                                   .map(i -> i * 2)
                                   .peek(i -> System.out.println("阶段1转换: " + i))
                                   .map(i -> i + 1)
                                   .peek(i -> System.out.println("阶段2转换: " + i))
                                   .filter(i -> {
                                       boolean pass = i > 10;
                                       System.out.println("过滤" + (pass ? "通过" : "拒绝") + ": " + i);
                                       return pass;
                                   })
                                   .boxed()
                                   .collect(Collectors.toList());
    
    // 无限Stream
    Stream<Integer> infinitePrimes = Stream.iterate(2, n -> n + 1)
                                          .filter(this::isPrime);
    
    List<Integer> first20Primes = infinitePrimes.limit(20)
                                               .collect(Collectors.toList());
    """
    
    print()


def demo_coroutine_basics():
    """演示协程基础"""
    print("=== 5. 协程基础 ===")
    
    # 简单的协程示例
    def simple_coroutine():
        """简单协程"""
        print("协程启动")
        x = yield
        print(f"协程收到值: {x}")
        y = yield x * 2
        print(f"协程收到值: {y}")
        return x + y
    
    print("简单协程示例:")
    coro = simple_coroutine()
    
    # 启动协程
    next(coro)  # 或者 coro.send(None)
    
    # 发送值
    result1 = coro.send(10)
    print(f"协程返回: {result1}")
    
    # 再次发送值并结束协程
    try:
        coro.send(5)
    except StopIteration as e:
        print(f"协程结束，返回值: {e.value}")
    
    # 协程状态
    print(f"\n协程状态:")
    
    def stateful_coroutine():
        """有状态的协程"""
        total = 0
        count = 0
        
        while True:
            value = yield total  # 返回当前总和，接收新值
            if value is None:
                break
            total += value
            count += 1
            print(f"  添加 {value}, 总和: {total}, 计数: {count}")
    
    coro = stateful_coroutine()
    next(coro)  # 启动协程
    
    print("累加协程:")
    print(f"发送 5: {coro.send(5)}")
    print(f"发送 10: {coro.send(10)}")
    print(f"发送 3: {coro.send(3)}")
    
    # 结束协程
    try:
        coro.send(None)
    except StopIteration:
        print("协程正常结束")
    
    # 生产者-消费者模式
    print(f"\n生产者-消费者模式:")
    
    def consumer():
        """消费者协程"""
        print("消费者准备就绪")
        while True:
            item = yield
            if item is None:
                break
            print(f"  消费者处理: {item}")
    
    def producer(consumer_coro):
        """生产者"""
        print("生产者开始生产")
        for i in range(5):
            item = f"产品{i}"
            print(f"  生产者产生: {item}")
            consumer_coro.send(item)
        consumer_coro.send(None)  # 结束信号
    
    # 运行生产者-消费者
    consumer_coro = consumer()
    next(consumer_coro)  # 启动消费者
    producer(consumer_coro)
    
    # 协程装饰器
    def coroutine(func):
        """协程装饰器 - 自动启动协程"""
        def wrapper(*args, **kwargs):
            coro = func(*args, **kwargs)
            next(coro)  # 自动启动
            return coro
        return wrapper
    
    @coroutine
    def auto_started_coroutine():
        """自动启动的协程"""
        print("协程自动启动了!")
        while True:
            value = yield
            if value is None:
                break
            print(f"  处理值: {value}")
    
    print(f"\n自动启动协程:")
    auto_coro = auto_started_coroutine()  # 自动启动，无需next()
    auto_coro.send("测试数据1")
    auto_coro.send("测试数据2")
    auto_coro.send(None)
    
    """
    Java协程等价实现（使用CompletableFuture或虚拟线程）:
    
    // Java 19+ 虚拟线程
    public class ProducerConsumer {
        
        public void runProducerConsumer() {
            BlockingQueue<String> queue = new LinkedBlockingQueue<>();
            
            // 消费者虚拟线程
            Thread consumer = Thread.ofVirtual().start(() -> {
                try {
                    while (true) {
                        String item = queue.take();
                        if ("STOP".equals(item)) break;
                        System.out.println("消费者处理: " + item);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            // 生产者虚拟线程
            Thread producer = Thread.ofVirtual().start(() -> {
                for (int i = 0; i < 5; i++) {
                    String item = "产品" + i;
                    System.out.println("生产者产生: " + item);
                    queue.offer(item);
                }
                queue.offer("STOP");
            });
            
            // 等待完成
            try {
                producer.join();
                consumer.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    // 或使用CompletableFuture链式处理
    CompletableFuture<Void> pipeline = CompletableFuture
        .supplyAsync(() -> "数据")
        .thenApply(data -> "处理:" + data)
        .thenAccept(result -> System.out.println("结果:" + result));
    """
    
    print()


def demo_practical_applications():
    """演示实际应用"""
    print("=== 6. 实际应用 ===")
    
    # 大文件逐行处理
    def read_large_file_lines(filename):
        """模拟大文件逐行读取"""
        # 模拟大文件内容
        file_content = [
            "日志行1: 用户登录 user123",
            "日志行2: 数据查询 query456", 
            "日志行3: 错误信息 error789",
            "日志行4: 用户登出 user123",
            "日志行5: 系统维护 maintenance"
        ]
        
        print(f"开始读取文件: {filename}")
        for line_num, line in enumerate(file_content, 1):
            print(f"  读取第{line_num}行")
            yield line
        print(f"文件读取完成: {filename}")
    
    def process_log_lines(lines_generator):
        """处理日志行"""
        for line in lines_generator:
            if "错误" in line or "error" in line:
                yield f"[ERROR] {line}"
            elif "用户" in line:
                yield f"[USER] {line}"
            else:
                yield f"[INFO] {line}"
    
    print("大文件处理示例:")
    raw_lines = read_large_file_lines("app.log")
    processed_lines = process_log_lines(raw_lines)
    
    for processed_line in processed_lines:
        print(f"  {processed_line}")
    
    # 批量数据处理
    print(f"\n批量数据处理:")
    
    def batch_processor(data_generator, batch_size=3):
        """批量处理生成器"""
        batch = []
        for item in data_generator:
            batch.append(item)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        
        # 处理剩余数据
        if batch:
            yield batch
    
    def data_stream():
        """数据流生成器"""
        for i in range(10):
            print(f"    生成数据: {i}")
            yield f"data_{i}"
    
    print("批量处理数据流:")
    data_gen = data_stream()
    batches = batch_processor(data_gen, batch_size=3)
    
    for batch_num, batch in enumerate(batches, 1):
        print(f"  批次{batch_num}: {batch}")
    
    # 实时数据监控
    print(f"\n实时数据监控:")
    
    def sensor_data_simulator():
        """传感器数据模拟器"""
        while True:
            # 模拟传感器数据
            temperature = random.uniform(20.0, 30.0)
            humidity = random.uniform(40.0, 80.0)
            
            yield {
                "timestamp": time.time(),
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2)
            }
            
            time.sleep(0.1)  # 模拟数据采集间隔
    
    def alert_monitor(sensor_gen):
        """警报监控器"""
        for data in sensor_gen:
            if data["temperature"] > 28.0:
                yield f"⚠️  高温警报: {data['temperature']}°C"
            elif data["temperature"] < 22.0:
                yield f"🧊 低温警报: {data['temperature']}°C"
            
            if data["humidity"] > 75.0:
                yield f"💧 高湿度警报: {data['humidity']}%"
    
    print("传感器监控 (5秒):")
    sensor_gen = sensor_data_simulator()
    alert_gen = alert_monitor(sensor_gen)
    
    start_time = time.time()
    alert_count = 0
    
    for alert in alert_gen:
        print(f"  {alert}")
        alert_count += 1
        
        # 运行5秒或收到10个警报就停止
        if time.time() - start_time > 2 or alert_count >= 10:
            break
    
    print(f"监控结束，共收到 {alert_count} 个警报")
    
    # 缓存和预加载
    print(f"\n缓存和预加载:")
    
    def cached_data_loader():
        """带缓存的数据加载器"""
        cache = deque(maxlen=3)  # 最多缓存3个项目
        
        def expensive_data_source():
            """昂贵的数据源"""
            for i in range(10):
                print(f"    从数据源加载: item_{i}")
                time.sleep(0.05)  # 模拟昂贵操作
                yield f"expensive_item_{i}"
        
        data_source = expensive_data_source()
        
        # 预加载前几个项目
        for _ in range(min(3, 10)):
            try:
                cache.append(next(data_source))
            except StopIteration:
                break
        
        # 返回缓存的数据，同时在后台加载更多
        while cache or True:
            if cache:
                item = cache.popleft()
                print(f"  从缓存返回: {item}")
                yield item
                
                # 尝试加载下一个项目到缓存
                try:
                    cache.append(next(data_source))
                except StopIteration:
                    if not cache:  # 缓存为空且数据源耗尽
                        break
            else:
                break
    
    print("缓存数据加载:")
    cached_loader = cached_data_loader()
    
    # 只消费前5个项目
    for i, item in enumerate(cached_loader):
        if i >= 5:
            break
        print(f"消费: {item}")
    
    """
    Java实际应用等价实现:
    
    // 大文件处理
    public Stream<String> readLargeFile(String filename) {
        try {
            return Files.lines(Paths.get(filename));
        } catch (IOException e) {
            return Stream.empty();
        }
    }
    
    public Stream<String> processLogLines(Stream<String> lines) {
        return lines.map(line -> {
            if (line.contains("错误") || line.contains("error")) {
                return "[ERROR] " + line;
            } else if (line.contains("用户")) {
                return "[USER] " + line;
            } else {
                return "[INFO] " + line;
            }
        });
    }
    
    // 批量处理
    public static <T> Stream<List<T>> batch(Stream<T> stream, int batchSize) {
        List<T> batch = new ArrayList<>();
        List<List<T>> batches = new ArrayList<>();
        
        stream.forEach(item -> {
            batch.add(item);
            if (batch.size() >= batchSize) {
                batches.add(new ArrayList<>(batch));
                batch.clear();
            }
        });
        
        if (!batch.isEmpty()) {
            batches.add(batch);
        }
        
        return batches.stream();
    }
    
    // 实时数据监控
    @Component
    public class SensorMonitor {
        
        @EventListener
        public void handleSensorData(SensorDataEvent event) {
            SensorData data = event.getData();
            
            if (data.getTemperature() > 28.0) {
                alertService.sendAlert("高温警报: " + data.getTemperature());
            }
            
            if (data.getHumidity() > 75.0) {
                alertService.sendAlert("高湿度警报: " + data.getHumidity());
            }
        }
    }
    """
    
    print()


def main():
    """主函数：运行所有演示"""
    print("Python生成器函数完整学习指南")
    print("=" * 50)
    
    demo_basic_generator_syntax()
    demo_generator_state_management()
    demo_yield_from()
    demo_generator_performance()
    demo_coroutine_basics()
    demo_practical_applications()
    
    print("学习总结:")
    print("1. 生成器函数使用yield关键字实现惰性求值")
    print("2. 维持内部状态，支持暂停和恢复执行")
    print("3. yield from实现生成器委托和组合")
    print("4. 内存效率高，适合处理大数据集和无限序列")
    print("5. 协程基础：支持双向通信和状态管理")
    print("6. Java虚拟线程和Stream API提供部分类似功能")
    print("7. 实际应用：文件处理、数据流水线、实时监控等")


if __name__ == "__main__":
    main() 