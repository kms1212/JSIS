<script>
import { defineAsyncComponent } from "vue";
import {
  getCommunityArticleList,
  getCommunityArticle,
} from "@/scripts/api/community.js";
import { getFile, readFileAsDataURL } from "@/scripts/api/file.js";

export default {
  name: "CommunityForumView",
  components: {
    MarkdownComp: defineAsyncComponent(() =>
      import("@/components/MarkdownComp.vue")
    ),
    ProfileImageComp: defineAsyncComponent(() =>
      import("@/components/ProfileImageComp.vue")
    ),
  },
  data() {
    return {
      posts: {},
      postDetails: {},
      postStatus: {},
      postidalloc: 1,
    };
  },
  created() {
    this.getPage({ page: 1, size: 5 });
  },
  methods: {
    checkPostVisibilities() {
      for (let i = 1; i <= Object.keys(this.posts).length; i++) {
        const refid = "post" + i;
        let post = this.$refs[refid][0];
        this.setPostStatus(post, refid);
      }
    },
    setPostStatus(el, refid) {
      var rect = el.getBoundingClientRect();
      if (
        rect.top <=
          (window.innerHeight || document.documentElement.clientHeight) &&
        rect.bottom >= 0
      ) {
        // if element is in viewport
        if (!this.postStatus[refid]) {
          this.onPostShown(refid, this.posts[refid].articleid);
          this.postStatus[refid] = true;
        }
      } else {
        if (this.postStatus[refid]) {
          this.onPostShown(refid, this.posts[refid].articleid);
          delete this.postStatus[refid];
        }
      }
    },
    async onPostShown(refid, articleid) {
      if (!this.postDetails[refid]) {
        const article = await getCommunityArticle(articleid);

        if (article.type === 0 && !!article.files) {
          const file = await getFile(article.files[0]);
          const dataurl = await readFileAsDataURL(file);

          article.files_data = [];
          article.files_data[0] = dataurl;
        }

        this.postDetails[refid] = article;
      }
    },
    onPostHidden() {
      // refid, articleid
      return; // TODO: Implement
    },
    async getPage(option) {
      const articlelist = await getCommunityArticleList(option);

      for (const post in articlelist.list) {
        this.posts["post" + this.postidalloc] = articlelist.list[post];
        this.postidalloc++;
      }
      this.$nextTick(() => {
        this.checkPostVisibilities();
      });
    },
  },
};
</script>

<template>
  <div
    @scroll="checkPostVisibilities"
    class="flex flex-row justify-between gap-4"
  >
    <div class="gap-4 w-full place-items-center space-y-4">
      <div v-for="idx in Object.keys(posts).length" :key="idx">
        <div
          v-if="posts['post' + idx].type === 0"
          :ref="'post' + idx"
          class="w-10/12 max-w-lg mx-auto overflow-hidden border border-gray-200"
        >
          <div class="relative group">
            <img
              class="w-full aspect-square"
              v-if="
                !!postDetails['post' + idx] &&
                !!postDetails['post' + idx].files_data
              "
              :src="postDetails['post' + idx].files_data[0]"
            />
          </div>
          <div class="w-full p-3 bg-white space-y-3">
            <div class="flex flex-row justify-between mb-2">
              <div class="flex flex-row space-x-3">
                <vue-feather type="thumbs-up" size="1.5rem"></vue-feather>
                <vue-feather type="message-square" size="1.5rem"></vue-feather>
              </div>
              <h3 class="text-base font-semibold">
                {{ posts["post" + idx].title }}
              </h3>
              <div class="flex flex-row space-x-3">
                <vue-feather type="share-2" size="1.5rem"></vue-feather>
                <vue-feather type="more-horizontal" size="1.5rem"></vue-feather>
              </div>
            </div>
            <div class="flex flex-row space-x-2 place-items-center">
              <ProfileImageComp
                :userid="posts['post' + idx].author.userid"
                class="w-8 h-8"
              />
              <span class="text-sm lg:text-base space-y-1">
                {{ posts["post" + idx].author.visiblename }} @{{
                  posts["post" + idx].author.username
                }}
                <span class="text-xs block tracking-widest">2시간 전</span>
              </span>
            </div>
            <MarkdownComp
              v-if="!!postDetails['post' + idx]"
              :document="postDetails['post' + idx].document"
              class="text-sm"
            />
            <span class="text-sm font-bold">댓글 보기</span>
          </div>
        </div>
        <div
          v-else
          :ref="'post' + idx"
          class="p-3 w-10/12 max-w-lg mx-auto overflow-hidden border border-gray-200 bg-white space-y-2"
        >
          <div class="flex flex-row justify-between mb-2">
            <h3 class="text-lg font-semibold">
              {{ posts["post" + idx].title }}
            </h3>
            <div class="flex flex-row space-x-3">
              <vue-feather type="thumbs-up" size="1.5rem"></vue-feather>
              <vue-feather type="message-square" size="1.5rem"></vue-feather>
              <vue-feather type="share-2" size="1.5rem"></vue-feather>
              <vue-feather type="more-horizontal" size="1.5rem"></vue-feather>
            </div>
          </div>
          <div class="flex flex-row space-x-2 place-items-center">
            <ProfileImageComp
              :userid="posts['post' + idx].author.userid"
              class="w-8 h-8"
            />
            <span class="text-sm lg:text-base space-y-1">
              {{ posts["post" + idx].author.visiblename }} @{{
                posts["post" + idx].author.username
              }}
              <span class="text-xs block tracking-widest">2시간 전</span>
            </span>
          </div>
          <MarkdownComp
            v-if="!!postDetails['post' + idx]"
            :document="postDetails['post' + idx].document"
            class="text-sm"
          />
          <span class="text-sm font-bold">댓글 보기</span>
        </div>
      </div>
    </div>
    <div class="hidden lg:block w-64 xl:w-96">
      <div class="rounded-2xl bg-white border-gray-200 border p-5">asdf</div>
    </div>
  </div>
</template>
