function checkInputNumber(flower_id) {
    const max = parseInt(document.getElementById(`q-${flower_id}`).innerText);
    const domElt = document.getElementById(`i-${flower_id}`);
    const strValue = domElt.value.replace(/[^0-9]/g, "");
    const value = parseInt(strValue, 10) || 0;
    domElt.value = (value > max) ? max : value;
}
