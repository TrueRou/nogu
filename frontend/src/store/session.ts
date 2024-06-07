import { client } from '@/requests';
import type { User } from '@/schemas/types';
import { defineStore } from 'pinia';

export const useSessionStore = defineStore('session', {
    state: () => ({
        user: null as User | null,
        isLoggedIn: false as boolean,
    }),

    actions: {
        async login(username: string, password: string) {
            const { data } = await client.POST('/auth/jwt/login', {
                body: {
                    username: username,
                    password: password
                }
            })
            if (data) localStorage.setItem('accessToken', data.access_token)
            return data != undefined
        },

        async register(username: string, email: string, country: string, password: string) {
            const { data } = await client.POST('/auth/register', {
                body: {
                    username: username,
                    email: email,
                    country: country,
                    password: password
                }
            })
            if (data) return await this.login(username, password)
            return false
        },

        logout() {
            localStorage.removeItem('accessToken');
            this.user = null;
            this.isLoggedIn = false;
        },

        async authorize() {
            const { data, error } = await client.GET('/users/me')
            this.user = data ? data : null
            this.isLoggedIn = error ? false : true
        }
    },
});