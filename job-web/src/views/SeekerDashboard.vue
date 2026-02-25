<template>
  <div>
    <nav class="navbar navbar-dark bg-primary mb-0">
      <div class="container">
        <span class="navbar-brand">个人中心</span>
        <button class="btn btn-outline-light btn-sm" @click="$router.push('/home')">返回首页</button>
      </div>
    </nav>

    <div class="d-flex" style="min-height: 100vh;">
      <div class="bg-light border-end p-3" style="width: 250px;">
        <div class="list-group list-group-flush">
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'profile' }" @click="currentTab = 'profile'">
            👤 个人资料
          </button>
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'resume' }" @click="currentTab = 'resume'">
            📄 简历管理
          </button>
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'applications' }" @click="currentTab = 'applications'">
            📫 投递记录
          </button>
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'collection' }" @click="currentTab = 'collection'">
            ⭐ 我的收藏
          </button>
        </div>
      </div>

      <div class="flex-grow-1 p-4">

        <div v-if="currentTab === 'profile'">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h4>编辑个人信息</h4>
            <button class="btn btn-primary" @click="updateProfile">💾 保存修改</button>
          </div>
          <hr>

          <form @submit.prevent="updateProfile">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">真实姓名</label>
                <input type="text" class="form-control" v-model="profileForm.name">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">性别</label>
                <select class="form-select" v-model="profileForm.gender">
                  <option value="男">男</option>
                  <option value="女">女</option>
                </select>
              </div>

              <div class="col-md-6 mb-3">
                <label class="form-label">最高学历</label>
                <select class="form-select" v-model="profileForm.education">
                  <option value="本科">本科</option>
                  <option value="硕士">硕士</option>
                  <option value="博士">博士</option>
                  <option value="大专">大专</option>
                </select>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">专业</label>
                <input type="text" class="form-control" v-model="profileForm.major" placeholder="例如：计算机科学">
              </div>

              <div class="col-md-6 mb-3">
                <label class="form-label">出生日期</label>
                <input type="date" class="form-control" v-model="profileForm.birth_date">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">求职状态</label>
                 <select class="form-select" v-model="profileForm.job_status">
                  <option value="待业">待业</option>
                  <option value="在职">在职</option>
                 
                </select>
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label">技能标签 (用逗号分隔)</label>
              <input type="text" class="form-control" v-model="profileForm.skills" placeholder="例如：Python, Vue, MySQL">
            </div>

            <div class="mb-3">
              <label class="form-label">工作/实习经历</label>
              <textarea class="form-control" rows="4" v-model="profileForm.experience" placeholder="请详细描述您的工作经历..."></textarea>
            </div>

          </form>
        </div>

        <div v-if="currentTab === 'resume'">
          <h4>我的简历库</h4>
          <hr>
          <div class="row">
            <div class="col-md-6 mb-3" v-for="resume in myResumes" :key="resume.id">
              <div class="card h-100">
                <div class="card-body">
                  <h5 class="card-title">{{ resume.resume_title }}</h5>
                  <p class="text-muted small">上传时间：{{ new Date(resume.create_time).toLocaleString() }}</p>
                  <div class="d-flex justify-content-between mt-3">
                    <a :href="resume.resume_file" target="_blank" class="btn btn-sm btn-outline-primary">👁️ 查看</a>
                    <button class="btn btn-sm btn-outline-danger" @click="deleteResume(resume.id)">🗑️ 删除</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="myResumes.length === 0" class="alert alert-warning">您还没有上传任何简历。</div>
          <div class="card p-4 mt-4 bg-light">
            <h5>📤 上传新简历</h5>
            <div class="mb-3">
              <label class="form-label">简历标题</label>
              <input type="text" class="form-control" v-model="resumeForm.title">
            </div>
            <div class="mb-3">
              <input type="file" class="form-control" @change="handleFileChange">
            </div>
            <button class="btn btn-success" @click="uploadResume">确认上传</button>
          </div>
        </div>

        <div v-if="currentTab === 'applications'">
          <h4>我的投递记录</h4>
          <hr>
          <table class="table table-hover">
            <thead>
              <tr><th>职位</th><th>公司</th><th>状态</th></tr>
            </thead>
            <tbody>
              <tr v-for="app in applications" :key="app.id">
                <td>{{ app.job_info.job_title }}</td>
                <td>{{ app.job_info.company_name }}</td>
                <td><span class="badge" :class="getStatusBadge(app.status)">{{ getStatusText(app.status) }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="currentTab === 'collection'">
          <h4>我的收藏</h4>
          <hr>
          <div class="row">
            <div class="col-md-6 mb-3" v-for="item in myCollections" :key="item.id">
              <div class="card shadow-sm h-100">
                <div class="card-body">
                  <h5 class="text-primary fw-bold">{{ item.job_info.job_title }}</h5>
                  <p class="text-danger fw-bold mb-1">{{ item.job_info.salary_min }}k - {{ item.job_info.salary_max }}k</p>
                  <p class="text-muted small mb-3">🏢 {{ item.job_info.company_name }} | 📍 {{ item.job_info.city }}</p>
                  <div class="d-flex justify-content-between">
                    <button class="btn btn-sm btn-outline-primary w-50 me-2" @click="$router.push(`/jobs/${item.job_info.id}`)">查看详情</button>
                    <button class="btn btn-sm btn-outline-danger w-50" @click="removeCollection(item.job)">取消收藏</button>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="myCollections.length === 0" class="col-12 text-center text-muted py-5">
              您还没有收藏过任何职位哦。
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'

const currentTab = ref('profile')
const myResumes = ref([])
const applications = ref([])
const token = localStorage.getItem('access_token')

// 1. 初始化表单数据 (包含所有后端字段)
const profileForm = reactive({
  name: '',
  gender: '男',
  education: '本科',
  major: '',           // 新增
  skills: '',          // 新增
  birth_date: '',      // 新增
  experience: '', // 新增
  job_status: '待业'        // 新增
})

const resumeForm = reactive({ title: '', file: null })

// 获取个人资料
const fetchProfile = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/seeker/profile/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    // 自动填充数据
    Object.assign(profileForm, res.data)
  } catch (e) { console.error(e) }
}

