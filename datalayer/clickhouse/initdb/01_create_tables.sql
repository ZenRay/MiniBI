-- Mini BI项目初始化SQL脚本
-- 创建主数据库（如果没有通过环境变量创建）
CREATE DATABASE IF NOT EXISTS bi_mvp;

-- 使用bi_mvp数据库
USE bi_mvp;

-- 用户行为事实表
CREATE TABLE IF NOT EXISTS user_behavior (
    event_date Date,
    event_time DateTime,
    user_id UInt32,
    product_id UInt32,
    action_type String,
    revenue Decimal(10,2),
    session_id String,
    platform String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_date)
ORDER BY (event_date, user_id, product_id)
SETTINGS index_granularity = 8192;

-- 产品维度表
CREATE TABLE IF NOT EXISTS dim_products (
    product_id UInt32,
    product_name String,
    category String,
    price Decimal(10,2),
    created_date Date
) ENGINE = MergeTree()
ORDER BY product_id;

-- 用户维度表
CREATE TABLE IF NOT EXISTS dim_users (
    user_id UInt32,
    username String,
    signup_date Date,
    is_active Boolean
) ENGINE = MergeTree()
ORDER BY user_id;

-- 演示数据：产品
INSERT INTO dim_products (product_id, product_name, category, price, created_date)
VALUES
    (1, '笔记本电脑', '电子产品', 5999.00, '2023-01-01'),
    (2, '智能手机', '电子产品', 2999.00, '2023-01-01'),
    (3, '平板电脑', '电子产品', 3499.00, '2023-01-01'),
    (4, '无线耳机', '配件', 799.00, '2023-01-01'),
    (5, '智能手表', '配件', 1299.00, '2023-01-01');

-- 演示数据：用户
INSERT INTO dim_users (user_id, username, signup_date, is_active)
VALUES
    (101, 'user1', '2023-01-10', 1),
    (102, 'user2', '2023-02-15', 1),
    (103, 'user3', '2023-03-20', 0),
    (104, 'user4', '2023-04-05', 1),
    (105, 'user5', '2023-05-12', 1);

-- 演示数据：用户行为
INSERT INTO user_behavior (event_date, event_time, user_id, product_id, action_type, revenue, session_id, platform)
VALUES
    ('2023-10-01', '2023-10-01 08:30:00', 101, 1, 'view', 0.00, 's1001', 'web'),
    ('2023-10-01', '2023-10-01 09:15:00', 101, 1, 'add_to_cart', 0.00, 's1001', 'web'),
    ('2023-10-01', '2023-10-01 09:30:00', 101, 1, 'purchase', 5999.00, 's1001', 'web'),
    ('2023-10-01', '2023-10-01 10:20:00', 102, 2, 'view', 0.00, 's1002', 'mobile'),
    ('2023-10-01', '2023-10-01 10:25:00', 102, 2, 'purchase', 2999.00, 's1002', 'mobile'),
    ('2023-10-02', '2023-10-02 14:10:00', 103, 4, 'view', 0.00, 's1003', 'mobile'),
    ('2023-10-02', '2023-10-02 14:30:00', 103, 4, 'add_to_cart', 0.00, 's1003', 'mobile'),
    ('2023-10-03', '2023-10-03 09:15:00', 104, 3, 'view', 0.00, 's1004', 'web'),
    ('2023-10-03', '2023-10-03 09:20:00', 104, 3, 'add_to_cart', 0.00, 's1004', 'web'),
    ('2023-10-03', '2023-10-03 09:25:00', 104, 3, 'purchase', 3499.00, 's1004', 'web'),
    ('2023-10-04', '2023-10-04 11:30:00', 105, 5, 'view', 0.00, 's1005', 'mobile'),
    ('2023-10-04', '2023-10-04 11:40:00', 105, 5, 'add_to_cart', 0.00, 's1005', 'mobile'),
    ('2023-10-04', '2023-10-04 11:45:00', 105, 5, 'purchase', 1299.00, 's1005', 'mobile');