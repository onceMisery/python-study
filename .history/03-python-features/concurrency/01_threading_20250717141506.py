#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python多线程编程详解
Threading in Python

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习Python threading模块、线程同步机制和与Java Thread的对比

学习目标:
1. 掌握Python threading模块的基本使用
2. 理解GIL的影响和线程同步机制
3. 学会线程池和异步任务处理
4. 对比Java多线程编程的实现方式

注意：由于Python GIL的存在，多线程主要适用于I/O密集型任务
"""

import threading
import time
import random
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from threading import Lock, RLock, Condition, Semaphore, Event
from contextlib import contextmanager


def demo_basic_threading():
    """演示基本线程操作"""
    print("=== 1. 基本线程操作 ===")
    
    # 简单的线程函数
    def worker(name, duration):
        """工作线程函数"""
        print(f"线程 {name} 开始工作")
        for i in range(3):
            print(f"  {name}: 正在执行任务 {i+1}")
            time.sleep(duration)
        print(f"线程 {name} 工作完成")
    
    # 创建和启动线程的方式1：使用函数
    print("方式1: 使用函数创建线程")
    thread1 = threading.Thread(target=worker, args=("Worker-1", 0.5))
    thread2 = threading.Thread(target=worker, args=("Worker-2", 0.3))
    
    # 启动线程
    thread1.start()
    thread2.start()
    
    # 等待线程完成
    thread1.join()
    thread2.join()
    
    print("所有线程完成\n")
    
    # 创建和启动线程的方式2：继承Thread类
    class WorkerThread(threading.Thread):
        """工作线程类"""
        
        def __init__(self, name, duration):
            super().__init__()
            self.name = name
            self.duration = duration
        
        def run(self):
            """线程执行方法"""
            print(f"类线程 {self.name} 开始工作")
            for i in range(2):
                print(f"  {self.name}: 执行任务 {i+1}")
                time.sleep(self.duration)
            print(f"类线程 {self.name} 完成")
    
    print("方式2: 继承Thread类")
    worker_thread1 = WorkerThread("ClassWorker-1", 0.4)
    worker_thread2 = WorkerThread("ClassWorker-2", 0.6)
    
    worker_thread1.start()
    worker_thread2.start()
    
    worker_thread1.join()
    worker_thread2.join()
    
    # 线程属性和方法
    print(f"\n线程属性:")
    current_thread = threading.current_thread()
    print(f"当前线程名称: {current_thread.name}")
    print(f"当前线程ID: {current_thread.ident}")
    print(f"活跃线程数: {threading.active_count()}")
    print(f"所有线程: {[t.name for t in threading.enumerate()]}")
    
    """
    Java等价实现:
    
    // 方式1: 实现Runnable接口
    public class Worker implements Runnable {
        private String name;
        private int duration;
        
        public Worker(String name, int duration) {
            this.name = name;
            this.duration = duration;
        }
        
        @Override
        public void run() {
            System.out.println("线程 " + name + " 开始工作");
            for (int i = 0; i < 3; i++) {
                System.out.println(name + ": 正在执行任务 " + (i+1));
                try { Thread.sleep(duration); } catch (InterruptedException e) {}
            }
            System.out.println("线程 " + name + " 工作完成");
        }
    }
    
    // 创建和启动线程
    Thread thread1 = new Thread(new Worker("Worker-1", 500));
    Thread thread2 = new Thread(new Worker("Worker-2", 300));
    
    thread1.start();
    thread2.start();
    
    thread1.join();
    thread2.join();
    
    // 方式2: 继承Thread类
    public class WorkerThread extends Thread {
        private String workerName;
        private int duration;
        
        public WorkerThread(String name, int duration) {
            this.workerName = name;
            this.duration = duration;
        }
        
        @Override
        public void run() {
            // 执行逻辑同上
        }
    }
    """
    
    print()


def demo_thread_synchronization():
    """演示线程同步机制"""
    print("=== 2. 线程同步机制 ===")
    
    # 1. Lock（互斥锁）
    print("1. Lock（互斥锁）演示:")
    
    shared_resource = 0
    resource_lock = Lock()
    
    def increment_with_lock(name, times):
        """使用锁的增量函数"""
        global shared_resource
        for i in range(times):
            with resource_lock:  # 使用with语句自动加锁/解锁
                temp = shared_resource
                print(f"  {name}: 读取值 {temp}")
                time.sleep(0.01)  # 模拟处理时间
                shared_resource = temp + 1
                print(f"  {name}: 写入值 {shared_resource}")
    
    # 不使用锁的版本（可能出现竞态条件）
    def increment_without_lock(name, times):
        """不使用锁的增量函数"""
        global shared_resource
        for i in range(times):
            temp = shared_resource
            time.sleep(0.01)
            shared_resource = temp + 1
    
    # 使用锁的线程
    shared_resource = 0
    lock_thread1 = threading.Thread(target=increment_with_lock, args=("LockThread1", 3))
    lock_thread2 = threading.Thread(target=increment_with_lock, args=("LockThread2", 3))
    
    lock_thread1.start()
    lock_thread2.start()
    lock_thread1.join()
    lock_thread2.join()
    
    print(f"使用锁的最终值: {shared_resource}")
    
    # 2. RLock（可重入锁）
    print(f"\n2. RLock（可重入锁）演示:")
    
    rlock = RLock()
    
    def recursive_function(name, depth):
        """递归函数需要可重入锁"""
        with rlock:
            print(f"  {name}: 进入深度 {depth}")
            if depth > 0:
                recursive_function(name, depth - 1)
            print(f"  {name}: 退出深度 {depth}")
    
    rlock_thread = threading.Thread(target=recursive_function, args=("RLockThread", 3))
    rlock_thread.start()
    rlock_thread.join()
    
    # 3. Condition（条件变量）
    print(f"\n3. Condition（条件变量）演示:")
    
    items = []
    condition = Condition()
    
    def consumer(name):
        """消费者"""
        with condition:
            while len(items) == 0:
                print(f"  {name}: 等待物品...")
                condition.wait()  # 等待条件满足
            item = items.pop(0)
            print(f"  {name}: 消费了 {item}")
    
    def producer(name):
        """生产者"""
        for i in range(3):
            with condition:
                item = f"{name}-Item{i}"
                items.append(item)
                print(f"  {name}: 生产了 {item}")
                condition.notify()  # 通知等待的线程
            time.sleep(0.1)
    
    consumer_thread = threading.Thread(target=consumer, args=("Consumer",))
    producer_thread = threading.Thread(target=producer, args=("Producer",))
    
    consumer_thread.start()
    time.sleep(0.1)  # 确保消费者先启动
    producer_thread.start()
    
    consumer_thread.join()
    producer_thread.join()
    
    # 4. Semaphore（信号量）
    print(f"\n4. Semaphore（信号量）演示:")
    
    # 限制同时访问资源的线程数量
    resource_semaphore = Semaphore(2)  # 最多2个线程同时访问
    
    def access_resource(name):
        """访问受限资源"""
        print(f"  {name}: 请求访问资源")
        with resource_semaphore:
            print(f"  {name}: 获得资源访问权")
            time.sleep(random.uniform(0.5, 1.0))  # 模拟使用资源
            print(f"  {name}: 释放资源")
    
    # 创建多个线程尝试访问资源
    semaphore_threads = []
    for i in range(5):
        thread = threading.Thread(target=access_resource, args=(f"Thread{i}",))
        semaphore_threads.append(thread)
        thread.start()
    
    for thread in semaphore_threads:
        thread.join()
    
    # 5. Event（事件）
    print(f"\n5. Event（事件）演示:")
    
    ready_event = Event()
    
    def waiter(name):
        """等待者"""
        print(f"  {name}: 等待事件...")
        ready_event.wait()  # 等待事件被设置
        print(f"  {name}: 事件发生，开始工作!")
    
    def setter():
        """事件设置者"""
        print("  Setter: 准备设置事件...")
        time.sleep(2)
        ready_event.set()  # 设置事件
        print("  Setter: 事件已设置!")
    
    waiter_threads = [
        threading.Thread(target=waiter, args=(f"Waiter{i}",))
        for i in range(3)
    ]
    setter_thread = threading.Thread(target=setter)
    
    for thread in waiter_threads:
        thread.start()
    
    setter_thread.start()
    
    for thread in waiter_threads:
        thread.join()
    setter_thread.join()
    
    """
    Java线程同步等价实现:
    
    // 1. synchronized关键字（类似Python的Lock）
    private final Object lock = new Object();
    
    public void incrementWithLock() {
        synchronized(lock) {
            // 临界区代码
            int temp = sharedResource;
            sharedResource = temp + 1;
        }
    }
    
    // 2. ReentrantLock（可重入锁）
    private final ReentrantLock rlock = new ReentrantLock();
    
    public void recursiveFunction(int depth) {
        rlock.lock();
        try {
            if (depth > 0) {
                recursiveFunction(depth - 1);
            }
        } finally {
            rlock.unlock();
        }
    }
    
    // 3. Condition
    private final ReentrantLock lock = new ReentrantLock();
    private final Condition condition = lock.newCondition();
    
    public void consumer() throws InterruptedException {
        lock.lock();
        try {
            while (items.isEmpty()) {
                condition.await();
            }
            Item item = items.remove(0);
        } finally {
            lock.unlock();
        }
    }
    
    public void producer() {
        lock.lock();
        try {
            items.add(new Item());
            condition.signal();
        } finally {
            lock.unlock();
        }
    }
    
    // 4. Semaphore
    private final Semaphore semaphore = new Semaphore(2);
    
    public void accessResource() throws InterruptedException {
        semaphore.acquire();
        try {
            // 访问资源
        } finally {
            semaphore.release();
        }
    }
    
    // 5. CountDownLatch（类似Event）
    private final CountDownLatch latch = new CountDownLatch(1);
    
    public void waiter() throws InterruptedException {
        latch.await();
        // 开始工作
    }
    
    public void setter() {
        latch.countDown();
    }
    """
    
    print()


def demo_thread_pool():
    """演示线程池"""
    print("=== 3. 线程池演示 ===")
    
    # 1. ThreadPoolExecutor基本用法
    print("1. ThreadPoolExecutor基本用法:")
    
    def cpu_bound_task(n):
        """CPU密集型任务（受GIL影响）"""
        result = 0
        for i in range(n):
            result += i ** 2
        return result
    
    def io_bound_task(duration):
        """I/O密集型任务"""
        start_time = time.time()
        time.sleep(duration)  # 模拟I/O等待
        end_time = time.time()
        return f"任务完成，耗时: {end_time - start_time:.2f}秒"
    
    # I/O密集型任务适合多线程
    print("I/O密集型任务测试:")
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 提交任务
        tasks = [0.5, 1.0, 0.3, 0.8, 0.6]
        futures = [executor.submit(io_bound_task, duration) for duration in tasks]
        
        # 获取结果
        for i, future in enumerate(futures):
            result = future.result()
            print(f"  任务{i+1}: {result}")
    
    # 2. map方法
    print(f"\n2. 使用map方法:")
    
    def process_number(n):
        """处理数字"""
        time.sleep(0.1)  # 模拟I/O
        return n ** 2
    
    numbers = [1, 2, 3, 4, 5]
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(process_number, numbers))
        print(f"  处理结果: {dict(zip(numbers, results))}")
    
    # 3. as_completed获取最先完成的任务
    print(f"\n3. as_completed - 获取最先完成的任务:")
    
    def random_task(task_id):
        """随机耗时任务"""
        duration = random.uniform(0.1, 1.0)
        time.sleep(duration)
        return f"任务{task_id}完成，耗时{duration:.2f}秒"
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 提交多个任务
        future_to_id = {
            executor.submit(random_task, i): i 
            for i in range(5)
        }
        
        # 按完成顺序获取结果
        for future in as_completed(future_to_id):
            task_id = future_to_id[future]
            try:
                result = future.result()
                print(f"  {result}")
            except Exception as e:
                print(f"  任务{task_id}失败: {e}")
    
    # 4. 线程池异常处理
    print(f"\n4. 异常处理:")
    
    def unreliable_task(task_id):
        """不可靠任务"""
        if random.random() < 0.3:  # 30%失败率
            raise Exception(f"任务{task_id}随机失败")
        time.sleep(0.2)
        return f"任务{task_id}成功完成"
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(unreliable_task, i) for i in range(6)]
        
        for i, future in enumerate(futures):
            try:
                result = future.result(timeout=1.0)
                print(f"  ✅ {result}")
            except Exception as e:
                print(f"  ❌ 任务{i}失败: {e}")
    
    """
    Java线程池等价实现:
    
    // 1. ExecutorService
    ExecutorService executor = Executors.newFixedThreadPool(4);
    
    // 提交任务
    List<Future<String>> futures = new ArrayList<>();
    for (double duration : Arrays.asList(0.5, 1.0, 0.3, 0.8, 0.6)) {
        Future<String> future = executor.submit(() -> {
            Thread.sleep((long)(duration * 1000));
            return "任务完成，耗时: " + duration + "秒";
        });
        futures.add(future);
    }
    
    // 获取结果
    for (int i = 0; i < futures.size(); i++) {
        try {
            String result = futures.get(i).get();
            System.out.println("任务" + (i+1) + ": " + result);
        } catch (Exception e) {
            System.out.println("任务" + (i+1) + "失败: " + e.getMessage());
        }
    }
    
    executor.shutdown();
    
    // 2. CompletableFuture异步处理
    List<CompletableFuture<String>> futures = numbers.stream()
        .map(n -> CompletableFuture.supplyAsync(() -> {
            try { Thread.sleep(100); } catch (InterruptedException e) {}
            return n * n;
        }))
        .collect(Collectors.toList());
    
    // 等待所有完成
    CompletableFuture<Void> allOf = CompletableFuture.allOf(
        futures.toArray(new CompletableFuture[0])
    );
    
    allOf.join();
    
    // 3. 获取最先完成的任务
    CompletableFuture<Object> anyOf = CompletableFuture.anyOf(
        futures.toArray(new CompletableFuture[0])
    );
    
    Object firstResult = anyOf.join();
    """
    
    print()


def demo_producer_consumer():
    """演示生产者-消费者模式"""
    print("=== 4. 生产者-消费者模式 ===")
    
    # 使用queue模块实现线程安全的队列
    task_queue = queue.Queue(maxsize=3)  # 限制队列大小
    
    def producer(name, item_count):
        """生产者"""
        for i in range(item_count):
            item = f"{name}-产品{i}"
            try:
                task_queue.put(item, timeout=2)  # 2秒超时
                print(f"  🏭 {name}: 生产了 {item}")
                time.sleep(random.uniform(0.1, 0.5))
            except queue.Full:
                print(f"  ⚠️  {name}: 队列已满，放弃生产 {item}")
        
        print(f"  ✅ {name}: 生产完成")
    
    def consumer(name, consume_count):
        """消费者"""
        consumed = 0
        while consumed < consume_count:
            try:
                item = task_queue.get(timeout=3)  # 3秒超时
                print(f"  🛒 {name}: 消费了 {item}")
                time.sleep(random.uniform(0.2, 0.8))  # 模拟消费时间
                task_queue.task_done()  # 标记任务完成
                consumed += 1
            except queue.Empty:
                print(f"  ⏰ {name}: 等待超时，停止消费")
                break
        
        print(f"  ✅ {name}: 消费完成，共消费{consumed}个")
    
    # 创建生产者和消费者线程
    producer1 = threading.Thread(target=producer, args=("生产者1", 5))
    producer2 = threading.Thread(target=producer, args=("生产者2", 3))
    consumer1 = threading.Thread(target=consumer, args=("消费者1", 4))
    consumer2 = threading.Thread(target=consumer, args=("消费者2", 4))
    
    # 启动所有线程
    producer1.start()
    producer2.start()
    consumer1.start()
    consumer2.start()
    
    # 等待生产者完成
    producer1.join()
    producer2.join()
    
    # 等待队列中的所有任务完成
    task_queue.join()
    
    print(f"  📊 队列状态: 剩余{task_queue.qsize()}个未消费")
    
    # 消费者可能还在等待，需要优雅关闭
    consumer1.join(timeout=1)
    consumer2.join(timeout=1)
    
    # 优先级队列示例
    print(f"\n优先级队列示例:")
    
    priority_queue = queue.PriorityQueue()
    
    # 添加任务（优先级，任务描述）
    tasks = [
        (3, "低优先级任务"),
        (1, "高优先级任务"),
        (2, "中优先级任务"),
        (1, "另一个高优先级任务")
    ]
    
    for priority, task in tasks:
        priority_queue.put((priority, task))
    
    print("  按优先级处理任务:")
    while not priority_queue.empty():
        priority, task = priority_queue.get()
        print(f"    优先级{priority}: {task}")
    
    # LIFO队列（栈）示例
    print(f"\nLIFO队列（栈）示例:")
    
    lifo_queue = queue.LifoQueue()
    
    # 添加任务
    for i in range(5):
        task = f"任务{i}"
        lifo_queue.put(task)
        print(f"  入栈: {task}")
    
    print("  出栈顺序:")
    while not lifo_queue.empty():
        task = lifo_queue.get()
        print(f"    出栈: {task}")
    
    """
    Java生产者-消费者等价实现:
    
    // 使用BlockingQueue
    BlockingQueue<String> queue = new ArrayBlockingQueue<>(3);
    
    // 生产者
    public class Producer implements Runnable {
        @Override
        public void run() {
            try {
                for (int i = 0; i < 5; i++) {
                    String item = "产品" + i;
                    queue.put(item); // 阻塞直到有空间
                    System.out.println("生产了: " + item);
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    // 消费者
    public class Consumer implements Runnable {
        @Override
        public void run() {
            try {
                while (true) {
                    String item = queue.take(); // 阻塞直到有元素
                    System.out.println("消费了: " + item);
                    Thread.sleep(200);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    // 优先级队列
    PriorityBlockingQueue<Task> priorityQueue = new PriorityBlockingQueue<>();
    
    public class Task implements Comparable<Task> {
        private int priority;
        private String description;
        
        @Override
        public int compareTo(Task other) {
            return Integer.compare(this.priority, other.priority);
        }
    }
    """
    
    print()


def demo_thread_local():
    """演示线程本地存储"""
    print("=== 5. 线程本地存储 ===")
    
    # 创建线程本地存储
    thread_local_data = threading.local()
    
    def process_data(thread_id):
        """处理数据的函数"""
        # 为当前线程设置本地数据
        thread_local_data.user_id = f"user_{thread_id}"
        thread_local_data.session_token = f"token_{thread_id}_{random.randint(1000, 9999)}"
        thread_local_data.request_count = 0
        
        print(f"  线程{thread_id}: 初始化本地数据")
        print(f"    用户ID: {thread_local_data.user_id}")
        print(f"    会话令牌: {thread_local_data.session_token}")
        
        # 模拟处理多个请求
        for request_num in range(3):
            thread_local_data.request_count += 1
            
            # 模拟业务处理
            time.sleep(random.uniform(0.1, 0.3))
            
            print(f"  线程{thread_id}: 处理请求{request_num + 1}")
            print(f"    当前用户: {thread_local_data.user_id}")
            print(f"    请求计数: {thread_local_data.request_count}")
    
    # 创建多个线程，每个都有自己的本地数据
    threads = []
    for i in range(3):
        thread = threading.Thread(target=process_data, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # 线程本地存储的实际应用示例
    print(f"\n实际应用示例 - 数据库连接管理:")
    
    class DatabaseManager:
        """数据库管理器"""
        
        def __init__(self):
            self.local = threading.local()
        
        def get_connection(self):
            """获取线程本地数据库连接"""
            if not hasattr(self.local, 'connection'):
                # 为当前线程创建连接
                thread_name = threading.current_thread().name
                self.local.connection = f"DB_Connection_{thread_name}_{random.randint(100, 999)}"
                print(f"    创建新连接: {self.local.connection}")
            
            return self.local.connection
        
        def execute_query(self, query):
            """执行查询"""
            connection = self.get_connection()
            thread_name = threading.current_thread().name
            print(f"    {thread_name}: 使用连接 {connection} 执行查询: {query}")
            time.sleep(0.1)  # 模拟查询时间
            return f"查询结果_{random.randint(1, 100)}"
    
    db_manager = DatabaseManager()
    
    def database_worker(worker_id):
        """数据库工作线程"""
        print(f"  工作线程{worker_id}开始")
        
        for i in range(2):
            query = f"SELECT * FROM table_{i}"
            result = db_manager.execute_query(query)
            print(f"    工作线程{worker_id}: {result}")
            time.sleep(0.1)
        
        print(f"  工作线程{worker_id}完成")
    
    # 创建数据库工作线程
    db_threads = []
    for i in range(3):
        thread = threading.Thread(target=database_worker, args=(i,), name=f"DBWorker-{i}")
        db_threads.append(thread)
        thread.start()
    
    for thread in db_threads:
        thread.join()
    
    """
    Java线程本地存储等价实现:
    
    // ThreadLocal
    private static final ThreadLocal<String> userContext = new ThreadLocal<>();
    private static final ThreadLocal<String> sessionToken = new ThreadLocal<>();
    private static final ThreadLocal<Integer> requestCount = new ThreadLocal<Integer>() {
        @Override
        protected Integer initialValue() {
            return 0;
        }
    };
    
    public void processData(int threadId) {
        // 设置线程本地数据
        userContext.set("user_" + threadId);
        sessionToken.set("token_" + threadId + "_" + new Random().nextInt(9999));
        
        for (int i = 0; i < 3; i++) {
            requestCount.set(requestCount.get() + 1);
            
            System.out.println("线程" + threadId + ": 处理请求" + (i+1));
            System.out.println("当前用户: " + userContext.get());
            System.out.println("请求计数: " + requestCount.get());
        }
        
        // 清理线程本地数据（重要！）
        userContext.remove();
        sessionToken.remove();
        requestCount.remove();
    }
    
    // 数据库连接管理
    public class DatabaseManager {
        private static final ThreadLocal<Connection> connectionHolder = new ThreadLocal<>();
        
        public Connection getConnection() {
            Connection conn = connectionHolder.get();
            if (conn == null) {
                conn = createNewConnection();
                connectionHolder.set(conn);
            }
            return conn;
        }
        
        public void cleanup() {
            Connection conn = connectionHolder.get();
            if (conn != null) {
                try { conn.close(); } catch (SQLException e) {}
                connectionHolder.remove();
            }
        }
    }
    """
    
    print()


def demo_gil_impact():
    """演示GIL的影响"""
    print("=== 6. GIL影响演示 ===")
    
    import multiprocessing
    
    def cpu_intensive_task(n):
        """CPU密集型任务"""
        total = 0
        for i in range(n):
            total += i ** 2
        return total
    
    def io_intensive_task(duration):
        """I/O密集型任务"""
        time.sleep(duration)
        return f"IO任务完成，耗时{duration}秒"
    
    # 测试CPU密集型任务
    print("CPU密集型任务测试:")
    
    # 单线程
    start_time = time.time()
    results = [cpu_intensive_task(100000) for _ in range(4)]
    single_thread_time = time.time() - start_time
    print(f"  单线程时间: {single_thread_time:.4f}秒")
    
    # 多线程（受GIL影响）
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_intensive_task, 100000) for _ in range(4)]
        results = [future.result() for future in futures]
    multi_thread_time = time.time() - start_time
    print(f"  多线程时间: {multi_thread_time:.4f}秒")
    print(f"  多线程效率: {single_thread_time/multi_thread_time:.2f}x")
    
    # 测试I/O密集型任务
    print(f"\nI/O密集型任务测试:")
    
    # 单线程
    start_time = time.time()
    results = [io_intensive_task(0.2) for _ in range(4)]
    single_thread_io_time = time.time() - start_time
    print(f"  单线程时间: {single_thread_io_time:.4f}秒")
    
    # 多线程（不受GIL影响）
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(io_intensive_task, 0.2) for _ in range(4)]
        results = [future.result() for future in futures]
    multi_thread_io_time = time.time() - start_time
    print(f"  多线程时间: {multi_thread_io_time:.4f}秒")
    print(f"  多线程效率: {single_thread_io_time/multi_thread_io_time:.2f}x")
    
    print(f"\nGIL影响总结:")
    print(f"  - CPU密集型：多线程效率 {single_thread_time/multi_thread_time:.2f}x（受GIL限制）")
    print(f"  - I/O密集型：多线程效率 {single_thread_io_time/multi_thread_io_time:.2f}x（GIL释放）")
    print(f"  - 建议：CPU密集型使用多进程，I/O密集型使用多线程")
    
    """
    Java GIL对比说明:
    
    Java没有GIL限制，所以：
    1. CPU密集型任务可以真正并行执行
    2. 多线程在多核CPU上有明显性能提升
    3. 但需要更仔细的同步控制
    
    // Java多线程CPU密集型任务
    ExecutorService executor = Executors.newFixedThreadPool(4);
    
    // 提交CPU密集型任务
    List<Future<Integer>> futures = new ArrayList<>();
    for (int i = 0; i < 4; i++) {
        futures.add(executor.submit(() -> {
            int total = 0;
            for (int j = 0; j < 100000; j++) {
                total += j * j;
            }
            return total;
        }));
    }
    
    // 在Java中，这4个任务可以真正并行执行
    // 而在Python中，由于GIL，实际上是串行执行的
    """
    
    print()


def main():
    """主函数：运行所有演示"""
    print("Python多线程编程完整学习指南")
    print("=" * 50)
    
    demo_basic_threading()
    demo_thread_synchronization()
    demo_thread_pool()
    demo_producer_consumer()
    demo_thread_local()
    demo_gil_impact()
    
    print("学习总结:")
    print("1. Python threading模块提供完整的多线程支持")
    print("2. 丰富的同步原语：Lock、RLock、Condition、Semaphore、Event")
    print("3. ThreadPoolExecutor简化线程池管理")
    print("4. queue模块提供线程安全的队列实现")
    print("5. threading.local实现线程本地存储")
    print("6. GIL限制CPU密集型任务的并行性，但不影响I/O密集型任务")
    print("7. Java多线程无GIL限制，但同步机制更复杂")
    print("8. 选择原则：I/O密集型用多线程，CPU密集型用多进程")


if __name__ == "__main__":
    main() 