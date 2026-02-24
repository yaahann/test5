<template>
  <div class="container mt-5">
    <button class="btn btn-outline-secondary mb-3" @click="$router.back()">&lt; 返回列表</button>

    <div v-if="job" class="card shadow-lg">
      <div class="card-header bg-white p-4">
        <h2>{{ job.job_title }}</h2>
        <h5 class="text-muted">{{ job.company_name }}</h5>
        </div>
      <div class="card-body p-4">
        <p style="white-space: pre-wrap;">{{ job.description }}</p>
        <hr>
        <div class="d-flex justify-content-end">
          <button class="btn btn-primary btn-lg" @click="openApplyModal">立即投递</button>
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { Modal } from 'bootstrap' // 引入 Bootstrap JS 控制弹窗

const route = useRoute()
const router = useRouter()
const job = ref(null)
const myResumes = ref([])
const selectedResumeId = ref(null)
const token = localStorage.getItem('access_token')
let applyModal = null

// 1. 获取职位详情
const fetchJobDetail = async () => {
  const res = await axios.get(`http://127.0.0.1:8000/api/jobs/${route.params.id}/`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  job.value = res.data
}

// 2. 打开投递弹窗 (同时加载简历列表)
const openApplyModal = async () => {
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
    alert('无法加载简历列表，请检查网络')
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
    applyModal.hide()
    alert('🎉 投递成功！')
    router.push('/home')

  } catch (error) {
    alert('投递失败：' + (error.response?.data?.message || '您可能已经投递过该职位'))
  }
}

onMounted(() => {
  fetchJobDetail()
})
</script>