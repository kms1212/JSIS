<script>
import { RouterLink } from "vue-router";
import APIAuth from "@/scripts/api/auth.js";

export default {
  name: "LoginView",
  components: {
    RouterLink,
  },
  methods: {
    login() {
      APIAuth.login(this.username, this.password)
        .then(() => {
          this.$router.push({ name: "Main" });
        })
        .catch((error) => {
          if (error.response.data.non_field_errors) {
            this.errormsg = error.response.data.non_field_errors.join("\n");
          }
        });
    },
  },
  data() {
    return {
      username: "",
      password: "",
      errormsg: "",
    };
  },
};
</script>

<template>
  <div class="space-y-6 py-8 text-base leading-7 text-black">
    <h1 class="text-center text-3xl font-extrabold">로그인</h1>
    <div>
      <ul class="space-y-5">
        <li class="flex flex-col items-start space-y-2">
          <div class="flex w-full items-center">
            <input
              @keyup.enter="login"
              class="w-full border-b outline-none transition-all focus:border-b-2 focus:border-b-blue-600"
              type="text"
              placeholder="아이디"
              v-model="username"
            />
          </div>
        </li>
        <li class="flex flex-col items-start space-y-2">
          <div class="flex w-full items-center">
            <input
              @keyup.enter="login"
              class="w-full border-b outline-none transition-all focus:border-b-2 focus:border-b-blue-600"
              type="password"
              placeholder="비밀번호"
              v-model="password"
            />
          </div>
        </li>
        <li class="flex items-center">
          <p class="text-red-500">{{ errormsg }}</p>
        </li>
        <li class="flex items-center">
          <button
            @click="login"
            class="w-full rounded-lg bg-blue-600 py-2 px-4 text-white shadow-md"
          >
            확인
          </button>
        </li>
      </ul>
    </div>
    <div class="grid grid-cols-2 pt-8 text-base font-semibold leading-none">
      <p>JSIS</p>
      <RouterLink class="text-right" to="/auth/register">회원가입</RouterLink>
    </div>
  </div>
</template>
