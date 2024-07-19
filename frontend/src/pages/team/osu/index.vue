<script setup lang="ts">
import Profile from './profile.vue';
import Sheet from './sheet.vue';
import { markRaw, ref } from 'vue';

const selectedComponent = ref(markRaw(Profile))
</script>
<template>
    <div class="flex flex-col-reverse md:flex-row w-full justify-start h-full">
        <div class="sticky bottom-1 pt-2 md:pt-0 md:top-12 w-full md:w-40 self-start">
            <div
                class="flex pt-4 pb-4 rounded-2xl md:flex-col h-12 md:h-full w-full bg-primary md:bg-neutral md:mt-6 md:justify-start content-center flex-wrap justify-center">
                <input v-model="selectedComponent" :value="markRaw(Profile)"
                    class="flex btn h-full w-32 md:h-6 md:w-full btn-ghost rounded-none normal-case" type="radio"
                    aria-label="Profile">
                <input v-model="selectedComponent" :value="markRaw(Sheet)"
                    class="flex btn h-full w-32 md:h-6 md:w-full btn-ghost rounded-none normal-case" type="radio"
                    aria-label="Sheet">
                <input v-model="selectedComponent" :value="null"
                    class="flex btn h-full w-32 md:h-6 md:w-full btn-ghost rounded-none normal-case" type="radio"
                    aria-label="Analysis">
                <input v-model="selectedComponent" :value="null"
                    class="flex btn h-full w-32 md:h-6 md:w-full btn-ghost rounded-none normal-case" type="radio"
                    aria-label="Member">
            </div>
        </div>
        <div class="flex w-full justify-center">
            <div class="flex md:w-11/12 w-full justify-center">
                <component :is="selectedComponent"></component>
            </div>
        </div>
    </div>
</template>

<style scoped>
@media (min-width: 768px) {
    .md\:h-90p {
        height: 89.5%;
    }

    .md\:w-40 {
        width: 10rem !important;
    }

    .md\:w-full {
        width: 100% !important;
    }

    .btn:is(input[type="radio"]:checked) {
        background-color: #5639AC !important;
        color: white !important;
    }
}


.w-90p {
    width: 97.5%;
}

.btn:is(input[type="radio"]:checked) {
    background-color: #E2E8F0;
    color: black;
}
</style>