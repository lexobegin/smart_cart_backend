from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class IsEmpleado(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'EMPLEADO'

class IsCliente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'CLIENTE'
    
class AdminOrEmpleadoPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'EMPLEADO']
    
class IsAdminOrEmpleado(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'EMPLEADO']

class IsAdminOrRole(BasePermission):
    def __init__(self, role):
        self.allowed_role = role

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'ADMIN' or request.user.role == self.allowed_role
        )

class PermisosPorAccion(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        role = getattr(user, 'role', None)
        action = view.action  # 'list', 'retrieve', 'create', etc.

        # Reglas por rol
        if role == 'ADMIN':
            return True  # puede hacer todo

        if role == 'EMPLEADO':
            return action in ['list', 'retrieve', 'create']

        if role == 'CLIENTE':
            # Solo ver productos o su carrito, etc.
            return action in ['list', 'retrieve', 'create']

        return False