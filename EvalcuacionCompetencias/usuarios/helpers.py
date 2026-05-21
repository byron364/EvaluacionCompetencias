from .models import ConfiguracionUsuario

MENU_DEFAULTS = {
    # Admin
    'inicio': True,
    'batallones': True,
    'companias': True,
    'usuarios': True,
    'evaluaciones': True,
    'inscripciones': True,
    'test': True,
    'reportes': True,
    # Instructor / Admin
    'cursos': True,
    'soldados': True,
    # Soldado
    'resultados': True,
    'retroalimentacion': True,
}

DASHBOARD_DEFAULTS = {
    'estadisticas': True,
    'accesos_rapidos': True,
    'ultimas_actividades': True,
    'notificaciones': True,
    'calendario': True,
}

ACCESOS_DEFAULTS = {
    'crear_usuario': True,
    'crear_curso': True,
    'exportar_reporte': True,
    'cargar_excel': True,
    'descargar_plantilla': True,
    'registrar_soldados': True,
    'calificar': True,
    'generar_reporte': True,
    'ver_calendario': True,
}


def _aplicar_preferencias(permitido, personal):
    """
    Intersects admin-allowed keys with user personal preferences.
    Admin False → always False. Admin True → user decides (default True).
    """
    result = {}
    for key, allowed in permitido.items():
        if not allowed:
            result[key] = False
        else:
            result[key] = personal.get(key, True)
    return result


def obtener_configuracion_usuario(usuario):
    """
    Returns the effective config for a user: two layers.
    Layer 1 (allowed): from PerfilPanel assigned by admin (all True if none).
    Layer 2 (personal): user's own preferences within what's allowed.
    """
    try:
        config_obj = usuario.configuracion
        usuario_config = config_obj.configuracion or {}
        perfil = config_obj.perfil_asignado
    except ConfiguracionUsuario.DoesNotExist:
        usuario_config = {}
        perfil = None

    if perfil and perfil.configuracion:
        p = perfil.configuracion
        permitido_menu = {**MENU_DEFAULTS, **p.get('menu_lateral', {})}
        permitido_dashboard = {**DASHBOARD_DEFAULTS, **p.get('dashboard', {})}
        permitido_accesos = {**ACCESOS_DEFAULTS, **p.get('accesos_rapidos', {})}
    else:
        permitido_menu = MENU_DEFAULTS.copy()
        permitido_dashboard = DASHBOARD_DEFAULTS.copy()
        permitido_accesos = ACCESOS_DEFAULTS.copy()

    personal_menu = usuario_config.get('menu_lateral', {})
    personal_dashboard = usuario_config.get('dashboard', {})
    personal_accesos = usuario_config.get('accesos_rapidos', {})

    return {
        'menu_lateral': _aplicar_preferencias(permitido_menu, personal_menu),
        'dashboard': _aplicar_preferencias(permitido_dashboard, personal_dashboard),
        'accesos_rapidos': _aplicar_preferencias(permitido_accesos, personal_accesos),
    }


def obtener_modulos_bloqueados(usuario):
    """
    Returns sets of keys that the admin-assigned profile has disabled.
    Used by the config UI to lock checkboxes.
    """
    try:
        perfil = usuario.configuracion.perfil_asignado
    except ConfiguracionUsuario.DoesNotExist:
        perfil = None

    if not perfil or not perfil.configuracion:
        return {'menu_lateral': set(), 'dashboard': set(), 'accesos_rapidos': set()}

    p = perfil.configuracion
    return {
        'menu_lateral': {k for k, v in p.get('menu_lateral', {}).items() if not v},
        'dashboard': {k for k, v in p.get('dashboard', {}).items() if not v},
        'accesos_rapidos': {k for k, v in p.get('accesos_rapidos', {}).items() if not v},
    }
