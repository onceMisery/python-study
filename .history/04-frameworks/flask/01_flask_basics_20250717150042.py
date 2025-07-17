#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flask框架基础学习
Flask Framework Basics

作者: Python学习项目
日期: 2024-01-16
描述: Flask框架轻量级架构、扩展性、蓝图模式和与Spring MVC的详细对比

学习目标:
1. 掌握Flask的微框架理念和核心组件
2. 理解蓝图(Blueprint)模式和应用结构
3. 学会Flask扩展生态和自定义扩展
4. 对比Flask与Spring MVC的设计差异

注意：Flask是微框架，提供核心功能，通过扩展实现完整功能
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask import Blueprint, g, current_app, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from functools import wraps
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


def demo_flask_basic_setup():
    """演示Flask基本设置和核心概念"""
    print("=== 1. Flask基本设置和核心概念 ===")
    
    basic_app_example = '''
# app.py - Flask应用基本设置

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
import os

# 创建Flask应用实例
def create_app(config_name='development'):
    app = Flask(__name__)
    
    # 配置应用
    app.config.from_object(get_config(config_name))
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    CORS(app)
    
    # 注册蓝图
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    return app

# 配置类
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 分页配置
    POSTS_PER_PAGE = 20
    
    # 邮件配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(name):
    return config.get(name, config['default'])

# 全局扩展实例
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请登录后访问此页面。'

# 应用上下文处理器
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# 错误处理器
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# 请求钩子
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.teardown_appcontext
def close_db(error):
    """在应用上下文结束时关闭数据库连接"""
    if hasattr(g, 'db'):
        g.db.close()

# 启动应用
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    print("Flask核心特点:")
    print("1. 微框架理念：提供核心功能，按需扩展")
    print("2. Werkzeug WSGI工具库：处理HTTP请求响应")
    print("3. Jinja2模板引擎：强大的模板系统")
    print("4. 应用工厂模式：支持多环境配置")
    print("5. 简单直观的路由装饰器")
    
    # Spring MVC配置对比
    spring_mvc_config = '''
// Spring MVC配置对比

