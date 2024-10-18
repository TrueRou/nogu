<script setup lang="tsx">
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

const itemClick = (btn_label: string) => {
    console.log(btn_label)
}

const fillData = async (sheet: Spreadsheet, index: number) => {
    const sheetAny: any = sheet
    const stage_id: number = stages.value[index - 1]?.id ?? 0; // index is 1-based, null value won't be used
    const record = (await client.GET('/osu/stages/sheet/', { params: { query: { stage_id: stage_id } } })).data
    if (record) {
        record.rows.forEach((row, i) => {
            sheet.cellText(1, i + 3, row.username, index)
            sheetAny.datas[index].getCell(1, i + 3)['data-value'] = row
            sheetAny.datas[index].getCell(1, i + 3)['data-type'] = 'stage_user'
        })
        record.cols.forEach((col, i) => {
            sheet.cellText(i + 2, 0, String(col.beatmap_id), index)
            sheet.cellText(i + 2, 1, col.label, index)
            sheet.cellText(i + 2, 2, col.title, index)
            sheetAny.datas[index].getCell(i + 2, 2)['data-value'] = col
            sheetAny.datas[index].getCell(i + 2, 2)['data-type'] = 'stage_map'
            record.rows.forEach((row, j) => {
                const cell = record.cells[col.map_md5]![String(row.user_id)]
                if (cell) {
                    sheet.cellText(i + 2, j + 3, String(cell.average_accuracy), index)
                    sheetAny.datas[index].getCell(i + 2, j + 3)['data-value'] = cell
                    sheetAny.datas[index].getCell(i + 2, j + 3)['data-type'] = 'stage_map_user'
                }
            })
        })
        sheet.reRender()
    }
}

const modifyMenu = (menu: any, dict: Record<string, string> = { "AAA": "BBB" }) => {
    const menuParent = document.getElementsByClassName('x-spreadsheet-contextmenu')[0]!
    menuParent.innerHTML = "" // clear the default menu
    Object.keys(dict).forEach((key) => {
        const button = document.createElement('div')
        button.innerText = dict[key] ?? key
        button.classList.add('x-spreadsheet-item')
        button.onclick = () => {
            menu.hide()
            menu.itemClick(key)
        }
        menuParent.appendChild(button)
    })
}

</script>
<template>
    <div class="flex w-full h-full justify-center content-center">
        <ScoresSheet v-if="stages.length != 0" :sheets="stages.map(stage => stage.name)" @fill-data="fillData"
            @modify-menu="modifyMenu" />
    </div>
</template>
