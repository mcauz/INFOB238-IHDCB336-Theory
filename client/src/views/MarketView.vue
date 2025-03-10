<script setup>
import { reactive } from "vue";
import FlowerSection from "@/components/FlowerSection.vue";
import { useUserStore } from "@/stores/user.js";

const state = reactive({
  flowers: []
});

useUserStore().request("GET", "/flowers")
  .then(flowers => state.flowers = flowers)
  .catch(error => console.error(error));
</script>

<template>
  <div class="grid">
    <flower-section v-for="flower in state.flowers" :key="flower.id" :flower="flower" :others="0" />
  </div>
</template>

<style lang="sass" scoped>
.grid
  display: grid
  grid-template-columns: repeat(4, 25%)
  grid-gap: 10px
</style>
