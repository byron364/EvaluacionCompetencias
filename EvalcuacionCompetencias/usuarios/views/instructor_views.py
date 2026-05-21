from django.shortcuts import render, redirect
from ..decorators import rol_requerido, modulo_requerido
from ..helpers import obtener_configuracion_usuario


@rol_requerido('instructor')
def instructor_dashboard(request):
    return render(
        request,
        'instructor.html',
        {'configuracion': obtener_configuracion_usuario(request.user)}
    )


@rol_requerido('instructor')
def instructor_inicio(request):
    return render(
        request,
        'instructor_inicio.html',
        {'configuracion': obtener_configuracion_usuario(request.user)}
    )


@rol_requerido('instructor')
@modulo_requerido('cursos')
def instructor_cursos(request):
    return render(request, 'instructor_cursos.html')


@rol_requerido('instructor')
@modulo_requerido('evaluaciones')
def instructor_evaluaciones(request):
    return render(request, 'instructor_evaluaciones.html')


@rol_requerido('instructor')
@modulo_requerido('soldados')
def instructor_soldados(request):
    return render(request, 'instructor_soldados.html')


@rol_requerido('instructor')
@modulo_requerido('reportes')
def instructor_reportes(request):
    return render(request, 'instructor_reportes.html')


@rol_requerido('soldado')
def soldado_dashboard(request):
    return render(request, 'soldado.html', {
        'configuracion': obtener_configuracion_usuario(request.user)
    })
