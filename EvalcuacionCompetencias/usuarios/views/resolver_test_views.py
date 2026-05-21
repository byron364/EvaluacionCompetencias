from django.views.decorators.http import require_POST

from django.http import JsonResponse

from django.utils import timezone

import json

from ..models import (

    Test,

    TestAsignado,

    RespuestaUsuario,

    OpcionRespuesta

)

from ..utils import calcular_nota

# =========================================
# FINALIZAR TEST
# =========================================

@require_POST
def finalizar_test(request):

    try:

        data = json.loads(
            request.body
        )

        test_id = data.get(
            "test_id"
        )

        respuestas = data.get(
            "respuestas",
            []
        )

        usuario = request.user

        # =====================================
        # TEST
        # =====================================

        test = Test.objects.get(
            id=test_id
        )

        # =====================================
        # ASIGNACION
        # =====================================

        asignacion = TestAsignado.objects.get(

            test=test,

            soldado=usuario
        )

        # =====================================
        # VALIDAR INTENTOS
        # =====================================

        if (

            asignacion.intentos_realizados

            >= test.max_intentos

        ):

            return JsonResponse({

                "error":
                    "Intentos agotados"

            }, status=400)

        # =====================================
        # LIMPIAR RESPUESTAS ANTERIORES
        # =====================================

        RespuestaUsuario.objects.filter(

            asignacion=asignacion

        ).delete()

        # =====================================
        # CONTADOR
        # =====================================

        correctas = 0

        # =====================================
        # GUARDAR RESPUESTAS
        # =====================================

        for r in respuestas:

            opcion = OpcionRespuesta.objects.get(

                id=r["opcion_id"]

            )

            es_correcta = (
                opcion.es_correcta
            )

            if es_correcta:

                correctas += 1

            RespuestaUsuario.objects.create(

                asignacion=asignacion,

                pregunta=opcion.pregunta,

                opcion=opcion,

                es_correcta=es_correcta
            )

        # =====================================
        # CALCULAR NOTA
        # =====================================

        nota = calcular_nota(

            test,

            correctas

        )

        aprobado = (
            nota >= test.nota_aprobacion
        )

        # =====================================
        # ACTUALIZAR ASIGNACION
        # =====================================

        asignacion.nota = nota

        asignacion.aprobado = aprobado

        asignacion.completado = True

        asignacion.intentos_realizados += 1

        asignacion.finalizacion_test = (
            timezone.now()
        )

        asignacion.save()

        # =====================================
        # RESPUESTA
        # =====================================

        return JsonResponse({

            "success": True,

            "nota":
                nota,

            "correctas":
                correctas,

            "total":
                test.preguntas.count(),

            "aprobado":
                aprobado

        })

    except Exception as e:

        return JsonResponse({

            "error":
                str(e)

        }, status=500)
    

# =========================================
# OBTENER TEST
# =========================================

def obtener_test(

    request,

    test_id

):

    try:

        test = Test.objects.prefetch_related(

            "preguntas__opciones"

        ).get(id=test_id)

        preguntas = []

        for pregunta in test.preguntas.all():

            opciones = []

            for opcion in pregunta.opciones.all():

                opciones.append({

                    "id":
                        opcion.id,

                    "texto":
                        opcion.texto

                })

            preguntas.append({

                "id":
                    pregunta.id,

                "pregunta":
                    pregunta.pregunta,

                "opciones":
                    opciones

            })

        return JsonResponse({

            "id":
                test.id,

            "titulo":
                test.titulo,

            "descripcion":
                test.descripcion,

            "tiempo_limite":
                test.tiempo_limite,

            "preguntas":
                preguntas

        })

    except Test.DoesNotExist:

        return JsonResponse({

            "error":
                "Test no encontrado"

        }, status=404)
