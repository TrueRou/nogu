<script setup lang="ts">
import type { Team } from '@/schemas/types';
import MemberGizmo from './member-gizmo.vue';

const props = defineProps<{
    team: Team
}>()
</script>

<template>
    <div class="flex flex-col w-full h-full flex-wrap backdrop-brightness-50 rounded-2xl justify-center"
        style="background-image: linear-gradient(to right, rgba(0, 0, 0, 0.5) 25%, rgba(255, 255, 255, 0) 75%);">
        <div class="flex">
            <div class="flex flex-col ml-10">
                <span class="text-2xl font-bold shadow-md">{{ props.team.name }}</span>
                <span class="text-sm mont">Stage on {{ props.team.active_stage.name }}</span>
            </div>
        </div>
        <MemberGizmo :member="team.member" />
    </div>
</template>