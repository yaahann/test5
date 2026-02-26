<template>
  <div class="container mt-4 mb-5">
    <button class="btn btn-outline-secondary mb-3" @click="$router.back()">&lt; 返回上一页</button>

    <div class="card shadow-sm border-0" v-if="news">
      <div class="card-body p-5">
        <h2 class="fw-bold mb-3 text-center">{{ news.title }}</h2>
        <div class="text-center text-muted mb-4 pb-3 border-bottom">
          <span class="me-4">🕒 发布时间：{{ news.publish_time }}</span>
          <span>👁️ 阅读量：{{ news.views }}</span>
        </div>

        <div v-if="news.summary" class="alert alert-secondary border-start border-4 border-primary">
          <strong>导读：</strong>{{ news.summary }}
        </div>

        <div class="news-content mt-4" style="white-space: pre-wrap; line-height: 2; font-size: 16px; color: #333;">
          {{ news.content }}
        </div>
      </div>
    </div>

    <div v-else class="text-center py-5 mt-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">文章加载中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const news = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/jobs/news/${route.params.id}/`)
    news.value = res.data
  } catch (error) {
    console.error('获取资讯详情失败', error)
    alert('文章不存在或已被删除')
  }
})
</script>