import { createApp } from "vue";
import { createPinia } from "pinia";
import VueFeather from "vue-feather";
import vueDompurifyHTMLPlugin from "vue-dompurify-html";
import * as Sentry from "@sentry/vue";
import { BrowserTracing } from "@sentry/tracing";

import App from "./App.vue";
import router from "./router";

import "./assets/css/tailwind.css";

// Create app
const app = createApp(App);

// Pinia config
const pinia = createPinia();

// Sentry config
if (import.meta.env.MODE === "production") {
  Sentry.init({
    app,
    dsn: import.meta.env.VITE_SENTRY_DSN,
    integrations: [
      new BrowserTracing({
        routingInstrumentation: Sentry.vueRouterInstrumentation(router),
        tracePropagationTargets: [
          "localhost",
          import.meta.env.VITE_SERVER_DOMAIN,
        ],
      }),
    ],
    tracesSampleRate: 1.0,
  });
}

// Plugins
app.use(pinia);
app.use(router);
app.use(vueDompurifyHTMLPlugin);

// Components
app.component(VueFeather.name, VueFeather);

// Mount
app.mount("#app");
