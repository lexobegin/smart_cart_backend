import os
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from faker import Faker
from django.utils import timezone
from datetime import datetime, timedelta
from core.models import *

fake = Faker('es_ES')  # Configuración regional en español

class Command(BaseCommand):
    help = 'Poblar la base de datos con ventas, carritos, pedidos y métodos de pago.'
    
    def handle(self, *args, **options):
        self.stdout.write("Poblando base de datos con ventas, carritos, pedidos y métodos de pago...")
        
        # Crear en el orden correcto para respetar relaciones
        
        self.crear_metodos_pago()
        self.crear_carritos()
        self.crear_pedidos()
        self.crear_ventas()
        
        self.stdout.write(self.style.SUCCESS('¡Datos creados exitosamente!'))

    def crear_metodos_pago(self):
        if MetodoPago.objects.exists():
            self.stdout.write("Ya existen métodos de pago.")
            return

        metodos = [
            {"tipo": "Tarjeta de crédito", "descripcion": "Visa, Mastercard"},
            {"tipo": "Débito", "descripcion": "Tarjeta de débito bancaria"},
            {"tipo": "Efectivo", "descripcion": "Pago en efectivo"},
            {"tipo": "Transferencia", "descripcion": "Transferencia bancaria"},
            {"tipo": "PayPal", "descripcion": "Pago en línea vía PayPal"},
        ]
        for m in metodos:
            MetodoPago.objects.create(**m)

        self.stdout.write(f"Métodos de pago creados: {MetodoPago.objects.count()}")

    def crear_carritos(self):
        clientes = User.objects.filter(role='CLIENTE')
        productos = Producto.objects.filter(activo=True)

        for cliente in clientes[:50]:  # Crear hasta 50 carritos
            carrito = Carrito.objects.create(
                cliente=cliente,
                estado='activo'
            )
            for _ in range(random.randint(1, 5)):
                producto = random.choice(productos)
                cantidad = random.randint(1, 3)
                CarritoDetalle.objects.create(
                    carrito=carrito,
                    producto=producto,
                    cantidad=cantidad
                )

        self.stdout.write(f"Carritos creados: {Carrito.objects.count()}")
        self.stdout.write(f"Detalles de carritos creados: {CarritoDetalle.objects.count()}")

    def crear_pedidos(self):
        clientes = User.objects.filter(role='CLIENTE')
        metodos = list(MetodoPago.objects.all())
        productos = Producto.objects.all()

        for _ in range(50):  # Crear 50 pedidos
            cliente = random.choice(clientes)
            metodo_pago = random.choice(metodos)
            fecha_pedido = timezone.now() - timedelta(days=random.randint(0, 30))
            direccion = fake.address()
            estado = random.choice(['pendiente', 'enviado', 'entregado'])

            pedido = Pedido.objects.create(
                cliente=cliente,
                fecha_pedido=fecha_pedido,
                total=0,  # temporal
                metodo_pago=metodo_pago,
                direccion_envio=direccion,
                estado=estado
            )

            total = 0
            for _ in range(random.randint(1, 5)):
                producto = random.choice(productos)
                cantidad = random.randint(1, 3)
                precio = producto.precio
                PedidoDetalle.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio
                )
                total += cantidad * precio

            pedido.total = total
            pedido.save()

        self.stdout.write(f"Pedidos creados: {Pedido.objects.count()}")
        self.stdout.write(f"Detalles de pedidos creados: {PedidoDetalle.objects.count()}")

    def crear_ventas(self):
        clientes = User.objects.filter(role='CLIENTE')
        empleados = User.objects.filter(role='EMPLEADO')
        productos = Producto.objects.filter(activo=True)
        metodos = MetodoPago.objects.all()

        for _ in range(100):
            cliente = random.choice(clientes)
            empleado = random.choice(empleados)
            metodo_pago = random.choice(metodos)
            fecha_venta = timezone.now() - timedelta(days=random.randint(1, 30))
            
            venta = Venta.objects.create(
                fecha_hora=fecha_venta,
                cliente=cliente,
                empleado=empleado,
                metodo_pago=metodo_pago,
                total=0  # se actualizará
            )

            total = 0
            for _ in range(random.randint(1, 4)):
                producto = random.choice(productos)
                cantidad = random.randint(1, 3)
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )
                total += cantidad * producto.precio

            venta.total = total
            venta.save()

        self.stdout.write(f"Ventas creadas: {Venta.objects.count()}")
        self.stdout.write(f"Detalles de ventas creados: {DetalleVenta.objects.count()}")
