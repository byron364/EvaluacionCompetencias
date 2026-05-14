from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from ..models import ( Batallon,
    Compania)

import json


def admin_batallones(request):

    batallones = Batallon.objects.all()

    soldados = User.objects.filter(
        perfil__rol="soldado"
    )

    cuadros = User.objects.filter(
        perfil__rol="instructor"
    )

    return render(

        request,

        "admin_batallones.html",

        {
            "batallones": batallones,
            "soldados": soldados,
            "cuadros": cuadros
        }
    )


@csrf_exempt
def crear_batallon(request):

    if request.method != "POST":

        return JsonResponse({
            "error": "Método no permitido"
        }, status=405)

    try:

        data = json.loads(request.body)

        nombre = data.get("nombre")
        ciudad = data.get("ciudad")
        descripcion = data.get("descripcion")

        if not nombre:

            return JsonResponse({
                "error": "El nombre es obligatorio"
            }, status=400)

        Batallon.objects.create(

            nombre=nombre,
            ciudad=ciudad,
            descripcion=descripcion

        )

        return JsonResponse({
            "mensaje": (
                "Batallón creado correctamente"
            )
        })

    except Exception as e:

        return JsonResponse({
            "error": str(e)
        }, status=500)
    
@csrf_exempt
def editar_batallon(request, batallon_id):

    if request.method != "PUT":

        return JsonResponse({

            "error": "Método no permitido"

        }, status=405)

    try:

        batallon = Batallon.objects.get(
            id=batallon_id
        )

        data = json.loads(request.body)

        batallon.nombre = data.get(
            "nombre"
        )

        batallon.ciudad = data.get(
            "ciudad"
        )

        batallon.descripcion = data.get(
            "descripcion"
        )

        batallon.save()

        return JsonResponse({

            "mensaje":
                "Batallón actualizado"

        })

    except Exception as e:

        return JsonResponse({

            "error": str(e)

        }, status=500)

@csrf_exempt
def cambiar_estado_batallon(
    request,
    batallon_id
):

    if request.method != "PUT":

        return JsonResponse({

            "error":
                "Método no permitido"

        }, status=405)

    try:

        batallon = Batallon.objects.get(
            id=batallon_id
        )

        batallon.activo = (
            not batallon.activo
        )

        batallon.save()

        estado = (
            "activado"
            if batallon.activo
            else "desactivado"
        )

        return JsonResponse({

            "mensaje":
                f"Batallón {estado} correctamente"

        })

    except Exception as e:

        return JsonResponse({

            "error": str(e)

        }, status=500)
    
def admin_companias(request):

    batallones = Batallon.objects.filter(
        activo=True
    )

    companias = Compania.objects.select_related(
        "batallon"
    ).all()

    return render(

        request,

        "admin_companias.html",

        {

            "batallones": batallones,

            "companias": companias
        }
    )

@csrf_exempt
def crear_compania(request):

    if request.method != "POST":

        return JsonResponse({

            "error":
                "Método no permitido"

        }, status=405)

    try:

        data = json.loads(
            request.body
        )

        nombre = data.get(
            "nombre"
        )

        descripcion = data.get(
            "descripcion"
        )

        batallon_id = data.get(
            "batallon"
        )


        if not nombre:

            return JsonResponse({

                "error":
                    "Ingrese el nombre"

            }, status=400)

        if not batallon_id:

            return JsonResponse({

                "error":
                    "Seleccione un batallón"

            }, status=400)

        batallon = Batallon.objects.filter(
            id=batallon_id
        ).first()

        if not batallon:

            return JsonResponse({

                "error":
                    "Batallón no válido"

            }, status=400)

        # =========================
        # CREAR COMPAÑÍA
        # =========================

        compania = Compania.objects.create(

            nombre=nombre,

            descripcion=descripcion,

            batallon=batallon
        )

        return JsonResponse({

            "mensaje":
                "Compañía creada correctamente",

            "codigo":
                compania.codigo
        })

    except Exception as e:

        return JsonResponse({

            "error":
                str(e)

        }, status=500)
    
@csrf_exempt
def editar_compania(request, id):

    compania = Compania.objects.get(
        id=id
    )

    data = json.loads(
        request.body
    )

    compania.nombre = data.get(
        "nombre"
    )

    compania.descripcion = data.get(
        "descripcion"
    )

    compania.save()

    return JsonResponse({

        "mensaje":
            "Compañía actualizada"
    })

@csrf_exempt
def toggle_compania(request, id):

    compania = Compania.objects.get(
        id=id
    )

    compania.activa = not compania.activa

    compania.save()

    return JsonResponse({

        "mensaje":
            "Estado actualizado"
    })

@csrf_exempt
def eliminar_compania(request, id):

    compania = Compania.objects.get(
        id=id
    )

    compania.delete()

    return JsonResponse({

        "mensaje":
            "Compañía eliminada"
    })