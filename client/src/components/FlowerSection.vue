<script setup>
import { reactive, computed } from 'vue';
import { useCartStore } from "@/stores/cart.js";

const cartStore = useCartStore();

const props = defineProps(['flower']);

const state = reactive({
  flower: { ...props.flower },
  input: 0,
  error: false
});

const others = computed(() => {
  const elt = cartStore.others.find(elt => elt.id === state.flower.id);
  return elt?.number;
});

function checkInputNumber() {
  const max = state.flower.quantity;
  const strValue = state.input.replace(/[^0-9]/g, "");
  const value = parseInt(strValue, 10) || 0;
  state.input = (value > max) ? max : value;
}

async function addToCart() {
  const number = parseInt(state.input) || 0;
  const { success, quantity } = await cartStore.addToCart(state.flower.id, number);
  state.flower.quantity = quantity;
  if (success) {
    state.input = 0;
  } else {
    state.input = quantity;
    state.error = true;
    setTimeout(() => state.error = false, 3000);
  }
}
</script>

<template>
  <section>
    <img :src="state.flower.image" :alt="state.flower.name" />
    <p><span class="flowerName">{{state.flower.name}}</span> (Category: {{state.flower.category.name}})</p>
    <p>{{state.flower.description}}</p>
    <div>
      <input type="text" v-model="state.input" @change="checkInputNumber" />
      <p>/ {{state.flower.quantity}}</p>
      <button class="btn submit" @click="addToCart">Add to cart</button>
    </div>
    <p v-show="others > 0">{{others}} flowers in other cart.</p>
    <p v-if="state.error" class="error-message">The available quantity has changed.</p>
  </section>
</template>

<style lang="sass" scoped>
img
  width: 100%

.flowerName
  font-weight: bold

section div
  display: flex
  flex-direction: row
  align-items: center

section div input
  width: 50px
  margin-right: 5px

section div button
  margin-left: 10px
</style>
