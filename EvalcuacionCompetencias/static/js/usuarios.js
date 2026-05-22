// ========================================
// USUARIOS.JS
// ========================================

// ========================================
// VARIABLES GLOBALES
// ========================================

window.huellaCapturada = false;
window.documentoHuella = null;

// ========================================
// EVENTOS PRINCIPALES
// ========================================

window.inicializarUsuarios = function () {

    inicializarEventosUsuarios();

    inicializarBuscadorCompanias();

    inicializarBuscadorCompaniasExcel();

    inicializarRoles();

};

// ========================================
// EVENTOS CLICK
// ========================================

function inicializarEventosUsuarios() {

    document.addEventListener("click", async function (e) {

        // ========================================
        // CREAR USUARIO
        // ========================================

        if (e.target.closest("#btnCrearUsuario")) {

            await crearUsuario();

            return;
        }

        // ========================================
        // ELIMINAR USUARIO
        // ========================================

        const btnEliminar =
            e.target.closest(".btn-eliminar");

        if (btnEliminar) {

            await eliminarUsuario(btnEliminar);

            return;
        }

        // ========================================
        // EDITAR USUARIO
        // ========================================

        const btnEditar =
            e.target.closest(".btn-editar");

        if (btnEditar) {

            await editarUsuario(btnEditar);

            return;
        }

    });

}

// ========================================
// REGISTRAR HUELLA
// ========================================

window.registrarHuella = async function () {

    const documento =
        document.getElementById("documento")?.value
            .trim();

    if (!documento) {

        mostrarToast(
            "⚠️ Ingrese documento primero",
            "warning"
        );

        return;
    }

    try {

        mostrarToast(
            "🔄 Abriendo huellero...",
            "info"
        );

        const response =
            await fetch(
                `/abrir-huellero/${documento}/`
            );

        const data =
            await response.json();

        if (!data.success) {

            mostrarToast(
                "❌ No se pudo abrir huellero",
                "error"
            );

            return;
        }

        // ========================================
        // ESPERAR JSON TEMPORAL
        // ========================================

        let intentos = 0;

        const intervalo =
            setInterval(async () => {

                intentos++;

                try {

                    const validar =
                        await fetch(
                            `/validar-huella-temp/${documento}/`
                        );

                    const resultado =
                        await validar.json();

                    if (resultado.success) {

                        clearInterval(intervalo);

                        window.huellaCapturada = true;

                        window.documentoHuella =
                            documento;

                        mostrarToast(
                            "✅ Huella capturada correctamente",
                            "success"
                        );

                        // ========================================
                        // MOSTRAR PREVIEW
                        // ========================================

                        if (resultado.imagen) {

                            const preview =
                                document.getElementById(
                                    "previewHuella"
                                );

                            if (preview) {

                                preview.src =
                                    `data:image/png;base64,${resultado.imagen}`;

                                preview.style.display =
                                    "block";
                            }
                        }

                    }

                    // ========================================
                    // TIMEOUT
                    // ========================================

                    if (intentos >= 40) {

                        clearInterval(intervalo);

                        mostrarToast(
                            "⚠️ Tiempo agotado para captura",
                            "warning"
                        );
                    }

                } catch (error) {

                    console.error(error);
                }

            }, 500);

    } catch (error) {

        console.error(error);

        mostrarToast(
            "❌ Error abriendo huellero",
            "error"
        );
    }

};

// ========================================
// CREAR USUARIO
// ========================================

