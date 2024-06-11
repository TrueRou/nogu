<script setup lang="ts">
import { reactive, ref, watch } from 'vue';
import teamBanner from '@/components/team/team-banner.vue';
import type { TeamWithMembers } from '@/def/types';
import { client } from '@/def/requests';

const teams = ref<TeamWithMembers[]>([])
const teamParams = reactive({
    status: -1
})

const fetchTeams = async () => {
    const { data } = await client.GET('/teams/', { params: { query: { status: teamParams.status } } })
    if (data) teams.value = data
}

watch([teamParams], async () => await fetchTeams(), { immediate: true })
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
        <teamBanner v-for="team in teams" :team="team" />
    </div>
</template>