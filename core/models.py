
from django.contrib.auth.models import AbstractUser
from django.db import models

# Modelo User = Usuario
class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('EMPLEADO', 'Empleado'),
        ('CLIENTE', 'Cliente'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='ADMIN')
    
    def __str__(self):
        return f"{self.username} ({self.role})"

#Modelo Bitacora
class Bitacora(models.Model):
    fecha = models.DateField()
    accion = models.CharField(max_length=255, blank=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    # llave secundaria usuario
    usuario_id = models.IntegerField()  # Cambiado a IntegerField para almacenar el ID del usuario
    
    def __str__(self):
        return f"{self.id} - {self.fecha} - User #{self.usuario_id} "

# Modelo Marca
class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

# Modelo Tipo Categoria
class TipoCategoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Ej: "Smartphone", "Accesorio"

    def __str__(self):
        return self.nombre

# Modelo Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    tipo_categoria = models.ForeignKey(TipoCategoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre} - {self.descripcion} ({self.tipo_categoria})"
    
# Modelo Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_minimo = models.IntegerField(default=0)
    # llave secundaria categorias
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)  # Suponiendo que 1 es un ID válido de Categoria
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    def calcular_stock_actual(self):
        inventarios = self.inventario_set.all()
        entradas = inventarios.filter(tipo='entrada').aggregate(total=models.Sum('cantidad'))['total'] or 0
        salidas = inventarios.filter(tipo='salida').aggregate(total=models.Sum('cantidad'))['total'] or 0
        devoluciones = inventarios.filter(tipo='devolucion').aggregate(total=models.Sum('cantidad'))['total'] or 0
        ajustes = inventarios.filter(tipo='ajuste').aggregate(total=models.Sum('cantidad'))['total'] or 0
        return entradas + devoluciones + ajustes - salidas

# Modelo Foto
class Foto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='fotos')
    url_imagen = models.URLField()

    def __str__(self):
        return self.url_imagen

# Modelo Atributo
class Atributo(models.Model):
    nombre = models.CharField(max_length=255)
    productos = models.ManyToManyField(Producto,through='ProductoAtributo',related_name='atributos',blank=True)
    
    def __str__(self):
        return self.nombre

# Modelo intermedia Producto Atributo
class ProductoAtributo(models.Model):
    atributo = models.ForeignKey(Atributo, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    valor = models.CharField(max_length=255)  # atributo adicional en la tabla intermedia
    
    def __str__(self):
        return f'{self.atributo.nombre} - {self.producto.nombre}: {self.valor}'

# Modelo Metodo de Pago
class MetodoPago(models.Model):
    tipo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.tipo

# Modelo Descuento
class Descuento(models.Model):
    TIPO_CHOICES = [('porcentaje', 'Porcentaje'), ('fijo', 'Fijo')]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    productos = models.ManyToManyField(Producto, through='ProductoDescuento')

    def __str__(self):
        return self.nombre

# Modelo ProductoDescuento
class ProductoDescuento(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('producto', 'descuento')

# Modelo Carrito
class Carrito(models.Model):
    ESTADO_CHOICES = [('activo', 'Activo'), ('comprado', 'Comprado'), ('cancelado', 'Cancelado')]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'CLIENTE'})
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')

# Modelo CarritoDetalle
class CarritoDetalle(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

# Modelo Pedido
class Pedido(models.Model):
    ESTADO_CHOICES = [('pendiente', 'Pendiente'), ('enviado', 'Enviado'), ('entregado', 'Entregado'), ('cancelado', 'Cancelado')]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'CLIENTE'})
    fecha_pedido = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)
    direccion_envio = models.TextField()
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='pendiente')

# Modelo PedidoDetalle
class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

#Modelo Venta
class Venta(models.Model):
    fecha_hora = models.DateTimeField()
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas_como_cliente')
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas_como_empleado')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.username}"

# Modelo DetalleVenta
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Venta #{self.venta.id})"

# Modelo Factura
class Factura(models.Model):
    tipo = models.CharField(max_length=10)  # venta o pedido
    id_origen = models.IntegerField()
    fecha_emision = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    rfc_emisor = models.CharField(max_length=20)
    rfc_receptor = models.CharField(max_length=20)
    serie = models.CharField(max_length=10)
    folio = models.CharField(max_length=20)

    def __str__(self):
        return f"Factura #{self.fecha_emision.strftime('%Y-%m-%d')} "

# Modelo Comprobante
class Comprobante(models.Model):
    tipo = models.CharField(max_length=20)  # recibo o factura
    id_origen = models.IntegerField()
    fecha_emision = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

# Modelo Sucursal
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"

# Modelo Inventario
class Inventario(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
        ('devolucion', 'Devolución')
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField()
    motivo = models.TextField()

    class Meta:
        unique_together = ('producto', 'sucursal')  # evita duplicados

    def __str__(self):
        return f"{self.producto.nombre} - {self.sucursal.nombre} ({self.cantidad})"

# Modelo Devolucion
class Devolucion(models.Model):
    tipo = models.CharField(max_length=10)  # venta o pedido
    id_origen = models.IntegerField()
    fecha = models.DateTimeField()
    motivo = models.TextField()

# Modelo DetalleDevolucion
class DetalleDevolucion(models.Model):
    devolucion = models.ForeignKey(Devolucion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()