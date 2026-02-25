<template>
  <div class="container mt-4">
    <h3 class="mb-4">🏢 热门招聘企业</h3>
    <div class="row">
      <div class="col-md-3 mb-4" v-for="company in companies" :key="company.id">
        <div class="card h-100 shadow-sm text-center p-4 hover-up" @click="$router.push(`/companies/${company.id}`)" style="cursor: pointer;">
          <div class="mb-3 display-4">🏢</div> <h5 class="fw-bold">{{ company.company_name }}</h5>
          <button class="btn btn-outline-primary btn-sm">查看 {{ company.job_count || '' }} 在招职位</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const companies = ref([])

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  const res = await axios.get('http://127.0.0.1:8000/api/users/companies/', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  companies.value = res.data
})
</script>

<style>
.hover-up { transition: transform 0.2s; }
.hover-up:hover { transform: translateY(-5px); }
</style>