<script>
import { RouterLink } from "vue-router";
import { defineAsyncComponent } from "vue";
import { getProfile } from "@/scripts/api/profile.js";

export default {
  name: "ProfileView",
  components: {
    RouterLink,
    ProfileImageComp: defineAsyncComponent(() =>
      import("@/components/ProfileImageComp.vue")
    ),
  },
  data() {
    return {
      user: {},
    };
  },
  created() {
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
  <div>
    <div
      class="rounded-2xl bg-white w-full border-gray-200 border p-5 flex flex-row space-x-4"
    >
      <div class="flex flex-col space-y-4">
        <ProfileImageComp class="h-48 w-48"></ProfileImageComp>
        <ul>
          <li class="text-xl font-bold">
            {{ user.visiblename }} @{{ user.username }}
          </li>
          <li>{{ user.email }}</li>
          <li class="rounded-md bg-gray-100 p-3 text-sm">
            {{ !!user.description ? user.description : "설명이 없습니다." }}
          </li>
        </ul>
      </div>
      <div class="flex-grow flex flex-col">
        <nav class="border-b border-gray-200 pb-2">
          <ul class="flex flex-row space-x-4">
            <li>
              <RouterLink
                to=""
                class="flex content-center p-2 hover:bg-gray-100 transition-colors duration-200 rounded-md"
              >
                <span>기본 정보</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to=""
                class="flex content-center p-2 hover:bg-gray-100 transition-colors duration-200 rounded-md"
              >
                <span>보안</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to=""
                class="flex content-center p-2 hover:bg-gray-100 transition-colors duration-200 rounded-md"
              >
                <span>드라이브</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to=""
                class="flex content-center p-2 hover:bg-gray-100 transition-colors duration-200 rounded-md"
              >
                <span>설정</span>
              </RouterLink>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>
