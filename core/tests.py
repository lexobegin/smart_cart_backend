from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Producto, Venta, DetalleVenta
from decimal import Decimal

User = get_user_model()

class VentaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cliente1", email="cliente1@example.com", password="1234", role="CLIENTE")
        self.producto1 = Producto.objects.create(nombre="Mesa", precio=Decimal('100.00'), stock=10)
        self.producto2 = Producto.objects.create(nombre="Silla", precio=Decimal('50.00'), stock=20)

    def test_crear_venta(self):
        venta = Venta.objects.create(usuario=self.user, total=Decimal('150.00'))
        DetalleVenta.objects.create(venta=venta, producto=self.producto1, cantidad=1, precio_unitario=self.producto1.precio)
        DetalleVenta.objects.create(venta=venta, producto=self.producto2, cantidad=1, precio_unitario=self.producto2.precio)
        
        self.assertEqual(venta.detalles.count(), 2)
        self.assertEqual(venta.total, Decimal('150.00'))
