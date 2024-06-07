import { createRouter, createWebHistory } from 'vue-router'
import HomeIndex from './pages/index.vue'
import TeamIndex from './pages/team/index.vue'
import ShowcaseIndex from './pages/showcase/index.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: HomeIndex,
    },
    {
      path: '/showcase',
      name: 'showcase',
      component: ShowcaseIndex,
    },
    {
      path: '/teams/:teamId',
      name: 'team',
      component: TeamIndex,
    }
  ]
})

export default router
