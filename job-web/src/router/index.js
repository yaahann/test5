import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import JobDetailView from '../views/JobDetailView.vue'
import RegisterView from '../views/RegisterView.vue'
import SeekerDashboard from '../views/SeekerDashboard.vue'
import RecruiterDashboard from '../views/RecruiterDashboard.vue'
import JobListView from '../views/JobListView.vue'
import CompanyListView from '../views/CompanyListView.vue'
import CompanyDetailView from '../views/CompanyDetailView.vue'
import NewsView from '../views/NewsView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    // 2. 添加首页路由
    {
      path: '/home',
      name: 'home',
      component: HomeView
    },

    {
      path: '/jobs/:id',
      name: 'job-detail',
      component: JobDetailView
    },

    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },

    {
      path: '/seeker/dashboard',
      name: 'seeker-dashboard',
      component: SeekerDashboard
    },

    {
    path: '/recruiter/dashboard',
    name: 'recruiter-dashboard',
    component: RecruiterDashboard
    },

    { path: '/jobs', name: 'job-list', component: JobListView },
    { path: '/jobs/:id', name: 'job-detail', component: JobDetailView },

    { path: '/companies', name: 'company-list', component: CompanyListView },
    { path: '/companies/:id', name: 'company-detail', component: CompanyDetailView },

    { path: '/news', name: 'news', component: NewsView },

    {path: '/admin/dashboard', name: 'admin-dashboard', component: AdminDashboard},
    {path: '/news/:id', name: 'NewsDetail', component: () => import('../views/NewsDetailView.vue')
  },

  ]
})

export default router