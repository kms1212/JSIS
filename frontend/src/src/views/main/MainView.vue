<script>
import { defineAsyncComponent } from "vue";
import { RouterLink } from "vue-router";
import carouselTest1 from "@/assets/img/carouseltest1.png";
import carouselTest2 from "@/assets/img/carouseltest2.png";
import { getProfile } from "@/scripts/api/profile.js";
import { getNoticeArticleList } from "@/scripts/api/notice.js";
import { getMeal } from "@/scripts/api/meal.js";
import moment from "moment";

export default {
  name: "MainView",
  components: {
    CarouselComp: defineAsyncComponent(() =>
      import("@/components/CarouselComp.vue")
    ),
    RouterLink,
  },
  data() {
    return {
      images: [
        { url: carouselTest1, link: "/", alt: "NoticeImage" },
        { url: carouselTest2, link: "/class", alt: "NoticeImage" },
      ],
      user: {},
      notices: {},
      mealdata: null,
      currenttime: moment().format("YYYY-MM-DD HH:mm:ss"),
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

    getNoticeArticleList({ count: 5 })
      .then((response) => {
        this.notices = response;
      })
      .catch((error) => {
        console.error(error);
      });

    getMeal({ mdate: '221227', mtime: 2 })
      .then((response) => {
        this.mealdata = response;
      })
      .catch((error) => {
        console.error(error);
      });

    setInterval(() => {
      this.currenttime = moment().format("YYYY-MM-DD HH:mm:ss");
    }, 1000);
  },
  computed: {
    getMealDateStr() {
      if (!this.mealdata) return "";

      const date = String(this.mealdata.serve_date);
      return `20${date.slice(0, 2)}/${date.slice(2, 4)}/${date.slice(4, 6)}`;
    },
    getMealTimeStr() {
      if (!this.mealdata) return "";

      switch (this.mealdata.serve_time) {
        case 1:
          return "조식";
        case 2:
          return "중식";
        case 3:
          return "석식";
        default:
          return "";
      }
    },
  },
};
</script>

<template>
  <div
    id="main-view"
    class="space-y-4 gap-4 sm:grid sm:grid-cols-2 sm:space-y-0 xl:grid-cols-4"
  >
    <div
      class="rounded-2xl bg-white w-full border-gray-200 h-64 border p-5 max-w-64"
    >
      <div v-if="!!mealdata">
        <div class="flex flex-col justify-between mb-1">
          <span class="text-2xl font-semibold">급식</span>
          <span class="text-sm">{{ getMealDateStr }} 중식</span>
        </div>
        <ul class="overflow-y-scroll text-base">
          <li v-for="menu in mealdata.menus" :key="menu">{{ menu.name }}</li>
        </ul>
      </div>
      <div class="text-center h-full" v-else>
        <span class="text-sm">급식 정보가 없습니다.</span>
      </div>
    </div>
    <div
      class="col-span-1 rounded-2xl bg-white w-full border-gray-200 border p-5 flex flex-col items-center xl:order-3"
    >
      <div class="w-full h-full flex-1 flex items-center">
        <span class="text-2xl font-bold w-full text-center">{{
          currenttime
        }}</span>
      </div>
      <div class="w-full h-full flex-1 flex items-center">
        <span class="text-2xl font-bold w-full text-center"
          >2025 수능 D-662</span
        >
      </div>
    </div>
    <div
      class="col-span-2 sm:col-span-3 h-48 xl:h-full overflow-hidden rounded-2xl bg-white w-full border-gray-200 border"
    >
      <CarouselComp :images="images" />
    </div>
    <div
      class="col-span-3 grid sm:grid-cols-2 divide-gray-300/50 rounded-2xl bg-white w-full border-gray-200 border p-5 gap-4"
    >
      <div>
        <h2>
          <RouterLink to="/notice" class="text-xl font-bold"
            >공지사항</RouterLink
          >
        </h2>
        <ul class="divide-y py-2" v-if="notices.list">
          <li v-for="notice in notices.list" v-bind:key="notice">
            <RouterLink
              v-if="notice"
              :to="{
                name: 'NoticeArticle',
                params: { id: notice.articleid },
              }"
              class="py-2 flex justify-between items-center"
            >
              <span class="text-base">{{ notice.title }}</span>
              <span class="text-sm flex items-center">
                <vue-feather type="user" size=".75rem"></vue-feather>
                <span>{{ notice.views }}</span>
                &nbsp;
                <vue-feather type="thumbs-up" size=".75rem"></vue-feather>
                <span>{{ notice.likes_count }}</span>
                &nbsp;
                <vue-feather type="message-square" size=".75rem"></vue-feather>
                <span>{{ notice.replies_count }}</span>
              </span>
            </RouterLink>
            <span v-if="!notice" class="block h-[40px]"></span>
          </li>
        </ul>
      </div>
      <div>
        <h2 class="text-xl font-bold">커뮤니티 인기글</h2>
        <ul class="divide-y py-2">
          <li v-for="idx in 5" v-bind:key="idx">
            <RouterLink
              to="/notice/1"
              class="py-2 flex justify-between items-center"
            >
              <span class="text-base">게시물{{ idx }}</span>
              <span class="text-sm flex items-center">
                <vue-feather type="thumbs-up" size=".75rem"></vue-feather>
                <span>23</span>
                &nbsp;
                <vue-feather type="message-square" size=".75rem"></vue-feather>
                <span>23</span>
              </span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
