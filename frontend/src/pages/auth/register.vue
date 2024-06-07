<script setup lang="ts">
import { client } from '@/requests';
import router from '@/routes';
import { useGlobal } from '@/store/global';
import { markRaw, ref } from 'vue';
import Login from './login.vue';

const email = ref('')
const username = ref('')
const country = ref('')
const password = ref('')
const global = useGlobal()

const handleLogin = async () => {
    const { data, error } = await client.POST('/auth/jwt/login', {
        body: {
            username: username.value,
            password: password.value
        }
    })
    if (!error && data) {
        localStorage.setItem('accessToken', data.access_token)
        global.closeDialog() // close the dialog
        router.go(0) // refresh the page
    }
}

const handleRegister = async () => {
    let { data, error } = await client.POST('/auth/register', {
        body: {
            username: username.value,
            email: email.value,
            country: country.value,
            password: password.value
        }
    })
    if (error || !data) await handleLogin()
}

</script>
<template>
    <div class="flex w-96" style="height: 28rem;">
        <div class="flex m-6 w-full h-full flex-col">
            <span class="flex font-bold text-2xl mb-4">Register</span>
            <form>
                <input v-model="username" class="input bg-neutral-content input-bordered mt-2 mb-2 w-full" placeholder="Username" />
                <input v-model="email" class="input bg-neutral-content input-bordered mt-2 mb-2 w-full" placeholder="Email" />
                <input v-model="country" class="input bg-neutral-content input-bordered mt-2 mb-2 w-full" placeholder="Country" />
                <input v-model="password" type="password" class="input bg-neutral-content input-bordered mt-2 mb-2 w-full" placeholder="Password" />
            </form>
            <button class="btn btn-primary mt-3 w-full" @click="handleRegister">Register</button>
            <span class="flex mt-3 text-sm text-secondary"><a href="/" @click="global.openDialog(markRaw(Login))">Already have an account</a></span>
        </div>
    </div>
</template>