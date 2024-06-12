<script setup lang="ts">
</script>

<template>
    <div class="flex flex-col justify-center content-center flex-wrap">
        <div class="flex">
            <div class="flex flex-col justify-center">
                <span class="text-5xl font-extrabold bg-clip-text text-transparent"
                    style="background-image: linear-gradient(to top,#F093FB, #F5576C);">NOGU</span>
                <h2 class="text-xl font-bold ">Focusing on collecting, sorting, analyzing scores</h2>
                <span class="mt-4" style="max-width: 500px">More introduction to nogu and its featured games. This page
                    is only for information represention and provide a route to the specific featured game pages.</span>
            </div>
            <img class="hidden h-64 sm:flex md:ml-24" src="https://s2.loli.net/2023/11/01/mrZisGMnxqtC8Tv.png">
        </div>
        <div class="flex mt-4 flex-col">
            <div class="flex mb-4">Featured Games</div>
            <div class="flex flex-wrap">
                <div class="flex flex-col mr-4 mb-4 w-36 h-44 rounded-2xl">
                    <RouterLink to="/osu">
                        <img class="flex w-full h-full object-cover rounded-2xl"
                            src="../assets/images/games/osu-vertical.png">
                    </RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>
