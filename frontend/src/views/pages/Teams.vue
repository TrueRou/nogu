<script setup lang="ts">
import { reactive, ref, watch } from 'vue';
import { Team, type ITeam, type ITeamParams, type ITeamMember } from '@/objects/team';
import MemberShowcase from '../widgets/MemberShowcase.vue';

const statelessTeam = new Team() // Create stateless instance for axios lifetime
const teams = ref<ITeam[]>([])
const teamParams = reactive({
    privacy_limit: 3,
    active_only: false,
} as ITeamParams)

watch([teamParams], async () => teams.value = await statelessTeam.fetchAll(teamParams), { immediate: true })

</script>

<template>
    <div class="flex w-full flex-col flex-panel">
        <div class="flex flex-col">
            <span class="text-3xl font-extrabold md:h-10 bg-clip-text text-transparent"
                style="background-image: linear-gradient(to top,#84FAB0, #8FD3F4);">Team</span>
            <span class="text-lg font-bold">Manage your teams and interact with other teams</span>
        </div>
        <div class="flex justify-between mt-2">
            <div class="flex">
                <input v-model="teamParams.privacy_limit" :value="3" type="radio" class="btn btn-ghost btn-sm"
                    aria-label="Homewide" />
                <input v-model="teamParams.privacy_limit" :value="0" type="radio" class="btn btn-ghost btn-sm"
                    aria-label="Globalwide" />
            </div>
            <div class="flex">
                <input v-model="teamParams.active_only" type="checkbox" class="btn btn-sm btn-ghost"
                    aria-label="Active only">
            </div>
        </div>
        <div class="flex flex-col mt-2">
            <div v-for="team in teams" :key="team['id']" class="flex mb-4 h-44 rounded-2xl"
                style="background: url('https://assets.ppy.sh/beatmaps/1990406/covers/cover@2x.jpg?1699284105') center center no-repeat; background-size: cover;">
                <div class="flex flex-col w-full h-full flex-wrap backdrop-brightness-50 rounded-2xl justify-center"
                    style="background-image: linear-gradient(to right, rgba(0, 0, 0, 0.5) 25%, rgba(255, 255, 255, 0) 75%);">
                    <div class="flex">
                        <div class="flex flex-col ml-10">
                            <span class="text-2xl font-bold shadow-md">{{ team.name }}</span>
                            <span class="text-sm mont">Stage on {{ team.active_stage.name }}</span>
                        </div>
                    </div>
                    <MemberShowcase :member="team.member" />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>