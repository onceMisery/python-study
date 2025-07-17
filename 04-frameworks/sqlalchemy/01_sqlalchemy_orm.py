#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SQLAlchemy ORM详解
SQLAlchemy ORM Comprehensive Guide

作者: Python学习项目
日期: 2024-01-16
描述: 详细学习SQLAlchemy ORM的模型定义、关系映射、查询语法和与JPA的对比

学习目标:
1. 掌握SQLAlchemy模型定义和数据库映射
2. 理解关系映射和复杂查询构建
3. 学会会话管理和事务处理
4. 对比SQLAlchemy与JPA/Hibernate的设计差异

注意：SQLAlchemy是Python最强大的ORM框架，支持多种数据库
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy import ForeignKey, Table, Index, UniqueConstraint, CheckConstraint
from sqlalchemy import func, and_, or_, not_, case, cast, distinct, literal_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, joinedload, selectinload
from sqlalchemy.orm import Session, Query, aliased, contains_eager
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import select, update, delete, insert
from sqlalchemy.dialects import postgresql, mysql, sqlite
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional
import enum


def demo_sqlalchemy_setup():
    """演示SQLAlchemy基本设置"""
    print("=== 1. SQLAlchemy基本设置 ===")
    
    setup_example = '''
# SQLAlchemy基本设置和配置

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# 1. 数据库连接配置
# PostgreSQL
DATABASE_URL = "postgresql://user:password@localhost:5432/mydb"

# MySQL
# DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/mydb"

# SQLite
# DATABASE_URL = "sqlite:///./app.db"

# 2. 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    # 连接池配置
    poolclass=QueuePool,
    pool_size=20,                    # 连接池大小
    max_overflow=30,                 # 最大溢出连接数
    pool_timeout=30,                 # 获取连接超时时间
    pool_recycle=3600,              # 连接回收时间
    pool_pre_ping=True,             # 连接前预检查
    
    # 调试配置
    echo=False,                     # 是否打印SQL语句
    echo_pool=False,                # 是否打印连接池信息
    
    # 其他配置
    future=True,                    # 启用SQLAlchemy 2.0风格
    connect_args={
        "check_same_thread": False  # SQLite专用
    }
)

# 3. 创建会话工厂
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,              # 不自动提交
    autoflush=True,                # 自动刷新
    expire_on_commit=True          # 提交后过期对象
)

# 4. 声明基类
Base = declarative_base()

# 5. 数据库连接管理
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 异步版本（SQLAlchemy 1.4+）
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

async_engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost:5432/mydb",
    echo=True,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_db():
    """获取异步数据库会话"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
'''
    
    print("SQLAlchemy设置特点:")
    print("1. 支持多种数据库后端（PostgreSQL、MySQL、SQLite等）")
    print("2. 灵活的连接池配置和性能优化")
    print("3. 同步和异步两种操作模式")
    print("4. 声明式模型定义")
    print("5. 强大的查询构建器")
    
    # JPA配置对比
    jpa_setup_example = '''
// JPA/Hibernate配置对比

// 1. application.properties配置
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=user
spring.datasource.password=password
spring.datasource.driver-class-name=org.postgresql.Driver

// 连接池配置（HikariCP）
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000
spring.datasource.hikari.idle-timeout=600000
spring.datasource.hikari.max-lifetime=1800000

// JPA配置
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.use_sql_comments=true

// 2. 实体管理器配置
@Configuration
@EnableJpaRepositories
@EnableTransactionManagement
public class JpaConfig {
    
    @Bean
    @Primary
    public LocalContainerEntityManagerFactoryBean entityManagerFactory(
            DataSource dataSource,
            JpaProperties jpaProperties) {
        
        LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
        em.setDataSource(dataSource);
        em.setPackagesToScan("com.example.entity");
        
        HibernateJpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
        em.setJpaVendorAdapter(vendorAdapter);
        em.setJpaPropertyMap(jpaProperties.getProperties());
        
        return em;
    }
    
    @Bean
    public PlatformTransactionManager transactionManager(EntityManagerFactory emf) {
        return new JpaTransactionManager(emf);
    }
}

// 3. 实体管理器使用
@Repository
public class ProductRepositoryImpl {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    public List<Product> findProducts(ProductCriteria criteria) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Product> query = cb.createQuery(Product.class);
        Root<Product> product = query.from(Product.class);
        
        // 构建查询条件
        List<Predicate> predicates = new ArrayList<>();
        
        if (criteria.getName() != null) {
            predicates.add(cb.like(product.get("name"), "%" + criteria.getName() + "%"));
        }
        
        query.where(predicates.toArray(new Predicate[0]));
        
        return entityManager.createQuery(query).getResultList();
    }
}
'''
    
    print(f"\n配置对比:")
    print("SQLAlchemy:")
    print("- Python代码配置，灵活直观")
    print("- 支持多种数据库切换")
    print("- 连接池参数精细控制")
    print("- 同步/异步统一API")
    
    print(f"\nJPA/Hibernate:")
    print("- 配置文件+注解配置")
    print("- 自动配置和约定优于配置")
    print("- 企业级事务管理")
    print("- 成熟的缓存机制")
    print()