window.crearUsuario = async function () {

    // ========================================
    // ELEMENTOS
    // ========================================

    const elementos = {

        nombres:
            document.getElementById("nombres"),

        apellidos:
            document.getElementById("apellidos"),

        email:
            document.getElementById("email"),

        documento:
            document.getElementById("documento"),

        grado:
            document.getElementById("grado"),

        rol:
            document.getElementById("rol"),

        compania:
            document.getElementById(
                "companiaSeleccionada"
            ),

    };

    // ========================================
    // DATA
    // ========================================

    const data = {

        nombres:
            elementos.nombres?.value.trim(),

        apellidos:
            elementos.apellidos?.value.trim(),

        email:
            elementos.email?.value.trim(),

        documento:
            elementos.documento?.value.trim(),

        grado:
            elementos.grado?.value.trim(),

        rol:
            elementos.rol?.value,

        compania:
            elementos.compania?.value,

    };

    // ========================================
    // VALIDAR CAMPOS
    // ========================================

    if (
        !data.nombres ||
        !data.apellidos ||
        !data.email ||
        !data.documento ||
        !data.compania
    ) {

        mostrarToast(
            "⚠️ Complete los campos obligatorios",
            "warning"
        );

        return;
    }

    // ========================================
    // VALIDAR HUELLA TEMPORAL
    // ========================================

    try {

        const validarHuella =
            await fetch(
                `/validar-huella-temp/${data.documento}/`
            );

        const resultadoHuella =
            await validarHuella.json();

        if (!resultadoHuella.success) {

            mostrarToast(
                "⚠️ No existe huella temporal",
                "warning"
            );

            return;
        }

    } catch (error) {

        console.error(error);

        mostrarToast(
            "❌ Error validando huella",
            "error"
        );

        return;
    }

    // ========================================
    // VALIDAR EMAIL
    // ========================================

    if (data.rol === "soldado") {

        if (
            !data.email.endsWith(
                "@buzonejercito.mil.co"
            )
        ) {

            mostrarToast(
                "⚠️ El soldado debe usar @buzonejercito.mil.co",
                "warning"
            );

            return;
        }

    } else {

        if (
            !data.email.endsWith(
                "@ejercito.mil.co"
            )
        ) {

            mostrarToast(
                "⚠️ Debe usar @ejercito.mil.co",
                "warning"
            );

            return;
        }

    }

    // ========================================
    // CREAR USUARIO
    // ========================================

    try {

        mostrarToast(
            "🔄 Creando usuario...",
            "info"
        );

        const response =
            await fetch(
                "/crear-usuario/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );

        const resultado =
            await response.json();

        if (resultado.error) {

            mostrarToast(
                "❌ " + resultado.error,
                "error"
            );

            return;
        }

        // ========================================
        // ÉXITO
        // ========================================

        mostrarToast(
            "✅ Usuario creado correctamente",
            "success"
        );

        // ========================================
        // LIMPIAR HUELLA TEMP
        // ========================================

        try {

            await fetch(
                `/eliminar-huella-temp/${data.documento}/`
            );

        } catch (error) {

            console.error(error);
        }

        // ========================================
        // RESETEAR VARIABLES
        // ========================================

        window.huellaCapturada = false;

        window.documentoHuella = null;

        // ========================================
        // LIMPIAR FORMULARIO
        // ========================================

        elementos.nombres.value = "";
        elementos.apellidos.value = "";
        elementos.email.value = "";
        elementos.documento.value = "";
        elementos.grado.value = "";

        if (elementos.compania) {

            elementos.compania.value = "";
        }

        if (elementos.rol) {

            elementos.rol.value =
                "soldado";
        }

        // ========================================
        // LIMPIAR BUSCADOR
        // ========================================

        const buscador =
            document.getElementById(
                "buscarCompania"
            );

        if (buscador) {

            buscador.value = "";
        }

        // ========================================
        // LIMPIAR RESULTADOS
        // ========================================

        const resultados =
            document.getElementById(
                "resultadosCompanias"
            );

        if (resultados) {

            resultados.innerHTML = "";

            resultados.style.display =
                "none";
        }

        // ========================================
        // LIMPIAR PREVIEW
        // ========================================

        const preview =
            document.getElementById(
                "previewHuella"
            );

        if (preview) {

            preview.src = "";

            preview.style.display =
                "none";
        }

        // ========================================
        // RECARGAR VISTA SPA
        // ========================================

        if (window.cargarVista) {

            setTimeout(() => {

                window.cargarVista(
                    "/usuarios/"
                );

            }, 1000);
        }

    } catch (error) {

        console.error(error);

        mostrarToast(
            "❌ Error del servidor",
            "error"
        );
    }

};

// ========================================
// ELIMINAR USUARIO
// ========================================

async function eliminarUsuario(boton) {

    const userId =
        boton.dataset.id;

    Swal.fire({

        title:
            "¿Eliminar usuario?",

        text:
            "Esta acción no se puede deshacer",

        icon:
            "warning",

        showCancelButton:
            true,

        confirmButtonColor:
            "#198754",

        cancelButtonColor:
            "#dc3545",

        confirmButtonText:
            "Sí, eliminar",

        cancelButtonText:
            "Cancelar"

    }).then(async (result) => {

        if (!result.isConfirmed)
            return;

        try {

            const response =
                await fetch(
                    `/eliminar-usuario/${userId}/`,
                    {
                        method: "POST"
                    }
                );

            const data =
                await response.json();

            if (data.error) {

                mostrarToast(
                    data.error,
                    "error"
                );

                return;
            }

            boton.closest("tr").remove();

            mostrarToast(
                "✅ Usuario eliminado",
                "success"
            );

        } catch (error) {

            console.error(error);

            mostrarToast(
                "❌ Error eliminando usuario",
                "error"
            );
        }

    });

}

// ========================================
// EDITAR USUARIO
// ========================================

async function editarUsuario(boton) {

    const userId =
        boton.dataset.id;

    const nombre =
        boton.dataset.nombre;

    const apellido =
        boton.dataset.apellido;

    const email =
        boton.dataset.email;

    const rol =
        boton.dataset.rol;

    const activo =
        boton.dataset.activo === "True";

    Swal.fire({

        title:
            "Editar Usuario",

        html: `

            <input 
                id="swal-nombre" 
                class="swal2-input" 
                placeholder="Nombre" 
                value="${nombre}"
            >

            <input 
                id="swal-apellido" 
                class="swal2-input" 
                placeholder="Apellido" 
                value="${apellido}"
            >

            <input 
                id="swal-email" 
                class="swal2-input" 
                placeholder="Correo" 
                value="${email}"
            >

            <select 
                id="swal-rol" 
                class="swal2-input"
            >

                <option value="soldado"
                    ${rol === "soldado"
                ? "selected"
                : ""}>
                    Soldado
                </option>

                <option value="instructor"
                    ${rol === "instructor"
                ? "selected"
                : ""}>
                    Instructor
                </option>

                <option value="admin"
                    ${rol === "admin"
                ? "selected"
                : ""}>
                    Admin
                </option>

            </select>

            <select 
                id="swal-activo" 
                class="swal2-input"
            >

                <option value="true"
                    ${activo
                ? "selected"
                : ""}>
                    Activo
                </option>

                <option value="false"
                    ${!activo
                ? "selected"
                : ""}>
                    Inactivo
                </option>

            </select>
        `,

        confirmButtonText:
            "Guardar cambios",

        showCancelButton:
            true,

        cancelButtonText:
            "Cancelar",

        confirmButtonColor:
            "#198754",

        preConfirm: () => {

            return {

                nombre:
                    document.getElementById(
                        "swal-nombre"
                    ).value,

                apellido:
                    document.getElementById(
                        "swal-apellido"
                    ).value,

                email:
                    document.getElementById(
                        "swal-email"
                    ).value,

                rol:
                    document.getElementById(
                        "swal-rol"
                    ).value,

                activo:
                    document.getElementById(
                        "swal-activo"
                    ).value === "true"
            };
        }

    }).then(async (result) => {

        if (!result.isConfirmed)
            return;

        try {

            const response =
                await fetch(
                    `/editar-usuario/${userId}/`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                result.value
                            )
                    }
                );

            const data =
                await response.json();

            Swal.fire({

                title:
                    "Actualizado",

                text:
                    data.mensaje,

                icon:
                    "success",

                confirmButtonColor:
                    "#198754"

            });

        } catch (error) {

            console.error(error);

            mostrarToast(
                "❌ Error editando usuario",
                "error"
            );
        }

    });

}

