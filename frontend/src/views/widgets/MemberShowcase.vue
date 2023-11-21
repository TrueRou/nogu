<script setup lang="ts">
import { ref } from 'vue';
import { type ITeamMember, Team } from '../../objects/team'
import { t } from '@/translateable';
const props = defineProps<{
    member: ITeamMember[]
}>()
const statelessTeam = new Team()

const selectedMember = ref<ITeamMember | undefined>(statelessTeam.getLeader(props.member))
</script>

<template>
    <div class="flex flex-col ml-10">
        <div class="flex h-13">
            <div class=" mt-2 flex w-10 rounded-full">
                <img class="rounded-full" src="https://a.ppy.sb/1094" />
            </div>
            <div class="flex flex-col ml-2 mt-2">
                <span class="flex text-xs">{{ t(`member-position.${selectedMember?.member_position}`) }}: </span>
                <span class="flex text-lg -mt-1 mont font-bold">{{ selectedMember?.member.username }}</span>
            </div>
        </div>
        <div class="inline-block mt-1.5">
            <input v-for="member in props.member" v-model="selectedMember" :value="member" type="radio"
                class="btn btn-xs btn-accent rounded-2xl text-sm mont font-bold mr-1" style="text-transform: none;"
                :aria-label="member.member.username" />
        </div>
    </div>
</template>@/translatable