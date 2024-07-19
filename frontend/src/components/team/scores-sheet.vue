<script setup lang="ts">
import { onMounted } from "vue";
import Spreadsheet, { type Options } from "x-data-spreadsheet";

const props = defineProps<{
    sheets: string[]
}>()

const emit = defineEmits({
    fillData: (sheet: Spreadsheet, index: number) => true,
    modifyMenu: (menu: any) => true
})

const options: Options = {
    mode: 'edit', // edit | read
    showToolbar: true,
    showGrid: true,
    showContextmenu: true,
    view: {
        height: () => document.documentElement.clientHeight - 100,
        width: () => document.documentElement.clientWidth - 200,
    },
    row: {
        len: 100,
        height: 25,
        indexHeight: 0,
    },
    col: {
        len: 26,
        width: 100,
        indexWidth: 0,
        minWidth: 60,
    },
    style: {
        bgcolor: '#1f2025',
        align: 'left',
        valign: 'middle',
        textwrap: false,
        strike: false,
        underline: false,
        color: '#ffffff',
        font: {
            name: 'Helvetica',
            size: 10,
            bold: false,
            italic: false,
        },
    },
}

onMounted(async () => {
    const sheet: any = new Spreadsheet("#x-spreadsheet", options)
    props.sheets.forEach(title => sheet.addSheet(title, true))
    emit('fillData', sheet, props.sheets.length) // Manually fill the last sheet with data
    sheet.on('swap', (index: number) => emit('fillData', sheet, index))
    emit('modifyMenu', sheet.sheet.contextMenu)
    const lastButton: Element & { click: () => void } | null = document.querySelector("#x-spreadsheet > div > div.x-spreadsheet-bottombar > ul > li:last-child")
    lastButton?.click() // Activate the last sheet by emulating clicking the button. (this might be a bug in x-spreadsheet)
})

</script>
<template>
    <div id="x-spreadsheet"></div>
</template>
<style>
.x-spreadsheet {
    color: white;
    background-color: #1f2025;
}

.x-spreadsheet-toolbar {
    color: black;
    width: unset !important;
}

.x-spreadsheet-scrollbar {
    color: #382e32;
}

.x-spreadsheet-editor-area>textarea {
    background-color: #1f2025;
}

.x-spreadsheet-bottombar .x-spreadsheet-menu>li {
    height: 39px;
}

.x-spreadsheet-scrollbar.horizontal {
    right: 0;
}

#x-spreadsheet>div>div.x-spreadsheet-bottombar>ul>li:nth-child(1) {
    display: none;
}

#x-spreadsheet>div>div.x-spreadsheet-bottombar>ul>li:nth-child(2) {
    display: none;
}
</style>