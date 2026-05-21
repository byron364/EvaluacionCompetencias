async function crearBatallon() {

    const nombre =

        document.getElementById(
            "nombreBatallon"
        ).value;

    const ciudad =

        document.getElementById(
            "ciudadBatallon"
        ).value;

    const descripcion =

        document.getElementById(
            "descripcionBatallon"
        ).value;

    if (!nombre.trim()) {

        mostrarToast(
            "⚠️ Debe ingresar el nombre del batallón",
            "warning"
        );

        return;
    }

    try {

        const response = await fetch(

            "/crear-batallon/",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    nombre,
                    ciudad,
                    descripcion

                })
            }
        );

        const data = await response.json();

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

        }, 1200);

    } catch (error) {

        mostrarToast(
            "❌ Error del sistema",
            "error"
        );

        console.error(error);

    }

}

async function guardarEdicionBatallon() {

    const id =
        document.getElementById(
            "editarBatallonId"
        ).value;

    const nombre =
        document.getElementById(
            "editarNombreBatallon"
        ).value;

    const ciudad =
        document.getElementById(
            "editarCiudadBatallon"
        ).value;

    const descripcion =
        document.getElementById(
            "editarDescripcionBatallon"
        ).value;

    try {

        const response = await fetch(

            `/editar-batallon/${id}/`,

            {

                method: "PUT",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    nombre,
                    ciudad,
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
            "✅ Batallón actualizado",
            "success"
        );

        $("#modalEditarBatallon")
            .modal("hide");

        setTimeout(() => {

            location.reload();

        }, 1000);

    } catch (error) {

        mostrarToast(
            "❌ Error del sistema",
            "error"
        );

        console.error(error);

    }

}
// ABRIR MODAL EDITAR
$(document).on(
    "click",
    ".btn-editar-batallon",
    function () {

        const id =
            $(this).data("id");

        const nombre =
            $(this).data("nombre");

        const ciudad =
            $(this).data("ciudad");

        const descripcion =
            $(this).data("descripcion");

        $("#editarBatallonId").val(id);

        $("#editarNombreBatallon")
            .val(nombre);

        $("#editarCiudadBatallon")
            .val(ciudad);

        $("#editarDescripcionBatallon")
            .val(descripcion);

        $("#modalEditarBatallon")
            .modal("show");

    }
);

$(document).on(
    "click",
    ".btn-cambiar-estado",
    async function () {

        const id =
            $(this).data("id");

        const activo =
            $(this).data("activo");

        let accion =
            activo ? "desactivar" : "activar";

        const resultado = await Swal.fire({

            title:
                `¿Desea ${accion} este batallón?`,

            text:
                "El estado del batallón cambiará",

            icon: "warning",

            showCancelButton: true,

            confirmButtonColor: "#198754",

            cancelButtonColor: "#dc3545",

            confirmButtonText:
                `Sí, ${accion}`,

            cancelButtonText:
                "Cancelar"

        });

        if (!resultado.isConfirmed) {

            return;

        }

        try {

            const response = await fetch(

                `/cambiar-estado-batallon/${id}/`,

                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                            "application/json"

                    }

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
                "❌ Error del sistema",
                "error"
            );

            console.error(error);

        }

    }
);