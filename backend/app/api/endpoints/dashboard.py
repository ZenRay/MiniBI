from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import date, datetime, timedelta

router = APIRouter()

@router.get("/summary")
async def get_dashboard_summary(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    metrics: List[str] = Query(["revenue", "user_count"], description="指标"),
    dimensions: List[str] = Query(["event_date"], description="维度")
):
    """
    获取仪表板汇总数据
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