from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import views
from .views import *

# Initialize router
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)  # Rutas CRUD completas
router.register(r'productos-readonly', ProductoReadOnlyViewSet, basename='producto-readonly')  # Solo lectura
router.register(r'fotos', FotoViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'sucursales', SucursalViewSet)
router.register(r'clientes', ClienteViewSet)
#router.register(r'carrito', CarritoView)
router.register(r'carrito-detalles', CarritoDetalleViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'pedido-detalles', PedidoDetalleViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'detalle-ventas', DetalleVentaViewSet)
router.register(r'tipo-categorias', TipoCategoriaViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'bitacoras', BitacoraViewSet)
router.register(r'descuentos', DescuentoViewSet)
router.register(r'producto-descuentos', ProductoDescuentoViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'comprobantes', ComprobanteViewSet)
router.register(r'metodo-pagos', MetodoPagoViewSet)
router.register(r'atributos', AtributoViewSet)
router.register(r'producto-atributos', ProductoAtributoViewSet)
router.register(r'inventarios', InventarioViewSet)
router.register(r'devoluciones', DevolucionViewSet)
router.register(r'detalle-devoluciones', DetalleDevolucionViewSet)

# Define URL patterns
urlpatterns = [
    # API routes
    path('', include(router.urls)),

    path('productos-list/', ProductoListAPIView.as_view(), name='producto-list'),

    # JWT Authentication routes
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/registro-cliente/', ClienteRegisterView.as_view(), name='registro_cliente'),
    path('auth/users/me/', CurrentUserView.as_view(), name='current_user'),

    # Client-specific routes
    path('cliente/dashboard/', ClienteDashboardView.as_view(), name='cliente-dashboard'),
    path('cliente/recomendaciones/', VerRecomendacionesView.as_view(), name='ver-recomendaciones'),
    path('cliente/carrito/', CarritoMovilView.as_view(), name='carrito-movil'),
    path('cli-carrito/', CarritoView.as_view(), name='carrito'),
    path('cli-carrito/<id>/cantidad/', CarritoView.as_view(), name='carrito-cantidad'),

    # Recommendation routes
    path('recomendaciones/', obtener_recomendaciones, name='recomendaciones'),
    path('cliente/recomendaciones/personalizadas/', recomendaciones_cliente_actual, name='recomendaciones-cliente'),

    # Voice recognition API
    path('reconocimiento-voz/', ReconocimientoVozAPIView.as_view(), name='reconocimiento-voz'),

    # Usuario
    path('users/', UserListAPIView.as_view(), name='user-list'),  # Listar todos los usuarios
    path('users/register/', UserRegisterAPIView.as_view(), name='user-register'),  # Registrar un usuario
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),  # Detalle, actualizar y eliminar usuario
    path('users/me/', CurrentUserAPIView.as_view(), name='current-user'),  # Obtener el usuario autenticado
]
