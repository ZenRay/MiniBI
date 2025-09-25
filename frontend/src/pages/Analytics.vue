<template>
  <div class="analytics">
    <h1>数据分析</h1>
    
    <!-- 筛选器 -->
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
        />
      </el-col>
      <el-col :span="8">
        <el-select 
          v-model="selectedMetrics" 
          multiple 
          placeholder="请选择指标"
          style="width: 100%"
        >
          <el-option
            v-for="item in metricOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-col>
      <el-col :span="8">
        <el-button type="primary" @click="fetchChartData">分析数据</el-button>
      </el-col>
    </el-row>

    <!-- 图表 -->
    <el-row class="chart-row">
      <el-col :span="24">
        <line-chart 
          :data="chartData" 
          :loading="loading" 
          :title="chartTitle" 
          :xAxisKey="'date'"
          :yAxisKeys="selectedMetrics"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import LineChart from '../components/charts/LineChart.vue'
import api from '../services/api'

// 状态
const dateRange = ref([
  // 默认显示最近7天
  new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
  new Date().toISOString().split('T')[0]
])
const selectedMetrics = ref(['revenue'])
const chartData = ref([])
const loading = ref(false)

// 指标选项
const metricOptions = [
  { value: 'revenue', label: '营收' },
  { value: 'user_count', label: '用户数' },
  { value: 'conversion_rate', label: '转化率' }
]

// 计算属性
const chartTitle = computed(() => {
  if (selectedMetrics.value.length === 0) return '请选择指标'
  
  const metricLabels = selectedMetrics.value.map(value => {
    const option = metricOptions.find(opt => opt.value === value)
    return option ? option.label : value
  })
  
  return `${metricLabels.join('/')} 趋势分析`
})

// 方法
const fetchChartData = async () => {
  if (!dateRange.value || dateRange.value.length !== 2 || selectedMetrics.value.length === 0) {
    return
  }
  
  loading.value = true
  try {
    const [startDate, endDate] = dateRange.value
    const response = await api.getChartData(
      'line',
      startDate, 
      endDate, 
      selectedMetrics.value
    )
    chartData.value = response.data || []
  } catch (error) {
    console.error('获取图表数据失败:', error)
    // 在实际应用中，你应该向用户显示错误消息
  } finally {
    loading.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  fetchChartData()
})
</script>

<style scoped>
.analytics {
  padding: 20px;
}

.filter-row {
  margin-bottom: 20px;
}

.chart-row {
  margin-top: 20px;
}
</style>