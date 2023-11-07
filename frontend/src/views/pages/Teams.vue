<script setup lang="ts">
import { reactive, ref, watch } from 'vue';
import { format } from 'timeago.js';
import { Team, type ITeam, type ITeamArgs as ITeamParams } from '@/objects/team';

const statelessTeam = new Team() // Create stateless instance for axios lifetime
const teams = ref<ITeam[]>([])
const teamParams = reactive({
    privacy_limit: 0,
    active_only: false,
} as ITeamParams)

watch([teamParams], async () => teams.value = await statelessTeam.fetchAll(teamParams), { immediate: true })

</script>

<template>
    <div class="flex ml-4 mr-4 mt-6 w-full">
        <div class="flex justify-center w-full">
            <div class="flex flex-col flex-panel">
                <div class="flex flex-col">
                    <span class="text-3xl font-extrabold md:h-10 bg-clip-text text-transparent"
                        style="background-image: linear-gradient(to top,#84FAB0, #8FD3F4);">TEAM</span>
                    <span class="text-lg font-bold">Manage your teams and interact with other teams</span>
                </div>
                <div class="flex flex-col mt-4">
                    <div v-for="team in teams" :key="team['id']"
                        class="flex mb-4 h-16 bg-primary hover:bg-primary-focus transition-colors rounded-2xl content-center flex-wrap justify-between">
                        <div class="flex">
                            <div style="height: 3.5rem; width: 6.2rem;" class="flex bg-black rounded-2xl ml-3"></div>
                            <div class="flex flex-col ml-3 justify-center">
                                <div class="flex flex-col">
                                    <span class="text-lg font-bold">{{ team.name }}</span>
                                    <span class="text-sm">Created at {{ format(team.create_at) }}</span>
                                </div>
                            </div>
                        </div>
                        <div class="flex mr-3 flex-col justify-center">
                            <div class="flex justify-end content-center flex-wrap">
                                <span class="mr-1"><i class="fa-xs fa-solid fa-lock mb-1"></i></span>
                                <span class="flex items-center w-4 rounded-full">
                                    <img class="rounded-full" src="https://a.ppy.sb/1094" />
                                </span>
                                <span class="flex text-sm items-center">{{ statelessTeam.getLeaderUsername(team) }}</span>
                            </div>
                            <div class="flex">
                                <span class="text-sm">Stage on {{ team.active_stage.name }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>