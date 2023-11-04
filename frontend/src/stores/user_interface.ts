import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUIStore = defineStore('user_interface', () => {
    const dialog = ref({
        'isOpen': false,
        'component': null,
        'data': {}
    })

    const toast = ref({
        'isOpen': false,
        'type': '',
        'message': ''
    })

    function openDialog(component: any) {
        dialog.value.isOpen = true
        dialog.value.component = component
        dialog.value.data = {}
    }

    function closeDialog() {
        dialog.value.isOpen = false
        dialog.value.component = null
    }

    function showNotification(type: string, message: string, i18n_node: string = '') {
        // if (i18n_node != '') message = handle(i18n_node)
        toast.value.isOpen = true
        toast.value.type = type
        toast.value.message = message
        setTimeout(() => {
            toast.value.isOpen = false
        }, 3000)
    }

    return { dialog, toast, openDialog, closeDialog, showNotification }
})