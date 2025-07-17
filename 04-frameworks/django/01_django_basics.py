#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Django框架基础学习
Django Framework Basics

作者: Python学习项目
日期: 2024-01-16
描述: Django框架基础概念、项目结构、MVT模式和与Spring Boot的详细对比

学习目标:
1. 掌握Django项目结构和基本配置
2. 理解MVT(Model-View-Template)架构模式
3. 学会Django的核心组件使用
4. 对比Django与Spring Boot的设计理念和实现方式

注意：本文件主要展示概念和配置，实际运行需要创建Django项目
"""

# Django项目结构示例
"""
myproject/                    # 项目根目录
├── manage.py                # Django管理脚本
├── myproject/               # 项目配置包
│   ├── __init__.py
│   ├── settings.py          # 项目设置
│   ├── urls.py              # URL路由配置
│   ├── wsgi.py              # WSGI配置
│   └── asgi.py              # ASGI配置（异步支持）
├── myapp/                   # 应用模块
│   ├── __init__.py
│   ├── admin.py             # 管理后台配置
│   ├── apps.py              # 应用配置
│   ├── models.py            # 数据模型
│   ├── views.py             # 视图逻辑
│   ├── urls.py              # 应用URL配置
│   ├── tests.py             # 测试
│   ├── migrations/          # 数据库迁移
│   │   └── __init__.py
│   └── templates/           # 模板文件
│       └── myapp/
│           └── index.html
├── static/                  # 静态文件
│   ├── css/
│   ├── js/
│   └── images/
└── requirements.txt         # 依赖列表

对比Spring Boot项目结构:
src/
├── main/
│   ├── java/
│   │   └── com/example/demo/
│   │       ├── DemoApplication.java     # 主启动类
│   │       ├── controller/              # 控制器层
│   │       ├── service/                 # 服务层
│   │       ├── repository/              # 数据访问层
│   │       └── model/                   # 实体类
│   └── resources/
│       ├── application.properties       # 配置文件
│       ├── static/                      # 静态资源
│       └── templates/                   # 模板文件
└── test/                                # 测试代码
"""


def demo_django_project_setup():
    """演示Django项目设置和配置"""
    print("=== 1. Django项目设置和配置 ===")
    
    # Django settings.py 核心配置示例
    django_settings_example = """
# settings.py - Django项目核心配置

import os
from pathlib import Path

# 项目基础路径
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全配置
SECRET_KEY = 'your-secret-key-here'
DEBUG = True  # 开发模式
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 应用注册
INSTALLED_APPS = [
    'django.contrib.admin',          # 管理后台
    'django.contrib.auth',           # 认证系统
    'django.contrib.contenttypes',   # 内容类型
    'django.contrib.sessions',       # 会话管理
    'django.contrib.messages',       # 消息框架
    'django.contrib.staticfiles',    # 静态文件
    
    # 第三方应用
    'rest_framework',                # DRF API框架
    'corsheaders',                   # 跨域支持
    
    # 自定义应用
    'myapp',                         # 自定义应用
    'accounts',                      # 用户管理
]

# 中间件配置
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL配置
ROOT_URLCONF = 'myproject.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myproject_db',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'MAX_CONNS': 20,
        }
    }
}

# 国际化配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# 静态文件配置
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# 缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# REST Framework配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
"""
    
    print("Django配置文件特点:")
    print("1. 集中式配置：所有配置都在settings.py中")
    print("2. 应用注册：INSTALLED_APPS列出所有应用模块")
    print("3. 中间件栈：请求处理的中间件链")
    print("4. 数据库配置：支持多数据库配置")
    print("5. 国际化支持：内置多语言和时区支持")
    
    # Spring Boot配置对比
    spring_boot_config_example = """
# application.properties - Spring Boot配置

# 服务器配置
server.port=8080
server.servlet.context-path=/api

