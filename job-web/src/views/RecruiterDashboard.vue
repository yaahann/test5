<template>
  <div>
    <nav class="navbar navbar-dark bg-dark mb-0">
      <div class="container">
        <span class="navbar-brand">🏢 企业招聘管理后台</span>
        <button class="btn btn-outline-light btn-sm" @click="$router.push('/home')">返回首页</button>
      </div>
    </nav>

    <div class="d-flex" style="min-height: 100vh;">
      <div class="bg-light border-end p-3" style="width: 250px;">
        <div class="list-group list-group-flush">
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'profile' }" @click="currentTab = 'profile'">
            🏢 企业信息完善
          </button>
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'post' }" @click="currentTab = 'post'">
            ✍️ 发布新职位
          </button>
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'myjobs' }" @click="currentTab = 'myjobs'">
            📋 职位管理
          </button>
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'candidates' }" @click="currentTab = 'candidates'">
            👥 候选人处理
            <span v-if="applications.length > 0" class="badge bg-danger ms-2">{{ applications.length }}</span>
          </button>
          <button class="list-group-item list-group-item-action" :class="{ active: currentTab === 'recommend' }" @click="currentTab = 'recommend'">
            ✨ 发现牛人
          </button>
        </div>
      </div>

      <div class="flex-grow-1 p-4">

        <div v-if="currentTab === 'profile'">
          <h4>企业信息完善</h4>
          <hr>
          <form @submit.prevent="updateProfile" class="col-md-8">
            <div class="mb-3">
              <label class="form-label">企业名称 <span class="text-danger">*</span></label>
              <input type="text" class="form-control" v-model="profileForm.company_name" required placeholder="请输入公司全称">
            </div>

            <div class="row mb-3">
              <div class="col-md-6">
                <label class="form-label">所属行业</label>
                <input type="text" class="form-control" v-model="profileForm.industry" placeholder="例如：互联网/电子商务">
              </div>
              <div class="col-md-6">
                <label class="form-label">公司规模</label>
                <select class="form-select" v-model="profileForm.company_scale">
                  <option value="">请选择</option>
                  <option value="0-20人">0-20人</option>
                  <option value="20-99人">20-99人</option>
                  <option value="100-499人">100-499人</option>
                  <option value="500-999人">500-999人</option>
                  <option value="1000人以上">1000人以上</option>
                </select>
              </div>
            </div>

            <div class="mb-4">
              <label class="form-label">企业详细地址</label>
              <input type="text" class="form-control" v-model="profileForm.company_addr" placeholder="例如：上海市浦东新区xxx街道xxx号">
            </div>

            <div class="mb-4">
              <label class="form-label">公司简介</label>
              <textarea class="form-control" rows="4" v-model="profileForm.description" placeholder="请输入公司简介，向求职者展示企业的优势与特色..."></textarea>
            </div>

            <div class="alert mb-4" :class="auditStatus === 1 ? 'alert-success' : (auditStatus === 2 ? 'alert-danger' : 'alert-warning')">
              <strong>当前资质认证状态：</strong>
              {{ auditStatus === 1 ? '✅ 已通过认证' : (auditStatus === 2 ? '❌ 认证被拒绝，请重新上传资质' : '⏳ 待审核中') }}
            </div>

            <div class="mb-4">
               <label class="form-label">营业执照 / 认证文件</label>
               <input type="file" class="form-control" @change="handleLicenseChange">
               <div v-if="licenseUrl" class="mt-2 text-muted small">
                 📄 当前已上传：<a :href="licenseUrl" target="_blank">点击查看文件</a>
             </div>
            </div>

            <button type="submit" class="btn btn-primary">💾 保存修改</button>
          </form>
        </div>

        <div v-if="currentTab === 'post'">
          <h4>发布新职位</h4>
          <hr>
          <div v-if="auditStatus !== 1" class="alert alert-danger">
            ⚠️ 您的企业资质尚未通过审核，暂时无法发布职位。请先在【企业信息完善】中上传真实有效的认证文件并等待管理员审核。
          </div>
          <form @submit.prevent="createJob">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label>职位名称</label>
                <input type="text" class="form-control" v-model="jobForm.job_title" required>
              </div>
              <div class="col-md-3 mb-3">
                <label>城市</label>
                <input type="text" class="form-control" v-model="jobForm.city" required>
              </div>
              <div class="col-md-3 mb-3">
                <label>学历要求</label>
                <select class="form-select" v-model="jobForm.education_req">
                  <option>本科</option><option>硕士</option><option>大专</option><option>不限</option>
                </select>
              </div>
            </div>
            <div class="row mb-3">
              <div class="col-md-6">
                <label>经验要求</label>
                <select class="form-select" v-model="jobForm.exp_req">
                  <option>不限</option><option>1年以内</option><option>1-3年</option><option>3-5年</option><option>5年以上</option>
                </select>
              </div>
              <div class="col-md-6">
                <label>职位标签（用逗号分隔，如：Python,后端）</label>
                <input type="text" class="form-control" v-model="jobForm.job_tags" required>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label>薪资范围 (k)</label>
                <div class="input-group">
                  <input type="number" class="form-control" v-model="jobForm.salary_min" placeholder="Min">
                  <span class="input-group-text">-</span>
                  <input type="number" class="form-control" v-model="jobForm.salary_max" placeholder="Max">
                </div>
              </div>
              <div class="col-md-6 mb-3">
                <label>职位类型</label>
                 <select class="form-select" v-model="jobForm.job_type">
                  <option value="全职">全职</option><option value="实习">实习</option><option value="兼职">兼职</option>
                </select>
              </div>
            </div>
            <div class="mb-3">
              <label>职位描述</label>
              <textarea class="form-control" rows="5" v-model="jobForm.description" required></textarea>
            </div>
            <button class="btn btn-primary">🚀 立即发布</button>
          </form>
        </div>

        <div v-if="currentTab === 'myjobs'">
          <h4>职位管理</h4>
          <hr>
          <table class="table align-middle">
            <thead><tr><th>名称</th><th>发布时间</th><th>当前状态</th><th>操作</th></tr></thead>
            <tbody>
              <tr v-for="job in myJobs" :key="job.id">
                <td>{{ job.job_title }}</td>
                <td>{{ new Date(job.create_time).toLocaleDateString() }}</td>
                <td>
                  <span v-if="job.status === 0" class="badge bg-warning text-dark">⏳ 待审核</span>
                  <span v-else-if="job.status === 1" class="badge bg-success">✅ 招聘中</span>
                  <span v-else class="badge bg-secondary">⛔ 已下架/驳回</span>
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-primary me-2" @click="openEditModal(job)">
                    ✏️ 编辑
                  </button>
                  <button v-if="job.status === 1" class="btn btn-sm btn-outline-danger" @click="toggleJobStatus(job.id, 2)">
                    ⛔ 停止招聘
                  </button>
                  <button v-else-if="job.status === 2" class="btn btn-sm btn-outline-success" @click="toggleJobStatus(job.id, 0)">
                    🔄 重新提交审核
                  </button>
                  <span v-else-if="job.status === 0" class="text-muted small">
                    审核中不可操作
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="currentTab === 'recommend'">
          <h4>✨ 发现牛人 <span class="fs-6 text-muted fw-normal ms-2">AI 智能简历匹配</span></h4>
          <hr>

          <div class="card bg-light border-0 shadow-sm mb-4 p-3">
            <label class="form-label fw-bold text-dark">🎯 请选择您要为哪个岗位寻找候选人？</label>
            <select class="form-select form-select-lg" v-model="selectedJobId" @change="fetchCandidates">
              <option value="">-- 请下拉选择一个您正在招聘中的职位 --</option>
              <option v-for="job in activeJobs" :key="job.id" :value="job.id">
                {{ job.job_title }} ({{ job.city }}) - {{ job.salary_min }}k~{{ job.salary_max }}k
              </option>
            </select>
          </div>

          <div v-if="selectedJobId" class="row">
            <div class="col-md-6 mb-3" v-for="candidate in recommendedCandidates" :key="candidate.id">
              <div class="card shadow-sm h-100 border-0" style="transition: transform 0.2s;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-start mb-2">
                    <h5 class="fw-bold text-primary mb-0">
                      {{ candidate.name ? candidate.name[0] + '先生/女士' : '某求职者' }}
                      <small class="text-muted ms-1 fs-6">{{ candidate.gender || '' }}</small>
                    </h5>

                  </div>

                  <div class="mb-2">
                    <span class="badge bg-light text-dark border me-1">{{ candidate.education || '学历不限' }}</span>
                    <span class="badge bg-light text-dark border me-1">{{ candidate.major || '专业不限' }}</span>
                  </div>

                  <p class="mb-1 text-dark small fw-bold">期望：{{ candidate.exp_job || '未填' }} | {{ candidate.exp_city || '未填' }}</p>

                  <div class="bg-light p-2 rounded mt-2 mb-3 small" style="height: 60px; overflow: hidden;">
                    <span class="fw-bold text-secondary">核心技能：</span>
                    {{ candidate.skills || '未填写技能，算法根据其他维度推荐' }}
                  </div>
                  <button class="btn btn-outline-primary btn-sm w-100 mt-auto" @click="openInterviewModal(candidate.user_id)">🚀 邀请TA面试</button>
                </div>
              </div>
            </div>

            <div v-if="recommendedCandidates.length === 0" class="col-12 text-center py-5 text-muted">
              没有找到高匹配度的候选人，可能是目前人才库没有对口求职者。
            </div>
          </div>

          <div v-else class="text-center py-5 text-muted">
            <h1 class="display-4 mb-3">🔍</h1>
            <h5>请先在上方选择一个职位</h5>
            <p>将自动为您从全平台匹配最适合的牛人</p>
          </div>
        </div>

        <div v-if="currentTab === 'candidates'">
          <h4>收到的简历</h4>
          <hr>
          <div v-for="app in applications" :key="app.id" class="card mb-3">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <h5>{{ app.job_info.job_title }} <small class="text-muted">- 候选人ID: {{ app.resume }}</small></h5>
                <span class="badge" :class="getBadgeClass(app.status)">{{ getStatusText(app.status) }}</span>
              </div>
              <p class="text-muted small">投递时间：{{ new Date(app.apply_time).toLocaleString() }}</p>

             <div class="d-flex gap-2 align-items-center">
                <a :href="getResumeUrl(app.resume_file_url)" target="_blank" download class="btn btn-sm btn-outline-primary">
                  📄 下载简历
                </a>

                <template v-if="app.status === 0">
                  <button class="btn btn-sm btn-success me-2" @click="openInterviewModal(app.seeker_user_id, app.id)">邀请面试</button>
                  <button class="btn btn-sm btn-danger" @click="updateStatus(app.id, 4)">
                    ❌ 不合适
                  </button>
                </template>

                <template v-if="app.status === 2">
                  <button class="btn btn-sm btn-success" @click="updateStatus(app.id, 3)">
                    🎉 录用
                  </button>
                  <button class="btn btn-sm btn-danger" @click="updateStatus(app.id, 4)">
                    ❌ 不合适
                  </button>
                </template>

                <span v-if="app.status === 3 || app.status === 4" class="text-muted small ms-2">
                  🔒 已处理完结
                </span>
              </div>
            </div>
          </div>
          <p v-if="applications.length === 0" class="text-muted">暂无收到的投递。</p>
        </div>

      </div>
    </div>
  </div>
  <div class="modal fade" id="editJobModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">编辑职位</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <form @submit.prevent="submitEditJob">
            <div class="modal-body">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label>职位名称</label>
                  <input type="text" class="form-control" v-model="editJobForm.job_title" required>
                </div>
                <div class="col-md-3 mb-3">
                  <label>城市</label>
                  <input type="text" class="form-control" v-model="editJobForm.city" required>
                </div>
                <div class="col-md-3 mb-3">
                  <label>学历要求</label>
                  <select class="form-select" v-model="editJobForm.education_req">
                    <option>本科</option><option>硕士</option><option>大专</option><option>不限</option>
                  </select>
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <label>经验要求</label>
                  <select class="form-select" v-model="editJobForm.exp_req">
                    <option>不限</option><option>1年以内</option><option>1-3年</option><option>3-5年</option><option>5年以上</option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label>职位标签（用逗号分隔）</label>
                  <input type="text" class="form-control" v-model="editJobForm.job_tags" required>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label>薪资范围 (k)</label>
                  <div class="input-group">
                    <input type="number" class="form-control" v-model="editJobForm.salary_min">
                    <span class="input-group-text">-</span>
                    <input type="number" class="form-control" v-model="editJobForm.salary_max">
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label>职位类型</label>
                   <select class="form-select" v-model="editJobForm.job_type">
                    <option value="全职">全职</option><option value="实习">实习</option><option value="兼职">兼职</option>
                  </select>
                </div>
              </div>
              <div class="mb-3">
                <label>职位描述</label>
                <textarea class="form-control" rows="5" v-model="editJobForm.description" required></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
              <button type="submit" class="btn btn-primary">💾 保存修改</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  <div class="modal fade" id="interviewModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">发送面试邀请</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">面试时间</label>
              <input type="datetime-local" class="form-control" v-model="interviewForm.time">
            </div>
            <div class="mb-3">
              <label class="form-label">面试地点</label>
              <input type="text" class="form-control" v-model="interviewForm.location" placeholder="例如：某某大厦5楼会议室">
            </div>
            <div class="mb-3">
              <label class="form-label">联系人及电话</label>
              <input type="text" class="form-control" v-model="interviewForm.contact" placeholder="例如：王经理 138xxxx0000">
            </div>
            <div class="mb-3">
              <label class="form-label">附加说明 (可选)</label>
              <textarea class="form-control" v-model="interviewForm.note" rows="2" placeholder="例如：请携带纸质简历或作品集..."></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
            <button type="button" class="btn btn-primary" @click="sendInterviewInvite">🚀 发送邀请并更新状态</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted ,computed } from 'vue'
