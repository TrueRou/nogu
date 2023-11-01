<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="bg-background-brown h-full w-full flex flex-1">
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
</template>

<style scoped></style>