# 数据库配置
spring.datasource.url=jdbc:postgresql://localhost:5432/myproject_db
spring.datasource.username=myuser
spring.datasource.password=mypassword
spring.datasource.driver-class-name=org.postgresql.Driver

# 连接池配置
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000

# JPA配置
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect

# 缓存配置
spring.cache.type=redis
spring.redis.host=localhost
spring.redis.port=6379
spring.redis.database=1

# 日志配置
logging.level.com.example=INFO
logging.file.name=application.log

# 国际化配置
spring.messages.basename=messages
spring.web.locale=zh_CN

# 静态资源配置
spring.web.resources.static-locations=classpath:/static/
spring.web.resources.cache.period=3600
"""
    
    print(f"\nSpring Boot配置对比:")
    print("1. 属性文件配置：使用.properties或.yml文件")
    print("2. 自动配置：基于classpath自动配置组件")
    print("3. 配置分离：可以按环境分离配置文件")
    print("4. 外部化配置：支持环境变量、命令行参数等")
    
    print(f"\n配置管理对比:")
    print("Django: 集中式配置，Python代码形式，灵活但可能混乱")
    print("Spring Boot: 分层配置，属性文件形式，结构化但相对固化")
    print()


def demo_django_mvt_pattern():
    """演示Django的MVT模式"""
    print("=== 2. Django MVT模式 ===")
    
    # Model层示例 (models.py)
    models_example = """
