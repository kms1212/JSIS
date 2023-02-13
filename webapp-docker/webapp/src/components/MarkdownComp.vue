<script>
import MDRenderer from "@/scripts/MDRenderer.js";
import "highlightjs/styles/github.css";

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
        return MDRenderer.parse(this.document);
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
