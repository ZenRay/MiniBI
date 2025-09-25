"""
SQLAlchemy与ClickHouse集成示例
"""
from datetime import date, timedelta
from sqlalchemy import select, func
from app.db.database import engine, SessionLocal
from app.db.models import UserBehavior, Product, User
from app.db.repository import AnalyticsRepository

def run_example():
    """
    运行SQLAlchemy ClickHouse集成示例
    """
    # 创建会话
    db = SessionLocal()
    
    try:
        # 创建存储库
        repo = AnalyticsRepository(db)
        
        # 设置日期范围
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        # 获取每日收入数据
        print("\n===== 每日收入数据 =====")
        revenues = repo.get_revenue_by_date(start_date, end_date)
        for item in revenues[:5]:  # 只显示前5条
            print(f"日期: {item['event_date']}, 收入: {item['revenue']}")
        
        # 获取每日用户数据
        print("\n===== 每日用户数据 =====")
        users = repo.get_user_count_by_date(start_date, end_date)
        for item in users[:5]:  # 只显示前5条
            print(f"日期: {item['event_date']}, 用户数: {item['user_count']}")
        
        # 获取热门产品
        print("\n===== 热门产品 =====")
        top_products = repo.get_top_products(start_date, end_date)
        for item in top_products:
            print(f"产品: {item['product_name']}, 分类: {item['category']}, " +
                  f"销量: {item['purchase_count']}, 收入: {item['total_revenue']}")
        
        # 原生SQL查询示例
        print("\n===== 原生SQL查询 =====")
        with engine.connect() as connection:
            result = connection.execute("""
                SELECT 
                    product_name, 
                    category, 
                    price 
                FROM dim_products 
                ORDER BY price DESC 
                LIMIT 3
            """)
            for row in result:
                print(f"产品: {row[0]}, 分类: {row[1]}, 价格: {row[2]}")
    
    finally:
        db.close()

if __name__ == "__main__":
    run_example()