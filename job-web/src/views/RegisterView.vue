<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow p-4" style="width: 400px;">
      <h3 class="text-center mb-4">新用户注册</h3>

      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label class="form-label">账号</label>
          <input type="text" class="form-control" v-model="form.username" placeholder="请输入用户名" required>
        </div>

        <div class="mb-3">
          <label class="form-label">密码</label>
          <input type="password" class="form-control" v-model="form.password" placeholder="请输入密码" required>
        </div>

        <div class="mb-3">
          <label class="form-label">手机号</label>
          <input type="tel" class="form-control" v-model="form.phone" placeholder="方便联系（选填）">
        </div>

        <div class="mb-4">
          <label class="form-label">您的身份</label>
          <select class="form-select" v-model="form.role_type" required>
            <option value="1">我是求职者 (找工作)</option>
            <option value="2">我是招聘者 (招人)</option>
          </select>
        </div>

        <div class="d-grid gap-2">
          <button type="submit" class="btn btn-success">立即注册</button>
        </div>
      </form>

      <div class="mt-3 text-center">
        <small class="text-muted">已有账号？
          <a href="#" @click.prevent="$router.push('/login')">去登录</a>
        </small>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

// 使用 reactive 对象来管理表单数据
const form = reactive({
  username: '',
  password: '',
  phone: '',
  role_type: '1' // 默认选求职者
})

const handleRegister = async () => {
  try {
    // 调用我们在后端写的注册接口
    await axios.post('http://127.0.0.1:8000/api/users/register/', {
      username: form.username,
      password: form.password,
      phone: form.phone,
      role_type: parseInt(form.role_type) // 确保转成数字发送
    })

    alert('🎉 注册成功！请使用新账号登录。')
    router.push('/login') // 注册完跳去登录

  } catch (error) {
    console.error(error)
    // 如果用户名已存在，后端通常会报400
    if (error.response && error.response.data) {
       // 把后端返回的错误信息展示出来 (比如: username: ["该用户名已存在"])
       alert('注册失败：' + JSON.stringify(error.response.data))
    } else {
       alert('注册失败，请稍后再试')
    }
  }
}
</script>