import { Modal } from 'bootstrap'
import axios from 'axios'

// 修改：默认显示"企业信息"页面
const currentTab = ref('profile')
const myJobs = ref([])
const applications = ref([])
// 从本地存储获取token（这里如果获取不到，要注意提示登录）
const token = localStorage.getItem('access_token') || localStorage.getItem('token')
const selectedJobId = ref('')
const recommendedCandidates = ref([])

// 新增：企业信息表单数据
const profileForm = reactive({
  company_name: '',
  industry: '',
  company_scale: '',
  company_addr: '',
  description: ''
})

const jobForm = reactive({
  job_title: '', city: '北京', salary_min: 10, salary_max: 20,
  education_req: '本科',exp_req: '不限',
  job_tags: '', job_type: '全职', description: ''
})

const auditStatus = ref(0)
const licenseUrl = ref('')
const licenseFile = ref(null)
// 2. 新增一个专门捕获文件的函数
const handleLicenseChange = (e) => {
  licenseFile.value = e.target.files[0]
  console.log("准备上传的资质文件:", licenseFile.value) // 你可以在F12控制台看到是否成功抓取到文件
}
// 新增：获取企业资料
const fetchProfile = async () => {
  if (!token) return;
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/recruiter/profile/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    // 赋值给表单
    profileForm.company_name = res.data.company_name || ''
    profileForm.industry = res.data.industry || ''
    profileForm.company_scale = res.data.company_scale || ''
    profileForm.company_addr = res.data.company_addr || ''
    profileForm.description = res.data.description || ''
    auditStatus.value = res.data.audit_status
    licenseUrl.value = res.data.license || ''
  } catch (error) {
    console.error('获取企业资料失败:', error)
  }
}

