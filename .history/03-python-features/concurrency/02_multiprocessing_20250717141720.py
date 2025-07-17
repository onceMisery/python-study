#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python多进程编程详解
Multiprocessing in Python

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习Python multiprocessing模块、进程间通信和并行计算优化

学习目标:
1. 掌握Python multiprocessing模块的基本使用
2. 理解进程间通信机制（IPC）
3. 学会并行计算和性能优化
4. 对比多线程和多进程的适用场景

注意：多进程适用于CPU密集型任务，可以绕过GIL限制
"""

import multiprocessing as mp
import time
import random
import os
import math
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Process, Queue, Pipe, Value, Array, Manager
from multiprocessing import Lock, RLock, Condition, Semaphore, Event
import pickle


def demo_basic_multiprocessing():
    """演示基本多进程操作"""
    print("=== 1. 基本多进程操作 ===")
    
    # 简单的进程函数
    def worker_process(name, duration):
        """工作进程函数"""
        pid = os.getpid()
        print(f"进程 {name} (PID: {pid}) 开始工作")
        
        for i in range(3):
            print(f"  {name}: 正在执行任务 {i+1}")
            time.sleep(duration)
        
        print(f"进程 {name} (PID: {pid}) 工作完成")
        return f"{name}_完成"
    
    # 创建和启动进程的方式1：使用函数
    print("方式1: 使用函数创建进程")
    
    if __name__ == '__main__':  # 在Windows上必须使用这个保护
        process1 = Process(target=worker_process, args=("Worker-1", 0.5))
        process2 = Process(target=worker_process, args=("Worker-2", 0.3))
        
        print(f"主进程 PID: {os.getpid()}")
        
        # 启动进程
        process1.start()
        process2.start()
        
        # 等待进程完成
        process1.join()
        process2.join()
        
        print("所有进程完成\n")
    
    # 创建和启动进程的方式2：继承Process类
    class WorkerProcess(Process):
        """工作进程类"""
        
        def __init__(self, name, duration):
            super().__init__()
            self.worker_name = name
            self.duration = duration
        
        def run(self):
            """进程执行方法"""
            pid = os.getpid()
            print(f"类进程 {self.worker_name} (PID: {pid}) 开始工作")
            
            for i in range(2):
                print(f"  {self.worker_name}: 执行任务 {i+1}")
                time.sleep(self.duration)
            
            print(f"类进程 {self.worker_name} (PID: {pid}) 完成")
    
    print("方式2: 继承Process类")
    if __name__ == '__main__':
        worker_proc1 = WorkerProcess("ClassWorker-1", 0.4)
        worker_proc2 = WorkerProcess("ClassWorker-2", 0.6)
        
        worker_proc1.start()
        worker_proc2.start()
        
        worker_proc1.join()
        worker_proc2.join()
    
    # 进程属性和方法
    print(f"\n进程属性:")
    current_process = mp.current_process()
    print(f"当前进程名称: {current_process.name}")
    print(f"当前进程PID: {current_process.pid}")
    print(f"CPU核心数: {mp.cpu_count()}")
    
    """
    Java等价实现:
    
    // Java中没有直接的多进程API，通常使用ProcessBuilder或Runtime.exec()
    public class ProcessExample {
        
        public void createProcess() throws IOException, InterruptedException {
            // 创建新的Java进程
            ProcessBuilder pb = new ProcessBuilder(
                "java", "-cp", ".", "WorkerProcess", "Worker-1", "500"
            );
            
            Process process = pb.start();
            
            // 等待进程完成
            int exitCode = process.waitFor();
            System.out.println("进程退出码: " + exitCode);
        }
        
        // 或者使用ExecutorService在同一JVM内并行执行
        public void parallelExecution() {
            ForkJoinPool commonPool = ForkJoinPool.commonPool();
            
            CompletableFuture<Void> task1 = CompletableFuture.runAsync(() -> {
                workerTask("Worker-1", 500);
            }, commonPool);
            
            CompletableFuture<Void> task2 = CompletableFuture.runAsync(() -> {
                workerTask("Worker-2", 300);
            }, commonPool);
            
            CompletableFuture.allOf(task1, task2).join();
        }
        
        private void workerTask(String name, int duration) {
            System.out.println("任务 " + name + " 开始执行");
            try { Thread.sleep(duration); } catch (InterruptedException e) {}
            System.out.println("任务 " + name + " 完成");
        }
    }
    
    // 对于CPU密集型任务，Java可以使用ForkJoinPool
    public class CPUIntensiveTask extends RecursiveTask<Integer> {
        private final int[] array;
        private final int start, end;
        
        @Override
        protected Integer compute() {
            if (end - start <= THRESHOLD) {
                // 直接计算
                return computeDirectly();
            } else {
                // 分割任务
                int mid = (start + end) / 2;
                CPUIntensiveTask left = new CPUIntensiveTask(array, start, mid);
                CPUIntensiveTask right = new CPUIntensiveTask(array, mid, end);
                
                left.fork(); // 异步执行左半部分
                int rightResult = right.compute(); // 同步执行右半部分
                int leftResult = left.join(); // 等待左半部分完成
                
                return leftResult + rightResult;
            }
        }
    }
    """
    
    print()


def demo_process_communication():
    """演示进程间通信"""
    print("=== 2. 进程间通信 ===")
    
    # 1. Queue（队列）通信
    print("1. Queue队列通信:")
    
    def producer(queue, name, count):
        """生产者进程"""
        for i in range(count):
            item = f"{name}-产品{i}"
            queue.put(item)
            print(f"  🏭 {name}: 生产了 {item}")
            time.sleep(random.uniform(0.1, 0.3))
        
        queue.put(None)  # 结束信号
        print(f"  ✅ {name}: 生产完成")
    
    def consumer(queue, name):
        """消费者进程"""
        consumed_count = 0
        while True:
            item = queue.get()
            if item is None:
                queue.put(None)  # 传递结束信号给其他消费者
                break
            
            print(f"  🛒 {name}: 消费了 {item}")
            consumed_count += 1
            time.sleep(random.uniform(0.2, 0.4))
        
        print(f"  ✅ {name}: 消费完成，共消费{consumed_count}个")
    
    if __name__ == '__main__':
        # 创建队列
        task_queue = Queue()
        
        # 创建进程
        producer_proc = Process(target=producer, args=(task_queue, "生产者", 5))
        consumer_proc1 = Process(target=consumer, args=(task_queue, "消费者1"))
        consumer_proc2 = Process(target=consumer, args=(task_queue, "消费者2"))
        
        # 启动进程
        producer_proc.start()
        consumer_proc1.start()
        consumer_proc2.start()
        
        # 等待完成
        producer_proc.join()
        consumer_proc1.join()
        consumer_proc2.join()
    
    # 2. Pipe（管道）通信
    print(f"\n2. Pipe管道通信:")
    
    def sender(conn, messages):
        """发送进程"""
        for msg in messages:
            conn.send(msg)
            print(f"  📤 发送: {msg}")
            time.sleep(0.2)
        
        conn.send("END")  # 结束信号
        conn.close()
    
    def receiver(conn):
        """接收进程"""
        while True:
            msg = conn.recv()
            if msg == "END":
                break
            print(f"  📥 接收: {msg}")
        
        conn.close()
    
    if __name__ == '__main__':
        # 创建管道
        parent_conn, child_conn = Pipe()
        
        messages = ["消息1", "消息2", "消息3", "消息4"]
        
        # 创建进程
        sender_proc = Process(target=sender, args=(child_conn, messages))
        receiver_proc = Process(target=receiver, args=(parent_conn,))
        
        # 启动进程
        sender_proc.start()
        receiver_proc.start()
        
        # 等待完成
        sender_proc.join()
        receiver_proc.join()
    
    # 3. 共享内存
    print(f"\n3. 共享内存:")
    
    def worker_with_shared_value(shared_val, lock, worker_id):
        """使用共享值的工作进程"""
        for i in range(3):
            with lock:
                old_val = shared_val.value
                time.sleep(0.01)  # 模拟处理时间
                shared_val.value = old_val + 1
                print(f"  工作进程{worker_id}: {old_val} -> {shared_val.value}")
    
    def worker_with_shared_array(shared_arr, lock, worker_id):
        """使用共享数组的工作进程"""
        with lock:
            for i in range(len(shared_arr)):
                shared_arr[i] += worker_id
            print(f"  进程{worker_id}: 数组更新完成")
    
    if __name__ == '__main__':
        # 共享值
        shared_value = Value('i', 0)  # 'i'表示整数类型
        value_lock = Lock()
        
        # 共享数组
        shared_array = Array('d', [1.0, 2.0, 3.0, 4.0])  # 'd'表示double类型
        array_lock = Lock()
        
        print("  共享值测试:")
        value_processes = []
        for i in range(3):
            proc = Process(target=worker_with_shared_value, 
                          args=(shared_value, value_lock, i))
            value_processes.append(proc)
            proc.start()
        
        for proc in value_processes:
            proc.join()
        
        print(f"  最终共享值: {shared_value.value}")
        
        print("  共享数组测试:")
        array_processes = []
        for i in range(2):
            proc = Process(target=worker_with_shared_array, 
                          args=(shared_array, array_lock, i+1))
            array_processes.append(proc)
            proc.start()
        
        for proc in array_processes:
            proc.join()
        
        print(f"  最终共享数组: {list(shared_array[:])}")
    
    # 4. Manager（管理器）
    print(f"\n4. Manager管理器:")
    
    def worker_with_manager(shared_dict, shared_list, worker_id):
        """使用管理器的工作进程"""
        # 更新共享字典
        shared_dict[f'worker_{worker_id}'] = f'进程{worker_id}的数据'
        
        # 更新共享列表
        shared_list.append(f'来自进程{worker_id}')
        
        print(f"  进程{worker_id}: 更新共享数据完成")
    
    if __name__ == '__main__':
        with Manager() as manager:
            # 创建管理器对象
            shared_dict = manager.dict()
            shared_list = manager.list()
            
            # 初始化数据
            shared_dict['初始'] = '初始值'
            shared_list.append('初始项目')
            
            # 创建工作进程
            manager_processes = []
            for i in range(3):
                proc = Process(target=worker_with_manager, 
                              args=(shared_dict, shared_list, i))
                manager_processes.append(proc)
                proc.start()
            
            for proc in manager_processes:
                proc.join()
            
            print(f"  最终共享字典: {dict(shared_dict)}")
            print(f"  最终共享列表: {list(shared_list)}")
    
    """
    Java进程间通信等价实现:
    
    // Java主要使用以下方式进行进程间通信：
    
    // 1. 套接字通信
    public class SocketIPC {
        // 服务器进程
        public void serverProcess() throws IOException {
            ServerSocket serverSocket = new ServerSocket(8080);
            Socket clientSocket = serverSocket.accept();
            
            BufferedReader in = new BufferedReader(
                new InputStreamReader(clientSocket.getInputStream())
            );
            PrintWriter out = new PrintWriter(
                clientSocket.getOutputStream(), true
            );
            
            String inputLine = in.readLine();
            out.println("Echo: " + inputLine);
        }
        
        // 客户端进程
        public void clientProcess() throws IOException {
            Socket socket = new Socket("localhost", 8080);
            
            PrintWriter out = new PrintWriter(
                socket.getOutputStream(), true
            );
            BufferedReader in = new BufferedReader(
                new InputStreamReader(socket.getInputStream())
            );
            
            out.println("Hello Server");
            String response = in.readLine();
            System.out.println("服务器响应: " + response);
        }
    }
    
    // 2. 文件映射（内存映射文件）
    public class MemoryMappedFileIPC {
        public void writeProcess() throws IOException {
            RandomAccessFile file = new RandomAccessFile("shared.dat", "rw");
            MappedByteBuffer buffer = file.getChannel().map(
                FileChannel.MapMode.READ_WRITE, 0, 1024
            );
            
            buffer.put("Hello from Process 1".getBytes());
            file.close();
        }
        
        public void readProcess() throws IOException {
            RandomAccessFile file = new RandomAccessFile("shared.dat", "r");
            MappedByteBuffer buffer = file.getChannel().map(
                FileChannel.MapMode.READ_ONLY, 0, 1024
            );
            
            byte[] data = new byte[21];
            buffer.get(data);
            System.out.println("读取到: " + new String(data));
            file.close();
        }
    }
    
    // 3. JVM内共享（不是真正的进程间通信，但可以在同一JVM内共享）
    public class SharedMemoryExample {
        private static final List<String> sharedList = 
            Collections.synchronizedList(new ArrayList<>());
        
        private static final Map<String, String> sharedMap = 
            new ConcurrentHashMap<>();
    }
    """
    
    print()


def demo_process_pool():
    """演示进程池"""
    print("=== 3. 进程池演示 ===")
    
    # CPU密集型任务
    def cpu_intensive_task(n):
        """CPU密集型任务 - 计算质数"""
        def is_prime(num):
            if num < 2:
                return False
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    return False
            return True
        
        primes = [i for i in range(2, n) if is_prime(i)]
        return len(primes)
    
    def fibonacci(n):
        """斐波那契数列计算"""
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    # 1. ProcessPoolExecutor基本用法
    print("1. ProcessPoolExecutor基本用法:")
    
    tasks = [1000, 2000, 1500, 3000, 2500]
    
    # 单进程执行
    start_time = time.time()
    single_results = [cpu_intensive_task(n) for n in tasks]
    single_time = time.time() - start_time
    print(f"  单进程时间: {single_time:.4f}秒")
    print(f"  结果: {single_results}")
    
    # 多进程执行
    if __name__ == '__main__':
        start_time = time.time()
        with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
            multi_results = list(executor.map(cpu_intensive_task, tasks))
        multi_time = time.time() - start_time
        
        print(f"  多进程时间: {multi_time:.4f}秒")
        print(f"  结果: {multi_results}")
        print(f"  性能提升: {single_time/multi_time:.2f}x")
    
    # 2. submit方法和Future对象
    print(f"\n2. submit方法和Future:")
    
    fib_numbers = [30, 32, 34, 31, 33]
    
    if __name__ == '__main__':
        with ProcessPoolExecutor(max_workers=4) as executor:
            # 提交任务
            future_to_number = {
                executor.submit(fibonacci, n): n 
                for n in fib_numbers
            }
            
            # 按完成顺序获取结果
            print("  按完成顺序获取斐波那契结果:")
            for future in as_completed(future_to_number):
                number = future_to_number[future]
                try:
                    result = future.result()
                    print(f"    fibonacci({number}) = {result}")
                except Exception as e:
                    print(f"    fibonacci({number}) 计算失败: {e}")
    
    # 3. 处理大数据集
    print(f"\n3. 大数据集处理:")
    
    def process_chunk(chunk):
        """处理数据块"""
        return sum(x**2 for x in chunk)
    
    # 生成大数据集
    large_dataset = list(range(100000))
    chunk_size = 10000
    chunks = [large_dataset[i:i+chunk_size] 
              for i in range(0, len(large_dataset), chunk_size)]
    
    print(f"  数据集大小: {len(large_dataset)}")
    print(f"  分块数量: {len(chunks)}")
    
    if __name__ == '__main__':
        # 单进程处理
        start_time = time.time()
        single_result = sum(process_chunk(chunk) for chunk in chunks)
        single_time = time.time() - start_time
        
        # 多进程处理
        start_time = time.time()
        with ProcessPoolExecutor() as executor:
            chunk_results = list(executor.map(process_chunk, chunks))
            multi_result = sum(chunk_results)
        multi_time = time.time() - start_time
        
        print(f"  单进程时间: {single_time:.4f}秒")
        print(f"  多进程时间: {multi_time:.4f}秒")
        print(f"  性能提升: {single_time/multi_time:.2f}x")
        print(f"  结果一致: {single_result == multi_result}")
    
    # 4. 异常处理和超时
    print(f"\n4. 异常处理和超时:")
    
    def unreliable_task(task_id, fail_rate=0.3):
        """不可靠任务"""
        if random.random() < fail_rate:
            raise ValueError(f"任务{task_id}随机失败")
        
        # 模拟长时间运行
        time.sleep(random.uniform(0.5, 2.0))
        return f"任务{task_id}成功完成"
    
    if __name__ == '__main__':
        with ProcessPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(unreliable_task, i, 0.4) 
                for i in range(6)
            ]
            
            for i, future in enumerate(futures):
                try:
                    result = future.result(timeout=3.0)  # 3秒超时
                    print(f"  ✅ {result}")
                except TimeoutError:
                    print(f"  ⏰ 任务{i}超时")
                except Exception as e:
                    print(f"  ❌ 任务{i}失败: {e}")
    
    """
    Java进程池等价实现:
    
    // Java中使用ForkJoinPool处理CPU密集型任务
    public class ParallelProcessing {
        
        // 使用并行流处理
        public void parallelStreamExample() {
            List<Integer> tasks = Arrays.asList(1000, 2000, 1500, 3000, 2500);
            
            // 并行执行CPU密集型任务
            List<Integer> results = tasks.parallelStream()
                                        .map(this::cpuIntensiveTask)
                                        .collect(Collectors.toList());
        }
        
        // 使用ForkJoinPool自定义并行度
        public void forkJoinPoolExample() {
            ForkJoinPool customThreadPool = new ForkJoinPool(4);
            
            try {
                List<Integer> results = customThreadPool.submit(() ->
                    tasks.parallelStream()
                         .map(this::cpuIntensiveTask)
                         .collect(Collectors.toList())
                ).get();
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                customThreadPool.shutdown();
            }
        }
        
        // 使用CompletableFuture处理异步任务
        public void completableFutureExample() {
            List<CompletableFuture<Integer>> futures = tasks.stream()
                .map(task -> CompletableFuture.supplyAsync(() -> 
                    cpuIntensiveTask(task), ForkJoinPool.commonPool()))
                .collect(Collectors.toList());
            
            // 等待所有任务完成
            CompletableFuture<Void> allOf = CompletableFuture.allOf(
                futures.toArray(new CompletableFuture[0])
            );
            
            allOf.join();
            
            // 收集结果
            List<Integer> results = futures.stream()
                                          .map(CompletableFuture::join)
                                          .collect(Collectors.toList());
        }
    }
    """
    
    print()


def demo_parallel_algorithms():
    """演示并行算法"""
    print("=== 4. 并行算法演示 ===")
    
    # 1. 并行排序（归并排序）
    def parallel_merge_sort(arr, processes=None):
        """并行归并排序"""
        if processes is None:
            processes = mp.cpu_count()
        
        if len(arr) <= 1:
            return arr
        
        if len(arr) < 1000:  # 小数组直接排序
            return sorted(arr)
        
        # 分割数组
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        
        if len(arr) > 10000 and processes > 1:
            # 并行处理
            with ProcessPoolExecutor(max_workers=2) as executor:
                left_future = executor.submit(parallel_merge_sort, left, processes//2)
                right_future = executor.submit(parallel_merge_sort, right, processes//2)
                
                left_sorted = left_future.result()
                right_sorted = right_future.result()
        else:
            # 串行处理
            left_sorted = parallel_merge_sort(left, 1)
            right_sorted = parallel_merge_sort(right, 1)
        
        # 合并
        return merge(left_sorted, right_sorted)
    
    def merge(left, right):
        """合并两个有序数组"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    # 2. 并行搜索
    def parallel_search(arr, target, chunk_size=1000):
        """并行搜索"""
        def search_chunk(chunk_data):
            chunk, start_index = chunk_data
            for i, value in enumerate(chunk):
                if value == target:
                    return start_index + i
            return -1
        
        # 分割数组
        chunks = []
        for i in range(0, len(arr), chunk_size):
            chunk = arr[i:i+chunk_size]
            chunks.append((chunk, i))
        
        if __name__ == '__main__':
            with ProcessPoolExecutor() as executor:
                results = list(executor.map(search_chunk, chunks))
            
            # 找到第一个匹配
            for result in results:
                if result != -1:
                    return result
            
            return -1
    
    # 3. 并行矩阵乘法
    def parallel_matrix_multiply(A, B):
        """并行矩阵乘法"""
        def multiply_row(row_data):
            row_index, row = row_data
            result_row = []
            for j in range(len(B[0])):
                value = sum(row[k] * B[k][j] for k in range(len(row)))
                result_row.append(value)
            return result_row
        
        if __name__ == '__main__':
            row_data = [(i, A[i]) for i in range(len(A))]
            
            with ProcessPoolExecutor() as executor:
                result_rows = list(executor.map(multiply_row, row_data))
            
            return result_rows
    
    # 4. 并行数值积分
    def parallel_integrate(func, a, b, n_intervals=1000000):
        """并行数值积分（梯形法则）"""
        def integrate_chunk(chunk_data):
            start, end, intervals = chunk_data
            h = (end - start) / intervals
            
            total = 0.5 * (func(start) + func(end))
            for i in range(1, intervals):
                x = start + i * h
                total += func(x)
            
            return total * h
        
        # 分割积分区间
        n_processes = mp.cpu_count()
        chunk_intervals = n_intervals // n_processes
        chunks = []
        
        for i in range(n_processes):
            start = a + i * (b - a) / n_processes
            end = a + (i + 1) * (b - a) / n_processes
            chunks.append((start, end, chunk_intervals))
        
        if __name__ == '__main__':
            with ProcessPoolExecutor() as executor:
                partial_results = list(executor.map(integrate_chunk, chunks))
            
            return sum(partial_results)
    
    # 测试并行算法
    print("1. 并行排序测试:")
    if __name__ == '__main__':
        # 生成随机数组
        test_array = [random.randint(1, 10000) for _ in range(50000)]
        
        # 串行排序
        start_time = time.time()
        serial_sorted = sorted(test_array.copy())
        serial_time = time.time() - start_time
        
        # 并行排序
        start_time = time.time()
        parallel_sorted = parallel_merge_sort(test_array.copy())
        parallel_time = time.time() - start_time
        
        print(f"  数组大小: {len(test_array)}")
        print(f"  串行时间: {serial_time:.4f}秒")
        print(f"  并行时间: {parallel_time:.4f}秒")
        print(f"  性能提升: {serial_time/parallel_time:.2f}x")
        print(f"  结果正确: {serial_sorted == parallel_sorted}")
    
    print(f"\n2. 并行搜索测试:")
    if __name__ == '__main__':
        # 生成大数组
        search_array = list(range(1000000))
        target = 777777
        
        # 串行搜索
        start_time = time.time()
        serial_index = search_array.index(target)
        serial_search_time = time.time() - start_time
        
        # 并行搜索
        start_time = time.time()
        parallel_index = parallel_search(search_array, target)
        parallel_search_time = time.time() - start_time
        
        print(f"  数组大小: {len(search_array)}")
        print(f"  串行搜索时间: {serial_search_time:.6f}秒")
        print(f"  并行搜索时间: {parallel_search_time:.6f}秒")
        print(f"  结果正确: {serial_index == parallel_index}")
    
    print(f"\n3. 并行数值积分测试:")
    if __name__ == '__main__':
        # 计算 sin(x) 在 [0, π] 的积分（理论值为2）
        import math
        
        def sin_func(x):
            return math.sin(x)
        
        # 串行积分
        start_time = time.time()
        # 简单积分实现
        def simple_integrate(func, a, b, n):
            h = (b - a) / n
            total = 0.5 * (func(a) + func(b))
            for i in range(1, n):
                x = a + i * h
                total += func(x)
            return total * h
        
        serial_result = simple_integrate(sin_func, 0, math.pi, 1000000)
        serial_integrate_time = time.time() - start_time
        
        # 并行积分
        start_time = time.time()
        parallel_result = parallel_integrate(sin_func, 0, math.pi, 1000000)
        parallel_integrate_time = time.time() - start_time
        
        print(f"  理论值: 2.0")
        print(f"  串行结果: {serial_result:.6f}, 时间: {serial_integrate_time:.4f}秒")
        print(f"  并行结果: {parallel_result:.6f}, 时间: {parallel_integrate_time:.4f}秒")
        print(f"  性能提升: {serial_integrate_time/parallel_integrate_time:.2f}x")
    
    """
    Java并行算法等价实现:
    
    // 1. 并行排序（使用Arrays.parallelSort）
    public void parallelSortExample() {
        int[] array = new Random().ints(50000, 1, 10001).toArray();
        
        // Java内置并行排序
        long startTime = System.nanoTime();
        Arrays.parallelSort(array);
        long parallelTime = System.nanoTime() - startTime;
        
        System.out.println("并行排序时间: " + parallelTime / 1_000_000 + "ms");
    }
    
    // 2. 并行搜索（使用并行流）
    public int parallelSearch(List<Integer> list, int target) {
        Optional<Integer> result = IntStream.range(0, list.size())
                                          .parallel()
                                          .filter(i -> list.get(i).equals(target))
                                          .findFirst();
        return result.orElse(-1);
    }
    
    // 3. 并行归约（reduce）
    public double parallelSum(List<Double> numbers) {
        return numbers.parallelStream()
                     .reduce(0.0, Double::sum);
    }
    
    // 4. Fork/Join框架自定义任务
    public class ParallelSum extends RecursiveTask<Long> {
        private final int[] array;
        private final int start, end;
        private static final int THRESHOLD = 1000;
        
        @Override
        protected Long compute() {
            if (end - start <= THRESHOLD) {
                // 直接计算
                long sum = 0;
                for (int i = start; i < end; i++) {
                    sum += array[i];
                }
                return sum;
            } else {
                // 分割任务
                int mid = (start + end) / 2;
                ParallelSum leftTask = new ParallelSum(array, start, mid);
                ParallelSum rightTask = new ParallelSum(array, mid, end);
                
                leftTask.fork(); // 异步执行左半部分
                long rightResult = rightTask.compute(); // 同步执行右半部分
                long leftResult = leftTask.join(); // 等待左半部分完成
                
                return leftResult + rightResult;
            }
        }
    }
    """
    
    print()


def main():
    """主函数：运行所有演示"""
    print("Python多进程编程完整学习指南")
    print("=" * 50)
    
    demo_basic_multiprocessing()
    demo_process_communication()
    demo_process_pool()
    demo_parallel_algorithms()
    
    print("学习总结:")
    print("1. multiprocessing模块提供完整的多进程支持")
    print("2. 进程间通信：Queue、Pipe、共享内存、Manager")
    print("3. ProcessPoolExecutor简化进程池管理")
    print("4. 多进程适合CPU密集型任务，绕过GIL限制")
    print("5. 并行算法可以显著提升性能")
    print("6. Java使用ForkJoinPool和并行流实现类似功能")
    print("7. 选择建议：CPU密集型用多进程，I/O密集型用多线程")


if __name__ == "__main__":
    main() 