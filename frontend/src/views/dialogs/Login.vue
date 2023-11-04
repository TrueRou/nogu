<script setup lang="ts">
import Button from '@/components/Button.vue';
import Input from '@/components/Input.vue';
import { ButtonKinds, InputKinds } from '@/components/typedef';


</script>
<template>
    <div class="flex w-96" style="height: 20rem;">
        <div class="flex m-6 w-full h-full flex-col">
            <span class="flex font-bold text-2xl mb-4">Login</span>
            <form>
                <Input :kind="InputKinds.Dark" class="flex mt-2 mb-3" height="2.5rem" width="100%"
                    placeholder="Username / Email" />
                <Input type="password" :kind="InputKinds.Dark" class="flex mb-3" height="2.5rem" width="100%"
                    placeholder="Password" />
            </form>
            <Button class="flex mt-3" :kind="ButtonKinds.Primary" text="Login" width="100%"></Button>
            <span class="flex mt-3 text-sm text-primary-pink"><a href="/">Forget password</a></span>
            <span class="flex mt-3 text-sm text-primary-pink"><a href="/">Without an account</a></span>
        </div>
    </div>
</template>