// 新增：更新企业资料
const updateProfile = async () => {
  try {
    // 因为有文件，必须用 FormData 而不能用普通 JSON 对象
    const formData = new FormData()
    formData.append('company_name', profileForm.company_name)
    formData.append('industry', profileForm.industry)
    formData.append('company_scale', profileForm.company_scale)
    formData.append('company_addr', profileForm.company_addr)

    if (licenseFile.value) {
      formData.append('license', licenseFile.value)
    }

    await axios.patch('http://127.0.0.1:8000/api/users/recruiter/profile/', formData, {
      headers: {
        'Authorization': `Bearer ${token}`
        // 让 axios 自己识别 FormData，浏览器会自动加上带 boundary 的 Content-Type！
      }
    })
    alert('✅ 企业信息保存成功！')
  } catch (error) {
    console.error('保存失败:', error)
    alert('保存失败，请检查网络或联系管理员')
  }
}

// 发布职位
const createJob = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/api/jobs/', jobForm,{
      headers: { 'Authorization': `Bearer ${token}` }
    })
    alert('发布成功！请等待管理员审核。')
    // 清空表单
    jobForm.job_title = ''
    jobForm.description = ''
  } catch (e) {
      console.dir(e);
      const errorMsg = e.response?.data?.detail || JSON.stringify(e.response?.data) || '发布失败';
      alert('发布失败: ' + errorMsg);
    }
}

