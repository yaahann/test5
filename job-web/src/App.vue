<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm sticky-top">
      <div class="container">
        <a class="navbar-brand fw-bold" href="#" @click.prevent="$router.push('/home')">
          🚀 智能求职系统
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/home" class="nav-link" active-class="active">🏠 首页</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/jobs" class="nav-link" active-class="active">💼 职位大厅</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/companies" class="nav-link" active-class="active">🏢 热门企业</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/news" class="nav-link" active-class="active">📰 求职资讯</router-link>
            </li>
          </ul>

          <div class="d-flex align-items-center">
            <template v-if="userStore.isLoggedIn">
              <span class="text-light me-3">你好, {{ userStore.username }}</span>
              <button class="btn btn-outline-light btn-sm me-2" @click="goToDashboard">个人中心</button>
              <button class="btn btn-danger btn-sm" @click="logout">退出</button>
            </template>
            <template v-else>
              <router-link to="/login" class="btn btn-primary btn-sm me-2">登录</router-link>
              <router-link to="/register" class="btn btn-outline-light btn-sm">注册</router-link>
            </template>
          </div>

        </div>
      </div>
    </nav>

    <div style="min-height: 80vh;">
      <RouterView />
    </div>

    <footer class="bg-light text-center py-4 mt-5">
      <p class="text-muted mb-0">© 2026 智能求职推荐系统 | 毕业设计演示</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from './stores/user'

const router = useRouter()
const username = localStorage.getItem('username')
const isLoggedIn = computed(() => !!localStorage.getItem('access_token'))
const userStore = useUserStore()

const goToDashboard = () => {
  const role = localStorage.getItem('role_type')
  if (role == '2') router.push('/recruiter/dashboard')
  else router.push('/seeker/dashboard')
}

// 这里的 logout 直接调用仓库的方法
const logout = () => {
  if(confirm('确定要退出吗？')) {
    userStore.logout() // 调用 Pinia 的 logout，它会自动清空 localStorage 并更新页面
    router.push('/login')
  }
}



</script>

<style>
.nav-link.active {
  font-weight: bold;
  color: #fff !important;
  border-bottom: 2px solid #0d6efd;
}
</style>