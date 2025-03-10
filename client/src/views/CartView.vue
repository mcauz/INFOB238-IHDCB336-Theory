<script setup>
import { reactive, computed } from 'vue';
import { useCartStore } from "@/stores/cart.js";
import { useUserStore } from "@/stores/user.js";

const cartStore = useCartStore();

const state = reactive({
  flowers: [],
  error: false
});

useUserStore().request("GET", "/flowers")
    .then(flowers => state.flowers = flowers)
    .catch(error => console.error(error));

const flowers = computed(() => {
  if (state.flowers.length === 0) return [];
  return cartStore.items.map(({ id, number }) => {
    const flower = state.flowers.find(f => f.id === id);
    return { ...flower, number, total_price: number * flower.unit_price };
  });
});

const totalPrice = computed(() => {
  return flowers.value.reduce((acc, flower) => acc + flower.total_price, 0);
});

async function buy() {
  const { success } = await cartStore.buy();
  if (!success) state.error = true;
}

</script>

<template>
  <section>
    <table v-if="state.flowers.length>0">
      <thead>
      <tr>
        <th>Image</th>
        <th>Name</th>
        <th>Number selected</th>
        <th>Unit price</th>
        <th>Total price</th>
      </tr>
      </thead>
      <tbody id="cart">
        <tr v-for="item in flowers" :key="item.id">
          <td><img :src="item.image" :alt="item.name"/></td>
          <td>{{item.name}}</td>
          <td>{{item.number}}</td>
          <td>{{item.unit_price}}</td>
          <td>{{item.total_price}}</td>
        </tr>
      </tbody>
      <tfoot>
      <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td id="total">{{totalPrice}}</td>
      </tr>
      </tfoot>
    </table>
    <div class="actions">
      <button class="btn reset" @click="cartStore.reset">Reset</button>
      <button class="btn submit" @click="buy">Buy</button>
    </div>
    <p v-if="state.error" class="error-message">You don't have enough tokens.</p>
  </section>
</template>

<style lang="sass" scoped>
table
  width: 100%
  border-collapse: collapse

table img
  width: 50px

td
  text-align: center
  padding: 5px

tr:last-child td
  border-top: 1px solid black

.actions
  display: flex
  flex-direction: row
  justify-content: end
  margin-top: 20px

</style>
