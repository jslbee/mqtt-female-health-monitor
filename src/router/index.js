import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import('../views/Login.vue')
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
    name: 'HealthRecords',
    component: () => import('../views/HealthRecords.vue')
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