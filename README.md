# Mini MVP BI项目架构设计方案

## 项目概述
本项目是一个mini MVP版本的BI（商业智能）系统，采用现代技术栈实现数据开发、后端API和前端可视化功能。架构设计注重快速开发、学习价值和未来扩展性。

## 整体架构

### 架构图
```
+-------------------------------------------------------------------+
|                       前端层 (Frontend)                            |
|              (Vue.js 3 + Element Plus + ECharts)                 |
+--------------------------------------+----------------------------+
                                       | (HTTP/RESTful API)
+--------------------------------------v----------------------------+
|                       后端层 (Backend API)                         |
|                 (Python FastAPI + ClickHouse + Redis)            |
+--------------------------------------+----------------------------+
                                       | (SQL查询 + 缓存读写)
+--------------------------------------v----------------------------+
|                       数据层 (Data Layer)                          |
|   +------------------+  +------------------+  +-----------------+ |
|   |   ClickHouse     |  |      Redis       |  |   数据源接入      | |
|   |   (主数据仓库)    |  |   (查询结果缓存)  |  |  (MySQL,API,CSV) | |
|   +------------------+  +------------------+  +-----------------+ |
+-------------------------------------------------------------------+
```

### 技术栈选型
| 层级 | 技术栈 | 版本 | 选择理由 |
|------|--------|------|----------|
| **前端** | Vue.js 3 + Element Plus + ECharts | 最新稳定版 | 组件丰富，学习曲线平缓，图表功能强大 |
| **后端** | Python FastAPI + Uvicorn | 0.104+ | 高性能，自动API文档，异步支持 |
| **数据存储** | ClickHouse + Redis | 最新稳定版 | 分析查询性能极佳，缓存提升响应速度 |
| **数据开发** | Python (Pandas, Requests) | 3.8+ | 生态丰富，开发效率高 |
| **部署** | Docker + Docker Compose | 最新 | 环境一致性，快速部署 |

## 详细设计

### 1. 数据层架构

#### ClickHouse 数据模型设计
下面只是示例，不作为实际业务需求的代码
```sql
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
```

#### Redis 缓存策略
```python
# 缓存配置
CACHE_CONFIG = {
    'high_frequency': 60,      # 1分钟缓存
    'medium_frequency': 300,   # 5分钟缓存
    'low_frequency': 1800,     # 30分钟缓存
    'static_data': 86400       # 24小时缓存
}
```

### 2. 后端API设计

#### 核心模块结构
```
backend/
├── app/
│   ├── api/           # API路由
│   │   ├── endpoints/
│   │   │   ├── dashboard.py
│   │   │   ├── charts.py
│   │   │   └── data.py
│   ├── core/          # 核心配置
│   │   ├── config.py
│   │   └── security.py
│   ├── models/        # 数据模型
│   ├── schemas/       # Pydantic模型
│   ├── services/      # 业务逻辑
│   │   ├── analytics_service.py
│   │   ├── cache_service.py
│   │   └── data_service.py
│   └── utils/         # 工具函数
│       ├── database.py
│       └── cache.py
├── requirements.txt
└── main.py
```

#### 核心API示例
```python
# backend/app/api/endpoints/dashboard.py
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import date
from app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    metrics: List[str] = Query(["revenue", "user_count"], description="指标"),
    dimensions: List[str] = Query(["event_date"], description="维度"),
    analytics_service: AnalyticsService = Depends()
):
    """
    获取仪表板汇总数据
    """
    return await analytics_service.get_dashboard_data(
        start_date, end_date, metrics, dimensions
    )
```

### 3. 前端架构设计

#### 项目结构
```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── charts/
│   │   │   ├── LineChart.vue
│   │   │   ├── BarChart.vue
│   │   │   └── PieChart.vue
│   │   ├── filters/
│   │   │   ├── DateRangePicker.vue
│   │   │   └── MetricSelector.vue
│   │   └── layout/
│   │       ├── Header.vue
│   │       └── Sidebar.vue
│   ├── pages/
│   │   ├── Dashboard.vue
│   │   ├── Analytics.vue
│   │   └── DataManagement.vue
│   ├── services/
│   │   ├── api.js
│   │   └── auth.js
│   ├── stores/        # Pinia状态管理
│   │   ├── dashboard.js
│   │   └── user.js
│   ├── utils/
│   │   ├── constants.js
│   │   └── helpers.js
│   ├── App.vue
│   └── main.js
├── package.json
└── vite.config.js
```

