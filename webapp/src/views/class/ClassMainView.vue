<script>
import TableComp from "@/components/TableComp.vue";

export default {
  name: "ClassMainView",
  components: {
    TableComp,
  },
  data() {
    return {
      table_cols: [
        { label: '#', ratio: 1 },
        { label: 'name', ratio: 7 },
        { label: 'date', ratio: 3 },
        { label: 'status', ratio: 3 },
      ],
      table_row_info: {
        page: 1,
        pages: 1,
        total: 18,
        count: 18,
        rows: [
          { id: 1, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 2, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 3, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 4, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 5, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 6, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 7, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 8, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 9, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 10, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 11, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 12, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 13, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 14, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 15, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 16, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 17, name: 'asdf', date: '2021-01-01', status: 'asdf' },
          { id: 18, name: 'asdf', date: '2021-01-01', status: 'asdf' },
        ]
      }
    }
  },
  methods: {
    getRows(options) {
      return new Promise((resolve, reject) => {
        resolve(this.table_rows_info);
      });
    }
  }
};
</script>

<template>
  <div class="space-y-4 px-4">
    <div class="grid lg:grid-cols-2 gap-4">
      <div class="rounded-2xl bg-white w-full border-gray-200 border p-5">
        <TableComp :columns="table_cols" :getRows="getRows"></TableComp>
      </div>
      <div class="rounded-2xl bg-white w-full border-gray-200 border p-5">
        asdf
      </div>
    </div>
  </div>
</template>
