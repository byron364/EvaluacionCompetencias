from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Perfil
import json



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


# 🧾 REGISTRO
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
            password=make_password(password)
        )

        Perfil.objects.create(user=user, rol=rol)

        return redirect('login')

    return render(request, 'registro.html')


# 🔒 DECORADOR PERSONALIZADO POR ROL
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


# 🪖 DASHBOARDS
@rol_requerido('admin')
def admin_dashboard(request):
    return render(request, 'admin.html')


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


# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')

def cursos(request):
    return render(request, 'cursos.html')

def evaluaciones(request):
    return render(request, 'evaluaciones.html')

def resultados(request):
    return render(request, 'resultados.html')

def retroalimentacion(request):
    return render(request, 'retro.html')

def inicio(request):
    return render(request, 'inicio.html')

# ADMIN SPA VISTAS

def admin_usuarios(request):
    return render(request, 'admin_usuarios.html')

def admin_cursos(request):
    return render(request, 'admin_cursos.html')

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

            # 🔒 VALIDACIONES
            if not all([nombres, apellidos, email, documento, rol]):
                return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

            if not email.endswith('@ejercito.mil.co'):
                return JsonResponse({'error': 'Correo institucional requerido'}, status=400)

            if User.objects.filter(username=email).exists():
                return JsonResponse({'error': 'El usuario ya existe'}, status=400)

            if Perfil.objects.filter(documento=documento).exists():
                return JsonResponse({'error': 'Documento ya registrado'}, status=400)

            # ✅ CREAR USUARIO
            user = User.objects.create(
                username=email,
                email=email,
                first_name=nombres,
                last_name=apellidos,
                password=make_password(documento)  # 🔥 contraseña inicial
            )

            # ✅ CREAR PERFIL
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