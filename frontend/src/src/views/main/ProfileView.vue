<script>
import { RouterLink, RouterView } from "vue-router";
import { defineAsyncComponent } from "vue";
import { getProfile } from "@/scripts/api/profile.js";
import { getSimplifiedTimestamp } from "@/scripts/time";

export default {
  name: "ProfileView",
  components: {
    RouterLink,
    RouterView,
    ProfileImageComp: defineAsyncComponent(() =>
      import("@/components/ProfileImageComp.vue")
    ),
  },
  data() {
    return {
      user: {},
      isSelfProfile: false,
    };
  },
  created() {
    this.isSelfProfile = !this.$route.params.id;

    getProfile()
      .then((profile) => {
        this.user = profile;
      })
      .catch((error) => {
        console.error(error);
      });

    if (this.$route.params.id) {
      getProfile({ userid: this.$route.params.id })
        .then((profile) => {
          if (profile.userid === this.user.userid) {
            this.isSelfProfile = true;
          } else {
            this.user = profile;
          }
        })
        .catch((error) => {
          console.error(error);
        });
    }
  },
  computed: {
    currentRoute() {
      return this.$route.name;
    },
  },
  methods: {
    simplifyTimestamp(timestamp) {
      return getSimplifiedTimestamp(timestamp);
    },
  },
};
</script>

<template>
  <div>
    <div
      class="rounded-2xl bg-white w-full border-gray-200 border p-5 flex flex-col sm:flex-row space-x-4 max-w-4xl mx-auto"
    >
      <div class="flex flex-col space-y-4">
        <div class="flex justify-center w-full sm:w-fit">
          <ProfileImageComp
            class="sm:h-56 sm:w-56 sm:m-6 w-full h-full max-w-xs"
          ></ProfileImageComp>
        </div>
        <span class="text-xl font-bold">
          {{ user.visiblename }} @{{ user.username }}
        </span>
        <ul
          class="flex flex-row justify-between space-x-2"
          v-if="!isSelfProfile"
        >
          <li
            class="flex-grow bg-gray-100 rounded-md p-2 text-center hover:bg-gray-200 duration-200"
          >
            <span class="text-sm">팔로우</span>
          </li>
          <li
            class="flex-grow bg-gray-100 rounded-md p-2 text-center hover:bg-gray-200 duration-200"
          >
            <span class="text-sm">차단</span>
          </li>
          <li
            class="bg-gray-100 rounded-md p-2 text-center hover:bg-gray-200 duration-200"
          >
            <vue-feather type="flag" class="h-5 w-5 -mb-1"></vue-feather>
          </li>
        </ul>
        <ul class="flex flex-row space-x-2" v-else>
          <li
            class="flex-grow bg-gray-100 rounded-md p-2 text-center hover:bg-gray-200 duration-200"
          >
            <span class="text-sm">프로필 수정</span>
          </li>
        </ul>
        <ul>
          <li class="text-xl font-bold"></li>
          <li v-if="!!user.email">{{ user.email }}</li>
          <li v-if="!!user.studentid">{{ user.studentid }}</li>
          <li class="rounded-md bg-gray-100 p-3 text-sm">
            {{ !!user.description ? user.description : "설명이 없습니다." }}
          </li>
          <li>가입: {{ simplifyTimestamp(user.date_joined) }}</li>
          <li>마지막 로그인: {{ simplifyTimestamp(user.date_lastlogin) }}</li>
          <li>
            <div class="flex justify-between mb-1">
              <span class="text-base">8GB 중 2GB 사용</span>
              <span class="text-sm">25%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
              <div
                class="bg-blue-600 h-2.5 rounded-full"
                style="width: 25%"
              ></div>
            </div>
          </li>
        </ul>
      </div>
      <div class="flex-grow flex flex-col">
        <nav class="border-b border-gray-200 w-full">
          <ul>
            <li class="float-left mr-4">
              <RouterLink
                to=""
                class="flex content-center p-2 hover:bg-gray-100 transition-colors duration-200 rounded-t-md border-b-2"
                :class="{
                  'border-blue-600': currentRoute.includes('Posts'),
                  'border-transparent': !currentRoute.includes('Posts'),
                }"
              >
                <span>게시물</span>
              </RouterLink>
            </li>
            <li v-if="isSelfProfile" class="float-left mr-4">
              <RouterLink
                to=""
                class="flex content-center p-2 hover:bg-gray-100 transition-colors duration-200 rounded-t-md border-b-2"
                :class="{
                  'border-blue-600': currentRoute.includes('Security'),
                  'border-transparent': !currentRoute.includes('Security'),
                }"
              >
                <span>보안</span>
              </RouterLink>
            </li>
            <li v-if="isSelfProfile" class="float-left mr-4">
              <RouterLink
                to=""
                class="flex content-center p-2 hover:bg-gray-100 transition-colors duration-200 rounded-t-md border-b-2"
                :class="{
                  'border-blue-600': currentRoute.includes('Drive'),
                  'border-transparent': !currentRoute.includes('Drive'),
                }"
              >
                <span>드라이브</span>
              </RouterLink>
            </li>
            <li v-if="isSelfProfile" class="float-left mr-4">
              <RouterLink
                to=""
                class="flex content-center p-2 hover:bg-gray-100 transition-colors duration-200 rounded-t-md border-b-2"
                :class="{
                  'border-blue-600': currentRoute.includes('Settings'),
                  'border-transparent': !currentRoute.includes('Settings'),
                }"
              >
                <span>설정</span>
              </RouterLink>
            </li>
          </ul>
        </nav>
        <RouterView></RouterView>
      </div>
    </div>
  </div>
</template>
