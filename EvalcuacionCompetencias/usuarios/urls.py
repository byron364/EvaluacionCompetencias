from django.urls import path
from .views import *

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


    # 🚀 SPA (VISTAS DINÁMICAS)
    path('inicio/', inicio, name='inicio'),
    path('cursos/', cursos, name='cursos'),
    path('evaluaciones/', evaluaciones, name='evaluaciones'),
    path('resultados/', resultados, name='resultados'),
    path('retro/', retroalimentacion, name='retroalimentacion'),
]