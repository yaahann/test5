<template>
  <div class="container mt-4">

    <div class="card p-4 mb-3 bg-white shadow-sm border-0">
      <div class="row g-2">
        <div class="col-md-10">
          <input type="text" class="form-control form-control-lg bg-light border-0" v-model="search" placeholder="输入职位名称、公司名称或技能关键字..." @keyup.enter="fetchJobs">
        </div>
        <div class="col-md-2 d-grid">
          <button class="btn btn-primary btn-lg fw-bold" @click="fetchJobs">🔍 搜索职位</button>
        </div>
      </div>
    </div>

    <div class="card p-4 mb-4 bg-white shadow-sm border-0">
      <div class="d-flex align-items-center mb-3">
        <span class="fw-bold me-3 text-muted" style="min-width: 60px;">工作城市</span>
        <div class="d-flex flex-wrap gap-2">
          <span class="badge filter-badge" :class="filters.city === '全部' ? 'bg-primary' : 'bg-light text-dark'" @click="setFilter('city', '全部')">全国</span>
          <span class="badge filter-badge" :class="filters.city === city ? 'bg-primary' : 'bg-light text-dark'" v-for="city in filterOptions.cities" :key="city" @click="setFilter('city', city)">{{ city }}</span>
        </div>
      </div>

      <div class="d-flex align-items-center mb-3">
        <span class="fw-bold me-3 text-muted" style="min-width: 60px;">学历要求</span>
        <div class="d-flex flex-wrap gap-2">
          <span class="badge filter-badge" :class="filters.education_req === '不限' ? 'bg-primary' : 'bg-light text-dark'" @click="setFilter('education_req', '不限')">不限</span>
          <span class="badge filter-badge" :class="filters.education_req === edu ? 'bg-primary' : 'bg-light text-dark'" v-for="edu in filterOptions.educations" :key="edu" @click="setFilter('education_req', edu)">{{ edu }}</span>
        </div>
      </div>

      <div class="d-flex align-items-center mb-3">
        <span class="fw-bold me-3 text-muted" style="min-width: 60px;">经验要求</span>
        <div class="d-flex flex-wrap gap-2">
          <span class="badge filter-badge" :class="filters.exp_req === '不限' ? 'bg-primary' : 'bg-light text-dark'" @click="setFilter('exp_req', '不限')">不限</span>
          <span class="badge filter-badge" :class="filters.exp_req === exp ? 'bg-primary' : 'bg-light text-dark'" v-for="exp in filterOptions.experiences" :key="exp" @click="setFilter('exp_req', exp)">{{ exp }}</span>
        </div>
      </div>

      <div class="d-flex align-items-center">
        <span class="fw-bold me-3 text-muted" style="min-width: 60px;">职位类型</span>
        <div class="d-flex flex-wrap gap-2">
          <span class="badge filter-badge" :class="filters.job_type === '全部' ? 'bg-primary' : 'bg-light text-dark'" @click="setFilter('job_type', '全部')">全部</span>
          <span class="badge filter-badge" :class="filters.job_type === type ? 'bg-primary' : 'bg-light text-dark'" v-for="type in filterOptions.jobTypes" :key="type" @click="setFilter('job_type', type)">{{ type }}</span>
        </div>
      </div>
    </div>

    <h5 class="mb-3 fw-bold">为您找到 {{ jobs.length }} 个职位</h5>
    <div class="row">
      <div class="col-md-12 mb-3" v-for="job in jobs" :key="job.id">
        <div class="card shadow-sm hover-shadow border-0" @click="$router.push(`/jobs/${job.id}`)" style="cursor: pointer;">
          <div class="card-body p-4 d-flex justify-content-between align-items-center">
            <div>
              <h5 class="card-title text-primary fw-bold mb-2">{{ job.job_title }}</h5>
              <div class="mb-2">
                <span class="badge bg-light text-dark border me-2 px-2 py-1">{{ job.city }}</span>
                <span class="badge bg-light text-dark border me-2 px-2 py-1">{{ job.exp_req }}</span>
                <span class="badge bg-light text-dark border me-2 px-2 py-1">{{ job.education_req }}</span>
                <span class="badge bg-light text-dark border px-2 py-1">{{ job.job_type }}</span>
              </div>
              <small class="text-muted">
                🏢 <span class="fw-bold text-dark">{{ job.company_name || '知名企业' }}</span> | 发布于 {{ new Date(job.create_time).toLocaleDateString() }}
              </small>
            </div>
            <div class="text-end">
              <h3 class="text-danger fw-bold mb-2">{{ job.salary_min }}-{{ job.salary_max }}k</h3>
              <button class="btn btn-primary px-4 rounded-pill">投递简历</button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="jobs.length === 0" class="col-12 text-center py-5 mt-4">
        <h1 class="display-1 text-muted mb-3">📭</h1>
        <h4 class="text-muted">抱歉，没有找到符合条件的职位</h4>
        <p class="text-secondary">建议您减少筛选条件或更换关键词重新搜索</p>
        <button class="btn btn-outline-primary mt-2" @click="resetFilters">清空所有筛选条件</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const jobs = ref([])
const search = ref('')

// 筛选项配置
const filterOptions = {
  cities: ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', '苏州'],
  educations: ['大专', '本科', '硕士', '博士'],
  experiences: ['1年以内', '1-3年', '3-5年', '5-10年', '10年以上'],
  jobTypes: ['全职', '实习', '兼职']
}

// 当前选中的筛选状态
const filters = reactive({
  city: '全部',
  education_req: '不限',
  exp_req: '不限',
  job_type: '全部'
})

// 点击筛选标签的事件
const setFilter = (key, value) => {
  filters[key] = value
  fetchJobs() // 选中后直接发起请求，无需点搜索按钮
}

// 清空所有条件
const resetFilters = () => {
  search.value = ''
  filters.city = '全部'
  filters.education_req = '不限'
  filters.exp_req = '不限'
  filters.job_type = '全部'
  fetchJobs()
}

// 核心请求方法
const fetchJobs = async () => {
  const token = localStorage.getItem('access_token')

  // 1. 组装请求参数
  const params = {}
  if (search.value) params.search = search.value
  if (filters.city !== '全部') params.city = filters.city
  if (filters.education_req !== '不限') params.education_req = filters.education_req
  if (filters.exp_req !== '不限') params.exp_req = filters.exp_req
  if (filters.job_type !== '全部') params.job_type = filters.job_type

  // 2. 发起请求
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/jobs/', {
      // 允许未登录用户浏览，所以只有 token 存在时才加 header
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
      params: params
    })
    jobs.value = res.data
  } catch (error) {
    console.error('获取职位列表失败:', error)
  }
}

onMounted(() => {
  // 如果从首页搜索框带了搜索词跳转过来
  if (route.query.search) {
    search.value = route.query.search
  }
  fetchJobs()
})
</script>

<style scoped>
/* 筛选项标签的交互样式 */
.filter-badge {
  cursor: pointer;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: normal;
  transition: all 0.2s;
}
.filter-badge:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* 职位卡片的悬浮特效 */
.hover-shadow {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.hover-shadow:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1.5rem rgba(0,0,0,0.15)!important;
}
</style>