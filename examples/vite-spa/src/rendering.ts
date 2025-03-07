function createTitle(text: string, level: number) {
    const title = document.createElement(`h${level}`);
    title.innerText = text;
    return title;
}

function createLink(text: string, callback: () => void) {
    const link = document.createElement("a");
    link.addEventListener("click", callback);
    link.innerText = text;
    return link;
}

function createImage(path: string, alt: string) {
    const image = document.createElement("img");
    image.setAttribute("src", path);
    image.setAttribute("alt", alt);
    return image;
}

export function render_first_page(target: Element, navigationCallback: (path: string) => void) {
    target.appendChild(createTitle("First page", 1));
    target.appendChild(createLink("Go to second page", () => navigationCallback("/second")));
    target.appendChild(createImage("/HTML5_logo.png", "HTML 5 Logo"));
}

export function render_second_page(target: Element, navigationCallback: (path: string) => void) {
    target.appendChild(createTitle("Second page", 1));
    target.appendChild(createLink("Go to first page", () => navigationCallback("/")));
}