# models.py - 数据模型层

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    \"\"\"商品分类模型\"\"\"
    name = models.CharField('分类名称', max_length=100, unique=True)
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    is_active = models.BooleanField('是否激活', default=True)
    
    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    \"\"\"商品模型\"\"\"
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('discontinued', '已下架'),
    ]
    
    name = models.CharField('商品名称', max_length=200)
    slug = models.SlugField('URL标识', unique=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name='分类',
        related_name='products'
    )
    description = models.TextField('商品描述')
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField('库存数量', default=0)
    status = models.CharField(
        '状态', 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='创建者'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def is_in_stock(self):
        \"\"\"是否有库存\"\"\"
        return self.stock_quantity > 0
    
    def reduce_stock(self, quantity):
        \"\"\"减少库存\"\"\"
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
            return True
        return False


class Order(models.Model):
    \"\"\"订单模型\"\"\"
    ORDER_STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('cancelled', '已取消'),
    ]
    
    order_number = models.CharField('订单号', max_length=50, unique=True)
    customer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='客户',
        related_name='orders'
    )
    products = models.ManyToManyField(
        Product, 
        through='OrderItem', 
        verbose_name='商品'
    )
    total_amount = models.DecimalField('总金额', max_digits=10, decimal_places=2)
    status = models.CharField(
        '订单状态', 
        max_length=20, 
        choices=ORDER_STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'订单 {self.order_number}'


class OrderItem(models.Model):
    \"\"\"订单项模型\"\"\"
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField('数量')
    unit_price = models.DecimalField('单价', max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = '订单项'
        unique_together = ['order', 'product']
    
    @property
    def total_price(self):
        \"\"\"小计\"\"\"
        return self.quantity * self.unit_price
"""
    
    # View层示例 (views.py)
    views_example = """
# views.py - 视图层

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import Product, Category, Order
from .forms import ProductForm, OrderForm


# 函数式视图
def product_list(request):
    \"\"\"商品列表视图\"\"\"
    # 获取查询参数
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort', '-created_at')
    
    # 构建查询
    products = Product.objects.filter(status='published')
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # 排序
    products = products.order_by(sort_by)
    
    # 分页
    paginator = Paginator(products, 12)  # 每页12个商品
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 获取分类列表
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_id,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'products/list.html', context)


def product_detail(request, slug):
    \"\"\"商品详情视图\"\"\"
    product = get_object_or_404(Product, slug=slug, status='published')
    
    # 相关商品推荐
    related_products = Product.objects.filter(
        category=product.category,
        status='published'
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'products/detail.html', context)


@login_required
@require_http_methods(["POST"])
def add_to_cart(request, product_id):
    \"\"\"添加到购物车（Ajax视图）\"\"\"
    try:
        product = get_object_or_404(Product, id=product_id, status='published')
        quantity = int(request.POST.get('quantity', 1))
        
        if not product.is_in_stock:
            return JsonResponse({
                'success': False, 
                'message': '商品缺货'
            })
        
        if quantity > product.stock_quantity:
            return JsonResponse({
                'success': False, 
                'message': f'库存不足，仅剩{product.stock_quantity}件'
            })
        
        # 添加到购物车逻辑（这里简化）
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart
        
        return JsonResponse({
            'success': True,
            'message': '已添加到购物车',
            'cart_count': sum(cart.values())
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': '操作失败'
        })


# 类式视图
class ProductListView(ListView):
    \"\"\"商品列表类式视图\"\"\"
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(status='published')
        
        # 处理搜索
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # 处理分类筛选
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # 处理排序
        sort_by = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('search')
        return context


class ProductDetailView(DetailView):
    \"\"\"商品详情类式视图\"\"\"
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        
        # 相关商品
        context['related_products'] = Product.objects.filter(
            category=product.category,
            status='published'
        ).exclude(id=product.id)[:4]
        
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    \"\"\"商品创建视图\"\"\"
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@login_required
def order_dashboard(request):
    \"\"\"订单仪表板\"\"\"
    # 获取用户订单统计
    user_orders = Order.objects.filter(customer=request.user)
    
    order_stats = user_orders.aggregate(
        total_orders=Count('id'),
        total_spent=Sum('total_amount'),
        pending_orders=Count('id', filter=Q(status='pending')),
        completed_orders=Count('id', filter=Q(status='delivered'))
    )
    
    # 最近订单
    recent_orders = user_orders.order_by('-created_at')[:5]
    
    context = {
        'order_stats': order_stats,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'orders/dashboard.html', context)
"""
    
    # Template层示例
    template_example = """
<!-- products/list.html - 模板层 -->

{% extends 'base.html' %}
{% load static %}

{% block title %}商品列表{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/products.css' %}">
{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <!-- 侧边栏筛选 -->
        <div class="col-md-3">
            <div class="sidebar">
                <h5>商品分类</h5>
                <ul class="list-unstyled">
                    <li>
                        <a href="{% url 'products:list' %}" 
                           class="{% if not current_category %}active{% endif %}">
                            全部分类
                        </a>
                    </li>
                    {% for category in categories %}
                    <li>
                        <a href="{% url 'products:list' %}?category={{ category.id }}" 
                           class="{% if current_category == category.id|stringformat:'s' %}active{% endif %}">
                            {{ category.name }}
                            <span class="badge">{{ category.products.count }}</span>
                        </a>
                    </li>
                    {% endfor %}
                </ul>
                
                <h5>价格排序</h5>
                <ul class="list-unstyled">
                    <li><a href="?sort=price">价格从低到高</a></li>
                    <li><a href="?sort=-price">价格从高到低</a></li>
                    <li><a href="?sort=-created_at">最新发布</a></li>
                </ul>
            </div>
        </div>
        
        <!-- 主内容区 -->
        <div class="col-md-9">
            <!-- 搜索栏 -->
            <div class="search-bar mb-4">
                <form method="get" class="d-flex">
                    <input type="text" name="search" class="form-control" 
                           placeholder="搜索商品..." value="{{ search_query }}">
                    <button type="submit" class="btn btn-primary">搜索</button>
                </form>
            </div>
            
            <!-- 商品列表 -->
            <div class="row">
                {% for product in page_obj %}
                <div class="col-md-4 mb-4">
                    <div class="card product-card">
                        <img src="{{ product.image.url|default:'/static/images/no-image.png' }}" 
                             class="card-img-top" alt="{{ product.name }}">
                        <div class="card-body">
                            <h6 class="card-title">
                                <a href="{% url 'products:detail' product.slug %}">
                                    {{ product.name }}
                                </a>
                            </h6>
                            <p class="card-text text-muted">
                                {{ product.description|truncatechars:60 }}
                            </p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="price">¥{{ product.price }}</span>
                                <small class="text-muted">库存: {{ product.stock_quantity }}</small>
                            </div>
                            <div class="mt-2">
                                {% if product.is_in_stock %}
                                <button class="btn btn-sm btn-primary add-to-cart" 
                                        data-product-id="{{ product.id }}">
                                    加入购物车
                                </button>
                                {% else %}
                                <button class="btn btn-sm btn-secondary" disabled>
                                    暂时缺货
                                </button>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
                {% empty %}
                <div class="col-12">
                    <div class="alert alert-info">
                        没有找到相关商品。
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <!-- 分页 -->
            {% if page_obj.has_other_pages %}
            <nav aria-label="商品分页">
                <ul class="pagination justify-content-center">
                    {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}">
                            上一页
                        </a>
                    </li>
                    {% endif %}
                    
                    {% for num in page_obj.paginator.page_range %}
                    {% if page_obj.number == num %}
                    <li class="page-item active">
                        <span class="page-link">{{ num }}</span>
                    </li>
                    {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ num }}">{{ num }}</a>
                    </li>
                    {% endif %}
                    {% endfor %}
                    
                    {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}">
                            下一页
                        </a>
                    </li>
                    {% endif %}
                </ul>
            </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
// 添加到购物车功能
document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            
            fetch(`/products/${productId}/add-to-cart/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: 'quantity=1'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 显示成功消息
                    showMessage(data.message, 'success');
                    // 更新购物车数量
                    updateCartCount(data.cart_count);
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(error => {
                showMessage('操作失败，请重试', 'error');
            });
        });
    });
});

function showMessage(message, type) {
    // 显示消息的实现
    const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const alertDiv = `<div class="alert ${alertClass} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>`;
    
    document.querySelector('.container').insertAdjacentHTML('afterbegin', alertDiv);
}

function updateCartCount(count) {
    const cartCountElement = document.querySelector('.cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = count;
    }
}
</script>
{% endblock %}
"""
    
    print("Django MVT模式特点:")
    print("1. Model（模型）：数据层，定义数据结构和业务逻辑")
    print("2. View（视图）：控制层，处理请求逻辑和数据流转")
    print("3. Template（模板）：展示层，负责UI渲染和用户交互")
    print("4. URL配置：路由分发，连接URL和视图函数")
    
    # Spring Boot MVC对比
    spring_boot_mvc_example = """
// Spring Boot MVC对比

// 1. Model层 - Entity + Repository
@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    @Column(unique = true)
    private String slug;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id")
    private Category category;
    
    @Column(columnDefinition = "TEXT")
    private String description;
    
    @Column(precision = 10, scale = 2)
    private BigDecimal price;
    
    @Column(name = "stock_quantity")
    private Integer stockQuantity = 0;
    
    @Enumerated(EnumType.STRING)
    private ProductStatus status = ProductStatus.DRAFT;
    
    @CreationTimestamp
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    private LocalDateTime updatedAt;
    
    // 构造器、getter、setter、业务方法
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
}

// Repository层
public interface ProductRepository extends JpaRepository<Product, Long> {
    List<Product> findByStatusAndCategory(ProductStatus status, Category category);
    
    Page<Product> findByStatusAndNameContainingOrDescriptionContaining(
        ProductStatus status, String name, String description, Pageable pageable
    );
    
    @Query("SELECT p FROM Product p WHERE p.status = :status " +
           "AND (:categoryId IS NULL OR p.category.id = :categoryId)")
    Page<Product> findProducts(
        @Param("status") ProductStatus status,
        @Param("categoryId") Long categoryId,
        Pageable pageable
    );
}

// 2. Controller层 - 对应Django View
@Controller
@RequestMapping("/products")
public class ProductController {
    
    @Autowired
    private ProductService productService;
    
    @GetMapping
    public String productList(
            @RequestParam(required = false) Long category,
            @RequestParam(required = false) String search,
            @RequestParam(defaultValue = "createdAt") String sort,
            @RequestParam(defaultValue = "desc") String direction,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "12") int size,
            Model model) {
        
        // 构建分页和排序
        Sort.Direction sortDirection = "desc".equals(direction) ? 
            Sort.Direction.DESC : Sort.Direction.ASC;
        Pageable pageable = PageRequest.of(page, size, Sort.by(sortDirection, sort));
        
        // 获取商品分页数据
        Page<Product> productPage = productService.findProducts(
            category, search, pageable
        );
        
        // 获取分类列表
        List<Category> categories = categoryService.findActiveCategories();
        
        // 添加到模型
        model.addAttribute("productPage", productPage);
        model.addAttribute("categories", categories);
        model.addAttribute("currentCategory", category);
        model.addAttribute("searchQuery", search);
        model.addAttribute("currentSort", sort);
        model.addAttribute("currentDirection", direction);
        
        return "products/list";  // 返回模板名称
    }
    
    @GetMapping("/{slug}")
    public String productDetail(@PathVariable String slug, Model model) {
        Product product = productService.findBySlug(slug)
            .orElseThrow(() -> new ProductNotFoundException("商品不存在"));
        
        List<Product> relatedProducts = productService
            .findRelatedProducts(product, 4);
        
        model.addAttribute("product", product);
        model.addAttribute("relatedProducts", relatedProducts);
        
        return "products/detail";
    }
    
    @PostMapping("/{productId}/add-to-cart")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> addToCart(
            @PathVariable Long productId,
            @RequestParam(defaultValue = "1") int quantity,
            HttpSession session) {
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            Product product = productService.findById(productId)
                .orElseThrow(() -> new ProductNotFoundException("商品不存在"));
            
            if (!product.isInStock()) {
                response.put("success", false);
                response.put("message", "商品缺货");
                return ResponseEntity.ok(response);
            }
            
            if (quantity > product.getStockQuantity()) {
                response.put("success", false);
                response.put("message", "库存不足，仅剩" + product.getStockQuantity() + "件");
                return ResponseEntity.ok(response);
            }
            
            // 添加到购物车
            Cart cart = cartService.getOrCreateCart(session);
            cartService.addItem(cart, product, quantity);
            
            response.put("success", true);
            response.put("message", "已添加到购物车");
            response.put("cartCount", cart.getTotalItems());
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            response.put("success", false);
            response.put("message", "操作失败");
            return ResponseEntity.ok(response);
        }
    }
}

