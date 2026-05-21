window.mostrarToast = function (mensaje, tipo = "success") {

    const container = document.getElementById("toast-container");

    const toast = document.createElement("div");
    toast.className = `toast-custom toast-${tipo}`;

    const texto = document.createElement("span");
    texto.textContent = mensaje;

    toast.appendChild(texto);

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
};
document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menuToggle");
    const sidebar = document.querySelector(".sidebar");

    menuToggle.addEventListener("click", function () {
        sidebar.classList.toggle("active");
    });
});
