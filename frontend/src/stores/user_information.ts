import { ref } from 'vue'
import { defineStore } from 'pinia'


export const useUserStore = defineStore('user_information', () => {
    const isLoggedIn = ref(false)
    const user = ref({})

    function login(email: string, password: string) {
        isLoggedIn.value = true
        user.value = {}
    }

    function register(email: string, password: string) {
        isLoggedIn.value = true
        user.value = {}
    }

    function logout() {
        isLoggedIn.value = false
        user.value = {}
    }
})
