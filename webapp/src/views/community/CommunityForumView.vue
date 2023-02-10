<script>
export default {
  name: "CommunityForumView",
};
</script>

<template>
  <div class="flex flex-row justify-between gap-4">
    <div
      class="gap-4 w-full place-items-center divide-y divide-gray-300/50 space-y-4"
    >
      <div
        v-for="idx in 10"
        v-bind:key="idx"
        class="divide-y divide-gray-300/50 w-10/12 max-w-lg mx-auto overflow-hidden border border-gray-200"
      >
        <div class="relative group">
          <img
            class="w-full aspect-square"
            src="@/assets/img/forumimgtest.png"
          />
        </div>
        <div class="w-full p-3 bg-white space-y-3">
          <div class="flex flex-row justify-between mb-2">
            <div class="flex flex-row space-x-3">
              <vue-feather type="thumbs-up" size="1.5rem"></vue-feather>
              <vue-feather type="message-square" size="1.5rem"></vue-feather>
            </div>
            <h3 class="text-base font-semibold">게시물 제목</h3>
            <div class="flex flex-row space-x-3">
              <vue-feather type="share-2" size="1.5rem"></vue-feather>
              <vue-feather type="more-horizontal" size="1.5rem"></vue-feather>
            </div>
          </div>
          <span class="text-sm lg:text-base space-y-1">
            권민수 @kms1212
            <span class="text-xs block tracking-widest">2시간 전</span>
          </span>
          <p class="text-sm">게시물 내용</p>
          <span class="text-sm font-bold">댓글 보기</span>
        </div>
      </div>
    </div>
    <div class="hidden lg:block w-64 xl:w-96">
      <div class="rounded-2xl bg-white border-gray-200 border p-5">asdf</div>
    </div>
  </div>
</template>
