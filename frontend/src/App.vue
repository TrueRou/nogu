<script setup lang="ts">
import { RouterView } from 'vue-router';
import { Transition, computed } from 'vue';
import { useGlobal } from '@/store/global';
import NavBar from './components/navbar.vue'

const global = useGlobal();
const alertStyle = computed(() => {
  return { top: global.dialog.isOpen ? '0.5rem' : '4rem' }
})


</script>

<template>
  <div :class="global.dialog.isOpen ? 'saturate-50' : ''" class="transition-all ease-in-out">
    <NavBar />
    <RouterView v-slot="{ Component }">
      <keep-alive>
        <div>
          <component class="ml-auto mr-auto" :is="Component" />
        </div>
      </keep-alive>
    </RouterView>
  </div>
  <Transition name="fade">
    <div v-if="global.toast.isOpen" class="z-40">
      <div v-if="global.toast.type == 'info'" class="fixed left-0 right-0 z-50 gap-2 p-3 m-auto alert w-96"
        :style="alertStyle">
        <i class="fa-solid fa-circle-info"></i>
        <p class="whitespace-pre-line">{{ global.toast.message }}</p>
      </div>
      <div v-if="global.toast.type == 'error'" class="fixed left-0 right-0 z-50 gap-2 p-3 m-auto alert alert-error w-96"
        :style="alertStyle">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <p class="whitespace-pre-line">{{ global.toast.message }}</p>
      </div>
    </div>
  </Transition>
  <Transition name="fade">
    <div v-if="global.dialog.isOpen" class="absolute z-20 dialog-mask" @click="global.closeDialog()">
    </div>
  </Transition>
  <div class="z-30 dialog-container">
    <Transition name="bounce">
      <div v-if="global.dialog.isOpen" class="bg-neutral rounded-xl">
        <component :is="global.dialog.component"></component>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.alert {
  grid-auto-flow: row;
  grid-template-columns: auto minmax(auto, 1fr);
  justify-items: start;
  text-align: left;
}


.dialog-container {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.dialog-mask {
  background-color: rgba(0, 0, 0, 0.8);
  height: 100%;
  width: 100%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.bounce-enter-active {
  animation: bounce-in 0.5s;
}

.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}

@keyframes bounce-in {
  0% {
    transform: scale(0);
  }

  50% {
    transform: scale(1.25);
  }

  100% {
    transform: scale(1);
  }
}
</style>