<script setup lang="ts">
import { useUserStore } from '@/stores/user_information';
import { computed, ref, watch } from 'vue';
import { format } from 'timeago.js';
import type { Team } from '@/schema';
import { MemberPosition } from '@/constants';
import 

const user = useUserStore()

const active_only = ref(false)
const homewide = ref(false)
const teams = ref<Team[]>([])

const entrypoint = computed(() => {
    return homewide.value ? '/teams/me/' : '/teams/all/'
})

const getLeader = (team: Team) => {
    return team.member.find(member => member.member_position == MemberPosition.OWNER)
}

fetchOne

const fetch = async () => {
    const response = await user.requests().get(entrypoint.value, {
        params: {
            active_only: active_only.value
        }
    })
    teams.value = response.data
}

fetch()
watch([active_only, homewide], async () => await fetch())

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
                                <span class="flex text-sm items-center">{{ getLeader(team)?.member.username }}</span>
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