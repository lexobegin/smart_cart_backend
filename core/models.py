
from django.contrib.auth.models import AbstractUser
from django.db import models

# Modelo Descuento
class Descuento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)  
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre
    
# Modelo Metodo de Pago
class MetodoPago(models.Model):
    tipo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.tipo
   
# Modelo User = Usuario
class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('EMPLEADO', 'Empleado'),
        ('CLIENTE', 'Cliente'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='ADMIN')
    descuento_id = models.ForeignKey(Descuento, on_delete=models.CASCADE, blank=True, null=True)  # llave secundaria descuento
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE, blank=True, null=True)  # llave secundaria metodo
    
    def __str__(self):
        return f"{self.username} ({self.role})"
 
# Modelo Nota de Devolucion
class NotaDevolucion(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'CLIENTE'})
    fecha = models.DateField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id} - User #{self.usuario_id} - {self.fecha.strftime("%Y-%m-%d")} "

#Modelo Bitacora
class Bitacora(models.Model):
    fecha = models.DateField()
    accion = models.CharField(max_length=255, blank=True)
    ip = models.GenericIPAddressField(blank=True, null=True)  
    # llave secundaria usuario
    usuario_id = models.IntegerField()  # Cambiado a IntegerField para almacenar el ID del usuario
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.fecha} - User #{self.usuario_id} "

# Modelo Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)  
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.nombre} - {self.descripcion}"
    
# Modelo Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    # llave secundaria categorias
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)  # Suponiendo que 1 es un ID válido de Categoria

    def __str__(self):
        return self.nombre

#Este modelo Cliente ya no se ocupa, si hace referencia en otro archivo ese cliente hace referencia a User
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class CarritoItem(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'CLIENTE'})
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} ({self.cliente.username})'

#Modelo Venta
class Venta(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'CLIENTE'})
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.username}"

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
    fecha_emision = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    # llave secundaria nota venta
    notaventa_id = models.OneToOneField(Venta,on_delete=models.CASCADE)   
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Factura #{self.id} - {self.notaventa_id} - {self.fecha_emision.strftime('%Y-%m-%d')} "

# Modelo Intermedia Detalle Devolucion
class DetalleDevolucion(models.Model):
    devolucion = models.ForeignKey(NotaDevolucion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'CLIENTE'})
    
    def __str__(self):
        return f"{self.id} - (Devolucion #{self.devolucion.id})"
 
 # Modelo Atributo
class Atributo(models.Model):
    nombre = models.CharField(max_length=255) 
    productos = models.ManyToManyField(Producto,through='ProductoAtributo',related_name='atributos',blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

# Modelo intermedia Producto Atributo  
class ProductoAtributo(models.Model):
    atributo = models.ForeignKey(Atributo, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    valor = models.CharField(max_length=255)  # atributo adicional en la tabla intermedia
        
    def __str__(self):
        return f'{self.atributo.nombre} - {self.producto.nombre}: {self.valor}'

# Modelo Inventario
class Inventario(models.Model):
    cantidad = models.IntegerField(default=1)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField()
    producto_id = models.ForeignKey(Producto,on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.cantidad} - {self.fecha_ingreso.strftime('%Y-%m-%d')} - {self.fecha_vencimiento.strftime('%Y-%m-%d')} - {self.producto_id.nombre}"

# Modilo Nota Salida
class NotaSalida(models.Model):
    motivo = models.CharField(max_length=255) 
    fecha = models.DateField(auto_now_add=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.id + self.fecha.strftime('%Y-%m-%d') + " - " + self.motivo
    
class DetalleSalida(models.Model):
    notasalida = models.ForeignKey(NotaSalida, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)  # atributo adicional en la tabla intermedia
        
    def __str__(self):
        return f'{self.id} - {self.notasalida.fecha} - {self.producto.nombre}: {self.cantidad}'
