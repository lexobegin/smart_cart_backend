from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Serializador para el usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

# serializacion Bitacora
class BitacoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitacora
        fields = ['id', 'usuario_id', 'accion', 'fecha']

# Serializador para el registro de usuario
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )
        return user

# Serializador para obtener el token JWT (Si estás utilizando JWT)
class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

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

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre']

class TipoCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCategoria
        fields = ['id', 'nombre']

# serializacion Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    tipo_categoria = TipoCategoriaSerializer(read_only=True)
    tipo_categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoCategoria.objects.all(),
        source='tipo_categoria',
        write_only=True
    )

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'tipo_categoria', 'tipo_categoria_id']

class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foto
        fields = ['id', 'url_imagen']

"""class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(source='categoria_id')
    categoria_id_input = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria_id',
        write_only=True
    )
    atributos = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'categoria_id_input', 'atributos']

    def get_atributos(self, obj):
        atributos = ProductoAtributo.objects.filter(producto=obj)
        return ProductoAtributoSerializer(atributos, many=True).data
"""

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(source='categoria_id')
    categoria_id_input = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria_id',
        write_only=True
    )
    atributos = serializers.SerializerMethodField()
    marca = serializers.StringRelatedField()  # Muestra el nombre de la marca
    fotos = serializers.SerializerMethodField()  # Campo para las fotos

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 
            'categoria', 'categoria_id_input', 'atributos',
            'marca', 'fotos', 'activo', 'creado'
        ]

    def get_atributos(self, obj):
        atributos = ProductoAtributo.objects.filter(producto=obj)
        return ProductoAtributoSerializer(atributos, many=True).data

    def get_fotos(self, obj):
        fotos = obj.fotos.all()  # Accede a las fotos relacionadas
        return FotoSerializer(fotos, many=True).data

class ProductoAtributoSerializer(serializers.ModelSerializer):
    #producto = ProductoSerializer()
    #atributo = AtributoSerializer()
    atributo = serializers.CharField(source='atributo.nombre')  # Mostrar nombre del atributo

    class Meta:
        model = ProductoAtributo
        fields = ['atributo', 'valor']

class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = ['id', 'nombre']

class ProductoListSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(source='categoria_id')  # Relación con la categoría
    marca = serializers.StringRelatedField()
    fotos = FotoSerializer(many=True, read_only=True)
    atributos = serializers.SerializerMethodField()  # Relación con ProductoAtributo para acceder a Atributo
    # También podemos incluir atributos directamente como un ManyToMany, si es necesario.
    # atributos = AtributoSerializer(many=True, read_only=True)  # Si no quieres detalles adicionales de ProductoAtributo
    inventario = serializers.SerializerMethodField()
    stock_actual = serializers.SerializerMethodField()
    en_stock_minimo = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock_minimo', 'marca', 'categoria', 'activo', 'creado', 'fotos', 'atributos', 'inventario', 'stock_actual', 'en_stock_minimo']

    def get_atributos(self, obj):
        atributos = ProductoAtributo.objects.filter(producto=obj)
        return ProductoAtributoSerializer(atributos, many=True).data

    def get_inventario(self, obj):
        inventarios = Inventario.objects.filter(producto=obj)
        return InventarioSerializer(inventarios, many=True).data

    """def get_stock_actual(self, obj):
        inventarios = Inventario.objects.filter(producto=obj)
        entradas = inventarios.filter(tipo='entrada').aggregate(total=models.Sum('cantidad'))['total'] or 0
        salidas = inventarios.filter(tipo='salida').aggregate(total=models.Sum('cantidad'))['total'] or 0
        devoluciones = inventarios.filter(tipo='devolucion').aggregate(total=models.Sum('cantidad'))['total'] or 0
        ajustes = inventarios.filter(tipo='ajuste').aggregate(total=models.Sum('cantidad'))['total'] or 0
        return entradas + devoluciones + ajustes - salidas"""
    def get_stock_actual(self, obj):
        return obj.calcular_stock_actual()

    def get_en_stock_minimo(self, obj):
        stock = self.get_stock_actual(obj)
        return stock <= obj.stock_minimo

    """def get_atributos(self, obj):
        atributos = ProductoAtributo.objects.filter(producto=obj)
        return ProductoAtributoSerializer(atributos, many=True).data"""


class ClienteSerializer(serializers.ModelSerializer):
    # Aquí no es necesario hacer cambios porque el modelo Cliente ya no se usa.
    class Meta:
        model = User  # Cambiamos de Cliente a User
        fields = ['id', 'username', 'email', 'role']  # Usamos los campos necesarios de User


class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'

class ProductoDescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoDescuento
        fields = '__all__'

class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = '__all__'

class CarritoDetalleSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()

    class Meta:
        model = CarritoDetalle
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    # Cambiar la referencia de Cliente a User
    cliente = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='CLIENTE'))  # Asegurarse de filtrar por rol CLIENTE
    detalles = CarritoDetalleSerializer(source='carritodetalle_set', many=True, read_only=True)

    class Meta:
        model = Carrito
        fields = '__all__'

class PedidoDetalleSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()

    class Meta:
        model = PedidoDetalle
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    cliente = UserSerializer()
    metodo_pago = MetodoPagoSerializer()
    detalles = PedidoDetalleSerializer(source='pedidodetalle_set', many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'

#class CarritoItemSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = CarritoItem
#        exclude = ['cliente']  # <- opcional si querés ocultarlo en inputs, pero sigue en outputs

#Opcional
#class CarritoItemSerializer(serializers.ModelSerializer):
#    cliente = serializers.ReadOnlyField(source='cliente.id')
#
#    class Meta:
#        model = CarritoItem
#        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario']

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)
    metodo_pago = MetodoPagoSerializer()
    cliente = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='CLIENTE'))  # Asegurarse de que el cliente sea un usuario con rol CLIENTE
    empleado = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='EMPLEADO'))

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'empleado', 'fecha_hora', 'total', 'detalles', 'metodo_pago']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        metodo_pago_data = validated_data.pop('metodo_pago')

        metodo_pago = MetodoPago.objects.create(**metodo_pago_data)
        venta = Venta.objects.create(metodo_pago=metodo_pago, **validated_data)

        for detalle_data in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle_data)
        
        return venta

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'

class ComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprobante
        fields = '__all__'

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)

    class Meta:
        model = Inventario
        fields = '__all__'

# serializacion Descuento

class DetalleDevolucionSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()

    class Meta:
        model = DetalleDevolucion
        fields = '__all__'

class DevolucionSerializer(serializers.ModelSerializer):
    detalles = DetalleDevolucionSerializer(source='detalledevolucion_set', many=True, read_only=True)

    class Meta:
        model = Devolucion
        fields = '__all__'