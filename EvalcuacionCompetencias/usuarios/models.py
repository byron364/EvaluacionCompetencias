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
    
class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)

    descripcion = models.TextField(blank=True, null=True)

    instructor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cursos_instructor"
        )

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    cupo_maximo = models.IntegerField(default=30)

    activo = models.BooleanField(default=True)

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class Inscripcion(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="inscripciones"
    )

    estudiante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="mis_cursos"
    )

    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("curso", "estudiante")

    def __str__(self):
        return f"{self.estudiante.username} - {self.curso.nombre}"

class Tarea(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="tareas"
    )

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    fecha_entrega = models.DateField()

    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.titulo

class Evaluacion(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="evaluaciones"
    )

    titulo = models.CharField(max_length=200)
    fecha = models.DateField()

    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.titulo

class Asistencia(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE
    )

    estudiante = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    fecha = models.DateField()

    presente = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.estudiante.username} - {self.fecha}"

class ArchivoCurso(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="archivos"
    )

    titulo = models.CharField(max_length=200)

    archivo = models.FileField(
        upload_to="cursos/"
    )

    subido_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Calificacion(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE
    )

    estudiante = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    evaluacion = models.ForeignKey(
        Evaluacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    nota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.username} - {self.nota}"