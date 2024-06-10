import { createRouter, createWebHistory } from 'vue-router'
import { useSession } from './store/session'
import { useGlobal } from './store/global'
import Login from './pages/auth/login.vue'
import { markRaw } from 'vue'

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

router.beforeEach(async (to, from, next) => {
  const session = useSession()
  const global = useGlobal()

  if (!session.isLoggedIn) await session.authorize()

  if (!session.isLoggedIn && to.meta.requireAuth) {
    global.cachedRoute = to.path
    global.showNotification("error", "Login is required to access that route.", "error.session.required")
    global.openDialog(markRaw(Login))
    return
  }

  next()
})

export default router
