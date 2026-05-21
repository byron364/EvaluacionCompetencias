document.addEventListener("DOMContentLoaded", function () {

    const content = document.getElementById("contenido-dinamico");
    const loader = document.getElementById("loader");
    const HOME_URL = "/admin-dashboard-partial/";

    function cargarVista(url, guardar = true) {


        loader.classList.add("active");

        content.classList.add("fade-out");
        fetch(url)
            .then(res => res.text())
            .then(data => {

                const parser = new DOMParser();
                const doc = parser.parseFromString(data, "text/html");
                const nuevo = doc.getElementById("contenido-parcial");

                if (nuevo) {
                    content.innerHTML = nuevo.innerHTML;

                    if (url.includes("/usuarios/") ||
                        url.includes("/biometrico/")) {

                        inicializarUsuarios();

                    }

                    // MAPA BATALLONES
                    if (document.getElementById("mapaBatallones")) {

                        setTimeout(() => {

                            // evitar duplicar mapa
                            const mapaContainer =
                                L.DomUtil.get('mapaBatallones');

                            if (mapaContainer != null) {

                                mapaContainer._leaflet_id = null;

                            }

                            const mapa = L.map(
                                'mapaBatallones'
                            ).setView(
                                [4.5709, -74.2973],
                                5
                            );

                            L.tileLayer(
                                'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                                {
                                    attribution: '&copy; OpenStreetMap'
                                }
                            ).addTo(mapa);

                            // BOGOTÁ
                            L.marker([4.7110, -74.0721])
                                .addTo(mapa)
                                .bindPopup(`
                <b>Batallón Bogotá</b><br>
                Bogotá
            `);

                            // MEDELLÍN
                            L.marker([6.2442, -75.5812])
                                .addTo(mapa)
                                .bindPopup(`
                <b>Batallón Medellín</b><br>
                Medellín
            `);

                            // CALI
                            L.marker([3.4516, -76.5320])
                                .addTo(mapa)
                                .bindPopup(`
                <b>Batallón Cali</b><br>
                Cali
            `);

                        }, 300);
                    }
                    // Si estamos en usuarios, actualizar cards automáticamente 
                    if (url.includes("/usuarios/")) {
                        actualizarTarjetas();
                    }

                    // TABLA BATALLONES
                    if ($("#tablaBatallones").length) {

                        $("#tablaBatallones").DataTable({

                            pageLength: 5,

                            lengthChange: false,

                            ordering: true,

                            searching: true,

                            info: true,

                            destroy: true,

                            responsive: true,

                            language: {

                                search: "Buscar batallón:",

                                zeroRecords:
                                    "No se encontraron batallones",

                                info:
                                    "Mostrando _START_ a _END_ de _TOTAL_ batallones",

                                infoEmpty:
                                    "No hay batallones disponibles",

                                paginate: {

                                    previous: "Anterior",

                                    next: "Siguiente"
                                }
                            }
                        });
                    }

                    // Inicializar DataTable si existe la tabla
                    if ($("#tablaUsuarios").length) {
                        $("#tablaUsuarios").DataTable({
                            pageLength: 5,
                            lengthChange: false,
                            ordering: true,
                            searching: true,
                            info: true,
                            destroy: true,

                            language: {
                                search: "Buscar usuario:",
                                zeroRecords: "No se encontraron usuarios",
                                info: "Mostrando _START_ a _END_ de _TOTAL_ usuarios",
                                infoEmpty: "No hay usuarios disponibles",
                                paginate: {
                                    previous: "Anterior",
                                    next: "Siguiente"
                                }
                            }
                        });
                    }

                    if ($("#tablaBiometrico").length) {

                        $("#tablaBiometrico").DataTable({

                            pageLength: 5,

                            lengthChange: false,

                            ordering: true,

                            searching: true,

                            info: true,

                            destroy: true,

                            responsive: true,

                            language: {

                                search: "Buscar usuario:",

                                zeroRecords:
                                    "No se encontraron usuarios",

                                info:
                                    "Mostrando _START_ a _END_ de _TOTAL_ usuarios",

                                infoEmpty:
                                    "No hay usuarios disponibles",

                                paginate: {

                                    previous: "Anterior",

                                    next: "Siguiente"
                                }
                            }
                        });
                    }

                }
                // TABLA CURSOS
                if ($("#tablaCursos").length) {

                    $("#tablaCursos").DataTable({
                        pageLength: 5,
                        lengthChange: false,
                        ordering: true,
                        searching: true,
                        info: true,
                        destroy: true,

                        language: {
                            search: "Buscar curso:",
                            zeroRecords: "No se encontraron cursos",
                            info: "Mostrando _START_ a _END_ de _TOTAL_ cursos",
                            infoEmpty: "No hay cursos disponibles",
                            paginate: {
                                previous: "Anterior",
                                next: "Siguiente"
                            }
                        }
                    });
                }

                // TABLA COMPAÑÍAS
                if ($("#tablaCompanias").length) {

                    $("#tablaCompanias").DataTable({
                        pageLength: 5,
                        lengthChange: false,
                        ordering: true,
                        searching: true,
                        info: true,
                        destroy: true,

                        language: {
                            search: "Buscar compañía:",
                            zeroRecords: "No se encontraron compañías",
                            info: "Mostrando _START_ a _END_ de _TOTAL_ compañías",
                            infoEmpty: "No hay compañías disponibles",
                            paginate: {
                                previous: "Anterior",
                                next: "Siguiente"
                            }
                        }
                    });
                }

                // TABLA COMPAÑÍAS
                if ($("#tablaTests").length) {

                    $("#tablaTests").DataTable({
                        pageLength: 5,
                        lengthChange: false,
                        ordering: true,
                        searching: true,
                        info: true,
                        destroy: true,

                        language: {
                            search: "Buscar test:",
                            zeroRecords: "No se encontraron tests",
                            info: "Mostrando _START_ a _END_ de _TOTAL_ tests",
                            infoEmpty: "No hay tests disponibles",
                            paginate: {
                                previous: "Anterior",
                                next: "Siguiente"
                            }
                        }
                    });
                }


                // Ocultar loader al terminar
                setTimeout(() => { loader.classList.remove("active"); content.classList.remove("fade-out"); content.classList.add("fade-in"); }, 500);

                if (guardar) {
                    sessionStorage.setItem("ultimaVista", url);

                    history.replaceState(
                        { url: url },
                        "",
                        "/admin-dashboard/"
                    );
                }
            })
            .catch((error) => {
                console.error("Error cargando vista:", error);

                // Ocultar loader también si falla
                setTimeout(() => { loader.classList.remove("active"); content.classList.remove("fade-out"); }, 500);
            });
    }

    // Eventos menú lateral SPA
    document.querySelectorAll(".nav-link-spa").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();

            // quitar active de todos
            document.querySelectorAll(".nav-link-spa").forEach(item => {
                item.classList.remove("active");
            });

            // activar solo el actual
            this.classList.add("active");

            cargarVista(this.dataset.url);
        });
    });


    // Restaurar última vista abierta
    const ultimaVista = sessionStorage.getItem("ultimaVista");

    if (ultimaVista) {

        // activar menú correcto
        document.querySelectorAll(".nav-link-spa").forEach(link => {
            link.classList.remove("active");

            if (link.dataset.url === ultimaVista) {
                link.classList.add("active");
            }
        });

        // cargar última vista SIN cambiar URL
        cargarVista(ultimaVista, false);

    } else {

        cargarVista(HOME_URL, false);
    }

});
