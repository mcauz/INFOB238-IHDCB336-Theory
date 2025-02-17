const flowersInfo = {
    f1: {
        image: "./assets/imgs/rose.jpeg",
        name: "Flower's name",
        unitPrice: 10,
    },
    f2: {
        image: "./assets/imgs/gerbera.jpeg",
        name: "Flower's name",
        unitPrice: 10,
    }
}

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

    displayToTable(tableId, totalId) {
        const table = document.getElementById(tableId);
        table.innerHTML = "";

        let sum = 0;
        for (const item of this.#items) {
            const info = flowersInfo[item.id];
            console.log(flowersInfo, item.id);
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
        }

        document.getElementById(totalId).innerText = sum;
    }

    buy(errorId, tableId, totalId) {
        if (this.#items.length === 0) return;
        console.log(this.#items.reduce((acc, i) => acc += i.number * flowersInfo[i.id].unitPrice, 0));
        if (this.#items.reduce((acc, i) => acc += i.number * flowersInfo[i.id].unitPrice, 0) > 30) {
            const error = document.getElementById(errorId);
            error.style.display = "block";
            setTimeout(() => error.style.display = "none", 3000);
            return;
        }
        alert("You buy flowers !");
        this.reset();
        this.displayToTable(tableId, totalId);
    }
}

const store = new Store();
