from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0014_perfilpanel_configuracionusuario_perfil_asignado'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='imagen_huella',
            field=models.ImageField(blank=True, null=True, upload_to='huellas/'),
        ),
        migrations.CreateModel(
            name='EvaluacionAsignada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje_actual', models.IntegerField(default=200)),
                ('completada', models.BooleanField(default=False)),
                ('fecha_asignacion', models.DateTimeField(auto_now_add=True)),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignaciones', to='usuarios.evaluacion')),
                ('soldado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones_asignadas', to=settings.AUTH_USER_MODEL)),
            ],
            options={'unique_together': {('evaluacion', 'soldado')}},
        ),
        migrations.CreateModel(
            name='ItemEvaluacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('suma', 'Suma'), ('resta', 'Resta')], max_length=20)),
                ('puntaje', models.IntegerField()),
                ('activo', models.BooleanField(default=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='usuarios.evaluacion')),
            ],
        ),
        migrations.CreateModel(
            name='ResultadoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntos_aplicados', models.IntegerField()),
                ('observacion', models.TextField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultados', to='usuarios.evaluacion')),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='calificaciones_realizadas', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.itemevaluacion')),
                ('soldado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultados_items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=20, unique=True)),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('puntaje_maximo', models.FloatField(default=100)),
                ('nota_aprobacion', models.FloatField(default=60)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('max_intentos', models.IntegerField(default=1)),
                ('tiempo_limite', models.IntegerField(default=30, help_text='Minutos')),
                ('mostrar_resultado', models.BooleanField(default=True)),
                ('preguntas_aleatorias', models.BooleanField(default=False)),
                ('activa', models.BooleanField(default=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('compania', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='usuarios.compania')),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tests_creados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PreguntaTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.TextField()),
                ('orden', models.IntegerField(default=1)),
                ('activa', models.BooleanField(default=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preguntas', to='usuarios.test')),
            ],
        ),
        migrations.CreateModel(
            name='OpcionRespuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=300)),
                ('es_correcta', models.BooleanField(default=False)),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opciones', to='usuarios.preguntatest')),
            ],
        ),
        migrations.CreateModel(
            name='TestAsignado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.FloatField(default=0)),
                ('aprobado', models.BooleanField(default=False)),
                ('completado', models.BooleanField(default=False)),
                ('intentos_realizados', models.IntegerField(default=0)),
                ('inicio_test', models.DateTimeField(blank=True, null=True)),
                ('finalizacion_test', models.DateTimeField(blank=True, null=True)),
                ('fecha_asignacion', models.DateTimeField(auto_now_add=True)),
                ('soldado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests_asignados', to=settings.AUTH_USER_MODEL)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignaciones', to='usuarios.test')),
            ],
            options={'unique_together': {('test', 'soldado')}},
        ),
        migrations.CreateModel(
            name='RespuestaUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('es_correcta', models.BooleanField(default=False)),
                ('respondido_en', models.DateTimeField(auto_now_add=True)),
                ('asignacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='usuarios.testasignado')),
                ('opcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.opcionrespuesta')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.preguntatest')),
            ],
        ),
    ]
