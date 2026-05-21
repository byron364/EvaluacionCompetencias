from django.urls import path
from .views.auth_views import login_view, logout_view, registro_view
from .views.dashboard_views import admin_dashboard, admin_dashboard_partial, obtener_estadisticas
from .views.instructor_views import instructor_dashboard, instructor_inicio, instructor_cursos, instructor_evaluaciones, instructor_soldados, instructor_reportes, soldado_dashboard
from .views.extras_views import inicio, evaluaciones, resultados, retroalimentacion, admin_reportes, admin_inscripciones, admin_test, admin_configuracion, admin_editar_config_usuario
from .views.usuarios_views import admin_usuarios, listar_usuarios, eliminar_usuario, editar_usuario, crear_usuario, cargar_usuarios_excel, descargar_plantilla_excel
from .views.cursos_views import admin_cursos, crear_curso, listar_cursos, editar_curso, eliminar_curso, asignar_soldado_curso
from .views.batallones_views import admin_batallones, crear_batallon, editar_batallon, cambiar_estado_batallon, admin_companias, crear_compania, editar_compania, toggle_compania, eliminar_compania
from .views.evaluaciones_views import admin_evaluaciones
from .views.reportes_views import exportar_reporte
                                     
urlpatterns = [
    # 🔐 Autenticación
    path('', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('logout/', logout_view, name='logout'),

    # 📊 Dashboards
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('instructor-dashboard/', instructor_dashboard, name='instructor_dashboard'),
    path('instructor/inicio/', instructor_inicio, name='instructor_inicio'),
    path('instructor/cursos/', instructor_cursos, name='instructor_cursos'),
    path('instructor/evaluaciones/', instructor_evaluaciones, name='instructor_evaluaciones'),
    path('instructor/soldados/', instructor_soldados, name='instructor_soldados'),
    path('instructor/reportes/', instructor_reportes, name='instructor_reportes'),
    path('soldado-dashboard/', soldado_dashboard, name='soldado_dashboard'),
    path('soldado/', soldado_dashboard),  # 👈 AGREGA ESTA
    path('usuarios/', admin_usuarios, name='usuarios'),
    path('cursos/', admin_cursos, name='cursos'),
    path('reportes/', admin_reportes, name='reportes'),
    path('admin-dashboard-partial/', admin_dashboard_partial),
    path('crear-usuario/', crear_usuario, name='crear_usuario'),

    path('inicio/', inicio, name='inicio'),
    path('evaluaciones/', evaluaciones, name='evaluaciones'),
    path('resultados/', resultados, name='resultados'),
    path('retro/', retroalimentacion, name='retroalimentacion'),
    path("batallones/", admin_batallones, name="admin_batallones"),
    path("evaluaciones/", admin_evaluaciones, name="admin_evaluaciones"),
    path("inscripciones/", admin_inscripciones, name="admin_inscripciones"),
    path("test/", admin_test, name="admin_test"),
    path("configuracion/", admin_configuracion, name="admin_configuracion"),
    path("configurar-usuario/<int:usuario_id>/", admin_editar_config_usuario, name="admin_editar_config_usuario"),
    path("cargar-usuarios-excel/", cargar_usuarios_excel, name="cargar_usuarios_excel"),
    path("descargar-plantilla-excel/", descargar_plantilla_excel, name="descargar_plantilla_excel"),
    path("obtener-estadisticas/", obtener_estadisticas, name="obtener_estadisticas"),
    path("usuarios/", listar_usuarios, name="listar_usuarios"),
    path("eliminar-usuario/<int:user_id>/", eliminar_usuario, name="eliminar_usuario"),
    path("editar-usuario/<int:user_id>/", editar_usuario, name="editar_usuario"),
    path("crear-curso/", crear_curso, name="crear_curso"),
    path('listar-cursos/', listar_cursos, name='listar_cursos'),
    path('editar-curso/<int:curso_id>/', editar_curso, name='editar_curso'),
    path('eliminar-curso/<int:curso_id>/', eliminar_curso, name='eliminar_curso'),
    path('asignar-soldado-curso/', asignar_soldado_curso, name='asignar_soldado_curso'),
    path('exportar-reporte/<str:tipo>/', exportar_reporte, name='exportar_reporte'),
    path("crear-batallon/", crear_batallon, name="crear_batallon"),
    path('editar-batallon/<int:batallon_id>/', editar_batallon, name='editar_batallon'),
    path('cambiar-estado-batallon/<int:batallon_id>/', cambiar_estado_batallon, name='cambiar_estado_batallon'),
    path("companias/", admin_companias, name="admin_companias"),
    path("crear-compania/", crear_compania, name="crear_compania"),
    path("editar-compania/<int:id>/", editar_compania, name="editar_compania"),
    path("toggle-compania/<int:id>/", toggle_compania, name="toggle_compania"),
    path("eliminar-compania/<int:id>/", eliminar_compania, name="eliminar_compania"),

]
