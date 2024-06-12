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
      component: () => import('@/pages/index.vue'),
      meta: { featured_game: '' },
    },
    {
      path: '/osu',
      component: () => import('@/pages/osu.vue'),
      meta: { featured_game: 'osu' },
    },
    {
      path: '/osu/discover',
      component: () => import('@/pages/discover/osu/index.vue'),
      meta: { featured_game: 'osu' },
    },
    {
      path: '/osu/teams/:teamId',
      component: () => import('@/pages/team/osu/index.vue'),
      meta: { featured_game: 'osu' },
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const session = useSession()
  const global = useGlobal()

  if (to.meta.requireAuth) {
    if (!session.isLoggedIn) await session.authorize() // wait for the session to be authorized
    if (!session.isLoggedIn) { // if the user is still not logged in
      global.showNotification("error", "Login is required to access that route.", "error.session.required")
      global.openDialog(markRaw(Login))
      return
    }
  }

  if (!session.isLoggedIn) session.authorize() // authorize the session in the background
  global.navMenu.featured_game = String(to.meta.featured_game)
  next()
})

export default router
