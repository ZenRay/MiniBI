<template>
  <div class="data-management">
    <h1>数据管理</h1>
    
    <!-- 数据源选择 -->
    <el-row :gutter="20" class="filter-row">
      <el-col :span="8">
        <el-select 
          v-model="selectedSource" 
          placeholder="请选择数据源"
          style="width: 100%"
          @change="fetchData"
        >
          <el-option
            v-for="item in sourceOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-col>
      <el-col :span="8">
        <el-input-number 
          v-model="limit" 
          :min="1" 
          :max="100" 
          placeholder="显示条数"
          @change="fetchData"
        />
      </el-col>
      <el-col :span="8">
        <el-button type="primary" @click="fetchData">查询数据</el-button>
      </el-col>
    </el-row>

    <!-- 数据表格 -->
    <el-row>
      <el-col :span="24">
        <el-table
          v-loading="loading"
          :data="tableData"
          style="width: 100%"
          border
          stripe
        >
          <el-table-column
            v-for="column in tableColumns"
            :key="column.prop"
            :prop="column.prop"
            :label="column.label"
            :width="column.width"
          />
        </el-table>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '../services/api'

// 状态
const selectedSource = ref('products')
const limit = ref(10)
const tableData = ref([])
const loading = ref(false)

// 数据源选项
const sourceOptions = [
  { value: 'products', label: '产品数据' },
  { value: 'users', label: '用户数据' }
]

// 动态表格列
const tableColumns = computed(() => {
  if (!tableData.value || tableData.value.length === 0) {
    return []
  }
  
  // 从第一行数据动态生成列
  const firstRow = tableData.value[0]
  return Object.keys(firstRow).map(key => {
    let label = key
    
    // 美化列标题
    if (key === 'product_id') label = '产品ID'
    else if (key === 'product_name') label = '产品名称'
    else if (key === 'category') label = '分类'
    else if (key === 'price') label = '价格'
    else if (key === 'user_id') label = '用户ID'
    else if (key === 'username') label = '用户名'
    else if (key === 'signup_date') label = '注册日期'
    else if (key === 'is_active') label = '是否活跃'
    
    return {
      prop: key,
      label: label,
      width: key.includes('id') ? '100' : ''
    }
  })
})

// 方法
const fetchData = async () => {
  loading.value = true
  try {
    const response = await api.getDataList(selectedSource.value, limit.value)
    tableData.value = Array.isArray(response) ? response : []
  } catch (error) {
    console.error('获取数据列表失败:', error)
    tableData.value = []
    // 在实际应用中，你应该向用户显示错误消息
  } finally {
    loading.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  fetchData()
})

// 监听
watch(selectedSource, () => {
  fetchData()
})
</script>

<style scoped>
.data-management {
  padding: 20px;
}

.filter-row {
  margin-bottom: 20px;
}
</style>