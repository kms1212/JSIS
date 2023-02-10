<script>
import { getProfileImage } from "@/scripts/api/profile.js";

export default {
  name: "ProfileImageComp",
  data() {
    return {
      profileimage: "",
    };
  },
  mounted() {
    getProfileImage()
      .then((profileimage) => {
        this.profileimage = profileimage;
      })
      .catch((error) => {
        console.error(error);
      });
  },
};
</script>

<template>
  <div class="rounded-full">
    <img
      v-if="profileimage"
      :src="profileimage"
      class="rounded-full"
      alt="Profile image"
    />
    <vue-feather
      v-if="!profileimage"
      type="user"
      class="rounded-full border border-gray-200 w-full p-[10%]"
    ></vue-feather>
  </div>
</template>
