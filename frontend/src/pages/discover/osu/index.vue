<script setup lang="ts">
import { ref, markRaw } from 'vue';
import Teams from './teams.vue';
import Users from './users.vue';
import Playlsts from './playlists.vue';

const selectedComponent = ref(markRaw(Playlsts))
</script>
<template>
    <div class="flex w-full flex-col flex-panel">
        <div class="flex w-full flex-col">
            <div class="flex mt-2">
                <div class="flex font-bold text-md pt-1 mr-3">General:</div>
                <input v-model="selectedComponent" :value="markRaw(Playlsts)" type="radio"
                    class="btn btn-sm btn-accent btn-ghost mr-1" aria-label="Playlists" />
                <input v-model="selectedComponent" :value="markRaw(Teams)" type="radio"
                    class="btn btn-sm btn-accent btn-ghost mr-1" aria-label="Teams" />
                <input v-model="selectedComponent" :value="markRaw(Users)" type="radio"
                    class="btn btn-sm btn-accent btn-ghost mr-1" aria-label="Users" />
            </div>
        </div>
        <component class="pl-1 pr-1" :is="selectedComponent"></component>
    </div>
</template>