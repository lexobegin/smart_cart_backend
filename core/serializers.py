from rest_framework import serializers
from .models import Atributo, Bitacora, Categoria, Descuento, DetalleDevolucion, Factura, Inventario, MetodoPago, NotaDevolucion, Producto, ProductoAtributo, User, CarritoItem, Venta, DetalleVenta

from django.contrib.auth import get_user_model

User = get_user_model()

class ClienteRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
            role='CLIENTE'
        )
        return user

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    # Aquí no es necesario hacer cambios porque el modelo Cliente ya no se usa.
    class Meta:
        model = User  # Cambiamos de Cliente a User
        fields = ['id', 'username', 'email', 'role']  # Usamos los campos necesarios de User

class CarritoItemSerializer(serializers.ModelSerializer):
    # Cambiar la referencia de Cliente a User
    cliente = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='CLIENTE'))  # Asegurarse de filtrar por rol CLIENTE
    class Meta:
        model = CarritoItem
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario']

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)
    cliente = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='CLIENTE'))  # Asegurarse de que el cliente sea un usuario con rol CLIENTE

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'fecha', 'total', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        venta = Venta.objects.create(**validated_data)
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle_data)
        return venta

# serializacion Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']
        
# serializacion Bitacora
class BitacoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitacora
        fields = ['id', 'usuario_id', 'accion', 'fecha']
 
# serializacion Descuento       
class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = ['id', 'nombre', 'descripcion', 'porcentaje']
        
class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['id', 'fecha_emision', 'total', 'notaventa_id']
        
class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = ['id', 'tipo', 'descripcion']
        
class NotaDevolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaDevolucion
        fields = ['id', 'cliente', 'fecha']
        
class DetalleDevolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleDevolucion
        fields = ['id', 'producto', 'cantidad', 'devolucion']
        
class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = ['id', 'nombre']
        
class ProductoAtributoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    atributo = AtributoSerializer()

    class Meta:
        model = ProductoAtributo
        fields = ['id','producto', 'atributo', 'valor']
        
class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = ['id', 'cantidad', 'producto_id', 'fecha_ingreso', 'fecha_salida']
        
class NotaSalidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = ['id', 'fecha', 'motivo']
        
class DetalleSalidaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    atributo = AtributoSerializer()

    class Meta:
        model = ProductoAtributo
        fields = ['id','producto', 'atributo', 'cantidad']