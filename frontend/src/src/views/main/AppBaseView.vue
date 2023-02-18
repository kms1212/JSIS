<script>
import { defineAsyncComponent } from "vue";
import { RouterLink, RouterView } from "vue-router";
import APIAuth from "@/scripts/api/auth.js";
import { getProfile } from "@/scripts/api/profile.js";

export default {
  name: "AppBaseView",
  components: {
    ProfileImageComp: defineAsyncComponent(() =>
      import("@/components/ProfileImageComp.vue")
    ),
    RouterLink,
    RouterView,
  },
  data() {
    return {
      user: {},
      mobileMenu: false,
    };
  },
  created() {
    getProfile()
      .then((profile) => {
        this.user = profile;
      })
      .catch((e) => {
        console.log(e);
      });
  },
  methods: {
    toggleMobileMenu() {
      this.mobileMenu = !this.mobileMenu;
    },
    logout() {
      APIAuth.logout();
    },
  },
  computed: {
    currentRoute() {
      return this.$route.name;
    },
  },
};
</script>

<template>
  <div class="h-screen flex flex-col">
    <header
      class="h-20 bg-white p-4 md:mx-auto place-items-center w-full flex flex-row justify-between items-center"
    >
      <div class="flex flex-row gap-5 items-center">
        <RouterLink to="/">
          <img class="h-10" src="@/assets/img/site_logo_alpha.png" alt="JSIS" />
        </RouterLink>
      </div>
      <vue-feather type="menu" class="md:invisible" @click="toggleMobileMenu" />
    </header>
    <div class="h-[calc(100vh-5rem)]">
      <div class="flex flex-row h-full">
        <!-- Navigation for large devices (>md) -->
        <nav
          class="place-items-center lg:w-72 bg-white justify-between hidden md:flex flex-col p-3 pr-0"
        >
          <ul
            class="items-center space-y-1 justify-center text-lg font-semibold w-full"
          >
            <li>
              <RouterLink
                to="/"
                class="relative flex justify-center lg:justify-start p-3 hover:bg-gray-100 transition-colors duration-200"
                :class="{
                  'pr-6 bg-gray-100 w-[calc(100%+3px)] rounded-l-md text-black':
                    currentRoute === 'Main',
                  'mr-3 text-gray-600 rounded-md': currentRoute !== 'Main',
                }"
              >
                <vue-feather
                  type="home"
                  class="lg:mr-2 w-7 h-7 lg:w-6 lg:h-6"
                />
                <span class="hidden lg:block">메인</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/class"
                class="relative flex justify-center lg:justify-start p-3 hover:bg-gray-100 transition-colors duration-200"
                :class="{
                  'pr-6 bg-gray-100 w-[calc(100%+3px)] rounded-l-md text-black':
                    currentRoute === 'ClassMain',
                  'mr-3 text-gray-600 rounded-md': currentRoute !== 'ClassMain',
                }"
              >
                <vue-feather
                  type="briefcase"
                  class="lg:mr-2 w-7 h-7 lg:w-6 lg:h-6"
                />
                <span class="hidden lg:block">학급</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/meal"
                class="relative flex justify-center lg:justify-start p-3 hover:bg-gray-100 transition-colors duration-200"
                :class="{
                  'pr-6 bg-gray-100 w-[calc(100%+3px)] rounded-l-md text-black':
                    currentRoute === 'MealMain',
                  'mr-3 text-gray-600 rounded-md': currentRoute !== 'MealMain',
                }"
              >
                <vue-feather
                  type="coffee"
                  class="lg:mr-2 w-7 h-7 lg:w-6 lg:h-6"
                />
                <span class="hidden lg:block">급식정보</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/community"
                class="relative flex justify-center lg:justify-start p-3 hover:bg-gray-100 transition-colors duration-200"
                :class="{
                  'pr-6 bg-gray-100 w-[calc(100%+3px)] rounded-l-md text-black':
                    currentRoute === 'CommunityMain',
                  'mr-3 text-gray-600 rounded-md':
                    currentRoute !== 'CommunityMain',
                }"
              >
                <vue-feather
                  type="message-circle"
                  class="lg:mr-2 w-7 h-7 lg:w-6 lg:h-6"
                />
                <span class="hidden lg:block">커뮤니티</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/hq"
                class="relative flex justify-center lg:justify-start p-3 hover:bg-gray-100 transition-colors duration-200"
                :class="{
                  'pr-6 bg-gray-100 w-[calc(100%+3px)] rounded-l-md text-black':
                    currentRoute === 'HQMain',
                  'mr-3 text-gray-600 rounded-md': currentRoute !== 'HQMain',
                }"
              >
                <vue-feather
                  type="users"
                  class="lg:mr-2 w-7 h-7 lg:w-6 lg:h-6"
                />
                <span class="hidden lg:block">학생회</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/conv"
                class="relative flex justify-center lg:justify-start p-3 hover:bg-gray-100 transition-colors duration-200"
                :class="{
                  'pr-6 bg-gray-100 w-[calc(100%+3px)] rounded-l-md text-black':
                    currentRoute === 'ConvMain',
                  'mr-3 text-gray-600 rounded-md': currentRoute !== 'ConvMain',
                }"
              >
                <vue-feather
                  type="book"
                  class="lg:mr-2 w-7 h-7 lg:w-6 lg:h-6"
                />
                <span class="hidden lg:block">중앙하우스/탑서점</span>
              </RouterLink>
            </li>
          </ul>
          <div class="lg:flex gap-3 mr-3 items-center">
            <RouterLink
              to="/profile"
              class="hidden sm:flex flex-row space-x-3 p-3 rounded-md items-center hover:bg-gray-100"
            >
              <ProfileImageComp class="h-10 w-10"></ProfileImageComp>
              <p class="text-base font-medium hidden lg:block">
                {{ user.visiblename }}
                <span class="text-sm block tracking-widest">
                  {{ user.studentid }}
                </span>
              </p>
            </RouterLink>
            <div
              @click="logout"
              class="p-2 pb-1 rounded hover:bg-gray-200 text-center"
            >
              <vue-feather type="log-out"></vue-feather>
            </div>
          </div>
        </nav>
        <div
          class="w-full flex flex-col md:rounded-tl-2xl bg-gray-100 border-l border-gray-100"
        >
          <RouterView class="overflow-scroll p-4 md:p-8"></RouterView>
        </div>
      </div>
    </div>
  </div>
</template>
