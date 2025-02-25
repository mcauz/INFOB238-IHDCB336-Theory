const flowersInfo = [
    {
        image: "/public/images/gerbera.jpeg",
        name: "Gerbera",
        unitPrice: 1,
    },
    {
        image: "/public/images/red-rose.jpeg",
        name: "Red rose",
        unitPrice: 3,
    },
    {
        image: "/public/images/lily.jpeg",
        name: "Lily",
        unitPrice: 5,
    },
    {
        image: "/public/images/daisy.jpeg",
        name: "Daisy",
        unitPrice: 2,
    }
]

class Store {
    #items = null;

    constructor() {
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

    displayToTable(tableId, totalId, formId) {
        const table = document.getElementById(tableId);
        table.innerHTML = "";

        let sum = 0;
        let str = "";
        for (const item of this.#items) {
            const info = flowersInfo[item.id];
            const tr = document.createElement("tr");

            const tdImage = document.createElement("td");
            const image = document.createElement("img");
            image.setAttribute("src", info.image);
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
            tdUnitPrice.innerText = info.unitPrice;
            tr.appendChild(tdUnitPrice);

            const tdTotalPrice = document.createElement("td");
            tdTotalPrice.innerText = info.unitPrice * item.number;
            tr.appendChild(tdTotalPrice);

            table.appendChild(tr);
            sum += info.unitPrice * item.number;

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
