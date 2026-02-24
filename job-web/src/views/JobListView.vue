<template>
  <div class="container mt-4">
    <div class="card p-4 mb-4 bg-light border-0">
      <div class="row">
        <div class="col-md-10">
          <input type="text" class="form-control" v-model="search" placeholder="搜索职位名称、技能..." @keyup.enter="fetchJobs">
        </div>
        <div class="col-md-2 d-grid">
          <button class="btn btn-primary" @click="fetchJobs">搜索</button>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12 mb-3" v-for="job in jobs" :key="job.id">
        <div class="card shadow-sm hover-shadow" @click="$router.push(`/jobs/${job.id}`)" style="cursor: pointer;">
          <div class="card-body d-flex justify-content-between align-items-center">
            <div>
              <h5 class="card-title text-primary fw-bold mb-1">{{ job.job_title }}</h5>
              <div class="mb-2">
                <span class="badge bg-light text-dark border me-2">{{ job.city }}</span>
                <span class="badge bg-light text-dark border me-2">{{ job.education_req }}</span>
                <span class="badge bg-light text-dark border">{{ job.job_type }}</span>
              </div>
              <small class="text-muted">{{ job.company_name }} | 发布于 {{ new Date(job.create_time).toLocaleDateString() }}</small>
            </div>
            <div class="text-end">
              <h4 class="text-success fw-bold">{{ job.salary_min }}-{{ job.salary_max }}k</h4>
              <button class="btn btn-sm btn-outline-primary mt-2">查看详情</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const jobs = ref([])
const search = ref('')

const fetchJobs = async () => {
  const token = localStorage.getItem('access_token')
  const params = { search: search.value }
  const res = await axios.get('http://127.0.0.1:8000/api/jobs/', {
    headers: { 'Authorization': `Bearer ${token}` },
    params
  })
  jobs.value = res.data
}

onMounted(() => {
  // 如果从首页带了搜索词过来
  if (route.query.search) {
    search.value = route.query.search
  }
  fetchJobs()
})
</script>

<style>
.hover-shadow:hover { box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15)!important; }
</style>