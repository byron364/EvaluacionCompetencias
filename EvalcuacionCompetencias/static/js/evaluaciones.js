async function cambiarEstadoEvaluacion(id) {

    try {

        const response = await fetch(

            `/activar-evaluacion/${id}/`,

            {

                method: "POST",

                headers: {

                    "X-CSRFToken":
                        getCookie("csrftoken")

                }

            }

        );

        const data =
            await response.json();

        if (data.success) {

            mostrarToast(

                data.mensaje,

                "success"

            );

            setTimeout(() => {

                location.reload();

            }, 1000);

        } else {

            mostrarToast(

                data.error,

                "error"

            );

        }

    } catch (error) {

        console.error(error);

        mostrarToast(

            "Error al cambiar estado",

            "error"

        );

    }

}

async function verEvaluacion(id) {

    try {

        const response = await fetch(

            `/detalle-evaluacion/${id}/`

        );

        const data =
            await response.json();

        console.log(data);

        // =====================================
        // DATOS GENERALES
        // =====================================

        document.getElementById(
            "tituloVerEvaluacion"
        ).innerHTML = `
            📋 ${data.titulo}
        `;

        document.getElementById(
            "verCompania"
        ).textContent =
            data.compania;

        document.getElementById(
            "verInstructor"
        ).textContent =
            data.instructor;

        document.getElementById(
            "verFecha"
        ).textContent =
            data.fecha;

        // =====================================
        // PARTICIPANTES
        // =====================================

        const tabla =
            document.getElementById(
                "tablaParticipantesEvaluacion"
            );

        tabla.innerHTML = "";

        document.getElementById(
            "totalParticipantes"
        ).textContent =
            data.participantes.length;

        data.participantes.forEach(p => {

            tabla.innerHTML += `

                <tr>

                    <td>
                        ${p.apellidos}
                    </td>

                    <td>
                        ${p.nombres}
                    </td>

                    <td>
                        ${p.documento}
                    </td>

                </tr>

            `;

        });

        // =====================================
        // ABRIR MODAL
        // =====================================

        const modal = new bootstrap.Modal(

            document.getElementById(
                "modalVerEvaluacion"
            )

        );

        modal.show();

    } catch (error) {

        console.error(error);

        mostrarToast(

            "Error al obtener evaluación",

            "error"

        );

    }

}
// =====================================
// EDITAR EVALUACIÓN
// =====================================

async function editarEvaluacion(id) {

    try {

        const response = await fetch(

            `/detalle-evaluacion/${id}/`

        );

        const data =
            await response.json();

        console.log(data);

        // =====================================
        // LLENAR CAMPOS
        // =====================================

        document.getElementById(
            "editarEvaluacionId"
        ).value = data.id;

        document.getElementById(
            "editarTituloEvaluacion"
        ).value = data.titulo;

        document.getElementById(
            "editarFechaEvaluacion"
        ).value = data.fecha;

        document.getElementById(
            "editarInstructorEvaluacion"
        ).value = data.instructor_id;

        const selectCompania =
            document.getElementById(
                "editarCompaniaEvaluacion"
            );

        selectCompania.innerHTML = "";

        // =====================================
        // CARGAR COMPAÑIAS
        // =====================================

        companias.forEach(compania => {

            const option =
                document.createElement("option");

            option.value = compania.id;

            option.textContent =
                compania.nombre;

            // =====================================
            // SELECCIONAR
            // =====================================

            if (
                compania.id == data.compania_id
            ) {

                option.selected = true;

            }

            selectCompania.appendChild(
                option
            );

        });

        document.getElementById(
            "editarDescripcionEvaluacion"
        ).value = data.descripcion;

        // =====================================
        // ABRIR MODAL
        // =====================================

        const modal = new bootstrap.Modal(

            document.getElementById(
                "modalEditarEvaluacion"
            )

        );

        modal.show();

    } catch (error) {

        console.error(error);

        mostrarToast(

            "Error cargando evaluación",

            "error"

        );

    }

}

async function guardarEdicionEvaluacion() {

    try {

        const id = document.getElementById(
            "editarEvaluacionId"
        ).value;

        const datos = {

            titulo:
                document.getElementById(
                    "editarTituloEvaluacion"
                ).value,

            fecha:
                document.getElementById(
                    "editarFechaEvaluacion"
                ).value,

            instructor:
                document.getElementById(
                    "editarInstructorEvaluacion"
                ).value,

            compania:
                document.getElementById(
                    "editarCompaniaEvaluacion"
                ).value,

            descripcion:
                document.getElementById(
                    "editarDescripcionEvaluacion"
                ).value

        };

        const response = await fetch(

            `/editar-evaluacion/${id}/`,

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json",

                    "X-CSRFToken":
                        getCookie("csrftoken")

                },

                body: JSON.stringify(
                    datos
                )

            }

        );

        const resultado =
            await response.json();

        if (resultado.success) {

            mostrarToast(

                "Evaluación actualizada",

                "success"

            );

            setTimeout(() => {

                location.reload();

            }, 1000);

        } else {

            mostrarToast(

                resultado.error,

                "error"

            );

        }

    } catch (error) {

        console.error(error);

        mostrarToast(

            "Error actualizando evaluación",

            "error"

        );

    }

}
