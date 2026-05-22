import json
import base64
import os
import subprocess
import pandas as pd

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image
from django.conf import settings
from ..models import *
from ..models import Perfil
from ..models import Batallon
from ..models import Compania
from django.core.files.base import ContentFile
def biometrico(request):

    usuarios = Perfil.objects.select_related(
        "user",
        "compania"
    ).all()

    return render(

        request,

        "biometrico.html",

        {
            "usuarios": usuarios
        }

    )


# ==========================================
# REGISTRAR HUELLA USUARIO EXISTENTE
# ==========================================

@csrf_exempt
def registrar_huella_usuario(
    request,
    documento
):

    try:

        perfil = Perfil.objects.get(
            documento=documento
        )

        ruta_temp = rf"C:\Huellero\temp\temp_huella_{documento}.json"

        # ==========================================
        # VALIDAR JSON
        # ==========================================

        if not os.path.exists(ruta_temp):

            return JsonResponse({

                "success": False,

                "error":
                    "No existe huella temporal"

            })

        # ==========================================
        # LEER JSON
        # ==========================================

        with open(
            ruta_temp,
            "r",
            encoding="utf-8"
        ) as f:

            datos = json.load(f)

        # ==========================================
        # GUARDAR TEMPLATE
        # ==========================================

        perfil.huella = datos.get(
            "huella"
        )

        # ==========================================
        # IMAGEN BASE64
        # ==========================================

        imagen_base64 = datos.get(
            "imagen"
        )

        # ==========================================
        # GUARDAR IMAGEN
        # ==========================================

        if imagen_base64:

            image_data = ContentFile(

                base64.b64decode(
                    imagen_base64
                ),

                name=
                    f"huella_{documento}.png"

            )

            perfil.imagen_huella = image_data

        perfil.save()

        # ==========================================
        # ELIMINAR JSON TEMP
        # ==========================================

        if os.path.exists(ruta_temp):

            os.remove(ruta_temp)

        return JsonResponse({

            "success": True,

            "mensaje":
                "Huella registrada correctamente"

        })

    except Perfil.DoesNotExist:

        return JsonResponse({

            "success": False,

            "error":
                "Usuario no encontrado"

        })

    except Exception as e:

        return JsonResponse({

            "success": False,

            "error": str(e)

        })