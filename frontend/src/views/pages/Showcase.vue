<script setup lang="ts">
import Teams from '@/views/showcase/Teams.vue';
import Users from '@/views/showcase/Users.vue';
import Stages from '@/views/showcase/Stages.vue';
import Beatmaps from '@/views/showcase/Beatmaps.vue';
import { ref, markRaw } from 'vue';

const selectedComponent = ref(markRaw(Teams))
</script>
<template>
    <div class="flex w-full flex-col flex-panel">
        <div class="flex w-full flex-col">
            <div class="flex mt-2">
                <div class="flex font-bold text-md pt-1 mr-3">General:</div>
                <input v-model="selectedComponent" :value="markRaw(Teams)" type="radio"
                    class="btn btn-sm btn-accent btn-ghost mr-1" aria-label="Teams" />
                <input v-model="selectedComponent" :value="markRaw(Users)" type="radio"
                    class="btn btn-sm btn-accent btn-ghost mr-1" aria-label="Users" />
                <input v-model="selectedComponent" :value="markRaw(Stages)" type="radio"
                    class="btn btn-sm btn-accent btn-ghost mr-1" aria-label="Stages" />
                <input v-model="selectedComponent" :value="markRaw(Beatmaps)" type="radio"
                    class="btn btn-sm btn-accent btn-ghost mr-1" aria-label="Beatmaps" />
            </div>
        </div>
        <component :is="selectedComponent"></component>
    </div>
</template>