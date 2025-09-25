"""
ClickHouse数据库模型定义
"""
from sqlalchemy import Column, String, DateTime, Numeric, Date, Integer, Boolean
from app.db.database import Base

# 在实际项目中，应该导入 clickhouse_sqlalchemy 的类型和引擎
# 这里先用 sqlalchemy 的通用类型替代，安装库后可以替换回来
# from clickhouse_sqlalchemy import engines, types

class UserBehavior(Base):
    """
    用户行为事实表模型
    """
    __tablename__ = 'user_behavior'
    # 在实际项目中，应该使用 engines.MergeTree
    # __table_args__ = (
    #     engines.MergeTree(
    #         partition_by='toYYYYMM(event_date)',
    #         order_by=('event_date', 'user_id', 'product_id')
    #     ),
    # )

    event_date = Column(Date, primary_key=True)
    event_time = Column(DateTime)
    user_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    action_type = Column(String)
    revenue = Column(Numeric(10, 2))
    session_id = Column(String)
    platform = Column(String)

class Product(Base):
    """
    产品维度表模型
    """
    __tablename__ = 'dim_products'
    # 在实际项目中，应该使用 engines.MergeTree
    # __table_args__ = (
    #     engines.MergeTree(
    #         order_by='product_id'
    #     ),
    # )

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    category = Column(String)
    price = Column(Numeric(10, 2))
    created_date = Column(Date)

class User(Base):
    """
    用户维度表模型
    """
    __tablename__ = 'dim_users'
    # 在实际项目中，应该使用 engines.MergeTree
    # __table_args__ = (
    #     engines.MergeTree(
    #         order_by='user_id'
    #     ),
    # )

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    signup_date = Column(Date)
    is_active = Column(Boolean)  # 使用Boolean来表示布尔值