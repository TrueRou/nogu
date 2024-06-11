<script setup>
import { useGlobal } from '@/store/global';
import { useSession } from '@/store/session';
import { computed } from 'vue';
import osu_logo from '@/assets/images/osu/osu-logo.svg';

const session = useSession();
const global = useGlobal();

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
</script>

<template>
    <div class="navbar min-h-fit h-12 md:h-14 bg-primary pt-0 pb-0">
        <div class="navbar-start">
            <RouterLink class="btn btn-ghost normal-case text-lg rounded-3xl h-8 md:h-10 min-h-fit"
                :to="currentGame.route">
                <img v-if="hasFeaturedGame" :src="currentGame.icon" width="24" height="24">
                <span>NOGU</span>
            </RouterLink>
        </div>
        <div class="navbar-center">
            <template v-if="hasFeaturedGame">
                <RouterLink class="btn btn-ghost normal-case text-lg font-normal rounded-3xl h-8 md:h-10 min-h-fit"
                    to="/discover/osu">
                    <i class="fa-solid fa-globe"></i>
                    <b>Discover</b>
                </RouterLink>
            </template>
        </div>
        <div class="navbar-end">
            <RouterLink
                class="btn btn-ghost btn-circle normal-case text-lg font-normal rounded-full h-10 w-10 min-h-fit"
                to="/discover/osu">
                <i class="fa-solid fa-search"></i>
            </RouterLink>
            <div class="dropdown dropdown-end h-10">
                <label tabindex="0" class="btn btn-ghost btn-circle avatar p-0 w-10 h-fit min-h-fit">
                    <div class="w-10 rounded-full">
                        <img v-if="session.isLoggedIn" src="https://a.ppy.sb/1094" />
                    </div>
                </label>
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
        </div>
    </div>
</template>