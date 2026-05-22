from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0015_nuevos_modelos_y_campos'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[],
            database_operations=[
                migrations.AddField(
                    model_name='perfil',
                    name='huella',
                    field=models.TextField(blank=True, null=True),
                ),
            ],
        ),
    ]
