import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { list } from 'postcss'
import type { ExceptionNode } from '@/schema'

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

    function translate(i18n_node: string, fallback?: string) {
        return fallback || ''
    }

    function showException(exception_node: ExceptionNode) {
        let message = translate(exception_node.i18n_node, exception_node.message)
        if (exception_node.details != null) {
            message += ': \n'
            for (const detail of exception_node.details) {
                message += translate(detail.i18n_node, detail.message) + '\n'
            }
        }
        showNotification('error', message)
    }

    function showNotification(type: string, message: string, i18n_node?: string) {
        toast.value.isOpen = true
        toast.value.type = type
        toast.value.message = message
        setTimeout(() => {
            toast.value.isOpen = false
        }, 3000)
    }

    return { dialog, toast, openDialog, closeDialog, showNotification, showException }
})