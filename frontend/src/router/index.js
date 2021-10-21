import Vue from 'vue'
import Router from 'vue-router'
import Register from '@/components/auth/Register'
import Login from '@/components/auth/Login'
import Main from '@/components/Main'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Register',
      component: Register
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/myprofile',
      name: 'Main',
      component: Main,
      children: [
        { path: '', component: () => import('@/components/My-profile.vue') },
        { path: '/perfomance-review', component: () => import('@/components/Perfomance-review.vue') },
        { path: '/me-estimate', component: () => import('@/components/Me-estimate.vue') },
        { path: '/me-manager', component: () => import('@/components/Me-manager.vue') },
        { path: '/self-review', component: () => import('@/components/Self-review.vue') },
        { path: '/one-to-one', component: () => import('@/components/One-to-one.vue') },
        { path: '/last-periods', component: () => import('@/components/Last-periods.vue') }
      ]
    }
  ]
})