// 1. 主启动类
@SpringBootApplication
@EnableWebMvc
public class FlaskComparisonApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(FlaskComparisonApplication.class, args);
    }
    
    // 配置视图解析器
    @Bean
    public ViewResolver viewResolver() {
        InternalResourceViewResolver resolver = new InternalResourceViewResolver();
        resolver.setPrefix("/WEB-INF/views/");
        resolver.setSuffix(".jsp");
        return resolver;
    }
    
    // 配置静态资源
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/static/**")
               .addResourceLocations("classpath:/static/");
    }
    
    // 配置拦截器
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new AuthenticationInterceptor())
               .addPathPatterns("/admin/**")
               .excludePathPatterns("/admin/login");
    }
}

// 2. 配置类
@Configuration
@ConfigurationProperties(prefix = "app")
public class AppConfig {
    private String secretKey;
    private int postsPerPage = 20;
    private String mailServer;
    private int mailPort = 587;
    
    // getter、setter
}

// 3. 全局异常处理
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(EntityNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("NOT_FOUND", ex.getMessage());
        return ResponseEntity.status(404).body(error);
    }
    
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidation(ValidationException ex) {
        ErrorResponse error = new ErrorResponse("VALIDATION_ERROR", ex.getMessage());
        return ResponseEntity.status(400).body(error);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneral(Exception ex) {
        ErrorResponse error = new ErrorResponse("INTERNAL_ERROR", "系统内部错误");
        return ResponseEntity.status(500).body(error);
    }
}

// 4. 拦截器（类似Flask before_request）
@Component
public class AuthenticationInterceptor implements HandlerInterceptor {
    
    @Override
    public boolean preHandle(HttpServletRequest request, 
                           HttpServletResponse response, 
                           Object handler) throws Exception {
        
        String token = request.getHeader("Authorization");
        if (token == null || !isValidToken(token)) {
            response.setStatus(401);
            return false;
        }
        
        User user = getUserFromToken(token);
        request.setAttribute("currentUser", user);
        
        return true;
    }
    
    @Override
    public void postHandle(HttpServletRequest request, 
                          HttpServletResponse response, 
                          Object handler, 
                          ModelAndView modelAndView) throws Exception {
        // 请求处理后的逻辑
    }
    
    @Override
    public void afterCompletion(HttpServletRequest request, 
                               HttpServletResponse response, 
                               Object handler, 
                               Exception ex) throws Exception {
        // 请求完成后的清理工作
    }
}
'''
    
    print(f"\n配置方式对比:")
    print("Flask:")
    print("- Python配置类，灵活直观")
    print("- 应用工厂模式，支持多实例")
    print("- 装饰器式路由和中间件")
    print("- 简单的扩展初始化")
    
    print(f"\nSpring MVC:")
    print("- 注解+配置类，类型安全")
    print("- 自动配置+外部配置文件")
    print("- 拦截器链和AOP")
    print("- 复杂但功能完整的配置")
    print()


def demo_flask_blueprints():
    """演示Flask蓝图模式"""
    print("=== 2. Flask蓝图模式 ===")
    
    # 主应用蓝图
    main_blueprint_example = '''
# app/main/__init__.py - 主应用蓝图

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes

# app/main/routes.py - 主应用路由
from flask import render_template, request, current_app, redirect, url_for, flash
from app.main import bp
from app.models import Product, Category
from app import db

@bp.route('/')
@bp.route('/index')
def index():
    """首页"""
    featured_products = Product.query.filter_by(
        status='published', 
        is_featured=True
    ).limit(8).all()
    
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('main/index.html', 
                         featured_products=featured_products,
                         categories=categories)

@bp.route('/products')
def product_list():
    """商品列表页"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '', type=str)
    sort_by = request.args.get('sort', 'created_at', type=str)
    
    # 构建查询
    query = Product.query.filter_by(status='published')
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(
            Product.name.contains(search) | 
            Product.description.contains(search)
        )
    
    # 排序
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())
    
    # 分页
    products = query.paginate(
        page=page, 
        per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('main/products.html',
                         products=products,
                         categories=categories,
                         current_category=category_id,
                         search_query=search,
                         sort_by=sort_by)

@bp.route('/products/<slug>')
def product_detail(slug):
    """商品详情页"""
    product = Product.query.filter_by(slug=slug, status='published').first_or_404()
    
    # 相关商品
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.status == 'published'
    ).limit(4).all()
    
    return render_template('main/product_detail.html',
                         product=product,
                         related_products=related_products)

@bp.route('/search')
def search():
    """搜索页面"""
    query = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return redirect(url_for('main.index'))
    
    # 全文搜索
    products = Product.query.filter(
        Product.status == 'published',
        Product.name.contains(query) | Product.description.contains(query)
    ).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    
    return render_template('main/search_results.html',
                         products=products,
                         query=query)
'''
    
    # 认证蓝图
    auth_blueprint_example = '''
# app/auth/__init__.py - 认证蓝图

from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes

# app/auth/routes.py - 认证路由
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.auth import bp
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm
from app import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # 重定向到原来要访问的页面
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        return redirect(next_page)
    
    return render_template('auth/login.html', title='登录', form=form)

@bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功！')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='注册', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """重置密码请求"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ResetPasswordRequestForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            send_password_reset_email(user)
        
        flash('密码重置邮件已发送，请检查您的邮箱')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_request.html',
                         title='重置密码', form=form)

# 认证装饰器
def admin_required(f):
    """需要管理员权限的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    """需要特定权限的装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
'''
    
    # API蓝图
    api_blueprint_example = '''
# app/api/__init__.py - API蓝图

from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import products, categories, auth, errors

# app/api/products.py - 商品API
from flask import jsonify, request, current_app
from app.api import bp
from app.models import Product, Category
from app.api.auth import token_auth
from app.api.errors import bad_request, not_found
from app import db

@bp.route('/products', methods=['GET'])
def get_products():
    """获取商品列表API"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', type=str)
    
    # 构建查询
    query = Product.query.filter_by(status='published')
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(
            Product.name.contains(search) | 
            Product.description.contains(search)
        )
    
    # 分页
    data = query.paginate(
        page=page, 
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'products': [item.to_dict() for item in data.items],
        'total': data.total,
        'page': page,
        'per_page': per_page,
        'pages': data.pages,
        '_links': {
            'self': url_for('api.get_products', page=page, per_page=per_page),
            'next': url_for('api.get_products', page=page+1, per_page=per_page) 
                   if data.has_next else None,
            'prev': url_for('api.get_products', page=page-1, per_page=per_page) 
                   if data.has_prev else None
        }
    })

@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    """获取单个商品API"""
    product = Product.query.filter_by(id=id, status='published').first()
    
    if not product:
        return not_found('商品不存在')
    
    return jsonify(product.to_dict())

@bp.route('/products', methods=['POST'])
@token_auth.login_required
def create_product():
    """创建商品API"""
    data = request.get_json() or {}
    
    # 验证必需字段
    required_fields = ['name', 'price', 'category_id']
    for field in required_fields:
        if field not in data:
            return bad_request(f'必须包含字段: {field}')
    
    # 验证分类存在
    category = Category.query.get(data['category_id'])
    if not category:
        return bad_request('分类不存在')
    
    # 创建商品
    product = Product()
    product.from_dict(data)
    product.created_by_id = token_auth.current_user().id
    
    db.session.add(product)
    db.session.commit()
    
    response = jsonify(product.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_product', id=product.id)
    
    return response

@bp.route('/products/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_product(id):
    """更新商品API"""
    product = Product.query.get_or_404(id)
    
    # 权限检查
    if product.created_by_id != token_auth.current_user().id and \\
       not token_auth.current_user().is_admin:
        abort(403)
    
    data = request.get_json() or {}
    product.from_dict(data)
    
    db.session.commit()
    
    return jsonify(product.to_dict())

@bp.route('/products/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_product(id):
    """删除商品API"""
    product = Product.query.get_or_404(id)
    
    # 权限检查
    if product.created_by_id != token_auth.current_user().id and \\
       not token_auth.current_user().is_admin:
        abort(403)
    
    db.session.delete(product)
    db.session.commit()
    
    return '', 204

# API错误处理
from app.api import bp

@bp.errorhandler(400)
def bad_request(message):
    return jsonify({'error': 'bad request', 'message': message}), 400

@bp.errorhandler(404)
def not_found(message):
    return jsonify({'error': 'not found', 'message': message}), 404

@bp.errorhandler(403)
def forbidden(message):
    return jsonify({'error': 'forbidden', 'message': message}), 403
'''
    
    print("Flask蓝图特点:")
    print("1. 模块化组织：按功能领域拆分应用")
    print("2. URL前缀：不同蓝图可使用不同URL前缀")
    print("3. 独立的模板和静态文件目录")
    print("4. 灵活的注册机制：可选择性注册蓝图")
    print("5. 支持嵌套蓝图和子应用模式")
    
    # Spring MVC模块化对比
    spring_mvc_modular = '''
// Spring MVC模块化对比

// 1. 控制器分组
@RestController
@RequestMapping("/api/v1/products")
public class ProductController {
    
    @GetMapping
    public ResponseEntity<PagedResponse<ProductResponse>> getProducts(
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) String search,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int size) {
        
        ProductQueryParams params = new ProductQueryParams();
        params.setCategoryId(categoryId);
        params.setSearch(search);
        params.setPage(page);
        params.setSize(size);
        
        PagedResponse<ProductResponse> products = productService.findProducts(params);
        return ResponseEntity.ok(products);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<ProductResponse> getProduct(@PathVariable Long id) {
        ProductResponse product = productService.findById(id);
        return ResponseEntity.ok(product);
    }
    
    @PostMapping
    @PreAuthorize("hasPermission('product', 'create')")
    public ResponseEntity<ProductResponse> createProduct(
            @Valid @RequestBody ProductCreateRequest request) {
        
        ProductResponse product = productService.createProduct(request);
        return ResponseEntity.status(201).body(product);
    }
}

// 2. 认证控制器
@RestController
@RequestMapping("/auth")
public class AuthController {
    
    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        String token = authService.authenticate(request.getUsername(), request.getPassword());
        
        if (token != null) {
            LoginResponse response = new LoginResponse(token, "登录成功");
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.status(401).body(new LoginResponse(null, "用户名或密码错误"));
        }
    }
    
    @PostMapping("/register")
    public ResponseEntity<RegisterResponse> register(@Valid @RequestBody RegisterRequest request) {
        try {
            UserResponse user = userService.createUser(request);
            RegisterResponse response = new RegisterResponse(user, "注册成功");
            return ResponseEntity.status(201).body(response);
        } catch (UserExistsException e) {
            return ResponseEntity.status(409).body(new RegisterResponse(null, "用户已存在"));
        }
    }
    
    @PostMapping("/logout")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Void> logout(HttpServletRequest request) {
        String token = extractToken(request);
        authService.invalidateToken(token);
        return ResponseEntity.ok().build();
    }
}

// 3. 配置类分组
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(authz -> authz
                .requestMatchers("/auth/**").permitAll()
                .requestMatchers("/api/v1/products").permitAll()
                .requestMatchers(HttpMethod.POST, "/api/v1/products").authenticated()
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthenticationFilter(), UsernamePasswordAuthenticationFilter.class)
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .csrf(csrf -> csrf.disable());
        
        return http.build();
    }
}

// 4. 服务层分组
@Service
@Transactional
public class ProductService {
    
    @Autowired
    private ProductRepository productRepository;
    
    @Autowired
    private CategoryRepository categoryRepository;
    
    public PagedResponse<ProductResponse> findProducts(ProductQueryParams params) {
        Specification<Product> spec = buildProductSpecification(params);
        
        Pageable pageable = PageRequest.of(
            params.getPage() - 1, 
            params.getSize(),
            Sort.by(Sort.Direction.DESC, "createdAt")
        );
        
        Page<Product> productPage = productRepository.findAll(spec, pageable);
        
        List<ProductResponse> products = productPage.getContent()
                                                   .stream()
                                                   .map(this::toProductResponse)
                                                   .collect(Collectors.toList());
        
        return new PagedResponse<>(
            products,
            productPage.getTotalElements(),
            params.getPage(),
            params.getSize(),
            productPage.getTotalPages()
        );
    }
}
'''
    
    print(f"\n模块化组织对比:")
    print("Flask蓝图:")
    print("- 轻量级模块分割")
    print("- URL前缀和独立配置")
    print("- 简单的注册机制")
    print("- 适合中小型应用")
    
    print(f"\nSpring MVC:")
    print("- 包结构组织")
    print("- 注解驱动的配置")
    print("- 分层架构清晰")
    print("- 适合大型企业应用")
    print()


def demo_flask_extensions():
    """演示Flask扩展生态"""
    print("=== 3. Flask扩展生态 ===")
    
    extensions_example = '''
# Flask扩展使用示例

# 1. Flask-SQLAlchemy - ORM扩展
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='draft')
    
    # 关系
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref='products')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock_quantity': self.stock_quantity,
            'status': self.status,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def from_dict(self, data):
        for field in ['name', 'description', 'price', 'stock_quantity', 'status', 'category_id']:
            if field in data:
                setattr(self, field, data[field])

# 2. Flask-Login - 用户会话管理
from flask_login import UserMixin, LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 3. Flask-WTF - 表单处理
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Email

class ProductForm(FlaskForm):
    name = StringField('商品名称', validators=[
        DataRequired(message='商品名称不能为空'),
        Length(min=1, max=200, message='商品名称长度应在1-200字符之间')
    ])
    
    description = TextAreaField('商品描述', validators=[
        Length(max=2000, message='描述长度不能超过2000字符')
    ])
    
    price = StringField('价格', validators=[
        DataRequired(message='价格不能为空')
    ])
    
    stock_quantity = IntegerField('库存数量', validators=[
        NumberRange(min=0, message='库存数量不能为负数')
    ])
    
    category_id = SelectField('商品分类', coerce=int, validators=[
        DataRequired(message='请选择商品分类')
    ])
    
    status = SelectField('状态', choices=[
        ('draft', '草稿'),
        ('published', '已发布'),
        ('discontinued', '已下架')
    ], default='draft')
    
    submit = SubmitField('保存')
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # 动态加载分类选项
        self.category_id.choices = [
            (c.id, c.name) for c in Category.query.filter_by(is_active=True).all()
        ]

# 4. Flask-Migrate - 数据库迁移
from flask_migrate import Migrate

migrate = Migrate()

# 使用命令: flask db init, flask db migrate, flask db upgrade

# 5. Flask-Mail - 邮件发送
from flask_mail import Mail, Message

mail = Mail()

def send_email(to, subject, template, **kwargs):
    msg = Message(
        subject=current_app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        sender=current_app.config['MAIL_SENDER'],
        recipients=[to]
    )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_async_email_wrapper(to, subject, template, **kwargs):
    msg = Message(
        subject=current_app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        sender=current_app.config['MAIL_SENDER'],
        recipients=[to]
    )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    
    from threading import Thread
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

# 6. Flask-CORS - 跨域支持
from flask_cors import CORS

# 全局CORS配置
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "https://myapp.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# 7. Flask-Limiter - 请求限流
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/products")
@limiter.limit("10 per minute")
def get_products():
    return jsonify(products)

# 8. Flask-Caching - 缓存支持
from flask_caching import Cache

cache = Cache()

@app.route('/expensive-operation')
@cache.cached(timeout=300)  # 缓存5分钟
def expensive_operation():
    # 模拟昂贵操作
    import time
    time.sleep(2)
    return jsonify({"result": "expensive calculation"})

@cache.memoize(timeout=60)
def get_product_by_id(product_id):
    return Product.query.get(product_id)

# 9. Flask-JWT-Extended - JWT令牌
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

jwt = JWTManager()

@app.route('/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "用户名或密码错误"}), 401

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)

# 10. 自定义扩展
class ProductAnalytics:
    """商品分析扩展"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        app.config.setdefault('ANALYTICS_ENABLED', True)
        app.config.setdefault('ANALYTICS_PROVIDER', 'internal')
        
        # 注册蓝图
        from .analytics import bp
        app.register_blueprint(bp, url_prefix='/analytics')
        
        # 注册CLI命令
        app.cli.add_command(analytics_cli)
    
    def track_product_view(self, product_id, user_id=None):
        if current_app.config['ANALYTICS_ENABLED']:
            # 记录商品浏览
            pass
    
    def get_popular_products(self, limit=10):
        # 获取热门商品
        pass

# 扩展使用
analytics = ProductAnalytics()
analytics.init_app(app)
'''
    
    print("Flask扩展生态特点:")
    print("1. 丰富的第三方扩展库")
    print("2. 统一的初始化模式")
    print("3. 插件式架构，按需加载")
    print("4. 社区驱动的开发模式")
    print("5. 简单易用的API设计")
    
    # Spring Boot Starter对比
    spring_starters = '''
// Spring Boot Starter生态对比

// 1. 数据库访问 - Spring Data JPA
@Entity
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    // 其他字段...
}

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    List<Product> findByStatusAndCategory(ProductStatus status, Category category);
    
    @Query("SELECT p FROM Product p WHERE p.name LIKE %:search% OR p.description LIKE %:search%")
    Page<Product> searchProducts(@Param("search") String search, Pageable pageable);
}

// 2. 安全认证 - Spring Security
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class SecurityConfig {
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
    
    @Bean
    public AuthenticationManager authenticationManager(
            AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }
}

// 3. 缓存支持 - Spring Cache
@Service
public class ProductService {
    
    @Cacheable(value = "products", key = "#id")
    public Product findById(Long id) {
        return productRepository.findById(id).orElse(null);
    }
    
    @CacheEvict(value = "products", key = "#product.id")
    public Product save(Product product) {
        return productRepository.save(product);
    }
}

// 4. 邮件发送 - Spring Mail
@Service
public class EmailService {
    
    @Autowired
    private JavaMailSender mailSender;
    
    @Async
    public void sendSimpleEmail(String to, String subject, String text) {
        SimpleMailMessage message = new SimpleMailMessage();
        message.setTo(to);
        message.setSubject(subject);
        message.setText(text);
        mailSender.send(message);
    }
}

// 5. 数据验证 - Bean Validation
public class ProductCreateRequest {
    @NotBlank(message = "商品名称不能为空")
    @Size(max = 200, message = "商品名称长度不能超过200")
    private String name;
    
    @NotNull(message = "价格不能为空")
    @DecimalMin(value = "0.01", message = "价格必须大于0")
    private BigDecimal price;
    
    @Min(value = 0, message = "库存不能为负数")
    private Integer stockQuantity = 0;
    
    // getter、setter
}

// 6. API文档 - SpringDoc OpenAPI
@RestController
@Tag(name = "商品管理", description = "商品相关操作API")
public class ProductController {
    
    @Operation(summary = "获取商品列表", description = "分页获取商品列表")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "成功获取商品列表"),
        @ApiResponse(responseCode = "400", description = "请求参数错误")
    })
    @GetMapping
    public ResponseEntity<PagedResponse<ProductResponse>> getProducts(
            @Parameter(description = "分类ID") @RequestParam(required = false) Long categoryId,
            @Parameter(description = "搜索关键词") @RequestParam(required = false) String search,
            @Parameter(description = "页码") @RequestParam(defaultValue = "1") int page,
            @Parameter(description = "每页数量") @RequestParam(defaultValue = "20") int size) {
        
        // 实现逻辑
        return ResponseEntity.ok(products);
    }
}
'''
    
    print(f"\n扩展生态对比:")
    print("Flask扩展:")
    print("- 轻量级，单一职责")
    print("- 社区驱动，选择灵活")
    print("- 简单的API和配置")
    print("- 手动集成和配置")
    
    print(f"\nSpring Boot Starter:")
    print("- 自动配置，开箱即用")
    print("- 官方维护，质量稳定")
    print("- 复杂的配置选项")
    print("- 企业级功能完整")
    print()


def main():
    """主函数：运行所有演示"""
    print("Flask框架基础学习指南")
    print("=" * 50)
    
    demo_flask_basic_setup()
    demo_flask_blueprints()
    demo_flask_extensions()
    
    print("学习总结:")
    print("1. Flask是微框架，核心简单，通过扩展实现完整功能")
    print("2. 蓝图模式提供清晰的模块化组织方式")
    print("3. 丰富的扩展生态，满足各种开发需求")
    print("4. 轻量级设计，适合快速原型和中小型项目")
    print("5. 与Spring MVC相比更简单直接，但企业级功能需要额外配置")
    print("6. 灵活性高，可以根据需求选择合适的组件")


if __name__ == "__main__":
    main() 