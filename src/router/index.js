import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: Login
  },
  {
    path: '/metrics',
    name: 'HealthMetrics',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/prediction',
    name: 'Prediction',
    component: () => import('../views/Prediction.vue')
  },
  {
    path: '/messages',
    name: 'Messages',
    component: () => import('../views/Messages.vue')
  },
  {
    path: '/records',
    name: 'TeamMembers',
    component: () => import('../views/TeamMembers.vue')
  },
  {
    path: '/heart-rate',
    name: 'HeartRate',
    component: () => import('../views/HeartRate.vue')
  },
  {
    path: '/menstrual',
    name: 'Menstrual',
    component: () => import('../views/Menstrual.vue')
  },
  {
    path: '/temperature',
    name: 'Temperature',
    component: () => import('../views/Temperature.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 登录守卫
router.beforeEach((to, from, next) => {
  if (to.path !== '/' && !localStorage.getItem('isLoggedIn')) {
    next('/')
  } else {
    next()
  }
})

export default router 