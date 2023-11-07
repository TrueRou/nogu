import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios, { type AxiosResponse } from 'axios'
import qs from 'qs'
import { useUIStore } from './user_interface'
import type { IToken, IUserBase } from '@/objects/user'
import type { IExceptionNode } from '@/objects/object'

const API_URL = 'http://localhost:8000/'

export const useUserStore = defineStore('user_information', () => {
    const ui = useUIStore()

    const isLoggedIn = ref(false)
    const userInfo = ref({})

    const axiosGenerator = (useJson: boolean = true, token: string | null = null) => {
        const authorization = token == null ? {} : { Authorization: `Bearer ${token}` }
        const headers = {
            'Content-Type': useJson ? 'application/json' : 'application/x-www-form-urlencoded',
            Accept: 'application/json',
            ...authorization
        }

        const instance = axios.create({
            baseURL: API_URL,
            headers: headers,
            timeout: 5000,
        });

        instance.interceptors.response.use(
            (response: AxiosResponse) => {
                const { data } = response
                return data
            },
            (error) => {
                const exception: IExceptionNode = error.response.data
                ui.showException(exception)
                return Promise.resolve(null)
            }
        )

        return instance
    }

    let axiosInstance = axiosGenerator(true, null)

    function requests() {
        return axiosInstance
    }

    async function refreshInstance(token: string | null = null) {
        if (token == '') token = null
        if (token == null) {
            isLoggedIn.value = false
            userInfo.value = {}
            localStorage.removeItem('token')
        }
        axiosInstance = axiosGenerator(true, token)
        const response = await axiosInstance.get('/users/me')
        if (response.status == 200) {
            localStorage.setItem('token', response.data['access_token'])
            isLoggedIn.value = true
            userInfo.value = response.data
        }
    }

    async function login(username: string, password: string, mute: boolean = false) {
        const token: IToken = await axiosGenerator(false, null).post('/auth/jwt/login', qs.stringify({
            'username': username,
            'password': password
        }))

        if (token != null) {
            if (!mute) {
                ui.showNotification('info', 'Successfully logged in.')
                ui.closeDialog()
            }
            await refreshInstance(token.access_token)
        }
    }

    async function register(email: string, username: string, country: string, password: string, mute: boolean = false) {

        const user: IUserBase = await axiosGenerator(true, null).post('/auth/register', {
            'email': email,
            'username': username,
            'country': country,
            'password': password
        })
        if (user != null) {
            await login(email, password, true)
            if (!mute) {
                ui.showNotification('info', 'Successfully registered.')
                ui.closeDialog()
            }
        }
    }

    function logout() {
        refreshInstance()
        ui.showNotification('info', 'Successfully logged out.')
    }

    return { isLoggedIn, userInfo, login, register, logout, requests }
})
