<template>
  <div>
    <div class="bg-primary text-white py-5 text-center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
      <div class="container py-4">
        <h1 class="display-4 fw-bold">连接人才与机遇</h1>
        <p class="lead mb-4">最智能的匹配算法，帮你发现下一个可能</p>
        <div class="d-flex justify-content-center">
          <div class="input-group" style="max-width: 600px;">
            <input type="text" class="form-control form-control-lg" v-model="keyword" placeholder="搜职位、公司...">
            <button class="btn btn-warning px-4 fw-bold" @click="handleSearch">搜索</button>
          </div>
        </div>
      </div>
    </div>

    <div class="container mt-5">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h3>🔥 热门职位</h3>
        <router-link to="/jobs" class="text-decoration-none">查看全部 &gt;</router-link>
      </div>
      <div class="row">
        <div class="col-md-3 mb-4" v-for="job in hotJobs" :key="job.id">
          <div class="card h-100 shadow-sm border-0" @click="handleCardClick(`/jobs/${job.id}`)" style="cursor: pointer;">
            <div class="card-body">
              <h5 class="card-title text-truncate">{{ job.job_title }}</h5>
              <p class="text-success fw-bold">{{ job.salary_min }}-{{ job.salary_max }}k</p>
              <small class="text-muted">{{ job.company_name }}</small>
            </div>
          </div>
        </div>
      </div>

      <div class="d-flex justify-content-between align-items-center mt-4 mb-3">
        <h3>🏢 热门企业</h3>
        <router-link to="/companies" class="text-decoration-none">查看全部 &gt;</router-link>
      </div>
      <div class="row">
        <div class="col-md-3 mb-4" v-for="comp in hotCompanies" :key="comp.id">
          <div class="card h-100 shadow-sm text-center p-3" @click="handleCardClick(`/companies/${comp.id}`)" style="cursor: pointer;">
             <div class="fs-1 mb-2">🏢</div>
            <h5 class="fw-bold">{{ comp.company_name }}</h5>
            <small class="text-muted text-truncate">{{ comp.industry || '互联网' }}</small>
          </div>
        </div>
      </div>

      <div class="mt-4 mb-5">
        <div class="d-flex justify-content-between align-items-center">
          <h3>📰 最新资讯</h3>
          <router-link to="/news" class="text-decoration-none">查看更多 &gt;</router-link>
        </div>
        <div class="row mt-3">
          <div class="col-md-4 mb-3" v-for="news in latestNews" :key="news.id">
            <div class="card border-0 bg-light h-100 shadow-sm" style="cursor: pointer;" @click="$router.push(`/news/${news.id}`)">
              <div class="card-body">
                <h6 class="fw-bold text-truncate">{{ news.title }}</h6>
                <p class="small text-muted mb-0" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                  {{ news.summary }}
                </p>
              </div>
            </div>
          </div>
          <div v-if="latestNews.length === 0" class="col-12 text-muted text-center py-4">
             暂无资讯更新
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user' // 引入 store 用来判断是否登录

const userStore = useUserStore()
const router = useRouter()
const keyword = ref('')
const hotJobs = ref([])
const hotCompanies = ref([])
const latestNews = ref([])

const handleSearch = () => {
  // 跳转到职位列表页并带上参数
  router.push({ path: '/jobs', query: { search: keyword.value } })
}

onMounted(async () => {
  // 1. 删掉原来的 if (!token) router.push('/login')

  // 2. 无论是否登录，都去获取数据
  // 注意：axios 请求头需要判断一下，如果有 token 就带上，没有就不带
  const config = {}
  if (userStore.token) {
    config.headers = { 'Authorization': `Bearer ${userStore.token}` }
  }

  try {
    // 获取职位
    const jobRes = await axios.get('http://127.0.0.1:8000/api/jobs/', config)
    // 假设后端返回的数据结构没变
    hotJobs.value = jobRes.data.results ? jobRes.data.results.slice(0, 4) : jobRes.data.slice(0, 4)

    // 获取公司 (users/urls.py 里配置的 public_companies 应该是 AllowAny)
    const compRes = await axios.get('http://127.0.0.1:8000/api/users/companies/', config)
    hotCompanies.value = compRes.data.slice(0, 4)
    // 获取最新3条资讯
    const newsRes = await axios.get('http://127.0.0.1:8000/api/jobs/news/')
    latestNews.value = newsRes.data.slice(0, 3)
  } catch (e) {
    console.error(e)
  }
})

// 点击卡片时的检查函数
const handleCardClick = (path) => {
  if (!userStore.isLoggedIn) {
    alert('请先登录后再查看详情！')
    router.push('/login')
  } else {
    router.push(path)
  }
}



</script>