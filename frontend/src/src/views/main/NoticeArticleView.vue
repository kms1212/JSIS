<script>
import { defineAsyncComponent } from "vue";
import { RouterLink, RouterView } from "vue-router";
import { getNoticeArticle, likeNoticeArticle } from "@/scripts/api/notice.js";

export default {
  name: "NoticeArticleView",
  components: {
    RouterLink,
    RouterView,
    MarkdownComp: defineAsyncComponent(() =>
      import("@/components/MarkdownComp.vue")
    ),
  },
  data() {
    return {
      article: {},
    };
  },
  created() {
    getNoticeArticle(this.$route.params.id)
      .then((article) => {
        this.article = article;
      })
      .catch((error) => {
        console.error(error);
      });
  },
  methods: {
    like() {
      likeNoticeArticle(this.$route.params.id)
        .then((response) => {
          this.article.likes_count = response.likes;
          this.article.liked = response.status === "LIKED";
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<template>
  <div class="grid grid-cols-1 gap-4 px-4">
    <div class="rounded-2xl bg-white w-full border-gray-200 border p-5">
      <div class="xl:px-20 py-4">
        <h1 v-if="article.title" class="text-4xl font-bold">
          {{ article.title }}
        </h1>
        <div
          class="flex flex-col xs:flex-row justify-between items-center mb-3"
        >
          <span v-if="article.author" class="text-sm text-gray-500">{{
            article.author.visiblename
          }}</span>
          <div class="flex flex-row items-center space-x-3">
            <span v-if="article.created" class="text-sm text-gray-500">{{
              article.created
            }}</span>

            <div class="hidden xs:flex flex-row items-center">
              <div @click="like" class="flex items-center">
                <vue-feather
                  type="thumbs-up"
                  stroke="#3B82F6"
                  :fill="article.liked ? '#3B82F6' : 'none'"
                  size="1.25rem"
                ></vue-feather>
                <span v-if="article.likes_count != null">{{
                  article.likes_count
                }}</span>
              </div>
              &nbsp;
              <RouterLink
                :to="{ name: 'Replies', params: { id: $route.params.id } }"
                class="flex items-center"
              >
                <vue-feather type="message-square" size="1.25rem"></vue-feather>
                <span v-if="article.replies_count != null">{{
                  article.replies_count
                }}</span>
              </RouterLink>
            </div>
          </div>
          <div class="flex flex-row items-center xs:hidden">
            <div @click="like" class="flex items-center">
              <vue-feather
                type="thumbs-up"
                stroke="#3B82F6"
                :fill="article.liked ? '#3B82F6' : 'none'"
                size="1.25rem"
              ></vue-feather>
              <span v-if="article.likes_count != null">{{
                article.likes_count
              }}</span>
            </div>
            &nbsp;
            <RouterLink
              :to="{ name: 'Replies', params: { id: $route.params.id } }"
              class="flex items-center"
            >
              <vue-feather type="message-square" size="1.25rem"></vue-feather>
              <span v-if="article.replies_count != null">{{
                article.replies_count
              }}</span>
            </RouterLink>
          </div>
        </div>
        <ul v-if="article.files_fileinfo">
          <li
            v-for="file in article.files_fileinfo"
            :key="file.fileid"
            class="flex flex-row items-center justify-between p-2 rounded-md hover:bg-gray-200"
          >
            <div class="flex flex-row items-center">
              <vue-feather type="file" size="1.25rem"></vue-feather>
              <a :href="file.url" class="text-sm text-gray-500 ml-2">{{
                file.filename
              }}</a>
            </div>
            <span class="text-sm text-gray-500">{{ file.data_size }}</span>
          </li>
        </ul>
      </div>
      <MarkdownComp
        :document="article.document"
        class="px-3 pb-10 w-full xl:w-9/12 mx-auto"
      ></MarkdownComp>
      <RouterView
        class="fixed left-0 top-0 w-full h-full flex min-h-screen flex-col justify-center overflow-scroll"
      ></RouterView>
    </div>
  </div>
</template>
