# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from core.models import Producto, Venta, CarritoItem, Cliente, DetalleVenta
from django.db.utils import IntegrityError
from decimal import Decimal

User = get_user_model()

# Crear o recuperar usuario ADMIN si no existe
admin_user, admin_created = User.objects.get_or_create(
    username="admin",
    defaults={
        "email": "admin@example.com",
        "is_active": True,
        "is_staff": True,  # Rol de ADMIN
        "is_superuser": True,  # Rol de ADMIN
        "role": "ADMIN",  # Especificamos el rol ADMIN
    }
)
if admin_created:
    admin_user.set_password("admin123")  # Establecer contraseña
    admin_user.save()
    print("Usuario ADMIN creado")

# Crear o recuperar usuario CLIENTE con el rol CLIENTE
cliente_user, cliente_created = User.objects.get_or_create(
    username="cliente1",
    defaults={
        "email": "cliente1@example.com",
        "is_active": True,
        "role": "CLIENTE",  # Especificamos el rol CLIENTE
    }
)
if cliente_created:
    cliente_user.set_password("cliente123")  # Establecer contraseña
    cliente_user.save()
    print("Usuario CLIENTE creado")


# Crear productos si no existen
p1, _ = Producto.objects.get_or_create(nombre="Mesa", defaults={"precio": Decimal("100.00"), "stock": 10})
p2, _ = Producto.objects.get_or_create(nombre="Silla", defaults={"precio": Decimal("50.00"), "stock": 20})
p3, _ = Producto.objects.get_or_create(nombre="Sofa", defaults={"precio": Decimal("200.00"), "stock": 5})

# Función para crear venta y detalles
def crear_venta(cliente_user, productos_con_cantidad):
    total = sum(p.precio * c for p, c in productos_con_cantidad)
    venta = Venta.objects.create(cliente=cliente_user, total=total)
    for producto, cantidad in productos_con_cantidad:
        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )
    return venta

# Crear ventas de prueba
crear_venta(cliente_user, [(p1, 1), (p2, 1)])  # Mesa + Silla
crear_venta(cliente_user, [(p1, 1), (p3, 1)])  # Mesa + Sofa
crear_venta(cliente_user, [(p1, 1), (p2, 1), (p3, 1)])  # Mesa + Silla + Sofa

print("Datos de prueba cargados correctamente.")