// 3. Service层 - Django没有明确对应
@Service
@Transactional
public class ProductService {
    
    @Autowired
    private ProductRepository productRepository;
    
    public Page<Product> findProducts(Long categoryId, String search, Pageable pageable) {
        if (search != null && !search.trim().isEmpty()) {
            return productRepository.findByStatusAndNameContainingOrDescriptionContaining(
                ProductStatus.PUBLISHED, search, search, pageable
            );
        } else {
            return productRepository.findProducts(ProductStatus.PUBLISHED, categoryId, pageable);
        }
    }
    
    public Optional<Product> findBySlug(String slug) {
        return productRepository.findBySlugAndStatus(slug, ProductStatus.PUBLISHED);
    }
    
    public List<Product> findRelatedProducts(Product product, int limit) {
        return productRepository.findByStatusAndCategoryAndIdNot(
            ProductStatus.PUBLISHED, product.getCategory(), product.getId(),
            PageRequest.of(0, limit)
        ).getContent();
    }
}
"""
    
    print(f"\nMVT vs MVC模式对比:")
    print("Django MVT:")
    print("- Model: 数据模型 + 业务逻辑")
    print("- View: 控制逻辑 + 数据处理")
    print("- Template: 展示逻辑")
    print("- URL配置: 路由分发")
    
    print(f"\nSpring Boot MVC:")
    print("- Model: 数据模型（Entity）")
    print("- View: 模板或JSON响应")
    print("- Controller: 控制逻辑")
    print("- Service: 业务逻辑")
    print("- Repository: 数据访问")
    
    print(f"\n架构对比:")
    print("Django: 更偏向快速开发，集成度高，约定大于配置")
    print("Spring Boot: 更偏向企业级，分层清晰，灵活性更高")
    print()


def demo_django_orm():
    """演示Django ORM"""
    print("=== 3. Django ORM ===")
    
    orm_examples = """