// 获取职位
const fetchMyJobs = async () => {
  if (!token) return;
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/jobs/recruiter/my-jobs/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    myJobs.value = res.data
  } catch (error) {
    console.error('获取职位失败:', error)
    if (error.response && error.response.status === 401) {
      alert('登录已过期，请重新登录！')
    }
  }
}


// 1. 定义编辑表单的数据结构
const editJobForm = reactive({
  id: null,
  job_title: '', city: '', salary_min: 0, salary_max: 0,
  education_req: '', exp_req: '', job_tags: '',
  job_type: '', description: ''
})

let editModalInstance = null

// 2. 点击编辑按钮，打开弹窗并填充数据
const openEditModal = (job) => {
  // 把当前点击的 job 数据浅拷贝给编辑表单
  Object.assign(editJobForm, job)

  // 初始化并显示弹窗
  if (!editModalInstance) {
    editModalInstance = new Modal(document.getElementById('editJobModal'))
  }
  editModalInstance.show()
}

// 3. 提交修改请求到后端
const submitEditJob = async () => {
  try {
    // 调用后端的 JobDetailView 进行 PATCH 更新
    await axios.patch(`http://127.0.0.1:8000/api/jobs/${editJobForm.id}/`, editJobForm, {
      headers: { 'Authorization': `Bearer ${token}` }
    })

    alert('✅ 职位信息修改成功！')
    editModalInstance.hide() // 关闭弹窗
    fetchMyJobs() // 刷新列表，显示最新数据
  } catch (error) {
    console.error('修改失败:', error)
    alert('❌ 修改失败: ' + (error.response?.data?.detail || '请检查填写内容'))
  }
}


