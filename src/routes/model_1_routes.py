"""
model_1_routes.py

Este módulo define las rutas para ejecutar el modelo de optimización energética
utilizando Flask. Implementa validaciones, manejo de errores y documenta cada paso del proceso.
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from src.services.model_1_services import run_optimization
import logging

# Configurar logger para registrar errores y eventos importantes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear un blueprint para las rutas del modelo de optimización
main = Blueprint('optimization_blueprint', __name__)


@cross_origin  # Permitir solicitudes de orígenes cruzados
@main.route('/', methods=['POST'])
def optimize():
    """
    Ruta POST para ejecutar el modelo de optimización energética.
    Espera un JSON con los siguientes parámetros:
        - K (int): Número de días de simulación.
        - c1, c2, c3, c4 (float): Costos asociados al modelo.
        - gamma (float): Eficiencia de la batería.
        - r (float): Tasa máxima de carga/descarga de la batería.
        - X_max (float): Área máxima disponible para paneles solares (m²).
        - generacion_solar (list[float]): Energía generada por m² (kWh/m²) diaria.
        - consumo_energia (list[float]): Energía consumida diariamente (kWh).

    Returns:
        JSON:
            - status: "success" si la optimización se ejecuta correctamente.
            - results: Resultados del modelo, incluyendo área de panel y capacidad de batería.
            - status: "error" si ocurre un problema, con un mensaje descriptivo.

    Ejemplo de entrada JSON:
    {
        "K": 30,
        "c1": 100,
        "c2": 500,
        "c3": 0.05,
        "c4": 0.25,
        "gamma": 0.90,
        "r": 0.2,
        "X_max": 20,
        "generacion_solar": [4.5, 5.0, 4.8, ...],
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
        required_keys = {"K", "c1", "c2", "c3", "c4", "gamma",
                         "r", "X_max", "generacion_solar", "consumo_energia"}
        missing_keys = required_keys - data.keys()
        if missing_keys:
            logger.error(f"Faltan claves requeridas: {missing_keys}")
            return jsonify({"status": "error", "message": f"Faltan claves requeridas: {missing_keys}"}), 400

        # Validar tipos de datos básicos
        if not isinstance(data['K'], int) or data['K'] <= 0:
            logger.error("El valor de 'K' debe ser un entero positivo.")
            return jsonify({"status": "error", "message": "El valor de 'K' debe ser un entero positivo."}), 400

        if not all(isinstance(data[key], (float, int)) and data[key] > 0 for key in ['c1', 'c2', 'c3', 'c4', 'gamma', 'r', 'X_max']):
            logger.error(
                "Todos los costos y parámetros deben ser números positivos.")
            return jsonify({"status": "error", "message": "Todos los costos y parámetros deben ser números positivos."}), 400

        if not isinstance(data['generacion_solar'], list) or not isinstance(data['consumo_energia'], list):
            logger.error(
                "'generacion_solar' y 'consumo_energia' deben ser listas de números.")
            return jsonify({"status": "error", "message": "'generacion_solar' y 'consumo_energia' deben ser listas de números."}), 400

        if len(data['generacion_solar']) != data['K'] or len(data['consumo_energia']) != data['K']:
            logger.error(
                "Las listas 'generacion_solar' y 'consumo_energia' deben tener longitud igual a 'K'.")
            return jsonify({"status": "error", "message": "Las listas 'generacion_solar' y 'consumo_energia' deben tener longitud igual a 'K'."}), 400

        # Ejecutar el modelo de optimización
        results = run_optimization(data)

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
