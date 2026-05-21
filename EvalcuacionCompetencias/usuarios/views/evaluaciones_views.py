from django.shortcuts import render

from django.http import JsonResponse

from django.views.decorators.http import require_POST

from django.contrib.auth.models import User

from django.middleware.csrf import get_token

from datetime import datetime

from ..models import (
    Evaluacion,
    Compania,
    EvaluacionAsignada
)

import json


# =========================================
# PANEL EVALUACIONES
# =========================================

def admin_evaluaciones(request):

    instructores = User.objects.filter(
        perfil__rol="instructor"
    )

    companias = Compania.objects.select_related(
        "batallon"
    ).all()

    evaluaciones = Evaluacion.objects.select_related(
        "instructor",
        "compania"
    ).all().order_by("-id")

    # =====================================
    # GENERAR TOKEN CSRF
    # =====================================

    get_token(request)

    return render(

        request,

        "admin_evaluaciones.html",

        {
            "instructores": instructores,

            "companias": companias,

            "evaluaciones": evaluaciones
        }
    )


# =========================================
# CREAR EVALUACIÓN
# =========================================

@require_POST
def crear_evaluacion(request):

    try:

        data = json.loads(request.body)

        # =====================================
        # CAMPOS
        # =====================================

        titulo = (
            data.get("titulo", "")
            .strip()
        )

        descripcion = (
            data.get("descripcion", "")
            .strip()
        )

        instructor_id = data.get(
            "instructor"
        )

        compania_id = data.get(
            "compania"
        )

        fecha = data.get("fecha")

        # =====================================
        # VALIDACIONES
        # =====================================

        if not titulo:

            return JsonResponse({

                "error":
                    "El título es obligatorio"

            }, status=400)

        if not instructor_id:

            return JsonResponse({

                "error":
                    "Seleccione instructor"

            }, status=400)

        if not compania_id:

            return JsonResponse({

                "error":
                    "Seleccione compañía"

            }, status=400)

        if not fecha:

            return JsonResponse({

                "error":
                    "Seleccione fecha"

            }, status=400)

        # =====================================
        # VALIDAR FECHA
        # =====================================

        try:

            fecha = datetime.strptime(
                    fecha,
                    "%Y-%m-%d"
                ).date()

        except Exception:

            return JsonResponse({

                "error":
                    "Fecha inválida"

            }, status=400)

        # =====================================
        # VALIDAR INSTRUCTOR
        # =====================================

        try:

            instructor = User.objects.get(
                    id=instructor_id
                )

        except User.DoesNotExist:

            return JsonResponse({

                "error":
                    "Instructor no encontrado"

            }, status=404)

        # =====================================
        # VALIDAR COMPAÑÍA
        # =====================================

        try:

            compania = Compania.objects.get(
                    id=compania_id
                )

        except Compania.DoesNotExist:

            return JsonResponse({

                "error":
                    "Compañía no encontrada"

            }, status=404)

        # =====================================
        # CREAR EVALUACIÓN
        # =====================================

        evaluacion = Evaluacion.objects.create(

                titulo=titulo,

                descripcion=descripcion,

                instructor=instructor,

                compania=compania,

                fecha=fecha
            )

        # =====================================
        # ASIGNAR SOLDADOS
        # =====================================

        soldados = User.objects.filter(

                perfil__rol="soldado",

                perfil__compania=compania
            )

        asignados = 0

        for soldado in soldados:

            EvaluacionAsignada.objects.create(

                evaluacion=evaluacion,

                soldado=soldado,

                puntaje_actual=
                    evaluacion.puntaje_maximo
            )

            asignados += 1

        return JsonResponse({

            "success": True,

            "mensaje":
                "Evaluación creada correctamente",

            "codigo":
                evaluacion.codigo,

            "soldados_asignados":
                asignados
        })

    except json.JSONDecodeError:

        return JsonResponse({

            "error":
                "JSON inválido"

        }, status=400)

    except Exception as e:

        return JsonResponse({

            "error": str(e)

        }, status=500)


# =========================================
# EDITAR EVALUACIÓN
# =========================================

@require_POST
def editar_evaluacion(
    request,
    evaluacion_id
):

    try:

        # =====================================
        # BUSCAR EVALUACIÓN
        # =====================================

        try:

            evaluacion = Evaluacion.objects.get(
                    id=evaluacion_id
                )

        except Evaluacion.DoesNotExist:

            return JsonResponse({

                "error":
                    "Evaluación no encontrada"

            }, status=404)

        data = json.loads(request.body)

        titulo = (
            data.get("titulo", "")
            .strip()
        )

        descripcion = (
            data.get("descripcion", "")
            .strip()
        )

        fecha = data.get("fecha")

        instructor_id = data.get(
            "instructor"
        )

        compania_id = data.get(
            "compania"
        )

        # =====================================
        # VALIDACIONES
        # =====================================

        if not titulo:

            return JsonResponse({

                "error":
                    "El título es obligatorio"

            }, status=400)

        # =====================================
        # VALIDAR FECHA
        # =====================================

        try:

            fecha = datetime.strptime(
                    fecha,
                    "%Y-%m-%d"
                ).date()

        except Exception:

            return JsonResponse({

                "error":
                    "Fecha inválida"

            }, status=400)

        # =====================================
        # VALIDAR INSTRUCTOR
        # =====================================

        try:

            instructor = User.objects.get(
                    id=instructor_id
                )

        except User.DoesNotExist:

            return JsonResponse({

                "error":
                    "Instructor inválido"

            }, status=404)

        # =====================================
        # VALIDAR COMPAÑÍA
        # =====================================

        try:

            compania = Compania.objects.get(
                    id=compania_id
                )

        except Compania.DoesNotExist:

            return JsonResponse({

                "error":
                    "Compañía inválida"

            }, status=404)

        # =====================================
        # ACTUALIZAR
        # =====================================

        evaluacion.titulo = titulo

        evaluacion.descripcion = descripcion

        evaluacion.fecha = fecha

        evaluacion.instructor = instructor

        evaluacion.compania = compania

        evaluacion.save()

        return JsonResponse({

            "success": True,

            "mensaje":
                "Evaluación actualizada correctamente"
        })

    except json.JSONDecodeError:

        return JsonResponse({

            "error":
                "JSON inválido"

        }, status=400)

    except Exception as e:

        return JsonResponse({

            "error":
                str(e)

        }, status=500)


