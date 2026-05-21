import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from ..models import ConfiguracionUsuario
from ..decorators import rol_requerido, modulo_requerido
from ..helpers import obtener_modulos_bloqueados


def inicio(request):
    return render(request, 'inicio.html')


def cursos(request):
    return render(request, 'cursos.html')


def evaluaciones(request):
    return render(request, 'evaluaciones.html')


def resultados(request):
    return render(request, 'resultados.html')


def retroalimentacion(request):
    return render(request, 'retro.html')


@modulo_requerido('reportes')
def admin_reportes(request):
    return render(request, 'admin_reportes.html')


@modulo_requerido('inscripciones')
def admin_inscripciones(request):
    return render(request, "admin_inscripciones.html")


@modulo_requerido('test')
def admin_test(request):
    return render(request, "admin_test.html")


@rol_requerido(['admin', 'instructor'])
def admin_configuracion(request):
    config, _ = ConfiguracionUsuario.objects.get_or_create(
        usuario=request.user,
        defaults={'configuracion': {}}
    )

    rol = request.user.perfil.rol
    admin_menu_opciones = [
        {'key': 'inicio', 'label': 'Inicio'},
        {'key': 'batallones', 'label': 'Batallones'},
        {'key': 'companias', 'label': 'Compañías'},
        {'key': 'usuarios', 'label': 'Gestión de Usuarios'},
        {'key': 'evaluaciones', 'label': 'Evaluaciones'},
        {'key': 'inscripciones', 'label': 'Inscripciones'},
        {'key': 'test', 'label': 'Tests'},
        {'key': 'reportes', 'label': 'Reportes'},
    ]
    instructor_menu_opciones = [
        {'key': 'inicio', 'label': 'Panel principal'},
        {'key': 'cursos', 'label': 'Mis cursos'},
        {'key': 'evaluaciones', 'label': 'Calificar'},
        {'key': 'soldados', 'label': 'Ver soldados'},
        {'key': 'reportes', 'label': 'Subir resultados'},
    ]
    admin_accesos_opciones = [
        {'key': 'crear_usuario', 'label': 'Crear Usuario'},
        {'key': 'crear_curso', 'label': 'Crear Curso'},
        {'key': 'exportar_reporte', 'label': 'Exportar Reporte'},
        {'key': 'cargar_excel', 'label': 'Cargar Excel'},
        {'key': 'descargar_plantilla', 'label': 'Descargar Plantilla'},
    ]
    instructor_accesos_opciones = [
        {'key': 'inicio', 'label': 'Ir al Panel'},
        {'key': 'cursos', 'label': 'Mis cursos'},
        {'key': 'evaluaciones', 'label': 'Calificar ahora'},
        {'key': 'reportes', 'label': 'Subir resultados'},
    ]
    menu_opciones = admin_menu_opciones if rol == 'admin' else instructor_menu_opciones
    accesos_opciones = admin_accesos_opciones if rol == 'admin' else instructor_accesos_opciones
    dashboard_opciones = [
        {'key': 'estadisticas', 'label': 'Estadísticas Generales'},
        {'key': 'accesos_rapidos', 'label': 'Accesos Rápidos'},
        {'key': 'ultimas_actividades', 'label': 'Últimas Actividades'},
        {'key': 'notificaciones', 'label': 'Notificaciones'},
        {'key': 'calendario', 'label': 'Calendario'},
    ]

    bloqueados = obtener_modulos_bloqueados(request.user)

    if request.method == 'POST':
        configuracion = {'menu_lateral': {}, 'dashboard': {}, 'accesos_rapidos': {}}
        for opcion in menu_opciones:
            key = opcion['key']
            if key in bloqueados['menu_lateral']:
                configuracion['menu_lateral'][key] = False
            else:
                configuracion['menu_lateral'][key] = request.POST.get(f"menu_{key}", 'off') == 'on'

        for opcion in dashboard_opciones:
            key = opcion['key']
            if key in bloqueados['dashboard']:
                configuracion['dashboard'][key] = False
            else:
                configuracion['dashboard'][key] = request.POST.get(f"dashboard_{key}", 'off') == 'on'

        for opcion in accesos_opciones:
            key = opcion['key']
            if key in bloqueados['accesos_rapidos']:
                configuracion['accesos_rapidos'][key] = False
            else:
                configuracion['accesos_rapidos'][key] = request.POST.get(f"accesos_{key}", 'off') == 'on'

        config.configuracion = configuracion
        config.save()
        messages.success(request, 'Configuración guardada correctamente.')
        if rol == 'instructor':
            return redirect('instructor_dashboard')
        return redirect('admin_dashboard')

    configuracion_data = config.configuracion or {}
    menu_lateral_data = configuracion_data.get('menu_lateral', {})
    dashboard_data = configuracion_data.get('dashboard', {})
    accesos_data = configuracion_data.get('accesos_rapidos', {})

    menu_opciones = [
        {
            **opcion,
            'checked': menu_lateral_data.get(opcion['key'], True),
            'bloqueado': opcion['key'] in bloqueados['menu_lateral'],
        }
        for opcion in menu_opciones
    ]
    dashboard_opciones = [
        {
            **opcion,
            'checked': dashboard_data.get(opcion['key'], True),
            'bloqueado': opcion['key'] in bloqueados['dashboard'],
        }
        for opcion in dashboard_opciones
    ]
    accesos_opciones = [
        {
            **opcion,
            'checked': accesos_data.get(opcion['key'], True),
            'bloqueado': opcion['key'] in bloqueados['accesos_rapidos'],
        }
        for opcion in accesos_opciones
    ]

    return render(request, "admin_configuracion.html", {
        'configuracion': config.configuracion,
        'menu_opciones': menu_opciones,
        'dashboard_opciones': dashboard_opciones,
        'accesos_opciones': accesos_opciones,
        'rol': rol,
        'perfil_asignado': config.perfil_asignado,
    })


