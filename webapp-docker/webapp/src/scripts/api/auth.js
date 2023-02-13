import { instance, useAuthStore } from "@/scripts/api/axios.js";
import Router from "@/router/index.js";

export async function login(username, password) {
  const authStore = useAuthStore();
  const response = await instance.post("/api/auth/login/", {
    username,
    password,
  });

  if (response.status == 200) {
    authStore.setToken(response.data.token);

    await authStore.profile;
  }

  return response.data;
}

export async function logout() {
  const response = await instance.post("/api/auth/logout/");

  removeToken();
  removeProfile();

  Router.push({ name: "Login" });

  return response.data;
}

export function removeToken() {
  const authStore = useAuthStore();
  authStore.setToken("");
}

export function removeProfile() {
  const authStore = useAuthStore();
  authStore.setProfile("");
  authStore.setProfileImage("");
}

export function restoreToken() {
  const authStore = useAuthStore();
  authStore.setToken(authStore.token);
}

export default {
  login,
  logout,
  removeToken,
  removeProfile,
  restoreToken,
};
