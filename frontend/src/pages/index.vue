<script setup lang="ts">
</script>

<template>
    <div class="space-y-8">
        <div class="max-w-screen-md mx-auto">
            <div class="flex justify-between">
                <div class="flex flex-col justify-center">
                    <span
                        class="mx-auto my-12 font-extrabold !tracking-[40%] text-transparent text-7xl bg-clip-text nogu-brand"
                        style="background-image: linear-gradient(to top,#F093FB, #F5576C);">NOGU</span>
                    <h2 class="text-xl font-semibold tracking-wide">Focusing on collecting, sorting, analyzing scores.
                    </h2>
                    <span class="max-w-[500px] font-light mt-6 tracking-wide">More introduction to nogu and its featured
                        games. This
                        page
                        is only for information represention and provide a route to the specific featured game
                        pages.</span>
                </div>
                <img class="hidden h-96 ms-auto sm:block" src="https://s2.loli.net/2023/11/01/mrZisGMnxqtC8Tv.png">
            </div>
        </div>
        <div class="py-4 space-y-4 bg-neutral">
            <div class="max-w-screen-md mx-auto space-y-4">
                <div class="flex text-xl font-semibold tracking-widest uppercase">Featured Games</div>
                <div class="flex flex-wrap gap-2">
                    <RouterLink to="/osu" class="overflow-hidden">
                        <img class="flex object-cover w-36 h-44 rounded-2xl"
                            src="../assets/images/games/osu-vertical.png">
                    </RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>
