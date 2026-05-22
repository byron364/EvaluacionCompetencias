function actualizarTarjetas() {
    fetch("/obtener-estadisticas/")
        .then(res => res.json())
        .then(data => {
            const soldados =
                document.getElementById("total-soldados");

            if (soldados) {

                soldados.textContent =
                    data.total_soldados;
            }

            const instructores =
                document.getElementById("total-instructores");

            if (instructores) {

                instructores.textContent =
                    data.total_instructores;
            }

            const activos =
                document.getElementById("total-activos");

            if (activos) {

                activos.textContent =
                    data.total_activos;
            }
            const cursos = document.getElementById("total-cursos");
            if (cursos) {
                cursos.textContent = data.total_cursos;
            }

            const evaluaciones = document.getElementById("total-evaluaciones");
            if (evaluaciones) {
                evaluaciones.textContent = data.total_evaluaciones;
            }

            const aprobados =
                document.getElementById("porcentaje-aprobados");

            if (aprobados) {

                aprobados.textContent =
                    data.porcentaje_aprobados + "%";
            }
        });
}

document.addEventListener("DOMContentLoaded", function () {
    actualizarTarjetas();
});