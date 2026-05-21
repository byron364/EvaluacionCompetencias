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
    batallon = models.ForeignKey( 'Batallon', on_delete=models.SET_NULL, null=True, blank=True, related_name='personal')
    compania = models.ForeignKey(

    'Compania',

    on_delete=models.SET_NULL,

    null=True,

    blank=True,

    related_name="usuarios"
)
    activo = models.BooleanField(
        default=True
    )

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
    
class Batallon(models.Model):

    nombre = models.CharField(
        max_length=150,
        unique=True
    )

    codigo = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    ciudad = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    soldados = models.ManyToManyField(
        User,
        related_name="batallones_soldado",
        blank=True
    )

    cuadros = models.ManyToManyField(
        User,
        related_name="batallones_cuadro",
        blank=True
    )

    def total_soldados(self):

        return self.soldados.count()

    def total_cuadros(self):

        return self.cuadros.count()

    def save(self, *args, **kwargs):

        if not self.codigo:

            ultimo = Batallon.objects.order_by(
                '-id'
            ).first()

            if ultimo:

                ultimo_numero = int(
                    ultimo.codigo.split('-')[1]
                )

                nuevo_numero = ultimo_numero + 1

            else:

                nuevo_numero = 1

            self.codigo = (
                f'BAT-{nuevo_numero:04d}'
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.nombre

    nombre = models.CharField(
        max_length=150,
        unique=True
    )

    codigo = models.CharField(
    max_length=20,
    unique=True,
    editable=False
    )

    ciudad = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    soldados = models.ManyToManyField(
        User,
        related_name="batallones_soldado",
        blank=True
    )

    cuadros = models.ManyToManyField(
        User,
        related_name="batallones_cuadro",
        blank=True
    )

    def total_soldados(self):

        return self.soldados.count()

    def total_cuadros(self):

        return self.cuadros.count()

    def __str__(self):

        return self.nombre

class Compania(models.Model):

    batallon = models.ForeignKey(

        Batallon,

        on_delete=models.CASCADE,

        related_name="companias"
    )

    nombre = models.CharField(
        max_length=200
    )

    codigo = models.CharField(

        max_length=20,

        unique=True,

        blank=True
    )

    descripcion = models.TextField(

        blank=True,

        null=True
    )

    activa = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================
    # GENERAR CÓDIGO AUTOMÁTICO
    # =====================================

    def save(self, *args, **kwargs):

        if not self.codigo:

            ultimo = Compania.objects.order_by(
                '-id'
            ).first()

            if ultimo:

                ultimo_numero = int(
                    ultimo.codigo.split('-')[1]
                )

                nuevo_numero = ultimo_numero + 1

            else:

                nuevo_numero = 1

            self.codigo = (
                f"CIA-{nuevo_numero:04d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.nombre} - "
            f"{self.batallon.nombre}"
        )


class PerfilPanel(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    configuracion = models.JSONField(default=dict)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='perfiles_creados'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class ConfiguracionUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='configuracion')
    configuracion = models.JSONField(default=dict)
    perfil_asignado = models.ForeignKey(
        PerfilPanel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_asignados'
    )

    def __str__(self):
        return f"Configuración de {self.usuario.username}"