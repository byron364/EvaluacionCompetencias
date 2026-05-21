import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from ..models import PerfilPanel, ConfiguracionUsuario
from ..decorators import rol_requerido
from ..helpers import MENU_DEFAULTS, DASHBOARD_DEFAULTS, ACCESOS_DEFAULTS


@login_required
@rol_requerido('admin')
def admin_perfiles_panel(request):
    perfiles = PerfilPanel.objects.prefetch_related('usuarios_asignados').all()
    usuarios = User.objects.filter(
        perfil__rol__in=['admin', 'instructor', 'soldado']
    ).select_related('perfil')

    return render(request, 'admin_perfiles.html', {
        'perfiles': perfiles,
        'usuarios': usuarios,
    })


@login_required
@rol_requerido('admin')
def listar_perfiles_json(request):
    perfiles = PerfilPanel.objects.all().values('id', 'nombre', 'descripcion')
    return JsonResponse({'perfiles': list(perfiles)})


@login_required
@rol_requerido('admin')
def obtener_perfil_json(request, perfil_id):
    try:
        perfil = PerfilPanel.objects.get(id=perfil_id)
        return JsonResponse({
            'id': perfil.id,
            'nombre': perfil.nombre,
            'descripcion': perfil.descripcion or '',
            'configuracion': perfil.configuracion,
        })
    except PerfilPanel.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=404)


@login_required
@rol_requerido('admin')
@csrf_exempt
def crear_perfil_panel(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        if not nombre:
            return JsonResponse({'error': 'El nombre es obligatorio'}, status=400)
        if PerfilPanel.objects.filter(nombre=nombre).exists():
            return JsonResponse({'error': 'Ya existe un perfil con ese nombre'}, status=400)

        configuracion = _construir_configuracion(data)
        perfil = PerfilPanel.objects.create(
            nombre=nombre,
            descripcion=data.get('descripcion', '').strip() or None,
            configuracion=configuracion,
            creado_por=request.user,
        )
        return JsonResponse({'mensaje': 'Perfil creado correctamente', 'id': perfil.id}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@rol_requerido('admin')
@csrf_exempt
def editar_perfil_panel(request, perfil_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        perfil = PerfilPanel.objects.get(id=perfil_id)
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        if not nombre:
            return JsonResponse({'error': 'El nombre es obligatorio'}, status=400)
        if PerfilPanel.objects.filter(nombre=nombre).exclude(id=perfil_id).exists():
            return JsonResponse({'error': 'Ya existe un perfil con ese nombre'}, status=400)

        perfil.nombre = nombre
        perfil.descripcion = data.get('descripcion', '').strip() or None
        perfil.configuracion = _construir_configuracion(data)
        perfil.save()
        return JsonResponse({'mensaje': 'Perfil actualizado correctamente'})
    except PerfilPanel.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@rol_requerido('admin')
@csrf_exempt
def eliminar_perfil_panel(request, perfil_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        perfil = PerfilPanel.objects.get(id=perfil_id)
        usuarios_afectados = perfil.usuarios_asignados.count()
        perfil.delete()
        return JsonResponse({
            'mensaje': f'Perfil eliminado. {usuarios_afectados} usuario(s) quedaron sin perfil asignado.'
        })
    except PerfilPanel.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@rol_requerido('admin')
@csrf_exempt
def asignar_perfil_panel(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        usuario_id = data.get('usuario_id')
        perfil_id = data.get('perfil_id')

        usuario = User.objects.get(id=usuario_id)
        config, _ = ConfiguracionUsuario.objects.get_or_create(
            usuario=usuario,
            defaults={'configuracion': {}}
        )

        if perfil_id:
            perfil = PerfilPanel.objects.get(id=perfil_id)
            config.perfil_asignado = perfil
            msg = f'Perfil "{perfil.nombre}" asignado a {usuario.get_full_name() or usuario.username}'
        else:
            config.perfil_asignado = None
            msg = f'Perfil removido de {usuario.get_full_name() or usuario.username}'

        config.save()
        return JsonResponse({'mensaje': msg})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    except PerfilPanel.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def _construir_configuracion(data):
    """Builds the JSON config structure from POST data keys."""
    menu_keys = list(MENU_DEFAULTS.keys())
    dashboard_keys = list(DASHBOARD_DEFAULTS.keys())
    accesos_keys = list(ACCESOS_DEFAULTS.keys())

    return {
        'menu_lateral': {k: bool(data.get(f'menu_{k}')) for k in menu_keys},
        'dashboard': {k: bool(data.get(f'dashboard_{k}')) for k in dashboard_keys},
        'accesos_rapidos': {k: bool(data.get(f'accesos_{k}')) for k in accesos_keys},
    }
