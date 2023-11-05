<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { Transition, ref } from 'vue';
import { useUIStore } from './stores/user_interface';

const ui = useUIStore();
const scrollTop = ref(0);

const onScroll = () => {
  scrollTop.value = document.documentElement.scrollTop;
};

window.addEventListener('scroll', onScroll)

</script>

<template>
  <div :class="ui.dialog.isOpen ? 'saturate-50' : ''" class="w-full flex flex-1 transition-all ease-in-out">
    <div class="flex flex-col mb-2 flex-1">
      <div v-bind:class="scrollTop == 0 ? '' : 'detached'" class="navbar-container sticky top-0">
        <div class="navbar bg-primary min-h-12">
          <div class="navbar-start">
            <RouterLink class="btn btn-ghost normal-case text-xl h-10 min-h-0 rounded-3xl" to="/">NOGU</RouterLink>
          </div>
          <div class="navbar-center">
            <RouterLink class="btn btn-ghost normal-case text-lg h-10 min-h-0 font-normal rounded-3xl" to="/team">Team
            </RouterLink>
            <RouterLink class="btn btn-ghost normal-case text-lg h-10 min-h-0 font-normal rounded-3xl" to="/team">Stage
            </RouterLink>
            <RouterLink class="btn btn-ghost normal-case text-lg h-10 min-h-0 font-normal rounded-3xl" to="/team">Pool
            </RouterLink>
          </div>
          <div class="navbar-end">
            <div class="dropdown dropdown-end">
              <label tabindex="0" class="btn btn-ghost btn-circle avatar h-10 min-h-0 p-0 w-10">
                <div class="w-10 rounded-full">
                  <img src="https://a.ppy.sb/1094" />
                </div>
              </label>
              <ul tabindex="0" class="mt-3 z-[1] p-2 shadow menu menu-md dropdown-content bg-neutral rounded-box w-52">
                <li><a>Profile</a></li>
                <li><a>Settings</a></li>
                <li><a>Logout</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="flex flex-1 flex-wrap">
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
.navbar-container {
  /* Thank you guccho! */
  transition-duration: .15s;
  transition-property: padding;
  transition-timing-function: cubic-bezier(.4, 0, .2, 1);
}

.detached {
  /* Thank you guccho! */
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  padding-top: 0.5rem;
}

.detached .navbar {
  /* Thank you guccho! */
  border-radius: 1rem;
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