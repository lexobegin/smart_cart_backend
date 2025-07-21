import os
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from faker import Faker
from django.utils import timezone
from datetime import datetime
from core.models import *

fake = Faker('es_ES')  # Configuración regional en español

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos ficticios'
    
    def handle(self, *args, **options):
        self.stdout.write("Creando datos de prueba...")
        
        # Crear en el orden correcto para respetar relaciones
        self.crear_usuarios()
        self.crear_bitacoras()
        
        self.stdout.write(self.style.SUCCESS('¡Datos creados exitosamente!'))

    def crear_usuarios(self):
        # Crear administradores
        for i in range(1, 4):
            User.objects.create_superuser(
                username=f'admin{i}',
                email=f'admin{i}@tienda.com',
                password='admin123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_active=True,
                role='ADMIN'
            )
        
        # Crear empleados
        for i in range(1, 6):
            User.objects.create_user(
                username=f'empleado{i}',
                email=f'empleado{i}@tienda.com',
                password='empleado123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='EMPLEADO',
                is_active=True,
                is_staff=True
            )
        
        # Crear clientes (100)
        for i in range(1, 101):
            User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password='cliente123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='CLIENTE',
                is_active=True
            )
        self.stdout.write(f"Usuarios creados: {User.objects.count()}")

    def crear_bitacoras(self):
        usuarios = User.objects.all()
        acciones = [
            "Inicio de sesión",
            "Cierre de sesión",
            "Actualización de perfil",
            "Compra realizada",
            "Devolución solicitada",
            "Consulta de producto"
        ]
        
        for _ in range(50):  # 50 registros de bitácora
            # Generamos una fecha naive con Faker
            fecha_naive = fake.date_between(start_date='-1y', end_date='today')
        
            # Convertimos la fecha naive a una fecha aware
            fecha_aware = timezone.make_aware(datetime.combine(fecha_naive, datetime.min.time()))
        
            # Creamos el registro de inventario
            Bitacora.objects.create(
                usuario_id=random.choice(usuarios).id,
                fecha=fecha_aware,
                accion=random.choice(acciones),
                ip=fake.ipv4()
            )
        self.stdout.write(f"Registros de bitácora creados: {Bitacora.objects.count()}")
        