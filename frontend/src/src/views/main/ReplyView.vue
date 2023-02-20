<script>
import { RouterLink } from "vue-router";
import { getReplyList } from "@/scripts/api/reply.js";
import { getSimplifiedTimestamp } from "@/scripts/time.js";
import { defineAsyncComponent } from "vue";

export default {
  name: "ReplyView",
  components: {
    RouterLink,
    ProfileImageComp: defineAsyncComponent(() =>
      import("@/components/ProfileImageComp.vue")
    ),
  },
  data() {
    return {
      replies: null,
    };
  },
  created() {
    getReplyList({ articleid: this.$route.params.id })
      .then((response) => {
        this.replies = response;
      })
      .catch((error) => {
        console.error(error);
      });
  },
  methods: {
    simplifyTimestamp(timestamp) {
      return getSimplifiedTimestamp(timestamp);
    },
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
      <ul class="overflow-scroll divide-y divide-gray-200" v-if="replies">
        <li
          class="p-3 w-full flex flex-row"
          v-for="reply in replies"
          :key="reply"
        >
          <div class="flex flex-row flex-grow space-x-2">
            <ProfileImageComp :userid="reply.author" class="w-10 h-10 mt-2" />
            <div>
              <span class="text-sm space-y-1">
                {{ reply.author.visiblename }} @{{ reply.author.username }}
                <vue-feather
                  type="check-circle"
                  class="h-3 w-3 text-green-500"
                ></vue-feather>
              </span>
              <br />
              <p>
                {{ reply.text }}
              </p>
              <span v-if="reply.reply_count" class="text-sm text-gray-500">
                댓글 {{ reply.reply_count }}개 보기
              </span>
            </div>
          </div>
          <div class="flex flex-col items-end justify-between space-x-1 mt-2">
            <div class="space-x-1">
              <vue-feather type="flag" class="h-5 w-5"></vue-feather>
              <vue-feather type="thumbs-up" class="h-5 w-5"></vue-feather>
            </div>
            <span class="text-sm text-gray-500">
              {{ simplifyTimestamp(reply.created) }}
            </span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
