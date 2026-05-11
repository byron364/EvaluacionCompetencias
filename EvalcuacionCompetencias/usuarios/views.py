from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse 
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from django.contrib.auth.decorators import login_required
from openpyxl.drawing.image import Image
import os
from django.conf import settings 
from .models import Perfil
import json
import pandas as pd 
from .models import Curso




def login_view(request):
    if request.method == 'POST':

        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''

        if not email.endswith('@ejercito.mil.co'):
            messages.error(request, 'Correo no válido')
            return render(request, 'layout/login.html')

        user = authenticate(request, username=email, password=password)

        if user is None:
            try:
                usuario = User.objects.get(email__iexact=email)
                user = authenticate(request, username=usuario.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)

            try:
                rol = user.perfil.rol
            except:
                messages.error(request, 'Usuario sin rol')
                return redirect('login')

            if rol == 'admin':
                return redirect('admin_dashboard')
            elif rol == 'instructor':
                return redirect('instructor_dashboard')
            elif rol == 'soldado':
                return redirect('soldado_dashboard')

        else:
            messages.error(request, 'Credenciales incorrectas')

    return render(request, 'layout/login.html')



def registro_view(request):
    if request.method == 'POST':

        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''
        rol = request.POST.get('rol')

        if not email.endswith('@ejercito.mil.co'):
            return render(request, 'registro.html', {
                'error': 'Debe usar correo institucional'
            })

        user = User.objects.create(
            username=email,
            email=email,
            first_name=nombres, 
            last_name=apellidos,
            password=make_password(password)
        )

        Perfil.objects.create(user=user, rol=rol)

        return redirect('login')

    return render(request, 'registro.html')


def rol_requerido(rol_permitido):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if request.user.perfil.rol != rol_permitido:
                return redirect('login')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



@rol_requerido('admin')
def admin_dashboard(request): 
    instructores = User.objects.filter( 
        perfil__rol="instructor" 
        ) 
    return render(request, "admin.html", { 
        "instructores": instructores 
        })

@rol_requerido('instructor')
def instructor_dashboard(request):
    return render(request, 'instructor.html')


@rol_requerido('instructor')
def instructor_inicio(request):
    return render(request, 'instructor_inicio.html')


@rol_requerido('instructor')
def instructor_cursos(request):
    return render(request, 'instructor_cursos.html')


@rol_requerido('instructor')
def instructor_evaluaciones(request):
    return render(request, 'instructor_evaluaciones.html')


@rol_requerido('instructor')
def instructor_soldados(request):
    return render(request, 'instructor_soldados.html')


@rol_requerido('instructor')
def instructor_reportes(request):
    return render(request, 'instructor_reportes.html')


@rol_requerido('soldado')
def soldado_dashboard(request):
    return render(request, 'soldado.html')



def logout_view(request):
    logout(request)
    return redirect('login')

@rol_requerido('soldado')
def cursos(request):

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'cursos.html')

    return render(request, 'soldado.html')


@rol_requerido('soldado')
def evaluaciones(request):

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'evaluaciones.html')

    return render(request, 'soldado.html')


@rol_requerido('soldado')
def resultados(request):

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'resultados.html')

    return render(request, 'soldado.html')


@rol_requerido('soldado')
def retroalimentacion(request):

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'retro.html')

    return render(request, 'soldado.html')


@rol_requerido('soldado')
def inicio(request):

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'inicio.html')

    return render(request, 'soldado.html')


def admin_usuarios(request):
    usuarios = Perfil.objects.select_related("user").all()

    return render(
        request,
        "admin_usuarios.html",
        {
            "usuarios": usuarios
        }
    )


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

def admin_reportes(request):
    return render(request, 'admin_reportes.html')
