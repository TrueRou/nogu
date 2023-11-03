import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUIStore = defineStore('user_interface', () => {
    const dialog = ref({
        'isOpen': false,
        'component': '',
        'data': {}
    })

    function openDialog(component: string) {
        dialog.value.isOpen = true
        dialog.value.component = component
        dialog.value.data = {}
    }

    function closeDialog() {
        dialog.value.isOpen = false
        dialog.value.component = ''
    }

    return { dialog, openDialog, closeDialog }
})