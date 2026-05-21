from django.urls import path
from . import views
from .views.resolver_test_views import (
    finalizar_test,
    obtener_test
)
from .views.crear_test_views import (
    admin_test,
    crear_test,
    cambiar_estado_test,
    detalle_test
)                                  
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
    path('evaluaciones/', views.admin_evaluaciones, name='evaluaciones'),
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
    'crear-evaluacion/',
    views.crear_evaluacion,
    name='crear_evaluacion'
    ),
    path(
        'listar-evaluaciones/',
          views.listar_evaluaciones,
            name='listar_evaluaciones' ),
    
    path(
    'editar-evaluacion/<int:evaluacion_id>/',
    views.editar_evaluacion,
    name='editar_evaluacion' ),

    path(
    'eliminar-evaluacion/<int:evaluacion_id>/',
    views.eliminar_evaluacion,
    name='eliminar_evaluacion' ),

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

    path(
    "guardar-huella/",
    views.guardar_huella,
    name="guardar_huella"
    ),
    path(
    "abrir-huellero/<str:documento>/",
    views.abrir_huellero,
    name="abrir_huellero"
    ),
    path(
    'validar-huella-temp/<str:documento>/',
    views.validar_huella_temp
    ),
    path(
    "biometrico/",
    views.biometrico,
    name="biometrico"
    ),

    path(
    "registrar-huella-usuario/<str:documento>/",
    views.registrar_huella_usuario,
    name="registrar_huella_usuario"
    ),

    path(
    "buscar-companias/",
    views.buscar_companias,
    name="buscar_companias"
    ),

    path(
    "activar-evaluacion/<int:evaluacion_id>/",
    views.activar_evaluacion,
    name="activar_evaluacion"
    ),

    path(
    "detalle-evaluacion/<int:evaluacion_id>/",
    views.detalle_evaluacion,
    name="detalle_evaluacion"
    ),

    path(
    "editar-evaluacion/<int:evaluacion_id>/",
    views.editar_evaluacion,
    name="editar_evaluacion"
    ),

    path(
    "crear-test/",
    views.crear_test,
    name="crear_test"
    ),

    path(
    "admin-test/",
    views.admin_test,
    name="admin_test"
    ),

    path(
    "finalizar-test/",
    views.finalizar_test,
    name="finalizar_test"
    ),

    path(
    "obtener-test/<int:test_id>/",
    obtener_test,
    name="obtener_test"
    ),

    path(
    "activar-test/<int:test_id>/",
    cambiar_estado_test,
    name="activar_test"
    ),

    path(
    "detalle-test/<int:test_id>/",
    detalle_test,
    name="detalle_test"
    ),

]