# Django ORM查询示例

from django.db.models import Q, F, Count, Sum, Avg, Max, Min
from django.db.models import Case, When, Value, IntegerField
from datetime import datetime, timedelta

# 1. 基本查询
# 获取所有已发布商品
products = Product.objects.filter(status='published')

# 获取特定分类的商品
electronics = Product.objects.filter(category__name='电子产品')

# 排除特定条件
expensive_products = Product.objects.exclude(price__lt=100)

# 获取单个对象
product = Product.objects.get(slug='iphone-14')
# 安全获取（不存在时返回None）
product = Product.objects.filter(slug='iphone-14').first()

# 2. 复杂查询条件
# Q对象构建复杂查询
search_query = "iPhone"
products = Product.objects.filter(
    Q(name__icontains=search_query) | 
    Q(description__icontains=search_query),
    status='published',
    price__gte=100
)

# F对象引用字段
# 查找价格高于成本价2倍的商品
expensive = Product.objects.filter(price__gt=F('cost') * 2)

# 库存低于安全库存的商品
low_stock = Product.objects.filter(stock_quantity__lt=F('min_stock'))

# 3. 聚合查询
from django.db.models import Count, Sum, Avg

# 统计每个分类的商品数量
category_stats = Category.objects.annotate(
    product_count=Count('products'),
    avg_price=Avg('products__price'),
    total_stock=Sum('products__stock_quantity')
)

