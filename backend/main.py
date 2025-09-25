from fastapi import FastAPI, Depends, Query
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
import uvicorn
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="MiniBI API",
    description="MiniBI - 数据分析与可视化API",
    version="0.1.0"
)

# 健康检查接口
@app.get("/")
async def root():
    """
    API健康检查接口
    """
    return {
        "status": "ok",
        "message": "MiniBI API is running",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }

# 示例数据接口
@app.get("/api/sample-data")
async def get_sample_data():
    """
    获取示例数据
    """
    # 生成一些示例数据
    data = []
    now = datetime.now()
    for i in range(7):
        day = now - timedelta(days=i)
        data.append({
            "date": day.strftime("%Y-%m-%d"),
            "revenue": round(100 + i * 15 + i * i, 2),
            "user_count": 100 + i * 10,
            "conversion_rate": round(0.1 + i * 0.01, 2)
        })
    
    return data

# 仪表板概览接口
@app.get("/dashboard/summary")
async def get_dashboard_summary(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    metrics: List[str] = Query(["revenue", "user_count"], description="指标"),
    dimensions: List[str] = Query(["event_date"], description="维度")
):
    """
    获取仪表板概览数据
    """
    # 生成示例数据
    data = []
    current = start_date
    while current <= end_date:
        item = {"event_date": current.isoformat()}
        for metric in metrics:
            if metric == "revenue":
                item[metric] = round(1000 + (current.day * 50), 2)
            elif metric == "user_count":
                item[metric] = 500 + (current.day * 20)
            elif metric == "conversion_rate":
                item[metric] = round(0.1 + (current.day * 0.005), 3)
        data.append(item)
        current = current + timedelta(days=1)
    
    return {
        "data": data,
        "metadata": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "metrics": metrics,
            "dimensions": dimensions
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)