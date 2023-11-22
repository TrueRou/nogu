import { useUserStore } from '@/stores/user_information'
import { useUIStore } from '@/stores/user_interface'
import LeadinVue from '@/views/pages/Leadin.vue'
import TeamVue from '@/views/pages/Teams.vue'
import Login from '../views/dialogs/Login.vue';
import { markRaw } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'leadin',
      component: LeadinVue,
      meta: {
        requireAuth: false
      }
    },
    {
      path: '/team',
      name: 'team',
      component: TeamVue,
      meta: {
        requireAuth: true
      }
    },
  ]
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const ui = useUIStore()
  userStore.refreshInstance(localStorage.getItem('token'))

  if (!userStore.isLoggedIn && to.meta.requireAuth) {
    ui.cachedRoute = to.path
    ui.showNotification("error", "Login Required.")
    ui.openDialog(markRaw(Login))
    return
  }

  next()
})

export default router