// --- 面试邀请逻辑 ---
const interviewForm = reactive({
  applicationId: null, // 如果是主动发现的牛人，这个值就是 null
  receiverId: null,
  time: '',
  location: '',
  contact: '',
  note: ''
})

let interviewModalInstance = null

//  1：把参数顺序换一下，并且允许 appId 为空
const openInterviewModal = (seekerUserId, appId = null) => {
  if (!seekerUserId) {
    alert("系统错误：无法获取求职者账号ID！")
    return
  }
  interviewForm.receiverId = seekerUserId
  interviewForm.applicationId = appId // 可能是 null

  if (!interviewModalInstance) {
    interviewModalInstance = new Modal(document.getElementById('interviewModal'))
  }
  interviewModalInstance.show()
}

// 2：发送消息后，判断有没有 appId，有才去更新状态
const sendInterviewInvite = async () => {
  if (!interviewForm.time || !interviewForm.location || !interviewForm.contact) {
    alert('请填写完整的面试时间、地点和联系人！')
    return
  }

  const messageContent = `【面试邀请】\n您好！我们认真看了您的简历，认为您非常符合我们的岗位要求，特邀请您参加面试。\n\n📅 面试时间：${interviewForm.time.replace('T', ' ')}\n📍 面试地点：${interviewForm.location}\n📞 联系人：${interviewForm.contact}\n📝 附加说明：${interviewForm.note || '无'}\n\n期待您的到来！`

  try {
    // 1. 发送私信 (所有人都要发)
    await axios.post('http://127.0.0.1:8000/api/users/messages/send/', {
      receiver_id: interviewForm.receiverId,
      content: messageContent
    }, { headers: { 'Authorization': `Bearer ${token}` } })

    // 2. 如果存在投递记录 ID，才去更新投递状态
    if (interviewForm.applicationId) {
       await updateStatus(interviewForm.applicationId, 2)
    }

    alert('✅ 面试邀请已发送！求职者会在消息中心收到通知。')
    interviewModalInstance.hide()
  } catch (error) {
    console.error(error)
    alert('发送失败，请检查网络面板。')
  }
}


