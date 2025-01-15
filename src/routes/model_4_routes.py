"""
Este módulo define las rutas para el modelo de predicción de consumo energético utilizando Flask.

Rutas:
    - POST /: Ejecuta el modelo de predicción de consumo energético basado en los datos proporcionados en el cuerpo de la solicitud.

Funciones:
    - predict(): Maneja las solicitudes POST para ejecutar el modelo de predicción. Valida los datos de entrada, ejecuta el modelo y devuelve los resultados en formato JSON.

Dependencias:
    - Flask: Para manejar las solicitudes HTTP y definir las rutas.
    - Flask-CORS: Para permitir solicitudes de orígenes cruzados.
    - src.services.model_4_services: Contiene la lógica para ejecutar el modelo de predicción.
    - logging: Para registrar errores y eventos importantes.

Ejemplo de uso:
    Ejecutar el servidor Flask y enviar una solicitud POST a la ruta '/' con un JSON que contenga los parámetros necesarios para la predicción.
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
        - electrodomesticos (dict): Consumo diario de cada electrodoméstico (kWh).
        - dias_historicos (int): Número de días históricos a considerar.
        - orden_arima (list[int]): Orden del modelo ARIMA.
        - intervalo_confianza (float): Nivel de confianza para el intervalo de predicción.

    Returns:
        JSON:
            - status: "success" si la predicción se ejecuta correctamente.
            - results: Resultados del modelo, incluyendo la predicción y el intervalo de confianza.
            - status: "error" si ocurre un problema, con un mensaje descriptivo.

    Ejemplo de entrada JSON:
    {
        "electrodomesticos": {
            "Aire acondicionado": 1.5,
            "Televisor": 0.1,
            "Refrigeradora": 1.2,
            "Bombillas LED": 0.01,
            "Lavadora": 0.5,
            "Secadora": 2.0,
            "Microondas": 0.9,
            "Computadora de escritorio": 0.2,
            "Cargador de teléfono": 0.01
        },
        "dias_historicos": 30,
        "orden_arima": [5, 1, 0],
        "intervalo_confianza": 0.95
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
        required_keys = {"electrodomesticos", "dias_historicos",
                         "orden_arima", "intervalo_confianza"}
        missing_keys = required_keys - data.keys()
        if missing_keys:
            logger.error(f"Faltan claves requeridas: {missing_keys}")
            return jsonify({"status": "error", "message": f"Faltan claves requeridas: {missing_keys}"}), 400

        # Validar tipos de datos básicos
        if not isinstance(data['electrodomesticos'], dict):
            logger.error("'electrodomesticos' debe ser un diccionario.")
            return jsonify({"status": "error", "message": "'electrodomesticos' debe ser un diccionario."}), 400
        if not isinstance(data['dias_historicos'], int) or data['dias_historicos'] <= 0:
            logger.error("'dias_historicos' debe ser un entero positivo.")
            return jsonify({"status": "error", "message": "'dias_historicos' debe ser un entero positivo."}), 400
        if not isinstance(data['orden_arima'], list) or len(data['orden_arima']) != 3 or not all(isinstance(i, int) for i in data['orden_arima']):
            logger.error("'orden_arima' debe ser una lista de tres enteros.")
            return jsonify({"status": "error", "message": "'orden_arima' debe ser una lista de tres enteros."}), 400
        if not isinstance(data['intervalo_confianza'], float) or not (0 < data['intervalo_confianza'] < 1):
            logger.error(
                "'intervalo_confianza' debe ser un flotante entre 0 y 1.")
            return jsonify({"status": "error", "message": "'intervalo_confianza' debe ser un flotante entre 0 y 1."}), 400

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
