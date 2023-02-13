<script>
import { RouterLink } from "vue-router";

export default {
  name: "LinkCarouselComp",
  components: {
    RouterLink,
  },
  props: {
    images: {
      type: Array,
      required: true,
    },
  },
  methods: {
    nextBtnClick() {
      if (this.selected >= this.images.length - 1) {
        this.selected = 0;
      } else {
        this.selected++;
      }
    },
    prevBtnClick() {
      if (this.selected <= 0) {
        this.selected = this.images.length - 1;
      } else {
        this.selected--;
      }
    },
  },
  data() {
    return {
      selected: 0,
    };
  },
};
</script>

<template>
  <div class="relative overflow-hidden h-full">
    <div class="relative h-full">
      <RouterLink
        v-for="(image, idx) in images"
        v-bind:key="idx"
        :to="image.link"
        class="duration-700 ease-in-out items-center w-full h-full"
      >
        <transition>
          <img
            :src="image.url"
            v-if="idx == selected"
            class="object-cover absolute block w-full h-full"
            :alt="image.alt"
          />
        </transition>
      </RouterLink>
    </div>
    <button
      type="button"
      class="absolute top-0 left-0 flex items-center justify-center h-full px-4 cursor-pointer group focus:outline-none"
      @click="prevBtnClick"
    >
      <span
        class="inline-flex items-center justify-center w-10 h-10 rounded-full bg-white/30 dark:bg-gray-800/30 group-hover:bg-white/50 group-focus:ring-4 group-focus:ring-white group-focus:outline-none"
      >
        <vue-feather type="chevron-left"></vue-feather>
        <span class="sr-only">Previous</span>
      </span>
    </button>
    <button
      type="button"
      class="absolute top-0 right-0 flex items-center justify-center h-full px-4 cursor-pointer group focus:outline-none"
      @click="nextBtnClick"
    >
      <span
        class="inline-flex items-center justify-center w-10 h-10 rounded-full bg-white/30 dark:bg-gray-800/30 group-hover:bg-white/50 group-focus:ring-4 group-focus:ring-white group-focus:outline-none"
      >
        <vue-feather type="chevron-right"></vue-feather>
        <span class="sr-only">Next</span>
      </span>
    </button>
  </div>
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
