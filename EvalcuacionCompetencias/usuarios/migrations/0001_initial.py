from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='Batallon',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('nombre', models.CharField(max_length=150, unique=True)),
                        ('codigo', models.CharField(editable=False, max_length=20, unique=True)),
                        ('ciudad', models.CharField(max_length=100)),
                        ('descripcion', models.TextField(blank=True, null=True)),
                        ('activo', models.BooleanField(default=True)),
                        ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                        ('soldados', models.ManyToManyField(blank=True, related_name='batallones_soldado', to=settings.AUTH_USER_MODEL)),
                        ('cuadros', models.ManyToManyField(blank=True, related_name='batallones_cuadro', to=settings.AUTH_USER_MODEL)),
                    ],
                ),
                migrations.CreateModel(
                    name='Compania',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('nombre', models.CharField(max_length=200)),
                        ('codigo', models.CharField(blank=True, max_length=20, unique=True)),
                        ('descripcion', models.TextField(blank=True, null=True)),
                        ('activa', models.BooleanField(default=True)),
                        ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                        ('batallon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companias', to='usuarios.batallon')),
                    ],
                ),
                migrations.CreateModel(
                    name='Evaluacion',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('codigo', models.CharField(blank=True, max_length=20, unique=True)),
                        ('titulo', models.CharField(max_length=200)),
                        ('descripcion', models.TextField(blank=True, null=True)),
                        ('fecha', models.DateField()),
                        ('puntaje_maximo', models.IntegerField(default=200)),
                        ('activa', models.BooleanField(default=True)),
                        ('creado_en', models.DateTimeField(auto_now_add=True)),
                        ('compania', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='usuarios.compania')),
                        ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evaluaciones_creadas', to=settings.AUTH_USER_MODEL)),
                    ],
                ),
                migrations.CreateModel(
                    name='Perfil',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('rol', models.CharField(choices=[('admin', 'Administrador'), ('soldado', 'Soldado'), ('instructor', 'Instructor')], default='soldado', max_length=20)),
                        ('documento', models.CharField(db_index=True, max_length=20, unique=True)),
                        ('unidad', models.CharField(blank=True, max_length=100, null=True)),
                        ('grado', models.CharField(blank=True, max_length=50, null=True)),
                        ('estado', models.BooleanField(default=True)),
                        ('huella', models.TextField(blank=True, null=True)),
                        ('activo', models.BooleanField(default=True)),
                        ('batallon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='personal', to='usuarios.batallon')),
                        ('compania', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuarios', to='usuarios.compania')),
                        ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
                    ],
                ),
                migrations.CreateModel(
                    name='Curso',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('nombre', models.CharField(max_length=200)),
                        ('codigo', models.CharField(max_length=50, unique=True)),
                        ('descripcion', models.TextField(blank=True, null=True)),
                        ('fecha_inicio', models.DateField()),
                        ('fecha_fin', models.DateField()),
                        ('cupo_maximo', models.IntegerField(default=30)),
                        ('activo', models.BooleanField(default=True)),
                        ('creado_en', models.DateTimeField(auto_now_add=True)),
                        ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cursos_instructor', to=settings.AUTH_USER_MODEL)),
                    ],
                ),
                migrations.CreateModel(
                    name='Inscripcion',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('fecha_inscripcion', models.DateTimeField(auto_now_add=True)),
                        ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='usuarios.curso')),
                        ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mis_cursos', to=settings.AUTH_USER_MODEL)),
                    ],
                    options={'unique_together': {('curso', 'estudiante')}},
                ),
                migrations.CreateModel(
                    name='Tarea',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('titulo', models.CharField(max_length=200)),
                        ('descripcion', models.TextField(blank=True, null=True)),
                        ('fecha_entrega', models.DateField()),
                        ('porcentaje', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                        ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tareas', to='usuarios.curso')),
                    ],
                ),
                migrations.CreateModel(
                    name='Asistencia',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('fecha', models.DateField()),
                        ('presente', models.BooleanField(default=True)),
                        ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.curso')),
                        ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                    ],
                ),
                migrations.CreateModel(
                    name='ArchivoCurso',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('titulo', models.CharField(max_length=200)),
                        ('archivo', models.FileField(upload_to='cursos/')),
                        ('subido_en', models.DateTimeField(auto_now_add=True)),
                        ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archivos', to='usuarios.curso')),
                    ],
                ),
                migrations.CreateModel(
                    name='Calificacion',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('nota', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                        ('observaciones', models.TextField(blank=True, null=True)),
                        ('creado_en', models.DateTimeField(auto_now_add=True)),
                        ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.curso')),
                        ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                        ('tarea', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.tarea')),
                    ],
                ),
            ],
        ),
    ]
