"""
数据库模块初始化
"""
# 导出关键类和函数
from app.db.database import engine, SessionLocal, Base, get_db
from app.db.models import UserBehavior, Product, User
from app.db.repository import AnalyticsRepository