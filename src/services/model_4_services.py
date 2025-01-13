"""
model_4_services.py

Este módulo define la lógica para ejecutar el modelo de predicción de consumo energético utilizando ARIMA.
"""

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def run_prediction(data):
    """
    Ejecuta el modelo de predicción de consumo energético basado en los datos proporcionados.

    Args:
        data (dict): Diccionario con los parámetros del modelo. Debe contener:
            - consumo_energia (list[float]): Energía consumida diariamente (kWh).

    Returns:
        dict: Resultados de la predicción con los valores predichos y el intervalo de confianza.
            - prediccion (float): Predicción del consumo total para el siguiente día.
            - intervalo_confianza (tuple): Intervalo de confianza al 95%.
    """
    try:
        # Extraer parámetros del diccionario
        consumo_energia = data['consumo_energia']

        # Validar que la lista de consumo energético no esté vacía
        if not consumo_energia:
            raise ValueError("La lista 'consumo_energia' no debe estar vacía.")

        # Crear serie temporal
        serie_temporal = pd.Series(consumo_energia)

        # Dividir los datos en entrenamiento (todos menos el último día) y prueba (último día)
        train = serie_temporal[:-1]
        test = serie_temporal[-1:]

        # Entrenar el modelo ARIMA
        modelo = ARIMA(train, order=(5, 1, 0))  # Orden (p,d,q) del modelo ARIMA
        modelo_ajustado = modelo.fit()

        # Realizar la predicción para el siguiente día
        prediccion = modelo_ajustado.get_forecast(steps=1)
        conf_int = prediccion.conf_int(alpha=0.05)  # Intervalo de confianza al 95%

        # Retornar resultados
        return {
            "prediccion": prediccion.predicted_mean.iloc[0],
            "intervalo_confianza": (conf_int.iloc[0, 0], conf_int.iloc[0, 1])
        }

    except KeyError as e:
        # Capturar errores relacionados con claves faltantes
        raise KeyError(f"Clave faltante en los datos de entrada: {e}")
    except Exception as e:
        # Capturar cualquier otro error y volver a lanzarlo
        raise RuntimeError(f"Error al ejecutar el modelo: {str(e)}")