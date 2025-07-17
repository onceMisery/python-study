#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FastAPI框架基础学习
FastAPI Framework Basics

作者: Python学习项目
日期: 2024-01-16
描述: FastAPI框架异步支持、自动文档、类型提示和与Spring Boot的详细对比

学习目标:
1. 掌握FastAPI的核心特性和异步编程
2. 理解类型提示和自动文档生成
3. 学会依赖注入和中间件使用
4. 对比FastAPI与Spring Boot的设计理念

注意：FastAPI是现代、高性能的Web框架，基于Python类型提示
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json

# FastAPI核心导入
from fastapi import FastAPI, HTTPException, Depends, status, Query, Path, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Pydantic用于数据验证和序列化
from pydantic import BaseModel, Field, EmailStr, validator
from pydantic.config import ConfigDict

# SQLAlchemy异步支持
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, select

import uvicorn


def demo_fastapi_basic_setup():
    """演示FastAPI基本设置"""
    print("=== 1. FastAPI基本设置 ===")
    
    basic_app_example = '''
# main.py - FastAPI应用基本设置

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 创建FastAPI应用实例
app = FastAPI(
    title="商品管理API",
    description="一个现代化的商品管理系统API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",  # OpenAPI规范URL
    docs_url="/docs",                     # Swagger UI URL
    redoc_url="/redoc",                   # ReDoc URL
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://myapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置受信任主机
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "*.myapp.com"]
)

# 基本路由
@app.get("/")
async def root():
    return {"message": "欢迎使用商品管理API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

# 启动服务器
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,          # 开发模式热重载
        workers=1,            # 工作进程数
        log_level="info"
    )
'''
    
    print("FastAPI应用特点:")
    print("1. 基于Python类型提示，自动生成API文档")
    print("2. 内置异步支持，高性能处理并发请求")
    print("3. 自动数据验证和序列化")
    print("4. OpenAPI/Swagger标准兼容")
    print("5. 现代Python特性支持（async/await）")
    
    spring_boot_setup = '''
// Spring Boot应用设置对比

@SpringBootApplication
@EnableWebMvc
@EnableSwagger2  // 需要额外配置Swagger
public class ProductManagementApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(ProductManagementApplication.class, args);
    }
    
    // CORS配置
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/**")
                       .allowedOrigins("http://localhost:3000", "https://myapp.com")
                       .allowedMethods("*")
                       .allowCredentials(true);
            }
        };
    }
    
    // Swagger配置
    @Bean
    public Docket api() {
        return new Docket(DocumentationType.SWAGGER_2)
                .select()
                .apis(RequestHandlerSelectors.basePackage("com.example.controller"))
                .paths(PathSelectors.any())
                .build()
                .apiInfo(apiInfo());
    }
    
    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("商品管理API")
                .description("一个商品管理系统API")
                .version("1.0.0")
                .build();
    }
}

// application.properties
server.port=8080
server.servlet.context-path=/api/v1

# 启用actuator健康检查
management.endpoints.web.exposure.include=health,info
management.endpoint.health.show-details=always
'''
    
    print(f"\n配置对比:")
    print("FastAPI: 最少配置即可运行，内置文档生成")
    print("Spring Boot: 需要更多配置类和注解，但企业级功能丰富")
    print()


