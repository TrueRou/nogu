<script setup lang="ts">
import { type ITeam } from '@/objects/team'
import MemberSection from '@/views/widgets/MemberSection.vue';
const props = defineProps<{
    team: ITeam
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
        <MemberSection :member="team.member" />
    </div>
</template>