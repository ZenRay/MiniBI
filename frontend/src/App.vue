<template>
  <div class="app">
    <el-container>
      <el-aside width="200px">
        <el-menu 
          :default-active="$route.path"
          router
          class="el-menu-vertical"
          background-color="#001529"
          text-color="#fff">
          <el-menu-item index="/">
            <el-icon><DataLine /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/analytics">
            <el-icon><PieChart /></el-icon>
            <span>数据分析</span>
          </el-menu-item>
          <el-menu-item index="/data">
            <el-icon><Grid /></el-icon>
            <span>数据管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>
          <h2>Mini BI 系统</h2>
        </el-header>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { DataLine, PieChart, Grid } from '@element-plus/icons-vue'
</script>

<style>
.app {
  height: 100vh;
  width: 100%;
}

.el-aside {
  background-color: #001529;
  color: white;
  height: 100vh;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
}

.el-menu-vertical:not(.el-menu--collapse) {
  width: 200px;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
    'Noto Color Emoji';
}
</style>