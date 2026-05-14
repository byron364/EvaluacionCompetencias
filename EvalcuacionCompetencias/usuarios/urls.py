from django.urls import path
from . import views
                                     
urlpatterns = [
    # 🔐 Autenticación
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # 📊 Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('instructor-dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('instructor/inicio/', views.instructor_inicio, name='instructor_inicio'),
    path('instructor/cursos/', views.instructor_cursos, name='instructor_cursos'),
    path('instructor/evaluaciones/', views.instructor_evaluaciones, name='instructor_evaluaciones'),
    path('instructor/soldados/', views.instructor_soldados, name='instructor_soldados'),
    path('instructor/reportes/', views.instructor_reportes, name='instructor_reportes'),
    path('soldado-dashboard/', views.soldado_dashboard, name='soldado_dashboard'),
    path('soldado/', views.soldado_dashboard),  
    path('usuarios/', views.admin_usuarios, name='usuarios'),
    path('cursos/', views.admin_cursos, name='cursos'),
    path('reportes/', views.admin_reportes, name='reportes'),
    path('admin-dashboard-partial/', views.admin_dashboard_partial),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path("batallones/",  views.admin_batallones, name="admin_batallones"),
    path("evaluaciones/", views.admin_evaluaciones, name="admin_evaluaciones"),
    path("inscripciones/", views.admin_inscripciones, name="admin_inscripciones"),
    path("test/", views.admin_test, name="admin_test"),
    path("configuracion/", views.admin_configuracion, name="admin_configuracion"),
    path('inicio/', views.inicio, name='inicio'),
    path('cursos/', views.cursos, name='cursos'),
    path('evaluaciones/', views.evaluaciones, name='evaluaciones'),
    path('resultados/', views.resultados, name='resultados'),
    path('retro/', views.retroalimentacion, name='retroalimentacion'),
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
    "crear-batallon/",
    views.crear_batallon,
    name="crear_batallon" ),

    path(
    'editar-batallon/<int:batallon_id>/',
    views.editar_batallon,
    name='editar_batallon' ),

    path(
    'cambiar-estado-batallon/<int:batallon_id>/',
    views.cambiar_estado_batallon,
    name='cambiar_estado_batallon' ),

    path(
    "companias/",
    views.admin_companias,
    name="admin_companias" ),
    
    path(
    "crear-compania/",
    views.crear_compania,
    name="crear_compania" ),

    path(
    "editar-compania/<int:id>/",
    views.editar_compania,
    name="editar_compania"
    ),

    path(
    "toggle-compania/<int:id>/",
    views.toggle_compania,
    name="toggle_compania"
    ),

    path(
    "eliminar-compania/<int:id>/",
    views.eliminar_compania,
    name="eliminar_compania"
    ),
]