// 更新个人资料
// 修改 src/views/SeekerDashboard.vue

const updateProfile = async () => {
  try {
    // 注意：建议把 put 改为 patch (下面会解释为什么)
    await axios.patch('http://127.0.0.1:8000/api/users/seeker/profile/', profileForm, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    alert('个人资料保存成功！')
  } catch (error) {
    console.error('保存报错详情:', error) // 在控制台打印详细信息

    // 如果后端返回了具体的字段错误 (400错误)
    if (error.response && error.response.data) {
      // 把后端返回的错误信息（JSON）转成字符串弹窗显示出来
      alert('保存失败：' + JSON.stringify(error.response.data))
    } else {
      alert('保存失败，请检查网络或后端服务')
    }
  }
}

// 获取简历
const fetchResumes = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/recruitment/resumes/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    myResumes.value = res.data
  } catch (e) { console.error(e) }
}

// 删除简历
const deleteResume = async (id) => {
  if(!confirm('确定删除?')) return
  try {
    await axios.delete(`http://127.0.0.1:8000/api/recruitment/resumes/${id}/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    fetchResumes()
  } catch(e) { alert('删除失败') }
}

// 上传简历
const handleFileChange = (e) => resumeForm.file = e.target.files[0]
const uploadResume = async () => {
  if (!resumeForm.file || !resumeForm.title) return alert('请填写完整')
  const formData = new FormData()
  formData.append('resume_title', resumeForm.title)
  formData.append('resume_file', resumeForm.file)
  try {
    await axios.post('http://127.0.0.1:8000/api/recruitment/resumes/', formData, {
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
    })
    alert('上传成功')
    resumeForm.title = ''
    fetchResumes()
  } catch(e) { alert('上传失败') }
}

// 获取投递记录
const fetchApplications = async () => {
  const res = await axios.get('http://127.0.0.1:8000/api/recruitment/applications/', {
      headers: { 'Authorization': `Bearer ${token}` }
  })
  applications.value = res.data
}

// 状态文字转换
const getStatusText = (status) => {
  const map = {
    0: '已投递',
    1: 'HR已阅',
    2: '面试邀请',
    3: '录用',
    4: '不合适'
  }
  return map[status] || '未知状态'
}

// 状态颜色转换 (让不同状态显示不同颜色)
const getStatusBadge = (status) => {
  const map = {
    0: 'bg-secondary', // 灰色
    1: 'bg-info text-dark',      // 浅蓝
    2: 'bg-warning text-dark',   // 黄色 (面试)
    3: 'bg-success',   // 绿色 (录用)
    4: 'bg-danger'     // 红色 (不合适)
  }
  return map[status] || 'bg-light text-dark'
}

// 在getStatusText定义后添加
defineExpose({
  getStatusText,
  getStatusBadge
})

// 新增响应式变量
const myCollections = ref([])
// 获取收藏列表
const fetchCollections = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/jobs/collection/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    myCollections.value = res.data
  } catch (error) { console.error('获取收藏失败:', error) }
}

// 在列表页快速取消收藏
const removeCollection = async (jobId) => {
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/jobs/collection/', { job: jobId }, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    // 根据后端返回的状态提示
    alert(res.data.message)
    fetchCollections() // 刷新列表
  } catch (error) {
    // 区分不同错误类型提示
    if (error.response) {
      if (error.response.status === 403) {
        alert('操作失败：' + error.response.data.detail) // 提示“只有求职者可以收藏”
      } else if (error.response.status === 400) {
        alert('操作失败：缺少职位参数')
      } else if (error.response.status === 404) {
        alert('操作失败：该职位不存在')
      } else {
        alert('操作失败：' + (error.response.data.detail || '服务器错误'))
      }
    } else {
      alert('操作失败：网络异常')
    }
  }
}

onMounted(() => {
  fetchProfile()
  fetchResumes()
  fetchApplications()
  fetchCollections()
})
</script>