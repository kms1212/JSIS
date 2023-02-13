import { createRouter, createWebHistory } from "vue-router";
import AppBaseView from "@/views/main/AppBaseView.vue";
import MainView from "@/views/main/MainView.vue";
import NoticeView from "@/views/main/NoticeView.vue";
import NoticeArticleView from "@/views/main/NoticeArticleView.vue";
import ReplyView from "@/views/main/ReplyView.vue";
import ClassMainView from "@/views/class/ClassMainView.vue";
import ConvMainView from "@/views/conv/ConvMainView.vue";
import HQMainView from "@/views/hq/HQMainView.vue";
import MealMainView from "@/views/meal/MealMainView.vue";
import CommunityMainView from "@/views/community/CommunityMainView.vue";
import CommunityForumView from "@/views/community/CommunityForumView.vue";
import AuthBaseView from "@/views/auth/AuthBaseView.vue";
import LoginView from "@/views/auth/LoginView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Base",
      component: AppBaseView,
      children: [
        {
          path: "",
          name: "Main",
          component: MainView,
        },
        {
          path: "notice",
          name: "Notice",
          component: NoticeView,
        },
        {
          path: "notice/:id",
          name: "NoticeArticle",
          component: NoticeArticleView,
          children: [
            {
              path: "replies",
              name: "Replies",
              component: ReplyView,
            },
          ],
        },
        {
          path: "class",
          name: "ClassMain",
          component: ClassMainView,
        },
        {
          path: "conv",
          name: "ConvMain",
          component: ConvMainView,
        },
        {
          path: "hq",
          name: "HQMain",
          component: HQMainView,
        },
        {
          path: "meal",
          name: "MealMain",
          component: MealMainView,
        },
        {
          path: "community",
          name: "CommunityMain",
          component: CommunityMainView,
        },
        {
          path: "community/forum",
          name: "CommunityForum",
          component: CommunityForumView,
        },
      ],
    },
    {
      path: "/auth",
      name: "AuthBase",
      component: AuthBaseView,
      children: [
        {
          path: "login",
          name: "Login",
          component: LoginView,
        },
      ],
    },
  ],
});

export default router;
