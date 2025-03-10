import { reactive, watch } from 'vue'
import { defineStore, storeToRefs } from 'pinia'
import { useUserStore } from "@/stores/user.js";

export const useCartStore = defineStore('cart', () => {
    const items = reactive([]);
    const others = reactive([]);

    function addItem(id, number) {
        const item = items.find(item => item.id === id);
        if (item) item.number += number;
        else items.push({ id, number });
    }

    async function addToCart(id, number) {
        if (number === 0) return;
        const flower = await useUserStore().request("GET", `/flower/${id}`);
        if (flower.quantity >= number) {
            addItem(id, number);
            await send({flower_id: id, number});
            return { success: true, quantity: flower.quantity - number };
        } else {
            return { success: false, quantity: flower.quantity };
        }
    }

    async function reset() {
        for (const key in items) {
            await send({flower_id: items[key].id, number: -items[key].number});
        }
        items.splice(0, items.length);
    }

    async function buy() {
        const success = await useUserStore().request("POST", "/cart", items);
        if (success) {
            await reset();
            await useUserStore().refreshUser();
        }
        return { success };
    }

    let ws = null;

    function closeWs() {
        ws = null;
    }

    function startWs() {
        ws = new WebSocket(`ws://${import.meta.env.VITE_HOST}/ws`);
        ws.addEventListener("close", closeWs);
        ws.addEventListener("error", closeWs);
        ws.addEventListener("message", (event) => {
            const {flower_id, number} = JSON.parse(event.data);

            const item = items.find(elt => elt.id === flower_id);
            const inCart = item?.number || 0;

            const index = others.findIndex(elt => elt.id === flower_id);
            const obj = { id: flower_id, number: number - inCart };
            if (index !== -1) others[index] = obj;
            else others.push(obj);
        });
    }

    async function send(body) {
        if (ws === null) return;
        await ws.send(JSON.stringify(body));
    }

    return { items, others, addToCart, reset, buy, startWs, closeWs };
})
