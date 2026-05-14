from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from ..models import Curso

import json


def admin_cursos(request):

    instructores = User.objects.filter(
        perfil__rol="instructor"
    )

    cursos = Curso.objects.select_related(
        'instructor'
    ).all()

    return render(
        request,
        "admin_cursos.html",
        {
            "instructores": instructores,
            "cursos": cursos
        }
    )
@csrf_exempt
def crear_curso(request):

    if request.method != "POST":
        return JsonResponse({
            "error": "Método no permitido"
        }, status=405)

    try:
        data = json.loads(request.body)

        codigo = data.get("codigo")
        nombre = data.get("nombre")
        descripcion = data.get("descripcion")
        instructor_id = data.get("instructor")
        fecha_inicio = data.get("fecha_inicio")
        fecha_fin = data.get("fecha_fin")
        cupo_maximo = data.get("cupo_maximo")

        # Validaciones
        if not codigo or not nombre:
            return JsonResponse({
                "error": "Código y nombre son obligatorios"
            }, status=400)

        # Curso duplicado
        if Curso.objects.filter(codigo=codigo).exists():
            return JsonResponse({
                "error": "Ya existe un curso con ese código"
            }, status=400)

        # Instructor válido
        try:
            instructor = User.objects.get(id=instructor_id)

        except User.DoesNotExist:
            return JsonResponse({
                "error": "Instructor no encontrado"
            }, status=404)

        # Crear curso
        Curso.objects.create(
            codigo=codigo,
            nombre=nombre,
            descripcion=descripcion,
            instructor=instructor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            cupo_maximo=cupo_maximo
        )

        return JsonResponse({
            "mensaje": "Curso creado correctamente"
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            "error": "JSON inválido"
        }, status=400)

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
    
@csrf_exempt
def editar_curso(request, curso_id):

    if request.method != "POST":
        return JsonResponse({
            "error": "Método no permitido"
        }, status=405)

    try:

        curso = Curso.objects.get(id=curso_id)

        data = json.loads(request.body)

        curso.codigo = data.get("codigo")
        curso.nombre = data.get("nombre")
        curso.descripcion = data.get("descripcion")
        curso.fecha_inicio = data.get("fecha_inicio")
        curso.fecha_fin = data.get("fecha_fin")
        curso.cupo_maximo = data.get("cupo_maximo")

        instructor_id = data.get("instructor")

        curso.instructor = User.objects.get(
            id=instructor_id
        )

        curso.save()

        return JsonResponse({
            "mensaje": "Curso actualizado correctamente"
        })

    except Curso.DoesNotExist:
        return JsonResponse({
            "error": "Curso no encontrado"
        }, status=404)

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
    
@csrf_exempt
def eliminar_curso(request, curso_id):

    try:

        curso = Curso.objects.get(id=curso_id)

        curso.delete()

        return JsonResponse({
            "mensaje": "Curso eliminado correctamente"
        })

    except Curso.DoesNotExist:

        return JsonResponse({
            "error": "Curso no encontrado"
        }, status=404)
   
def listar_cursos(request):

    cursos = Curso.objects.select_related(
        'instructor'
    ).all()

    data = []

    for curso in cursos:

        data.append({

            "id": curso.id,

            "codigo": curso.codigo,

            "nombre": curso.nombre,

            "instructor":
                curso.instructor.first_name
                if curso.instructor
                else "Sin instructor",

            "fecha_inicio":
                curso.fecha_inicio,

            "fecha_fin":
                curso.fecha_fin,

            "estado":
                "Activo"
                if curso.activo
                else "Inactivo"
        })

    return JsonResponse({
        "data": data
    })