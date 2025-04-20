from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AtributoViewSet, BitacoraViewSet, CategoriaViewSet, DescuentoViewSet, FacturaViewSet, InventarioViewSet, MetodoPagoViewSet, NotaDevolucionViewSet, NotaSalidaViewSet, ProductoViewSet, ClienteViewSet, CarritoItemViewSet, VentaViewSet, ClienteDashboardView, VerRecomendacionesView, CarritoMovilView, obtener_recomendaciones, recomendaciones_cliente_actual, ReconocimientoVozAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'carrito', CarritoItemViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'bitacoras', BitacoraViewSet)
router.register(r'descuentos', DescuentoViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'metodo-pagos', MetodoPagoViewSet)
router.register(r'nota-devoluciones', NotaDevolucionViewSet)
router.register(r'nota-salidas', NotaSalidaViewSet)
router.register(r'atributos', AtributoViewSet)
router.register(r'inventarios', InventarioViewSet)

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
