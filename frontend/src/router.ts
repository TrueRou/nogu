import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: () => import('@/pages/index.vue'),
    },
    {
      path: '/showcase',
      name: 'showcase',
      component: () => import('@/pages/showcase/index.vue'),
    },
    {
      path: '/teams/:teamId',
      name: 'team',
      component: () => import('@/pages/team/index.vue'),
    }
  ]
})

export default router
