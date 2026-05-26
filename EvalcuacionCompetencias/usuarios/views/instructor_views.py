from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from ..decorators import rol_requerido, modulo_requerido
from ..helpers import obtener_configuracion_usuario
from ..models import Curso, Evaluacion, Inscripcion, Calificacion, EvaluacionAsignada


@rol_requerido('instructor')
def instructor_dashboard(request):
    return render(
        request,
        'instructor.html',
        {'configuracion': obtener_configuracion_usuario(request.user)}
    )


@rol_requerido('instructor')
def instructor_inicio(request):
    cursos = Curso.objects.filter(instructor=request.user).annotate(
        total_soldados=Count('inscripciones')
    )
    calificaciones = Calificacion.objects.filter(
        curso__instructor=request.user
    ).select_related('estudiante', 'curso').order_by('-creado_en')[:5]
    promedio_raw = Calificacion.objects.filter(
        curso__instructor=request.user
    ).aggregate(avg=Avg('nota'))['avg']

    return render(request, 'instructor_inicio.html', {
        'configuracion': obtener_configuracion_usuario(request.user),
        'cursos': cursos,
        'total_cursos': cursos.filter(activo=True).count(),
        'evaluaciones_pendientes': Evaluacion.objects.filter(
            instructor=request.user, activa=True
        ).count(),
        'soldados_asignados': Inscripcion.objects.filter(
            curso__instructor=request.user
        ).values('estudiante').distinct().count(),
        'calificaciones': calificaciones,
        'promedio_general': round(promedio_raw, 1) if promedio_raw else 0,
    })


@rol_requerido('instructor')
@modulo_requerido('cursos')
def instructor_cursos(request):
    cursos = Curso.objects.filter(instructor=request.user).annotate(
        total_soldados=Count('inscripciones')
    )
    return render(request, 'instructor_cursos.html', {'cursos': cursos})


@rol_requerido('instructor')
@modulo_requerido('evaluaciones')
def instructor_evaluaciones(request):
    evaluaciones = Evaluacion.objects.filter(
        instructor=request.user
    ).select_related('compania').prefetch_related(
        'asignaciones__soldado__perfil'
    )
    calificaciones = Calificacion.objects.filter(
        curso__instructor=request.user
    ).select_related('estudiante', 'estudiante__perfil', 'curso').order_by('-creado_en')[:30]

    return render(request, 'instructor_evaluaciones.html', {
        'evaluaciones': evaluaciones,
        'total_evaluaciones': evaluaciones.count(),
        'calificaciones': calificaciones,
        'total_calificaciones': Calificacion.objects.filter(curso__instructor=request.user).count(),
    })


@rol_requerido('instructor')
@modulo_requerido('soldados')
def instructor_soldados(request):
    inscripciones = Inscripcion.objects.filter(
        curso__instructor=request.user
    ).select_related('estudiante', 'estudiante__perfil', 'curso')
    return render(request, 'instructor_soldados.html', {
        'inscripciones': inscripciones,
        'total_soldados': inscripciones.count(),
    })


@rol_requerido('instructor')
@modulo_requerido('reportes')
def instructor_reportes(request):
    cursos = Curso.objects.filter(instructor=request.user).annotate(
        total_soldados=Count('inscripciones'),
        promedio=Avg('calificacion__nota')
    )
    return render(request, 'instructor_reportes.html', {'cursos': cursos})


@rol_requerido('soldado')
def soldado_dashboard(request):
    return render(request, 'soldado.html', {
        'configuracion': obtener_configuracion_usuario(request.user)
    })


@rol_requerido('instructor')
def instructor_guardar_calificacion(request):
    """Crea o actualiza una calificación de curso desde el panel del instructor."""
    if request.method != 'POST':
        return redirect('instructor_evaluaciones')

    curso_id = request.POST.get('curso_id', '').strip()
    estudiante_id = request.POST.get('estudiante_id', '').strip()
    nota = request.POST.get('nota', '').strip()
    observaciones = request.POST.get('observaciones', '').strip()
    calificacion_id = request.POST.get('calificacion_id', '').strip()

    try:
        curso = Curso.objects.get(id=curso_id, instructor=request.user)
        nota_val = float(nota)

        if calificacion_id:
            cal = get_object_or_404(Calificacion, id=calificacion_id, curso=curso)
            cal.nota = nota_val
            cal.observaciones = observaciones
            cal.save()
        else:
            estudiante = get_object_or_404(User, id=estudiante_id)
            Calificacion.objects.update_or_create(
                curso=curso,
                estudiante=estudiante,
                tarea=None,
                defaults={'nota': nota_val, 'observaciones': observaciones},
            )
    except (Curso.DoesNotExist, ValueError):
        pass

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        return JsonResponse({'ok': True})
    return redirect('instructor_evaluaciones')


@rol_requerido('instructor')
def instructor_listar_inscritos(request):
    """Devuelve JSON con los soldados inscritos en un curso del instructor."""
    curso_id = request.GET.get('curso_id', '')
    try:
        curso = Curso.objects.get(id=curso_id, instructor=request.user)
    except Curso.DoesNotExist:
        return JsonResponse({'soldados': []})

    inscritos = Inscripcion.objects.filter(curso=curso).select_related(
        'estudiante', 'estudiante__perfil'
    )
    data = [
        {
            'id': i.estudiante.id,
            'nombre': i.estudiante.get_full_name() or i.estudiante.username,
            'grado': getattr(i.estudiante.perfil, 'grado', '') or '',
        }
        for i in inscritos
    ]
    return JsonResponse({'soldados': data})
