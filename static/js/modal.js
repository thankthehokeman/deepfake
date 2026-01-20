const root = document.documentElement; 
const modal = document.getElementById("galleryModal");
const openBtn = document.getElementById("openGallery");
const closeBtn = document.getElementById("closeGallery");

const ANIM_MS = 400;

function openModal() {
    root.classList.add("modal-is-open", "modal-is-opening");
    modal.showModal();

    window.setTimeout(() => {
    root.classList.remove("modal-is-opening");
    }, ANIM_MS);
}

function closeModal() {
    root.classList.add("modal-is-closing");

    window.setTimeout(() => {
    modal.close();
    root.classList.remove("modal-is-open", "modal-is-closing");
    }, ANIM_MS);
}

openBtn.addEventListener("click", openModal);
closeBtn.addEventListener("click", closeModal);

modal.addEventListener("click", (event) => {
    if (event.target === modal) closeModal();
});
