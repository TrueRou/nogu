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

    function showNotification(type: string, message: string, i18n_node: string = '') {
        // if (i18n_node != '') message = handle(i18n_node)
    }

    return { dialog, openDialog, closeDialog, showNotification }
})