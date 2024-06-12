<script setup lang="ts">
import { client } from '@/utils/requests';
import router from '@/router';
import { useGlobal } from '@/store/global';
import { ref } from 'vue';

const username = ref('')
const password = ref('')
const global = useGlobal()

const handleLogin = async () => {
    const { data, error } = await client.POST('/auth/jwt/login', {
        body: {
            username: username.value,
            password: password.value
        },
        bodySerializer(body) {
            const form = new FormData();
            form.set('username', body.username);
            form.set('password', body.password);
            return form;
        },
    })
    if (!error && data) {
        localStorage.setItem('accessToken', data.access_token)
        global.closeDialog() // close the dialog
        router.go(0) // refresh the page
    }
}

</script>
<template>
    <div class="flex w-96" style="height: 22rem;">
        <div class="flex m-6 w-full h-full flex-col">
            <span class="flex font-bold text-2xl mb-4">Login</span>
            <form>
                <input v-model="username" class="input bg-neutral-content input-bordered w-full mt-2 mb-3"
                    placeholder="Username / Email" />
                <input v-model="password" type="password" class="input bg-neutral-content input-bordered w-full mb-3"
                    placeholder="Password" />
            </form>
            <button class="btn w-full btn-primary mt-2" @click="handleLogin">Login</button>
            <span class="flex mt-3 text-sm text-secondary"><a href="/">Forget password</a></span>
            <span class="flex mt-3 text-sm text-secondary"><a href="/">Without an account</a></span>
        </div>
    </div>
</template>