// ========================================
// BUSCADOR COMPAÑÍAS
// ========================================

function inicializarBuscadorCompanias() {

    const dataElement =
        document.getElementById(
            "companias-data"
        );

    if (!dataElement)
        return;

    let companias = [];

    try {

        companias =
            JSON.parse(
                dataElement.textContent
            );

    } catch (error) {

        console.error(error);

        return;
    }

    const buscador =
        document.getElementById(
            "buscarCompania"
        );

    const resultados =
        document.getElementById(
            "resultadosCompanias"
        );

    const hidden =
        document.getElementById(
            "companiaSeleccionada"
        );

    if (
        !buscador ||
        !resultados ||
        !hidden
    )
        return;

    let timeoutBusqueda;

    buscador.addEventListener(
        "input",
        function () {

            clearTimeout(
                timeoutBusqueda
            );

            timeoutBusqueda =
                setTimeout(() => {

                    const texto =
                        buscador.value
                            .toLowerCase()
                            .trim();

                    resultados.innerHTML = "";

                    if (!texto) {

                        resultados.style.display =
                            "none";

                        return;
                    }

                    const filtradas =
                        companias.filter(c =>

                            c.nombre
                                .toLowerCase()
                                .includes(texto)

                            ||

                            c.batallon
                                .toLowerCase()
                                .includes(texto)
                        );

                    if (
                        filtradas.length === 0
                    ) {

                        resultados.innerHTML = `
                            <div class="item-batallon">
                                No se encontraron compañías
                            </div>
                        `;

                        resultados.style.display =
                            "block";

                        return;
                    }

                    filtradas.forEach(c => {

                        const item =
                            document.createElement(
                                "div"
                            );

                        item.className =
                            "item-batallon";

                        item.innerHTML = `
                            <div>
                                <strong>${c.nombre}</strong><br>
                                <small>${c.batallon}</small>
                            </div>
                        `;

                        item.addEventListener(
                            "click",
                            function () {

                                buscador.value =
                                    c.nombre;

                                hidden.value =
                                    c.id;

                                resultados.style.display =
                                    "none";
                            }
                        );

                        resultados.appendChild(
                            item
                        );

                    });

                    resultados.style.display =
                        "block";

                }, 300);

        }
    );

}

