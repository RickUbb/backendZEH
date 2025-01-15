"""
model_4_services.py

Este módulo define la lógica para realizar predicciones del consumo energético utilizando un modelo ARIMA.
Genera predicciones basadas en datos históricos de consumo, incluyendo un intervalo de confianza y un gráfico visual.
"""


import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import datetime
import random
import logging

# Configurar logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_prediction(data):
    """
    Ejecuta el modelo de predicción de consumo energético basado en los datos proporcionados.

    Args:
        data (dict): Parámetros del modelo.

    Returns:
        dict: Resultados de la predicción.
    """
    try:
        dias_historicos = data['dias_historicos']
        orden_arima = tuple(data['orden_arima'])
        intervalo_confianza = data['intervalo_confianza']

        # Generar datos históricos ficticios
        historico = []
        for i in range(dias_historicos):
            fecha = (datetime.datetime.now(
            ) - datetime.timedelta(days=dias_historicos - i)).strftime('%Y-%m-%d')
            electrodomesticos = {k: round(random.uniform(
                0.01, 2.5), 2) for k in data['electrodomesticos'].keys()}
            consumo_total = sum(electrodomesticos.values())
            historico.append(
                {"Fecha": fecha, "Consumo Total (kWh)": consumo_total, **electrodomesticos})

        consumo_energia = [entry["Consumo Total (kWh)"] for entry in historico]
        serie_temporal = pd.Series(consumo_energia)

        # Ajustar modelo ARIMA sin validación de estacionariedad
        modelo = ARIMA(serie_temporal, order=orden_arima)
        modelo_fit = modelo.fit()

        prediccion = modelo_fit.get_forecast(steps=1)
        prediccion_valor = prediccion.predicted_mean.iloc[0]
        intervalo = prediccion.conf_int(alpha=1 - intervalo_confianza).iloc[0]

        # Generar gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(serie_temporal, label='Consumo Real')
        plt.plot([len(serie_temporal)], [prediccion_valor],
                 marker='o', color='red', label='Predicción')
        plt.fill_between([len(serie_temporal)], intervalo[0],
                         intervalo[1], color='pink', alpha=0.3, label='Confianza')
        plt.legend()
        plt.title('Consumo Real vs Predicción')
        plt.xlabel('Días')
        plt.ylabel('Consumo (kWh)')
        plt.grid(True)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        imagen_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        # Corregir fecha de predicción para ser el día siguiente al último histórico
        ultima_fecha_historico = datetime.datetime.strptime(
            historico[-1]['Fecha'], '%Y-%m-%d')
        fecha_prediccion = (ultima_fecha_historico +
                            datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        resultados = {
            "historico": historico,
            "prediccion": {
                "fecha_prediccion": fecha_prediccion,
                "consumo_predicho": prediccion_valor,
                "intervalo_confianza": {"inferior": intervalo[0], "superior": intervalo[1]}
            }
        }

        return resultados

    except Exception as e:
        logger.error(f"Error en la predicción: {str(e)}")
        raise RuntimeError(f"Error inesperado: {str(e)}")
