from fastapi import APIRouter
from app.api.endpoints import dashboard, charts, data

# 创建API路由器
api_router = APIRouter()

# 添加各模块路由
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(charts.router, prefix="/charts", tags=["charts"])
api_router.include_router(data.router, prefix="/data", tags=["data"])