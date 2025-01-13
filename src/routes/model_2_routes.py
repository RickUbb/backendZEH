"""
SolarPanelRoutes.py

Este módulo define las rutas para optimizar la energía solar generada
utilizando Flask. Implementa validaciones, manejo de errores y documenta cada paso del proceso.
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from src.services.model_2_services import optimize_solar_energy
import logging

# Configurar logger para registrar errores y eventos importantes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear un blueprint para las rutas del modelo de optimización solar
solar = Blueprint('solar_blueprint', __name__)


@cross_origin  # Permitir solicitudes de orígenes cruzados
@solar.route('/', methods=['POST'])
def optimize():
    """
    Ruta POST para calcular y optimizar la energía generada por un panel solar.
    Espera un JSON con los siguientes parámetros:
        - A (float): Área del panel solar (m²).
        - eta (float): Eficiencia del panel (%).
        - I_promedio (float): Radiación solar promedio diaria (kWh/m²).
        - horas_sol (int): Duración del día (horas).

    Returns:
        JSON:
            - status: "success" si el cálculo se ejecuta correctamente.
            - results: Resultados hora a hora del modelo.
            - total_energy: Energía total generada.
            - status: "error" si ocurre un problema, con un mensaje descriptivo.

    Ejemplo de entrada JSON:
    {
        "A": 10,
        "eta": 0.20,
        "I_promedio": 5.5,
        "horas_sol": 12
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
        required_keys = {"A", "eta", "I_promedio", "horas_sol"}
        missing_keys = required_keys - data.keys()
        if missing_keys:
            logger.error(f"Faltan claves requeridas: {missing_keys}")
            return jsonify({"status": "error", "message": f"Faltan claves requeridas: {missing_keys}"}), 400

        # Validar tipos de datos básicos
        if not all(isinstance(data[key], (float, int)) for key in required_keys):
            logger.error("Todos los parámetros deben ser numéricos.")
            return jsonify({"status": "error", "message": "Todos los parámetros deben ser numéricos."}), 400

        # Ejecutar el modelo de optimización solar
        results, total_energy = optimize_solar_energy(data)

        # Responder con los resultados
        logger.info("Modelo ejecutado exitosamente.")
        return jsonify({
            "status": "success",
            "results": results,
            "total_energy": total_energy
        }), 200

    except Exception as e:
        # Capturar errores generales
        logger.error(f"Error inesperado: {e}")
        return jsonify({"status": "error", "message": "Ocurrió un error inesperado. Por favor, intenta nuevamente."}), 500
