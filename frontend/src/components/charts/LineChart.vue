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
    title: String,
    xAxisKey: {
      type: String,
      default: 'date'
    },
    yAxisKeys: {
      type: Array,
      default: () => ['value']
    }
  },
  setup(props) {
    const chartEl = ref(null)
    let chartInstance = null
    
    const initChart = () => {
      if (!chartEl.value || !props.data || props.data.length === 0) return
      
      chartInstance = echarts.init(chartEl.value)
      
      // 准备x轴数据
      const xAxisData = props.data.map(item => item[props.xAxisKey])
      
      // 准备系列数据
      const series = props.yAxisKeys.map(key => {
        return {
          name: key,
          type: 'line',
          data: props.data.map(item => item[key]),
          smooth: true
        }
      })
      
      const option = {
        title: { 
          text: props.title,
          left: 'center'
        },
        tooltip: { 
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: props.yAxisKeys,
          bottom: '0%'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '10%',
          top: '15%',
          containLabel: true
        },
        xAxis: { 
          type: 'category',
          data: xAxisData,
          boundaryGap: false
        },
        yAxis: { type: 'value' },
        series: series
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
    
    watch(() => [props.data, props.title], initChart, { deep: true })
    
    return { chartEl }
  }
}
</script>

<style scoped>
.line-chart {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.loading {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: #909399;
}
</style>