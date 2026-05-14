import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EvalcuacionCompetencias.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import Perfil

# Datos de prueba
usuarios = [
    {'email': 'admin@ejercito.mil.co', 'password': 'admin123', 'rol': 'admin', 'documento': '1111111'},
    {'email': 'instructor@ejercito.mil.co', 'password': 'inst123', 'rol': 'instructor', 'documento': '2222222'},
    {'email': 'soldado@ejercito.mil.co', 'password': 'sold123', 'rol': 'soldado', 'documento': '3333333'},
]

for user_data in usuarios:
    email = user_data['email']
    try:
        user = User.objects.get(username=email)
        print(f'⚠️  Usuario {email} ya existe')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=user_data['password']
        )
        Perfil.objects.create(
            user=user,
            rol=user_data['rol'],
            documento=user_data['documento']
        )
        print(f'✓ Usuario {email} creado')

print('\n📋 Credenciales de acceso:')
print('=' * 50)
for user_data in usuarios:
    print(f"Email: {user_data['email']}")
    print(f"Contraseña: {user_data['password']}")
    print(f"Rol: {user_data['rol']}")
    print('-' * 50)