// ========================================
// BUSCADOR EXCEL
// ========================================

function inicializarBuscadorCompaniasExcel() {

    const dataElement =
        document.getElementById(
            "companias-data"
        );

    if (!dataElement)
        return;

    let companias = [];

    try {

        companias =
            JSON.parse(
                dataElement.textContent
            );

    } catch (error) {

        console.error(error);

        return;
    }

    const buscador =
        document.getElementById(
            "buscarCompaniaExcel"
        );

    const resultados =
        document.getElementById(
            "resultadosCompaniasExcel"
        );

    const hidden =
        document.getElementById(
            "companiaExcelSeleccionada"
        );

    if (
        !buscador ||
        !resultados ||
        !hidden
    )
        return;

    buscador.addEventListener(
        "input",
        function () {

            const texto =
                buscador.value
                    .toLowerCase()
                    .trim();

            resultados.innerHTML = "";

            if (!texto) {

                resultados.style.display =
                    "none";

                return;
            }

            const filtradas =
                companias.filter(c =>

                    c.nombre
                        .toLowerCase()
                        .includes(texto)

                    ||

                    c.batallon
                        .toLowerCase()
                        .includes(texto)
                );

            filtradas.forEach(c => {

                const item =
                    document.createElement(
                        "div"
                    );

                item.className =
                    "item-batallon";

                item.innerHTML = `
                    <div>
                        <strong>${c.nombre}</strong><br>
                        <small>${c.batallon}</small>
                    </div>
                `;

                item.addEventListener(
                    "click",
                    function () {

                        buscador.value =
                            c.nombre;

                        hidden.value =
                            c.id;

                        resultados.style.display =
                            "none";
                    }
                );

                resultados.appendChild(
                    item
                );

            });

            resultados.style.display =
                "block";
        }
    );

}

