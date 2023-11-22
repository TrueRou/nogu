<script setup lang="ts">
import { reactive, ref, watch } from 'vue';
import { Team, type ITeam, type ITeamShowcaseParams } from '@/objects/team'
import TeamCard from '@/views/widgets/TeamCard.vue';

const statelessTeam = new Team()

const teams = ref<ITeam[]>([])
const teamParams = reactive({
    status: -1
} as ITeamShowcaseParams)

watch([teamParams], async () => teams.value = await statelessTeam.fetchShowcase(teamParams), { immediate: true })
</script>

<template>
    <div class="flex mt-1">
        <div class="flex font-bold text-md pt-1 mr-3">Status:</div>
        <input v-model="teamParams.status" :value="-1" type="radio" class="btn btn-sm btn-accent btn-ghost mr-1"
            aria-label="All" />
        <input v-model="teamParams.status" :value="0" type="radio" class="btn btn-sm btn-accent btn-ghost mr-1"
            aria-label="Active" />
        <input v-model="teamParams.status" :value="1" type="radio" class="btn btn-sm btn-accent btn-ghost mr-1"
            aria-label="Achieved" />
    </div>
    <div class="flex flex-col mt-2">
        <div v-for="team in teams" :key="team['id']" class="flex mb-4 h-44 rounded-2xl"
            style="background: url('https://assets.ppy.sh/beatmaps/1990406/covers/cover@2x.jpg?1699284105') center center no-repeat; background-size: cover;">
            <TeamCard :team="team" />
        </div>
    </div>
</template>