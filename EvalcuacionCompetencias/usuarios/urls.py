from django.urls import path
from .views import * 
from . import views
                                     
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
    path('cursos/', cursos, name='cursos'),
    path('reportes/', admin_reportes, name='reportes'),
    path('admin-dashboard-partial/', admin_dashboard_partial),
    path('crear-usuario/', crear_usuario, name='crear_usuario'),


    path('inicio/', inicio, name='inicio'),
    path('evaluaciones/', evaluaciones, name='evaluaciones'),
    path('resultados/', resultados, name='resultados'),
    path('retro/', retroalimentacion, name='retroalimentacion'),
    path( "cargar-usuarios-excel/", 
         views.cargar_usuarios_excel, 
         name="cargar_usuarios_excel" ),
    path( "descargar-plantilla-excel/",
            views.descargar_plantilla_excel, 
            name="descargar_plantilla_excel" ),

     path(
        "obtener-estadisticas/",
        views.obtener_estadisticas,
        name="obtener_estadisticas"),


    path(
        "usuarios/",
        views.listar_usuarios,
        name="listar_usuarios"),

    path(
        "eliminar-usuario/<int:user_id>/",
        views.eliminar_usuario,
        name="eliminar_usuario"),

    path(
        "editar-usuario/<int:user_id>/",
        views.editar_usuario,
        name="editar_usuario"),

    path( 
        "crear-curso/", 
        views.crear_curso, 
        name="crear_curso" ),

    path(
        'listar-cursos/',
          views.listar_cursos,
            name='listar_cursos' ),
    
    path(
    'editar-curso/<int:curso_id>/',
    views.editar_curso,
    name='editar_curso' ),

    path(
    'eliminar-curso/<int:curso_id>/',
    views.eliminar_curso,
    name='eliminar_curso' ),

    path(
    'asignar-soldado-curso/',
    views.asignar_soldado_curso,
    name='asignar_soldado_curso' ),

    path(
    'exportar-reporte/<str:tipo>/',
    views.exportar_reporte,
    name='exportar_reporte' ),
]
