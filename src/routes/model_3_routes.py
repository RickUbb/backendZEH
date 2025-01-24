"""
model_3_routes.py

Este módulo define las rutas para ejecutar la simulación de Monte Carlo para el ahorro energético
utilizando Flask. Implementa validaciones, manejo de errores y documenta cada paso del proceso.
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from src.services.model_3_services import run_monte_carlo_simulation
import logging

# Configurar logger para registrar errores y eventos importantes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear un blueprint para las rutas del modelo de simulación
monte_carlo = Blueprint('monte_carlo_blueprint', __name__)

@cross_origin  # Permitir solicitudes de orígenes cruzados
@monte_carlo.route('/', methods=['POST'])
def simulate():
    """
    Ruta POST para ejecutar la simulación de Monte Carlo para el ahorro energético.
    Espera un JSON con los siguientes parámetros:
        - num_simulaciones (int): Número de simulaciones de Monte Carlo.
        - precio_energia_range (tuple): Rango de precios por kWh de energía alterna (USD).
        - produccion_solar_range (tuple): Rango de producción promedio diaria de energía solar (kWh).
        - consumo_energia_range (tuple): Rango de consumo energético de la casa (kWh).
        - impuesto_mensual (float): Impuesto total mensual de terceros (USD).

    Returns:
        JSON:
            - status: "success" si la simulación se ejecuta correctamente.
            - results: Resultados de la simulación, incluyendo estadísticas descriptivas y datos de simulación.
            - status: "error" si ocurre un problema, con un mensaje descriptivo.

    Ejemplo de entrada JSON:
    {
        "num_simulaciones": 10000,
        "precio_energia_range": [0.05, 0.15],
        "produccion_solar_range": [3, 7],
        "consumo_energia_range": [10, 30],
        "impuesto_mensual": 5
    }
    """
    try:
        # Obtener datos JSON enviados en la solicitud
        data = request.get_json()

        # Validar que los datos JSON sean proporcionados
        if not data:
            logger.error("No se proporcionó un JSON válido en la solicitud.")
            return jsonify({"status": "error", "message": "Solicitud inválida. Asegúrate de enviar un JSON válido."}), 400

        # Registrar datos de entrada para auditoría (si es seguro hacerlo)
        logger.info(f"Datos recibidos: {data}")

        # Validación inicial de las claves necesarias
        required_keys = {"num_simulaciones", "precio_energia_range", "produccion_solar_range", "consumo_energia_range", "impuesto_mensual"}
        missing_keys = required_keys - data.keys()
        if missing_keys:
            logger.error(f"Faltan claves requeridas: {missing_keys}")
            return jsonify({"status": "error", "message": f"Faltan claves requeridas: {missing_keys}"}), 400

        # Validar tipos de datos básicos
        if not isinstance(data['num_simulaciones'], int) or data['num_simulaciones'] <= 0:
            logger.error("El valor de 'num_simulaciones' debe ser un entero positivo.")
            return jsonify({"status": "error", "message": "El valor de 'num_simulaciones' debe ser un entero positivo."}), 400

        if not all(isinstance(data[key], list) and len(data[key]) == 2 for key in ['precio_energia_range', 'produccion_solar_range', 'consumo_energia_range']):
            logger.error("Los rangos deben ser listas de dos elementos.")
            return jsonify({"status": "error", "message": "Los rangos deben ser listas de dos elementos."}), 400

        if not isinstance(data['impuesto_mensual'], (float, int)) or data['impuesto_mensual'] < 0:
            logger.error("El valor de 'impuesto_mensual' debe ser un número no negativo.")
            return jsonify({"status": "error", "message": "El valor de 'impuesto_mensual' debe ser un número no negativo."}), 400

        # Ejecutar la simulación de Monte Carlo
        results = run_monte_carlo_simulation(
            data['num_simulaciones'],
            tuple(data['precio_energia_range']),
            tuple(data['produccion_solar_range']),
            tuple(data['consumo_energia_range']),
            data['impuesto_mensual'],
            data['region'],
            data['area_vivienda'],
            data['consumo_mensual']
        )

        # Responder con los resultados
        logger.info("Simulación ejecutada exitosamente.")
        return jsonify({
            "status": "success",
            "results": results
        }), 200

    except KeyError as e:
        # Capturar errores relacionados con claves faltantes
        logger.error(f"Clave faltante: {str(e)}")
        return jsonify({"status": "error", "message": f"Clave faltante: {str(e)}"}), 400

    except ValueError as e:
        # Capturar errores relacionados con validaciones del modelo
        logger.error(f"Error de validación: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

    except Exception as e:
        # Capturar errores generales
        logger.error(f"Error inesperado: {str(e)}")
        return jsonify({"status": "error", "message": "Ocurrió un error inesperado. Por favor, intenta nuevamente."}), 500