def demo_pydantic_models():
    """演示Pydantic模型和类型提示"""
    print("=== 2. Pydantic模型和类型提示 ===")
    
    # 基础Pydantic模型
    class ProductStatus(str, Enum):
        DRAFT = "draft"
        PUBLISHED = "published"
        DISCONTINUED = "discontinued"

    class ProductBase(BaseModel):
        """商品基础模型"""
        name: str = Field(..., min_length=1, max_length=200, description="商品名称")
        description: str = Field("", max_length=2000, description="商品描述")
        price: float = Field(..., gt=0, description="商品价格（必须大于0）")
        stock_quantity: int = Field(0, ge=0, description="库存数量")
        status: ProductStatus = Field(ProductStatus.DRAFT, description="商品状态")
        category_id: int = Field(..., gt=0, description="分类ID")

        model_config = ConfigDict(
            # 允许使用ORM对象
            from_attributes=True,
            # JSON编码配置
            json_encoders={
                datetime: lambda v: v.isoformat()
            }
        )

        @validator('name')
        def validate_name(cls, v):
            if not v.strip():
                raise ValueError('商品名称不能为空')
            return v.strip()

        @validator('price')
        def validate_price(cls, v):
            if v <= 0:
                raise ValueError('价格必须大于0')
            if v > 999999:
                raise ValueError('价格不能超过999999')
            return round(v, 2)

    class ProductCreate(ProductBase):
        """创建商品模型"""
        pass

    class ProductUpdate(BaseModel):
        """更新商品模型"""
        name: Optional[str] = Field(None, min_length=1, max_length=200)
        description: Optional[str] = Field(None, max_length=2000)
        price: Optional[float] = Field(None, gt=0)
        stock_quantity: Optional[int] = Field(None, ge=0)
        status: Optional[ProductStatus] = None
        category_id: Optional[int] = Field(None, gt=0)

    class ProductResponse(ProductBase):
        """商品响应模型"""
        id: int
        slug: str
        created_at: datetime
        updated_at: datetime
        created_by_id: int

        # 关联数据
        category_name: Optional[str] = None
        created_by_name: Optional[str] = None

    class ProductList(BaseModel):
        """商品列表响应"""
        items: List[ProductResponse]
        total: int
        page: int
        size: int
        pages: int

    class CategoryBase(BaseModel):
        """分类基础模型"""
        name: str = Field(..., min_length=1, max_length=100)
        description: str = Field("", max_length=500)
        is_active: bool = Field(True)

    class CategoryResponse(CategoryBase):
        """分类响应模型"""
        id: int
        product_count: int = 0
        created_at: datetime

    class ErrorResponse(BaseModel):
        """错误响应模型"""
        error: str
        message: str
        details: Optional[Dict[str, Any]] = None

    class SuccessResponse(BaseModel):
        """成功响应模型"""
        message: str
        data: Optional[Dict[str, Any]] = None

    # 查询参数模型
    class ProductQuery(BaseModel):
        """商品查询参数"""
        category_id: Optional[int] = Field(None, gt=0, description="分类ID")
        search: Optional[str] = Field(None, min_length=1, max_length=100, description="搜索关键词")
        min_price: Optional[float] = Field(None, ge=0, description="最低价格")
        max_price: Optional[float] = Field(None, ge=0, description="最高价格")
        status: Optional[ProductStatus] = Field(None, description="商品状态")
        page: int = Field(1, ge=1, description="页码")
        size: int = Field(20, ge=1, le=100, description="每页数量")
        sort_by: str = Field("created_at", description="排序字段")
        sort_desc: bool = Field(True, description="是否降序")

        @validator('max_price')
        def validate_price_range(cls, v, values):
            if v is not None and 'min_price' in values and values['min_price'] is not None:
                if v < values['min_price']:
                    raise ValueError('最高价格不能小于最低价格')
            return v

    print("Pydantic模型特点:")
    print("1. 自动类型验证和转换")
    print("2. 丰富的字段验证器和约束")
    print("3. 自动生成JSON Schema")
    print("4. 与FastAPI完美集成")
    print("5. 支持嵌套模型和复杂验证")
    
    # Java DTO对比
    java_dto_example = '''
// Spring Boot DTO/Entity对比

// 1. 基础Entity
@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotBlank(message = "商品名称不能为空")
    @Size(max = 200, message = "商品名称长度不能超过200")
    private String name;
    
    @Size(max = 2000, message = "描述长度不能超过2000")
    private String description;
    
    @NotNull(message = "价格不能为空")
    @DecimalMin(value = "0.01", message = "价格必须大于0")
    @DecimalMax(value = "999999.99", message = "价格不能超过999999")
    private BigDecimal price;
    
    @Min(value = 0, message = "库存不能为负数")
    private Integer stockQuantity = 0;
    
    @Enumerated(EnumType.STRING)
    private ProductStatus status = ProductStatus.DRAFT;
    
    @NotNull(message = "分类不能为空")
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id")
    private Category category;
    
    @CreationTimestamp
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    private LocalDateTime updatedAt;
    
    // 构造器、getter、setter
}

// 2. 请求DTO
public class ProductCreateRequest {
    @NotBlank(message = "商品名称不能为空")
    @Size(max = 200, message = "商品名称长度不能超过200")
    private String name;
    
    @Size(max = 2000, message = "描述长度不能超过2000")
    private String description;
    
    @NotNull(message = "价格不能为空")
    @DecimalMin(value = "0.01", message = "价格必须大于0")
    private BigDecimal price;
    
    @Min(value = 0, message = "库存不能为负数")
    private Integer stockQuantity = 0;
    
    private ProductStatus status = ProductStatus.DRAFT;
    
    @NotNull(message = "分类ID不能为空")
    @Positive(message = "分类ID必须为正数")
    private Long categoryId;
    
    // getter、setter
}

// 3. 响应DTO
public class ProductResponse {
    private Long id;
    private String name;
    private String description;
    private BigDecimal price;
    private Integer stockQuantity;
    private ProductStatus status;
    private String slug;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    // 关联数据
    private String categoryName;
    private String createdByName;
    
    // 构造器、getter、setter
}

// 4. 查询参数
public class ProductQueryParams {
    @Positive(message = "分类ID必须为正数")
    private Long categoryId;
    
    @Size(min = 1, max = 100, message = "搜索关键词长度在1-100之间")
    private String search;
    
    @DecimalMin(value = "0", message = "最低价格不能为负数")
    private BigDecimal minPrice;
    
    @DecimalMin(value = "0", message = "最高价格不能为负数")
    private BigDecimal maxPrice;
    
    private ProductStatus status;
    
    @Min(value = 1, message = "页码必须大于0")
    private int page = 1;
    
    @Min(value = 1, message = "每页数量必须大于0")
    @Max(value = 100, message = "每页数量不能超过100")
    private int size = 20;
    
    private String sortBy = "createdAt";
    private boolean sortDesc = true;
    
    // getter、setter、validation方法
    @AssertTrue(message = "最高价格不能小于最低价格")
    public boolean isPriceRangeValid() {
        if (minPrice != null && maxPrice != null) {
            return maxPrice.compareTo(minPrice) >= 0;
        }
        return true;
    }
}

// 5. 分页响应
public class PagedResponse<T> {
    private List<T> items;
    private long total;
    private int page;
    private int size;
    private int pages;
    
    // 构造器、getter、setter
}
'''
    
    print(f"\n类型验证对比:")
    print("Pydantic (FastAPI):")
    print("- Python类型提示语法")
    print("- 自动类型转换和验证")
    print("- 函数式验证器")
    print("- 自动生成JSON Schema")
    
    print(f"\nBean Validation (Spring Boot):")
    print("- 注解式验证")
    print("- 需要显式触发验证")
    print("- 更成熟的验证生态")
    print("- 需要额外配置文档生成")
    print()


