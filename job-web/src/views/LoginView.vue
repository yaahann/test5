<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow p-4" style="width: 400px;">
      <h3 class="text-center mb-4">系统登录</h3>

      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label class="form-label">账号</label>
          <input type="text" class="form-control" v-model="username" placeholder="请输入用户名" required>
        </div>

        <div class="mb-3">
          <label class="form-label">密码</label>
          <input type="password" class="form-control" v-model="password" placeholder="请输入密码" required>
        </div>

        <div class="d-grid gap-2">
          <button type="submit" class="btn btn-primary">立即登录</button>
        </div>
      </form>

      <div class="mt-3 text-center">
        <small class="text-muted">还没有账号？<a href="#" @click.prevent="$router.push('/register')">去注册</a></small>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router' // 1. 引入路由工具

const router = useRouter() // 2. 初始化路由
const username = ref('')
const password = ref('')

import { useUserStore } from '../stores/user' // 引入
const userStore = useUserStore() // 初始化

const handleLogin = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/users/login/', {
      username: username.value,
      password: password.value
    })

    // 🟢 关键修改：使用 Store 的 action 来登录
    // 这行代码执行后，App.vue 里的导航栏会瞬间自动更新！
    userStore.login(response.data)

    alert('登录成功！')
    router.push('/home')

  } catch (error) {
    console.error(error)
    alert('登录失败，请检查账号密码！')
  }
}

</script>