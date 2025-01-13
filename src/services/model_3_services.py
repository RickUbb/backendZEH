"""
model_3_services.py

Este módulo define la lógica para ejecutar la simulación de Monte Carlo para el ahorro energético.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_monte_carlo_simulation(num_simulaciones, precio_energia_range, produccion_solar_range, consumo_energia_range, impuesto_mensual):
    """
    Ejecuta la simulación de Monte Carlo para el ahorro energético basado en los datos proporcionados.

    Args:
        num_simulaciones (int): Número de simulaciones de Monte Carlo.
        precio_energia_range (tuple): Rango de precios por kWh de energía alterna (USD).
        produccion_solar_range (tuple): Rango de producción promedio diaria de energía solar (kWh).
        consumo_energia_range (tuple): Rango de consumo energético de la casa (kWh).
        impuesto_mensual (float): Impuesto total mensual de terceros (USD).

    Returns:
        dict: Resultados de la simulación con estadísticas descriptivas y datos de simulación.
    """
    # Inicializar listas para almacenar los resultados de ahorro
    ahorros_anuales = []
    precio_energia_simulacion = []
    produccion_solar_simulacion = []
    consumo_energia_simulacion = []

    # Simulación de Monte Carlo
    for _ in range(num_simulaciones):
        # Generar valores aleatorios para las variables
        precio_energia = np.random.uniform(*precio_energia_range)
        produccion_solar = np.random.uniform(*produccion_solar_range)
        consumo_energia = np.random.uniform(*consumo_energia_range)

        # Calcular la energía consumida de la red
        energia_red = max(0, consumo_energia - produccion_solar)

        # Calcular el costo de la energía consumida de la red
        costo_energia_red = energia_red * precio_energia

        # Calcular el ahorro anual
        ahorro_anual = costo_energia_red * 365  # Ahorrar todos los días del año

        # Almacenar los resultados de la simulación
        ahorros_anuales.append(ahorro_anual)
        precio_energia_simulacion.append(precio_energia)
        produccion_solar_simulacion.append(produccion_solar)
        consumo_energia_simulacion.append(consumo_energia)

    # Convertir los resultados a un array de numpy para análisis
    ahorros_anuales = np.array(ahorros_anuales)
    precio_energia_simulacion = np.array(precio_energia_simulacion)
    produccion_solar_simulacion = np.array(produccion_solar_simulacion)
    consumo_energia_simulacion = np.array(consumo_energia_simulacion)

    # Calcular estadísticas
    ahorro_promedio = np.mean(ahorros_anuales)
    ahorro_minimo = np.min(ahorros_anuales)
    ahorro_maximo = np.max(ahorros_anuales)
    desviacion_estandar = np.std(ahorros_anuales)

    # Calcular el ahorro neto después de impuestos
    impuesto_anual = impuesto_mensual * 12
    ahorro_neto_anual = ahorros_anuales - impuesto_anual

    # Guardar los resultados de la simulación en un archivo CSV
    df_simulaciones = pd.DataFrame({
        'Precio_Energia_USD': precio_energia_simulacion,
        'Produccion_Solar_kWh': produccion_solar_simulacion,
        'Consumo_Energia_kWh': consumo_energia_simulacion,
        'Ahorro_Anual_USD': ahorros_anuales,
        'Ahorro_Neto_Anual_USD': ahorro_neto_anual
    })

    df_simulaciones.to_csv('simulaciones_ahorro_energetico.csv', index=False)

    # Retornar resultados
    return {
        "ahorro_promedio": ahorro_promedio,
        "ahorro_minimo": ahorro_minimo,
        "ahorro_maximo": ahorro_maximo,
        "desviacion_estandar": desviacion_estandar,
        "ahorro_neto_anual_promedio": np.mean(ahorro_neto_anual),
        "simulaciones": df_simulaciones.to_dict(orient='records')
    }