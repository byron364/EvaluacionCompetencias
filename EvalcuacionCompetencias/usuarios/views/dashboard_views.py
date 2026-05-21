from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from ..models import Perfil, Curso
from ..helpers import obtener_configuracion_usuario


def rol_requerido(rol_permitido):

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:

                return redirect('login')

            if request.user.perfil.rol != rol_permitido:

                return redirect('login')

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator


@rol_requerido('admin')
def admin_dashboard(request):
    instructores = User.objects.filter(
        perfil__rol="instructor"
    )

    return render(
        request,
        "admin.html",
        {
            "instructores": instructores,
            "configuracion": obtener_configuracion_usuario(request.user)
        }
    )


@rol_requerido('admin')
def admin_dashboard_partial(request):
    return render(
        request,
        'admin_dashboard_partial.html',
        {
            'configuracion': obtener_configuracion_usuario(request.user)
        }
    )


def obtener_estadisticas(request):
    total_soldados = Perfil.objects.filter(rol="soldado").count()
    total_instructores = Perfil.objects.filter(rol="instructor").count()
    total_activos = User.objects.filter(is_active=True).count()
    total_cursos = Curso.objects.count()
    total_evaluaciones = 0

    soldados_aprobados = Perfil.objects.filter(
        rol="soldado",
        user__is_active=True
    ).count()

    porcentaje_aprobados = 0
    if total_soldados > 0:
        porcentaje_aprobados = round((soldados_aprobados / total_soldados) * 100)

    return JsonResponse({
        "total_usuarios": Perfil.objects.count(),
        "total_soldados": total_soldados,
        "total_instructores": total_instructores,
        "total_activos": total_activos,
        "total_cursos": total_cursos,
        "total_evaluaciones": total_evaluaciones,
        "porcentaje_aprobados": porcentaje_aprobados
    })
