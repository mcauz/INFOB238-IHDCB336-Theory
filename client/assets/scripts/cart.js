class Store {
    #items = null;

    __constructor() {
        this.#items = JSON.parse(sessionStorage.getItem("store") || "[]");
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

    addToCart(fieldId, flowerId) {
        const domElt = document.getElementById(fieldId);
        const number = parseInt(domElt.value) || 0;
        if (number === 0) return;
        this.#addItem(flowerId, number);
        this.saveStore();
        domElt.value = 0;
    }

    reset() {
        this.#items = [];
        this.saveStore();
    }
}

const store = new Store();
