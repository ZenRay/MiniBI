# 应用初始化模块
from fastapi import FastAPI
from app.api import api_router

def create_app() -> FastAPI:
    """
    创建并配置FastAPI应用
    """
    app = FastAPI(
        title="MiniBI API",
        description="MiniBI - 数据分析与可视化API",
        version="0.1.0"
    )
    
    # 添加API路由
    app.include_router(api_router, prefix="/api")
    
    # 添加健康检查端点
    @app.get("/health")
    def health_check():
        return {"status": "ok"}
    
    return app