from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    """
    Finaliza la corrección del esquema de usuarios_evaluacion.
    Las columnas viejas (porcentaje, curso_id) ya fueron eliminadas y las nuevas
    ya fueron agregadas por una ejecución parcial de la migración anterior.
    Esta versión aplica solo lo que falta: corregir tipo BIGINT en compania_id
    y agregar los FK constraints y el índice único en codigo.
    """

    dependencies = [
        ('usuarios', '0016_add_perfil_huella_db'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Corregir compania_id de INT a BIGINT para que coincida con usuarios_compania.id
        migrations.RunSQL(
            sql="ALTER TABLE usuarios_evaluacion MODIFY COLUMN compania_id BIGINT NULL;",
            reverse_sql=migrations.RunSQL.noop,
        ),

        # Índice único en codigo
        migrations.RunSQL(
            sql="ALTER TABLE usuarios_evaluacion ADD UNIQUE INDEX usuarios_evaluacion_codigo_uniq (codigo);",
            reverse_sql="ALTER TABLE usuarios_evaluacion DROP INDEX usuarios_evaluacion_codigo_uniq;",
        ),

        # FK instructor_id → auth_user.id (INT)
        migrations.RunSQL(
            sql="""
                ALTER TABLE usuarios_evaluacion
                ADD CONSTRAINT fk_evaluacion_instructor
                    FOREIGN KEY (instructor_id) REFERENCES auth_user(id) ON DELETE SET NULL;
            """,
            reverse_sql="ALTER TABLE usuarios_evaluacion DROP FOREIGN KEY fk_evaluacion_instructor;",
        ),

        # FK compania_id → usuarios_compania.id (BIGINT)
        migrations.RunSQL(
            sql="""
                ALTER TABLE usuarios_evaluacion
                ADD CONSTRAINT fk_evaluacion_compania
                    FOREIGN KEY (compania_id) REFERENCES usuarios_compania(id) ON DELETE CASCADE;
            """,
            reverse_sql="ALTER TABLE usuarios_evaluacion DROP FOREIGN KEY fk_evaluacion_compania;",
        ),
    ]