# 用户订单统计
user_stats = User.objects.annotate(
    order_count=Count('orders'),
    total_spent=Sum('orders__total_amount'),
    last_order_date=Max('orders__created_at')
)

# 4. 高级聚合
# 按月统计订单
from django.db.models.functions import TruncMonth
monthly_orders = Order.objects.annotate(
    month=TruncMonth('created_at')
).values('month').annotate(
    order_count=Count('id'),
    total_revenue=Sum('total_amount')
).order_by('month')

# 条件聚合
order_stats = Order.objects.aggregate(
    total_orders=Count('id'),
    pending_orders=Count('id', filter=Q(status='pending')),
    completed_orders=Count('id', filter=Q(status='delivered')),
    avg_order_value=Avg('total_amount'),
    total_revenue=Sum('total_amount', filter=Q(status='delivered'))
)

# 5. 关联查询
# 一对多关联
category_with_products = Category.objects.prefetch_related('products')
for category in category_with_products:
    print(f"{category.name}: {category.products.count()}个商品")

# 多对多关联
orders_with_products = Order.objects.prefetch_related('products')

# 反向关联
user_orders = User.objects.prefetch_related('orders__products')

# 6. 选择关联
# 避免N+1查询问题
products_with_category = Product.objects.select_related('category', 'created_by')

# 7. 自定义管理器
class ProductManager(models.Manager):
    def published(self):
        return self.filter(status='published')
    
    def in_stock(self):
        return self.filter(stock_quantity__gt=0)
    
    def by_category(self, category_name):
        return self.filter(category__name=category_name)
    
    def search(self, query):
        return self.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )

