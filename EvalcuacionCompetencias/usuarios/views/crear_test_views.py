from django.views.decorators.http import require_POST

from django.contrib.auth.models import User

from django.http import JsonResponse

from datetime import datetime

import json
from django.shortcuts import render

from ..models import (

    Test,

    PreguntaTest,

    OpcionRespuesta,

    TestAsignado,

    Compania

)

# =========================================
# ADMIN TESTS
# =========================================

def admin_test(request):

    tests = Test.objects.select_related(

        "compania",

        "instructor"

    ).all().order_by("-id")

    instructores = User.objects.filter(
        groups__name="Instructor"
    )

    companias = Compania.objects.all()

    context = {

        "tests":
            tests,

        "instructores":
            instructores,

        "companias":
            companias

    }

    return render(

        request,

        "admin_test.html",

        context
    )

# =========================================
# CREAR TEST
# =========================================

@require_POST
def crear_test(request):

    try:

        data = json.loads(
            request.body
        )

        # =====================================
        # DATOS TEST
        # =====================================

        titulo = data.get(
            "titulo"
        )

        descripcion = data.get(
            "descripcion"
        )

        instructor_id = data.get(
            "instructor"
        )

        compania_id = data.get(
            "compania"
        )

        fecha_inicio = data.get(
            "fecha_inicio"
        )

        fecha_fin = data.get(
            "fecha_fin"
        )

        max_intentos = data.get(
            "max_intentos",
            1
        )

        tiempo_limite = data.get(
            "tiempo_limite",
            30
        )

        preguntas = data.get(
            "preguntas",
            []
        )

        # =====================================
        # VALIDACIONES
        # =====================================

        if not titulo:

            return JsonResponse({

                "error":
                    "Título obligatorio"

            }, status=400)

        if len(preguntas) == 0:

            return JsonResponse({

                "error":
                    "Debe agregar preguntas"

            }, status=400)

        # =====================================
        # RELACIONES
        # =====================================

        instructor = User.objects.get(
            id=instructor_id
        )

        compania = Compania.objects.get(
            id=compania_id
        )

        # =====================================
        # FECHAS
        # =====================================

        fecha_inicio = datetime.fromisoformat(
            fecha_inicio
        )

        fecha_fin = datetime.fromisoformat(
            fecha_fin
        )

        # =====================================
        # CREAR TEST
        # =====================================

        test = Test.objects.create(

            titulo=titulo,

            descripcion=descripcion,

            instructor=instructor,

            compania=compania,

            fecha_inicio=fecha_inicio,

            fecha_fin=fecha_fin,

            max_intentos=max_intentos,

            tiempo_limite=tiempo_limite
        )

        # =====================================
        # CREAR PREGUNTAS
        # =====================================

        for index, p in enumerate(preguntas):

            pregunta = PreguntaTest.objects.create(

                test=test,

                pregunta=p["pregunta"],

                orden=index + 1
            )

            # =================================
            # OPCIONES
            # =================================

            for opcion in p["opciones"]:

                OpcionRespuesta.objects.create(

                    pregunta=pregunta,

                    texto=opcion["texto"],

                    es_correcta=opcion["correcta"]
                )

        # =====================================
        # ASIGNAR SOLDADOS
        # =====================================

        soldados = User.objects.filter(

            perfil__rol="soldado",

            perfil__compania=compania
        )

        for soldado in soldados:

            TestAsignado.objects.create(

                test=test,

                soldado=soldado
            )

        return JsonResponse({

            "success": True,

            "mensaje":
                "Test creado correctamente"

        })

    except Exception as e:

        return JsonResponse({

            "error":
                str(e)

        }, status=500)
    
# =========================================
# ACTIVAR / INACTIVAR TEST
# =========================================

@require_POST
def cambiar_estado_test(

    request,

    test_id

):

    try:

        test = Test.objects.get(
            id=test_id
        )

        test.activa = (
            not test.activa
        )

        test.save()

        return JsonResponse({

            "success": True,

            "mensaje":

                "Test activado"

                if test.activa

                else "Test inactivado"

        })

    except Test.DoesNotExist:

        return JsonResponse({

            "error":
                "Test no encontrado"

        }, status=404)
    
# =========================================
# DETALLE TEST
# =========================================

def detalle_test(

    request,

    test_id

):

    try :

        test = Test.objects.select_related(

            "compania",

            "instructor"

        ).prefetch_related(

            "asignaciones__soldado"

        ).get(id=test_id)

        soldados = []

        for asignacion in test.asignaciones.all():

            soldados.append({

                "apellidos":

                    asignacion.soldado.last_name,

                "nombres":

                    asignacion.soldado.first_name,

                "documento":

                    asignacion.soldado.username,

                "intentos":

                    asignacion.intentos_realizados,

                "nota":

                    asignacion.nota,

                "aprobado":

                    asignacion.aprobado

            })

        return JsonResponse({

            "id":
                test.id,

            "titulo":
                test.titulo,

            "descripcion":
                test.descripcion,

            "compania":
                test.compania.nombre,

            "instructor":

                f"{test.instructor.first_name} "
                f"{test.instructor.last_name}",

            "fecha_inicio":

                test.fecha_inicio.strftime(
                    "%Y-%m-%d %H:%M"
                ),

            "fecha_fin":

                test.fecha_fin.strftime(
                    "%Y-%m-%d %H:%M"
                ),

            "tiempo":
                test.tiempo_limite,

            "intentos":
                test.max_intentos,

            "soldados":
                soldados

        })

    except Test.DoesNotExist:

        return JsonResponse({

            "error":
                "Test no encontrado"

        }, status=404)