#### 核心组件示例
```vue
<!-- frontend/src/components/charts/LineChart.vue -->
<template>
  <div class="line-chart">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else ref="chartEl" style="width: 100%; height: 400px;"></div>
  </div>
</template>

<script>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'

export default {
  name: 'LineChart',
  props: {
    data: Array,
    loading: Boolean,
    title: String
  },
  setup(props) {
    const chartEl = ref(null)
    let chartInstance = null
    
    const initChart = () => {
      if (!chartEl.value) return
      
      chartInstance = echarts.init(chartEl.value)
      const option = {
        title: { text: props.title },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category' },
        yAxis: { type: 'value' },
        series: [{ type: 'line', data: props.data }]
      }
      chartInstance.setOption(option)
    }
    
    onMounted(() => {
      initChart()
      window.addEventListener('resize', () => chartInstance?.resize())
    })
    
    onUnmounted(() => {
      chartInstance?.dispose()
      window.removeEventListener('resize', () => chartInstance?.resize())
    })
    
    watch(() => props.data, initChart, { deep: true })
    
    return { chartEl }
  }
}
</script>
```

## 部署方案

### Docker Compose 配置
```yaml
# docker-compose.yml
version: '3.8'

services:
  clickhouse:
    image: clickhouse/clickhouse-server:latest
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - clickhouse_data:/var/lib/clickhouse
      - ./config/clickhouse:/etc/clickhouse-server
    environment:
      CLICKHOUSE_DB: bi_mvp
      CLICKHOUSE_USER: admin
      CLICKHOUSE_PASSWORD: password

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - clickhouse
      - redis
    environment:
      - CLICKHOUSE_URL=clickhouse:9000
      - REDIS_URL=redis:6379
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  clickhouse_data:
  redis_data:
```

### 环境变量配置
```bash
# backend/.env
CLICKHOUSE_URL=clickhouse:9000
CLICKHOUSE_USER=admin
CLICKHOUSE_PASSWORD=password
CLICKHOUSE_DB=bi_mvp

REDIS_URL=redis:6379
REDIS_PASSWORD=

DEBUG=true
SECRET_KEY=your-secret-key
```
<!-- 以下内容只是记录文档，不作为实际的需求文档
## 开发计划

### 第一阶段：基础搭建（1-2周）
1. **环境准备**：Docker环境搭建，基础服务部署
2. **数据模型**：设计ClickHouse表结构，创建示例数据
3. **基础API**：实现基础的数据查询接口

### 第二阶段：核心功能（2-3周）
1. **前端开发**：完成主要页面和组件开发
2. **数据可视化**：集成ECharts，实现多种图表类型
3. **缓存优化**：完善Redis缓存策略

### 第三阶段：功能完善（1-2周）
1. **用户认证**：添加用户登录和权限管理
2. **数据管理**：实现数据导入和管理功能
3. **性能优化**：查询优化和前端性能调优

## 核心优势

1. **技术先进性**：采用现代技术栈，具备学习和实践价值
2. **性能优秀**：ClickHouse提供极佳的分析查询性能
3. **开发效率**：完整的Docker化部署，快速开发环境搭建
4. **扩展性强**：模块化设计，便于功能扩展和迭代

## 下一步行动

1. 搭建基础开发环境
2. 创建示例数据集
3. 实现第一个端到端的数据查询和展示流程
4. 逐步完善各项功能模块 -->


# 建议与评估

本项目架构文档内容详实，涵盖了整体架构、技术选型、详细设计、部署方案和环境变量配置。以下为具体建议与评估，供团队参考：

1. **架构清晰**：采用前后端分离，前端(Vue3+Element Plus+ECharts)、后端(FastAPI+ClickHouse+Redis)、数据层(ClickHouse主仓库+Redis缓存+多数据源)的现代架构，便于扩展和维护。
2. **技术选型合理**：选用的技术栈主流且易于上手，适合快速开发和后续扩展。ClickHouse适合大数据分析，Redis提升查询性能，FastAPI高效且文档友好，前端栈适合数据可视化。
3. **详细设计到位**：数据层有示例表结构，后端API有目录和接口示例，前端有组件划分和代码示例，便于团队协作和后续开发。
4. **部署与环境配置完善**：提供了docker-compose和环境变量示例，方便一键部署和环境一致性。
5. **可扩展性强**：模块化设计，后续可方便地增加新功能或替换技术组件。

**改进建议：**
- 若用于实际生产，需补充安全、监控、日志等运维细节。
- 建议后续补充接口文档自动生成、测试用例、CI/CD流程等内容。
- 适合MVP快速落地和后续迭代，学习和实践价值高。

**总结：**
该文档是一个高质量的BI系统MVP架构方案，适合小团队或初创项目快速启动和迭代开发。