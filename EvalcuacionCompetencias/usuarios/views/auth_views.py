from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages

from ..models import Perfil


def login_view(request):

    if request.method == 'POST':

        email = (
            request.POST.get('email') or ''
        ).strip().lower()

        password = (
            request.POST.get('password') or ''
        )

        if not email.endswith(
            '@ejercito.mil.co'
        ):

            messages.error(
                request,
                'Correo no válido'
            )

            return render(
                request,
                'layout/login.html'
            )

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is None:

            try:

                usuario = User.objects.get(
                    email__iexact=email
                )

                user = authenticate(
                    request,
                    username=usuario.username,
                    password=password
                )

            except User.DoesNotExist:

                user = None

        if user is not None:

            login(request, user)

            try:

                rol = user.perfil.rol

            except:

                messages.error(
                    request,
                    'Usuario sin rol'
                )

                return redirect('login')

            if rol == 'admin':

                return redirect(
                    'admin_dashboard'
                )

            elif rol == 'instructor':

                return redirect(
                    'instructor_dashboard'
                )

            elif rol == 'soldado':

                return redirect(
                    'soldado_dashboard'
                )

        else:

            messages.error(
                request,
                'Credenciales incorrectas'
            )

    return render(
        request,
        'layout/login.html'
    )


def logout_view(request):

    logout(request)

    return redirect('login')

def registro_view(request):

    return render(
        request,
        'registro.html'
    )