def demo_async_endpoints():
    """演示异步端点和依赖注入"""
    print("=== 3. 异步端点和依赖注入 ===")
    
    async_api_example = '''
# async_api.py - 异步API端点示例

import asyncio
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query, Path, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_, or_

app = FastAPI()

# 安全配置
security = HTTPBearer()

# 数据库会话依赖
async def get_db_session() -> AsyncSession:
    """获取数据库会话"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# 认证依赖
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db_session)
) -> User:
    """获取当前用户"""
    token = credentials.credentials
    
    # 异步验证token
    user_id = await verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌"
        )
    
    # 异步查询用户
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    return user

# 权限检查依赖
def require_permission(permission: str):
    """权限检查装饰器"""
    async def permission_checker(current_user: User = Depends(get_current_user)):
        if not await has_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要权限: {permission}"
            )
        return current_user
    return permission_checker

# 查询参数依赖
async def get_product_query_params(
    category_id: Optional[int] = Query(None, gt=0, description="分类ID"),
    search: Optional[str] = Query(None, min_length=1, max_length=100, description="搜索关键词"),
    min_price: Optional[float] = Query(None, ge=0, description="最低价格"),
    max_price: Optional[float] = Query(None, ge=0, description="最高价格"),
    status: Optional[ProductStatus] = Query(None, description="商品状态"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_desc: bool = Query(True, description="是否降序")
) -> ProductQuery:
    """商品查询参数依赖"""
    
    # 验证价格范围
    if min_price is not None and max_price is not None and max_price < min_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="最高价格不能小于最低价格"
        )
    
    return ProductQuery(
        category_id=category_id,
        search=search,
        min_price=min_price,
        max_price=max_price,
        status=status,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_desc=sort_desc
    )

# 异步端点示例
@app.get("/products", response_model=ProductList)
async def get_products(
    query_params: ProductQuery = Depends(get_product_query_params),
    db: AsyncSession = Depends(get_db_session)
):
    """获取商品列表（异步）"""
    
    # 构建查询条件
    conditions = [Product.status == ProductStatus.PUBLISHED]
    
    if query_params.category_id:
        conditions.append(Product.category_id == query_params.category_id)
    
    if query_params.search:
        search_term = f"%{query_params.search}%"
        conditions.append(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
    
    if query_params.min_price is not None:
        conditions.append(Product.price >= query_params.min_price)
    
    if query_params.max_price is not None:
        conditions.append(Product.price <= query_params.max_price)
    
    if query_params.status:
        conditions.append(Product.status == query_params.status)
    
    # 构建查询
    query = select(Product).where(and_(*conditions))
    
    # 添加关联加载
    query = query.options(
        selectinload(Product.category),
        selectinload(Product.created_by)
    )
    
    # 排序
    sort_column = getattr(Product, query_params.sort_by, Product.created_at)
    if query_params.sort_desc:
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # 分页
    offset = (query_params.page - 1) * query_params.size
    query = query.offset(offset).limit(query_params.size)
    
    # 执行查询（异步）
    result = await db.execute(query)
    products = result.scalars().all()
    
    # 获取总数（异步）
    count_query = select(func.count(Product.id)).where(and_(*conditions))
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    # 构建响应
    return ProductList(
        items=[
            ProductResponse(
                **product.__dict__,
                category_name=product.category.name if product.category else None,
                created_by_name=product.created_by.username if product.created_by else None
            )
            for product in products
        ],
        total=total,
        page=query_params.page,
        size=query_params.size,
        pages=math.ceil(total / query_params.size) if total > 0 else 0
    )

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int = Path(..., gt=0, description="商品ID"),
    db: AsyncSession = Depends(get_db_session)
):
    """获取单个商品详情（异步）"""
    
    # 异步查询单个商品
    query = select(Product).where(
        and_(
            Product.id == product_id,
            Product.status == ProductStatus.PUBLISHED
        )
    ).options(
        selectinload(Product.category),
        selectinload(Product.created_by)
    )
    
    result = await db.execute(query)
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在"
        )
    
    return ProductResponse(
        **product.__dict__,
        category_name=product.category.name if product.category else None,
        created_by_name=product.created_by.username if product.created_by else None
    )

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(require_permission("product.create")),
    db: AsyncSession = Depends(get_db_session)
):
    """创建商品（异步）"""
    
    # 检查分类是否存在
    category_result = await db.execute(
        select(Category).where(Category.id == product_data.category_id)
    )
    category = category_result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="分类不存在"
        )
    
    # 创建商品
    product = Product(
        **product_data.model_dump(),
        created_by_id=current_user.id,
        slug=generate_slug(product_data.name)
    )
    
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    # 异步加载关联数据
    await db.refresh(product, ['category', 'created_by'])
    
    return ProductResponse(
        **product.__dict__,
        category_name=product.category.name,
        created_by_name=product.created_by.username
    )

@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int = Path(..., gt=0),
    product_data: ProductUpdate,
    current_user: User = Depends(require_permission("product.update")),
    db: AsyncSession = Depends(get_db_session)
):
    """更新商品（异步）"""
    
    # 查询现有商品
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在"
        )
    
    # 权限检查：只能更新自己创建的商品或管理员
    if product.created_by_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限更新此商品"
        )
    
    # 更新字段
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    await db.commit()
    await db.refresh(product, ['category', 'created_by'])
    
    return ProductResponse(
        **product.__dict__,
        category_name=product.category.name,
        created_by_name=product.created_by.username
    )

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int = Path(..., gt=0),
    current_user: User = Depends(require_permission("product.delete")),
    db: AsyncSession = Depends(get_db_session)
):
    """删除商品（异步）"""
    
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在"
        )
    
    # 权限检查
    if product.created_by_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限删除此商品"
        )
    
    await db.delete(product)
    await db.commit()

# 批量操作异步端点
@app.post("/products/batch", response_model=List[ProductResponse])
async def create_products_batch(
    products_data: List[ProductCreate],
    current_user: User = Depends(require_permission("product.create")),
    db: AsyncSession = Depends(get_db_session)
):
    """批量创建商品（异步）"""
    
    if len(products_data) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="单次最多创建100个商品"
        )
    
    # 验证所有分类ID
    category_ids = {p.category_id for p in products_data}
    category_result = await db.execute(
        select(Category.id).where(Category.id.in_(category_ids))
    )
    valid_category_ids = {row[0] for row in category_result.fetchall()}
    
    invalid_ids = category_ids - valid_category_ids
    if invalid_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"以下分类ID不存在: {list(invalid_ids)}"
        )
    
    # 批量创建
    products = []
    for product_data in products_data:
        product = Product(
            **product_data.model_dump(),
            created_by_id=current_user.id,
            slug=generate_slug(product_data.name)
        )
        products.append(product)
    
    db.add_all(products)
    await db.commit()
    
    # 批量刷新
    for product in products:
        await db.refresh(product, ['category', 'created_by'])
    
    return [
        ProductResponse(
            **product.__dict__,
            category_name=product.category.name,
            created_by_name=product.created_by.username
        )
        for product in products
    ]

# 异步工具函数
async def verify_token(token: str) -> Optional[int]:
    """验证JWT令牌（异步）"""
    try:
        # 模拟异步token验证
        await asyncio.sleep(0.001)  # 模拟网络延迟
        # 实际应用中这里会解析JWT
        return 1  # 返回用户ID
    except:
        return None

async def has_permission(user: User, permission: str) -> bool:
    """检查用户权限（异步）"""
    # 模拟异步权限检查
    await asyncio.sleep(0.001)
    return user.is_admin or permission in user.permissions

def generate_slug(name: str) -> str:
    """生成URL友好的slug"""
    import re
    slug = re.sub(r'[^\\w\\s-]', '', name.lower())
    slug = re.sub(r'[-\\s]+', '-', slug)
    return slug.strip('-')
'''
    
    print("FastAPI异步特性:")
    print("1. 原生异步支持，高并发处理能力")
    print("2. 依赖注入系统，支持嵌套和条件依赖")
    print("3. 自动参数验证和类型转换")
    print("4. 异步数据库操作支持")
    print("5. 中间件和安全集成")
    
    # Spring Boot异步对比
    spring_async_example = '''
// Spring Boot异步Controller对比

@RestController
@RequestMapping("/api/products")
@Validated
public class ProductController {
    
    @Autowired
    private ProductService productService;
    
    // 1. 返回CompletableFuture的异步端点
    @GetMapping
    public CompletableFuture<ResponseEntity<PagedResponse<ProductResponse>>> getProducts(
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) String search,
            @RequestParam(required = false) BigDecimal minPrice,
            @RequestParam(required = false) BigDecimal maxPrice,
            @RequestParam(required = false) ProductStatus status,
            @RequestParam(defaultValue = "1") @Min(1) int page,
            @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size,
            @RequestParam(defaultValue = "createdAt") String sortBy,
            @RequestParam(defaultValue = "true") boolean sortDesc) {
        
        return productService.findProductsAsync(
                categoryId, search, minPrice, maxPrice, status, 
                page, size, sortBy, sortDesc
        ).thenApply(ResponseEntity::ok);
    }
    
    // 2. 使用Mono的响应式端点（需要Spring WebFlux）
    @GetMapping("/reactive")
    public Mono<ResponseEntity<Flux<ProductResponse>>> getProductsReactive(
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) String search,
            Pageable pageable) {
        
        Flux<ProductResponse> products = productService.findProductsReactive(
            categoryId, search, pageable
        );
        
        return Mono.just(ResponseEntity.ok(products));
    }
    
    // 3. 异步创建商品
    @PostMapping
    @PreAuthorize("hasPermission('product', 'create')")
    public CompletableFuture<ResponseEntity<ProductResponse>> createProduct(
            @Valid @RequestBody ProductCreateRequest request,
            Authentication authentication) {
        
        String username = authentication.getName();
        
        return productService.createProductAsync(request, username)
                           .thenApply(product -> ResponseEntity.status(201).body(product))
                           .exceptionally(throwable -> {
                               if (throwable.getCause() instanceof ValidationException) {
                                   throw new ResponseStatusException(
                                       HttpStatus.BAD_REQUEST, 
                                       throwable.getCause().getMessage()
                                   );
                               }
                               throw new ResponseStatusException(
                                   HttpStatus.INTERNAL_SERVER_ERROR, 
                                   "创建商品失败"
                               );
                           });
    }
    
    // 4. 批量操作
    @PostMapping("/batch")
    @PreAuthorize("hasPermission('product', 'create')")
    public CompletableFuture<ResponseEntity<List<ProductResponse>>> createProductsBatch(
            @Valid @RequestBody List<ProductCreateRequest> requests,
            Authentication authentication) {
        
        if (requests.size() > 100) {
            return CompletableFuture.completedFuture(
                ResponseEntity.badRequest().build()
            );
        }
        
        String username = authentication.getName();
        
        return productService.createProductsBatchAsync(requests, username)
                           .thenApply(ResponseEntity::ok);
    }
}

// Service层异步实现
@Service
@Transactional
public class ProductService {
    
    @Autowired
    private ProductRepository productRepository;
    
    @Async("taskExecutor")
    public CompletableFuture<PagedResponse<ProductResponse>> findProductsAsync(
            Long categoryId, String search, BigDecimal minPrice, BigDecimal maxPrice,
            ProductStatus status, int page, int size, String sortBy, boolean sortDesc) {
        
        // 构建查询条件
        Specification<Product> spec = Specification.where(null);
        
        if (categoryId != null) {
            spec = spec.and((root, query, cb) -> 
                cb.equal(root.get("category").get("id"), categoryId));
        }
        
        if (search != null && !search.trim().isEmpty()) {
            spec = spec.and((root, query, cb) -> 
                cb.or(
                    cb.like(cb.lower(root.get("name")), "%" + search.toLowerCase() + "%"),
                    cb.like(cb.lower(root.get("description")), "%" + search.toLowerCase() + "%")
                ));
        }
        
        // 更多查询条件...
        
        // 分页和排序
        Sort.Direction direction = sortDesc ? Sort.Direction.DESC : Sort.Direction.ASC;
        Pageable pageable = PageRequest.of(page - 1, size, Sort.by(direction, sortBy));
        
        // 执行查询
        Page<Product> productPage = productRepository.findAll(spec, pageable);
        
        // 转换为响应DTO
        List<ProductResponse> responses = productPage.getContent()
                                                    .stream()
                                                    .map(this::toProductResponse)
                                                    .collect(Collectors.toList());
        
        PagedResponse<ProductResponse> result = new PagedResponse<>(
            responses,
            productPage.getTotalElements(),
            page,
            size,
            productPage.getTotalPages()
        );
        
        return CompletableFuture.completedFuture(result);
    }
    
    @Async("taskExecutor")
    public CompletableFuture<List<ProductResponse>> createProductsBatchAsync(
            List<ProductCreateRequest> requests, String username) {
        
        User user = userRepository.findByUsername(username)
                                 .orElseThrow(() -> new UserNotFoundException("用户不存在"));
        
        // 验证分类ID
        Set<Long> categoryIds = requests.stream()
                                      .map(ProductCreateRequest::getCategoryId)
                                      .collect(Collectors.toSet());
        
        Map<Long, Category> categoryMap = categoryRepository.findAllById(categoryIds)
                                                          .stream()
                                                          .collect(Collectors.toMap(
                                                              Category::getId, 
                                                              Function.identity()
                                                          ));
        
        // 批量创建
        List<Product> products = requests.stream()
                                       .map(request -> {
                                           Category category = categoryMap.get(request.getCategoryId());
                                           if (category == null) {
                                               throw new ValidationException("分类不存在: " + request.getCategoryId());
                                           }
                                           
                                           Product product = new Product();
                                           BeanUtils.copyProperties(request, product);
                                           product.setCategory(category);
                                           product.setCreatedBy(user);
                                           product.setSlug(generateSlug(request.getName()));
                                           
                                           return product;
                                       })
                                       .collect(Collectors.toList());
        
        List<Product> savedProducts = productRepository.saveAll(products);
        
        List<ProductResponse> responses = savedProducts.stream()
                                                     .map(this::toProductResponse)
                                                     .collect(Collectors.toList());
        
        return CompletableFuture.completedFuture(responses);
    }
}

// 异步配置
@Configuration
@EnableAsync
public class AsyncConfig {
    
    @Bean(name = "taskExecutor")
    public TaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(50);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-task-");
        executor.initialize();
        return executor;
    }
}
'''
    
    print(f"\n异步编程对比:")
    print("FastAPI:")
    print("- 原生async/await语法支持")
    print("- 自动异步/同步兼容")
    print("- 内置异步数据库支持")
    print("- 简洁的依赖注入")
    
    print(f"\nSpring Boot:")
    print("- CompletableFuture或响应式编程")
    print("- 需要显式配置异步执行器")
    print("- 更复杂的异步配置")
    print("- 成熟的企业级异步处理")
    print()


def main():
    """主函数：运行所有演示"""
    print("FastAPI框架基础学习指南")
    print("=" * 50)
    
    demo_fastapi_basic_setup()
    demo_pydantic_models()
    demo_async_endpoints()
    
    print("学习总结:")
    print("1. FastAPI基于Python类型提示，自动生成API文档")
    print("2. 原生异步支持，高性能处理并发请求")
    print("3. Pydantic模型提供强大的数据验证和序列化")
    print("4. 现代Python特性：类型提示、async/await、依赖注入")
    print("5. 与Spring Boot相比学习曲线更平缓，开发效率更高")
    print("6. 适合API优先的微服务架构和现代Web应用")


if __name__ == "__main__":
    main() 