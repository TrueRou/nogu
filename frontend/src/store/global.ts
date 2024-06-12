import { ref } from 'vue'
import { defineStore } from 'pinia'
import { t } from '@/utils/translations'

export const useGlobal = defineStore('global', () => {
    const dialog = ref({
        'isOpen': false,
        'component': null,
    })

    const toast = ref({
        'isOpen': false,
        'type': '',
        'message': ''
    })

    const navMenu = ref({
        'featured_game': '',
    })

    function openDialog(component: any) {
        if (dialog.value.isOpen) {
            dialog.value.isOpen = false
            setTimeout(() => {
                dialog.value.isOpen = true
                dialog.value.component = component
            }, 500)
        } else {
            dialog.value.isOpen = true
            dialog.value.component = component
        }
    }

    function closeDialog() {
        dialog.value.isOpen = false
        dialog.value.component = null
    }

    function showNotification(type: string, message: string, i18n_node: string = '') {
        toast.value.isOpen = true
        toast.value.type = type
        toast.value.message = t(i18n_node, message)
        setTimeout(() => {
            toast.value.isOpen = false
        }, 3000)
    }

    return { dialog, toast, navMenu, openDialog, closeDialog, showNotification }
})