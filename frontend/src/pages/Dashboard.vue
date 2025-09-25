<template>
  <div class="dashboard">
    <h1>仪表盘</h1>

    <!-- 日期选择器 -->
    <el-row :gutter="20" class="filter-row">
      <el-col :span="8">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="fetchDashboardData"
        />
      </el-col>
      <el-col :span="8">
        <el-button type="primary" @click="fetchDashboardData">刷新数据</el-button>
      </el-col>
    </el-row>

    <!-- 指标卡片 -->
    <el-row :gutter="20" class="metric-cards">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>总营收</span>
            </div>
          </template>
          <div class="card-content">
            <span class="metric-value">{{ totalRevenue }}</span>
            <span class="metric-unit">元</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用户数</span>
            </div>
          </template>
          <div class="card-content">
            <span class="metric-value">{{ totalUsers }}</span>
            <span class="metric-unit">人</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>转化率</span>
            </div>
          </template>
          <div class="card-content">
            <span class="metric-value">{{ conversionRate }}</span>
            <span class="metric-unit">%</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表 -->
    <el-row class="chart-row">
      <el-col :span="24">
        <line-chart 
          :data="chartData" 
          :loading="loading" 
          :title="'销售趋势'" 
          :xAxisKey="'event_date'"
          :yAxisKeys="['revenue']"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import LineChart from '../components/charts/LineChart.vue'
import api from '../services/api'

// 状态
const dateRange = ref([
  // 默认显示最近7天
  new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
  new Date().toISOString().split('T')[0]
])
const dashboardData = ref([])
const loading = ref(false)

// 计算属性
const totalRevenue = computed(() => {
  if (!dashboardData.value || dashboardData.value.length === 0) return '0.00'
  
  const sum = dashboardData.value.reduce((acc, item) => acc + (item.revenue || 0), 0)
  return sum.toFixed(2)
})

const totalUsers = computed(() => {
  if (!dashboardData.value || dashboardData.value.length === 0) return '0'
  
  // 在实际应用中，这可能是唯一用户数
  // 这里我们简单地取最后一个记录的用户数
  const lastRecord = dashboardData.value[dashboardData.value.length - 1]
  return lastRecord.user_count || '0'
})

const conversionRate = computed(() => {
  if (!dashboardData.value || dashboardData.value.length === 0) return '0.0'
  
  // 在实际应用中，这是基于真实数据计算的
  // 这里我们简单地取最后一个记录的转化率
  const lastRecord = dashboardData.value[dashboardData.value.length - 1]
  return ((lastRecord.conversion_rate || 0) * 100).toFixed(1)
})

const chartData = computed(() => {
  return dashboardData.value
})

// 方法
const fetchDashboardData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2) return
  
  loading.value = true
  try {
    const [startDate, endDate] = dateRange.value
    const response = await api.getDashboardSummary(
      startDate, 
      endDate, 
      ['revenue', 'user_count', 'conversion_rate']
    )
    dashboardData.value = response.data || []
  } catch (error) {
    console.error('获取仪表板数据失败:', error)
    // 在实际应用中，你应该向用户显示错误消息
  } finally {
    loading.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.filter-row {
  margin-bottom: 20px;
}

.metric-cards {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-content {
  text-align: center;
  padding: 10px 0;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.metric-unit {
  font-size: 14px;
  color: #909399;
  margin-left: 5px;
}

.chart-row {
  margin-top: 20px;
}
</style>