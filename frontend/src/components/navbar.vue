<script setup>
import { computed, ref } from 'vue';
import { useGlobal } from '@/store/global';
import { useSession } from '@/store/session';
import osu_logo from '@/assets/images/osu/osu-logo.svg';

const session = useSession();
const global = useGlobal();


const scrollTop = ref(0);

window.addEventListener('scroll', onScroll)



const featured_games = {
    '': {
        name: 'NOGU',
        icon: null,
        route: '/'
    },
    'osu': {
        name: 'osu!',
        icon: osu_logo,
        route: '/osu'
    },
}

const hasFeaturedGame = computed(() => {
    return global.navMenu.featured_game != '';
});

const currentGame = computed(() => {
    return featured_games[global.navMenu.featured_game];
});

function onScroll() {
    scrollTop.value = document.documentElement.scrollTop;
};

</script>

<template>
    <div class="sticky top-0 z-10 navbar-container" :class="{
        detached: scrollTop > 0
    }">
        <div class="navbar">
            <div class="x-spacer"></div>
            <div class="navbar-start">
                <RouterLink class="relative h-10 p-1 text-lg btn btn-ghost rounded-3xl min-h-fit"
                    :to="currentGame.route">
                    <img v-if="hasFeaturedGame" :src="currentGame.icon" class="h-7">
                    <span class="nogu-brand-small">NOGU</span>
                </RouterLink>
            </div>
            <div class="navbar-center">
                <template v-if="hasFeaturedGame">
                    <RouterLink class="h-10 text-lg btn btn-ghost rounded-3xl min-h-fit"
                        :to="currentGame.route + '/discover'">
                        <i class="fa-solid fa-globe" />
                        <b>Discover</b>
                    </RouterLink>
                </template>
            </div>
            <div class="items-center navbar-end">
                <RouterLink
                    class="text-lg btn btn-ghost btn-circle min-h-fit"
                    to="/">
                    <i class="fa-solid fa-search" />
                </RouterLink>
                <div class="dropdown dropdown-end">
                    <div role="button" tabindex="0" class="btn btn-ghost btn-circle avatar">
                        <div class="rounded-full w-9">
                            <img v-if="session.isLoggedIn" src="https://a.ppy.sb/1094" />
                            <img v-else="session.isLoggedIn" src="https://a.ppy.sb/-1" />
                        </div>
                    </div>
                    <ul tabindex="0"
                        class="mt-3 z-[1] p-2 shadow menu menu-md dropdown-content bg-neutral rounded-box w-52">
                        <template v-if="session.isLoggedIn">
                            <li><a>Profile</a></li>
                            <li><a>Settings</a></li>
                            <li><a>Logout</a></li>
                        </template>
                        <template v-else>
                            <li><a>Login</a></li>
                            <li><a>Register</a></li>
                        </template>
                    </ul>
                </div>
                <div class="x-spacer"></div>
            </div>
        </div>
    </div>

</template>


<style lang="postcss">
.navbar {
    @apply transition-[border-radius] duration-500;
    @apply p-1 top-0 h-12 min-h-fit md:h-14 from-primary/30 mix-blend-multiply bg-gradient-to-b;
}


.detached {
    .navbar {
        @apply bg-primary from-primary via-primary to-primary;
    }
}

.navbar-container {
    @apply pb-2;

    /* Thank you guccho! */
    transition-duration: .15s;
    transition-property: padding translate;
    transition-timing-function: cubic-bezier(.4, 0, .2, 1);

    &.detached {
        @apply px-1 translate-y-1;
        @apply md:px-[0.375rem] md:translate-y-[0.375rem];

        .navbar {
            @apply rounded-3xl md:rounded-xl;
        }
    }
}


.x-spacer {
    @apply hidden w-2 md:block;
}
</style>