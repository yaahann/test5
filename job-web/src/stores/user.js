// src/stores/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 1. 定义数据 (State)
  // 初始化时尝试从 localStorage 读取，这样刷新页面也不会丢
  const token = ref(localStorage.getItem('access_token') || '')
  const username = ref(localStorage.getItem('username') || '')
  const role = ref(localStorage.getItem('role_type') || '')

  // 2. 定义计算属性 (Getters)
  // 用来判断是否登录
  const isLoggedIn = computed(() => !!token.value)

  // 3. 定义动作 (Actions)
  // 登录动作：存数据到 Pinia 和 localStorage
  function login(data) {
    token.value = data.access
    username.value = data.username
    role.value = data.role_type

    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    localStorage.setItem('username', data.username)
    localStorage.setItem('role_type', data.role_type)
  }

  // 退出动作：清空所有数据
  function logout() {
    token.value = ''
    username.value = ''
    role.value = ''
    localStorage.clear()
  }

  return { token, username, role, isLoggedIn, login, logout }
})