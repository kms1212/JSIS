<script>
import CarouselComp from "@/components/CarouselComp.vue";
import TableComp from "@/components/TableComp.vue";
import carouselTest1 from "@/assets/img/carouseltest1.png";
import carouselTest2 from "@/assets/img/carouseltest2.png";
import { getNoticeArticleList } from "@/scripts/api/notice.js";
import { getSimplifiedTimestamp } from "@/scripts/time";

export default {
  name: "NoticeView",
  components: {
    CarouselComp,
    TableComp,
  },
  data() {
    return {
      images: [
        { url: carouselTest1, link: "/", alt: "NoticeImage" },
        { url: carouselTest2, link: "/class", alt: "NoticeImage" },
      ],
      table_cols: [
        {
          label: "#",
          key: "articleid",
          ratio: 1,
          class: "font-semibold text-black",
        },
        { label: "제목", key: "title", ratio: 9 },
        {
          label: "작성자",
          get: (row) => {
            console.log(row.author.visiblename);
            return row.author.visiblename;
          },
          ratio: 3,
        },
        { label: "조회수", key: "views", ratio: 2 },
        { label: "댓글", key: "replies_count", ratio: 2 },
        { label: "좋아요", key: "likes_count", ratio: 2 },
        {
          label: "작성일",
          get: (row) => {
            return getSimplifiedTimestamp(row.created);
          },
          ratio: 5,
        },
      ],
      table_rows: {},
    };
  },
  methods: {
    goToArticle(article) {
      this.$router.push("/notice/" + article.articleid);
    },
    getPage(option) {
      getNoticeArticleList(option)
        .then((response) => {
          this.table_rows = response;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  computed: {},
};
</script>

<template>
  <div class="grid grid-cols-1 gap-4 px-4">
    <div
      class="rounded-2xl bg-white w-full border-gray-200 border h-40 xl:h-48 overflow-hidden"
    >
      <CarouselComp :images="images" />
    </div>
    <div class="rounded-2xl bg-white w-full border-gray-200 border p-5">
      <TableComp
        :columns="table_cols"
        :rows="table_rows"
        @reloadRequired="getPage"
        @rowClicked="goToArticle"
      ></TableComp>
    </div>
  </div>
</template>
