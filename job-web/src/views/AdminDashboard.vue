<template>
  <div>
    <nav class="navbar navbar-dark bg-dark mb-0">
      <div class="container">
        <span class="navbar-brand">🛡️ 平台管理中心 (Admin)</span>
        <button class="btn btn-outline-light btn-sm" @click="logout">退出登录</button>
      </div>
    </nav>

    <div class="d-flex" style="min-height: 100vh;">
      <div class="bg-light border-end p-3" style="width: 250px;">
        <div class="list-group list-group-flush">
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'recruiters' }" @click="currentTab = 'recruiters'">
            🏢 企业资质审核
            <span v-if="pendingRecruiters.length > 0" class="badge bg-danger ms-2">{{ pendingRecruiters.length }}</span>
          </button>
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'jobs' }" @click="currentTab = 'jobs'">
            📋 职位发布审核
            <span v-if="pendingJobs.length > 0" class="badge bg-danger ms-2">{{ pendingJobs.length }}</span>
          </button>
        </div>
      </div>

      <div class="flex-grow-1 p-4">

        <div v-if="currentTab === 'recruiters'">
          <h4>企业资质审核</h4>
          <hr>
          <div v-if="pendingRecruiters.length === 0" class="alert alert-success">✅ 目前没有待审核的企业。</div>
          <div class="card mb-3 shadow-sm" v-for="rec in pendingRecruiters" :key="rec.id">
            <div class="card-body">
              <h5 class="fw-bold">{{ rec.company_name }}</h5>
              <p class="text-muted mb-1">行业: {{ rec.industry || '未填' }} | 规模: {{ rec.company_scale || '未填' }}</p>
              <p class="text-muted small">地址: {{ rec.company_addr }}</p>
              <p class="bg-light p-2 rounded" style="white-space: pre-wrap;">简介: {{ rec.description || '无' }}</p>
              <div class="mt-3">
                <button class="btn btn-success me-2" @click="auditRecruiter(rec.id, 1)">✅ 审核通过</button>
                <button class="btn btn-danger" @click="auditRecruiter(rec.id, 2)">❌ 拒绝认证</button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="currentTab === 'jobs'">
          <h4>职位发布审核</h4>
          <hr>
          <div v-if="pendingJobs.length === 0" class="alert alert-success">✅ 目前没有待审核的职位。</div>
          <div class="card mb-3 shadow-sm" v-for="job in pendingJobs" :key="job.id">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="fw-bold mb-0">{{ job.job_title }}</h5>
                <span class="text-danger fw-bold">{{ job.salary_min }}k - {{ job.salary_max }}k</span>
              </div>
              <p class="text-muted small mt-2">发布公司: {{ job.company_name }} | 城市: {{ job.city }}</p>
              <p class="bg-light p-2 rounded" style="white-space: pre-wrap; font-size: 14px;">{{ job.description }}</p>
              <div class="mt-3">
                <button class="btn btn-success me-2" @click="auditJob(job.id, 1)">✅ 允许发布</button>
                <button class="btn btn-danger" @click="auditJob(job.id, 2)">❌ 违规驳回</button>
              </div>
            </div>
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

const router = useRouter()
const currentTab = ref('recruiters')
const pendingRecruiters = ref([])
const pendingJobs = ref([])
const token = localStorage.getItem('access_token')

// 获取待审核企业
const fetchPendingRecruiters = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/admin/recruiters/pending/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    pendingRecruiters.value = res.data
  } catch (error) { console.error(error) }
}

// 获取待审核职位
const fetchPendingJobs = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/jobs/admin/jobs/pending/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    pendingJobs.value = res.data
  } catch (error) { console.error(error) }
}

// 审核企业
const auditRecruiter = async (id, status) => {
  if(!confirm(status === 1 ? '确认通过该企业资质？' : '确认拒绝该企业？')) return
  try {
    await axios.patch(`http://127.0.0.1:8000/api/users/admin/recruiters/${id}/audit/`, { audit_status: status }, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    fetchPendingRecruiters() // 刷新列表
  } catch (error) { alert('操作失败') }
}

// 审核职位
const auditJob = async (id, status) => {
  if(!confirm(status === 1 ? '确认允许该职位发布上架？' : '确认驳回该职位？')) return
  try {
    await axios.patch(`http://127.0.0.1:8000/api/jobs/admin/jobs/${id}/audit/`, { status: status }, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    fetchPendingJobs() // 刷新列表
  } catch (error) { alert('操作失败') }
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('role_type')
  router.push('/login')
}

onMounted(() => {
  if (!token) {
    alert('请先登录！')
    router.push('/login')
    return
  }
  fetchPendingRecruiters()
  fetchPendingJobs()
})
</script>