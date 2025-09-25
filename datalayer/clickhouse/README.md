# ClickHouse 数据层

本目录包含 Mini BI 项目的 ClickHouse 数据模型定义和初始化脚本。

## 目录结构

- `/initdb`: 包含 ClickHouse 数据库初始化脚本
  - `01_create_tables.sql`: 创建表结构和示例数据

## 数据模型

### 1. 事实表

#### user_behavior（用户行为事实表）

该表记录用户在平台上的各种行为事件。

| 字段名 | 类型 | 说明 |
|-------|------|-----|
| event_date | Date | 事件日期 |
| event_time | DateTime | 事件时间 |
| user_id | UInt32 | 用户ID |
| product_id | UInt32 | 产品ID |
| action_type | String | 行为类型（view、add_to_cart、purchase等） |
| revenue | Decimal(10,2) | 收入金额 |
| session_id | String | 会话ID |
| platform | String | 平台（web、mobile等） |

分区键: `toYYYYMM(event_date)`
排序键: `(event_date, user_id, product_id)`

### 2. 维度表

#### dim_products（产品维度表）

该表存储产品相关信息。

| 字段名 | 类型 | 说明 |
|-------|------|-----|
| product_id | UInt32 | 产品ID（主键） |
| product_name | String | 产品名称 |
| category | String | 产品分类 |
| price | Decimal(10,2) | 产品价格 |
| created_date | Date | 创建日期 |

排序键: `product_id`

#### dim_users（用户维度表）

该表存储用户相关信息。

| 字段名 | 类型 | 说明 |
|-------|------|-----|
| user_id | UInt32 | 用户ID（主键） |
| username | String | 用户名 |
| signup_date | Date | 注册日期 |
| is_active | Boolean | 是否活跃 |

排序键: `user_id`

## 使用说明

1. 这些脚本将在 ClickHouse 容器启动时自动执行
2. 通过环境变量可以配置数据库连接参数
3. 可使用 ClickHouse 客户端或 HTTP 接口查询数据

## 数据访问示例

```sql
-- 查询每日收入
SELECT 
    event_date,
    sum(revenue) as daily_revenue
FROM user_behavior
GROUP BY event_date
ORDER BY event_date;

-- 查询产品销量
SELECT 
    p.product_name,
    count() as purchase_count
FROM user_behavior as b
JOIN dim_products as p ON b.product_id = p.product_id
WHERE action_type = 'purchase'
GROUP BY p.product_name
ORDER BY purchase_count DESC;
```