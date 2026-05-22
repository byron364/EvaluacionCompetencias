function abrirModalCurso() {
    const modalElement = document.getElementById("modalCrearCurso");

    if (!modalElement) {
        console.error("Modal no encontrado");
        return;
    }

    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}