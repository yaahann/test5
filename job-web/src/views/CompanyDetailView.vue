<template>
  <div class="container mt-4" v-if="company">
    <button class="btn btn-outline-secondary mb-3" @click="$router.back()">&lt; 返回</button>
    <div class="card border-0 shadow-sm bg-white mb-4">
      <div class="card-body p-5 text-center">
        <div class="display-1 mb-3">🏢</div>
        <h1 class="fw-bold">{{ company.company_name || '未命名公司' }}</h1>

        <p class="lead text-muted">
          📍 {{ company.company_addr || '企业地址未完善' }}
        </p>

        <div class="mt-3 mb-3">
          <span class="badge bg-primary me-2 px-3 py-2 fs-6" v-if="company.industry">
            {{ company.industry }}
          </span>
          <span class="badge bg-info text-dark me-2 px-3 py-2 fs-6" v-if="company.company_scale">
            {{ company.company_scale }}
          </span>
        </div>

        <hr class="my-4" style="width: 100px; margin: 0 auto;">

        <div class="text-secondary text-start" style="max-width: 800px; margin: 0 auto; white-space: pre-wrap; line-height: 1.8;">
          {{ company.description || '这家公司很懒，暂时没有详细介绍。' }}
        </div>
      </div>
    </div>

    <h4 class="mb-3">🔥 正在热招 ({{ jobs.length }})</h4>
    <div class="row">
      <div class="col-md-6 mb-3" v-for="job in jobs" :key="job.id">
        <div class="card h-100 shadow-sm" @click="$router.push(`/jobs/${job.id}`)" style="cursor: pointer;">
          <div class="card-body">
            <h5 class="card-title text-primary">{{ job.job_title }}</h5>
            <div class="d-flex justify-content-between align-items-center mt-2">
              <span class="text-danger fw-bold">{{ job.salary_min }}-{{ job.salary_max }}k</span>
              <small class="text-muted">{{ job.city }} | {{ job.education_req }}</small>
            </div>
          </div>
        </div>
      </div>
      <div v-if="jobs.length === 0" class="col-12 text-center text-muted py-5">
        该公司暂时没有招聘中的职位。
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const company = ref(null)
const jobs = ref([])

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  const compId = route.params.id

  // 1. 获取公司详情
  const compRes = await axios.get(`http://127.0.0.1:8000/api/users/companies/${compId}/`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  company.value = compRes.data

  // 2. 获取该公司下的职位
  const jobRes = await axios.get('http://127.0.0.1:8000/api/jobs/', {
    headers: { 'Authorization': `Bearer ${token}` },
    params: { recruiter_id: compId }
  })
  jobs.value = jobRes.data
})
</script>

<style scoped>
/* 悬浮特效 */
.card {
  transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important;
}
</style>