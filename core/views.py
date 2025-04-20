
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    Atributo, ProductoAtributo, Inventario, NotaSalida, DetalleVenta, DetalleSalida, Producto, CarritoItem, Venta, Categoria, Bitacora, Descuento, Factura, MetodoPago, NotaDevolucion
)
from .serializers import (
    CategoriaSerializer, ProductoListSerializer, ProductoSerializer, ClienteSerializer, CarritoItemSerializer, VentaSerializer,
    BitacoraSerializer, DescuentoSerializer, FacturaSerializer, MetodoPagoSerializer, NotaDevolucionSerializer,
    AtributoSerializer, ProductoAtributoSerializer, InventarioSerializer, NotaSalidaSerializer,
    DetalleVentaSerializer, DetalleSalidaSerializer, ClienteRegisterSerializer
)
from rest_framework.permissions import AllowAny

from core.permissions import IsAdminOrEmpleado, IsCliente, PermisosPorAccion

from rest_framework.decorators import api_view, permission_classes
from core.utils.recomendaciones import generar_recomendaciones

from core.utils.recomendaciones import generar_recomendaciones_por_cliente

import speech_recognition as sr
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        })

class ClienteRegisterView(APIView):
    def post(self, request):
        serializer = ClienteRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario registrado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

class ProductoReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

#class ProductoListAPIView(generics.ListAPIView):
#    queryset = Producto.objects.all().select_related('categoria_id').prefetch_related('atributos')
#    serializer_class = ProductoListSerializer
#
#    def get_queryset(self):
#        #Aquí puedes filtrar productos por categoría o atributo si lo deseas.
#        queryset = Producto.objects.all().select_related('categoria_id').prefetch_related('atributos')
#
#        # Filtro opcional por nombre de atributo
#        atributo_nombre = self.request.query_params.get('atributo', None)
#        if atributo_nombre:
#            queryset = queryset.filter(atributos__nombre=atributo_nombre)
#
#        return queryset

#class ProductoListAPIView(generics.ListAPIView):
#    queryset = Producto.objects.all().select_related('categoria_id').prefetch_related(
#        'productoatributo_set__atributo'  # Relacionamos Producto con ProductoAtributo, y de ahí con Atributo
#    )
#    serializer_class = ProductoListSerializer
#
#    def get_queryset(self):
#        # Obtenemos el queryset base con las optimizaciones de consulta.
#        queryset = Producto.objects.all().select_related('categoria_id').prefetch_related(
#            'productoatributo_set__atributo'  # Relacionamos Producto con ProductoAtributo, y de ahí con Atributo
#        )
#        
#        # Filtro opcional por nombre de atributo
#        atributo_nombre = self.request.query_params.get('atributo', None)
#        if atributo_nombre:
#            queryset = queryset.filter(productoatributo__atributo__nombre=atributo_nombre)
#        
#        return queryset

class ProductoListAPIView(generics.ListAPIView):
    queryset = Producto.objects.all().prefetch_related('productoatributo_set__atributo')  # Optimiza las relaciones
    serializer_class = ProductoListSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='CLIENTE')
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated, PermisosPorAccion]

class CarritoItemViewSet(viewsets.ModelViewSet):
    queryset = CarritoItem.objects.all()
    serializer_class = CarritoItemSerializer
    permission_classes = [IsAuthenticated, IsCliente]

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class ClienteDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsCliente]

    def get(self, request):
        return Response({
            "mensaje": f"Hola {request.user.username}, bienvenido a la app móvil.",
            "acciones": ["ver_recomendaciones", "usar_voz", "comprar"]
        })

class VerRecomendacionesView(APIView):
    permission_classes = [IsAuthenticated, IsCliente]

    def get(self, request):
        # Por ahora es un placeholder. Luego se integrará con Apriori/ML.
        recomendaciones = [
            {"producto_id": 1, "nombre": "Auriculares Bluetooth"},
            {"producto_id": 2, "nombre": "Protector de Pantalla"},
        ]
        return Response({"recomendaciones": recomendaciones})
    
class CarritoMovilView(generics.ListAPIView):
    serializer_class = CarritoItemSerializer
    permission_classes = [IsAuthenticated, IsCliente]

    def get_queryset(self):
        return CarritoItem.objects.filter(cliente=self.request.user)

class CarritoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carrito = CarritoItem.objects.filter(cliente=request.user)
        serializer = CarritoItemSerializer(carrito, many=True)
        return Response(serializer.data)

    def post(self, request):
        producto_id = request.data.get('producto_id')
        cantidad = request.data.get('cantidad', 1)

        try:
            producto = Producto.objects.get(id=producto_id)
            item, created = CarritoItem.objects.get_or_create(
                cliente=request.user, producto=producto,
                defaults={'cantidad': cantidad}
            )
            if not created:
                item.cantidad += int(cantidad)
                item.save()
            return Response({'message': 'Producto agregado al carrito.'}, status=status.HTTP_201_CREATED)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_recomendaciones(request):
    recomendaciones = generar_recomendaciones()
    return Response(recomendaciones)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recomendaciones_cliente_actual(request):
    try:
        user = request.user
        cliente = User.objects.get(id=user.id, role='CLIENTE')
        recomendaciones = generar_recomendaciones_por_cliente(cliente)
        return Response(recomendaciones)
    except User.DoesNotExist:
        return Response({"error": "Cliente no encontrado"}, status=404)

class ReconocimientoVozAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'audio' not in request.FILES:
            return Response({"error": "No se envió ningún archivo de audio."}, status=status.HTTP_400_BAD_REQUEST)

        audio_file = request.FILES['audio']

        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
                texto = recognizer.recognize_google(audio, language='es-ES')  # Usa Google Web API (gratis, limitado)
                return Response({"transcripcion": texto})
        except sr.UnknownValueError:
            return Response({"error": "No se pudo entender el audio."}, status=status.HTTP_400_BAD_REQUEST)
        except sr.RequestError as e:
            return Response({"error": f"Error en el servicio de reconocimiento: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class BitacoraViewSet(viewsets.ModelViewSet):
    queryset = Bitacora.objects.all()
    serializer_class = BitacoraSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class DescuentoViewSet(viewsets.ModelViewSet):
    queryset = Descuento.objects.all()
    serializer_class = DescuentoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class NotaDevolucionViewSet(viewsets.ModelViewSet):
    queryset = NotaDevolucion.objects.all()
    serializer_class = NotaDevolucionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class AtributoViewSet(viewsets.ModelViewSet):
    queryset = Atributo.objects.all()
    serializer_class = AtributoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class ProductoAtributoViewSet(viewsets.ModelViewSet):
    queryset = ProductoAtributo.objects.all()
    serializer_class = ProductoAtributoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class NotaSalidaViewSet(viewsets.ModelViewSet):
    queryset = NotaSalida.objects.all()
    serializer_class = NotaSalidaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class DetalleSalidaViewSet(viewsets.ModelViewSet):
    queryset = DetalleSalida.objects.all()
    serializer_class = DetalleSalidaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]