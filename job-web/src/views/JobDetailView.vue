<template>
  <div class="container mt-4" v-if="job">
    <button class="btn btn-outline-secondary mb-3" @click="$router.back()">&lt; 返回</button>

    <div class="row">
      <div class="col-md-8">
        <div class="card shadow-sm mb-4 border-0">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h2 class="fw-bold mb-0">{{ job.job_title }}</h2>
              <h3 class="text-danger mb-0">{{ job.salary_min }}k - {{ job.salary_max }}k</h3>
            </div>

            <div class="text-muted mb-3 fs-6">
              <span class="me-3">📍 {{ job.city }}</span>
              <span class="me-3">💼 {{ job.exp_req }}</span>
              <span class="me-3">🎓 {{ job.education_req }}</span>
              <span class="me-3">⏱️ {{ job.job_type }}</span>
            </div>

            <div class="mb-4" v-if="job.job_tags">
              <span
                v-for="(tag, index) in parseTags(job.job_tags)"
                :key="index"
                class="badge bg-light text-dark border me-2 px-3 py-2 fw-normal"
              >
                {{ tag }}
              </span>
            </div>

            <hr class="my-4">

            <h5 class="fw-bold mb-3">职位详情</h5>
            <div class="text-secondary" style="white-space: pre-wrap; line-height: 1.8;">
              {{ job.description }}
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow-sm border-0 mb-4 sticky-top" style="top: 20px;">
          <div class="card-body p-4">
            <h5 class="fw-bold mb-3">所属公司</h5>

            <div
              class="d-flex align-items-center mb-4 company-card p-2 rounded"
              @click="goToCompany(job.recruiter_id)"
            >
              <div class="bg-light rounded text-center me-3" style="width: 50px; height: 50px; line-height: 50px; font-size: 24px;">
                🏢
              </div>
              <div>
                <h6 class="mb-1 text-primary fw-bold mb-0">
                  {{ job.company_name || '查看企业主页' }}
                </h6>
                <small class="text-muted">点击查看公司详情</small>
              </div>
            </div>

            <button class="btn btn-primary w-100 py-2 fw-bold" @click="openApplyModal">
              🚀 立即投递简历
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="applyModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">选择要投递的简历</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="myResumes.length === 0" class="alert alert-danger">
              您还没有上传简历，请先去个人中心上传！
            </div>

            <div v-else class="list-group">
              <button
                v-for="resume in myResumes"
                :key="resume.id"
                class="list-group-item list-group-item-action"
                :class="{ active: selectedResumeId === resume.id }"
                @click="selectedResumeId = resume.id"
              >
                {{ resume.resume_title }}
                <small class="text-muted ms-2">({{ new Date(resume.create_time).toLocaleDateString() }})</small>
              </button>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
            <button type="button" class="btn btn-primary" @click="confirmApply" :disabled="!selectedResumeId">确认投递</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="container mt-5 text-center" v-else>
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <p class="mt-2 text-muted">职位信息加载中...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { Modal } from 'bootstrap' //  Bootstrap JS 控制弹窗

const route = useRoute()
const router = useRouter()
const job = ref(null)

// 投递相关状态
const myResumes = ref([])
const selectedResumeId = ref(null)
const token = localStorage.getItem('access_token') || localStorage.getItem('token')
let applyModal = null

// --- 新增工具函数 ---

// 解析职位标签 (兼容中英文逗号)
const parseTags = (tagsString) => {
  if (!tagsString) return []
  return tagsString.split(/[,，]/).filter(t => t.trim() !== '')
}

// 跳转到公司详情页
const goToCompany = (companyId) => {
  console.log("准备跳转，获取到的公司ID是：", companyId);
  if (companyId) {
    router.push(`/companies/${companyId}`)
  } else {
    alert('暂无法获取该公司ID信息')
  }
}

// --- 原有核心逻辑 ---

// 1. 获取职位详情
const fetchJobDetail = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/jobs/${route.params.id}/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    job.value = res.data
    console.log("后端返回的职位详情：", job.value)
  } catch (error) {
    console.error('获取职位详情失败:', error)
    alert('该职位不存在或已被删除')
    router.push('/jobs') // 获取失败退回列表页
  }
}

// 2. 打开投递弹窗 (同时加载简历列表)
const openApplyModal = async () => {
  if (!token) {
    alert('请先登录您的求职者账号！')
    router.push('/login')
    return
  }

  try {
    // 先获取简历列表
    const res = await axios.get('http://127.0.0.1:8000/api/recruitment/resumes/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    myResumes.value = res.data

    // 如果有简历，默认选中第一个
    if (myResumes.value.length > 0) {
      selectedResumeId.value = myResumes.value[0].id
    }

    // 显示弹窗
    applyModal = new Modal(document.getElementById('applyModal'))
    applyModal.show()
  } catch (e) {
    alert('无法加载简历列表，请检查网络或确认您是否为求职者账号')
  }
}

// 3. 确认投递
const confirmApply = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/api/recruitment/applications/',
      {
        job: job.value.id,
        resume: selectedResumeId.value
      },
      { headers: { 'Authorization': `Bearer ${token}` } }
    )

    // 关闭弹窗
    if (applyModal) applyModal.hide()
    alert('🎉 投递成功！')

    // 如果想要投递完留在当前页，注释掉下面这行；如果要回到首页，保留。
    // router.push('/home')

  } catch (error) {
    alert('投递失败：' + (error.response?.data?.message || error.response?.data?.detail || '您可能已经投递过该职位'))
  }
}

onMounted(() => {
  fetchJobDetail()
})
</script>

<style scoped>
/* 悬浮可点击元素的交互特效 */
.company-card {
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
}
.company-card:hover {
  background-color: #f8f9fa;
  transform: translateX(5px);
}
</style>