from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterField(
                    model_name='archivocurso',
                    name='id',
                    field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                migrations.AlterField(
                    model_name='asistencia',
                    name='id',
                    field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                migrations.AlterField(
                    model_name='calificacion',
                    name='id',
                    field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                migrations.AlterField(
                    model_name='curso',
                    name='id',
                    field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                migrations.AlterField(
                    model_name='evaluacion',
                    name='id',
                    field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                migrations.AlterField(
                    model_name='inscripcion',
                    name='id',
                    field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                migrations.AlterField(
                    model_name='perfil',
                    name='id',
                    field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                migrations.AlterField(
                    model_name='tarea',
                    name='id',
                    field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
            ],
        ),
    ]
