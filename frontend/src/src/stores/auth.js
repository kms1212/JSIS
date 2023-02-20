import { defineStore } from "pinia";
import Cookies from "js-cookie";
import { updateRequestHeader } from "@/scripts/api/axios";


export const useAuthStore = defineStore('storeUser', {
    state () {
        return {
            token: '',
            profile: {},
        }
    },
    actions: {
        setToken(newToken) {
            if (newToken) {
                this.$patch({ token: newToken });
                updateRequestHeader(this.token);
                Cookies.set("token", newToken, { expires: 10, sameSite: "strict", path: "/" })
            } else {
                this.$patch({ token: "" });
                updateRequestHeader("");
                Cookies.remove("token")
            }
        },
        getToken() {
            if (this.token === "" && Cookies.get("token")) {
                this.setToken(Cookies.get("token"));
            }

            return this.token;
        },
        setProfile(newProfile) {
            this.$patch({ profile: newProfile });
            
        },
    },
    })