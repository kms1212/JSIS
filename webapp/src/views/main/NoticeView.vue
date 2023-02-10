<script>
import CarouselComp from "@/components/CarouselComp.vue";
import carouselTest1 from "@/assets/img/carouseltest1.png";
import carouselTest2 from "@/assets/img/carouseltest2.png";
import { getNoticeArticleList } from "@/scripts/api/notice.js";

export default {
  name: "ClassMainView",
  components: {
    CarouselComp,
  },
  created() {
    this.getPage(1);
  },
  data() {
    return {
      images: [
        { url: carouselTest1, link: "/", alt: "NoticeImage" },
        { url: carouselTest2, link: "/class", alt: "NoticeImage" },
      ],
      articles: {},
      keyword: "",
    };
  },
  methods: {
    goToArticle(id) {
      this.$router.push("/notice/" + id);
    },
    getPage(page) {
      getNoticeArticleList({ page: page })
        .then((response) => {
          this.articles = response;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    nextPage() {
      if (this.articles.page < this.articles.pages) {
        this.getPage(this.articles.page + 1);
      }
    },
    prevPage() {
      if (this.articles.page > 1) {
        this.getPage(this.articles.page - 1);
      }
    },
    search() {
      if (this.keyword === "") {
        this.getPage(1);
        return;
      }

      getNoticeArticleList({ search: this.keyword })
        .then((response) => {
          this.articles = response;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  computed: {
    articleIndexStart() {
      return (this.articles.page - 1) * this.articles.count + 1;
    },
    articleIndexEnd() {
      if (this.articles.page === this.articles.pages)
        return this.articles.total;
      else return this.articles.page * this.articles.count;
    },
  },
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
      <div class="relative">
        <div class="flex flex-col sm:flex-row justify-between">
          <h3 class="text-2xl font-semibold">공지사항</h3>
          <div class="flex items-center justify-between pb-4">
            <label for="table-search" class="sr-only">검색</label>
            <div class="relative">
              <div
                class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"
              >
                <vue-feather
                  type="search"
                  size="1rem"
                  class="text-gray-500"
                ></vue-feather>
              </div>
              <input
                type="text"
                id="table-search"
                class="block p-2 pl-10 text-sm border-b border-b-gray-200 focus:border-b-blue-600 focus:border-b-2 transition-all outline-none"
                placeholder="검색하기"
                v-model="keyword"
                @keyup.enter="search"
              />
            </div>
          </div>
        </div>
        <div
          class="relative overflow-x-auto rounded-2xl border border-gray-200"
        >
          <table class="w-full text-left text-gray-500">
            <thead
              class="hidden sm:table-header-group text-base text-gray-700 uppercase bg-gray-50"
            >
              <tr>
                <th scope="col" class="px-3 py-3 hidden sm:table-cell">#</th>
                <th scope="col" class="px-3 py-3">제목</th>
                <th scope="col" class="px-3 py-3 hidden sm:table-cell">
                  작성자
                </th>
                <th scope="col" class="px-3 py-3 hidden sm:table-cell">
                  조회수
                </th>
                <th scope="col" class="px-3 py-3 hidden sm:table-cell">댓글</th>
                <th scope="col" class="px-3 py-3 hidden sm:table-cell">
                  좋아요
                </th>
                <th scope="col" class="px-3 py-3 hidden lg:table-cell">
                  작성일
                </th>
              </tr>
            </thead>
            <tbody class="text-base" v-if="articles.articles">
              <tr
                v-for="article in articles.articles"
                :key="article.articleid"
                class="bg-white border-b hover:bg-gray-50 cursor-pointer"
                @click="goToArticle(article.articleid)"
              >
                <td scope="row" class="px-6 py-4 hidden sm:table-cell">
                  {{ article.articleid }}
                </td>
                <td
                  class="px-3 py-4 xl:w-[55%] text-gray-900 whitespace-nowrap"
                >
                  <span class="hidden sm:block font-medium">{{
                    article.title
                  }}</span>
                  <div class="block sm:hidden">
                    <div class="flex flex-col">
                      <span class="font-medium">{{ article.title }}</span>
                      <div class="flex flex-row justify-between">
                        <span class="text-sm font-medium text-gray-900">{{
                          article.author.username
                        }}</span>
                        <span class="text-sm flex items-center">
                          <vue-feather type="user" size=".75rem"></vue-feather>
                          <p>{{ article.views }}</p>
                          &nbsp;
                          <vue-feather
                            type="thumbs-up"
                            size=".75rem"
                          ></vue-feather>
                          <p>{{ article.likes_count }}</p>
                          &nbsp;
                          <vue-feather
                            type="message-square"
                            size=".75rem"
                          ></vue-feather>
                          <p>{{ article.replies_count }}</p>
                        </span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-3 py-4 hidden sm:table-cell">
                  {{ article.author.username }}
                </td>
                <td class="px-3 py-4 hidden sm:table-cell">
                  {{ article.views }}
                </td>
                <td class="px-3 py-4 hidden sm:table-cell">
                  {{ article.replies_count }}
                </td>
                <td class="px-3 py-4 hidden sm:table-cell">
                  {{ article.likes_count }}
                </td>
                <td class="px-3 py-4 hidden lg:table-cell">
                  {{ article.created }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <nav
          class="overflow-x-scroll flex items-center justify-between pt-4"
          aria-label="Table navigation"
        >
          <span class="hidden sm:block text-sm font-normal text-gray-500"
            ><span class="font-semibold text-gray-900">{{
              articles.total
            }}</span
            >개 중
            <span class="font-semibold text-gray-900"
              >{{ articleIndexStart }}-{{ articleIndexEnd }}</span
            >번째 게시물</span
          >
          <ul class="inline-flex items-center -space-x-px">
            <li>
              <div
                @click="prevPage"
                class="flex items-center px-3 py-2 ml-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-l-lg hover:bg-gray-100 hover:text-gray-700"
              >
                <span class="sr-only">Previous</span>
                <vue-feather
                  type="chevron-left"
                  class="w-5 h-5 my-auto"
                ></vue-feather>
              </div>
            </li>
            <li v-for="pagenum in articles.pages" :key="pagenum">
              <div
                @click="getPage(pagenum)"
                :class="
                  pagenum == articles.page
                    ? 'text-blue-600 border-blue-300 bg-blue-50 hover:bg-blue-100 hover:text-blue-700'
                    : 'text-gray-500 bg-white border-gray-300 hover:bg-gray-100 hover:text-gray-700'
                "
                class="px-3 py-2 leading-tight border"
              >
                {{ pagenum }}
              </div>
            </li>
            <li>
              <div
                @click="nextPage"
                class="flex items-center px-3 py-2 ml-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-r-lg hover:bg-gray-100 hover:text-gray-700"
              >
                <span class="sr-only">Next</span>
                <vue-feather
                  type="chevron-right"
                  class="w-5 h-5 my-auto"
                ></vue-feather>
              </div>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>
