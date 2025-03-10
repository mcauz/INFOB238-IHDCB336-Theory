import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import {useCartStore} from "@/stores/cart.js";

export const useUserStore = defineStore('user', () => {
    const auth_token = ref(sessionStorage.getItem("auth_token") || null);
    const is_connected = computed(() => auth_token.value !== null);
    const token = ref(0);

    async function refreshUser() {
        try {
            const response = await request("GET", "/user");
            token.value = response.token;
        } catch (e) {
            logout();
        }
    }

    if (auth_token.value !== null) {
        refreshUser();
        useCartStore().startWs();
    }

    async function login(token) {
        auth_token.value = token;
        sessionStorage.setItem("auth_token", token);
        await refreshUser();
        await useCartStore().startWs();
    }

    async function logout() {
        await request("PATCH", "/logout");
        auth_token.value = null;
        token.value = 0;
        await useCartStore().closeWs();
    }

    async function request(method, path, body = null) {
        const options = {
            method,
            headers: {
                "Content-Type": "application/json",
            },
        };
        if (method === "POST") options.body = JSON.stringify(body);
        if (auth_token.value !== null) options.headers["Authorization"] = `Bearer ${auth_token.value}`;

        const request = new Request(`http://${import.meta.env.VITE_HOST}/api${path}`, options);
        const response = await fetch(request);
        if (response.ok) return await response.json();
        else throw response.detail;
    }

    return { is_connected, token, refreshUser, logout, login, request };
})
