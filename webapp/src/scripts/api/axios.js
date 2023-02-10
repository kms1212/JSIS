import axios from "axios";
import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";

export const instance = axios.create({
  baseURL: import.meta.env.VITE_SERVER_DOMAIN,
  timeout: 3000,
  headers: {},
});

function updateRequestHeader(token) {
  if (token) {
    instance.defaults.headers.common["Authorization"] = `Token ${token}`;
  } else {
    delete instance.defaults.headers.common["Authorization"];
  }
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: useStorage("token", "", localStorage),
    profile: null,
    profileimage: useStorage("profileimage", null, sessionStorage),
  }),
  getters: {},
  actions: {
    setToken(newToken) {
      console.log(newToken);
      if (newToken) {
        this.$patch({ token: newToken });
        updateRequestHeader(this.token);
      } else {
        this.$patch({ token: "" });
        updateRequestHeader("");
      }
      console.log(this.token);
    },
    setProfile(newProfile) {
      this.$patch({ profile: newProfile });
    },
    setProfileImage(newProfileImage) {
      this.$patch({ profileimage: newProfileImage });
    },
  },
});

export default {
  instance,
  useAuthStore,
};
