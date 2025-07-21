import os
import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from datetime import timedelta
from core.models import *

fake = Faker('es_ES')  # Configuración regional en español

class Command(BaseCommand):
    help = 'Pobla facturas, comprobantes y devoluciones con datos de prueba.'
    
    def handle(self, *args, **options):
        self.stdout.write("Poblando facturas, comprobantes y devoluciones...")
        
        self.crear_facturas()
        self.crear_comprobantes()
        self.crear_devoluciones()
        
        self.stdout.write(self.style.SUCCESS('¡Datos creados exitosamente!'))

    def crear_facturas(self):
        ventas = Venta.objects.all()
        pedidos = Pedido.objects.all()
        count = 0

        for venta in ventas:
            Factura.objects.create(
                tipo='venta',
                id_origen=venta.id,
                total=venta.total,
                rfc_emisor=fake.bothify(text='???######'),
                rfc_receptor=fake.bothify(text='???######'),
                serie=fake.random_uppercase_letter(),
                folio=str(venta.id)
            )
            count += 1

        for pedido in pedidos:
            Factura.objects.create(
                tipo='pedido',
                id_origen=pedido.id,
                total=pedido.total,
                rfc_emisor=fake.bothify(text='???######'),
                rfc_receptor=fake.bothify(text='???######'),
                serie=fake.random_uppercase_letter(),
                folio=str(pedido.id)
            )
            count += 1

        self.stdout.write(f"Facturas creadas: {count}")

    def crear_comprobantes(self):
        ventas = Venta.objects.all()
        pedidos = Pedido.objects.all()
        count = 0

        for venta in ventas[:50]:
            Comprobante.objects.create(
                tipo='factura',
                id_origen=venta.id,
                fecha_emision=venta.fecha_hora,
                total=venta.total,
                observaciones=fake.sentence()
            )
            count += 1

        for pedido in pedidos[:50]:
            Comprobante.objects.create(
                tipo='recibo',
                id_origen=pedido.id,
                fecha_emision=pedido.fecha_pedido,
                total=pedido.total,
                observaciones=fake.sentence()
            )
            count += 1

        self.stdout.write(f"Comprobantes creados: {count}")

    def crear_devoluciones(self):
        ventas = list(Venta.objects.all())
        pedidos = list(Pedido.objects.all())
        productos = list(Producto.objects.all())
        total_devoluciones = 0
        total_detalles = 0

        for _ in range(30):  # Devoluciones sobre ventas
            venta = random.choice(ventas)
            devolucion = Devolucion.objects.create(
                tipo='venta',
                id_origen=venta.id,
                fecha=venta.fecha_hora + timedelta(days=random.randint(1, 10)),
                motivo=fake.sentence()
            )
            for detalle in venta.detalles.all()[:random.randint(1, 3)]:
                DetalleDevolucion.objects.create(
                    devolucion=devolucion,
                    producto=detalle.producto,
                    cantidad=random.randint(1, detalle.cantidad)
                )
                total_detalles += 1
            total_devoluciones += 1

        for _ in range(30):  # Devoluciones sobre pedidos
            pedido = random.choice(pedidos)
            devolucion = Devolucion.objects.create(
                tipo='pedido',
                id_origen=pedido.id,
                fecha=pedido.fecha_pedido + timedelta(days=random.randint(1, 10)),
                motivo=fake.sentence()
            )
            for detalle in pedido.pedidodetalle_set.all()[:random.randint(1, 3)]:
                DetalleDevolucion.objects.create(
                    devolucion=devolucion,
                    producto=detalle.producto,
                    cantidad=random.randint(1, detalle.cantidad)
                )
                total_detalles += 1
            total_devoluciones += 1

        self.stdout.write(f"Devoluciones creadas: {total_devoluciones}")
        self.stdout.write(f"Detalles de devolución creados: {total_detalles}")