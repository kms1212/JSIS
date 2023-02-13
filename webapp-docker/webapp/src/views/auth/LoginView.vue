<script>
import APIAuth from "@/scripts/api/auth.js";

export default {
  name: "LoginView",
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
    <h1 class="text-3xl font-extrabold text-center">로그인</h1>
    <div>
      <ul class="space-y-5">
        <li class="flex items-start flex-col space-y-2">
          <div class="flex items-center w-full">
            <input
              @keyup.enter="login"
              class="w-full border-b focus:border-b-blue-600 focus:border-b-2 transition-all outline-none"
              type="text"
              placeholder="아이디"
              v-model="username"
            />
          </div>
        </li>
        <li class="flex items-start flex-col space-y-2">
          <div class="flex items-center w-full">
            <input
              @keyup.enter="login"
              class="w-full border-b focus:border-b-blue-600 focus:border-b-2 transition-all outline-none"
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
            class="py-2 px-4 rounded-lg shadow-md bg-blue-600 text-white w-full"
          >
            확인
          </button>
        </li>
      </ul>
    </div>
    <div class="pt-8 text-base font-semibold leading-none grid grid-cols-2">
      <p>JSIS</p>
      <a class="text-right" href="{% url 'membersvc:register' %}">회원가입</a>
    </div>
  </div>
</template>
