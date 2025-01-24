"""
model_3_services.py

Este módulo define la lógica para ejecutar la simulación de Monte Carlo para el ahorro energético.
"""

from flask import jsonify
import numpy as np
import pandas as pd

def run_monte_carlo_simulation(num_simulaciones, precio_energia_range, produccion_solar_range, consumo_energia_range, impuesto_mensual, region, area_vivienda, consumo_mensual):
    """
    Ejecuta la simulación de Monte Carlo para el ahorro energético basado en los datos proporcionados.

    Args:
        num_simulaciones (int): Número de simulaciones de Monte Carlo.
        precio_energia_range (tuple): Rango de precios por kWh de energía alterna (USD).
        produccion_solar_range (tuple): Rango de producción promedio diaria de energía solar (kWh).
        consumo_energia_range (tuple): Rango de consumo energético de la casa (kWh).
        impuesto_mensual (float): Impuesto total mensual de terceros (USD).
        region (str): Nombre de la región de la vivienda.
        area_vivienda (float): Área de la vivienda en m².
        consumo_mensual (float): Consumo mensual de la vivienda en kWh.

    Returns:
        dict: Resultados de la simulación con estadísticas descriptivas y datos de simulación para graficar.
    """
    # Inicializar listas para almacenar los resultados de ahorro
    ahorros_anuales = []
    precio_energia_simulacion = []
    produccion_solar_simulacion = []
    consumo_energia_simulacion = []
    inversiones_iniciales = []
    periodos_recuperacion = []
    rois = []
    vpns = []

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

        # Cálculos adicionales para las métricas solicitadas
        inversion_inicial = 1000  # Ejemplo: inversión inicial de un sistema solar
        periodo_recuperacion = inversion_inicial / ahorro_anual
        roi = (ahorro_anual * 100) / inversion_inicial
        vpn = ahorro_anual / (1 + 0.05) ** periodo_recuperacion  # Suponiendo una tasa de descuento del 5%

        # Almacenar los resultados de la simulación
        ahorros_anuales.append(ahorro_anual)
        precio_energia_simulacion.append(precio_energia)
        produccion_solar_simulacion.append(produccion_solar)
        consumo_energia_simulacion.append(consumo_energia)
        inversiones_iniciales.append(inversion_inicial)
        periodos_recuperacion.append(periodo_recuperacion)
        rois.append(roi)
        vpns.append(vpn)

    # Si las variables de simulación son listas, conviértelas a arrays de numpy:
    ahorros_anuales = np.array(ahorros_anuales)
    periodos_recuperacion = np.array(periodos_recuperacion)
    rois = np.array(rois)
    vpns = np.array(vpns)

    # Calcular las estadísticas
    ahorro_promedio = np.mean(ahorros_anuales)
    periodo_recuperacion_promedio = np.mean(periodos_recuperacion)
    roi_promedio = np.mean(rois)
    vpn_promedio = np.mean(vpns)
    probabilidad_vpn_positivo = np.sum(vpns > 0) / num_simulaciones * 100

    # Convertir los arrays de numpy a listas antes de devolverlos
    def convert_to_list(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Solo convertir si es un numpy.ndarray
        return obj  # Si ya es una lista, devolverla tal cual

    # Definir el orden de las claves en el response
    response_data = {
        "region": region,
        "area_vivienda": area_vivienda,
        "consumo_mensual": consumo_mensual,
        "vpn_promedio": vpn_promedio,
        "roi_promedio": roi_promedio,
        "probabilidad_vpn_positivo": probabilidad_vpn_positivo,
        "periodo_recuperacion_promedio": periodo_recuperacion_promedio,
        "inversion_promedio": np.mean(inversiones_iniciales),
        "produccion_anual_promedio": np.mean(produccion_solar_simulacion) * 365,
        #"distribucion_vpn": convert_to_list(vpns),
        #"distribucion_roi": convert_to_list(rois),
        #"distribucion_periodo_recuperacion": convert_to_list(periodos_recuperacion),
        #"distribucion_inversion_inicial": convert_to_list(inversiones_iniciales)
    }

    # Devolver solo el diccionario de datos
    return response_data
