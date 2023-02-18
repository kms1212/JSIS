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
  <div class="relative h-full overflow-hidden">
    <div class="relative h-full">
      <RouterLink
        v-for="(image, idx) in images"
        v-bind:key="idx"
        :to="image.link"
        class="h-full w-full items-center duration-700 ease-in-out"
      >
        <transition>
          <img
            :src="image.url"
            v-if="idx == selected"
            class="absolute block h-full w-full object-cover"
            :alt="image.alt"
          />
        </transition>
      </RouterLink>
    </div>
    <button
      type="button"
      class="group absolute top-0 left-0 flex h-full items-center cursor-pointer justify-center px-4 focus:outline-none"
      @click="prevBtnClick"
    >
      <span
        class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/30 group-hover:bg-white/50 group-focus:outline-none group-focus:ring-4 group-focus:ring-white"
      >
        <vue-feather type="chevron-left"></vue-feather>
        <span class="sr-only">Previous</span>
      </span>
    </button>
    <button
      type="button"
      class="group absolute top-0 left-0 flex h-full items-center cursor-pointer justify-center px-4 focus:outline-none"
      @click="nextBtnClick"
    >
      <span
        class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/30 group-hover:bg-white/50 group-focus:outline-none group-focus:ring-4 group-focus:ring-white"
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
