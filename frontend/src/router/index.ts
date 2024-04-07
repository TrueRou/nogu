import { useUserStore } from '@/stores/user_information'
import { useUIStore } from '@/stores/user_interface'
import Index from '@/views/pages/Index.vue'
import Showcase from '@/views/pages/Showcase.vue'
import Login from '@/views/dialogs/Login.vue';
import Team from '@/views/pages/Team.vue';
import { markRaw } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: Index,
      meta: {
        requireAuth: false
      }
    },
    {
      path: '/showcase',
      name: 'showcase',
      component: Showcase,
      meta: {
        requireAuth: false
      }
    },
    {
      path: '/teams/:teamId',
      name: 'team',
      component: Team,
      meta: {
        requireAuth: false
      }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  const ui = useUIStore()
  await userStore.refreshInstance(localStorage.getItem('token'))

  if (!userStore.isLoggedIn && to.meta.requireAuth) {
    ui.cachedRoute = to.path
    ui.showNotification("error", "Login Required.")
    ui.openDialog(markRaw(Login))
    return
  }

  next()
})

export default router
