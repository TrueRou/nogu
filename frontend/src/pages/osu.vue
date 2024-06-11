<script setup lang="ts">
import Login from '@/pages/auth/login.vue';
import Register from '@/pages/auth/register.vue';
import { useGlobal } from '@/store/global';
import { useSession } from '@/store/session';
import { markRaw, ref } from 'vue';

const global = useGlobal();
const session = useSession();
const features = ref(
    [
        {
            title: 'Collecting',
            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore'
        },
        {
            title: 'Sorting',
            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore'
        },
        {
            title: 'Analyzing',
            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore'
        }
    ]);
</script>

<template>
    <div class="flex flex-col justify-center content-center flex-wrap">
        <div class="flex">
            <div class="flex flex-col justify-center">
                <span class="text-5xl font-extrabold bg-clip-text text-transparent"
                    style="background-image: linear-gradient(to top,#F093FB, #F5576C);">NOGU</span>
                <h2 class="text-xl font-bold ">Focusing on collecting, sorting, analyzing scores</h2>
                <div class="flex mt-2">
                    <template v-if="!session.isLoggedIn">
                        <button class="btn btn-primary mr-2 font-bold"
                            @click="global.openDialog(markRaw(Register));">Register</button>
                        <button class="btn btn-accent mr-2 font-bold"
                            @click="global.openDialog(markRaw(Login));">Login</button>
                    </template>
                    <template v-else>
                        <button class="btn btn-primary mr-2 font-bold"
                            @click="global.openDialog(markRaw(Login));">Continue</button>
                    </template>
                </div>
            </div>
            <img class="hidden h-64 sm:flex md:ml-24" src="https://s2.loli.net/2023/11/01/mrZisGMnxqtC8Tv.png">
        </div>
        <div class="flex flex-wrap">
            <div v-for="feature in features" class="flex mt-10 w-80 md:w-60 md:mr-4">
                <div class="flex flex-col">
                    <span class="flex font-bold text-xl mb-2">{{ feature.title }}</span>
                    <span class="jetbrains-mono text-sm">{{ feature.description }}</span>
                </div>
            </div>
        </div>
    </div>
</template>
