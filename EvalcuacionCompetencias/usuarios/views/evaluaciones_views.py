from django.shortcuts import render


def admin_evaluaciones(request):

    return render(
        request,
        "admin_evaluaciones.html"
    )