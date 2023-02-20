import axios from "axios";
import { removeToken, removeProfile } from "@/scripts/api/auth.js";
import Router from "@/router/index.js";

export const instance = axios.create({
  baseURL: import.meta.env.VITE_SERVER_DOMAIN,
  timeout: 3000,
  headers: {},
});

instance.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    if (error.response.status === 401) {
      removeToken();
      removeProfile();

      Router.push({ name: "Login" });
    }
    return Promise.reject(error);
  }
);

export function updateRequestHeader(token) {
  if (token) {
    instance.defaults.headers.common["Authorization"] = `Token ${token}`;
  } else {
    delete instance.defaults.headers.common["Authorization"];
  }
}

export default {
  instance,
};