// 计算属性：从 myJobs 列表里过滤出当前“招聘中”的职位供 HR 选择
const activeJobs = computed(() => {
  return myJobs.value.filter(job => job.status === 1)
})

// 根据选中的职位去请求推荐的牛人
const fetchCandidates = async () => {
  if (!selectedJobId.value) {
    recommendedCandidates.value = []
    return
  }

  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/recommendations/candidates/?job_id=${selectedJobId.value}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    recommendedCandidates.value = res.data
  } catch (error) {
    console.error('获取候选人失败:', error)
    alert('获取推荐失败，请确认职位状态是否正常')
  }
}

// 切换职位状态
const toggleJobStatus = async (jobId, newStatus) => {
  try {
    await axios.patch(`http://127.0.0.1:8000/api/jobs/${jobId}/status/`,
      { status: newStatus },
      { headers: { 'Authorization': `Bearer ${token}` } }
    )
    fetchMyJobs() // 刷新状态
  } catch (error) {
    alert('操作失败')
  }
}

// 获取简历
const fetchApplications = async () => {
  if (!token) return;
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/recruitment/recruiter/applications/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    applications.value = res.data
  } catch (error) {
    console.error('获取申请失败:', error)
  }
}

// 修改简历状态
const updateStatus = async (appId, newStatus) => {
  try {
    await axios.patch(`http://127.0.0.1:8000/api/recruitment/applications/${appId}/status/`,
      { status: newStatus },
      { headers: { 'Authorization': `Bearer ${token}` } }
    )
    alert('操作成功！')
    fetchApplications()
  } catch (e) {
    console.error(e)
    alert('操作失败: ' + (e.response?.data?.detail || '未知错误'))
  }
}

// 辅助：处理简历URL
const getResumeUrl = (path) => {
  if (!path) return '#'
  if (path.startsWith('http')) return path
  if (path.startsWith('/media/')) return `http://127.0.0.1:8000${path}`
  return `http://127.0.0.1:8000/media/${path}`
}

const getStatusText = (s) => {
  const map = {0: '未读', 1: '已读', 2: '面试邀请', 3: '录用', 4: '不合适'}
  return map[s] || s
}

const getBadgeClass = (s) => {
   const map = {0: 'bg-secondary', 2: 'bg-warning text-dark', 3: 'bg-success', 4: 'bg-danger'}
   return map[s] || 'bg-light text-dark'
}


onMounted(() => {
  // 新增：初始化时加载企业资料
  fetchProfile()
  fetchMyJobs()
  fetchApplications()
})
</script>