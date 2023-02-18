<script>
import { defineAsyncComponent } from "vue";
import { getProfile } from "@/scripts/api/profile.js";

export default {
  name: "CommunityMainView",
  components: {
    ProfileImageComp: defineAsyncComponent(() =>
      import("@/components/ProfileImageComp.vue")
    ),
  },
  data() {
    return {
      user: {},
    };
  },
  mounted() {
    getProfile()
      .then((profile) => {
        this.user = profile;
      })
      .catch((error) => {
        console.error(error);
      });
  },
};
</script>

<template>
  <div class="grid lg:grid-cols-2 gap-4">
    <div
      class="divide-y sm:divide-y-0 divide-gray-300/50 grid sm:grid-cols-2 rounded-2xl bg-white w-full md:h-48 border-gray-200 border p-5"
    >
      <div class="flex flex-col space-y-2 justify-between pb-4 sm:pb-0">
        <div class="flex flex-row gap-3 items-center">
          <ProfileImageComp class="h-16 w-16"></ProfileImageComp>
          <p class="text-xl font-medium">
            {{ user.visiblename }}
            <span class="text-base block tracking-widest">
              {{ user.studentid }} @{{ user.username }}
            </span>
            <span class="text-base block tracking-widest"> Ⓣ 0 </span>
          </p>
        </div>
        <span>📮 받은 쪽지가 없습니다.</span>
        <div class="w-full flex justify-between pr-4 text-sm">
          <span>게시물 {{ user.post_count }}개</span>
          <span>댓글 {{ user.reply_count }}개</span>
        </div>
      </div>
      <div class="pt-4 sm:pt-0 sm:pl-4">
        <p>받은 경고나 제재가 없습니다.</p>
      </div>
    </div>
    <RouterLink
      to="/community/forum"
      class="rounded-2xl bg-white w-full overflow-hidden border-gray-200 border p-5 h-32 md:h-48 items-center lg:order-3 relative"
    >
      <img
        src="@/assets/img/community_menu_forum.png"
        alt=""
        class="absolute right-0 bottom-0 h-full"
      />
      <span class="text-2xl font-extralight">게시판</span>
    </RouterLink>
    <a
      href="{% url 'webappcommunity:forum' %}"
      class="rounded-2xl bg-white w-full overflow-hidden border-gray-200 border p-5 h-32 md:h-48 items-center lg:order-3 relative"
    >
      <img
        src="@/assets/img/community_menu_anon_forum.png"
        alt=""
        class="absolute right-0 bottom-0 h-full"
      />
      <span class="text-2xl font-extralight">익명 게시판</span>
    </a>
    <a
      href="{% url 'webappcommunity:forum' %}"
      class="rounded-2xl bg-white w-full overflow-hidden border-gray-200 border p-5 h-32 md:h-48 items-center lg:order-3 relative"
    >
      <img
        src="@/assets/img/community_menu_game.png"
        alt=""
        class="absolute right-0 bottom-0 h-full"
      />
      <span class="text-2xl font-extralight">게임</span>
    </a>
    <a
      href="{% url 'webappcommunity:forum' %}"
      class="rounded-2xl bg-white w-full overflow-hidden border-gray-200 border p-5 h-32 md:h-48 items-center lg:order-3 relative"
    >
      <img
        src="@/assets/img/community_menu_preparing.png"
        alt=""
        class="absolute right-0 bottom-0 h-full"
      />
      <span class="text-2xl font-extralight">준비중</span>
    </a>
  </div>
</template>
