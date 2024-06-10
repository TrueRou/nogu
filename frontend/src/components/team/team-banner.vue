<script setup lang="ts">
import type { TeamWithMembers } from '@/def/types';
import MemberGizmo from './member-gizmo.vue';

const props = defineProps<{
    team: TeamWithMembers
}>()
</script>

<template>
    <div class="flex w-full h-36 rounded-2xl"
        style="background: url('https://assets.ppy.sh/beatmaps/1990406/covers/cover@2x.jpg?1699284105') center center no-repeat; background-size: cover;">
        <div class="flex rounded-2xl w-full h-full flex-wrap backdrop-brightness-50 items-center justify-between"
            style="background-image: linear-gradient(to right, rgba(0, 0, 0, 0.5) 25%, rgba(255, 255, 255, 0) 75%);">
            <div class="flex flex-col ml-6">
                <span class="text-2xl font-bold shadow-md mb-1">{{ props.team.name }}</span>
                <MemberGizmo :member="team.user_links" />
            </div>
            <div class="flex flex-col">

            </div>
        </div>
    </div>
</template>