def demo_model_definition():
    """演示模型定义和表映射"""
    print("=== 2. 模型定义和表映射 ===")
    
    model_examples = '''
# SQLAlchemy模型定义示例

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Numeric
from sqlalchemy import ForeignKey, Enum, Index, UniqueConstraint, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

# 1. 枚举定义
class ProductStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DISCONTINUED = "discontinued"

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# 2. 基础模型类
class TimestampMixin:
    """时间戳混入类"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class User(Base, TimestampMixin):
    """用户模型"""
    __tablename__ = 'users'
    
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 基本字段
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # 状态字段
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # 个人信息
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    birth_date = Column(DateTime)
    last_login = Column(DateTime)
    
    # 表级约束
    __table_args__ = (
        Index('idx_user_email_active', 'email', 'is_active'),
        Index('idx_user_username_active', 'username', 'is_active'),
        CheckConstraint('length(username) >= 3', name='check_username_length'),
        CheckConstraint('length(password_hash) >= 6', name='check_password_length'),
    )
    
    # 计算属性
    @hybrid_property
    def full_name(self):
        """全名"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @hybrid_property
    def is_new_user(self):
        """是否新用户（注册不到7天）"""
        if self.created_at:
            return (datetime.utcnow() - self.created_at).days < 7
        return False
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Category(Base, TimestampMixin):
    """商品分类模型"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    image_url = Column(String(255))
    
    # 层级结构
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    level = Column(Integer, default=0, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    
    # 状态
    is_active = Column(Boolean, default=True, nullable=False)
    
    # 自引用关系
    parent = relationship('Category', remote_side=[id], backref='children')
    
    # 商品关系
    products = relationship('Product', back_populates='category', lazy='dynamic')
    
    # 表约束
    __table_args__ = (
        Index('idx_category_parent_active', 'parent_id', 'is_active'),
        Index('idx_category_level_sort', 'level', 'sort_order'),
        CheckConstraint('level >= 0', name='check_category_level'),
        CheckConstraint('sort_order >= 0', name='check_sort_order'),
    )
    
    @hybrid_property
    def product_count(self):
        """商品数量"""
        return self.products.filter_by(status=ProductStatus.PUBLISHED).count()
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

class Product(Base, TimestampMixin):
    """商品模型"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text)
    short_description = Column(String(500))
    
    # 价格信息
    price = Column(Numeric(10, 2), nullable=False)
    cost_price = Column(Numeric(10, 2))
    sale_price = Column(Numeric(10, 2))
    
    # 库存信息
    stock_quantity = Column(Integer, default=0, nullable=False)
    min_stock_level = Column(Integer, default=5, nullable=False)
    
    # 商品属性
    sku = Column(String(50), unique=True, nullable=False)
    barcode = Column(String(50), unique=True)
    weight = Column(Numeric(8, 3))
    dimensions = Column(String(100))  # 存储JSON格式的尺寸信息
    
    # 状态
    status = Column(Enum(ProductStatus), default=ProductStatus.DRAFT, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    is_digital = Column(Boolean, default=False, nullable=False)
    
    # 关系
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # 关系映射
    category = relationship('Category', back_populates='products')
    created_by = relationship('User', foreign_keys=[created_by_id])
    
    # 图片关系（一对多）
    images = relationship('ProductImage', back_populates='product', cascade='all, delete-orphan')
    
    # 订单项关系
    order_items = relationship('OrderItem', back_populates='product')
    
    # 表约束
    __table_args__ = (
        Index('idx_product_category_status', 'category_id', 'status'),
        Index('idx_product_price_status', 'price', 'status'),
        Index('idx_product_stock', 'stock_quantity'),
        Index('idx_product_featured', 'is_featured', 'status'),
        CheckConstraint('price > 0', name='check_positive_price'),
        CheckConstraint('stock_quantity >= 0', name='check_non_negative_stock'),
        CheckConstraint('min_stock_level >= 0', name='check_min_stock'),
    )
    
    # 计算属性
    @hybrid_property
    def is_in_stock(self):
        """是否有库存"""
        return self.stock_quantity > 0
    
    @hybrid_property
    def is_low_stock(self):
        """是否库存不足"""
        return self.stock_quantity <= self.min_stock_level
    
    @hybrid_property
    def profit_margin(self):
        """利润率"""
        if self.cost_price and self.price:
            return (self.price - self.cost_price) / self.price * 100
        return None
    
    @hybrid_property
    def display_price(self):
        """显示价格（优先显示促销价）"""
        return self.sale_price if self.sale_price else self.price
    
    def reduce_stock(self, quantity):
        """减少库存"""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            return True
        return False
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

class ProductImage(Base, TimestampMixin):
    """商品图片模型"""
    __tablename__ = 'product_images'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    image_url = Column(String(255), nullable=False)
    alt_text = Column(String(200))
    sort_order = Column(Integer, default=0, nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    
    # 关系
    product = relationship('Product', back_populates='images')
    
    __table_args__ = (
        Index('idx_product_image_order', 'product_id', 'sort_order'),
        Index('idx_product_image_primary', 'product_id', 'is_primary'),
    )

# 多对多关系表
order_product_association = Table(
    'order_products',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('quantity', Integer, nullable=False),
    Column('unit_price', Numeric(10, 2), nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow),
    Index('idx_order_product_order', 'order_id'),
    Index('idx_order_product_product', 'product_id'),
)

class Order(Base, TimestampMixin):
    """订单模型"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # 客户信息
    customer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # 金额信息
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), default=0)
    shipping_amount = Column(Numeric(10, 2), default=0)
    discount_amount = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), nullable=False)
    
    # 状态
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    
    # 地址信息（简化，实际应该关联地址表）
    shipping_address = Column(Text)
    billing_address = Column(Text)
    
    # 时间信息
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    
    # 关系
    customer = relationship('User', foreign_keys=[customer_id])
    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    
    # 多对多关系（通过关联表）
    products = relationship(
        'Product',
        secondary=order_product_association,
        backref='orders'
    )
    
    __table_args__ = (
        Index('idx_order_customer_status', 'customer_id', 'status'),
        Index('idx_order_status_created', 'status', 'created_at'),
        Index('idx_order_total', 'total_amount'),
        CheckConstraint('total_amount >= 0', name='check_positive_total'),
        CheckConstraint('subtotal >= 0', name='check_positive_subtotal'),
    )
    
    @hybrid_property
    def item_count(self):
        """订单项数量"""
        return len(self.order_items)
    
    @hybrid_property
    def is_paid(self):
        """是否已支付"""
        return self.status in [OrderStatus.PROCESSING, OrderStatus.SHIPPED, OrderStatus.DELIVERED]
    
    def calculate_total(self):
        """计算总金额"""
        self.subtotal = sum(item.line_total for item in self.order_items)
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_amount - self.discount_amount
    
    def __repr__(self):
        return f"<Order(id={self.id}, number='{self.order_number}', total={self.total_amount})>"

class OrderItem(Base):
    """订单项模型"""
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    
    # 商品信息快照
    product_name = Column(String(200), nullable=False)
    product_sku = Column(String(50), nullable=False)
    
    # 数量和价格
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    line_total = Column(Numeric(10, 2), nullable=False)
    
    # 关系
    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='order_items')
    
    __table_args__ = (
        Index('idx_order_item_order', 'order_id'),
        Index('idx_order_item_product', 'product_id'),
        UniqueConstraint('order_id', 'product_id', name='uq_order_product'),
        CheckConstraint('quantity > 0', name='check_positive_quantity'),
        CheckConstraint('unit_price >= 0', name='check_non_negative_price'),
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.quantity and self.unit_price:
            self.line_total = self.quantity * self.unit_price
    
    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id}, qty={self.quantity})>"
'''
    
    print("SQLAlchemy模型特点:")
    print("1. 声明式定义，清晰直观")
    print("2. 丰富的字段类型和约束")
    print("3. 混入类支持代码复用")
    print("4. hybrid_property计算属性")
    print("5. 灵活的关系映射配置")
    print("6. 表级索引和约束定义")
    
    # JPA实体对比
    jpa_entity_example = '''
// JPA实体定义对比

// 1. 基础实体类
@MappedSuperclass
public abstract class TimestampEntity {
    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;
    
    // getter、setter
}

// 2. 用户实体
@Entity
@Table(name = "users", 
       indexes = {
           @Index(name = "idx_user_email_active", columnList = "email, is_active"),
           @Index(name = "idx_user_username_active", columnList = "username, is_active")
       })
public class User extends TimestampEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "username", unique = true, nullable = false, length = 80)
    @Size(min = 3, max = 80, message = "用户名长度必须在3-80字符之间")
    private String username;
    
    @Column(name = "email", unique = true, nullable = false, length = 120)
    @Email(message = "邮箱格式不正确")
    private String email;
    
    @Column(name = "password_hash", nullable = false)
    @Size(min = 6, message = "密码长度至少6位")
    private String passwordHash;
    
    @Column(name = "is_active", nullable = false)
    private Boolean isActive = true;
    
    @Column(name = "is_admin", nullable = false)
    private Boolean isAdmin = false;
    
    @Column(name = "first_name", length = 50)
    private String firstName;
    
    @Column(name = "last_name", length = 50)
    private String lastName;
    
    // 计算属性
    @Transient
    public String getFullName() {
        if (firstName != null && lastName != null) {
            return firstName + " " + lastName;
        }
        return username;
    }
    
    @Transient
    public boolean isNewUser() {
        return createdAt != null && 
               ChronoUnit.DAYS.between(createdAt, LocalDateTime.now()) < 7;
    }
    
    // 构造器、getter、setter、equals、hashCode
}

// 3. 商品实体
@Entity
@Table(name = "products",
       indexes = {
           @Index(name = "idx_product_category_status", columnList = "category_id, status"),
           @Index(name = "idx_product_price_status", columnList = "price, status")
       })
public class Product extends TimestampEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "name", nullable = false, length = 200)
    @NotBlank(message = "商品名称不能为空")
    private String name;
    
    @Column(name = "slug", unique = true, nullable = false, length = 200)
    private String slug;
    
    @Column(name = "description", columnDefinition = "TEXT")
    private String description;
    
    @Column(name = "price", nullable = false, precision = 10, scale = 2)
    @DecimalMin(value = "0.01", message = "价格必须大于0")
    private BigDecimal price;
    
    @Column(name = "stock_quantity", nullable = false)
    @Min(value = 0, message = "库存不能为负数")
    private Integer stockQuantity = 0;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private ProductStatus status = ProductStatus.DRAFT;
    
    @Column(name = "is_featured", nullable = false)
    private Boolean isFeatured = false;
    
    // 关系映射
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id", nullable = false)
    private Category category;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "created_by_id", nullable = false)
    private User createdBy;
    
    @OneToMany(mappedBy = "product", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<ProductImage> images = new ArrayList<>();
    
    @OneToMany(mappedBy = "product")
    private List<OrderItem> orderItems = new ArrayList<>();
    
    // 业务方法
    @Transient
    public boolean isInStock() {
        return stockQuantity > 0;
    }
    
    public boolean reduceStock(int quantity) {
        if (stockQuantity >= quantity) {
            stockQuantity -= quantity;
            return true;
        }
        return false;
    }
    
    // 构造器、getter、setter
}

// 4. 订单实体
@Entity
@Table(name = "orders",
       indexes = {
           @Index(name = "idx_order_customer_status", columnList = "customer_id, status"),
           @Index(name = "idx_order_status_created", columnList = "status, created_at")
       })
public class Order extends TimestampEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "order_number", unique = true, nullable = false, length = 50)
    private String orderNumber;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", nullable = false)
    private User customer;
    
    @Column(name = "total_amount", nullable = false, precision = 10, scale = 2)
    @DecimalMin(value = "0", message = "总金额不能为负数")
    private BigDecimal totalAmount;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private OrderStatus status = OrderStatus.PENDING;
    
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> orderItems = new ArrayList<>();
    
    // 多对多关系（通过中间表）
    @ManyToMany
    @JoinTable(
        name = "order_products",
        joinColumns = @JoinColumn(name = "order_id"),
        inverseJoinColumns = @JoinColumn(name = "product_id")
    )
    private List<Product> products = new ArrayList<>();
    
    // 计算属性
    @Transient
    public int getItemCount() {
        return orderItems.size();
    }
    
    @Transient
    public boolean isPaid() {
        return status == OrderStatus.PROCESSING || 
               status == OrderStatus.SHIPPED || 
               status == OrderStatus.DELIVERED;
    }
    
    public void calculateTotal() {
        BigDecimal total = orderItems.stream()
                                   .map(OrderItem::getLineTotal)
                                   .reduce(BigDecimal.ZERO, BigDecimal::add);
        this.totalAmount = total;
    }
    
    // 构造器、getter、setter
}
'''
    
    print(f"\n模型定义对比:")
    print("SQLAlchemy:")
    print("- Python类定义，动态类型")
    print("- 声明式映射，代码简洁")
    print("- hybrid_property计算属性")
    print("- 灵活的关系配置")
    
    print(f"\nJPA/Hibernate:")
    print("- Java类定义，静态类型")
    print("- 注解映射，类型安全")
    print("- @Transient计算属性")
    print("- 成熟的关系映射")
    print()


