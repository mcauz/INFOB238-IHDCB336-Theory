<script setup>
import { reactive } from "vue";
import { RouterLink } from 'vue-router'
import { useUserStore } from "@/stores/user.js";

const userStore = useUserStore();

const state = reactive({
  categories: []
});

userStore.request("GET", '/categories')
    .then(categories => { state.categories = categories; })
    .catch(error => console.error(error));
</script>

<template>
  <section>
    <h2>Welcome !</h2>
    <p>
      Welcome to my great marketplace. Use virtual token to buy beautiful flowers.
      <span v-if="!userStore.is_connected">
      Click <RouterLink to="/login">here</RouterLink> to create or login to an account and start to buy.
      </span>
    </p>
  </section>
  <section>
    <h2>New flowers on the market:</h2>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Availability</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody v-for="cat in state.categories" :key="cat.id">
        <tr class="tr-cat">
          <td colspan="3">{{cat.name}}</td>
        </tr>
        <tr v-for="flower in cat.flowers">
          <td><img :src="`/${flower.image}`" :alt="flower.name"/>{{flower.name}}</td>
          <td>{{flower.quantity}}</td>
          <td>{{flower.unit_price}}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<style lang="sass" scoped>
table, tr, th, td
  border: 1px solid black
  border-collapse: collapse

table
  width: 100%

td img
  height: 1em
  margin-right: 5px

td:not(:first-child)
  width: 200px
  text-align: center

th:first-child
  text-align: left

th, td
  padding: 3px

thead tr:first-child
  background-color: #0B4936

th
  color: white

.tr-cat
  background-color: #5BCAA1
</style>
