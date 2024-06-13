<script setup lang="ts">
import type { OsuTeamCombination } from '@/def/typedef';
import { client } from '@/utils/requests';
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const team = ref<OsuTeamCombination>()

const route = useRoute();
const { data } = await client.GET('/osu/teams/{team_id}', { params: { path: { team_id: Number(route.params.teamId) } } })
if (data) team.value = data

</script>
<template>
    <div class="flex flex-col flex-panel-2">
        <div class="flex h-36 w-full rounded-2xl"
            style="background: url('https://assets.ppy.sh/beatmaps/1990406/covers/cover@2x.jpg?1699284105') center center no-repeat; background-size: cover;">
            <div class="flex flex-col w-full h-full flex-wrap backdrop-brightness-50 rounded-2xl justify-center"
                style="background-image: linear-gradient(to right, rgba(0, 0, 0, 0.5) 25%, rgba(255, 255, 255, 0) 75%);">
            </div>
        </div>
        <div class="flex -translate-y-12">
            <div class="flex w-24 h-24 rounded-lg ml-6">
                <img class="rounded-lg" src="https://a.ppy.sb/1094" />
            </div>
            <div class="flex ml-2 mt-5 mb-10 flex-col justify-between">
                <div class="flex mont font-semibold h-6">{{ team?.team.slogan }}</div>
                <div class="flex"><span class="mont h-8 text-2xl font-bold bg-clip-text text-transparent mt-3"
                        style="background-image: linear-gradient(to top,#F093FB, #F5576C);">{{ team?.team.name }}</span>
                </div>
            </div>
        </div>
        <div v-if="team?.stage" class="flex -mt-16 w-full h-12 bg-neutral rounded-xl justify-between">
            <div class="flex content-center flex-wrap mont font-semibold ml-4">{{ team?.stage.name }}</div>
            <div class="flex h-full w-48 rounded-r-xl"
                style="background: linear-gradient(to right, #382e32 1%, transparent 100%), url('https://assets.ppy.sh/beatmaps/1994349/covers/cover.jpg') center center no-repeat; background-size: cover;">
            </div>
        </div>
        <span class="ml-2 mont font-bold text-lg mt-2">statistics: </span>
        <div class="flex w-full flex-col bg-neutral rounded-xl p-2">
            <div class="flex ml-2 mt-2">
                <div class="flex flex-col flex-wrap content-center mr-4">
                    <span class="text-center mont">Play Count</span>
                    <span class="text-center mont font-semibold text-lg">10,000</span>
                </div>
                <div class="flex flex-col flex-wrap content-center mr-4">
                    <span class="text-center mont">Play Time</span>
                    <span class="text-center mont font-semibold text-lg">128h</span>
                </div>
            </div>
            <div class="ml-2 mt-2">
                <span class="text-sm mont">Created at 14 days ago, Achieved after 30 days, Timezone UTC+8</span>
            </div>
        </div>
        <span class="ml-2 mont font-bold text-lg mt-2">me: </span>
        <div class="flex w-full flex-col bg-neutral rounded-xl p-3 mont">
            Welcome to our page<br>
            Main Sheet: https://www.google.com/sheets/about/<br>
            Sheet: https://www.google.com/sheets/about/
        </div>
        <span class="ml-2 mont font-bold text-lg mt-2">Latest scores: </span>
        <div class="flex w-full flex-col bg-neutral rounded-xl p-2 h-96">

        </div>
    </div>
</template>