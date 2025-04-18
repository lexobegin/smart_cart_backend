from django.core.management import call_command
from core.models import Producto, Venta, CarritoItem, Cliente, DetalleVenta
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from decimal import Decimal

User = get_user_model()

# Limpiar la base de datos antes de cargar los datos
def limpiar_base_de_datos():
    # Esto eliminará todos los datos de la base de datos, pero mantendrá las tablas
    print("Limpiando base de datos...")
    call_command('flush', interactive=False)
    print("Base de datos limpiada.")

# Crear los datos de prueba
def cargar_datos_prueba():
    # 1. Crear productos si no existen
    p1, _ = Producto.objects.get_or_create(nombre="Mesa", defaults={"precio": 100, "stock": 10})
    p2, _ = Producto.objects.get_or_create(nombre="Silla", defaults={"precio": 50, "stock": 20})
    p3, _ = Producto.objects.get_or_create(nombre="Sofá", defaults={"precio": 200, "stock": 5})

    # 2. Crear cliente (modelo Cliente, no User)
    cliente, _ = Cliente.objects.get_or_create(nombre="Juan Pérez", correo="cliente1@example.com")

    # 3. Crear ventas con combinaciones (y total calculado)
    def crear_venta(cliente, productos_con_cantidad):
        total = sum(p.precio * c for p, c in productos_con_cantidad)
        venta = Venta.objects.create(cliente=cliente, total=total)
        for producto, cantidad in productos_con_cantidad:
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )
        return venta

    crear_venta(cliente, [(p1, 1), (p2, 1)])       # Mesa + Silla
    crear_venta(cliente, [(p1, 1), (p3, 1)])       # Mesa + Sofá
    crear_venta(cliente, [(p1, 1), (p2, 1), (p3, 1)])  # Mesa + Silla + Sofá

    # 4. Crear superusuario si no existe
    def crear_superusuario():
        try:
            superuser = User.objects.get(username="superAdmin")
            print("Superusuario ya existe.")
        except User.DoesNotExist:
            superuser = User.objects.create_superuser(
                username="superAdmin",
                email="superadmin@example.com",
                password="superAdmin12345"
            )
            print(f"Superusuario creado: {superuser.username}")
    
    crear_superusuario()
    print("Datos de prueba cargados correctamente.")

# Ejecutar la limpieza y la carga de datos
limpiar_base_de_datos()
cargar_datos_prueba()
