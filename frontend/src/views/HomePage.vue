<template>
    <div class="flex flex-col">
        <div class="flex">
            <div class="flex flex-col justify-center">
                <img src="../assets/title.svg" class="flex h-16 w-40" />
                <h2 class="text-xl font-bold text-white">Focusing on collecting, sorting, analyzing scores</h2>
                <div class="flex mt-2">
                    <button class="flex bg-primary-purple w-20 h-9 hover:bg-primary-brighter-purple mr-2"></button>
                    <button class="flex bg-whitesmoke w-20 h-9 hover:bg-white"></button>
                </div>
            </div>
            <img class="hidden h-64 sm:flex md:ml-24" src="https://s2.loli.net/2023/11/01/mrZisGMnxqtC8Tv.png">
        </div>
        <div class="flex">
            some text
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const title = ref('Welcome to my page!');
const message = ref('This is a basic Vue composition API page.');

</script>
