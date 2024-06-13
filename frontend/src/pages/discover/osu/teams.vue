<script setup lang="ts">
import { reactive, ref, watch } from 'vue';
import type { OsuTeamCombination } from '@/def/typedef';
import { client } from '@/utils/requests';
import MemberGizmo from '@/components/team/member-gizmo.vue';
import { asIcon } from '@/utils/ruleset';
import { useRouter } from 'vue-router';

const router = useRouter()
const teams = ref<OsuTeamCombination[]>([])
const teamParams = reactive({
    status: -1
})


const fetchTeams = async () => {
    const { data } = await client.GET('/osu/teams/', { params: { query: { status: teamParams.status } } })
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
        <template v-for="team in teams" :team="team.team">
            <div class="flex w-full h-36 rounded-2xl"
                style="background: url('https://assets.ppy.sh/beatmaps/1990406/covers/cover@2x.jpg?1699284105') center center no-repeat; background-size: cover;">
                <div @click="router.push(`/osu/teams/${team.team.id}`)"
                    class="flex cursor-pointer rounded-2xl w-full h-full flex-wrap backdrop-brightness-50 items-center justify-between"
                    style="background-image: linear-gradient(to right, rgba(0, 0, 0, 0.5) 25%, rgba(255, 255, 255, 0) 75%);">
                    <div class="flex flex-col ml-6" @click.stop>
                        <div class="flex">
                            <span class="text-2xl font-bold shadow-md cursor-auto">{{ team.team.name }}</span>
                        </div>
                        <MemberGizmo :member="team.team.user_links" />
                    </div>
                    <div class="flex flex-col justify-between h-full p-5" @click.stop>
                        <div class="flex w-8 h-8 cursor-auto"><img :src="asIcon(team.stage.ruleset)"
                                onload="SVGInject(this)"></div>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>