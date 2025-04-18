import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from core.models import Venta, CarritoItem

def generar_recomendaciones(min_support=0.01, min_confidence=0.3):
    # Obtener todas las ventas
    ventas = Venta.objects.all()

    # Diccionario para almacenar productos por venta
    transacciones = []

    for venta in ventas:
        items = CarritoItem.objects.filter(venta=venta).values_list('producto__nombre', flat=True)
        transacciones.append(list(items))

    # Crear un DataFrame tipo one-hot encoding
    all_productos = sorted(set(prod for trans in transacciones for prod in trans))
    df = pd.DataFrame([{prod: (prod in trans) for prod in all_productos} for trans in transacciones])

    # Aplicar Apriori
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    reglas = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

    # Retornar recomendaciones en formato usable
    recomendaciones = []
    for _, row in reglas.iterrows():
        recomendaciones.append({
            "si_compras": list(row['antecedents']),
            "tambien_agrega": list(row['consequents']),
            "confianza": round(row['confidence'], 2)
        })

    return recomendaciones

def generar_recomendaciones_por_cliente(cliente, min_support=0.01, min_confidence=0.3):
    from core.models import Venta, DetalleVenta

    # Ventas del cliente
    ventas = Venta.objects.filter(cliente=cliente)

    # Recolectar productos por venta
    transacciones = []
    for venta in ventas:
        items = DetalleVenta.objects.filter(venta=venta).values_list('producto__nombre', flat=True)
        transacciones.append(list(items))

    if not transacciones:
        return []  # No hay historial para este cliente

    # One-hot encoding
    all_productos = sorted(set(prod for trans in transacciones for prod in trans))
    df = pd.DataFrame([{prod: (prod in trans) for prod in all_productos} for trans in transacciones])

    # Apriori
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    reglas = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

    recomendaciones = []
    for _, row in reglas.iterrows():
        recomendaciones.append({
            "si_compras": list(row['antecedents']),
            "tambien_agrega": list(row['consequents']),
            "confianza": round(row['confidence'], 2)
        })

    return recomendaciones

