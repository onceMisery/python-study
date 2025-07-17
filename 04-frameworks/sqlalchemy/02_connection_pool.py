#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库连接池详解
Database Connection Pool Guide

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习数据库连接池的连接管理、性能优化和与HikariCP的对比

学习目标:
1. 掌握SQLAlchemy连接池的配置和管理
2. 理解连接池的性能优化策略
3. 学会监控和调试连接池问题
4. 对比Python连接池与Java HikariCP的差异

注意：连接池是数据库应用性能的关键组件
"""

from sqlalchemy import create_engine, event, pool
from sqlalchemy.pool import QueuePool, StaticPool, NullPool, SingletonThreadPool
from sqlalchemy.pool import AssertionPool, InvalidatePoolError
from sqlalchemy.exc import DisconnectionError, TimeoutError
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import time
import threading
import logging
import psutil
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics


def demo_connection_pool_basics():
    """演示连接池基础配置"""
    print("=== 1. 连接池基础配置 ===")
    
    basic_pool_config = '''
# SQLAlchemy连接池配置示例

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# 1. 基础连接池配置
def create_engine_with_pool():
    """创建带连接池的数据库引擎"""
    
    DATABASE_URL = "postgresql://user:password@localhost:5432/mydb"
    
    engine = create_engine(
        DATABASE_URL,
        
        # 连接池类型
        poolclass=QueuePool,
        
        # 核心连接池参数
        pool_size=10,              # 连接池大小（保持的连接数）
        max_overflow=20,           # 最大溢出连接数
        pool_timeout=30,           # 获取连接的超时时间（秒）
        pool_recycle=3600,         # 连接回收时间（秒）
        pool_pre_ping=True,        # 连接前预检查
        
        # 连接池调试
        echo_pool=False,           # 是否记录连接池日志
        
        # 其他优化参数
        pool_reset_on_return='commit',  # 连接返回时的重置方式
        connect_args={
            "connect_timeout": 10,       # 连接超时
            "application_name": "MyApp", # 应用标识
            "options": "-c timezone=UTC" # PostgreSQL特定选项
        }
    )
    
    return engine

# 2. 不同类型的连接池
def different_pool_types():
    """不同类型的连接池配置"""
    
    # QueuePool - 默认连接池（推荐用于Web应用）
    queue_pool_engine = create_engine(
        "postgresql://user:password@localhost:5432/mydb",
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10
    )
    
    # StaticPool - 单连接池（适用于SQLite）
    static_pool_engine = create_engine(
        "sqlite:///app.db",
        poolclass=StaticPool,
        connect_args={
            "check_same_thread": False,
            "timeout": 20
        }
    )
    
    # NullPool - 无连接池（每次创建新连接）
    null_pool_engine = create_engine(
        "postgresql://user:password@localhost:5432/mydb",
        poolclass=NullPool
    )
    
    # SingletonThreadPool - 线程单例池
    singleton_pool_engine = create_engine(
        "sqlite:///app.db",
        poolclass=SingletonThreadPool
    )
    
    # AssertionPool - 调试用连接池
    assertion_pool_engine = create_engine(
        "postgresql://user:password@localhost:5432/mydb",
        poolclass=AssertionPool
    )
    
    return queue_pool_engine, static_pool_engine

# 3. 自定义连接池
class CustomQueuePool(QueuePool):
    """自定义连接池"""
    
    def __init__(self, *args, **kwargs):
        # 添加自定义监控
        self._connection_count = 0
        self._max_connections_used = 0
        super().__init__(*args, **kwargs)
    
    def _do_get(self):
        """获取连接时的自定义逻辑"""
        conn = super()._do_get()
        self._connection_count += 1
        self._max_connections_used = max(self._max_connections_used, self._connection_count)
        return conn
    
    def _do_return_conn(self, conn):
        """归还连接时的自定义逻辑"""
        self._connection_count -= 1
        return super()._do_return_conn(conn)
    
    def get_stats(self):
        """获取连接池统计信息"""
        return {
            'current_connections': self._connection_count,
            'max_connections_used': self._max_connections_used,
            'pool_size': self.size(),
            'checked_out': self.checkedout(),
            'overflow': self.overflow(),
            'checked_in': self.checkedin()
        }

def create_custom_pool_engine():
    """创建自定义连接池引擎"""
    return create_engine(
        "postgresql://user:password@localhost:5432/mydb",
        poolclass=CustomQueuePool,
        pool_size=5,
        max_overflow=10
    )
'''
    
    print("连接池类型特点:")
    print("1. QueuePool: 默认连接池，适合多线程Web应用")
    print("2. StaticPool: 单连接池，适合SQLite等轻量数据库")
    print("3. NullPool: 无连接池，每次创建新连接")
    print("4. SingletonThreadPool: 线程单例池，线程安全")
    print("5. AssertionPool: 调试专用，检测连接泄漏")
    
    # HikariCP配置对比
    hikaricp_config = '''
// HikariCP连接池配置对比

// 1. Spring Boot中的HikariCP配置
// application.properties
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=user
spring.datasource.password=password
spring.datasource.driver-class-name=org.postgresql.Driver

# HikariCP连接池配置
spring.datasource.hikari.pool-name=MyAppPool
spring.datasource.hikari.maximum-pool-size=20          # 最大连接数
spring.datasource.hikari.minimum-idle=5                # 最小空闲连接数
spring.datasource.hikari.connection-timeout=30000      # 连接超时（毫秒）
spring.datasource.hikari.idle-timeout=600000           # 空闲超时（毫秒）
spring.datasource.hikari.max-lifetime=1800000          # 连接最大生命周期
spring.datasource.hikari.leak-detection-threshold=60000 # 连接泄漏检测阈值

# 性能优化配置
spring.datasource.hikari.data-source-properties.cachePrepStmts=true
spring.datasource.hikari.data-source-properties.prepStmtCacheSize=250
spring.datasource.hikari.data-source-properties.prepStmtCacheSqlLimit=2048
spring.datasource.hikari.data-source-properties.useServerPrepStmts=true

// 2. 编程式配置
@Configuration
public class DatabaseConfig {
    
    @Bean
    @Primary
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        
        // 基础连接配置
        config.setJdbcUrl("jdbc:postgresql://localhost:5432/mydb");
        config.setUsername("user");
        config.setPassword("password");
        config.setDriverClassName("org.postgresql.Driver");
        
        // 连接池配置
        config.setPoolName("MyAppPool");
        config.setMaximumPoolSize(20);
        config.setMinimumIdle(5);
        config.setConnectionTimeout(30000);
        config.setIdleTimeout(600000);
        config.setMaxLifetime(1800000);
        config.setLeakDetectionThreshold(60000);
        
        // 连接测试
        config.setConnectionTestQuery("SELECT 1");
        config.setValidationTimeout(5000);
        
        // 性能优化
        config.addDataSourceProperty("cachePrepStmts", "true");
        config.addDataSourceProperty("prepStmtCacheSize", "250");
        config.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");
        config.addDataSourceProperty("useServerPrepStmts", "true");
        
        return new HikariDataSource(config);
    }
    
    @Bean
    public JdbcTemplate jdbcTemplate(DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
}

// 3. 连接池监控
@Component
public class HikariPoolMonitor {
    
    @Autowired
    private DataSource dataSource;
    
    @Scheduled(fixedRate = 60000) // 每分钟执行一次
    public void logPoolStats() {
        if (dataSource instanceof HikariDataSource) {
            HikariDataSource hikariDS = (HikariDataSource) dataSource;
            HikariPoolMXBean poolBean = hikariDS.getHikariPoolMXBean();
            
            log.info("HikariCP Stats - Active: {}, Idle: {}, Total: {}, Waiting: {}",
                poolBean.getActiveConnections(),
                poolBean.getIdleConnections(),
                poolBean.getTotalConnections(),
                poolBean.getThreadsAwaitingConnection()
            );
        }
    }
    
    public PoolStats getPoolStats() {
        if (dataSource instanceof HikariDataSource) {
            HikariDataSource hikariDS = (HikariDataSource) dataSource;
            HikariPoolMXBean poolBean = hikariDS.getHikariPoolMXBean();
            
            return PoolStats.builder()
                    .activeConnections(poolBean.getActiveConnections())
                    .idleConnections(poolBean.getIdleConnections())
                    .totalConnections(poolBean.getTotalConnections())
                    .threadsAwaitingConnection(poolBean.getThreadsAwaitingConnection())
                    .build();
        }
        return null;
    }
}
'''
    
    print(f"\n连接池配置对比:")
    print("SQLAlchemy:")
    print("- Python原生配置，灵活直观")
    print("- 多种连接池类型选择")
    print("- 基于事件的监控机制")
    print("- 适合Python异步编程")
    
    print(f"\nHikariCP:")
    print("- 零开销设计，高性能")
    print("- 丰富的监控指标")
    print("- 自动连接泄漏检测")
    print("- 企业级稳定性")
    print()


def demo_pool_monitoring():
    """演示连接池监控和调试"""
    print("=== 2. 连接池监控和调试 ===")
    
    monitoring_example = '''
# 连接池监控和调试

import logging
import time
import threading
from sqlalchemy import event, create_engine
from sqlalchemy.pool import Pool
from sqlalchemy.engine import Engine
from dataclasses import dataclass
from typing import Dict, List
from collections import defaultdict, deque

# 1. 连接池统计信息
@dataclass
class PoolStats:
    """连接池统计信息"""
    pool_size: int
    checked_out: int
    overflow: int
    checked_in: int
    total_connections: int
    peak_connections: int
    connection_requests: int
    connection_timeouts: int
    connection_errors: int

class PoolMonitor:
    """连接池监控器"""
    
    def __init__(self, engine):
        self.engine = engine
        self.stats = PoolStats(0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.connection_history = deque(maxlen=1000)
        self.request_times = deque(maxlen=1000)
        self._lock = threading.Lock()
        
        # 注册事件监听器
        self._register_events()
    
    def _register_events(self):
        """注册连接池事件监听器"""
        
        @event.listens_for(self.engine, "connect")
        def on_connect(dbapi_conn, connection_record):
            """连接创建事件"""
            with self._lock:
                self.connection_history.append({
                    'event': 'connect',
                    'timestamp': time.time(),
                    'thread_id': threading.get_ident()
                })
        
        @event.listens_for(self.engine, "checkout")
        def on_checkout(dbapi_conn, connection_record, connection_proxy):
            """连接检出事件"""
            with self._lock:
                self.stats.connection_requests += 1
                self.connection_history.append({
                    'event': 'checkout',
                    'timestamp': time.time(),
                    'thread_id': threading.get_ident()
                })
        
        @event.listens_for(self.engine, "checkin")
        def on_checkin(dbapi_conn, connection_record):
            """连接归还事件"""
            with self._lock:
                self.connection_history.append({
                    'event': 'checkin',
                    'timestamp': time.time(),
                    'thread_id': threading.get_ident()
                })
        
        @event.listens_for(self.engine, "invalidate")
        def on_invalidate(dbapi_conn, connection_record, exception):
            """连接失效事件"""
            with self._lock:
                self.stats.connection_errors += 1
                logging.warning(f"Connection invalidated: {exception}")
    
    def get_current_stats(self) -> PoolStats:
        """获取当前连接池统计"""
        pool = self.engine.pool
        
        with self._lock:
            self.stats.pool_size = pool.size()
            self.stats.checked_out = pool.checkedout()
            self.stats.overflow = pool.overflow()
            self.stats.checked_in = pool.checkedin()
            self.stats.total_connections = self.stats.checked_out + self.stats.checked_in
            self.stats.peak_connections = max(self.stats.peak_connections, self.stats.total_connections)
        
        return self.stats
    
    def get_connection_history(self, limit: int = 100) -> List[Dict]:
        """获取连接历史"""
        with self._lock:
            return list(self.connection_history)[-limit:]
    
    def reset_stats(self):
        """重置统计信息"""
        with self._lock:
            self.stats = PoolStats(0, 0, 0, 0, 0, 0, 0, 0, 0)
            self.connection_history.clear()

# 2. 性能测试工具
class PoolPerformanceTester:
    """连接池性能测试"""
    
    def __init__(self, engine, monitor: PoolMonitor):
        self.engine = engine
        self.monitor = monitor
    
    def test_concurrent_connections(self, num_threads: int = 10, operations_per_thread: int = 100):
        """测试并发连接性能"""
        print(f"测试并发连接: {num_threads}线程, 每线程{operations_per_thread}操作")
        
        start_time = time.time()
        results = []
        
        def worker_task(thread_id: int):
            """工作线程任务"""
            thread_results = {
                'thread_id': thread_id,
                'successful_operations': 0,
                'failed_operations': 0,
                'total_time': 0,
                'avg_connection_time': 0
            }
            
            connection_times = []
            
            for i in range(operations_per_thread):
                op_start = time.time()
                try:
                    with self.engine.connect() as conn:
                        conn_time = time.time() - op_start
                        connection_times.append(conn_time)
                        
                        # 模拟数据库操作
                        result = conn.execute("SELECT 1").scalar()
                        thread_results['successful_operations'] += 1
                        
                except Exception as e:
                    thread_results['failed_operations'] += 1
                    logging.error(f"Thread {thread_id} operation {i} failed: {e}")
            
            thread_results['total_time'] = time.time() - op_start
            if connection_times:
                thread_results['avg_connection_time'] = statistics.mean(connection_times)
            
            return thread_results
        
        # 执行并发测试
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker_task, i) for i in range(num_threads)]
            results = [future.result() for future in as_completed(futures)]
        
        total_time = time.time() - start_time
        
        # 统计结果
        total_successful = sum(r['successful_operations'] for r in results)
        total_failed = sum(r['failed_operations'] for r in results)
        avg_connection_time = statistics.mean([r['avg_connection_time'] for r in results if r['avg_connection_time'] > 0])
        
        print(f"并发测试结果:")
        print(f"  总耗时: {total_time:.2f}秒")
        print(f"  成功操作: {total_successful}")
        print(f"  失败操作: {total_failed}")
        print(f"  平均连接时间: {avg_connection_time:.4f}秒")
        print(f"  操作/秒: {total_successful / total_time:.2f}")
        
        # 连接池统计
        pool_stats = self.monitor.get_current_stats()
        print(f"  峰值连接数: {pool_stats.peak_connections}")
        print(f"  连接请求数: {pool_stats.connection_requests}")
        print(f"  连接错误数: {pool_stats.connection_errors}")
        
        return results
    
    def test_connection_leak(self, num_leaks: int = 5):
        """测试连接泄漏检测"""
        print(f"测试连接泄漏检测: 创建{num_leaks}个泄漏连接")
        
        leaked_connections = []
        
        try:
            # 故意创建未关闭的连接
            for i in range(num_leaks):
                conn = self.engine.connect()
                leaked_connections.append(conn)
                print(f"  创建泄漏连接 {i+1}")
            
            # 检查连接池状态
            pool_stats = self.monitor.get_current_stats()
            print(f"当前检出连接数: {pool_stats.checked_out}")
            
            # 尝试获取更多连接
            try:
                with self.engine.connect() as conn:
                    conn.execute("SELECT 1").scalar()
                    print("  正常连接仍可获取")
            except Exception as e:
                print(f"  连接池耗尽: {e}")
        
        finally:
            # 清理泄漏的连接
            for conn in leaked_connections:
                conn.close()
            print(f"  清理了{len(leaked_connections)}个泄漏连接")

# 3. 连接池健康检查
class PoolHealthChecker:
    """连接池健康检查"""
    
    def __init__(self, engine):
        self.engine = engine
    
    def check_pool_health(self) -> Dict[str, Any]:
        """检查连接池健康状态"""
        health_report = {
            'status': 'healthy',
            'checks': {},
            'recommendations': []
        }
        
        pool = self.engine.pool
        
        # 检查连接池大小
        pool_size = pool.size()
        checked_out = pool.checkedout()
        checked_in = pool.checkedin()
        overflow = pool.overflow()
        
        health_report['checks']['pool_utilization'] = {
            'pool_size': pool_size,
            'checked_out': checked_out,
            'checked_in': checked_in,
            'overflow': overflow,
            'utilization_rate': checked_out / (pool_size + overflow) if (pool_size + overflow) > 0 else 0
        }
        
        # 连接池利用率检查
        utilization_rate = checked_out / (pool_size + overflow) if (pool_size + overflow) > 0 else 0
        if utilization_rate > 0.8:
            health_report['status'] = 'warning'
            health_report['recommendations'].append('连接池利用率过高，建议增加pool_size')
        
        # 溢出连接检查
        if overflow > pool_size * 0.5:
            health_report['status'] = 'warning'
            health_report['recommendations'].append('溢出连接过多，建议调整连接池配置')
        
        # 连接测试
        try:
            start_time = time.time()
            with self.engine.connect() as conn:
                conn.execute("SELECT 1").scalar()
            connection_time = time.time() - start_time
            
            health_report['checks']['connection_test'] = {
                'success': True,
                'response_time': connection_time
            }
            
            if connection_time > 1.0:
                health_report['status'] = 'warning'
                health_report['recommendations'].append('数据库连接响应时间过长')
                
        except Exception as e:
            health_report['status'] = 'unhealthy'
            health_report['checks']['connection_test'] = {
                'success': False,
                'error': str(e)
            }
        
        return health_report
    
    def diagnose_slow_connections(self, threshold_seconds: float = 1.0):
        """诊断慢连接问题"""
        print(f"诊断连接时间超过{threshold_seconds}秒的问题")
        
        slow_connections = []
        
        for i in range(10):  # 测试10次连接
            start_time = time.time()
            try:
                with self.engine.connect() as conn:
                    conn.execute("SELECT 1").scalar()
                connection_time = time.time() - start_time
                
                if connection_time > threshold_seconds:
                    slow_connections.append({
                        'attempt': i + 1,
                        'connection_time': connection_time
                    })
                    
            except Exception as e:
                slow_connections.append({
                    'attempt': i + 1,
                    'error': str(e)
                })
        
        if slow_connections:
            print(f"发现{len(slow_connections)}次慢连接:")
            for conn_info in slow_connections:
                if 'error' in conn_info:
                    print(f"  尝试{conn_info['attempt']}: 错误 - {conn_info['error']}")
                else:
                    print(f"  尝试{conn_info['attempt']}: {conn_info['connection_time']:.3f}秒")
        else:
            print("未发现慢连接问题")
        
        return slow_connections

# 4. 使用示例
def example_usage():
    """监控使用示例"""
    
    # 创建引擎和监控器
    engine = create_engine(
        "postgresql://user:password@localhost:5432/mydb",
        pool_size=5,
        max_overflow=10,
        echo_pool=True
    )
    
    monitor = PoolMonitor(engine)
    tester = PoolPerformanceTester(engine, monitor)
    health_checker = PoolHealthChecker(engine)
    
    # 性能测试
    tester.test_concurrent_connections(num_threads=20, operations_per_thread=50)
    
    # 健康检查
    health_report = health_checker.check_pool_health()
    print(f"连接池健康状态: {health_report}")
    
    # 连接泄漏测试
    tester.test_connection_leak(num_leaks=3)
    
    # 获取统计信息
    stats = monitor.get_current_stats()
    print(f"当前连接池统计: {stats}")
'''
    
    print("连接池监控特点:")
    print("1. 实时统计信息：连接数、利用率、响应时间")
    print("2. 事件监听：连接创建、检出、归还、失效")
    print("3. 性能测试：并发压力测试、连接时间分析")
    print("4. 健康检查：连接池状态诊断和建议")
    print("5. 泄漏检测：未关闭连接监控")
    
    # Java监控对比
    java_monitoring = '''
// Java连接池监控对比

// 1. HikariCP JMX监控
@Component
public class HikariMonitor {
    
    @Autowired
    private DataSource dataSource;
    
    // 获取连接池指标
    public HikariPoolStats getPoolStats() {
        if (dataSource instanceof HikariDataSource) {
            HikariDataSource hikariDS = (HikariDataSource) dataSource;
            HikariPoolMXBean poolBean = hikariDS.getHikariPoolMXBean();
            
            return HikariPoolStats.builder()
                    .activeConnections(poolBean.getActiveConnections())
                    .idleConnections(poolBean.getIdleConnections())
                    .totalConnections(poolBean.getTotalConnections())
                    .threadsAwaitingConnection(poolBean.getThreadsAwaitingConnection())
                    .build();
        }
        return null;
    }
    
    // 暂停连接池
    public void suspendPool() {
        if (dataSource instanceof HikariDataSource) {
            HikariDataSource hikariDS = (HikariDataSource) dataSource;
            hikariDS.getHikariPoolMXBean().suspendPool();
        }
    }
    
    // 恢复连接池
    public void resumePool() {
        if (dataSource instanceof HikariDataSource) {
            HikariDataSource hikariDS = (HikariDataSource) dataSource;
            hikariDS.getHikariPoolMXBean().resumePool();
        }
    }
}

// 2. Micrometer监控集成
@Component
public class DataSourceMetrics {
    
    private final MeterRegistry meterRegistry;
    private final DataSource dataSource;
    
    public DataSourceMetrics(MeterRegistry meterRegistry, DataSource dataSource) {
        this.meterRegistry = meterRegistry;
        this.dataSource = dataSource;
        
        // 注册连接池指标
        if (dataSource instanceof HikariDataSource) {
            HikariDataSource hikariDS = (HikariDataSource) dataSource;
            new HikariCPMetrics(hikariDS).bindTo(meterRegistry);
        }
    }
    
    @EventListener
    public void handleDataSourceHealthCheck(DataSourceHealthEvent event) {
        Timer.Sample sample = Timer.start(meterRegistry);
        
        try (Connection conn = dataSource.getConnection()) {
            // 执行健康检查查询
            try (PreparedStatement stmt = conn.prepareStatement("SELECT 1")) {
                stmt.executeQuery();
                sample.stop(Timer.builder("datasource.health.check")
                          .description("DataSource health check time")
                          .register(meterRegistry));
            }
        } catch (SQLException e) {
            meterRegistry.counter("datasource.health.check.failures",
                               "error", e.getClass().getSimpleName())
                        .increment();
        }
    }
}

// 3. 自定义连接池监控
@Component
public class CustomConnectionPoolMonitor {
    
    private final AtomicLong connectionCount = new AtomicLong(0);
    private final AtomicLong maxConnectionsUsed = new AtomicLong(0);
    private final ConcurrentHashMap<String, Long> connectionTimes = new ConcurrentHashMap<>();
    
    @EventListener
    public void handleConnectionAcquired(ConnectionAcquiredEvent event) {
        long currentCount = connectionCount.incrementAndGet();
        maxConnectionsUsed.updateAndGet(max -> Math.max(max, currentCount));
        
        connectionTimes.put(event.getConnectionId(), System.currentTimeMillis());
    }
    
    @EventListener
    public void handleConnectionReleased(ConnectionReleasedEvent event) {
        connectionCount.decrementAndGet();
        
        Long acquireTime = connectionTimes.remove(event.getConnectionId());
        if (acquireTime != null) {
            long holdTime = System.currentTimeMillis() - acquireTime;
            
            // 记录连接持有时间指标
            Metrics.timer("connection.hold.time")
                   .record(holdTime, TimeUnit.MILLISECONDS);
        }
    }
    
    @Scheduled(fixedRate = 60000)
    public void logConnectionStats() {
        log.info("Connection Pool Stats - Current: {}, Max Used: {}, Avg Hold Time: {}ms",
                connectionCount.get(),
                maxConnectionsUsed.get(),
                getAverageConnectionHoldTime());
    }
    
    private double getAverageConnectionHoldTime() {
        Timer timer = Metrics.timer("connection.hold.time");
        return timer.mean(TimeUnit.MILLISECONDS);
    }
}
'''
    
    print(f"\n监控能力对比:")
    print("SQLAlchemy:")
    print("- 基于事件的监控机制")
    print("- 灵活的自定义监控器")
    print("- Python生态工具集成")
    print("- 适合开发和调试")
    
    print(f"\nHikariCP:")
    print("- 内置JMX监控支持")
    print("- 丰富的性能指标")
    print("- 企业级监控集成")
    print("- 生产环境优化")
    print()


def demo_performance_optimization():
    """演示连接池性能优化"""
    print("=== 3. 连接池性能优化 ===")
    
    optimization_example = '''
# 连接池性能优化策略

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from contextlib import asynccontextmanager

# 1. 连接池参数优化
def optimize_pool_parameters():
    """优化连接池参数"""
    
    # 基于负载特征的优化配置
    def create_optimized_engine(workload_type="web_app"):
        """根据工作负载类型创建优化的引擎"""
        
        if workload_type == "web_app":
            # Web应用优化：中等连接数，快速响应
            return create_engine(
                "postgresql://user:password@localhost:5432/mydb",
                pool_size=10,                    # 基础连接数
                max_overflow=20,                 # 峰值时的额外连接
                pool_timeout=5,                  # 快速超时避免请求堆积
                pool_recycle=1800,              # 30分钟回收连接
                pool_pre_ping=True,             # 预检查避免失效连接
                connect_args={
                    "connect_timeout": 5,
                    "application_name": "WebApp"
                }
            )
        
        elif workload_type == "batch_processing":
            # 批处理优化：更多连接，更长超时
            return create_engine(
                "postgresql://user:password@localhost:5432/mydb",
                pool_size=20,                    # 更多基础连接
                max_overflow=10,                 # 较少溢出连接
                pool_timeout=30,                 # 更长超时时间
                pool_recycle=3600,              # 1小时回收
                pool_pre_ping=True,
                connect_args={
                    "connect_timeout": 10,
                    "application_name": "BatchProcessor"
                }
            )
        
        elif workload_type == "analytics":
            # 分析工作负载：长连接，大超时
            return create_engine(
                "postgresql://user:password@localhost:5432/mydb",
                pool_size=5,                     # 较少连接数
                max_overflow=5,                  # 少量溢出
                pool_timeout=60,                 # 长超时
                pool_recycle=7200,              # 2小时回收
                pool_pre_ping=True,
                connect_args={
                    "connect_timeout": 30,
                    "statement_timeout": 300000,  # 5分钟查询超时
                    "application_name": "Analytics"
                }
            )
    
    return create_optimized_engine

# 2. 异步连接池优化
async def async_pool_optimization():
    """异步连接池优化"""
    
    # 异步引擎配置
    async_engine = create_async_engine(
        "postgresql+asyncpg://user:password@localhost:5432/mydb",
        pool_size=20,                        # 异步可以支持更多连接
        max_overflow=0,                      # 异步环境减少溢出
        pool_timeout=1,                      # 更短超时时间
        pool_recycle=3600,
        pool_pre_ping=True,
        echo=False
    )
    
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    @asynccontextmanager
    async def get_async_session():
        """异步会话上下文管理器"""
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    # 批量异步操作示例
    async def batch_async_operations(queries):
        """批量异步操作"""
        async with get_async_session() as session:
            tasks = []
            for query in queries:
                task = session.execute(query)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
    
    return async_engine, get_async_session

# 3. 连接重用策略
class ConnectionReuseOptimizer:
    """连接重用优化器"""
    
    def __init__(self, engine):
        self.engine = engine
        self.local_storage = threading.local()
    
    @contextmanager
    def reused_connection(self):
        """重用连接的上下文管理器"""
        # 检查线程本地存储中是否有连接
        if not hasattr(self.local_storage, 'connection') or \\
           self.local_storage.connection.closed:
            self.local_storage.connection = self.engine.connect()
        
        try:
            yield self.local_storage.connection
        except Exception:
            # 发生错误时关闭连接
            if hasattr(self.local_storage, 'connection'):
                self.local_storage.connection.close()
                delattr(self.local_storage, 'connection')
            raise
    
    def cleanup_thread_connections(self):
        """清理线程连接"""
        if hasattr(self.local_storage, 'connection'):
            self.local_storage.connection.close()
            delattr(self.local_storage, 'connection')

# 4. 连接池预热
class PoolWarmer:
    """连接池预热器"""
    
    def __init__(self, engine):
        self.engine = engine
    
    def warm_up_pool(self, target_connections: int = None):
        """预热连接池"""
        if target_connections is None:
            target_connections = self.engine.pool.size()
        
        print(f"预热连接池，目标连接数: {target_connections}")
        
        connections = []
        try:
            # 创建连接
            for i in range(target_connections):
                conn = self.engine.connect()
                connections.append(conn)
                print(f"  创建连接 {i+1}/{target_connections}")
            
            # 执行测试查询确保连接有效
            for i, conn in enumerate(connections):
                conn.execute("SELECT 1").scalar()
                print(f"  验证连接 {i+1}/{target_connections}")
        
        finally:
            # 归还所有连接到池中
            for conn in connections:
                conn.close()
        
        print(f"连接池预热完成，已创建 {len(connections)} 个连接")
    
    def scheduled_warmup(self, interval_minutes: int = 30):
        """定期预热连接池"""
        import schedule
        
        def warmup_job():
            try:
                self.warm_up_pool()
            except Exception as e:
                logging.error(f"连接池预热失败: {e}")
        
        schedule.every(interval_minutes).minutes.do(warmup_job)
        
        # 立即执行一次预热
        warmup_job()

# 5. 智能连接池调优
class SmartPoolTuner:
    """智能连接池调优器"""
    
    def __init__(self, engine, monitor):
        self.engine = engine
        self.monitor = monitor
        self.tuning_history = []
    
    def analyze_usage_patterns(self, observation_period_minutes: int = 60):
        """分析使用模式"""
        print(f"分析 {observation_period_minutes} 分钟的使用模式")
        
        start_time = time.time()
        end_time = start_time + (observation_period_minutes * 60)
        
        usage_samples = []
        
        while time.time() < end_time:
            stats = self.monitor.get_current_stats()
            usage_samples.append({
                'timestamp': time.time(),
                'checked_out': stats.checked_out,
                'total_connections': stats.total_connections,
                'utilization': stats.checked_out / max(stats.total_connections, 1)
            })
            
            time.sleep(10)  # 每10秒采样一次
        
        # 分析结果
        avg_utilization = statistics.mean([s['utilization'] for s in usage_samples])
        max_utilization = max([s['utilization'] for s in usage_samples])
        peak_connections = max([s['checked_out'] for s in usage_samples])
        
        analysis = {
            'avg_utilization': avg_utilization,
            'max_utilization': max_utilization,
            'peak_connections': peak_connections,
            'samples_count': len(usage_samples)
        }
        
        return analysis
    
    def recommend_tuning(self, analysis_result):
        """推荐调优参数"""
        recommendations = []
        
        avg_util = analysis_result['avg_utilization']
        max_util = analysis_result['max_utilization']
        peak_conn = analysis_result['peak_connections']
        
        current_pool_size = self.engine.pool.size()
        current_overflow = self.engine.pool._max_overflow
        
        # 分析并给出建议
        if avg_util > 0.8:
            new_pool_size = int(current_pool_size * 1.3)
            recommendations.append({
                'parameter': 'pool_size',
                'current': current_pool_size,
                'recommended': new_pool_size,
                'reason': f'平均利用率过高 ({avg_util:.2%})'
            })
        
        elif avg_util < 0.3:
            new_pool_size = max(5, int(current_pool_size * 0.8))
            recommendations.append({
                'parameter': 'pool_size',
                'current': current_pool_size,
                'recommended': new_pool_size,
                'reason': f'平均利用率过低 ({avg_util:.2%})'
            })
        
        if max_util > 0.95:
            new_overflow = int(current_overflow * 1.5)
            recommendations.append({
                'parameter': 'max_overflow',
                'current': current_overflow,
                'recommended': new_overflow,
                'reason': f'峰值利用率过高 ({max_util:.2%})'
            })
        
        return recommendations
    
    def auto_tune(self, dry_run: bool = True):
        """自动调优"""
        print("开始智能连接池调优...")
        
        # 分析当前使用模式
        analysis = self.analyze_usage_patterns(observation_period_minutes=5)  # 短期测试
        print(f"使用模式分析: {analysis}")
        
        # 获取调优建议
        recommendations = self.recommend_tuning(analysis)
        
        if not recommendations:
            print("当前连接池配置已最优，无需调整")
            return
        
        print("调优建议:")
        for rec in recommendations:
            print(f"  {rec['parameter']}: {rec['current']} -> {rec['recommended']} ({rec['reason']})")
        
        if not dry_run:
            # 实际应用调优（需要重新创建引擎）
            print("应用调优建议...")
            # 注意：实际生产环境中需要谨慎操作
            
        self.tuning_history.append({
            'timestamp': time.time(),
            'analysis': analysis,
            'recommendations': recommendations,
            'applied': not dry_run
        })

# 6. 使用示例
def optimization_example():
    """优化示例"""
    
    # 创建引擎
    engine = create_optimized_engine("web_app")
    monitor = PoolMonitor(engine)
    
    # 预热连接池
    warmer = PoolWarmer(engine)
    warmer.warm_up_pool()
    
    # 智能调优
    tuner = SmartPoolTuner(engine, monitor)
    tuner.auto_tune(dry_run=True)
    
    # 连接重用优化
    optimizer = ConnectionReuseOptimizer(engine)
    
    with optimizer.reused_connection() as conn:
        result = conn.execute("SELECT COUNT(*) FROM users").scalar()
        print(f"用户数量: {result}")
'''
    
    print("性能优化策略:")
    print("1. 参数调优：根据工作负载特征优化连接池参数")
    print("2. 异步优化：使用异步连接池提高并发能力")
    print("3. 连接重用：线程本地连接重用减少开销")
    print("4. 预热策略：应用启动时预热连接池")
    print("5. 智能调优：基于使用模式自动调整参数")
    
    # Java优化对比
    java_optimization = '''
// Java连接池优化对比

// 1. HikariCP性能优化
@Configuration
public class OptimizedDataSourceConfig {
    
    @Bean
    @ConfigurationProperties("app.datasource")
    public HikariConfig hikariConfig() {
        HikariConfig config = new HikariConfig();
        
        // 基础优化
        config.setAutoCommit(false);                    // 禁用自动提交
        config.setConnectionTimeout(5000);             // 5秒连接超时
        config.setIdleTimeout(300000);                 // 5分钟空闲超时
        config.setMaxLifetime(900000);                 // 15分钟最大生命周期
        config.setLeakDetectionThreshold(60000);       // 1分钟泄漏检测
        
        // 性能优化
        config.addDataSourceProperty("cachePrepStmts", "true");
        config.addDataSourceProperty("prepStmtCacheSize", "300");
        config.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");
        config.addDataSourceProperty("useServerPrepStmts", "true");
        config.addDataSourceProperty("rewriteBatchedStatements", "true");
        config.addDataSourceProperty("cacheResultSetMetadata", "true");
        config.addDataSourceProperty("cacheServerConfiguration", "true");
        config.addDataSourceProperty("elideSetAutoCommits", "true");
        config.addDataSourceProperty("maintainTimeStats", "false");
        
        return config;
    }
    
    @Bean
    public DataSource dataSource(HikariConfig hikariConfig) {
        return new HikariDataSource(hikariConfig);
    }
}

// 2. 动态连接池调优
@Component
public class DynamicPoolTuner {
    
    @Autowired
    private DataSource dataSource;
    
    @Value("${app.pool.auto-tune:false}")
    private boolean autoTuneEnabled;
    
    @Scheduled(fixedRate = 300000) // 每5分钟检查一次
    public void analyzePerfmanceAndTune() {
        if (!autoTuneEnabled || !(dataSource instanceof HikariDataSource)) {
            return;
        }
        
        HikariDataSource hikariDS = (HikariDataSource) dataSource;
        HikariPoolMXBean poolBean = hikariDS.getHikariPoolMXBean();
        
        // 收集指标
        int activeConnections = poolBean.getActiveConnections();
        int totalConnections = poolBean.getTotalConnections();
        int threadsAwaiting = poolBean.getThreadsAwaitingConnection();
        
        double utilization = (double) activeConnections / totalConnections;
        
        // 调优逻辑
        if (utilization > 0.9 && threadsAwaiting > 0) {
            // 高利用率且有等待线程，考虑增加连接数
            int currentMaxPool = hikariDS.getMaximumPoolSize();
            int newMaxPool = Math.min(currentMaxPool + 5, 50); // 最大不超过50
            
            log.info("Pool utilization high ({}%), increasing max pool size from {} to {}",
                    utilization * 100, currentMaxPool, newMaxPool);
                    
            hikariDS.setMaximumPoolSize(newMaxPool);
            
        } else if (utilization < 0.3 && totalConnections > 10) {
            // 低利用率，考虑减少连接数
            int currentMaxPool = hikariDS.getMaximumPoolSize();
            int newMaxPool = Math.max(currentMaxPool - 2, 10); // 最小保持10个
            
            log.info("Pool utilization low ({}%), decreasing max pool size from {} to {}",
                    utilization * 100, currentMaxPool, newMaxPool);
                    
            hikariDS.setMaximumPoolSize(newMaxPool);
        }
    }
}

// 3. 连接池预热
@Component
public class ConnectionPoolWarmer {
    
    @Autowired
    private DataSource dataSource;
    
    @EventListener(ApplicationReadyEvent.class)
    public void warmUpPool() {
        if (dataSource instanceof HikariDataSource) {
            HikariDataSource hikariDS = (HikariDataSource) dataSource;
            int poolSize = hikariDS.getMaximumPoolSize();
            
            log.info("Warming up connection pool with {} connections", poolSize);
            
            List<Connection> connections = new ArrayList<>();
            try {
                // 创建连接
                for (int i = 0; i < poolSize; i++) {
                    Connection conn = dataSource.getConnection();
                    connections.add(conn);
                    
                    // 验证连接
                    try (PreparedStatement stmt = conn.prepareStatement("SELECT 1")) {
                        stmt.executeQuery();
                    }
                }
                
                log.info("Connection pool warmed up successfully");
                
            } catch (SQLException e) {
                log.error("Failed to warm up connection pool", e);
            } finally {
                // 关闭所有连接，归还到池中
                connections.forEach(conn -> {
                    try { conn.close(); } catch (SQLException e) {}
                });
            }
        }
    }
}

// 4. 基于监控的自适应调优
@Component
public class AdaptivePoolTuner {
    
    private final MeterRegistry meterRegistry;
    private final DataSource dataSource;
    private final CircularBuffer<PoolMetrics> metricsHistory;
    
    public AdaptivePoolTuner(MeterRegistry meterRegistry, DataSource dataSource) {
        this.meterRegistry = meterRegistry;
        this.dataSource = dataSource;
        this.metricsHistory = new CircularBuffer<>(60); // 保存60个数据点
    }
    
    @Scheduled(fixedRate = 60000) // 每分钟收集一次指标
    public void collectMetrics() {
        if (dataSource instanceof HikariDataSource) {
            HikariDataSource hikariDS = (HikariDataSource) dataSource;
            HikariPoolMXBean poolBean = hikariDS.getHikariPoolMXBean();
            
            PoolMetrics metrics = PoolMetrics.builder()
                    .timestamp(Instant.now())
                    .activeConnections(poolBean.getActiveConnections())
                    .idleConnections(poolBean.getIdleConnections())
                    .totalConnections(poolBean.getTotalConnections())
                    .threadsAwaitingConnection(poolBean.getThreadsAwaitingConnection())
                    .build();
            
            metricsHistory.add(metrics);
            
            // 记录到监控系统
            meterRegistry.gauge("hikaricp.connections.active", metrics.getActiveConnections());
            meterRegistry.gauge("hikaricp.connections.idle", metrics.getIdleConnections());
            meterRegistry.gauge("hikaricp.connections.pending", metrics.getThreadsAwaitingConnection());
        }
    }
    
    @Scheduled(fixedRate = 300000) // 每5分钟分析一次
    public void analyzeAndTune() {
        if (metricsHistory.size() < 10) {
            return; // 数据不足，无法分析
        }
        
        List<PoolMetrics> recentMetrics = metricsHistory.getRecentItems(10);
        
        // 计算平均利用率
        double avgUtilization = recentMetrics.stream()
                .mapToDouble(m -> (double) m.getActiveConnections() / m.getTotalConnections())
                .average()
                .orElse(0.0);
        
        // 计算平均等待线程数
        double avgWaitingThreads = recentMetrics.stream()
                .mapToInt(PoolMetrics::getThreadsAwaitingConnection)
                .average()
                .orElse(0.0);
        
        // 基于分析结果调优
        if (avgUtilization > 0.8 && avgWaitingThreads > 1) {
            increasePoolSize();
        } else if (avgUtilization < 0.3 && avgWaitingThreads == 0) {
            decreasePoolSize();
        }
    }
    
    private void increasePoolSize() {
        // 增加连接池大小的逻辑
    }
    
    private void decreasePoolSize() {
        // 减少连接池大小的逻辑
    }
}
'''
    
    print(f"\n优化策略对比:")
    print("SQLAlchemy:")
    print("- 灵活的参数配置")
    print("- Python异步优化")
    print("- 自定义监控和调优")
    print("- 适合快速迭代优化")
    
    print(f"\nHikariCP:")
    print("- 零开销设计理念")
    print("- 内置性能优化")
    print("- JVM级别优化")
    print("- 生产环境稳定性")
    print()


def main():
    """主函数：运行所有演示"""
    print("数据库连接池完整学习指南")
    print("=" * 50)
    
    demo_connection_pool_basics()
    demo_pool_monitoring()
    demo_performance_optimization()
    
    print("学习总结:")
    print("1. 连接池是数据库应用性能的关键组件")
    print("2. 合理配置连接池参数至关重要")
    print("3. 实时监控帮助发现和解决问题")
    print("4. 性能优化需要结合具体业务场景")
    print("5. SQLAlchemy提供灵活的连接池解决方案")
    print("6. 与HikariCP相比各有优势，选择需考虑技术栈")


if __name__ == "__main__":
    main() 