# 在模型中使用
class Product(models.Model):
    # ... 字段定义 ...
    
    objects = ProductManager()  # 自定义管理器
    
    class Meta:
        # ...

# 使用自定义管理器
published_products = Product.objects.published()
in_stock_electronics = Product.objects.published().in_stock().by_category('电子产品')

# 8. 查询集方法链
recent_expensive_products = Product.objects\\
    .published()\\
    .filter(price__gte=1000)\\
    .order_by('-created_at')\\
    .select_related('category')\\
    [:10]

# 9. 批量操作
# 批量创建
products_to_create = [
    Product(name=f'商品{i}', price=100 + i, category=category)
    for i in range(100)
]
Product.objects.bulk_create(products_to_create, batch_size=50)

# 批量更新
Product.objects.filter(category__name='电子产品').update(
    price=F('price') * 1.1  # 涨价10%
)

# 批量删除
Product.objects.filter(
    status='draft',
    created_at__lt=datetime.now() - timedelta(days=30)
).delete()

# 10. 原生SQL
# 当ORM无法满足需求时
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('''
        SELECT c.name, COUNT(p.id) as product_count, AVG(p.price) as avg_price
        FROM products_category c
        LEFT JOIN products_product p ON c.id = p.category_id
        WHERE p.status = %s
        GROUP BY c.id, c.name
        ORDER BY product_count DESC
    ''', ['published'])
    
    results = cursor.fetchall()

# 或使用raw SQL
categories = Category.objects.raw('''
    SELECT c.*, COUNT(p.id) as product_count
    FROM products_category c
    LEFT JOIN products_product p ON c.id = p.category_id
    GROUP BY c.id
''')

# 11. 事务处理
from django.db import transaction

@transaction.atomic
def create_order(user, items):
    # 创建订单
    order = Order.objects.create(
        customer=user,
        order_number=generate_order_number(),
        total_amount=0
    )
    
    total = 0
    for item in items:
        product = Product.objects.select_for_update().get(id=item['product_id'])
        
        if not product.reduce_stock(item['quantity']):
            raise ValueError(f'商品{product.name}库存不足')
        
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            unit_price=product.price
        )
        
        total += item['quantity'] * product.price
    
    order.total_amount = total
    order.save()
    
    return order

# 12. 信号处理
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        # 发送订单确认邮件
        send_order_confirmation_email(instance)