# =========================================
# ELIMINAR EVALUACIÓN
# =========================================

@require_POST
def eliminar_evaluacion(
    request,
    evaluacion_id
):

    try:

        try:

            evaluacion = Evaluacion.objects.get(
                    id=evaluacion_id
                )

        except Evaluacion.DoesNotExist:

            return JsonResponse({

                "error":
                    "Evaluación no encontrada"

            }, status=404)

        evaluacion.delete()

        return JsonResponse({

            "success": True,

            "mensaje":
                "Evaluación eliminada correctamente"
        })

    except Exception as e:

        return JsonResponse({

            "error":
                str(e)

        }, status=500)


# =========================================
# LISTAR EVALUACIONES
# =========================================

def listar_evaluaciones(request):

    evaluaciones = Evaluacion.objects.select_related(

            "instructor",

            "compania"

        ).all().order_by("-id")

    data = []

    for evaluacion in evaluaciones:

        data.append({

            "id":
                evaluacion.id,

            "codigo":
                evaluacion.codigo,

            "titulo":
                evaluacion.titulo,

            "descripcion":
                evaluacion.descripcion,

            "instructor":

                evaluacion.instructor.first_name
                

                if evaluacion.instructor

                else "Sin instructor",

            "compania":
                evaluacion.compania.nombre,

            "fecha":
                evaluacion.fecha.strftime(
                    "%Y-%m-%d"
                ),

            "puntaje_maximo":
                evaluacion.puntaje_maximo,

            "estado":

                "Activa"

                if evaluacion.activa

                else "Inactiva"
        })

    return JsonResponse({

        "data": data

    })

def buscar_companias(request):

    try:

        companias = Compania.objects.all()

        data = []

        for c in companias:

            data.append({

                "id": c.id,

                "nombre": c.nombre,

                "codigo": c.codigo

            })

        print("COMPAÑIAS ENVIADAS:", data)

        return JsonResponse({

            "success": True,

            "companias": data

        })

    except Exception as e:

        print("ERROR:", str(e))

        return JsonResponse({

            "success": False,

            "error": str(e)

        })

@require_POST
def activar_evaluacion(
    request,
    evaluacion_id
):

    try:

        evaluacion = Evaluacion.objects.get(
            id=evaluacion_id
        )

        evaluacion.activa = (
            not evaluacion.activa
        )

        evaluacion.save()

        estado = (
            "activada"
            if evaluacion.activa
            else "inactivada"
        )

        return JsonResponse({

            "success": True,

            "mensaje":
                f"Evaluación {estado}"

        })

    except Evaluacion.DoesNotExist:

        return JsonResponse({

            "error":
                "Evaluación no encontrada"

        }, status=404)

    except Exception as e:

        return JsonResponse({

            "error":
                str(e)

        }, status=500)
    
def detalle_evaluacion(
    request,
    evaluacion_id
):

    try:

        evaluacion = Evaluacion.objects.select_related(

            "instructor",

            "compania"

        ).get(id=evaluacion_id)

        # =====================================
        # PARTICIPANTES
        # =====================================

        participantes = []

        for asignacion in evaluacion.asignaciones.select_related(
            "soldado"
        ).all():

            soldado = asignacion.soldado

            participantes.append({

                "nombres":
                    soldado.first_name,

                "apellidos":
                    soldado.last_name,

                "documento":
                    soldado.username

            })

        # =====================================
        # RESPUESTA JSON
        # =====================================

        return JsonResponse({

            "id":
                evaluacion.id,

            "codigo":
                evaluacion.codigo,

            "titulo":
                evaluacion.titulo,

            "descripcion":
                evaluacion.descripcion,

            "instructor":

                evaluacion.instructor.first_name,

            "instructor_id":

                evaluacion.instructor.id,

            "compania":

                evaluacion.compania.nombre,

            "compania_id":

                evaluacion.compania.id,

            "fecha":

                evaluacion.fecha.strftime(
                    "%Y-%m-%d"
                ),

            "estado":

                evaluacion.activa,

            # =====================================
            # PARTICIPANTES
            # =====================================

            "participantes":
                participantes

        })

    except Evaluacion.DoesNotExist:

        return JsonResponse({

            "error":
                "Evaluación no encontrada"

        }, status=404)