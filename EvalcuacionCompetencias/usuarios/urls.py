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
    path('soldado-dashboard/', soldado_dashboard, name='soldado_dashboard'),
    path('soldado/', soldado_dashboard),  # 👈 AGREGA ESTA


    # 🚀 SPA (VISTAS DINÁMICAS)
    path('inicio/', inicio, name='inicio'),
    path('cursos/', cursos, name='cursos'),
    path('evaluaciones/', evaluaciones, name='evaluaciones'),
    path('resultados/', resultados, name='resultados'),
    path('retro/', retroalimentacion, name='retroalimentacion'),
]