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
    compania = models.ForeignKey( 'Compania', on_delete=models.SET_NULL, null=True, blank=True, related_name="usuarios")
    huella = models.TextField( blank=True, null=True )
    imagen_huella = models.ImageField( upload_to='huellas/', blank=True, null=True )
    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.user.email} ({self.rol})"


# =========================================
# CURSOS
# =========================================

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    instructor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
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
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="inscripciones")
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mis_cursos")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("curso", "estudiante")

    def __str__(self):
        return f"{self.estudiante.username} - {self.curso.nombre}"


class Tarea(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="tareas")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_entrega = models.DateField()
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.titulo


# =========================================
# EVALUACIONES MILITARES
# =========================================

class Evaluacion(models.Model):

    codigo = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    titulo = models.CharField(
        max_length=200
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    instructor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="evaluaciones_creadas"
    )

    compania = models.ForeignKey(
    'Compania',
    on_delete=models.CASCADE,
    related_name="evaluaciones"
    )

    fecha = models.DateField()

    puntaje_maximo = models.IntegerField(
        default=200
    )

    activa = models.BooleanField(
        default=True
    )

    creado_en = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================
    # GENERAR CÓDIGO AUTOMÁTICO
    # =====================================

    def save(self, *args, **kwargs):

        if not self.codigo:

            ultima = Evaluacion.objects.order_by(
                "-id"
            ).first()

            if ultima and ultima.codigo:

                numero = int(
                    ultima.codigo.split("-")[1]
                ) + 1

            else:

                numero = 1

            self.codigo = (
                f"EVA-{numero:04d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.codigo} - {self.titulo}"
        )
    
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


class Asistencia(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    presente = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.estudiante.username} - {self.fecha}"


class ArchivoCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="archivos")
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to="cursos/")
    subido_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Calificacion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.SET_NULL, null=True, blank=True)
    nota = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.username} - {self.nota}"


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


# =========================================
# SOLDADOS ASIGNADOS A EVALUACIÓN
# =========================================

class EvaluacionAsignada(models.Model):

    evaluacion = models.ForeignKey(
        'Evaluacion',
        on_delete=models.CASCADE,
        related_name="asignaciones"
    )

    soldado = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="evaluaciones_asignadas"
    )

    puntaje_actual = models.IntegerField(
        default=200
    )

    completada = models.BooleanField(
        default=False
    )

    fecha_asignacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "evaluacion",
            "soldado"
        )

    def __str__(self):

        return (
            f"{self.soldado.username} - "
            f"{self.evaluacion.codigo}"
        )

# =========================================
# ITEMS DE EVALUACIÓN
# =========================================

