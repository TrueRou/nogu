<script setup lang="ts">
import { ref, type PropType } from 'vue';
import { InputKinds } from './typedef';

const kind_sets = {
    'dark': ['bg-background-brighter-pink', 'text-white'],
    'bright': ['bg-slate-100', 'text-black'],
}

defineEmits(['update:modelValue'])

const props = defineProps({
    kind: {
        type: String as PropType<InputKinds>,
        default: InputKinds.Bright,
        required: false,
    },
    height: {
        type: String,
        default: '2.25',
        required: false,
    },
    width: {
        type: String,
        default: '10',
        required: false,
    },
    weight: {
        type: String,
        default: '400',
        required: false,
    },
    placeholder: {
        type: String,
        default: '',
        required: false,
    },
    modelValue: String,
})

const styles = ref({
    'height': `${props.height}rem`,
    'width': `${props.width}rem`,
    'font-weight': `${props.weight}`,
})

</script>

<template>
    <input :value="modelValue" @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        :class="kind_sets[props.kind]" :style="styles" :placeholder="props.placeholder">
</template>

<style scoped>
input {
    display: flex;
    border-radius: 0.4rem;
    align-items: center;
    justify-content: center;
    padding: 0.35rem;
    font-size: 14px;
    /* transition: background-color 0.2s ease-in-out; */
}
</style>