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

import pandas as pd
import json
import os


def admin_usuarios(request):

    usuarios = Perfil.objects.select_related(
        'user'
    ).all()

    companias = Compania.objects.filter(
    activa=True
    )

    return render(

        request,

        "admin_usuarios.html",

        {

            "usuarios": usuarios,

            "companias": companias

        }

    )

def listar_usuarios(request):

    usuarios = Perfil.objects.select_related(
        "user"
    ).all()

    return render(
        request,
        "admin_usuarios.html",
        {
            "usuarios": usuarios
        }
    )


@csrf_exempt
def crear_usuario(request):

    if request.method == 'POST':

        try:

            data = json.loads(request.body)

            nombres = data.get('nombres')
            apellidos = data.get('apellidos')
            email = data.get('email')
            documento = data.get('documento')
            unidad = data.get('unidad')
            grado = data.get('grado')
            rol = data.get('rol')
            compania_id = data.get("compania")

            compania = None

            if compania_id:
                compania = Compania.objects.filter(
                    id=compania_id
                ).first()

            campos_obligatorios = [
                nombres,
                apellidos,
                email,
                documento,
                unidad,
                rol,
                compania_id
            ]
            if rol != "soldado":
                campos_obligatorios.append(grado)
                if not all(campos_obligatorios):
                    return JsonResponse({
                        'error': 'Todos los campos son obligatorios'
                        }, status=400)

            if rol == "soldado":
                if not email.endswith(
                    "@buzonejercito.mil.co"
                ):return JsonResponse({
                "error": "El soldado debe usar correo @buzonejercito.mil.co"
                }, status=400)
            else:
                if not email.endswith(
                    "@ejercito.mil.co"
                    ):return JsonResponse({
                        "error": "Debe usar correo institucional @ejercito.mil.co"
                        }, status=400)

            if User.objects.filter(
                username__iexact=email
            ).exists():

                return JsonResponse({
                    'error':
                        'El usuario ya existe'
                }, status=400)

            if Perfil.objects.filter(
                documento__iexact=documento
            ).exists():

                return JsonResponse({
                    'error':
                        'Documento ya registrado'
                }, status=400)

            user = User.objects.create(

                username=email,
                email=email,
                first_name=nombres,
                last_name=apellidos,
                password=make_password(documento)
            )

            Perfil.objects.create(

                user=user,
                rol=rol,
                documento=documento,
                unidad=unidad,
                grado=grado,
                compania=compania,
            )

            return JsonResponse({
                'mensaje':
                    'Usuario creado correctamente'
            })

        except Exception as e:

            return JsonResponse({
                'error': str(e)
            }, status=500)


@csrf_exempt
def eliminar_usuario(request, user_id):

    try:

        user = User.objects.get(id=user_id)

        user.delete()

        return JsonResponse({
            "mensaje":
                "Usuario eliminado correctamente"
        })

    except User.DoesNotExist:

        return JsonResponse({
            "error":
                "Usuario no encontrado"
        }, status=404)


@csrf_exempt
def editar_usuario(request, user_id):

    if request.method == "POST":

        try:

            user = User.objects.get(id=user_id)

            perfil = Perfil.objects.get(user=user)

            data = json.loads(request.body)

            user.first_name = data.get("nombre")
            user.last_name = data.get("apellido")
            user.email = data.get("email")
            user.is_active = data.get("activo")

            perfil.rol = data.get("rol")

            user.save()

            perfil.save()

            return JsonResponse({
                "mensaje":
                    "Usuario actualizado correctamente"
            })

        except User.DoesNotExist:

            return JsonResponse({
                "error":
                    "Usuario no encontrado"
            }, status=404)

