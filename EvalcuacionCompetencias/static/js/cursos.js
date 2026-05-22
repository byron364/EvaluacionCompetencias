window.crearCurso = function () {

    const data = {
        codigo: document.getElementById("codigoCurso").value.trim(),
        nombre: document.getElementById("nombreCurso").value.trim(),
        descripcion: document.getElementById("descripcionCurso").value.trim(),
        instructor: document.getElementById("instructorCurso").value,
        fecha_inicio: document.getElementById("fechaInicioCurso").value,
        fecha_fin: document.getElementById("fechaFinCurso").value,
        cupo_maximo: document.getElementById("cupoCurso").value
    };

    if (!data.codigo || !data.nombre) {
        mostrarToast("Complete los campos obligatorios", "warning");
        return;
    }

    fetch("/crear-curso/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(res => {
            if (res.error) {
                mostrarToast(res.error, "error");
            } else {
                mostrarToast(res.mensaje, "success");

                const modal = bootstrap.Modal.getInstance(
                    document.getElementById("modalCrearCurso")
                );

                if (modal) {
                    modal.hide();
                }

                location.reload();
            }
        })
        .catch(() => {
            mostrarToast("Error del servidor", "error");
        });
};

document.addEventListener("click", function (e) {

    const boton = e.target.closest(".btn-editar-curso");

    if (!boton) return;

    document.getElementById("editarCursoId").value =
        boton.dataset.id;

    document.getElementById("editarCodigoCurso").value =
        boton.dataset.codigo;

    document.getElementById("editarNombreCurso").value =
        boton.dataset.nombre;

    document.getElementById("editarDescripcionCurso").value =
        boton.dataset.descripcion;

    document.getElementById("editarInstructorCurso").value =
        boton.dataset.instructor;

    document.getElementById("editarFechaInicioCurso").value =
        boton.dataset.fecha_inicio;

    document.getElementById("editarFechaFinCurso").value =
        boton.dataset.fecha_fin;

    document.getElementById("editarCupoCurso").value =
        boton.dataset.cupo;

    const modal = new bootstrap.Modal(
        document.getElementById("modalEditarCurso")
    );

    modal.show();

});
window.guardarEdicionCurso = function () {

    const cursoId =
        document.getElementById("editarCursoId").value;

    const data = {

        codigo:
            document.getElementById("editarCodigoCurso").value,

        nombre:
            document.getElementById("editarNombreCurso").value,

        descripcion:
            document.getElementById("editarDescripcionCurso").value,

        instructor:
            document.getElementById("editarInstructorCurso").value,

        fecha_inicio:
            document.getElementById("editarFechaInicioCurso").value,

        fecha_fin:
            document.getElementById("editarFechaFinCurso").value,

        cupo_maximo:
            document.getElementById("editarCupoCurso").value
    };

    fetch(`/editar-curso/${cursoId}/`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    })
        .then(res => res.json())
        .then(res => {

            if (res.error) {

                mostrarToast(res.error, "error");

            } else {

                mostrarToast(
                    "Curso actualizado correctamente",
                    "success"
                );

                location.reload();
            }

        });

}
document.addEventListener("click", async function (e) {

    const boton = e.target.closest(".btn-eliminar-curso");

    if (!boton) return;

    e.preventDefault();

    const cursoId = boton.dataset.id;

    const result = await Swal.fire({

        title: "¿Eliminar curso?",

        text: "Esta acción no se puede deshacer",

        icon: "warning",

        showCancelButton: true,

        confirmButtonColor: "#198754",

        cancelButtonColor: "#dc3545",

        confirmButtonText: "Sí, eliminar",

        cancelButtonText: "Cancelar"

    });

    if (!result.isConfirmed) return;

    try {

        const response = await fetch(

            `/eliminar-curso/${cursoId}/`,

            {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            }
        );

        const data = await response.json();

        if (data.error) {

            mostrarToast(data.error, "error");
            return;
        }

        // ELIMINAR FILA VISUALMENTE
        const fila = boton.closest("tr");

        // SI EXISTE DATATABLE
        if ($.fn.DataTable.isDataTable("#tablaCursos")) {

            const tabla =
                $("#tablaCursos").DataTable();

            tabla
                .row(fila)
                .remove()
                .draw(false);

        } else {

            fila.remove();

        }

        Swal.fire({

            title: "Eliminado",

            text: "Curso eliminado correctamente",

            icon: "success",

            confirmButtonColor: "#198754"

        });

    } catch (error) {

        console.error(error);

        mostrarToast(
            "Error eliminando curso",
            "error"
        );
    }

});
