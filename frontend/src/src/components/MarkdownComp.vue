<script>
import "highlightjs/styles/github.css";

const MDRenderer = await import("@/scripts/MDRenderer.js");

export default {
  name: "MarkdownComp",
  props: {
    document: {
      type: String,
      default: "",
      required: true,
    },
  },
  computed: {
    getHtmlDocument() {
      if (this.document) {
        return MDRenderer.default.parse(this.document);
      } else {
        return "";
      }
    },
  },
};
</script>

<template>
  <article v-dompurify-html="getHtmlDocument" />
</template>
