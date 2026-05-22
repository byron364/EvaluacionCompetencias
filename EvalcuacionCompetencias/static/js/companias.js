async function crearCompania() {

    const nombre =

        document.getElementById(
            "nombreCompania"
        ).value.trim();

    const descripcion =

        document.getElementById(
            "descripcionCompania"
        ).value.trim();

    const batallon =

        document.getElementById(
            "batallonCompania"
        ).value;

    // =========================
    // VALIDAR
    // =========================

    if (!nombre) {

        mostrarToast(

            "⚠️ Ingrese el nombre",

            "warning"
        );

        return;
    }

    if (!batallon) {

        mostrarToast(

            "⚠️ Seleccione un batallón",

            "warning"
        );

        return;
    }

    try {

        const response = await fetch(

            "/crear-compania/",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    nombre,
                    descripcion,
                    batallon
                })
            }
        );

        const data =
            await response.json();

        if (data.error) {

            mostrarToast(

                "❌ " + data.error,

                "error"
            );

            return;
        }

        mostrarToast(

            "✅ " + data.mensaje,

            "success"
        );

        setTimeout(() => {

            location.reload();

        }, 1000);

    } catch (error) {

        mostrarToast(

            "❌ Error del servidor",

            "error"
        );
    }
}
function abrirModalEditarCompania(

    id,
    nombre,
    descripcion

) {

    document.getElementById(
        "editarCompaniaId"
    ).value = id;

    document.getElementById(
        "editarNombreCompania"
    ).value = nombre;

    document.getElementById(
        "editarDescripcionCompania"
    ).value = descripcion;

    const modal = new bootstrap.Modal(

        document.getElementById(
            "modalEditarCompania"
        )
    );

    modal.show();
}

async function guardarEdicionCompania() {

    const id =
        document.getElementById(
            "editarCompaniaId"
        ).value;

    const nombre =
        document.getElementById(
            "editarNombreCompania"
        ).value;

    const descripcion =
        document.getElementById(
            "editarDescripcionCompania"
        ).value;

    try {

        const response = await fetch(

            `/editar-compania/${id}/`,

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    nombre,
                    descripcion
                })
            }
        );

        const data =
            await response.json();

        if (data.error) {

            mostrarToast(
                "❌ " + data.error,
                "error"
            );

            return;
        }

        mostrarToast(
            "✅ Compañía actualizada",
            "success"
        );

        $("#modalEditarCompania")
            .modal("hide");

        setTimeout(() => {

            location.reload();

        }, 800);

    } catch (error) {

        console.error(error);

        mostrarToast(
            "❌ Error del sistema",
            "error"
        );
    }
}
async function toggleCompania(id, estadoActual) {

    const accion = estadoActual
        ? "desactivar"
        : "activar";

    Swal.fire({

        icon: "warning",

        title:
            `¿Desea ${accion} esta compañía?`,

        text:
            "El estado de la compañía cambiará",

        showCancelButton: true,

        confirmButtonColor: "#198754",

        cancelButtonColor: "#dc3545",

        confirmButtonText:
            `Sí, ${accion}`,

        cancelButtonText:
            "Cancelar"

    }).then(async (result) => {

        if (result.isConfirmed) {

            const response = await fetch(

                `/toggle-compania/${id}/`,

                {
                    method: "POST"
                }
            );

            const data =
                await response.json();

            mostrarToast(

                "✅ " + data.mensaje,

                "success"
            );

            setTimeout(() => {

                location.reload();

            }, 700);
        }
    });
}
