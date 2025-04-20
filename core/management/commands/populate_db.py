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
        self.crear_descuentos()
        self.crear_metodos_pago()
        self.crear_categorias()
        self.crear_usuarios()
        self.crear_productos()
        self.crear_atributos()
        self.crear_producto_atributos()
        self.crear_inventarios()
        self.crear_carritos()
        self.crear_ventas()
        #self.crear_detalles_venta()
        self.crear_facturas()
        self.crear_notas_devolucion()
        self.crear_detalles_devolucion()
        self.crear_notas_salida()
        self.crear_detalles_salida()
        self.crear_bitacoras()
        
        self.stdout.write(self.style.SUCCESS('¡Datos creados exitosamente!'))

    def crear_descuentos(self):
        descuentos = [
            {"nombre": "Descuento por temporada", "descripcion": "Aplicable en temporada baja", "porcentaje": 10.00},
            {"nombre": "Descuento membresía", "descripcion": "Para clientes premium", "porcentaje": 15.00},
            {"nombre": "Descuento volumen", "descripcion": "Compras mayores a $1000", "porcentaje": 5.00},
            {"nombre": "Descuento lanzamiento", "descripcion": "Para nuevos productos", "porcentaje": 7.50},
            {"nombre": "Descuento fidelidad", "descripcion": "Clientes recurrentes", "porcentaje": 12.00},
        ]
        
        for desc in descuentos:
            Descuento.objects.create(**desc)
        self.stdout.write(f"Descuentos creados: {Descuento.objects.count()}")

    def crear_metodos_pago(self):
        metodos = [
            {"tipo": "Tarjeta de crédito", "descripcion": "Visa, Mastercard, Amex"},
            {"tipo": "Tarjeta de débito", "descripcion": "Pago con tarjeta de débito"},
            {"tipo": "Efectivo", "descripcion": "Pago en efectivo en tienda"},
            {"tipo": "Transferencia bancaria", "descripcion": "Transferencia interbancaria"},
            {"tipo": "PayPal", "descripcion": "Pago a través de PayPal"},
        ]
        
        for metodo in metodos:
            MetodoPago.objects.create(**metodo)
        self.stdout.write(f"Métodos de pago creados: {MetodoPago.objects.count()}")

    def crear_categorias(self):
        categorias = [
            {"nombre": "Smartphones", "descripcion": "Teléfonos inteligentes de última generación"},
            {"nombre": "Teléfonos básicos", "descripcion": "Teléfonos con funciones básicas"},
            {"nombre": "Teléfonos empresariales", "descripcion": "Para uso corporativo"},
            {"nombre": "Teléfonos resistentes", "descripcion": "Resistentes a agua, polvo y golpes"},
            {"nombre": "Teléfonos plegables", "descripcion": "Pantallas plegables innovadoras"},
        ]
        
        for cat in categorias:
            Categoria.objects.create(**cat)
        self.stdout.write(f"Categorías creadas: {Categoria.objects.count()}")

    def crear_usuarios(self):
        # Crear administradores
        for i in range(1, 4):
            User.objects.create_superuser(
                username=f'admin{i}',
                email=f'admin{i}@tienda.com',
                password='admin123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
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
                is_staff=True,
                descuento_id=Descuento.objects.order_by('?').first(),
                metodo_pago=MetodoPago.objects.order_by('?').first()
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
                descuento_id=Descuento.objects.order_by('?').first(),
                metodo_pago=MetodoPago.objects.order_by('?').first()
            )
        self.stdout.write(f"Usuarios creados: {User.objects.count()}")

    def crear_productos(self):
        marcas = ['Samsung', 'Apple', 'Xiaomi', 'Huawei', 'Oppo', 'Motorola']
        modelos = ['Galaxy S', 'iPhone', 'Redmi Note', 'P series', 'Reno', 'Moto G']
        
        for _ in range(50):  # Crear 50 productos
            Producto.objects.create(
                nombre=f"{random.choice(marcas)} {random.choice(modelos)} {fake.random_int(min=8, max=20)}",
                descripcion=fake.text(max_nb_chars=200),
                precio=round(random.uniform(200, 2000)),  # Precio entre 200 y 2000
                stock=random.randint(0, 100),
                categoria_id=Categoria.objects.order_by('?').first()
            )
        self.stdout.write(f"Productos creados: {Producto.objects.count()}")

    def crear_atributos(self):
        atributos = [
            {"nombre": "Color"},
            {"nombre": "Capacidad"},
            {"nombre": "Procesador"},
            {"nombre": "RAM"},
            {"nombre": "Sistema Operativo"},
            {"nombre": "Resolución de pantalla"},
            {"nombre": "Tamaño de pantalla"},
            {"nombre": "Batería"},
            {"nombre": "Cámara principal"},
            {"nombre": "Cámara frontal"},
        ]
        
        for attr in atributos:
            Atributo.objects.create(**attr)
        self.stdout.write(f"Atributos creados: {Atributo.objects.count()}")

    def crear_producto_atributos(self):
        productos = Producto.objects.all()
        atributos = Atributo.objects.all()
        
        for producto in productos:
            for _ in range(random.randint(1, 5)):  # 1-5 atributos por producto
                atributo = random.choice(atributos)
                valor = self.generar_valor_atributo(atributo.nombre)
                
                ProductoAtributo.objects.create(
                    producto=producto,
                    atributo=atributo,
                    valor=valor
                )
        self.stdout.write(f"Relaciones producto-atributo creadas: {ProductoAtributo.objects.count()}")

    def generar_valor_atributo(self, nombre_atributo):
        if nombre_atributo == "Color":
            return fake.color_name()
        elif nombre_atributo == "Capacidad":
            return f"{random.choice([64, 128, 256, 512])}GB"
        elif nombre_atributo == "RAM":
            return f"{random.choice([4, 6, 8, 12])}GB"
        elif nombre_atributo == "Sistema Operativo":
            return random.choice(["Android", "iOS", "HarmonyOS"])
        elif nombre_atributo == "Resolución de pantalla":
            return f"{random.choice([1080, 1440, 2160])}x{random.choice([1920, 2560, 3840])}"
        elif nombre_atributo == "Tamaño de pantalla":
            return f"{round(random.uniform(5.0, 7.5), 1)}\""
        elif nombre_atributo == "Batería":
            return f"{random.randint(3000, 6000)} mAh"
        elif "Cámara" in nombre_atributo:
            return f"{random.choice([12, 48, 64, 108])}MP"
        else:
            return fake.word()

    def crear_inventarios(self):
        productos = Producto.objects.all()
        
        for producto in productos:
            # Generamos una fecha naive con Faker
            fecha_vencimiento_naive = fake.date_between(start_date='+1y', end_date='+3y')
        
            # Convertimos la fecha naive a una fecha aware
            fecha_vencimiento_aware = timezone.make_aware(datetime.combine(fecha_vencimiento_naive, datetime.min.time()))
        
            # Creamos el registro de inventario
            Inventario.objects.create(
                cantidad=random.randint(1, 100),
                fecha_vencimiento=fecha_vencimiento_aware,
                producto_id=producto
            )
        self.stdout.write(f"Registros de inventario creados: {Inventario.objects.count()}")

    def crear_carritos(self):
        clientes = User.objects.filter(role='CLIENTE')
        productos = Producto.objects.all()
        
        for cliente in clientes[:50]:  # 50 clientes con carritos
            for _ in range(random.randint(1, 5)):  # 1-5 items por carrito
                CarritoItem.objects.create(
                    cliente=cliente,
                    producto=random.choice(productos),
                    cantidad=random.randint(1, 3)
                )
        self.stdout.write(f"Items de carrito creados: {CarritoItem.objects.count()}")

    def crear_ventas(self):
        clientes = User.objects.filter(role='CLIENTE')
        
        for _ in range(100):  # 100 ventas
            cliente = random.choice(clientes)
            venta = Venta.objects.create(
                cliente=cliente,
                total=0  # Se actualizará con los detalles
            )
            
            # Crear detalles de venta
            productos = Producto.objects.order_by('?')[:random.randint(1, 5)]
            total = 0
            
            for producto in productos:
                cantidad = random.randint(1, 3)
                precio = producto.precio
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio
                )
                total += cantidad * precio
            
            # Actualizar total de la venta
            venta.total = total
            venta.save()
        self.stdout.write(f"Ventas creadas: {Venta.objects.count()}")

    def crear_facturas(self):
        ventas = Venta.objects.all()
        
        for venta in ventas:
            Factura.objects.create(
                notaventa_id=venta,
                total=venta.total
            )
        self.stdout.write(f"Facturas creadas: {Factura.objects.count()}")

    def crear_notas_devolucion(self):
        ventas = Venta.objects.all()
        
        for _ in range(50):  # 50 notas de devolución
            venta = random.choice(ventas)
            # Generamos una fecha naive con Faker
            fecha_naive = fake.date_between(start_date=venta.fecha.date(), end_date='today')
        
            # Convertimos la fecha naive a una fecha aware
            fecha_aware = timezone.make_aware(datetime.combine(fecha_naive, datetime.min.time()))
        
        # Creamos el registro de inventario
            NotaDevolucion.objects.create(
                cliente=venta.cliente,
                fecha=fecha_aware
            )
        self.stdout.write(f"Notas de devolución creadas: {NotaDevolucion.objects.count()}")

    def crear_detalles_devolucion(self):
        notas = NotaDevolucion.objects.all()
        ventas = {nota.cliente_id: nota for nota in notas}
        
        for venta in Venta.objects.filter(cliente__in=ventas.keys()):
            nota = ventas[venta.cliente_id]
            for detalle in venta.detalles.all()[:random.randint(1, 3)]:  # 1-3 productos devueltos
                DetalleDevolucion.objects.create(
                    devolucion=nota,
                    producto=detalle.producto,
                    cantidad=random.randint(1, detalle.cantidad),
                    cliente=venta.cliente
                )
        self.stdout.write(f"Detalles de devolución creados: {DetalleDevolucion.objects.count()}")

    def crear_notas_salida(self):
        motivos = [
            "Daño en transporte",
            "Error en pedido",
            "Devolución a proveedor",
            "Muestra para demostración",
            "Donación a caridad"
        ]
        
        for _ in range(50):  # 50 notas de salida
            NotaSalida.objects.create(
                motivo=random.choice(motivos)
            )
        self.stdout.write(f"Notas de salida creadas: {NotaSalida.objects.count()}")

    def crear_detalles_salida(self):
        notas = NotaSalida.objects.all()
        productos = Producto.objects.all()
        
        for nota in notas:
            for _ in range(random.randint(1, 5)):  # 1-5 productos por nota
                DetalleSalida.objects.create(
                    notasalida=nota,
                    producto=random.choice(productos),
                    cantidad=random.randint(1, 10)
                )
        self.stdout.write(f"Detalles de salida creados: {DetalleSalida.objects.count()}")

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
        