@rol_requerido('admin')
def admin_editar_config_usuario(request, usuario_id):
    try:
        usuario_obj = User.objects.select_related('perfil').get(id=usuario_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    rol = usuario_obj.perfil.rol
    config, _ = ConfiguracionUsuario.objects.get_or_create(
        usuario=usuario_obj, defaults={'configuracion': {}}
    )

    if rol == 'soldado':
        menu_opciones = [
            {'key': 'inicio',            'label': 'Inicio'},
            {'key': 'cursos',            'label': 'Mis Cursos'},
            {'key': 'evaluaciones',      'label': 'Evaluaciones'},
            {'key': 'resultados',        'label': 'Resultados'},
            {'key': 'retroalimentacion', 'label': 'Retroalimentación'},
        ]
        accesos_opciones = []
    elif rol == 'instructor':
        menu_opciones = [
            {'key': 'inicio',       'label': 'Panel principal'},
            {'key': 'cursos',       'label': 'Mis cursos'},
            {'key': 'evaluaciones', 'label': 'Calificar'},
            {'key': 'soldados',     'label': 'Ver soldados'},
            {'key': 'reportes',     'label': 'Subir resultados'},
        ]
        accesos_opciones = [
            {'key': 'inicio',       'label': 'Ir al Panel'},
            {'key': 'cursos',       'label': 'Mis cursos'},
            {'key': 'evaluaciones', 'label': 'Calificar ahora'},
            {'key': 'reportes',     'label': 'Subir resultados'},
        ]
    else:
        menu_opciones = [
            {'key': 'inicio',        'label': 'Inicio'},
            {'key': 'batallones',    'label': 'Batallones'},
            {'key': 'companias',     'label': 'Compañías'},
            {'key': 'usuarios',      'label': 'Gestión de Usuarios'},
            {'key': 'evaluaciones',  'label': 'Evaluaciones'},
            {'key': 'inscripciones', 'label': 'Inscripciones'},
            {'key': 'test',          'label': 'Tests'},
            {'key': 'reportes',      'label': 'Reportes'},
        ]
        accesos_opciones = [
            {'key': 'crear_usuario',       'label': 'Crear Usuario'},
            {'key': 'crear_curso',         'label': 'Crear Curso'},
            {'key': 'exportar_reporte',    'label': 'Exportar Reporte'},
            {'key': 'cargar_excel',        'label': 'Cargar Excel'},
            {'key': 'descargar_plantilla', 'label': 'Descargar Plantilla'},
        ]

    dashboard_opciones = [
        {'key': 'estadisticas',        'label': 'Estadísticas Generales'},
        {'key': 'accesos_rapidos',     'label': 'Accesos Rápidos'},
        {'key': 'ultimas_actividades', 'label': 'Últimas Actividades'},
        {'key': 'notificaciones',      'label': 'Notificaciones'},
        {'key': 'calendario',          'label': 'Calendario'},
    ]

    bloqueados = obtener_modulos_bloqueados(usuario_obj)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, Exception):
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        configuracion = {'menu_lateral': {}, 'dashboard': {}, 'accesos_rapidos': {}}
        for op in menu_opciones:
            k = op['key']
            configuracion['menu_lateral'][k] = False if k in bloqueados['menu_lateral'] else bool(data.get(f'menu_{k}'))
        for op in dashboard_opciones:
            k = op['key']
            configuracion['dashboard'][k] = False if k in bloqueados['dashboard'] else bool(data.get(f'dashboard_{k}'))
        for op in accesos_opciones:
            k = op['key']
            configuracion['accesos_rapidos'][k] = False if k in bloqueados['accesos_rapidos'] else bool(data.get(f'accesos_{k}'))

        config.configuracion = configuracion
        config.save()
        return JsonResponse({'mensaje': f'Configuración de {usuario_obj.get_full_name() or usuario_obj.username} guardada correctamente.'})

    cfg = config.configuracion or {}
    menu_lateral_data  = cfg.get('menu_lateral', {})
    dashboard_data     = cfg.get('dashboard', {})
    accesos_data       = cfg.get('accesos_rapidos', {})

    menu_opciones = [
        {**op, 'checked': menu_lateral_data.get(op['key'], True), 'bloqueado': op['key'] in bloqueados['menu_lateral']}
        for op in menu_opciones
    ]
    dashboard_opciones = [
        {**op, 'checked': dashboard_data.get(op['key'], True), 'bloqueado': op['key'] in bloqueados['dashboard']}
        for op in dashboard_opciones
    ]
    accesos_opciones = [
        {**op, 'checked': accesos_data.get(op['key'], True), 'bloqueado': op['key'] in bloqueados['accesos_rapidos']}
        for op in accesos_opciones
    ]

    return render(request, 'admin_config_usuario.html', {
        'usuario_obj': usuario_obj,
        'rol': rol,
        'menu_opciones': menu_opciones,
        'dashboard_opciones': dashboard_opciones,
        'accesos_opciones': accesos_opciones,
        'perfil_asignado': config.perfil_asignado,
    })
