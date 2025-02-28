class Store {
    #items = null;
    #ws = null;

    constructor() {
        this.#items = JSON.parse(sessionStorage.getItem("store") || "[]");
        this.#ws = new WebSocket("ws://" + location.host + "/ws");

        const close_ws = () => this.#ws = null;
        this.#ws.addEventListener("close", close_ws);
        this.#ws.addEventListener("error", close_ws);
        this.#ws.addEventListener("message", (event) => this.onWebsocketMessage(JSON.parse(event.data)));
    }

    get items() {
        return this.#items.map(i => JSON.parse(JSON.stringify(i)));
    }

    saveStore() {
        sessionStorage.setItem("store", JSON.stringify(this.#items));
    }

    #addItem(flowerId, number) {
        const elt = this.#items.find(e => e.id === flowerId);
        if (elt) elt.number += number;
        else this.#items.push({ id: flowerId, number });
    }

    async addToCart(flowerId) {
        const domElt = document.getElementById(`i-${flowerId}`);
        const number = parseInt(domElt.value) || 0;
        if (number === 0) return;

        const flower = await (await fetch(`/api/flower/${flowerId}`)).json();
        if (flower.quantity >= number) {
            this.#addItem(flowerId, number);
            this.saveStore();
            domElt.value = 0;
            document.getElementById(`q-${flowerId}`).innerText = flower.quantity - number;
            await this.#ws.send(JSON.stringify({flower_id: flowerId, number}));
        } else {
            domElt.value = flower.quantity;
            document.getElementById(`q-${flowerId}`).innerText = flower.quantity;
            const error_elt = document.getElementById(`e-${flowerId}`);
            error_elt.style.display = "block";
            setTimeout(() => error_elt.style.display = "none", 3000);
        }
    }

    async reset() {
        const copy = this.#items;
        this.#items = [];
        this.saveStore();

        const ws = this.#ws;
        async function send() {
            for (const key in copy) {
                await ws.send(JSON.stringify({flower_id: copy[key].id, number: -copy[key].number}));
            }
        }

        if (this.#ws.readyState !== 1) this.#ws.addEventListener("open", send);
        else await send();
    }

    onWebsocketMessage({flower_id, number}) {
        const elt = document.getElementById(`info-${flower_id}`);
        if (!elt) return;

        if (number === 0) {
            elt.style.display = 'none';
            return;
        }

        const item = this.#items.find(i => i.id === flower_id);
        if (!!item) number -= item.number;

        elt.innerText = `${number} flowers in other carts.`;
        elt.style.display = 'block';
    }

    async displayToTable(tableId, totalId, formId) {
        const flowers = await (await fetch('/api/flowers')).json();

        const table = document.getElementById(tableId);
        table.innerHTML = "";

        let sum = 0;
        let str = "";
        for (const item of this.#items) {
            const info = flowers.find(f => f.id === item.id);
            const tr = document.createElement("tr");

            const tdImage = document.createElement("td");
            const image = document.createElement("img");
            image.setAttribute("src", `/public/images/${info.image}`);
            image.setAttribute("alt", info.name);
            tdImage.appendChild(image);
            tr.appendChild(tdImage);

            const tdName = document.createElement("td");
            tdName.innerText = info.name;
            tr.appendChild(tdName);

            const tdNumber = document.createElement("td");
            tdNumber.innerText = item.number;
            tr.appendChild(tdNumber);

            const tdUnitPrice = document.createElement("td");
            tdUnitPrice.innerText = info.unit_price;
            tr.appendChild(tdUnitPrice);

            const tdTotalPrice = document.createElement("td");
            tdTotalPrice.innerText = info.unit_price * item.number;
            tr.appendChild(tdTotalPrice);

            table.appendChild(tr);
            sum += info.unit_price * item.number;

            if (str.length > 0) str += ";";
            str += item.id + "=" + item.number;
        }

        document.getElementById(totalId).innerText = sum;

        const input = document.createElement("input");
        input.setAttribute("type", "hidden");
        input.setAttribute("name", "cart");
        input.setAttribute("value", str);

        document.getElementById(formId).appendChild(input);
    }
}

const store = new Store();
