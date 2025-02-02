"""
src.__init__.py

Este módulo inicializa la aplicación Flask y configura sus componentes principales,
incluyendo el registro de blueprints y la configuración de CORS.
"""

from flask import Flask  # Clase principal para crear aplicaciones Flask
from flask_cors import CORS  # Habilitar CORS (Cross-Origin Resource Sharing)
from src.routes import model_1_routes, model_2_routes, model_3_routes, model_4_routes # Importa las rutas del modelo


# Instancia global de la aplicación Flask
app = Flask(__name__)

# Configuración de CORS para permitir solicitudes desde diferentes dominios
CORS(app)


def init_app():
    """
    Inicializa la aplicación Flask y registra los blueprints requeridos.

    Returns:
        Flask: Instancia configurada de la aplicación Flask.

    Raises:
        RuntimeError: Si ocurre un error al registrar los blueprints.
    """
    try:
        # Registrar el blueprint del modelo modulo 1 con el prefijo '/optimize'
        app.register_blueprint(model_1_routes.main, url_prefix='/api/v1/modulo1')
        # Registrar el blueprint del modelo modulo 2 con el prefijo '/solar'
        app.register_blueprint(model_2_routes.solar, url_prefix='/api/v1/modulo2')
        # Registrar el blueprint del modelo modulo 3 con el prefijo '/solar'
        app.register_blueprint(model_3_routes.monte_carlo, url_prefix='/api/v1/modulo3')
        # Registrar el blueprint del modelo modulo 4 con el prefijo '/solar'
        app.register_blueprint(model_4_routes.main, url_prefix='/api/v1/modulo4')

        return app  # Devuelve la aplicación configurada
    except Exception as e:
        # Registrar errores de inicialización y lanzar una excepción
        raise RuntimeError(
            f"Error al registrar las rutas en la aplicación Flask: {e}"
        )
