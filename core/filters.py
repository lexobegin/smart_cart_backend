# core/filters.py
import django_filters
from .models import Producto

#//Filtra por nombre de producto y por id categoria
#class ProductoFilter(django_filters.FilterSet):
#    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains')
#    categoria_id = django_filters.NumberFilter(field_name='categoria_id')
#
#    class Meta:
#        model = Producto
#        fields = ['nombre', 'categoria_id']

"""class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    categoria_id = django_filters.NumberFilter(field_name='categoria_id')

    atributo = django_filters.CharFilter(method='filtrar_por_atributo')
    valor = django_filters.CharFilter(method='filtrar_por_valor')

    class Meta:
        model = Producto
        fields = ['nombre', 'categoria_id']

    #def filtrar_por_atributo(self, queryset, name, value):
    #    return queryset.filter(atributos__atributo__nombre__icontains=value)

    #def filtrar_por_valor(self, queryset, name, value):
    #    return queryset.filter(atributos__valor__icontains=value)
    def filtrar_por_atributo(self, queryset, name, value):
        valor = self.data.get('valor', None)
        if valor:
            return queryset.filter(
                productoatributo__atributo__nombre__icontains=value,
                productoatributo__valor__icontains=valor
            )
        return queryset

    def filtrar_por_valor(self, queryset, name, value):
        atributo = self.data.get('atributo', None)
        if atributo:
            return queryset.filter(
                productoatributo__atributo__nombre__icontains=atributo,
                productoatributo__valor__icontains=value
            )
        return queryset"""

class ProductoFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    categoria = django_filters.CharFilter(field_name='categoria_id__nombre', lookup_expr='icontains')
    marca = django_filters.CharFilter(field_name='marca__nombre', lookup_expr='icontains')
    en_stock_minimo = django_filters.BooleanFilter(method='filtrar_stock_minimo')

    class Meta:
        model = Producto
        fields = ['precio_min', 'precio_max', 'categoria', 'marca', 'activo']

    def filtrar_stock_minimo(self, queryset, name, value):
        if value:
            return [p for p in queryset if p.stock_minimo >= p.inventario_actual()]
        return queryset