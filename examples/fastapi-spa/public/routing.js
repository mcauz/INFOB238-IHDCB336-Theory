const pages = {
    "/": render_first_page,
    "/second": render_second_page
};

function navigate(path) {
    window.history.pushState({}, "", path);
    render_page();
}

function render_page() {
    const path = window.location.pathname;
    document.body.innerHTML = "";

    if (Object.keys(pages).includes(path)) pages[path](document.body, navigate);
    else pages["/"](document.body, navigate);
}

window.addEventListener("popstate", render_page);
window.addEventListener("load", render_page);