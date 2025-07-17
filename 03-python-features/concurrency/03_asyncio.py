#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python异步编程详解
Asyncio Programming in Python

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习Python asyncio模块、async/await语法和与Java CompletableFuture的对比

学习目标:
1. 掌握asyncio模块和async/await语法
2. 理解异步编程模型和事件循环
3. 学会异步I/O操作和并发控制
4. 对比Java CompletableFuture和响应式编程

注意：异步编程适用于I/O密集型任务，通过协作式多任务提高效率
"""

import asyncio
import aiohttp
import aiofiles
import time
import random
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import json


async def demo_basic_async_syntax():
    """演示基本异步语法"""
    print("=== 1. 基本异步语法 ===")
    
    # 简单的异步函数
    async def simple_async_function():
        """简单异步函数"""
        print("  异步函数开始执行")
        await asyncio.sleep(1)  # 异步等待1秒
        print("  异步函数执行完成")
        return "异步函数结果"
    
    # 多个异步任务
    async def async_task(name, duration):
        """异步任务"""
        print(f"  任务 {name} 开始")
        await asyncio.sleep(duration)
        print(f"  任务 {name} 完成")
        return f"{name}_结果"
    
    print("1. 基本async/await语法:")
    
    # 运行单个异步函数
    result = await simple_async_function()
    print(f"  结果: {result}")
    
    print("\n2. 并发执行多个异步任务:")
    
    # 并发执行多个任务
    tasks = [
        async_task("任务A", 1.0),
        async_task("任务B", 0.5),
        async_task("任务C", 1.5)
    ]
    
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    
    print(f"  所有任务结果: {results}")
    print(f"  总耗时: {end_time - start_time:.2f}秒")
    
    print("\n3. 对比同步vs异步执行:")
    
    # 同步执行
    def sync_task(name, duration):
        print(f"  同步任务 {name} 开始")
        time.sleep(duration)
        print(f"  同步任务 {name} 完成")
        return f"{name}_结果"
    
    sync_start = time.time()
    sync_results = [
        sync_task("同步A", 1.0),
        sync_task("同步B", 0.5),
        sync_task("同步C", 1.5)
    ]
    sync_end = time.time()
    
    print(f"  同步执行总耗时: {sync_end - sync_start:.2f}秒")
    print(f"  异步vs同步性能提升: {(sync_end - sync_start)/(end_time - start_time):.2f}x")
    
    """
    Java等价实现:
    
    // 1. 基本CompletableFuture
    public CompletableFuture<String> simpleAsyncFunction() {
        return CompletableFuture.supplyAsync(() -> {
            System.out.println("异步函数开始执行");
            try { Thread.sleep(1000); } catch (InterruptedException e) {}
            System.out.println("异步函数执行完成");
            return "异步函数结果";
        });
    }
    
    // 2. 并发执行多个任务
    public void concurrentTasks() {
        CompletableFuture<String> taskA = CompletableFuture.supplyAsync(() -> {
            return asyncTask("任务A", 1000);
        });
        
        CompletableFuture<String> taskB = CompletableFuture.supplyAsync(() -> {
            return asyncTask("任务B", 500);
        });
        
        CompletableFuture<String> taskC = CompletableFuture.supplyAsync(() -> {
            return asyncTask("任务C", 1500);
        });
        
        // 等待所有任务完成
        CompletableFuture<Void> allTasks = CompletableFuture.allOf(taskA, taskB, taskC);
        
        allTasks.thenRun(() -> {
            try {
                List<String> results = Arrays.asList(
                    taskA.get(), taskB.get(), taskC.get()
                );
                System.out.println("所有任务结果: " + results);
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }
    
    // 3. 异步链式操作
    public CompletableFuture<String> chainedAsync() {
        return CompletableFuture.supplyAsync(() -> "初始值")
                               .thenApply(value -> value + " -> 处理1")
                               .thenApply(value -> value + " -> 处理2")
                               .thenCompose(value -> 
                                   CompletableFuture.supplyAsync(() -> value + " -> 最终结果")
                               );
    }
    """
    
    print()


async def demo_asyncio_patterns():
    """演示asyncio常用模式"""
    print("=== 2. asyncio常用模式 ===")
    
    # 1. asyncio.create_task()
    print("1. 使用create_task创建任务:")
    
    async def background_task(name, interval, count):
        """后台任务"""
        for i in range(count):
            print(f"  后台任务 {name}: 第{i+1}次执行")
            await asyncio.sleep(interval)
        return f"{name} 完成"
    
    # 创建任务但不立即等待
    task1 = asyncio.create_task(background_task("后台1", 0.5, 3))
    task2 = asyncio.create_task(background_task("后台2", 0.8, 2))
    
    # 做其他工作
    await asyncio.sleep(1.0)
    print("  主任务工作中...")
    
    # 等待后台任务完成
    results = await asyncio.gather(task1, task2)
    print(f"  后台任务结果: {results}")
    
    # 2. asyncio.wait()
    print(f"\n2. 使用wait控制任务:")
    
    async def random_delay_task(task_id):
        delay = random.uniform(0.5, 2.0)
        await asyncio.sleep(delay)
        return f"任务{task_id}完成，延迟{delay:.2f}秒"
    
    tasks = [asyncio.create_task(random_delay_task(i)) for i in range(4)]
    
    # 等待第一个完成
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    first_result = list(done)[0].result()
    print(f"  第一个完成的任务: {first_result}")
    print(f"  还有 {len(pending)} 个任务未完成")
    
    # 等待剩余任务完成
    if pending:
        remaining_results = await asyncio.gather(*pending)
        print(f"  剩余任务结果: {remaining_results}")
    
    # 3. asyncio.as_completed()
    print(f"\n3. 使用as_completed按完成顺序处理:")
    
    async def varying_task(task_id):
        delay = random.uniform(0.2, 1.0)
        await asyncio.sleep(delay)
        return f"任务{task_id}(延迟{delay:.2f}s)"
    
    tasks = [varying_task(i) for i in range(5)]
    
    async for task in asyncio.as_completed(tasks):
        result = await task
        print(f"  按完成顺序: {result}")
    
    # 4. 超时控制
    print(f"\n4. 超时控制:")
    
    async def slow_task():
        await asyncio.sleep(3.0)
        return "慢任务完成"
    
    try:
        result = await asyncio.wait_for(slow_task(), timeout=2.0)
        print(f"  任务结果: {result}")
    except asyncio.TimeoutError:
        print("  任务超时")
    
    # 5. 异常处理
    print(f"\n5. 异常处理:")
    
    async def unreliable_task(task_id, fail_probability=0.3):
        await asyncio.sleep(0.5)
        if random.random() < fail_probability:
            raise ValueError(f"任务{task_id}随机失败")
        return f"任务{task_id}成功"
    
    tasks = [unreliable_task(i) for i in range(5)]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  任务{i}失败: {result}")
        else:
            print(f"  任务{i}成功: {result}")
    
    """
    Java异步模式等价实现:
    
    // 1. 创建任务但不立即等待
    public void createTaskExample() {
        CompletableFuture<String> task1 = CompletableFuture.supplyAsync(() -> 
            backgroundTask("后台1", 500, 3)
        );
        
        CompletableFuture<String> task2 = CompletableFuture.supplyAsync(() -> 
            backgroundTask("后台2", 800, 2)
        );
        
        // 做其他工作
        try { Thread.sleep(1000); } catch (InterruptedException e) {}
        System.out.println("主任务工作中...");
        
        // 等待后台任务完成
        CompletableFuture.allOf(task1, task2).join();
    }
    
    // 2. 超时控制
    public void timeoutExample() {
        CompletableFuture<String> slowTask = CompletableFuture.supplyAsync(() -> {
            try { Thread.sleep(3000); } catch (InterruptedException e) {}
            return "慢任务完成";
        });
        
        try {
            String result = slowTask.get(2, TimeUnit.SECONDS);
            System.out.println("任务结果: " + result);
        } catch (TimeoutException e) {
            System.out.println("任务超时");
            slowTask.cancel(true);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    // 3. 异常处理
    public void exceptionHandlingExample() {
        List<CompletableFuture<String>> tasks = IntStream.range(0, 5)
            .mapToObj(i -> CompletableFuture.supplyAsync(() -> 
                unreliableTask(i, 0.3)
            ).exceptionally(throwable -> 
                "任务" + i + "失败: " + throwable.getMessage()
            ))
            .collect(Collectors.toList());
        
        CompletableFuture<Void> allTasks = CompletableFuture.allOf(
            tasks.toArray(new CompletableFuture[0])
        );
        
        allTasks.thenRun(() -> {
            tasks.forEach(task -> {
                try {
                    System.out.println(task.get());
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
        });
    }
    """
    
    print()


async def demo_async_io_operations():
    """演示异步I/O操作"""
    print("=== 3. 异步I/O操作 ===")
    
    # 1. 异步文件操作
    print("1. 异步文件操作:")
    
    # 模拟写入多个文件
    async def write_file_async(filename, content):
        """异步写入文件"""
        try:
            async with aiofiles.open(filename, 'w') as f:
                await f.write(content)
            print(f"  写入文件 {filename} 完成")
            return f"文件 {filename} 写入成功"
        except Exception as e:
            print(f"  写入文件 {filename} 失败: {e}")
            # 模拟文件操作，不实际写入
            await asyncio.sleep(0.1)
            return f"文件 {filename} 模拟写入成功"
    
    # 并发写入多个文件
    write_tasks = [
        write_file_async(f"temp_file_{i}.txt", f"这是文件{i}的内容\n" * 100)
        for i in range(3)
    ]
    
    start_time = time.time()
    write_results = await asyncio.gather(*write_tasks)
    write_time = time.time() - start_time
    
    print(f"  异步写入耗时: {write_time:.4f}秒")
    print(f"  写入结果: {write_results}")
    
    # 2. 异步HTTP请求
    print(f"\n2. 异步HTTP请求:")
    
    async def fetch_url(session, url):
        """异步获取URL"""
        try:
            async with session.get(url) as response:
                return {
                    'url': url,
                    'status': response.status,
                    'content_length': len(await response.text())
                }
        except Exception as e:
            return {
                'url': url,
                'error': str(e)
            }
    
    # 模拟HTTP请求（使用httpbin.org测试API）
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2', 
        'https://httpbin.org/delay/1',
        'https://httpbin.org/status/200'
    ]
    
    try:
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            
            # 并发请求
            http_tasks = [fetch_url(session, url) for url in urls]
            http_results = await asyncio.gather(*http_tasks, return_exceptions=True)
            
            http_time = time.time() - start_time
            
            print(f"  异步HTTP请求耗时: {http_time:.4f}秒")
            for result in http_results:
                if isinstance(result, Exception):
                    print(f"    请求失败: {result}")
                else:
                    print(f"    {result}")
    
    except ImportError:
        print("  aiohttp未安装，模拟HTTP请求")
        
        async def mock_http_request(url):
            # 模拟网络延迟
            delay = random.uniform(0.5, 2.0)
            await asyncio.sleep(delay)
            return {
                'url': url,
                'status': 200,
                'delay': delay
            }
        
        start_time = time.time()
        mock_results = await asyncio.gather(*[mock_http_request(url) for url in urls])
        mock_time = time.time() - start_time
        
        print(f"  模拟HTTP请求耗时: {mock_time:.4f}秒")
        for result in mock_results:
            print(f"    {result}")
    
    # 3. 异步数据库操作模拟
    print(f"\n3. 异步数据库操作模拟:")
    
    class MockAsyncDB:
        """模拟异步数据库"""
        
        def __init__(self):
            self.data = {}
        
        async def insert(self, key, value):
            await asyncio.sleep(0.1)  # 模拟数据库插入延迟
            self.data[key] = value
            return f"插入 {key}: {value}"
        
        async def select(self, key):
            await asyncio.sleep(0.05)  # 模拟数据库查询延迟
            return self.data.get(key, None)
        
        async def update(self, key, value):
            await asyncio.sleep(0.08)  # 模拟数据库更新延迟
            if key in self.data:
                self.data[key] = value
                return f"更新 {key}: {value}"
            return f"键 {key} 不存在"
        
        async def delete(self, key):
            await asyncio.sleep(0.06)  # 模拟数据库删除延迟
            if key in self.data:
                del self.data[key]
                return f"删除 {key}"
            return f"键 {key} 不存在"
    
    db = MockAsyncDB()
    
    # 并发数据库操作
    db_operations = [
        db.insert("user1", {"name": "Alice", "age": 25}),
        db.insert("user2", {"name": "Bob", "age": 30}),
        db.insert("user3", {"name": "Charlie", "age": 35}),
    ]
    
    start_time = time.time()
    insert_results = await asyncio.gather(*db_operations)
    
    # 并发查询
    query_operations = [
        db.select("user1"),
        db.select("user2"),
        db.select("user3"),
        db.select("user4")  # 不存在的键
    ]
    
    query_results = await asyncio.gather(*query_operations)
    db_time = time.time() - start_time
    
    print(f"  数据库操作耗时: {db_time:.4f}秒")
    print(f"  插入结果: {insert_results}")
    print(f"  查询结果: {query_results}")
    
    """
    Java异步I/O等价实现:
    
    // 1. 异步文件操作（Java NIO.2）
    public CompletableFuture<String> writeFileAsync(String filename, String content) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                Path path = Paths.get(filename);
                Files.write(path, content.getBytes(), StandardOpenOption.CREATE);
                return "文件 " + filename + " 写入成功";
            } catch (IOException e) {
                throw new RuntimeException("写入文件失败", e);
            }
        });
    }
    
    // 2. 异步HTTP请求（使用Java 11+ HttpClient）
    public CompletableFuture<String> fetchUrlAsync(String url) {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                                        .uri(URI.create(url))
                                        .build();
        
        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                    .thenApply(response -> {
                        return "URL: " + url + ", Status: " + response.statusCode() +
                               ", Length: " + response.body().length();
                    });
    }
    
    // 3. 响应式数据库操作（使用Spring WebFlux + R2DBC）
    @Repository
    public class ReactiveUserRepository {
        
        @Autowired
        private R2dbcEntityTemplate template;
        
        public Mono<User> save(User user) {
            return template.insert(user);
        }
        
        public Mono<User> findById(Long id) {
            return template.selectOne(
                Query.query(Criteria.where("id").is(id)), 
                User.class
            );
        }
        
        public Flux<User> findAll() {
            return template.select(User.class).all();
        }
    }
    
    // 使用示例
    public void reactiveExample() {
        Flux<User> users = userRepository.findAll();
        
        users.map(user -> user.getName().toUpperCase())
             .filter(name -> name.startsWith("A"))
             .subscribe(
                 name -> System.out.println("处理用户: " + name),
                 error -> System.err.println("错误: " + error),
                 () -> System.out.println("处理完成")
             );
    }
    """
    
    print()


async def demo_async_synchronization():
    """演示异步同步机制"""
    print("=== 4. 异步同步机制 ===")
    
    # 1. asyncio.Lock
    print("1. asyncio.Lock:")
    
    shared_resource = 0
    async_lock = asyncio.Lock()
    
    async def increment_with_lock(name, count):
        """使用异步锁的增量函数"""
        global shared_resource
        for i in range(count):
            async with async_lock:
                temp = shared_resource
                await asyncio.sleep(0.01)  # 模拟异步操作
                shared_resource = temp + 1
                print(f"  {name}: {temp} -> {shared_resource}")
    
    # 并发运行增量任务
    lock_tasks = [
        increment_with_lock("任务A", 3),
        increment_with_lock("任务B", 3),
        increment_with_lock("任务C", 2)
    ]
    
    await asyncio.gather(*lock_tasks)
    print(f"  最终共享值: {shared_resource}")
    
    # 2. asyncio.Semaphore
    print(f"\n2. asyncio.Semaphore:")
    
    # 限制并发访问资源的数量
    semaphore = asyncio.Semaphore(2)  # 最多2个并发
    
    async def limited_resource_access(task_id):
        """受限资源访问"""
        print(f"  任务{task_id}: 请求访问资源")
        
        async with semaphore:
            print(f"  任务{task_id}: 获得资源访问权")
            await asyncio.sleep(random.uniform(1.0, 2.0))  # 模拟使用资源
            print(f"  任务{task_id}: 释放资源")
    
    semaphore_tasks = [limited_resource_access(i) for i in range(5)]
    await asyncio.gather(*semaphore_tasks)
    
    # 3. asyncio.Event
    print(f"\n3. asyncio.Event:")
    
    ready_event = asyncio.Event()
    
    async def waiter(name):
        """等待者"""
        print(f"  {name}: 等待事件...")
        await ready_event.wait()
        print(f"  {name}: 事件发生，开始工作!")
        await asyncio.sleep(0.5)  # 模拟工作
        print(f"  {name}: 工作完成")
    
    async def event_setter():
        """事件设置者"""
        print("  设置者: 准备设置事件...")
        await asyncio.sleep(2.0)
        ready_event.set()
        print("  设置者: 事件已设置!")
    
    # 启动等待者和设置者
    event_tasks = [
        waiter("等待者1"),
        waiter("等待者2"),
        waiter("等待者3"),
        event_setter()
    ]
    
    await asyncio.gather(*event_tasks)
    
    # 4. asyncio.Condition
    print(f"\n4. asyncio.Condition:")
    
    items = []
    condition = asyncio.Condition()
    
    async def async_consumer(name):
        """异步消费者"""
        async with condition:
            while len(items) == 0:
                print(f"  {name}: 等待物品...")
                await condition.wait()
            
            item = items.pop(0)
            print(f"  {name}: 消费了 {item}")
    
    async def async_producer(name):
        """异步生产者"""
        for i in range(3):
            async with condition:
                item = f"{name}-物品{i}"
                items.append(item)
                print(f"  {name}: 生产了 {item}")
                condition.notify()  # 通知等待的消费者
            
            await asyncio.sleep(0.5)  # 生产间隔
    
    # 运行生产者和消费者
    condition_tasks = [
        async_consumer("消费者"),
        async_producer("生产者")
    ]
    
    await asyncio.gather(*condition_tasks)
    
    # 5. asyncio.Queue
    print(f"\n5. asyncio.Queue:")
    
    async_queue = asyncio.Queue(maxsize=3)
    
    async def queue_producer(name, count):
        """队列生产者"""
        for i in range(count):
            item = f"{name}-产品{i}"
            await async_queue.put(item)
            print(f"  🏭 {name}: 生产了 {item}")
            await asyncio.sleep(0.3)
        
        # 发送结束信号
        await async_queue.put(None)
    
    async def queue_consumer(name):
        """队列消费者"""
        consumed = 0
        while True:
            item = await async_queue.get()
            if item is None:
                # 结束信号，放回队列供其他消费者使用
                await async_queue.put(None)
                break
            
            print(f"  🛒 {name}: 消费了 {item}")
            consumed += 1
            await asyncio.sleep(0.5)  # 消费时间
            async_queue.task_done()
        
        print(f"  ✅ {name}: 消费完成，共{consumed}个")
    
    # 启动生产者和消费者
    queue_tasks = [
        queue_producer("异步生产者", 5),
        queue_consumer("异步消费者1"),
        queue_consumer("异步消费者2")
    ]
    
    await asyncio.gather(*queue_tasks)
    
    """
    Java异步同步等价实现:
    
    // 1. 异步锁（使用CompletableFuture + synchronized）
    public class AsyncLock {
        private final Object lock = new Object();
        private volatile boolean isLocked = false;
        private final Queue<CompletableFuture<Void>> waitingQueue = new ConcurrentLinkedQueue<>();
        
        public CompletableFuture<Void> acquire() {
            synchronized (lock) {
                if (!isLocked) {
                    isLocked = true;
                    return CompletableFuture.completedFuture(null);
                } else {
                    CompletableFuture<Void> future = new CompletableFuture<>();
                    waitingQueue.offer(future);
                    return future;
                }
            }
        }
        
        public void release() {
            synchronized (lock) {
                CompletableFuture<Void> next = waitingQueue.poll();
                if (next != null) {
                    next.complete(null);
                } else {
                    isLocked = false;
                }
            }
        }
    }
    
    // 2. 信号量（Semaphore已经内置异步支持）
    Semaphore semaphore = new Semaphore(2);
    
    public CompletableFuture<Void> limitedResourceAccess(int taskId) {
        return CompletableFuture.runAsync(() -> {
            try {
                semaphore.acquire();
                System.out.println("任务" + taskId + ": 获得资源访问权");
                Thread.sleep(1000); // 模拟使用资源
                System.out.println("任务" + taskId + ": 释放资源");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                semaphore.release();
            }
        });
    }
    
    // 3. 响应式队列（使用Reactor）
    public class ReactiveQueue {
        private final Flux<String> sourceFlux;
        private final EmitterProcessor<String> processor;
        
        public ReactiveQueue() {
            this.processor = EmitterProcessor.create();
            this.sourceFlux = processor.share();
        }
        
        public void produce(String item) {
            processor.onNext(item);
        }
        
        public Flux<String> consume() {
            return sourceFlux;
        }
        
        public void complete() {
            processor.onComplete();
        }
    }
    
    // 使用示例
    public void reactiveQueueExample() {
        ReactiveQueue queue = new ReactiveQueue();
        
        // 消费者
        queue.consume()
             .subscribe(item -> System.out.println("消费: " + item));
        
        // 生产者
        Flux.interval(Duration.ofMillis(500))
            .take(5)
            .map(i -> "产品" + i)
            .subscribe(queue::produce);
    }
    """
    
    print()


async def demo_performance_optimization():
    """演示异步性能优化"""
    print("=== 5. 异步性能优化 ===")
    
    # 1. 批量处理优化
    print("1. 批量处理优化:")
    
    async def process_item(item):
        """处理单个项目"""
        await asyncio.sleep(0.1)  # 模拟I/O延迟
        return item ** 2
    
    async def batch_process(items, batch_size=10):
        """批量处理项目"""
        results = []
        for i in range(0, len(items), batch_size):
            batch = items[i:i+batch_size]
            batch_tasks = [process_item(item) for item in batch]
            batch_results = await asyncio.gather(*batch_tasks)
            results.extend(batch_results)
            print(f"  处理批次 {i//batch_size + 1}, 大小: {len(batch)}")
        
        return results
    
    items = list(range(50))
    
    # 对比不同批处理大小的性能
    for batch_size in [5, 10, 20]:
        start_time = time.time()
        results = await batch_process(items.copy(), batch_size)
        batch_time = time.time() - start_time
        print(f"  批大小 {batch_size}: {batch_time:.4f}秒")
    
    # 2. 连接池优化
    print(f"\n2. 连接池优化:")
    
    class MockConnectionPool:
        """模拟连接池"""
        
        def __init__(self, pool_size=5):
            self.pool = asyncio.Queue(maxsize=pool_size)
            self.pool_size = pool_size
            self.created_connections = 0
        
        async def get_connection(self):
            """获取连接"""
            if self.pool.empty() and self.created_connections < self.pool_size:
                # 创建新连接
                connection = f"连接{self.created_connections}"
                self.created_connections += 1
                print(f"    创建新连接: {connection}")
                return connection
            else:
                # 从池中获取连接
                connection = await self.pool.get()
                print(f"    从池中获取连接: {connection}")
                return connection
        
        async def return_connection(self, connection):
            """归还连接"""
            await self.pool.put(connection)
            print(f"    归还连接到池: {connection}")
    
    async def use_connection_pool(pool, task_id):
        """使用连接池的任务"""
        connection = await pool.get_connection()
        
        # 模拟使用连接进行工作
        await asyncio.sleep(random.uniform(0.5, 1.0))
        print(f"  任务{task_id}: 使用{connection}完成工作")
        
        await pool.return_connection(connection)
    
    pool = MockConnectionPool(pool_size=3)
    
    # 并发任务超过连接池大小
    pool_tasks = [use_connection_pool(pool, i) for i in range(8)]
    await asyncio.gather(*pool_tasks)
    
    # 3. 缓存优化
    print(f"\n3. 缓存优化:")
    
    class AsyncCache:
        """异步缓存"""
        
        def __init__(self, ttl=5.0):
            self.cache = {}
            self.ttl = ttl
        
        async def get(self, key, fetcher):
            """获取缓存值，如果不存在则使用fetcher获取"""
            current_time = time.time()
            
            if key in self.cache:
                value, timestamp = self.cache[key]
                if current_time - timestamp < self.ttl:
                    print(f"    缓存命中: {key}")
                    return value
                else:
                    print(f"    缓存过期: {key}")
                    del self.cache[key]
            
            print(f"    缓存未命中，获取新值: {key}")
            value = await fetcher(key)
            self.cache[key] = (value, current_time)
            return value
    
    cache = AsyncCache(ttl=3.0)
    
    async def expensive_operation(key):
        """昂贵的操作"""
        await asyncio.sleep(1.0)  # 模拟昂贵计算
        return f"结果_{key}_{random.randint(1, 100)}"
    
    # 测试缓存效果
    cache_keys = ["数据A", "数据B", "数据A", "数据C", "数据A"]
    
    for key in cache_keys:
        start_time = time.time()
        result = await cache.get(key, expensive_operation)
        operation_time = time.time() - start_time
        print(f"  获取 {key}: {result[:20]}..., 耗时: {operation_time:.4f}秒")
        
        await asyncio.sleep(0.5)  # 间隔
    
    # 4. 限流优化
    print(f"\n4. 限流优化:")
    
    class RateLimiter:
        """速率限制器"""
        
        def __init__(self, rate, per_second=1.0):
            self.rate = rate  # 每per_second秒允许的请求数
            self.per_second = per_second
            self.tokens = rate
            self.last_update = time.time()
            self.lock = asyncio.Lock()
        
        async def acquire(self):
            """获取令牌"""
            async with self.lock:
                now = time.time()
                # 补充令牌
                elapsed = now - self.last_update
                self.tokens = min(self.rate, self.tokens + elapsed * (self.rate / self.per_second))
                self.last_update = now
                
                if self.tokens >= 1:
                    self.tokens -= 1
                    return True
                else:
                    # 需要等待
                    wait_time = (1 - self.tokens) * (self.per_second / self.rate)
                    await asyncio.sleep(wait_time)
                    self.tokens = 0
                    return True
    
    rate_limiter = RateLimiter(rate=3, per_second=1.0)  # 每秒3个请求
    
    async def rate_limited_task(task_id):
        """受限流控制的任务"""
        await rate_limiter.acquire()
        print(f"  执行限流任务{task_id}: {time.time():.2f}")
        return f"任务{task_id}完成"
    
    # 快速提交多个任务，观察限流效果
    start_time = time.time()
    rate_tasks = [rate_limited_task(i) for i in range(8)]
    rate_results = await asyncio.gather(*rate_tasks)
    total_time = time.time() - start_time
    
    print(f"  限流任务总耗时: {total_time:.2f}秒")
    
    """
    Java异步性能优化等价实现:
    
    // 1. 批量处理（使用Reactor）
    public Flux<Integer> batchProcess(List<Integer> items, int batchSize) {
        return Flux.fromIterable(items)
                  .buffer(batchSize)
                  .flatMap(batch -> 
                      Flux.fromIterable(batch)
                          .flatMap(this::processItem)
                          .collectList()
                          .flatMapMany(Flux::fromIterable)
                  );
    }
    
    // 2. 连接池（使用HikariCP + R2DBC）
    @Configuration
    public class DatabaseConfig {
        
        @Bean
        public ConnectionFactory connectionFactory() {
            return new PostgresqlConnectionFactory(
                PostgresqlConnectionConfiguration.builder()
                    .host("localhost")
                    .port(5432)
                    .database("mydb")
                    .username("user")
                    .password("password")
                    .initialSize(5)
                    .maxSize(10)
                    .build()
            );
        }
    }
    
    // 3. 异步缓存（使用Caffeine + CompletableFuture）
    public class AsyncCache<K, V> {
        private final Cache<K, CompletableFuture<V>> cache;
        
        public AsyncCache(Duration ttl) {
            this.cache = Caffeine.newBuilder()
                               .expireAfterWrite(ttl)
                               .build();
        }
        
        public CompletableFuture<V> get(K key, Function<K, CompletableFuture<V>> loader) {
            return cache.get(key, k -> loader.apply(k));
        }
    }
    
    // 4. 限流器（使用Resilience4j）
    public class RateLimiterExample {
        private final RateLimiter rateLimiter;
        
        public RateLimiterExample() {
            this.rateLimiter = RateLimiter.of("api", RateLimiterConfig.custom()
                .limitRefreshPeriod(Duration.ofSeconds(1))
                .limitForPeriod(3)
                .timeoutDuration(Duration.ofSeconds(5))
                .build());
        }
        
        public CompletableFuture<String> rateLimitedTask(int taskId) {
            Supplier<String> decoratedSupplier = RateLimiter
                .decorateSupplier(rateLimiter, () -> {
                    return "任务" + taskId + "完成";
                });
            
            return CompletableFuture.supplyAsync(decoratedSupplier);
        }
    }
    """
    
    print()


async def main_async():
    """异步主函数：运行所有演示"""
    print("Python异步编程完整学习指南")
    print("=" * 50)
    
    await demo_basic_async_syntax()
    await demo_asyncio_patterns()
    await demo_async_io_operations()
    await demo_async_synchronization()
    await demo_performance_optimization()
    
    print("学习总结:")
    print("1. async/await提供简洁的异步编程语法")
    print("2. asyncio模块提供完整的异步I/O支持")
    print("3. 事件循环是异步编程的核心")
    print("4. 异步同步原语：Lock、Semaphore、Event、Condition、Queue")
    print("5. 性能优化：批处理、连接池、缓存、限流")
    print("6. 适用于I/O密集型任务，可以大幅提升并发性能")
    print("7. Java CompletableFuture和响应式编程提供类似功能")
    print("8. Python asyncio更直观，Java响应式编程更强大")


def main():
    """同步主函数入口"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main() 