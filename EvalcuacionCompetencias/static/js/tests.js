let contadorPreguntas = 0;
let companiasTest = [];
let tiempoRestante = 0;
let intervaloTest = null;
let testActual = null;

// =====================================
// AGREGAR PREGUNTA
// =====================================

function agregarPregunta() {

    contadorPreguntas++;

    const contenedor =
        document.getElementById(
            "contenedorPreguntas"
        );

    const html = `

        <div
            class="card mb-4 p-3"
            id="pregunta-${contadorPreguntas}"
        >

            <div class="d-flex justify-content-between">

                <h5>
                    Pregunta ${contadorPreguntas}
                </h5>

                <button
                    class="btn btn-danger btn-sm"
                    onclick="eliminarPregunta(${contadorPreguntas})"
                >

                    ✖

                </button>

            </div>

            <!-- PREGUNTA -->

            <textarea
                class="form-control mt-2 pregunta-texto"
                rows="2"
                placeholder="Escriba la pregunta..."
            ></textarea>

            <!-- OPCIONES -->

            <div
                class="mt-3 opciones"
            >

                ${crearOpcion()}

                ${crearOpcion()}

            </div>

            <button
                class="btn btn-outline-primary btn-sm mt-3"
                onclick="agregarOpcion(${contadorPreguntas})"
            >

                ➕ Agregar Opción

            </button>

        </div>

    `;

    contenedor.innerHTML += html;

}
function crearOpcion() {

    return `

        <div class="input-group mb-2 opcion-item">

            <div class="input-group-text">

                <input
                    type="radio"
                    class="form-check-input correcta"
                    name="correcta-${Date.now()}"
                >

            </div>

            <input
                type="text"
                class="form-control opcion-texto"
                placeholder="Opción respuesta"
            >

        </div>

    `;
}
function agregarOpcion(id) {

    const pregunta = document.getElementById(
        `pregunta-${id}`
    );

    pregunta.querySelector(
        ".opciones"
    ).innerHTML += crearOpcion();

}
function eliminarPregunta(id){

    document.getElementById(
        `pregunta-${id}`
    ).remove();

}
async function guardarTest(){

    try {

        const preguntas = [];

        document.querySelectorAll(
            "#contenedorPreguntas .card"
        ).forEach(card => {

            const preguntaTexto =
                card.querySelector(
                    ".pregunta-texto"
                ).value;

            const opciones = [];

            card.querySelectorAll(
                ".opcion-item"
            ).forEach(opcion => {

                opciones.push({

                    texto:
                        opcion.querySelector(
                            ".opcion-texto"
                        ).value,

                    correcta:
                        opcion.querySelector(
                            ".correcta"
                        ).checked

                });

            });

            preguntas.push({

                pregunta:
                    preguntaTexto,

                opciones:
                    opciones

            });

        });

        // =====================================
        // DATOS
        // =====================================

        const datos = {

            titulo:
                document.getElementById(
                    "tituloTest"
                ).value,

            descripcion:
                document.getElementById(
                    "descripcionTest"
                ).value,

            instructor:
                document.getElementById(
                    "instructorTest"
                ).value,

            compania:
                document.getElementById(
                    "companiaTest"
                ).value,

            fecha_inicio:
                document.getElementById(
                    "fechaInicioTest"
                ).value,

            fecha_fin:
                document.getElementById(
                    "fechaFinTest"
                ).value,

            max_intentos:
                document.getElementById(
                    "intentosTest"
                ).value,

            tiempo_limite:
                document.getElementById(
                    "tiempoTest"
                ).value,

            preguntas:
                preguntas

        };

        console.log(datos);

        // =====================================
        // FETCH
        // =====================================

        const response = await fetch(

            "/crear-test/",

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

        if(resultado.success){

            mostrarToast(

                "✅ Test creado",

                "success"

            );

            setTimeout(() => {

                location.reload();

            }, 1500);

        } else {

            mostrarToast(

                resultado.error,

                "error"

            );

        }

    } catch(error){

        console.error(error);

        mostrarToast(

            "Error creando test",

            "error"

        );

    }

}

function editarTest(id){

    mostrarToast(

        `Editar test ${id}`,

        "info"

    );

}

// =====================================
// VER TEST
// =====================================

async function verTest(id){

    try {

        const response = await fetch(

            `/detalle-test/${id}/`

        );

        const data =
            await response.json();

        // =====================================
        // TITULO
        // =====================================

        document.getElementById(
            "tituloVerTest"
        ).textContent =
            data.titulo;

        // =====================================
        // INFO
        // =====================================

        document.getElementById(
            "infoTest"
        ).innerHTML = `

            <h5>

                ${data.compania}

            </h5>

            <p>

                <strong>Instructor:</strong>
                ${data.instructor}

            </p>

            <p>

                <strong>Inicio:</strong>
                ${data.fecha_inicio}

            </p>

            <p>

                <strong>Fin:</strong>
                ${data.fecha_fin}

            </p>

            <p>

                <strong>Tiempo:</strong>
                ${data.tiempo} min

            </p>

        `;

        // =====================================
        // SOLDADOS
        // =====================================

        const tabla =
            document.getElementById(
                "tablaSoldadosTest"
            );

        tabla.innerHTML = "";

        data.soldados.forEach(s => {

            tabla.innerHTML += `

                <tr>

                    <td>
                        ${s.apellidos}
                    </td>

                    <td>
                        ${s.nombres}
                    </td>

                    <td>
                        ${s.documento}
                    </td>

                    <td>
                        ${s.intentos}
                    </td>

                    <td>

                        ${s.nota}/100

                    </td>

                    <td>

                        ${
                            s.aprobado

                            ?

                            `<span class="badge bg-success">
                                APROBADO
                            </span>`

                            :

                            `<span class="badge bg-danger">
                                REPROBADO
                            </span>`
                        }

                    </td>

                </tr>

            `;

        });

        // =====================================
        // MODAL
        // =====================================

        const modal = new bootstrap.Modal(

            document.getElementById(
                "modalVerTest"
            )

        );

        modal.show();

    } catch(error){

        console.error(error);

    }

}

// =====================================
// ACTIVAR / INACTIVAR
// =====================================

async function cambiarEstadoTest(id){

    try {

        const response = await fetch(

            `/activar-test/${id}/`,

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

        if(data.success){

            mostrarToast(

                data.mensaje,

                "success"

            );

            setTimeout(() => {

                location.reload();

            }, 1000);

        }

    } catch(error){

        console.error(error);

    }

}

// =====================================
// CARGAR COMPAÑIAS TEST
// =====================================

async function cargarCompaniasTest(){

    try {

        const response = await fetch(

            "/buscar-companias/"

        );

        const data =
            await response.json();

        companiasTest =
            data.companias;

        console.log(
            companiasTest
        );

    } catch(error){

        console.error(error);

    }

}
// =====================================
// BUSCADOR COMPAÑIAS TEST
// =====================================

document.addEventListener(

    "input",

    function(e){

        if(
            e.target.id !==
            "buscadorCompaniaTest"
        ) return;

        const texto =
            e.target.value.toLowerCase();

        const lista =
            document.getElementById(
                "listaCompaniasTest"
            );

        lista.innerHTML = "";

        if(texto.length < 1){

            return;

        }

        const filtradas =
            companiasTest.filter(c =>

                c.nombre.toLowerCase()
                    .includes(texto)

            );

        filtradas.forEach(compania => {

            const item =
                document.createElement(
                    "button"
                );

            item.type = "button";

            item.className =
                "list-group-item list-group-item-action";

            item.innerHTML = `

                ${compania.nombre}

                <small class="text-muted">

                    (${compania.codigo})

                </small>

            `;

            item.onclick = () => {

                document.getElementById(
                    "buscadorCompaniaTest"
                ).value =
                    compania.nombre;

                document.getElementById(
                    "companiaTest"
                ).value =
                    compania.id;

                lista.innerHTML = "";

                console.log(
                    "COMPAÑIA:",
                    compania
                );

            };

            lista.appendChild(item);

        });

    }

);
document.addEventListener(

    "DOMContentLoaded",

    () => {

        cargarCompaniasTest();

    }

);

// =====================================
// DATATABLE TESTS
// =====================================

function iniciarTablaTests(){

    if ($.fn.DataTable.isDataTable('#tablaTests')) {

        $('#tablaTests').DataTable().destroy();

    }

    $('#tablaTests').DataTable({

        responsive: true,

        pageLength: 5,

        lengthMenu: [

            [5, 10, 25, 50],

            [5, 10, 25, 50]

        ],

        language: {

            url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json'

        },

        dom: 'Bfrtip',

        buttons: [

            {

                extend: 'excelHtml5',

                text: '📗 Excel',

                className:
                    'btn btn-success btn-sm'

            },

            {

                extend: 'pdfHtml5',

                text: '📕 PDF',

                className:
                    'btn btn-danger btn-sm'

            },

            {

                extend: 'print',

                text: '🖨️ Imprimir',

                className:
                    'btn btn-secondary btn-sm'

            }

        ]

    });

}

// =====================================
// RESOLVER TEST
// =====================================

async function resolverTest(id){

    try {

        const response = await fetch(

            `/obtener-test/${id}/`

        );

        const data =
            await response.json();

        console.log(data);

        // =====================================
        // GUARDAR TEST ACTUAL
        // =====================================

        testActual = data.id;

        // =====================================
        // TITULO
        // =====================================

        document.getElementById(
            "tituloResolverTest"
        ).textContent =
            data.titulo;

        // =====================================
        // TEMPORIZADOR
        // =====================================

        tiempoRestante =
            data.tiempo_limite * 60;

        iniciarTemporizador();

        // =====================================
        // CONTENEDOR
        // =====================================

        const contenedor =
            document.getElementById(
                "contenedorResolverTest"
            );

        contenedor.innerHTML = "";

        // =====================================
        // PREGUNTAS
        // =====================================

        data.preguntas.forEach((p, index) => {

            let opcionesHTML = "";

            p.opciones.forEach(op => {

                opcionesHTML += `

                    <div class="form-check mb-2">

                        <input
                            class="form-check-input"
                            type="radio"
                            name="pregunta-${p.id}"
                            value="${op.id}"
                        >

                        <label
                            class="form-check-label"
                        >

                            ${op.texto}

                        </label>

                    </div>

                `;

            });

            contenedor.innerHTML += `

                <div class="card mb-4 p-3">

                    <h5>

                        ${index + 1}.
                        ${p.pregunta}

                    </h5>

                    <hr>

                    ${opcionesHTML}

                </div>

            `;

        });

        // =====================================
        // ABRIR MODAL
        // =====================================

        const modal = new bootstrap.Modal(

            document.getElementById(
                "modalResolverTest"
            )

        );

        modal.show();

    } catch(error){

        console.error(error);

        mostrarToast(

            "Error cargando test",

            "error"

        );

    }

}

// =====================================
// TEMPORIZADOR
// =====================================

function iniciarTemporizador(){

    clearInterval(
        intervaloTest
    );

    intervaloTest = setInterval(() => {

        if(tiempoRestante <= 0){

            clearInterval(
                intervaloTest
            );

            mostrarToast(

                "Tiempo agotado",

                "error"

            );

            enviarTest();

            return;

        }

        tiempoRestante--;

        const minutos = Math.floor(

            tiempoRestante / 60

        );

        const segundos =
            tiempoRestante % 60;

        document.getElementById(
            "temporizadorTest"
        ).textContent =

            `${String(minutos).padStart(2,'0')}:${String(segundos).padStart(2,'0')}`;

    }, 1000);

}

async function enviarTest(){

    try {

        const respuestas = [];

        document.querySelectorAll(

            "#contenedorResolverTest .card"

        ).forEach(card => {

            const radio =
                card.querySelector(

                    "input[type='radio']:checked"

                );

            if(radio){

                respuestas.push({

                    opcion_id:
                        radio.value

                });

            }

        });

        // =====================================
        // FETCH
        // =====================================

        const response = await fetch(

            "/finalizar-test/",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json",

                    "X-CSRFToken":
                        getCookie("csrftoken")

                },

                body: JSON.stringify({

                    test_id:
                        testActual,

                    respuestas:
                        respuestas

                })

            }

        );

        const resultado =
            await response.json();

        console.log(resultado);

        // =====================================
        // RESULTADO
        // =====================================

        if(resultado.success){

            clearInterval(
                intervaloTest
            );

            mostrarToast(

                `Nota: ${resultado.nota}`,

                resultado.aprobado
                    ? "success"
                    : "warning"

            );

            setTimeout(() => {

                location.reload();

            }, 3000);

        } else {

            mostrarToast(

                resultado.error,

                "error"

            );

        }

    } catch(error){

        console.error(error);

        mostrarToast(

            "Error enviando test",

            "error"

        );

    }

}