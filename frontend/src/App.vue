<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { Transition } from 'vue';
import { useUIStore } from './stores/user_interface';

const ui = useUIStore();
</script>

<template>
  <div :class="ui.dialog.isOpen ? 'saturate-50' : ''"
    class="bg-background-brown w-full flex flex-1 transition-all ease-in-out">
    <div class="flex flex-col m-1 mt-2 mb-2 flex-1">
      <header class="mb-2 flex">
        <nav class="flex flex-1">
          <div class="flex flex-1 justify-center content-center items-center bg-primary-purple rounded-xl h-10">
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
    <div v-if="ui.toast.isOpen" class="toast w-72 h-12 bg-pink-200 rounded-xl items-center text-black text-lg font-semibold">
      <div class=" mt-2.5 ml-2.5">
        {{ ui.toast.message }}
      </div>
    </div>
  </Transition>
  
  <Transition name="fade">
    <div v-if="ui.dialog.isOpen" class="dialog-mask absolute" @click="ui.closeDialog()">
    </div>
  </Transition>
  <div class="dialog-container">
    <Transition name="bounce">
      <div v-if="ui.dialog.isOpen" class="bg-background-brighter-brown rounded-xl">
        <component :is="ui.dialog.component"></component>
      </div>
    </Transition>
  </div>
</template>

<style scoped>

.toast {
  position: fixed;
  top: 3.5rem;
  right: 0.5rem;
  z-index: 2000;

}
.dialog-container {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
}

.dialog-mask {
  background-color: rgba(0, 0, 0, 0.8);
  height: 100%;
  width: 100%;
  z-index: 999;
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