function createTitle(text, level) {
    const title = document.createElement(`h${level}`);
    title.innerText = text;
    return title;
}

function createLink(text, callback) {
    const link = document.createElement("a");
    link.addEventListener("click", callback);
    link.innerText = text;
    return link;
}

function render_first_page(target, navigationCallback) {
    target.appendChild(createTitle("First page", 1));
    target.appendChild(createLink("Go to second page", () => navigationCallback("/second")));
}

function render_second_page(target, navigationCallback) {
    target.appendChild(createTitle("Second page", 1));
    target.appendChild(createLink("Go to first page", () => navigationCallback("/")));
}

