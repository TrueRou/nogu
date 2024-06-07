<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { Transition, ref } from 'vue';
import { useGlobal } from './store/global';

const global = useGlobal();
const scrollTop = ref(0);

const onScroll = () => {
  scrollTop.value = document.documentElement.scrollTop;
};

window.addEventListener('scroll', onScroll)

</script>

<template>
  <div :class="global.dialog.isOpen ? 'saturate-50' : ''" class="w-full flex flex-1 transition-all ease-in-out">
    <div class="flex flex-col mb-2 flex-1">
      <div v-bind:class="scrollTop == 0 ? '' : 'detached'" class="navbar-container sticky top-0 z-10">
        <div class="navbar min-h-fit h-12 md:h-14 bg-primary pt-0 pb-0">
          <div class="navbar-start">
            <RouterLink class="btn btn-ghost normal-case text-lg rounded-3xl h-8 md:h-10 min-h-fit" to="/">NOGU
            </RouterLink>
          </div>
          <div class="navbar-center">
            <RouterLink class="btn btn-ghost normal-case text-lg font-normal rounded-3xl h-8 md:h-10 min-h-fit"
              to="/showcase">
              Showcase
            </RouterLink>
          </div>
          <div class="navbar-end">
            <div class="dropdown dropdown-end h-10">
              <label tabindex="0" class="btn btn-ghost btn-circle avatar p-0 w-10 h-fit min-h-fit">
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
        <div class="flex justify-center ml-2 mr-2 mt-2 w-full">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
  <Transition name="fade">
    <div v-if="global.toast.isOpen" class="z-20">
      <div v-if="global.toast.type == 'info'" class="alert fixed w-72 right-2 top-2 z-50">
        <i class="fa-solid fa-circle-info"></i>
        <p class="whitespace-pre-line">{{ global.toast.message }}</p>
      </div>
      <div v-if="global.toast.type == 'error'" class="alert alert-error fixed w-72 right-2 top-2 z-50">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <p class="whitespace-pre-line">{{ global.toast.message }}</p>
      </div>
    </div>
  </Transition>
  <Transition name="fade">
    <div v-if="global.dialog.isOpen" class="dialog-mask absolute z-30" @click="global.closeDialog()">
    </div>
  </Transition>
  <div class="dialog-container z-40">
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