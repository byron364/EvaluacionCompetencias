$(document).ready(function () {

    $('#tablaBatallones').DataTable({

        responsive: true,

        language: {

            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
        }

    });

});
$(document).ready(function () {

    $('#tablaCompanias').DataTable({

        responsive: true,

        language: {

            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
        }

    });

});
// TABLA BIOMÉTRICO
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