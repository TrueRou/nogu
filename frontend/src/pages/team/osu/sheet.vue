<script setup lang="ts">
import ScoresSheet from "@/components/team/scores-sheet.vue";
import type { Stage } from "@/def/typedef";
import { useGlobal } from "@/store/global";
import { client } from "@/utils/requests";
import { ref } from "vue";
import { useRoute } from "vue-router";
import type Spreadsheet from "x-data-spreadsheet";

const stages = ref<Stage[]>([])
const route = useRoute()
const global = useGlobal()

const { data } = await client.GET('/osu/teams/stages/', { params: { query: { team_id: Number(route.params.teamId) } } })
data?.forEach((stage) => stages.value.push(stage))
if (stages.value.length == 0) {
    global.showNotification('error', 'There are no stages to show in the team.', 'error.team.no-stages')
}

const fillData = async (sheet: Spreadsheet, index: number) => {
    const stage_id: number = stages.value[index - 1]?.id ?? 0; // index is 1-based, null value won't be used
    const record = (await client.GET('/osu/stages/sheet/', { params: { query: { stage_id: stage_id } } })).data
    if (!record) return
    for (var i = 0; i < record.rows.length; i++) {
        sheet.cellText(1, i + 3, record.rows[i]?.username ?? '', index)
    }
    for (var i = 0; i < record.cols.length; i++) {
        sheet.cellText(i + 2, 0, '' + record.cols[i]?.beatmap_id, index)
        // sheet.cellText(i + 2, 1, '' + record.cols[i]?.label, index)
        sheet.cellText(i + 2, 2, record.cols[i]?.title ?? '', index)
    }
    sheet.reRender()
}

const modifyMenu = (menu: any) => {
    console.log(menu)
}

</script>
<template>
    <div class="flex w-full h-full justify-center content-center">
        <ScoresSheet v-if="stages.length != 0" :sheets="stages.map(stage => stage.name)" @fill-data="fillData"
            @modify-menu="modifyMenu" />
    </div>
</template>
