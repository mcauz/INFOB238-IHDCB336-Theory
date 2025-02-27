function checkInputNumber(id, id_quantity) {
    const max = parseInt(document.getElementById(id_quantity).innerText);
    const domElt = document.getElementById(id);
    const strValue = domElt.value.replace(/[^0-9]/g, "");
    const value = parseInt(strValue, 10) || 0;
    domElt.value = (value > max) ? max : value;
}
