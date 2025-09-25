from fastapi import APIRouter, Query
from typing import List, Optional

router = APIRouter()

@router.get("/list")
async def get_data_list(
    source: str = Query(..., description="数据源"),
    limit: int = Query(10, description="返回条数")
):
    """
    获取数据列表
    """
    # 模拟返回不同数据源的示例数据
    if source == "products":
        return [
            {"product_id": 1, "product_name": "笔记本电脑", "category": "电子产品", "price": 5999.00},
            {"product_id": 2, "product_name": "智能手机", "category": "电子产品", "price": 2999.00},
            {"product_id": 3, "product_name": "平板电脑", "category": "电子产品", "price": 3499.00},
            {"product_id": 4, "product_name": "无线耳机", "category": "配件", "price": 799.00},
            {"product_id": 5, "product_name": "智能手表", "category": "配件", "price": 1299.00},
        ][:limit]
    elif source == "users":
        return [
            {"user_id": 101, "username": "user1", "signup_date": "2023-01-10", "is_active": True},
            {"user_id": 102, "username": "user2", "signup_date": "2023-02-15", "is_active": True},
            {"user_id": 103, "username": "user3", "signup_date": "2023-03-20", "is_active": False},
            {"user_id": 104, "username": "user4", "signup_date": "2023-04-05", "is_active": True},
            {"user_id": 105, "username": "user5", "signup_date": "2023-05-12", "is_active": True},
        ][:limit]
    else:
        return {"error": f"未知数据源: {source}"}