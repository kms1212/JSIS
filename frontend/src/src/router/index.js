import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Base",
      component: () => import("@/views/main/AppBaseView.vue"),
      children: [
        {
          path: "",
          name: "Main",
          component: () => import("@/views/main/MainView.vue"),
        },
        {
          path: "profile",
          name: "Profile",
          component: () => import("@/views/main/ProfileView.vue"),
        },
        {
          path: "notice",
          name: "Notice",
          component: () => import("@/views/main/NoticeView.vue"),
        },
        {
          path: "notice/:id",
          name: "NoticeArticle",
          component: () => import("@/views/main/NoticeArticleView.vue"),
          children: [
            {
              path: "replies",
              name: "Replies",
              component: () => import("@/views/main/ReplyView.vue"),
            },
          ],
        },
        {
          path: "class",
          name: "ClassMain",
          component: () => import("@/views/class/ClassMainView.vue"),
        },
        {
          path: "conv",
          name: "ConvMain",
          component: () => import("@/views/conv/ConvMainView.vue"),
        },
        {
          path: "hq",
          name: "HQMain",
          component: () => import("@/views/hq/HQMainView.vue"),
        },
        {
          path: "meal",
          name: "MealMain",
          component: () => import("@/views/meal/MealMainView.vue"),
        },
        {
          path: "community",
          name: "CommunityMain",
          component: () => import("@/views/community/CommunityMainView.vue"),
        },
        {
          path: "community/forum",
          name: "CommunityForum",
          component: () => import("@/views/community/CommunityForumView.vue"),
        },
      ],
    },
    {
      path: "/auth",
      name: "AuthBase",
      component: () => import("@/views/auth/AuthBaseView.vue"),
      children: [
        {
          path: "login",
          name: "Login",
          component: () => import("@/views/auth/LoginView.vue"),
        },
      ],
    },
  ],
});

export default router;