def admin_dashboard_partial(request):
    return render(request, 'admin_dashboard_partial.html')

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

            
            if not all([nombres, apellidos, email, documento, rol]):
                return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

            if not email.endswith('@ejercito.mil.co'):
                return JsonResponse({'error': 'Correo institucional requerido'}, status=400)

            if User.objects.filter(username=email).exists():
                return JsonResponse({'error': 'El usuario ya existe'}, status=400)

            if Perfil.objects.filter(documento=documento).exists():
                return JsonResponse({'error': 'Documento ya registrado'}, status=400)

            
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
                grado=grado
            )

            return JsonResponse({'mensaje': 'Usuario creado correctamente'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
def cargar_usuarios_excel(request):
    if request.method == "POST":

        archivo = request.FILES.get("archivo")
        rol = request.POST.get("rol")

        if not archivo:
            return JsonResponse({
                "error": "No se recibió ningún archivo"
            })

        if not rol:
            return JsonResponse({
                "error": "Debe seleccionar un tipo de usuario"
            })

        try: 
            df = pd.read_excel(archivo, header=7) 

            creados = 0
            errores = []

            for index, row in df.iterrows():

                nombres = str(row.get("nombres", "")).strip()
                apellidos = str(row.get("apellidos", "")).strip()
                email = str(row.get("email", "")).strip().lower()
                documento = str(row.get("documento", "")).strip()
                grado = str(row.get("grado", "")).strip()
                unidad = str(row.get("unidad", "")).strip()


                print( f"Fila {index+2}:", 
                      nombres, 
                      apellidos, 
                      email, 
                      documento, 
                      grado, 
                      unidad 
                    )
                
                print("GRADO:", grado)

                if not email:
                    errores.append(f"Fila {index+2}: email vacío")
                    continue

                if not documento:
                    errores.append(f"Fila {index+2}: documento vacío")
                    continue

                if not email.endswith("@ejercito.mil.co"):
                    errores.append(f"Fila {index+2}: correo no institucional")
                    continue

                if User.objects.filter(username=email).exists():
                    errores.append(f"Fila {index+2}: usuario ya existe")
                    continue

                if Perfil.objects.filter(documento=documento).exists():
                    errores.append(f"Fila {index+2}: documento ya registrado")
                    continue

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
                    grado=grado,
                    unidad=unidad
                )

                creados += 1

            return JsonResponse({
                "mensaje": f"{creados} usuarios creados",
                "errores": errores
            })

        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "error": "Método no permitido"
    })

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
    ws["C9"] = "juan@ejercito.mil.co"
    ws["D9"] = "12345678"
    ws["E9"] = "Capitán"
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


def obtener_estadisticas(request):
    total_usuarios = User.objects.count()
    total_soldados = Perfil.objects.filter(rol="soldado").count()
    total_instructores = Perfil.objects.filter(rol="instructor").count()
    total_activos = User.objects.filter(is_active=True).count()

    return JsonResponse({
        "total_usuarios": total_usuarios,
        "total_soldados": total_soldados,
        "total_instructores": total_instructores,
        "total_activos": total_activos
    })

def listar_usuarios(request):
    usuarios = Perfil.objects.select_related("user").all()

    return render(
        request,
        "admin_usuarios.html",
        {
            "usuarios": usuarios
        }
    )

@csrf_exempt
def eliminar_usuario(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()

        return JsonResponse({
            "mensaje": "Usuario eliminado correctamente"
        })

    except User.DoesNotExist:
        return JsonResponse({
            "error": "Usuario no encontrado"
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
                "mensaje": "Usuario actualizado correctamente"
            })

        except User.DoesNotExist:
            return JsonResponse({
                "error": "Usuario no encontrado"
            }, status=404)

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

def listar_cursos(request):

    cursos = Curso.objects.select_related('instructor').all()

    data = []

    for curso in cursos:
        data.append({
            "id": curso.id,
            "codigo": curso.codigo,
            "nombre": curso.nombre,
            "instructor": curso.instructor.first_name if curso.instructor else "Sin instructor",
            "fecha_inicio": curso.fecha_inicio,
            "fecha_fin": curso.fecha_fin,
            "estado": "Activo" if curso.activo else "Inactivo"
        })

    return JsonResponse({
        "data": data
    })

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