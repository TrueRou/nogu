<script setup lang="ts">
import type { TeamUserLinkPublic } from '@/def/types';
import { t } from '@/def/translations';
import { ref } from 'vue';
const props = defineProps<{
    member: TeamUserLinkPublic[]
}>()

const selectedMember = ref<TeamUserLinkPublic | undefined>(props.member[0])
</script>

<template>
    <div class="flex flex-col">
        <div class="flex h-13 items-center">
            <div class="flex w-8 h-8 rounded-full">
                <img class="rounded-full" src="https://a.ppy.sb/1094" />
            </div>
            <div class="flex flex-col ml-2">
                <span class="flex text-xs">{{ t(`member-position.${selectedMember?.role}`) }}: </span>
                <span class="flex text-base -mt-1 mont font-bold">{{ selectedMember?.user.username }}</span>
            </div>
        </div>
        <div class="inline-block mt-1.5">
            <input v-for="member in props.member" v-model="selectedMember" :value="member" type="radio"
                class="btn btn-xs btn-accent rounded-2xl text-sm mont font-bold mr-1" style="text-transform: none;"
                :aria-label="member.user.username" />
        </div>
    </div>
</template>