<template>
  <div>
    <nav class="navbar navbar-dark bg-dark mb-0">
      <div class="container">
        <span class="navbar-brand">🛡️ 平台管理中心 (Admin)</span>
        <button class="btn btn-outline-light btn-sm" @click="$router.push('/home')">返回首页</button>
      </div>
    </nav>

    <div class="d-flex" style="min-height: 100vh;">
      <div class="bg-light border-end p-3 flex-shrink-0" style="width: 250px;">
        <div class="list-group list-group-flush">
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'recruiters' }" @click="currentTab = 'recruiters'">
            🏢 企业资质审核
            <span v-if="pendingRecruiters.length > 0" class="badge bg-danger ms-2">{{ pendingRecruiters.length }}</span>
          </button>
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'jobs' }" @click="currentTab = 'jobs'">
            📋 职位发布审核
            <span v-if="pendingJobs.length > 0" class="badge bg-danger ms-2">{{ pendingJobs.length }}</span>
          </button>
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'stats' }" @click="currentTab = 'stats'">
            📊 数据监控大盘
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
              <div v-if="rec.license" class="mb-3">
                <span class="fw-bold">📎 资质文件：</span>
                <a :href="getMediaUrl(rec.license)" target="_blank" class="btn btn-sm btn-outline-primary">
                  📄 点击查看营业执照
                </a>
              </div>
              <div v-else class="mb-3 text-danger small">
                ⚠️ 该企业尚未上传任何资质认证文件！
              </div>
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

        <div v-if="currentTab === 'stats'">
          <h4>数据监控大盘</h4>
          <hr>

          <div class="row mt-4" v-if="sysStats">
            <div class="col-md-4 mb-4">
               <div class="card text-white bg-primary h-100 shadow-sm border-0">
                  <div class="card-body">
                    <h6 class="card-title text-white-50">👥 平台总用户数</h6>
                    <h2 class="fw-bold mb-0 mt-2">{{ sysStats.total_users }} <small class="fs-6 fw-normal text-white-50">人</small></h2>
                  </div>
               </div>
            </div>
            <div class="col-md-4 mb-4">
               <div class="card text-white bg-info h-100 shadow-sm border-0"
                    style="cursor: pointer; transition: transform 0.2s;"
                    @click="currentTab = 'all_seekers'"
                    onmouseover="this.style.transform='scale(1.05)'"
                    onmouseout="this.style.transform='scale(1)'">
                  <div class="card-body">
                    <h6 class="card-title text-white-50">🧑‍🎓 注册求职者 (点击查看)</h6>
                    <h2 class="fw-bold mb-0 mt-2">{{ sysStats.total_seekers }} <small class="fs-6 fw-normal text-white-50">人</small></h2>
                  </div>
               </div>
            </div>

            <div class="col-md-4 mb-4">
               <div class="card text-white bg-secondary h-100 shadow-sm border-0"
                    style="cursor: pointer; transition: transform 0.2s;"
                    @click="currentTab = 'all_recruiters'"
                    onmouseover="this.style.transform='scale(1.05)'"
                    onmouseout="this.style.transform='scale(1)'">
                  <div class="card-body">
                    <h6 class="card-title text-white-50">🏢 入驻企业数 (点击查看)</h6>
                    <h2 class="fw-bold mb-0 mt-2">{{ sysStats.total_recruiters }} <small class="fs-6 fw-normal text-white-50">家</small></h2>
                  </div>
               </div>
            </div>

            <div class="col-md-4 mb-4">
               <div class="card text-dark bg-light h-100 shadow-sm border-0 border-start border-4 border-success"
                    style="cursor: pointer; transition: transform 0.2s;"
                    @click="currentTab = 'all_jobs'"
                    onmouseover="this.style.transform='scale(1.05)'"
                    onmouseout="this.style.transform='scale(1)'">
                  <div class="card-body">
                    <h6 class="card-title text-muted">✅ 职位总数 (点击查看)</h6>
                    <h2 class="fw-bold text-success mb-0 mt-2">{{ sysStats.total_jobs }} <small class="fs-6 fw-normal text-muted">个</small></h2>
                  </div>
               </div>
            </div>
            <div class="col-md-4 mb-4">
               <div class="card text-dark bg-light h-100 shadow-sm border-0 border-start border-4 border-warning">
                  <div class="card-body">
                    <h6 class="card-title text-muted">⏳ 待审职位</h6>
                    <h2 class="fw-bold text-warning mb-0 mt-2">{{ sysStats.pending_jobs }} <small class="fs-6 fw-normal text-muted">个</small></h2>
                  </div>
               </div>
            </div>
            <div class="col-md-4 mb-4">
               <div class="card text-white bg-danger h-100 shadow-sm border-0">
                  <div class="card-body">
                    <h6 class="card-title text-white-50">🚀 平台总投递次数</h6>
                    <h2 class="fw-bold mb-0 mt-2">{{ sysStats.total_applications }} <small class="fs-6 fw-normal text-white-50">次</small></h2>
                  </div>
               </div>
            </div>
          </div>

          <div v-else class="text-center text-muted py-5">
             <div class="spinner-border text-primary" role="status"></div>
             <p class="mt-2">数据加载中...</p>
          </div>
        </div>

        <div v-if="currentTab === 'all_seekers'">
          <div class="d-flex justify-content-between mb-3">
            <h4>🧑‍🎓 求职者管理</h4>
            <button class="btn btn-sm btn-outline-secondary" @click="currentTab = 'stats'">返回大盘</button>
          </div>
          <table class="table table-hover bg-white shadow-sm rounded">
            <thead class="table-light"><tr><th>ID</th><th>姓名</th><th>性别</th><th>学历</th><th>求职状态</th></tr></thead>
            <tbody>
              <tr v-for="user in allSeekers" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.name || '未填' }}</td>
                <td>{{ user.gender || '-' }}</td>
                <td>{{ user.education || '-' }}</td>
                <td><span class="badge bg-info">{{ user.job_status === 0 ? '待业' : '在职' }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="currentTab === 'all_recruiters'">
          <div class="d-flex justify-content-between mb-3">
            <h4>🏢 入驻企业管理</h4>
            <button class="btn btn-sm btn-outline-secondary" @click="currentTab = 'stats'">返回大盘</button>
          </div>
          <table class="table table-hover bg-white shadow-sm rounded">
            <thead class="table-light"><tr><th>公司名称</th><th>行业</th><th>规模</th><th>状态</th></tr></thead>
            <tbody>
              <tr v-for="comp in allRecruiters" :key="comp.id">
                <td>{{ comp.company_name || '未填' }}</td>
                <td>{{ comp.industry || '-' }}</td>
                <td>{{ comp.company_scale || '-' }}</td>
                <td>
                  <span class="badge" :class="comp.audit_status === 1 ? 'bg-success' : (comp.audit_status === 2 ? 'bg-danger' : 'bg-warning text-dark')">
                    {{ comp.audit_status === 1 ? '通过' : (comp.audit_status === 2 ? '拒绝' : '待审') }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="currentTab === 'all_jobs'">
          <div class="d-flex justify-content-between mb-3">
            <h4>📋 全站职位管理</h4>
            <button class="btn btn-sm btn-outline-secondary" @click="currentTab = 'stats'">返回大盘</button>
          </div>
          <table class="table table-hover bg-white shadow-sm rounded">
            <thead class="table-light"><tr><th>职位名称</th><th>薪资</th><th>城市</th><th>状态</th></tr></thead>
            <tbody>
              <tr v-for="job in allJobs" :key="job.id">
                <td><a href="#" @click.prevent="$router.push(`/jobs/${job.id}`)">{{ job.job_title }}</a></td>
                <td class="text-danger">{{ job.salary_min }}-{{ job.salary_max }}k</td>
                <td>{{ job.city }}</td>
                <td>
                  <span class="badge" :class="job.status === 1 ? 'bg-success' : (job.status === 2 ? 'bg-secondary' : 'bg-warning text-dark')">
                    {{ job.status === 1 ? '招聘中' : (job.status === 2 ? '已下架' : '待审核') }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
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
const allSeekers = ref([])
const allRecruiters = ref([])
const allJobs = ref([])

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

// 辅助函数：处理媒体文件的绝对路径
const getMediaUrl = (path) => {
  if (!path) return '#'
  if (path.startsWith('http')) return path
  // 拼接 Django 后端地址
  return `http://127.0.0.1:8000${path}`
}


// 新增存储统计数据的变量
const sysStats = ref(null)

// 新增获取统计数据的方法
const fetchStats = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/admin/stats/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    sysStats.value = res.data
  } catch (error) {
    console.error('获取监控数据失败', error)
  }
}

// 编写请求函数
const fetchAllSeekers = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/admin/seekers/all/', { headers: { 'Authorization': `Bearer ${token}` } })
    allSeekers.value = res.data
  } catch (e) { console.error(e) }
}
const fetchAllRecruiters = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/admin/recruiters/all/', { headers: { 'Authorization': `Bearer ${token}` } })
    allRecruiters.value = res.data
  } catch (e) { console.error(e) }
}
const fetchAllJobs = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/jobs/admin/jobs/all/', { headers: { 'Authorization': `Bearer ${token}` } })
    allJobs.value = res.data
  } catch (e) { console.error(e) }
}

onMounted(() => {
  if (!token) {
    alert('请先登录！')
    router.push('/login')
    return
  }
  fetchStats()
  fetchPendingRecruiters()
  fetchPendingJobs()
  fetchAllSeekers()
  fetchAllRecruiters()
  fetchAllJobs()
})
</script>