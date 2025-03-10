<script setup>
import { computed } from "vue";
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from "@/stores/user.js";

const userStore = useUserStore();

const menu = computed(() => {
    const items = [{ text: 'Home', to: '/' }];
    if (userStore.is_connected) {
      items.push({ text: 'Market', to: '/market' });
      items.push({ text: 'Cart', to: '/cart' });
      items.push({ text: 'Logout', to: '/logout' });
    } else {
      items.push({ text: 'Login/Register', to: '/login' });
    }
    return items;
});

</script>

<template>
  <header>
    <h1>My marketplace</h1>
    <div class="separator"></div>
    <nav>
      <ul>
        <li v-for="item in menu"><RouterLink :to="item.to">{{item.text}}</RouterLink></li>
      </ul>
    </nav>
    <p v-if="userStore.is_connected" class="token">
      You have {{userStore.token}} <img class="token-logo" src="/token.png" alt="tokens" />
    </p>
  </header>
  <main>
    <RouterView />
  </main>
  <footer>
    <p>Site created by Adibou</p>
    <p>&#169; Copyright Adibou corporation</p>
  </footer>
</template>

<style scoped>
</style>
