import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

export default {
  // 获取仪表板摘要数据
  async getDashboardSummary(startDate, endDate, metrics = ['revenue', 'user_count'], dimensions = ['event_date']) {
    try {
      const response = await apiClient.get('/dashboard/summary', {
        params: { 
          start_date: startDate, 
          end_date: endDate,
          metrics: metrics.join(','),
          dimensions: dimensions.join(',')
        }
      })
      return response.data
    } catch (error) {
      console.error('获取仪表板数据失败:', error)
      throw error
    }
  },

  // 获取图表数据
  async getChartData(chartType, startDate, endDate, metrics = ['revenue']) {
    try {
      const response = await apiClient.get('/charts/charts', {
        params: { 
          chart_type: chartType,
          start_date: startDate, 
          end_date: endDate,
          metrics: metrics.join(',')
        }
      })
      return response.data
    } catch (error) {
      console.error('获取图表数据失败:', error)
      throw error
    }
  },

  // 获取数据列表
  async getDataList(source, limit = 10) {
    try {
      const response = await apiClient.get('/data/list', {
        params: { source, limit }
      })
      return response.data
    } catch (error) {
      console.error('获取数据列表失败:', error)
      throw error
    }
  }
}