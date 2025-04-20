
import json
import random
from django.utils import timezone
from core.models import User, MetodoPago, Descuento
from core.models import (
    Categoria, Producto, Atributo, ProductoAtributo, Inventario,
    Venta, DetalleVenta, Bitacora, NotaDevolucion, DetalleDevolucion
)
from pathlib import Path

def run():
    print("Iniciando carga de datos...")

    with open(Path(__file__).resolve().parent / 'smartcart_seed_data.json', encoding='utf-8') as f:
        data = json.load(f)

    # Categoría base
    categoria, _ = Categoria.objects.get_or_create(nombre='Smartphones', defaults={'descripcion': 'Teléfonos inteligentes'})

    # Crear atributos base
    atributos_def = ['Color', 'Almacenamiento', 'RAM', 'Procesador']
    atributos = {}
    for nombre in atributos_def:
        atributos[nombre], _ = Atributo.objects.get_or_create(nombre=nombre)

    # Métodos de pago
    metodo1, _ = MetodoPago.objects.get_or_create(tipo="Tarjeta de Crédito")
    metodo2, _ = MetodoPago.objects.get_or_create(tipo="PayPal")
    metodo3, _ = MetodoPago.objects.get_or_create(tipo="Transferencia Bancaria")
    metodos = [metodo1, metodo2, metodo3]

    # Descuentos
    desc1, _ = Descuento.objects.get_or_create(nombre="Black Friday", defaults={"descripcion": "Descuento especial", "porcentaje": 20})
    desc2, _ = Descuento.objects.get_or_create(nombre="Navidad", defaults={"descripcion": "Descuento navideño", "porcentaje": 15})
    descuentos = [desc1, desc2]

    # Crear usuarios CLIENTE
    print("Creando usuarios...")
    usuarios = []
    for cliente in data['clientes']:
        user = User.objects.create_user(
            username=cliente['username'],
            email=cliente['email'],
            password=cliente['password'],
            first_name=cliente['first_name'],
            last_name=cliente['last_name'],
            role='CLIENTE',
            metodo_pago=random.choice(metodos),
            descuento_id=random.choice(descuentos)
        )
        usuarios.append(user)

    # Crear productos y atributos
    print("Creando productos...")
    productos = []
    for p in data['productos']:
        producto = Producto.objects.create(
            nombre=p['nombre'],
            descripcion=p['descripcion'],
            precio=p['precio'],
            stock=p['stock'],
            categoria_id=categoria
        )
        for attr, valor in p['atributos'].items():
            ProductoAtributo.objects.create(
                producto=producto,
                atributo=atributos[attr],
                valor=valor
            )
        productos.append(producto)

    # Crear ventas
    print("Creando ventas y detalles...")
    ventas = []
    for v in data['ventas']:
        venta = Venta.objects.create(
            cliente=usuarios[v['cliente_id'] - 1],
            total=v['total']
        )
        ventas.append(venta)

    for dv in data['detalles_venta']:
        DetalleVenta.objects.create(
            venta=ventas[dv['venta_id'] - 1],
            producto=productos[dv['producto_idx']],
            cantidad=dv['cantidad'],
            precio_unitario=dv['precio_unitario']
        )

    # Inventario
    print("Creando inventario...")
    for i in data['inventarios']:
        Inventario.objects.create(
            producto_id=productos[i['producto_idx']],
            cantidad=i['cantidad'],
            fecha_vencimiento=i['fecha_vencimiento']
        )

    # Bitácora
    print("Creando bitácora...")
    for b in data['bitacoras']:
        Bitacora.objects.create(
            usuario_id=usuarios[b['usuario_id'] - 1],
            fecha=b['fecha'],
            accion=b['accion'],
            ip=b['ip']
        )

    # Notas y detalles de devolución
    print("Creando devoluciones...")
    devoluciones = []
    for nd in data['notas_devolucion']:
        devolucion = NotaDevolucion.objects.create(
            cliente=usuarios[nd['cliente_id'] - 1],
            fecha=nd['fecha']
        )
        devoluciones.append(devolucion)

    for dd in data['detalles_devolucion']:
        DetalleDevolucion.objects.create(
            devolucion=devoluciones[dd['devolucion_id'] - 1],
            producto=productos[dd['producto_idx']],
            cantidad=dd['cantidad'],
            cliente=usuarios[dd['cliente_id'] - 1]
        )

    print("✅ Datos cargados exitosamente.")