@csrf_exempt
def cargar_usuarios_excel(request):

    if request.method != "POST":

        return JsonResponse({

            "error":
                "Método no permitido"

        }, status=405)

    archivo = request.FILES.get("archivo")

    batallon_id = request.POST.get(
        "batallon"
    )

    batallon = None

    if batallon_id:

        batallon = Batallon.objects.filter(
            id=batallon_id
        ).first()

    if not batallon:

        return JsonResponse({

            "error":
                "Debe seleccionar un batallón"

        }, status=400)

    if not archivo:

        return JsonResponse({

            "error":
                "No se recibió ningún archivo"

        }, status=400)

    try:

        df = pd.read_excel(
            archivo,
            header=7
        )

        creados = 0

        errores = []

        for index, row in df.iterrows():

            nombres = str(
                row.get("nombres", "")
            ).strip()

            apellidos = str(
                row.get("apellidos", "")
            ).strip()

            email = str(
                row.get("email", "")
                ).strip().lower()
            email = email.replace(
                " ",
                ""
                )

            documento = str(
                row.get("documento", "")
                ).replace(".0", "").strip()
            documento = documento.replace(
                " ",
                ""
                )

            grado = str(
                row.get("grado", "")
            ).strip()

            unidad = str(
                row.get("unidad", "")
            ).strip()

            if grado.lower() == "soldado":

                rol = "soldado"

            else:

                rol = "instructor"

            if not nombres:

                errores.append(
                    f"Fila {index+2}: nombres vacíos"
                )

                continue

            if not apellidos:

                errores.append(
                    f"Fila {index+9}: apellidos vacíos"
                )

                continue

            if not email:

                errores.append(
                    f"Fila {index+9}: email vacío"
                )

                continue

            if not documento:

                errores.append(
                    f"Fila {index+9}: documento vacío"
                )

                continue

            if rol == "soldado":

                if not email.endswith(
                    "@buzonejercito.mil.co"
                ):

                    errores.append(
                        f"Fila {index+9}: correo inválido para soldado"
                    )

                    continue

            else:

                if not email.endswith(
                    "@ejercito.mil.co"
                ):

                    errores.append(
                        f"Fila {index+9}: correo institucional inválido"
                    )

                    continue

            if User.objects.filter(
                username=email
            ).exists():

                errores.append(
                    f"Fila {index+9}: usuario ya existe"
                )

                continue

            if Perfil.objects.filter(
                documento=documento
            ).exists():

                errores.append(
                    f"Fila {index+9}: documento ya registrado"
                )

                continue

            user = User.objects.create(

                username=email,

                email=email,

                first_name=nombres,

                last_name=apellidos,

                password=make_password(
                    documento
                )
            )

            # =====================================
            # CREAR PERFIL
            # =====================================

            Perfil.objects.create(

                user=user,

                rol=rol,

                documento=documento,

                grado=grado,

                unidad=unidad,

                batallon=batallon
            )

            creados += 1

        return JsonResponse({

            "mensaje":
                f"{creados} usuarios creados",

            "errores":
                errores
        })

    except Exception as e:

        return JsonResponse({

            "error":
                str(e)

        }, status=500)
    
@csrf_exempt
def descargar_plantilla_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Plantilla Usuarios"

    ruta_logo_principal = os.path.join(
        settings.BASE_DIR,
        "static",
        "img",
        "escudo.png"
    )

    if os.path.exists(ruta_logo_principal):
        logo_principal = Image(ruta_logo_principal)
        logo_principal.width = 140
        logo_principal.height = 140

        # Logo izquierdo superior
        ws.add_image(logo_principal, "A1")


    ruta_logo_secundario = os.path.join(
        settings.BASE_DIR,
        "static",
        "img",
        "CompromisoColombia.png"
    )

    if os.path.exists(ruta_logo_secundario):
        logo_secundario = Image(ruta_logo_secundario)
        logo_secundario.width = 180
        logo_secundario.height = 110

        # Logo derecho superior
        ws.add_image(logo_secundario, "E2")

    encabezados = [
        "nombres",
        "apellidos",
        "email",
        "documento",
        "grado",
        "unidad"
    ]

    for i, titulo in enumerate(encabezados, start=1):
        ws.cell(row=8, column=i, value=titulo)


    ejemplo = [
        "Juan",
        "Perez",
        "juan@ejercito.mil.co",
        "12345678",
        "Capitán",
        "Batallon Norte"
    ]

    ws["A9"] = "Juan"
    ws["B9"] = "Perez"
    ws["C9"] = "juan@buzonejercito.mil.co"
    ws["D9"] = "12345678"
    ws["E9"] = "Soldado"
    ws["F9"] = "Batallon Norte"

    for i, valor in enumerate(ejemplo, start=1):
        ws.cell(row=9, column=i, value=valor)

    header_fill = PatternFill(
        fill_type="solid",
        fgColor="789441"
    )

    header_font = Font(
        color="FFFFFF",
        bold=True,
        size=12
    )

    center = Alignment(
        horizontal="center",
        vertical="center"
    )

    thin = Side(
        style="thin",
        color="D9D9D9"
    )

    border = Border(
        left=thin,
        right=thin,
        top=thin,
        bottom=thin
    )

    for col in ws[8]:
        col.fill = header_fill
        col.font = header_font
        col.alignment = center
        col.border = border


    for row in ws.iter_rows(min_row=9, max_row=9):
        for cell in row:
            cell.border = border
            cell.alignment = center

    widths = {
        "A": 22,
        "B": 22,
        "C": 35,
        "D": 20,
        "E": 28,
        "F": 28
    }

    for col, width in widths.items():
        ws.column_dimensions[col].width = width


    for fila in range(10, 501):
        for col in ["A", "B", "C", "D", "E", "F"]:
            ws[f"{col}{fila}"] = ""

    ws.protection.sheet = True
    ws.protection.enable()

    # desbloquear celdas editables
    for fila in range(9, 501):
        for col in ["A", "B", "C", "D", "E", "F"]:
            ws[f"{col}{fila}"].protection = (
                ws[f"{col}{fila}"].protection.copy(locked=False)
            )

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="plantilla_usuarios.xlsx"'
    )

    wb.save(response)

    return response


