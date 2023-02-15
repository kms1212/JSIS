<script>
import { RouterLink } from "vue-router";

export default {
  name: "ReplyView",
  components: {
    RouterLink,
  },
};
</script>

<template>
  <div class="bg-black bg-opacity-50 py-6 sm:py-12">
    <div
      class="flex flex-col bg-white px-6 pt-10 pb-8 shadow-xl ring-1 ring-gray-900/5 h-5/6 lg:mx-auto lg:w-[56rem] lg:rounded-lg lg:px-10"
    >
      <div
        class="relative top-0 left-0 flex flex-row justify-between items-center pb-4"
      >
        <h2 class="text-3xl font-bold">댓글</h2>
        <RouterLink
          :to="{ name: 'NoticeArticle', params: { id: $route.params.id } }"
          ><vue-feather type="x"></vue-feather
        ></RouterLink>
      </div>
      <div class="overflow-scroll divide-y divide-gray-200">
        <div class="p-3 w-full">asdf</div>
        <div class="p-3 w-full">asdf</div>
        <div class="p-3 w-full">asdf</div>
      </div>
    </div>
  </div>
</template>
