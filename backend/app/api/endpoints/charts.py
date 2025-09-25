from fastapi import APIRouter, Query
from typing import List
from datetime import date, timedelta

router = APIRouter()

@router.get("/charts")
async def get_charts_data(
    chart_type: str = Query(..., description="图表类型"),
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    metrics: List[str] = Query(["revenue"], description="指标")
):
    """
    获取图表数据
    """
    # 生成示例图表数据
    data = []
    current = start_date
    while current <= end_date:
        item = {"date": current.isoformat()}
        
        # 生成不同指标的示例数据
        for metric in metrics:
            base_value = 0
            if metric == "revenue":
                base_value = 1000
            elif metric == "user_count":
                base_value = 500
            elif metric == "conversion_rate":
                base_value = 0.1
                
            # 添加一些随机变化，使图表更有趣
            day_factor = current.day / 30.0
            item[metric] = round(base_value + (base_value * day_factor), 2)
            
        data.append(item)
        current = current + timedelta(days=1)
    
    return {
        "chart_type": chart_type,
        "data": data,
        "config": {
            "title": f"{', '.join(metrics)} 趋势图",
            "xAxis": "date",
            "yAxis": metrics
        }
    }