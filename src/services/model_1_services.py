"""
model_1_services.py

Este módulo define la lógica para ejecutar el modelo de optimización energética utilizando `pulp`.
El modelo ahora es un modelo de programación lineal entera (PLE), donde el área de paneles solares
y la capacidad de la batería son variables enteras.
"""

import pulp
import numpy as np


def run_optimization(data):
    """
    Ejecuta el modelo de optimización energética basado en los datos proporcionados.

    Args:
        data (dict): Diccionario con los parámetros del modelo. Debe contener:
            - K (int): Número de días.
            - c1, c2, c3, c4 (float): Costos asociados al modelo.
            - gamma (float): Eficiencia de la batería.
            - r (float): Tasa máxima de carga/descarga de la batería.
            - X_max (float): Área máxima disponible para paneles solares.
            - generacion_solar (list[float]): Energía generada por m² (kWh/m²) diaria.
            - consumo_energia (list[float]): Energía consumida diariamente (kWh).

    Returns:
        dict: Resultados de la optimización con los valores óptimos de las variables.
            - Area_Panel_m2: Área óptima de paneles solares (entera).
            - Capacidad_Bateria_kWh: Capacidad óptima de la batería (entera).
            - Generacion_Solar_kWh_m2: Lista con la generación solar por día.
            - Consumo_Energetico_kWh: Lista con el consumo energético por día.
            - Estado_Carga_kWh: Lista con el estado de carga de la batería por día.
    """
    try:
        # Extraer parámetros del diccionario
        K = data['K']  # Número de días
        c1 = data['c1']  # Costo por m² de panel solar
        c2 = data['c2']  # Costo por kWh de batería
        c3 = data['c3']  # Costo por kWh de energía excedente
        c4 = data['c4']  # Costo por kWh de déficit energético
        gamma = data['gamma']  # Eficiencia de la batería
        r = data['r']  # Tasa máxima de carga/descarga
        X_max = data['X_max']  # Área máxima disponible para paneles solares

        # Generación de datos sintéticos de generación solar y consumo energético
        # Fijar semilla para reproducibilidad
        # np.random.seed(42)
        generacion_solar = np.random.uniform(
            2, 6, K)  # kWh/m² generados por día
        consumo_energia = np.random.uniform(5, 14, K)  # Consumo diario en kWh

        # Verificar dimensiones de listas
        if len(generacion_solar) != K or len(consumo_energia) != K:
            raise ValueError(
                "Las longitudes de 'generacion_solar' y 'consumo_energia' deben coincidir con 'K'.")

        # Crear modelo de optimización
        modelo = pulp.LpProblem("Optimizacion_Energetica", pulp.LpMinimize)

        # Variables de decisión
        # Área de paneles solares (entera)
        X1 = pulp.LpVariable("Area_Panel", lowBound=0,
                             upBound=X_max, cat='Integer')
        # Capacidad de la batería (entera)
        X2 = pulp.LpVariable("Capacidad_Bateria", lowBound=0, cat='Integer')
        # Estado de carga de la batería (continuo)
        X3 = [pulp.LpVariable(f"SoC_{k}", lowBound=0) for k in range(K)]
        # Energía excedente (continuo)
        exceso = [pulp.LpVariable(f"Exceso_{k}", lowBound=0) for k in range(K)]
        # Energía deficitaria (continuo)
        deficit = [pulp.LpVariable(
            f"Deficit_{k}", lowBound=0) for k in range(K)]

        # Definir función objetivo
        # Minimizamos el costo total compuesto por paneles solares, batería, excedentes y déficits
        costo_total = (
            c1 * X1 + c2 * X2 +
            pulp.lpSum([c3 * exceso[k] + c4 * deficit[k] for k in range(K)])
        )
        modelo += costo_total

        # Restricciones del modelo
        for k in range(K):
            if k == 0:
                # Restricción de balance energético inicial
                modelo += X3[k] == gamma * 0 + X1 * \
                    generacion_solar[k] - consumo_energia[k]
            else:
                # Restricción de balance energético para días subsiguientes
                modelo += X3[k] == gamma * X3[k-1] + X1 * \
                    generacion_solar[k] - consumo_energia[k]

            # Restricciones para exceso y déficit energético
            modelo += exceso[k] >= X3[k] - gamma * X2
            modelo += deficit[k] >= gamma * X2 - X3[k]

        for k in range(1, K):
            # Restricción de tasa máxima de carga
            modelo += X3[k] - X3[k-1] <= r * X2
            # Restricción de tasa máxima de descarga
            modelo += X3[k-1] - X3[k] <= r * X2

        # Restricción de cobertura energética
        modelo += X1 * sum(generacion_solar) >= sum(consumo_energia)

        for k in range(K):
            # Restricción de que el SoC no sea negativo
            modelo += X3[k] >= 0
            # Restricción de que el SoC no exceda la capacidad de la batería
            modelo += X3[k] <= X2

        # Resolver el modelo
        modelo.solve()

        # Verificar si se encontró una solución óptima
        if modelo.status != pulp.LpStatusOptimal:
            raise ValueError(
                "No se encontró una solución óptima para el modelo.")

        # Extraer valores óptimos de las variables
        X1_value = int(X1.varValue)  # Área óptima de panel solar (entera)
        X2_value = int(X2.varValue)  # Capacidad óptima de la batería (entera)
        # Estado de carga diario
        X3_values = [X3[k].varValue for k in range(K)]

        # Retornar resultados
        return {
            "Area_Panel_m2": X1_value,
            "Capacidad_Bateria_kWh": X2_value,
            "Generacion_Solar_kWh_m2": generacion_solar.tolist(),
            "Consumo_Energetico_kWh": consumo_energia.tolist(),
            "Estado_Carga_kWh": X3_values
        }

    except KeyError as e:
        # Capturar errores relacionados con claves faltantes
        raise KeyError(f"Clave faltante en los datos de entrada: {e}")
    except Exception as e:
        # Capturar cualquier otro error y volver a lanzarlo
        raise RuntimeError(f"Error al ejecutar el modelo: {str(e)}")
