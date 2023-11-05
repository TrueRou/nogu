<script setup lang="ts">
import { useUserStore } from '@/stores/user_information';
import { ref } from 'vue';

const email = ref('')
const username = ref('')
const country = ref('')
const password = ref('')

const user = useUserStore()

const handleRegister = async () => {
    await user.register(email.value, username.value, country.value, password.value)
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
            <span class="flex mt-3 text-sm text-secondary"><a href="/">Already have an account</a></span>
        </div>
    </div>
</template>