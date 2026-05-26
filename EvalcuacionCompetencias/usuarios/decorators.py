from django.shortcuts import redirect
from django.http import JsonResponse
from functools import wraps


def rol_requerido(roles):
    if isinstance(roles, str):
        roles = [roles]

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                if request.user.perfil.rol not in roles:
                    return redirect('login')
            except Exception:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def modulo_requerido(clave, seccion='menu_lateral'):
    """
    Blocks access to a view if the user's effective config disables the module.
    Returns 403 JSON for AJAX requests, redirects to the user's own dashboard otherwise.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            from .helpers import obtener_configuracion_usuario
            config = obtener_configuracion_usuario(request.user)
            if not config[seccion].get(clave, True):
                is_ajax = (
                    request.headers.get('X-Requested-With') == 'XMLHttpRequest'
                    or 'application/json' in request.headers.get('Accept', '')
                    or request.content_type == 'application/json'
                )
                if is_ajax:
                    return JsonResponse({'error': 'Módulo no disponible'}, status=403)
                try:
                    rol = request.user.perfil.rol
                except Exception:
                    rol = 'admin'
                if rol == 'instructor':
                    return redirect('instructor_dashboard')
                if rol == 'soldado':
                    return redirect('soldado_dashboard')
                return redirect('admin_dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
