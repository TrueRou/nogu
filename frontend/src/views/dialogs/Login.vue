<script setup lang="ts">
import { useUserStore } from '@/stores/user_information';
import { ref } from 'vue';

const username = ref('')
const password = ref('')
const user = useUserStore()

const handleLogin = async () => {
    await user.login(username.value, password.value)
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