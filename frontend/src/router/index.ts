import LeadinVue from '@/views/pages/Leadin.vue'
import TeamVue from '@/views/pages/Teams.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'leadin',
      component: LeadinVue
    },
    {
      path: '/team',
      name: 'team',
      component: TeamVue
    },
  ]
})

export default router