class ItemEvaluacion(models.Model):

    TIPOS = (
        ("suma", "Suma"),
        ("resta", "Resta"),
    )

    evaluacion = models.ForeignKey(

        Evaluacion,

        on_delete=models.CASCADE,

        related_name="items"
    )

    nombre = models.CharField(
        max_length=200
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    tipo = models.CharField(

        max_length=20,

        choices=TIPOS
    )

    puntaje = models.IntegerField()

    activo = models.BooleanField(
        default=True
    )

    creado_en = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        signo = (
            "+"
            if self.tipo == "suma"
            else "-"
        )

        return (
            f"{self.nombre} "
            f"({signo}{self.puntaje})"
        )
    
# =========================================
# RESULTADOS DE EVALUACIÓN
# =========================================

class ResultadoItem(models.Model):

    evaluacion = models.ForeignKey(

        Evaluacion,

        on_delete=models.CASCADE,

        related_name="resultados"
    )

    item = models.ForeignKey(

        ItemEvaluacion,

        on_delete=models.CASCADE
    )

    soldado = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="resultados_items"
    )

    instructor = models.ForeignKey(

        User,

        on_delete=models.SET_NULL,

        null=True,

        related_name="calificaciones_realizadas"
    )

    puntos_aplicados = models.IntegerField()

    observacion = models.TextField(

        blank=True,

        null=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (

            f"{self.soldado.username} - "

            f"{self.item.nombre}"
        )
    

# =========================================
# TEST
# =========================================

class Test(models.Model):

    codigo = models.CharField(

        max_length=20,

        unique=True,

        blank=True
    )

    titulo = models.CharField(
        max_length=200
    )

    descripcion = models.TextField(

        blank=True,

        null=True
    )

    instructor = models.ForeignKey(

        User,

        on_delete=models.SET_NULL,

        null=True,

        related_name="tests_creados"
    )

    compania = models.ForeignKey(

        'Compania',

        on_delete=models.CASCADE,

        related_name="tests"
    )

    # =====================================
    # CONFIGURACIÓN
    # =====================================

    puntaje_maximo = models.FloatField(
        default=100
    )

    nota_aprobacion = models.FloatField(
        default=60
    )

    # =====================================
    # FECHAS
    # =====================================

    fecha_inicio = models.DateTimeField()

    fecha_fin = models.DateTimeField()

    # =====================================
    # INTENTOS
    # =====================================

    max_intentos = models.IntegerField(
        default=1
    )

    # =====================================
    # TIEMPO LÍMITE
    # =====================================

    tiempo_limite = models.IntegerField(

        default=30,

        help_text="Minutos"
    )

    # =====================================
    # CONFIGURACIONES EXTRA
    # =====================================

    mostrar_resultado = models.BooleanField(
        default=True
    )

    preguntas_aleatorias = models.BooleanField(
        default=False
    )

    activa = models.BooleanField(
        default=True
    )

    creado_en = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================
    # GENERAR CÓDIGO
    # =====================================

    def save(self, *args, **kwargs):

        if not self.codigo:

            ultimo = Test.objects.order_by(
                "-id"
            ).first()

            if ultimo and ultimo.codigo:

                numero = int(

                    ultimo.codigo.split("-")[1]

                ) + 1

            else:

                numero = 1

            self.codigo = (
                f"TES-{numero:04d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.titulo
    

# =========================================
# PREGUNTAS TEST
# =========================================

class PreguntaTest(models.Model):

    test = models.ForeignKey(

        Test,

        on_delete=models.CASCADE,

        related_name="preguntas"
    )

    pregunta = models.TextField()

    orden = models.IntegerField(
        default=1
    )

    activa = models.BooleanField(
        default=True
    )

    creado_en = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.pregunta
    
# =========================================
# OPCIONES RESPUESTA
# =========================================

class OpcionRespuesta(models.Model):

    pregunta = models.ForeignKey(

        PreguntaTest,

        on_delete=models.CASCADE,

        related_name="opciones"
    )

    texto = models.CharField(
        max_length=300
    )

    es_correcta = models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.texto
    
# =========================================
# TEST ASIGNADO
# =========================================

class TestAsignado(models.Model):

    test = models.ForeignKey(

        Test,

        on_delete=models.CASCADE,

        related_name="asignaciones"
    )

    soldado = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="tests_asignados"
    )

    # =====================================
    # RESULTADO
    # =====================================

    nota = models.FloatField(
        default=0
    )

    aprobado = models.BooleanField(
        default=False
    )

    completado = models.BooleanField(
        default=False
    )

    # =====================================
    # INTENTOS
    # =====================================

    intentos_realizados = models.IntegerField(
        default=0
    )

    # =====================================
    # FECHAS
    # =====================================

    inicio_test = models.DateTimeField(

        null=True,

        blank=True
    )

    finalizacion_test = models.DateTimeField(

        null=True,

        blank=True
    )

    fecha_asignacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "test",
            "soldado"
        )

    def __str__(self):

        return (

            f"{self.soldado.username} - "

            f"{self.test.titulo}"
        )
    
# =========================================
# RESPUESTAS USUARIO
# =========================================

class RespuestaUsuario(models.Model):

    asignacion = models.ForeignKey(

        TestAsignado,

        on_delete=models.CASCADE,

        related_name="respuestas"
    )

    pregunta = models.ForeignKey(

        PreguntaTest,

        on_delete=models.CASCADE
    )

    opcion = models.ForeignKey(

        OpcionRespuesta,

        on_delete=models.CASCADE
    )

    es_correcta = models.BooleanField(
        default=False
    )

    respondido_en = models.DateTimeField(
        auto_now_add=True
    )