def demo_relationships():
    """演示关系映射和复杂查询"""
    print("=== 3. 关系映射和复杂查询 ===")
    
    relationships_example = '''
# SQLAlchemy关系映射和查询示例

from sqlalchemy.orm import Session, joinedload, selectinload, contains_eager
from sqlalchemy import func, and_, or_, case, desc, asc
from sqlalchemy.sql import select

# 假设我们已有session实例
session = Session()

# 1. 基本查询
def basic_queries():
    """基本查询示例"""
    
    # 查询所有用户
    users = session.query(User).all()
    
    # 条件查询
    active_users = session.query(User).filter(User.is_active == True).all()
    
    # 多条件查询
    admin_users = session.query(User).filter(
        and_(User.is_active == True, User.is_admin == True)
    ).all()
    
    # 模糊查询
    search_users = session.query(User).filter(
        User.username.like('%admin%')
    ).all()
    
    # 排序查询
    sorted_users = session.query(User).order_by(User.created_at.desc()).all()
    
    # 分页查询
    page_users = session.query(User).offset(10).limit(20).all()
    
    # 单个对象查询
    user = session.query(User).filter_by(username='admin').first()
    user_by_id = session.get(User, 1)  # SQLAlchemy 1.4+新语法
    
    return users, active_users, admin_users

# 2. 关系查询
def relationship_queries():
    """关系查询示例"""
    
    # 预加载关系（避免N+1问题）
    
    # joinedload - 使用JOIN查询
    products_with_category = session.query(Product).options(
        joinedload(Product.category),
        joinedload(Product.created_by)
    ).all()
    
    # selectinload - 使用IN查询
    products_with_images = session.query(Product).options(
        selectinload(Product.images)
    ).all()
    
    # 嵌套预加载
    orders_with_details = session.query(Order).options(
        joinedload(Order.customer),
        selectinload(Order.order_items).joinedload(OrderItem.product)
    ).all()
    
    # 关系过滤
    products_in_category = session.query(Product).join(Category).filter(
        Category.name == '电子产品'
    ).all()
    
    # 反向关系查询
    category_with_products = session.query(Category).filter(
        Category.products.any(Product.status == ProductStatus.PUBLISHED)
    ).all()
    
    # 关联表查询
    users_with_orders = session.query(User).filter(
        User.orders.any(Order.status == OrderStatus.DELIVERED)
    ).all()
    
    return products_with_category, orders_with_details

# 3. 聚合查询
def aggregation_queries():
    """聚合查询示例"""
    
    # 计数查询
    user_count = session.query(func.count(User.id)).scalar()
    active_user_count = session.query(func.count(User.id)).filter(
        User.is_active == True
    ).scalar()
    
    # 分组聚合
    category_stats = session.query(
        Category.name,
        func.count(Product.id).label('product_count'),
        func.avg(Product.price).label('avg_price'),
        func.sum(Product.stock_quantity).label('total_stock')
    ).join(Product).group_by(Category.id, Category.name).all()
    
    # 条件聚合
    order_stats = session.query(
        func.count(Order.id).label('total_orders'),
        func.sum(case([(Order.status == OrderStatus.DELIVERED, 1)], else_=0)).label('completed_orders'),
        func.avg(Order.total_amount).label('avg_order_value'),
        func.sum(Order.total_amount).label('total_revenue')
    ).scalar()
    
    # 时间分组
    monthly_sales = session.query(
        func.date_trunc('month', Order.created_at).label('month'),
        func.count(Order.id).label('order_count'),
        func.sum(Order.total_amount).label('revenue')
    ).filter(
        Order.status == OrderStatus.DELIVERED,
        Order.created_at >= datetime.utcnow() - timedelta(days=365)
    ).group_by(
        func.date_trunc('month', Order.created_at)
    ).order_by('month').all()
    
    return category_stats, monthly_sales

# 4. 子查询
def subquery_examples():
    """子查询示例"""
    
    # 子查询
    avg_price_subq = session.query(
        func.avg(Product.price).label('avg_price')
    ).subquery()
    
    expensive_products = session.query(Product).filter(
        Product.price > session.query(avg_price_subq.c.avg_price)
    ).all()
    
    # 相关子查询
    categories_with_products = session.query(Category).filter(
        session.query(Product.id).filter(
            Product.category_id == Category.id,
            Product.status == ProductStatus.PUBLISHED
        ).exists()
    ).all()
    
    # CTE（公共表表达式）
    from sqlalchemy import text
    
    recursive_category_cte = session.execute(text("""
        WITH RECURSIVE category_tree AS (
            SELECT id, name, parent_id, 0 as level
            FROM categories 
            WHERE parent_id IS NULL
            
            UNION ALL
            
            SELECT c.id, c.name, c.parent_id, ct.level + 1
            FROM categories c
            JOIN category_tree ct ON c.parent_id = ct.id
        )
        SELECT * FROM category_tree ORDER BY level, name
    """)).fetchall()
    
    return expensive_products, categories_with_products

# 5. 复杂连接查询
def complex_join_queries():
    """复杂连接查询"""
    
    # 多表连接
    user_order_stats = session.query(
        User.username,
        User.email,
        func.count(Order.id).label('order_count'),
        func.sum(Order.total_amount).label('total_spent'),
        func.max(Order.created_at).label('last_order_date')
    ).join(Order, User.id == Order.customer_id)\
     .filter(User.is_active == True)\
     .group_by(User.id, User.username, User.email)\
     .having(func.count(Order.id) > 0)\
     .order_by(desc('total_spent'))\
     .all()
    
    # 左连接
    all_users_with_order_count = session.query(
        User.username,
        User.email,
        func.coalesce(func.count(Order.id), 0).label('order_count')
    ).outerjoin(Order)\
     .group_by(User.id, User.username, User.email)\
     .all()
    
    # 自连接（查找同分类商品）
    Product1 = aliased(Product)
    Product2 = aliased(Product)
    
    related_products = session.query(
        Product1.name.label('product1'),
        Product2.name.label('product2'),
        Product1.price.label('price1'),
        Product2.price.label('price2')
    ).join(
        Product2, 
        and_(
            Product1.category_id == Product2.category_id,
            Product1.id != Product2.id
        )
    ).filter(
        Product1.status == ProductStatus.PUBLISHED,
        Product2.status == ProductStatus.PUBLISHED
    ).all()
    
    return user_order_stats, related_products

# 6. 窗口函数
def window_function_queries():
    """窗口函数查询"""
    
    from sqlalchemy import func
    
    # 排名函数
    product_rankings = session.query(
        Product.name,
        Product.price,
        Category.name.label('category_name'),
        func.row_number().over(
            partition_by=Product.category_id,
            order_by=Product.price.desc()
        ).label('price_rank'),
        func.dense_rank().over(
            partition_by=Product.category_id,
            order_by=Product.price.desc()
        ).label('dense_rank')
    ).join(Category)\
     .filter(Product.status == ProductStatus.PUBLISHED)\
     .all()
    
    # 累计计算
    running_totals = session.query(
        Order.order_number,
        Order.created_at,
        Order.total_amount,
        func.sum(Order.total_amount).over(
            order_by=Order.created_at,
            rows=(None, 0)  # 从开始到当前行
        ).label('running_total')
    ).filter(
        Order.status == OrderStatus.DELIVERED
    ).order_by(Order.created_at).all()
    
    return product_rankings, running_totals

# 7. 批量操作
def bulk_operations():
    """批量操作示例"""
    
    # 批量插入
    products_to_insert = [
        Product(name=f'Product {i}', price=100.0 + i, category_id=1, created_by_id=1)
        for i in range(1000)
    ]
    session.bulk_save_objects(products_to_insert)
    
    # 批量更新
    session.query(Product).filter(
        Product.category_id == 1
    ).update({
        Product.price: Product.price * 1.1  # 涨价10%
    }, synchronize_session=False)
    
    # 批量删除
    session.query(Product).filter(
        and_(
            Product.status == ProductStatus.DRAFT,
            Product.created_at < datetime.utcnow() - timedelta(days=30)
        )
    ).delete(synchronize_session=False)
    
    session.commit()

# 8. 原生SQL查询
def raw_sql_queries():
    """原生SQL查询"""
    
    # 执行原生SQL
    result = session.execute(text("""
        SELECT 
            c.name as category_name,
            COUNT(p.id) as product_count,
            AVG(p.price) as avg_price,
            SUM(CASE WHEN p.stock_quantity > 0 THEN 1 ELSE 0 END) as in_stock_count
        FROM categories c
        LEFT JOIN products p ON c.id = p.category_id
        WHERE c.is_active = :is_active
        GROUP BY c.id, c.name
        ORDER BY product_count DESC
    """), {'is_active': True}).fetchall()
    
    # 映射到模型
    from sqlalchemy.orm import Query
    
    products = session.query(Product).from_statement(text("""
        SELECT * FROM products 
        WHERE price > :min_price 
        ORDER BY created_at DESC
    """)).params(min_price=100).all()
    
    return result, products
'''
    
    print("SQLAlchemy查询特点:")
    print("1. 链式查询API，表达力强")
    print("2. 预加载策略避免N+1问题")
    print("3. 丰富的聚合和窗口函数支持")
    print("4. 子查询和CTE支持")
    print("5. 批量操作优化性能")
    print("6. 原生SQL无缝集成")
    
    # JPA查询对比
    jpa_query_example = '''
// JPA查询对比

@Repository
public class ProductRepositoryImpl {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    // 1. 基本查询
    public List<Product> findActiveProducts() {
        return entityManager.createQuery(
            "SELECT p FROM Product p WHERE p.status = :status",
            Product.class
        ).setParameter("status", ProductStatus.PUBLISHED)
         .getResultList();
    }
    
    // 2. 关系查询（预加载）
    public List<Product> findProductsWithCategory() {
        return entityManager.createQuery(
            "SELECT p FROM Product p " +
            "JOIN FETCH p.category " +
            "JOIN FETCH p.createdBy " +
            "WHERE p.status = :status",
            Product.class
        ).setParameter("status", ProductStatus.PUBLISHED)
         .getResultList();
    }
    
    // 3. 聚合查询
    public List<Object[]> getCategoryStats() {
        return entityManager.createQuery(
            "SELECT c.name, COUNT(p), AVG(p.price), SUM(p.stockQuantity) " +
            "FROM Category c LEFT JOIN c.products p " +
            "GROUP BY c.id, c.name"
        ).getResultList();
    }
    
    // 4. 子查询
    public List<Product> findExpensiveProducts() {
        return entityManager.createQuery(
            "SELECT p FROM Product p " +
            "WHERE p.price > (SELECT AVG(p2.price) FROM Product p2)",
            Product.class
        ).getResultList();
    }
    
    // 5. Criteria API（类型安全查询）
    public List<Product> findProductsByCriteria(ProductSearchCriteria criteria) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Product> query = cb.createQuery(Product.class);
        Root<Product> product = query.from(Product.class);
        
        List<Predicate> predicates = new ArrayList<>();
        
        if (criteria.getName() != null) {
            predicates.add(cb.like(
                cb.lower(product.get("name")),
                "%" + criteria.getName().toLowerCase() + "%"
            ));
        }
        
        if (criteria.getCategoryId() != null) {
            predicates.add(cb.equal(
                product.get("category").get("id"),
                criteria.getCategoryId()
            ));
        }
        
        if (criteria.getMinPrice() != null) {
            predicates.add(cb.greaterThanOrEqualTo(
                product.get("price"),
                criteria.getMinPrice()
            ));
        }
        
        query.where(predicates.toArray(new Predicate[0]));
        query.orderBy(cb.desc(product.get("createdAt")));
        
        return entityManager.createQuery(query).getResultList();
    }
    
    // 6. 批量操作
    @Modifying
    @Query("UPDATE Product p SET p.price = p.price * 1.1 WHERE p.category.id = :categoryId")
    int increasePriceByCategory(@Param("categoryId") Long categoryId);
    
    @Modifying
    @Query("DELETE FROM Product p WHERE p.status = 'DRAFT' AND p.createdAt < :date")
    int deleteOldDrafts(@Param("date") LocalDateTime date);
    
    // 7. 原生SQL
    @Query(value = """
        SELECT c.name as category_name,
               COUNT(p.id) as product_count,
               AVG(p.price) as avg_price
        FROM categories c
        LEFT JOIN products p ON c.id = p.category_id
        WHERE c.is_active = :isActive
        GROUP BY c.id, c.name
        ORDER BY product_count DESC
        """, nativeQuery = true)
    List<Object[]> getCategoryStatsNative(@Param("isActive") boolean isActive);
}

// Spring Data JPA Repository
public interface ProductRepository extends JpaRepository<Product, Long>, 
                                         JpaSpecificationExecutor<Product> {
    
    // 方法名查询
    List<Product> findByStatusAndCategoryId(ProductStatus status, Long categoryId);
    
    List<Product> findByNameContainingIgnoreCaseAndStatus(String name, ProductStatus status);
    
    // 自定义查询
    @Query("SELECT p FROM Product p WHERE p.price BETWEEN :minPrice AND :maxPrice")
    List<Product> findByPriceRange(@Param("minPrice") BigDecimal minPrice, 
                                 @Param("maxPrice") BigDecimal maxPrice);
    
    // 投影查询
    @Query("SELECT new com.example.dto.ProductSummary(p.name, p.price, c.name) " +
           "FROM Product p JOIN p.category c WHERE p.status = :status")
    List<ProductSummary> findProductSummaries(@Param("status") ProductStatus status);
    
    // 分页查询
    Page<Product> findByStatus(ProductStatus status, Pageable pageable);
}
'''
    
    print(f"\n查询能力对比:")
    print("SQLAlchemy:")
    print("- Python风格的链式API")
    print("- 动态查询构建")
    print("- 强大的关系预加载")
    print("- 函数式查询表达")
    
    print(f"\nJPA/Hibernate:")
    print("- JPQL和Criteria API")
    print("- 类型安全查询")
    print("- 丰富的注解查询")
    print("- 成熟的缓存机制")
    print()


def main():
    """主函数：运行所有演示"""
    print("SQLAlchemy ORM完整学习指南")
    print("=" * 50)
    
    demo_sqlalchemy_setup()
    demo_model_definition()
    demo_relationships()
    
    print("学习总结:")
    print("1. SQLAlchemy提供完整的ORM解决方案")
    print("2. 声明式模型定义，支持复杂关系映射")
    print("3. 强大的查询API，支持复杂业务场景")
    print("4. 灵活的会话管理和事务控制")
    print("5. 与JPA相比更Pythonic，学习曲线更平缓")
    print("6. 适合Python生态，与Web框架无缝集成")


if __name__ == "__main__":
    main() 