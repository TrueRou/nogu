import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import qs from 'qs'
import { useUIStore } from './user_interface'

const API_URL = 'http://localhost:8000/'

const axiosGenerator = (useJson: boolean = true, token: string | null = null) => {
    const authorization = token == null ? {} : {Authorization: `Bearer ${token}`}
    const headers = {
        'Content-Type': useJson ? 'application/json' : 'application/x-www-form-urlencoded',
        Accept: 'application/json',
        ...authorization
    }

    return axios.create({
        baseURL: API_URL,
        headers: headers,
        timeout: 5000,
    });
}

let axiosInstance = axiosGenerator(true, null)

export const useUserStore = defineStore('user_information', () => {
    const ui = useUIStore()

    const isLoggedIn = ref(false)
    const userInfo = ref({})

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
        try {
            const response = await axiosGenerator(false, null).post('/auth/jwt/login', qs.stringify({
                'username': username,
                'password': password
            }))
            if (!mute) {
                ui.showNotification('info', 'Successfully logged in.')
                ui.closeDialog()
            }
            await refreshInstance(response.data['access_token'])
        } catch (exception: any) {
            ui.showNotification('error', 'Invalid credentials.')
        }
    }

    async function register(email: string, username: string, country: string, password: string, mute: boolean = false) {
        try {
            await axiosGenerator(true, null).post('/auth/register', {
                'email': email,
                'username': username,
                'country': country,
                'password': password
            })
            await login(email, password, true)
            if (!mute) {
                ui.showNotification('info', 'Successfully registered.')
                ui.closeDialog()
            }
        } catch (exception: any) {
            ui.showNotification('error', 'Bad requests.')
        }
    }

    function logout() {
        refreshInstance()
        ui.showNotification('info', 'Successfully logged out.')
    }

    return { isLoggedIn, userInfo, login, register, logout, requests }
})
