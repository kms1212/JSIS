import { instance } from "@/scripts/api/axios.js";
import { useAuthStore } from "@/scripts/api/axios.js";
import { getFile, readFileAsDataURL } from "@/scripts/api/file.js";

export async function getProfile(cache = true) {
  const authStore = useAuthStore();

  if (!cache || !authStore.getProfile) {
    const response = await instance.get("/auth/user/");

    if (response.status == 200) {
      authStore.setProfile(response.data);
    }
  }

  return authStore.profile;
}

export async function getProfileImage() {
  const authStore = useAuthStore();

  if (!authStore.profile) {
    await getProfile();
  }

  const profile = authStore.profile;

  if (profile.profileimage) {
    if (!authStore.profileimage) {
      const response = await getFile(profile.profileimage);

      const file = new File([response], "profileimage", {
        type: profile.profileimage.mimetype,
      });
      let resultdata = await readFileAsDataURL(file);

      authStore.setProfileImage(resultdata);
    }

    return authStore.profileimage;
  } else {
    return null;
  }
}
