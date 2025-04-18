from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, ClienteViewSet, CarritoItemViewSet, VentaViewSet, ClienteDashboardView, VerRecomendacionesView, CarritoMovilView, obtener_recomendaciones, recomendaciones_cliente_actual, ReconocimientoVozAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'carrito', CarritoItemViewSet)
router.register(r'ventas', VentaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Rutas para autenticación JWT
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Cliente app movil
    path('cliente/dashboard/', ClienteDashboardView.as_view(), name='cliente-dashboard'),
    path('cliente/recomendaciones/', VerRecomendacionesView.as_view(), name='ver-recomendaciones'),
    path('cliente/carrito/', CarritoMovilView.as_view(), name='carrito-movil'),
    path('recomendaciones/', obtener_recomendaciones, name='recomendaciones'),
    path('cliente/recomendaciones/personalizadas/', recomendaciones_cliente_actual, name='recomendaciones-cliente'),
    path('api/reconocimiento-voz/', ReconocimientoVozAPIView.as_view(), name='reconocimiento-voz'),

]
