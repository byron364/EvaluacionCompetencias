from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    ROLES = (
        ('admin', 'Administrador'),
        ('soldado', 'Soldado'),
        ('instructor', 'Instructor'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='soldado')

    documento = models.CharField(max_length=20, unique=True, db_index=True)
    unidad = models.CharField(max_length=100, blank=True, null=True)
    grado = models.CharField(max_length=50, blank=True, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} ({self.rol})"