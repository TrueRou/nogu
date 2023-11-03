<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { useUIStore } from './stores/user_interface';

const ui = useUIStore();
</script>

<template>
  <div class="bg-background-brown w-full flex flex-1">
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
  <div v-if="ui.dialog.isOpen" class="dialog-container w-80 md:w-96 h-4/6 bg-background-brighter-brown">
    <component :is="ui.dialog.component"></component>
  </div>
</template>

<style scoped>
/* include some styles for dialog */
.dialog-container {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  border-radius: 1rem;
}
</style>