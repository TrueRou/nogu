import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import qs from 'qs'
import { useUIStore } from './user_interface'

const ui = useUIStore()

const API_URL = 'http://localhost:8000/api'

const axios_public = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    timeout: 5000,
});

axios_public.interceptors.response.use(function (response) {
    return response;
}, function (error) {
    if (error.response.status == 401) ui.showNotification('error', 'Unauthorized".')
    return Promise.reject(error);
});

export const useUserStore = defineStore('user_information', () => {
    const isLoggedIn = ref(false)
    const userInfo = ref({})

    function requests() {
        const token = localStorage.getItem('token');
        if (token == null) return axios_public;

        return axios.create({
            baseURL: API_URL,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                "Authorization": `Bearer ${token}`
            },
            timeout: 5000,
        });
    }

    async function login(username: string, password: string) {
        const response = await axios_public.post('/auth/jwt/login', qs.stringify({
            'username': username,
            'password': password
        }))
        if (response.status == 400) {
            ui.showNotification('error', 'Invalid credentials.')
        }
        if (response.status == 200) {
            localStorage.setItem('token', response.data['access_token'])
            isLoggedIn.value = true
        }
    }

    async function register(email: string, username: string, country: string, password: string) {
        const response = await axios_public.post('/auth/register', qs.stringify({
            'email': email,
            'username': username,
            'country': country,
            'password': password
        }))
        if (response.status == 400) {
            if (response.data['detail'] == 'REGISTER_USER_ALREADY_EXISTS') {
                ui.showNotification('error', 'User already exists.')
            }
        }
        if (response.status == 201) {
            await login(username, password)
            ui.showNotification('info', 'Successfully registered.')
        }
    }

    function logout() {
        localStorage.removeItem('token')
        isLoggedIn.value = false
        userInfo.value = {}
        ui.showNotification('info', 'Successfully logged out.')
    }
})
