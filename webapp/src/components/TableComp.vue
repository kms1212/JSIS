<script>
import { RouterLink } from "vue-router";

export default {
  name: "TableComp",
  components: {
    RouterLink,
  },
  props: {
    columns: {
      type: Array,
      required: true,
    },
    getRows: {
      type: Function,
      required: true,
    },
  },
  created() {
    this.getPage({
      page: 1,
    });
  },
  methods: {
    getPage(options) {
      this.getRows(options)
        .then((rows) => {
          this.rows = rows;
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
  data() {
    return {
      rows: null,
      keyword: "",
    };
  },
  computed: {
    colratiosum() {
      return this.columns.reduce((acc, cur) => acc + cur.ratio, 0);
    },
  }
};
</script>

<template>
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
          <tr class="flex flex-row">
            <th v-for="column in columns" :key="column" scope="col" :style="'flex-basis: ' + column.ratio / colratiosum * 100 + '%;'" class="px-3 py-3 hidden sm:table-cell">{{ column.label }}</th>
          </tr>
        </thead>
        <tbody class="text-base" v-if="rows">
          <tr
            v-for="row in rows.data"
            :key="row"
            class="bg-white border-b hover:bg-gray-50 cursor-pointer"
            @click="goToArticle(row.id)"
          >
            <td scope="row" class="px-6 py-4 hidden sm:table-cell">
              {{ row.id }}
            </td>
            <td
              class="px-3 py-4 xl:w-[55%] text-gray-900 whitespace-nowrap"
            >
              {{ row.name }}
            </td>
            <td class="px-3 py-4 hidden sm:table-cell">
              {{ row.date }}
            </td>
            <td class="px-3 py-4 hidden sm:table-cell">
              {{ row.status }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <nav
      class="overflow-x-scroll flex items-center justify-between pt-4"
      aria-label="Table navigation"
      v-if="rows"
    >
      <span class="hidden sm:block text-sm font-normal text-gray-500"
        ><span class="font-semibold text-gray-900">{{
          rows.total
        }}</span
        >개 중
        <span class="font-semibold text-gray-900"
          >{{ rows.count }}</span
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
        <li v-for="pagenum in rows.pages" :key="pagenum">
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
</template>
