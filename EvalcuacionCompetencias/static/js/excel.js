window.subirExcel = function () {

    const archivo = document.getElementById("archivoExcel").files[0];
    const compania = document.getElementById("companiaExcelSeleccionada").value;

    if (!archivo) {
        mostrarToast("Seleccione un archivo Excel", "warning");
        return;
    }

    let formData = new FormData();
    formData.append("archivo", archivo);
    formData.append("compania", compania);

    fetch("/cargar-usuarios-excel/", {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(res => {

            console.log(res);

            if (res.error) {

                mostrarToast(
                    res.error,
                    "error"
                );

                return;
            }

            mostrarToast(
                res.mensaje,
                "success"
            );

            actualizarTarjetas();

            // MOSTRAR ERRORES DEL EXCEL

            if (

                res.errores &&

                res.errores.length > 0

            ) {

                Swal.fire({

                    icon: "warning",

                    title: "Usuarios omitidos",

                    html: `

                <div style="
                    text-align:left;
                    max-height:300px;
                    overflow:auto;
                    font-size:14px;
                ">

                    ${res.errores.map(
                        e => `• ${e}`
                    ).join("<br>")}

                </div>

            `,

                    width: 700
                });
            }
        });
};