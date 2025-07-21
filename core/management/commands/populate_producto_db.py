"""import os
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
        self.crear_categorias()
        self.crear_productos()
        self.crear_atributos()
        self.crear_producto_atributos()
        
        self.stdout.write(self.style.SUCCESS('¡Datos creados exitosamente!'))

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
"""

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
        self.crear_marcas()
        self.crear_tipos_categoria()
        self.crear_categorias()
        self.crear_productos()
        self.crear_fotos()
        self.crear_atributos()
        self.crear_producto_atributos()
        self.crear_descuentos()
        self.crear_sucursales()
        self.crear_inventario()
        
        self.stdout.write(self.style.SUCCESS('¡Datos creados exitosamente!'))

    def crear_marcas(self):
        marcas = [
            "Samsung", "Apple", "Xiaomi", "Huawei", "Oppo",
            "Motorola", "OnePlus", "Google", "Sony", "Nokia"
        ]
        
        for nombre in marcas:
            Marca.objects.create(nombre=nombre)
        self.stdout.write(f"Marcas creadas: {Marca.objects.count()}")

    def crear_tipos_categoria(self):
        tipos = [
            {"nombre": "Smartphone"},
            {"nombre": "Tablet"},
            {"nombre": "Accesorio"},
            {"nombre": "Wearable"},
            {"nombre": "Audio"},
        ]
        
        for tipo in tipos:
            TipoCategoria.objects.create(**tipo)
        self.stdout.write(f"Tipos de categoría creados: {TipoCategoria.objects.count()}")

    def crear_categorias(self):
        categorias = [
            {"nombre": "Smartphones", "descripcion": "Teléfonos inteligentes de última generación", "tipo_categoria": TipoCategoria.objects.get(nombre="Smartphone")},
            {"nombre": "Teléfonos básicos", "descripcion": "Teléfonos con funciones básicas", "tipo_categoria": TipoCategoria.objects.get(nombre="Smartphone")},
            {"nombre": "Tablets Android", "descripcion": "Tablets con sistema operativo Android", "tipo_categoria": TipoCategoria.objects.get(nombre="Tablet")},
            {"nombre": "Tablets iOS", "descripcion": "Tablets de Apple", "tipo_categoria": TipoCategoria.objects.get(nombre="Tablet")},
            {"nombre": "Fundas", "descripcion": "Fundas y protectores", "tipo_categoria": TipoCategoria.objects.get(nombre="Accesorio")},
            {"nombre": "Cargadores", "descripcion": "Cargadores y cables", "tipo_categoria": TipoCategoria.objects.get(nombre="Accesorio")},
            {"nombre": "Smartwatches", "descripcion": "Relojes inteligentes", "tipo_categoria": TipoCategoria.objects.get(nombre="Wearable")},
            {"nombre": "Auriculares", "descripcion": "Auriculares inalámbricos y con cable", "tipo_categoria": TipoCategoria.objects.get(nombre="Audio")},
        ]
        
        for cat in categorias:
            Categoria.objects.create(**cat)
        self.stdout.write(f"Categorías creadas: {Categoria.objects.count()}")

    def crear_productos(self):
        modelos = {
            'Samsung': ['Galaxy S', 'Galaxy Note', 'Galaxy A', 'Galaxy Z', 'Galaxy M'],
            'Apple': ['iPhone', 'iPad', 'MacBook', 'Apple Watch', 'AirPods'],
            'Xiaomi': ['Redmi Note', 'Mi', 'Poco', 'Black Shark', 'Mi Band'],
            'Huawei': ['P series', 'Mate', 'Nova', 'Enjoy', 'MatePad'],
            'Oppo': ['Reno', 'Find X', 'A series', 'K series', 'F series'],
            'Motorola': ['Moto G', 'Moto E', 'Moto Z', 'Razr', 'Edge'],
            'OnePlus': ['OnePlus', 'Nord'],
            'Google': ['Pixel', 'Nest'],
            'Sony': ['Xperia', 'WH', 'WF'],
            'Nokia': ['G series', 'X series', 'C series']
        }
        
        for _ in range(50):  # Crear 50 productos
            marca = Marca.objects.order_by('?').first()
            modelo_base = random.choice(modelos[marca.nombre])
            
            Producto.objects.create(
                nombre=f"{marca.nombre} {modelo_base} {fake.random_int(min=8, max=20)}",
                descripcion=fake.text(max_nb_chars=200),
                precio=round(random.uniform(200, 2000)),  # Precio entre 200 y 2000
                marca=marca,
                categoria_id=Categoria.objects.order_by('?').first(),
                #categoria=Categoria.objects.order_by('?').first(),
                activo=random.choice([True, False])  # Algunos productos inactivos
            )
        self.stdout.write(f"Productos creados: {Producto.objects.count()}")

    """def crear_fotos(self):
        base_url = "https://example.com/images/"  # URL base ficticia para las imágenes
        productos = Producto.objects.all()
        
        for producto in productos:
            num_fotos = random.randint(1, 3)  # 1-3 fotos por producto
            for i in range(num_fotos):
                Foto.objects.create(
                    producto=producto,
                    url_imagen=f"{base_url}{producto.id}_{i}.jpg"
                )
        self.stdout.write(f"Fotos creadas: {Foto.objects.count()}")"""

    def crear_fotos(self):
        # Diccionario de imágenes por tipo de categoría
        imagenes_por_tipo = {
            "Smartphone": [
                "https://crazystore.com.bo/wp-content/uploads/2025/07/Sin-titulo-3-pixel-8a-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/07/image-aa50-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/05/iphone-13-green-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2024/10/iphone-13-pro-max-gold-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/07/S23-negro-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/SAMSUNG-GALAXY-S24-PLUS-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/04/Motorola-Edge-Plus-Cosmos-Blue-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/07/pixel-8-pro-bay-2.jpg",
            ],
            "Tablet": [
                "https://crazystore.com.bo/wp-content/uploads/2025/01/oneplus-pad-green-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/KINDLE-SCRIB-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/KINDLE-OCEAN-EXPLORER-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/oneplus-pad-2-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/04/Apple-iPad-Mini-7-Space-Gray-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/05/surface-pro-7-1.jpg",
            ],
            "Accesorio": [
                "https://crazystore.com.bo/wp-content/uploads/2024/10/c-to-jack-adapter-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/05/ATT-USB-C-to-Lightning-Braided-Cable-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/base-1-1-1-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2024/12/Blink-Video-Doorbell_0000_Capa-1-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/05/soporte-negro-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/EVGA-X12-MOUSE-1.jpg",
            ],
            "Wearable": [
                "https://crazystore.com.bo/wp-content/uploads/2025/06/image-ec12-1-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/wf-xm5-pink-2-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/image-b0a1-1-1-1-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/image-f3c2-1-1-1-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/07/sony-linkbuds-s-azul-1-1-1.jpg",
            ],
            "Audio": [
                "https://crazystore.com.bo/wp-content/uploads/2025/06/Beats-Flex-1-1-1-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/Beats-Solo-4-color-negro-y-dorado-1-1-1-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2022/08/plantilla-para-caratula-web-Recovered-2-1-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/hitune-max5-beige-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/AUDIFONO-AKG-1-1-1-1.jpg",
                "https://crazystore.com.bo/wp-content/uploads/2025/06/wh-1000xm5-blanco-1-1.jpg",
            ],
        }

        productos = Producto.objects.all()

        for producto in productos:
            tipo_categoria = producto.categoria_id.tipo_categoria.nombre

            imagenes_disponibles = imagenes_por_tipo.get(tipo_categoria)

            if imagenes_disponibles:
                num_fotos = random.randint(1, 3)
                imagenes_seleccionadas = random.sample(imagenes_disponibles, num_fotos)

                for url in imagenes_seleccionadas:
                    Foto.objects.create(producto=producto, url_imagen=url)

        self.stdout.write(f"Fotos reales creadas: {Foto.objects.count()}")

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
            {"nombre": "Peso"},
            {"nombre": "Material"},
            {"nombre": "Conectividad"},
            {"nombre": "Garantía"},
        ]
        
        for attr in atributos:
            Atributo.objects.create(**attr)
        self.stdout.write(f"Atributos creadas: {Atributo.objects.count()}")

    def generar_valor_atributo(self, nombre_atributo):
        if nombre_atributo == "Color":
            return fake.color_name()
        elif nombre_atributo == "Capacidad":
            return f"{random.choice([64, 128, 256, 512])}GB"
        elif nombre_atributo == "RAM":
            return f"{random.choice([4, 6, 8, 12])}GB"
        elif nombre_atributo == "Sistema Operativo":
            return random.choice(["Android", "iOS", "HarmonyOS", "Windows", "Tizen"])
        elif nombre_atributo == "Resolución de pantalla":
            return f"{random.choice([1080, 1440, 2160])}x{random.choice([1920, 2560, 3840])}"
        elif nombre_atributo == "Tamaño de pantalla":
            return f"{round(random.uniform(5.0, 12.9), 1)}\""
        elif nombre_atributo == "Batería":
            return f"{random.randint(3000, 10000)} mAh"
        elif "Cámara" in nombre_atributo:
            return f"{random.choice([12, 48, 64, 108])}MP"
        elif nombre_atributo == "Peso":
            return f"{random.randint(100, 500)} g"
        elif nombre_atributo == "Material":
            return random.choice(["Plástico", "Vidrio", "Metal", "Cerámica", "Cuero"])
        elif nombre_atributo == "Conectividad":
            return random.choice(["Bluetooth 5.0", "WiFi 6", "5G", "4G LTE", "NFC"])
        elif nombre_atributo == "Garantía":
            return f"{random.choice([1, 2])} año(s)"
        else:
            return fake.word()

    def crear_producto_atributos(self):
        productos = Producto.objects.all()
        atributos = Atributo.objects.all()
        
        for producto in productos:
            # Seleccionar entre 3 y 7 atributos aleatorios por producto
            atributos_seleccionados = random.sample(list(atributos), random.randint(3, 7))
            
            for atributo in atributos_seleccionados:
                valor = self.generar_valor_atributo(atributo.nombre)
                
                ProductoAtributo.objects.create(
                    producto=producto,
                    atributo=atributo,
                    valor=valor
                )
        self.stdout.write(f"Relaciones producto-atributo creadas: {ProductoAtributo.objects.count()}")
    
    def crear_descuentos(self):
        tipos = ['porcentaje', 'fijo']
        for i in range(10):
            descuento = Descuento.objects.create(
                nombre=f"Descuento {i+1}",
                tipo=random.choice(tipos),
                valor=random.randint(5, 30),
                activo=True,
                fecha_inicio=timezone.now(),
                fecha_fin=timezone.now() + timezone.timedelta(days=random.randint(10, 60))
            )
            # Asignar productos al descuento
            productos = Producto.objects.order_by('?')[:random.randint(1, 5)]
            for producto in productos:
                ProductoDescuento.objects.create(producto=producto, descuento=descuento)

        self.stdout.write(f"Descuentos creados: {Descuento.objects.count()}")
    
    def crear_sucursales(self):
        nombres = ["Sucursal Central", "Sucursal Norte", "Sucursal Sur"]
        for nombre in nombres:
            Sucursal.objects.create(nombre=nombre, ubicacion=fake.address())
        self.stdout.write(f"Sucursales creadas: {Sucursal.objects.count()}")

    def crear_inventario(self):
        sucursales = list(Sucursal.objects.all())
        productos = Producto.objects.all()

        for producto in productos:
            for sucursal in random.sample(sucursales, k=random.randint(1, len(sucursales))):
                Inventario.objects.update_or_create(
                    producto=producto,
                    sucursal=sucursal,
                    defaults={
                        'tipo': random.choice(['entrada', 'ajuste']),
                        'cantidad': random.randint(5, 50),
                        'fecha': timezone.now(),
                        'motivo': 'Carga inicial de inventario'
                    }
                )
        self.stdout.write(f"Inventario registrado para productos: {Inventario.objects.count()}")


