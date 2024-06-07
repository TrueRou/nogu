<script setup lang="ts">
import Profile from './profile.vue';
import { markRaw, ref } from 'vue';

const selectedComponent = ref(markRaw(Profile))
</script>
<template>
    <div class="flex flex-col-reverse w-full justify-start md:flex-row md:mt-1 md:mb-1 h-full">
        <div class="flex md:float-left md:h-full h-16 w-full md:w-40 rounded-2xl bg-neutral mr-10 mb-2"
            style="visibility: hidden;">
            this is fake which is used to make the room for the right side. so dirty i know.
        </div>
        <div
            class="flex md:float-left md:h-90p h-16 w-full md:w-40 bottom-2 left-2 rounded-2xl fixed bg-primary md:bg-neutral w-90p">
            <div class="flex md:flex-col w-full md:mt-6 md:justify-start content-center flex-wrap justify-center">
                <input v-model="selectedComponent" :value="markRaw(Profile)"
                    class="flex btn h-full w-32 md:h-6 md:w-full btn-ghost rounded-none normal-case" type="radio"
                    aria-label="Profile">
                <input v-model="selectedComponent" :value="null"
                    class="flex btn h-full w-32 md:h-6 md:w-full btn-ghost rounded-none normal-case" type="radio"
                    aria-label="Analysis">
                <input v-model="selectedComponent" :value="2"
                    class="flex btn h-full w-32 md:h-6 md:w-full btn-ghost rounded-none normal-case" type="radio"
                    aria-label="Member">
            </div>

        </div>

        <div class="flex w-full justify-center">
            <component :is="selectedComponent"></component>
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