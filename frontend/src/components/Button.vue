<script setup lang="ts">
import { ref, type PropType } from 'vue';
import { ButtonKinds } from './typedef';

const kind_sets = {
    'primary': ['bg-primary-purple', 'hover:bg-primary-brighter-purple', 'text-white'],
    'secondary': ['bg-slate-100', 'hover:bg-white', 'text-black'],
    'normal': ['bg-slate-100', 'hover:bg-white', 'text-black'],
}

defineEmits(['click'])

const props = defineProps({
    kind: {
        type: String as PropType<ButtonKinds>,
        default: ButtonKinds.Primary,
        required: false,
    },
    height: {
        type: String,
        default: '2.25',
        required: false,
    },
    width: {
        type: String,
        default: '5',
        required: false,
    },
    weight: {
        type: String,
        default: '400',
        required: false,
    },
    text: {
        type: String,
        required: true,
    }
})

const styles = ref({
    'height': `${props.height}rem`,
    'width': `${props.width}rem`,
    'font-weight': `${props.weight}`,
})

</script>

<template>
    <button :class="kind_sets[props.kind]" :style="styles" @click="$emit('click')">{{ props.text }}</button>
</template>

<style scoped>
button {
    display: flex;
    border-radius: 0.4rem;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s ease-in-out;
}
</style>