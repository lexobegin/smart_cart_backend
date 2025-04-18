from rest_framework import serializers
from .models import Producto, User, CarritoItem, Venta, DetalleVenta

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
