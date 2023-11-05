<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { Transition } from 'vue';
import { useUIStore } from './stores/user_interface';

const ui = useUIStore();
</script>

<template>
  <div :class="ui.dialog.isOpen ? 'saturate-50' : ''"
    class="w-full flex flex-1 transition-all ease-in-out">
    <div class="flex flex-col m-1 mt-2 mb-2 flex-1">
      <header class="mb-2 flex">
        <nav class="flex flex-1">
          <div class="flex flex-1 justify-center content-center items-center bg-primary rounded-xl h-10">
            <RouterLink class="flex m-1" to="/">Home</RouterLink>
          </div>
        </nav>
      </header>
      <div class="flex flex-1 justify-center content-center flex-wrap">
        <RouterView />
      </div>
    </div>
  </div>
  <Transition name="fade">
    <div v-if="ui.toast.isOpen">
      <div v-if="ui.toast.type == 'info'" class="alert fixed w-72 right-2 top-2 z-50">
        <i class="fa-solid fa-circle-info"></i>
        <span>{{ ui.toast.message }}</span>
      </div>
      <div v-if="ui.toast.type == 'error'" class="alert alert-error fixed w-72 right-2 top-2 z-50">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <span>{{ ui.toast.message }}</span>
      </div>
    </div>
  </Transition>

  <Transition name="fade">
    <div v-if="ui.dialog.isOpen" class="dialog-mask absolute z-30" @click="ui.closeDialog()">
    </div>
  </Transition>
  <div class="dialog-container z-40">
    <Transition name="bounce">
      <div v-if="ui.dialog.isOpen" class="bg-neutral rounded-xl">
        <component :is="ui.dialog.component"></component>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
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
}</style>