@receiver(pre_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    # 记录删除日志
    logger.info(f'商品被删除: {instance.name}')
"""
    
    print("Django ORM特点:")
    print("1. Active Record模式：模型类直接包含数据库操作方法")
    print("2. 查询集（QuerySet）：延迟执行，支持方法链")
    print("3. 自动反向关联：通过related_name访问反向关系")
    print("4. 丰富的查询API：支持复杂查询条件和聚合")
    print("5. 迁移系统：自动生成和管理数据库schema变更")
    print("6. 信号系统：模型事件的观察者模式")
    
    # JPA对比
    jpa_examples = """
// Spring Boot JPA/Hibernate对比

// 1. 基本查询
List<Product> products = productRepository.findByStatus(ProductStatus.PUBLISHED);

// 自定义查询方法
List<Product> electronics = productRepository.findByCategoryName("电子产品");
List<Product> expensive = productRepository.findByPriceGreaterThanEqual(100);

// 2. 复杂查询
@Query("SELECT p FROM Product p WHERE " +
       "(p.name LIKE %:search% OR p.description LIKE %:search%) " +
       "AND p.status = :status AND p.price >= :minPrice")
List<Product> searchProducts(
    @Param("search") String search,
    @Param("status") ProductStatus status,
    @Param("minPrice") BigDecimal minPrice
);

// 3. 聚合查询
@Query("SELECT c.name, COUNT(p), AVG(p.price), SUM(p.stockQuantity) " +
       "FROM Category c LEFT JOIN c.products p " +
       "GROUP BY c.id, c.name")
List<Object[]> getCategoryStats();

// 4. 投影查询
public interface CategoryStatsProjection {
    String getName();
    Long getProductCount();
    BigDecimal getAveragePrice();
    Integer getTotalStock();
}

@Query("SELECT c.name as name, COUNT(p) as productCount, " +
       "AVG(p.price) as averagePrice, SUM(p.stockQuantity) as totalStock " +
       "FROM Category c LEFT JOIN c.products p " +
       "GROUP BY c.id, c.name")
List<CategoryStatsProjection> getCategoryStatsProjection();

// 5. 批量操作
@Modifying
@Query("UPDATE Product p SET p.price = p.price * 1.1 WHERE p.category.name = :categoryName")
int increasePriceByCategory(@Param("categoryName") String categoryName);

// 6. 事务处理
@Service
@Transactional
public class OrderService {
    
    @Transactional(rollbackFor = Exception.class)
    public Order createOrder(User user, List<OrderItemDto> items) {
        Order order = new Order();
        order.setCustomer(user);
        order.setOrderNumber(generateOrderNumber());
        
        BigDecimal total = BigDecimal.ZERO;
        
        for (OrderItemDto item : items) {
            Product product = productRepository.findById(item.getProductId())
                .orElseThrow(() -> new ProductNotFoundException("商品不存在"));
            
            if (!product.reduceStock(item.getQuantity())) {
                throw new InsufficientStockException("库存不足");
            }
            
            OrderItem orderItem = new OrderItem();
            orderItem.setOrder(order);
            orderItem.setProduct(product);
            orderItem.setQuantity(item.getQuantity());
            orderItem.setUnitPrice(product.getPrice());
            
            order.getOrderItems().add(orderItem);
            total = total.add(product.getPrice().multiply(
                BigDecimal.valueOf(item.getQuantity())));
        }
        
        order.setTotalAmount(total);
        return orderRepository.save(order);
    }
}

// 7. 事件监听
@EventListener
public void handleOrderCreated(OrderCreatedEvent event) {
    Order order = event.getOrder();
    emailService.sendOrderConfirmation(order);
}

// 8. Criteria API（类似Django Q对象）
public List<Product> searchProducts(ProductSearchCriteria criteria) {
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
    
    return entityManager.createQuery(query).getResultList();
}
"""
    
    print(f"\nDjango ORM vs JPA对比:")
    print("Django ORM:")
    print("- Python风格的API，更直观易用")
    print("- Active Record模式，模型就是数据访问对象")
    print("- 查询集延迟执行，支持链式调用")
    print("- 自动化程度高，约定大于配置")
    
    print(f"\nJPA/Hibernate:")
    print("- 更接近SQL的查询语法")
    print("- Repository模式，数据访问层分离")
    print("- 类型安全的Criteria API")
    print("- 更灵活的配置和优化选项")
    
    print(f"\n选择建议:")
    print("Django ORM: 适合快速开发，学习成本低，满足大部分场景")
    print("JPA: 适合复杂企业应用，性能要求高，需要精细控制")
    print()


def main():
    """主函数：运行所有演示"""
    print("Django框架基础学习指南")
    print("=" * 50)
    
    demo_django_project_setup()
    demo_django_mvt_pattern()
    demo_django_orm()
    
    print("学习总结:")
    print("1. Django是全功能Web框架，内置管理后台、ORM、模板引擎")
    print("2. MVT模式清晰分离关注点，快速开发Web应用")
    print("3. Django ORM提供Python风格的数据库操作API")
    print("4. 约定大于配置，适合快速原型和中小型项目")
    print("5. 与Spring Boot相比更偏向快速开发，集成度更高")
    print("6. 学习曲线平缓，文档完善，社区活跃")


if __name__ == "__main__":
    main() 