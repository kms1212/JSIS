<script>
import APIAuth from "@/scripts/api/auth.js";

export default {
  name: "App",
  created() {
    APIAuth.restoreToken();
  },
};
</script>

<template>
  <RouterView></RouterView>
</template>
