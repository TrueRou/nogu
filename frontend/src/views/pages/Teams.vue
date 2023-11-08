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
                        style="background-image: linear-gradient(to top,#84FAB0, #8FD3F4);">Team</span>
                    <span class="text-lg font-bold">Manage your teams and interact with other teams</span>
                </div>
                <div class="flex flex-col mt-4">
                    <div v-for="team in teams" :key="team['id']" class="flex mb-4 h-44 rounded-2xl"
                        style="background: url('https://assets.ppy.sh/beatmaps/1395192/covers/cover.jpg') center center no-repeat;">
                        <div class="flex flex-col w-full h-full flex-wrap backdrop-brightness-50 rounded-2xl justify-center"
                            style="background-image: linear-gradient(to right, rgba(0, 0, 0, 0.5) 25%, rgba(255, 255, 255, 0) 75%);">
                            <div class="flex">
                                <div class="flex flex-col ml-10">
                                    <div class="flex flex-col">
                                        <span class="text-2xl font-bold shadow-md">{{ team.name }}</span>
                                        <span class="text-sm mont">Stage on {{ team.active_stage.name }}</span>
                                    </div>
                                    <div class="flex h-13">
                                        <div class=" mt-2 flex w-10 rounded-full">
                                            <img class="rounded-full" src="https://a.ppy.sb/1094" />
                                        </div>
                                        <div class="flex flex-col ml-2 mt-2">
                                            <span class="flex text-xs">Leader: </span>
                                            <span class="flex text-lg -mt-1 mont font-bold">{{
                                                statelessTeam.getLeaderUsername(team)
                                            }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="inline-block mt-1.5 ml-10">
                                <div style="background-color: rgba(128, 128, 128, 0.5)"
                                    class="inline-block w-auto pt-0.5 pb-0.5 pl-2 pr-2 mr-1 rounded-2xl text-sm mont font-bold">
                                    TuRou
                                </div>
                                <div style="background-color: rgba(128, 128, 128, 0.5)"
                                    class="inline-block w-auto pt-0.5 pb-0.5 pl-2 pr-2 mr-1 rounded-2xl text-sm mont font-bold">
                                    TuRou
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>