// ========================================
// ROLES
// ========================================

function inicializarRoles() {

    const rolSelect =
        document.getElementById(
            "rol"
        );

    const contenedorGrado =
        document.getElementById(
            "contenedorGrado"
        );

    if (
        !rolSelect ||
        !contenedorGrado
    )
        return;

    function validarRol() {

        if (
            rolSelect.value ===
            "soldado"
        ) {

            contenedorGrado.style.display =
                "none";

        } else {

            contenedorGrado.style.display =
                "block";
        }
    }

    validarRol();

    rolSelect.addEventListener(
        "change",
        validarRol
    );

}

async function registrarHuellaBiometrica(documento) {

    if (!documento) {

        mostrarToast(
            "⚠️ Documento inválido",
            "warning"
        );

        return;
    }

    try {

        mostrarToast(
            "🔄 Abriendo huellero...",
            "info"
        );

        // =====================================
        // ABRIR HUELLERO
        // =====================================

        const response =
            await fetch(
                `/abrir-huellero/${documento}/`
            );

        const data =
            await response.json();

        if (!data.success) {

            mostrarToast(
                "❌ Error abriendo huellero",
                "error"
            );

            return;
        }

        mostrarToast(
            "👆 Capture la huella",
            "info"
        );

        // =====================================
        // ESPERAR JSON TEMPORAL
        // =====================================

        let intentos = 0;

        const intervalo =
            setInterval(async () => {

                intentos++;

                try {

                    const validar =
                        await fetch(
                            `/validar-huella-temp/${documento}/`
                        );

                    const resultado =
                        await validar.json();

                    // =====================================
                    // HUELLA DETECTADA
                    // =====================================

                    if (resultado.success) {

                        clearInterval(
                            intervalo
                        );

                        mostrarToast(
                            "✅ Huella detectada",
                            "success"
                        );

                        // =====================================
                        // GUARDAR EN BD
                        // =====================================

                        const guardar =
                            await fetch(
                                `/registrar-huella-usuario/${documento}/`
                            );

                        const respuesta =
                            await guardar.json();

                        if (!respuesta.success) {

                            mostrarToast(
                                "❌ Error guardando huella",
                                "error"
                            );

                            return;
                        }

                        mostrarToast(
                            "✅ Huella registrada correctamente",
                            "success"
                        );

                        // =====================================
                        // RECARGAR VISTA
                        // =====================================

                        setTimeout(() => {

                            if (
                                window.cargarVista
                            ) {

                                window.cargarVista(
                                    "/biometrico/"
                                );

                            } else {

                                location.reload();
                            }

                        }, 1000);
                    }

                    // =====================================
                    // TIMEOUT
                    // =====================================

                    if (intentos >= 40) {

                        clearInterval(
                            intervalo
                        );

                        mostrarToast(
                            "⚠️ Tiempo agotado",
                            "warning"
                        );
                    }

                } catch (error) {

                    console.error(error);
                }

            }, 500);

    } catch (error) {

        console.error(error);

        mostrarToast(
            "❌ Error del sistema",
            "error"
        );
    }
};

// ========================================
// EVENTO BIOMÉTRICO
// ========================================

document.addEventListener(
    "click",
    async function (e) {

        const boton =
            e.target.closest(
                ".btn-registrar-biometria"
            );

        if (!boton)
            return;

        const documento =
            boton.dataset.documento;

        await registrarHuellaBiometrica(
            documento
        );
    }
);