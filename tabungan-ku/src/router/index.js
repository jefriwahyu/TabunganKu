import { createRouter, createWebHistory } from 'vue-router'
import SplashView from '../views/SplashView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'splash',
      component: SplashView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const user = localStorage.getItem('user')
  
  // If route requires auth and user is not logged in
  if (to.meta.requiresAuth && !user) {
    next('/login')
  }
  // If user is logged in and trying to access login page
  else if (to.name === 'login' && user) {
    next('/dashboard')
  }
  // Otherwise, proceed as normal
  else {
    next()
  }
})

export default router