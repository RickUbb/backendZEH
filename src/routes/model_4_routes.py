"""
model_4_routes.py

Este módulo define las rutas para ejecutar el modelo de predicción de consumo energético
utilizando Flask. Implementa validaciones, manejo de errores y documenta cada paso del proceso.
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from src.services.model_4_services import run_prediction
import logging

# Configurar logger para registrar errores y eventos importantes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear un blueprint para las rutas del modelo de predicción
main = Blueprint('prediction_blueprint', __name__)

@cross_origin  # Permitir solicitudes de orígenes cruzados
@main.route('/', methods=['POST'])
def predict():
    """
    Ruta POST para ejecutar el modelo de predicción de consumo energético.
    Espera un JSON con los siguientes parámetros:
        - consumo_energia (list[float]): Energía consumida diariamente (kWh).

    Returns:
        JSON:
            - status: "success" si la predicción se ejecuta correctamente.
            - results: Resultados del modelo, incluyendo la predicción y el intervalo de confianza.
            - status: "error" si ocurre un problema, con un mensaje descriptivo.

    Ejemplo de entrada JSON:
    {
        "consumo_energia": [5.5, 6.0, 7.2, ...]
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
        required_keys = {"consumo_energia"}
        missing_keys = required_keys - data.keys()
        if missing_keys:
            logger.error(f"Faltan claves requeridas: {missing_keys}")
            return jsonify({"status": "error", "message": f"Faltan claves requeridas: {missing_keys}"}), 400

        # Validar tipos de datos básicos
        if not isinstance(data['consumo_energia'], list):
            logger.error("'consumo_energia' debe ser una lista de números.")
            return jsonify({"status": "error", "message": "'consumo_energia' debe ser una lista de números."}), 400

        # Validar que la lista de consumo energético no esté vacía
        if not data['consumo_energia']:
            logger.error("La lista 'consumo_energia' no debe estar vacía.")
            return jsonify({"status": "error", "message": "La lista 'consumo_energia' no debe estar vacía."}), 400

        # Ejecutar el modelo de predicción
        results = run_prediction(data)

        # Responder con los resultados
        logger.info("Modelo ejecutado exitosamente.")
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