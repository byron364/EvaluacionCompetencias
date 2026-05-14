from django.shortcuts import render


def inicio(request):

    return render(
        request,
        'inicio.html'
    )


def cursos(request):

    return render(
        request,
        'cursos.html'
    )


def evaluaciones(request):

    return render(
        request,
        'evaluaciones.html'
    )


def resultados(request):

    return render(
        request,
        'resultados.html'
    )


def retroalimentacion(request):

    return render(
        request,
        'retro.html'
    )


def admin_reportes(request):

    return render(
        request,
        'admin_reportes.html'
    )


def admin_inscripciones(request):

    return render(
        request,
        "admin_inscripciones.html"
    )


def admin_test(request):

    return render(
        request,
        "admin_test.html"
    )


def admin_configuracion(request):

    return render(
        request,
        "admin_configuracion.html"
    )