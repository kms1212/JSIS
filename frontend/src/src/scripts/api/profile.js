import { instance } from "@/scripts/api/axios.js";
import { useAuthStore } from "@/scripts/api/axios.js";

export async function getProfile(options = {}) {
  if (options.userid) {
    console.log(options.userid);
    const response = await instance.get("/auth/user/", {
      params: {
        userid: options.userid,
      },
    });

    if (response.status === 200) {
      return response.data;
    }
  } else {
    const authStore = useAuthStore();

    if (!options.cache || !authStore.getProfile) {
      const response = await instance.get("/auth/user/");

      if (response.status === 200) {
        authStore.setProfile(response.data);
      }
    }

    return authStore.profile;
  }
}
