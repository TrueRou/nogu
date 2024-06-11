import { client } from '@/def/requests';
import type { User } from '@/def/types';
import router from '@/router';
import { defineStore } from 'pinia';

export const useSession = defineStore('session', {
    state: () => ({
        user: null as User | null,
        isLoggedIn: false as boolean,
    }),

    actions: {
        logout() {
            localStorage.removeItem('accessToken')
            this.user = null
            this.isLoggedIn = false
            router.go(0) // reload the page and reset the guards
        },

        async authorize() {
            if (localStorage.getItem('accessToken') === null) return
            try {
                const { data, error } = await client.GET('/users/me')
                this.user = data ? data : null
                this.isLoggedIn = error ? false : true
            } catch (error) {
                console.error("Failed to authorize user: " + error)
            }
        }
    },
});