from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    ROLES = (
        ('admin', 'Administrador'),
        ('soldado', 'Soldado'),
        ('instructor', 'Instructor'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"