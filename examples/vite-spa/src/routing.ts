import { render_first_page, render_second_page } from "@/rendering";
import "@/assets/stylesheets/main.sass"

let counter = 0;

const pages = {
    "/": render_first_page,
    "/second": render_second_page
};

function navigate(path: string) {
    window.history.pushState({}, "", path);
    render_page();
}

async function load_lazy_loading() {
    const module = await import("@/lazyLoading");
    module.default();
}

function render_page() {
    const path = window.location.pathname;
    document.body.innerHTML = "";

    if (Object.keys(pages).includes(path)) pages[path](document.body, navigate);
    else pages["/"](document.body, navigate);

    if (counter === 3) load_lazy_loading();
    counter++;
}

window.addEventListener("popstate", render_page);
window.addEventListener("load", render_page);
