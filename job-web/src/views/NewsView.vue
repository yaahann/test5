<template>
  <div class="container mt-4">
    <h3 class="mb-4">📰 求职资讯</h3>
    <div class="row">
      <div class="col-md-8">

        <div class="card mb-3 border-0 shadow-sm hover-card" v-for="item in newsList" :key="item.id" @click="$router.push(`/news/${item.id}`)">
          <div class="card-body">
            <h5 class="card-title fw-bold text-primary">{{ item.title }}</h5>
            <p class="card-text text-muted">{{ item.summary }}</p>
            <small class="text-muted">发布于 {{ item.publish_time }} • 阅读 {{ item.views }}</small>
          </div>
        </div>

        <div v-if="newsList.length === 0" class="text-center text-muted py-5">
           暂无最新资讯...
        </div>

      </div>

      <div class="col-md-4">
        <div class="card bg-light border-0 p-3 sticky-top" style="top: 20px;">
          <h5>🔥 热门话题</h5>
          <ul class="list-unstyled mt-2">
            <li class="mb-2"><a href="#" class="text-decoration-none text-dark"># 2026春招攻略</a></li>
            <li class="mb-2"><a href="#" class="text-decoration-none text-dark"># 简历优化技巧</a></li>
            <li class="mb-2"><a href="#" class="text-decoration-none text-dark"># 算法面试高频题</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const newsList = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/jobs/news/')
    newsList.value = res.data
  } catch (error) {
    console.error('获取资讯失败', error)
  }
})
</script>

<style scoped>
.hover-card {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}
.hover-card:hover {
  transform: translateX(5px);
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.1) !important;
}
</style>