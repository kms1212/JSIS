<script>
import { RouterView } from "vue-router";
import { getProfile } from "@/scripts/api/profile.js";
import APIAuth from "@/scripts/api/auth.js";

export default {
  name: "AuthBaseView",
  components: {
    RouterView,
  },
  created() {
    getProfile(false)
      .then(() => {
        // this.$router.push({ name: "Main" });
        console.log("asdf");
      })
      .catch(() => {
        APIAuth.removeToken();
        APIAuth.removeProfile();
      });
  },
};
</script>

<template>
  <div
    class="relative flex min-h-screen flex-col justify-center overflow-scroll bg-gray-50 py-6 sm:py-12"
  >
    <div
      class="relative bg-white px-6 pt-10 pb-8 shadow-xl ring-1 ring-gray-900/5 sm:mx-auto sm:rounded-lg sm:px-10 sm:min-w-max"
    >
      <div class="mx-auto">
        <header class="">
          <img
            class="block max-h-14 sm:h-14 object-cover mx-auto"
            src="@/assets/img/site_logo_alpha.png"
            alt="JSIS"
          />
        </header>
        <RouterView class="space-y-6 py-8 text-base leading-7 text-black" />
      </div>
    </div>
  </div>
</template>
