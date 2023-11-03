<script setup lang="ts">
import { useUIStore } from '@/stores/user_interface';
import { ref } from 'vue';


const ui = useUIStore();
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
    <div class="flex flex-col ml-4 mr-4 mt-6 md:mt-0 justify-center">
        <div class="flex flex-col">
            <div class="flex">
                <div class="flex flex-col justify-center">
                    <img src="../../assets/title.svg" class="flex h-16 w-40" />
                    <h2 class="text-xl font-bold text-white">Focusing on collecting, sorting, analyzing scores</h2>
                    <div class="flex mt-2">
                        <button
                            class="bg-primary-purple w-20 h-9 hover:bg-primary-brighter-purple mr-2 text-white font-semibold">Try</button>
                        <button class="bg-whitesmoke w-20 h-9 hover:bg-white text-black font-semibold"
                            @click="ui.openDialog('Login')">Login</button>
                    </div>
                </div>
                <img class="hidden h-64 sm:flex md:ml-24" src="https://s2.loli.net/2023/11/01/mrZisGMnxqtC8Tv.png">
            </div>
            <div class="flex flex-wrap">
                <div v-for="feature in features" class="flex mt-10 w-80 md:w-60 md:mr-4">
                    <div class="flex flex-col">
                        <span class="flex font-bold text-xl mb-2">{{ feature.title }}</span>
                        <span>{{ feature.description }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
