<script setup lang="ts">
import Button from '@/components/Button.vue';
import Input from '@/components/Input.vue';
import { ButtonKinds, InputKinds } from '@/components/typedef';
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
    <div class="flex w-96" style="height: 30rem;">
        <div class="flex m-6 w-full h-full flex-col">
            <span class="flex font-bold text-2xl mb-4">Register</span>
            <form>
                <Input v-model="username" :kind="InputKinds.Dark" class="flex mt-2 mb-3" height="2.5rem" width="100%" placeholder="Username" />
                <Input v-model="email" :kind="InputKinds.Dark" class="flex mt-2 mb-3" height="2.5rem" width="100%" placeholder="Email" />
                <Input v-model="country" :kind="InputKinds.Dark" class="flex mt-2 mb-3" height="2.5rem" width="100%" placeholder="Country" />
                <Input v-model="password" type="password" :kind="InputKinds.Dark" class="flex mb-3" height="2.5rem" width="100%"
                    placeholder="Password" />
            </form>
            <Button class="flex mt-3" :kind="ButtonKinds.Primary" text="Register" width="100%" @click="handleRegister"></Button>
        </div>
    </div>
</template>