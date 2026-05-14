from django.shortcuts import render, redirect


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


@rol_requerido('instructor')
def instructor_dashboard(request):

    return render(
        request,
        'instructor.html'
    )


@rol_requerido('instructor')
def instructor_inicio(request):

    return render(
        request,
        'instructor_inicio.html'
    )


@rol_requerido('instructor')
def instructor_cursos(request):

    return render(
        request,
        'instructor_cursos.html'
    )


@rol_requerido('instructor')
def instructor_evaluaciones(request):

    return render(
        request,
        'instructor_evaluaciones.html'
    )


@rol_requerido('instructor')
def instructor_soldados(request):

    return render(
        request,
        'instructor_soldados.html'
    )


@rol_requerido('instructor')
def instructor_reportes(request):

    return render(
        request,
        'instructor_reportes.html'
    )


@rol_requerido('soldado')
def soldado_dashboard(request):

    return render(
        request,
        'soldado.html'
    )