import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'

// 导入页面
import Dashboard from './pages/Dashboard.vue'
import Analytics from './pages/Analytics.vue'
import DataManagement from './pages/DataManagement.vue'

// 创建路由
const routes = [
  { path: '/', component: Dashboard },
  { path: '/analytics', component: Analytics },
  { path: '/data', component: DataManagement },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 创建状态管理
const pinia = createPinia()

// 创建应用
const app = createApp(App)

// 使用插件
app.use(router)
app.use(pinia)
app.use(ElementPlus)

// 挂载应用
app.mount('#app')