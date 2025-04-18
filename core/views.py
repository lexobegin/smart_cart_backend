
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Producto, User, CarritoItem, Venta
from .serializers import ProductoSerializer, ClienteSerializer, CarritoItemSerializer, VentaSerializer
from core.permissions import IsAdminOrEmpleado, IsCliente, PermisosPorAccion

from rest_framework.decorators import api_view, permission_classes
from core.utils.recomendaciones import generar_recomendaciones

from core.utils.recomendaciones import generar_recomendaciones_por_cliente

import speech_recognition as sr
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmpleado]

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