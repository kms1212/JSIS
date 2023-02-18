<script>
import { getFile, readFileAsDataURL } from "../scripts/api/file";
import { getProfile } from "../scripts/api/profile";

export default {
  name: "ProfileImageComp",
  props: {
    userid: {
      type: Number,
      required: false,
    },
  },
  data() {
    return {
      profileimage: "",
    };
  },
  mounted() {
    const getProfileImage = async (id) => {
      const profile = await getProfile(id);
      const file = await getFile(profile.profileimage);
      const dataurl = await readFileAsDataURL(file);
      return dataurl;
    };

    if (!this.userid) {
      console.log("asf");
      getProfileImage()
        .then((file) => {
          this.profileimage = file;
        })
        .catch((error) => {
          console.error(error);
        });
    } else {
      getProfileImage(this.userid)
        .then((file) => {
          this.profileimage = file;
        })
        .catch((error) => {
          console.error(error);
        });
    }
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
      class="rounded-full border border-gray-200 w-full p-[10%] bg-white"
    ></vue-feather>
  </div>
</template>
