import { instance } from "@/scripts/api/axios.js";
import { useAuthStore } from "@/scripts/api/axios.js";
import { getFile } from "@/scripts/api/file.js";

export async function getProfile(cache = true) {
  const authStore = useAuthStore();

  if (!cache || !authStore.getProfile) {
    const response = await instance.get("/api/auth/user/");

    if (response.status == 200) {
      authStore.setProfile(response.data);
    }
  }

  return authStore.profile;
}

async function readFileAsDataURL(file) {
  let result_base64 = await new Promise((resolve) => {
    let fileReader = new FileReader();
    fileReader.onload = () => resolve(fileReader.result);
    fileReader.readAsDataURL(file);
  });

  return result_base64;
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
