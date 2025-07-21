
from rest_framework import viewsets, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *

from .serializers import *

from rest_framework.permissions import AllowAny

from core.permissions import IsAdminOrEmpleado, IsCliente, PermisosPorAccion

from rest_framework.decorators import api_view, permission_classes
from core.utils.recomendaciones import generar_recomendaciones

from core.utils.recomendaciones import generar_recomendaciones_por_cliente

import speech_recognition as sr
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ProductoFilter

class CustomPagination(PageNumberPagination):
    page_size = 7

User = get_user_model()

# Vista para obtener la lista de usuarios
class UserListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Asegura que solo los usuarios autenticados puedan ver
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Filtra los usuarios según el rol proporcionado en los parámetros de la URL.
        Si no se proporciona un parámetro de rol, se devuelven todos los usuarios.
        """
        queryset = User.objects.all()
        role = self.request.query_params.get('role', None)  # Obtener el parámetro 'role' de la URL
        if role:
            queryset = queryset.filter(role=role)  # Filtrar los usuarios por el rol
        return queryset

# Vista para obtener, actualizar o eliminar un usuario específico
class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Asegura que solo los usuarios autenticados puedan ver

# Vista para registrar un nuevo usuario
class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

# Vista para obtener el usuario actual (si estás usando JWT)
class CurrentUserAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

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

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = serializers.ModelSerializer  # o crea MarcaSerializer si quieres custom
    permission_classes = [AllowAny]

class TipoCategoriaViewSet(viewsets.ModelViewSet):
    queryset = TipoCategoria.objects.all()
    serializer_class = TipoCategoriaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    pagination_class = CustomPagination

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('-id')
    #serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        #if self.action == 'list' or self.action == 'retrieve':
        if self.action in ['list', 'retrieve']:
            return ProductoListSerializer
        return ProductoSerializer

class FotoViewSet(viewsets.ModelViewSet):
    queryset = Foto.objects.all()
    serializer_class = FotoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class AtributoViewSet(viewsets.ModelViewSet):
    queryset = Atributo.objects.all()
    serializer_class = AtributoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    
class ProductoAtributoViewSet(viewsets.ModelViewSet):
    queryset = ProductoAtributo.objects.all()
    serializer_class = ProductoAtributoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class DescuentoViewSet(viewsets.ModelViewSet):
    queryset = Descuento.objects.all()
    serializer_class = DescuentoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class ProductoDescuentoViewSet(viewsets.ModelViewSet):
    queryset = ProductoDescuento.objects.all()
    serializer_class = ProductoDescuentoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class CarritoMovilView(generics.ListAPIView):
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated, IsCliente]

    def get_queryset(self):
        return Carrito.objects.filter(cliente=self.request.user)

class CarritoView(APIView):
    queryset = Carrito.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carrito = Carrito.objects.filter(cliente=request.user)
        serializer = CarritoSerializer(carrito, many=True)
        return Response(serializer.data)

    def post(self, request):
        producto_id = request.data.get('producto_id')
        cantidad = request.data.get('cantidad', 1)

        try:
            producto = Producto.objects.get(id=producto_id)
            item, created = Carrito.objects.get_or_create(
                cliente=request.user, producto=producto,
                defaults={'cantidad': cantidad}
            )
            if not created:
                item.cantidad += int(cantidad)
                item.save()
            return Response({'message': 'Producto agregado al carrito.'}, status=status.HTTP_201_CREATED)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk=None):
        try:
            item = Carrito.objects.get(id=pk, cliente=request.user)
            cantidad = int(request.data.get('cantidad', 1))
            item.cantidad = cantidad
            item.save()
            return Response({'message': 'Cantidad actualizada.'}, status=status.HTTP_200_OK)
        except Carrito.DoesNotExist:
            return Response({'error': 'Item no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    
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

class CarritoDetalleViewSet(viewsets.ModelViewSet):
    queryset = CarritoDetalle.objects.all()
    serializer_class = CarritoDetalleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class PedidoDetalleViewSet(viewsets.ModelViewSet):
    queryset = PedidoDetalle.objects.all()
    serializer_class = PedidoDetalleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by('-fecha_hora')
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class ComprobanteViewSet(viewsets.ModelViewSet):
    queryset = Comprobante.objects.all()
    serializer_class = ComprobanteSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all().order_by('id')  # o el campo que prefieras
    serializer_class = SucursalSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class DevolucionViewSet(viewsets.ModelViewSet):
    queryset = Devolucion.objects.all()
    serializer_class = DevolucionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class DetalleDevolucionViewSet(viewsets.ModelViewSet):
    queryset = DetalleDevolucion.objects.all()
    serializer_class = DetalleDevolucionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

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
    #queryset = Producto.objects.select_related('categoria_id').prefetch_related('atributos').order_by('-id')  # Optimiza las relaciones
    #serializer_class = ProductoListSerializer
    serializer_class = ProductoListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductoFilter

    def get_queryset(self):
        orden_param = self.request.query_params.get('orden', 'desc')  # valor por defecto: descendente
        orden = '-id' if orden_param == 'desc' else 'id'

        return Producto.objects.select_related('categoria_id').prefetch_related('atributos').order_by(orden)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='CLIENTE')
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated, PermisosPorAccion]

class CarritoItemViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated, IsCliente]

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

class BitacoraViewSet(viewsets.ModelViewSet):
    queryset = Bitacora.objects.all()
    serializer_class = BitacoraSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]
    pagination_class = CustomPagination


"""class NotaDevolucionViewSet(viewsets.ModelViewSet):
    queryset = NotaDevolucion.objects.all()
    serializer_class = NotaDevolucionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class NotaSalidaViewSet(viewsets.ModelViewSet):
    queryset = NotaSalida.objects.all()
    serializer_class = NotaSalidaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

class DetalleSalidaViewSet(viewsets.ModelViewSet):
    queryset = DetalleSalida.objects.all()
    serializer_class = DetalleSalidaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]"""