<script>
export default {
  name: "TableComp",
  props: {
    columns: {
      type: Array,
      required: true,
    },
    rows: {
      type: Object,
      required: true,
    },
  },
  created() {
    this.getPage({
      page: 1,
    });
  },
  methods: {
    rowClicked(row) {
      this.$emit("rowClicked", row);
    },
    getPage(options) {
      if (this.keyword) {
        options.keyword = this.keyword;
      }

      this.$emit("reloadRequired", options);
    },
    nextPage() {
      if (this.rows.page < this.rows.pages) {
        this.getPage({ page: this.rows.page + 1 });
      }
    },
    prevPage() {
      if (this.rows.page > 1) {
        this.getPage({ page: this.rows.page - 1 });
      }
    },
  },
  data() {
    return {
      keyword: "",
    };
  },
  computed: {
    colratiosum() {
      return this.columns.reduce((acc, cur) => acc + cur.ratio, 0);
    },
  },
};
</script>

<template>
  <div class="relative">
    <div class="flex flex-col justify-between sm:flex-row">
      <h3 class="text-2xl font-semibold">공지사항</h3>
      <div class="flex items-center justify-between pb-4">
        <label for="table-search" class="sr-only">검색</label>
        <div class="relative">
          <div
            class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"
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
            class="border-b border-b-gray-200 p-2 pl-10 text-sm outline-none transition-all focus:border-b-2 focus:border-b-blue-600"
            placeholder="검색하기"
            v-model="keyword"
            @keyup.enter="search"
          />
        </div>
      </div>
    </div>
    <div class="relative overflow-x-auto rounded-2xl border border-gray-200">
      <table class="w-full text-left text-gray-500">
        <thead
          class="hidden bg-gray-50 text-base uppercase text-gray-700 sm:table-header-group"
        >
          <tr>
            <th
              v-for="column in columns"
              :key="column"
              scope="col"
              :style="
                !!column.ratio
                  ? 'width: ' + (column.ratio / colratiosum) * 100 + '%;'
                  : ''
              "
              class="hidden px-3 py-3 sm:table-cell"
            >
              {{ column.label }}
            </th>
          </tr>
        </thead>
        <tbody class="text-base" v-if="rows">
          <tr
            v-for="row in rows.list"
            :key="row"
            class="cursor-pointer border-b bg-white hover:bg-gray-50"
            @click="rowClicked(row)"
          >
            <td
              v-for="column in columns"
              :key="column"
              scope="row"
              :class="column.class"
              class="hidden px-3 py-4 sm:table-cell"
            >
              {{
                !!column.key
                  ? row[column.key]
                  : !!column.get
                  ? column.get(row)
                  : row[column.label]
              }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <nav
      class="flex items-center justify-between pt-4 overflow-x-scroll"
      aria-label="Table navigation"
      v-if="rows"
    >
      <span class="hidden text-sm font-normal text-gray-500 sm:block"
        ><span class="font-semibold text-gray-900">{{ rows.total }}</span
        >개 중 <span class="font-semibold text-gray-900">{{ rows.count }}</span
        >번째 게시물</span
      >
      <ul class="inline-flex items-center -space-x-px">
        <li>
          <div
            @click="prevPage"
            class="ml-0 flex items-center rounded-l-lg border border-gray-300 bg-white px-3 py-2 leading-tight text-gray-500 hover:bg-gray-100 hover:text-gray-700"
          >
            <span class="sr-only">Previous</span>
            <vue-feather
              type="chevron-left"
              class="my-auto w-5 h-5"
            ></vue-feather>
          </div>
        </li>
        <li v-for="pagenum in rows.pages" :key="pagenum">
          <div
            @click="getPage({ page: pagenum })"
            :class="
              pagenum == rows.page
                ? 'border-blue-300 bg-blue-50 text-blue-600 hover:bg-blue-100 hover:text-blue-700'
                : 'border-gray-300 bg-white text-gray-500 hover:bg-gray-100 hover:text-gray-700'
            "
            class="border px-3 py-2 leading-tight"
          >
            {{ pagenum }}
          </div>
        </li>
        <li>
          <div
            @click="nextPage"
            class="ml-0 flex items-center rounded-r-lg border border-gray-300 bg-white px-3 py-2 leading-tight text-gray-500 hover:bg-gray-100 hover:text-gray-700"
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
