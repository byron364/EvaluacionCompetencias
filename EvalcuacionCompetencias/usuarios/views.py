from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Perfil


# 🔐 LOGIN
def login_view(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email.endswith('@ejercito.mil.co'):
            messages.error(request, 'Correo no válido')
            return render(request, 'layout/login.html')

        user = authenticate(request, username=email, password=password)

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

        email = request.POST.get('email')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        if not email.endswith('@ejercito.mil.co'):
            return render(request, 'layout/registro.html', {
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