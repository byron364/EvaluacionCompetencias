window.registrarHuella = function () {

    const documento =
        document.getElementById(
            "documento"
        )?.value;

    if (!documento) {

        mostrarToast(
            "⚠️ Ingrese documento",
            "warning"
        );

        return;
    }

    fetch(`/abrir-huellero/${documento}/`)

        .then(response => response.json())

        .then(data => {

            if (data.success) {

                mostrarToast(
                    "✅ Huellero abierto correctamente",
                    "success"
                );

            } else {

                mostrarToast(
                    "❌ Error abriendo huellero",
                    "error"
                );
            }

        })

        .catch(error => {

            console.error(error);

            mostrarToast(
                "❌ Error del servidor",
                "error"
            );

        });

}