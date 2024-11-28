"""
main.py

Este módulo inicializa y ejecuta la aplicación Flask. Se utiliza como punto de entrada
para el servidor local en modo desarrollo o producción.
"""

from src import init_app  # Función para inicializar la aplicación Flask
import sys  # Para manejar errores y registrar en stderr


def initialize_app():
    """
    Inicializa la aplicación Flask.

    Llama a `init_app()` desde el módulo `src.__init__` para obtener una instancia configurada
    de Flask con blueprints registrados y configuraciones iniciales aplicadas.

    Returns:
        Flask: Instancia configurada de la aplicación Flask.

    Raises:
        RuntimeError: Si ocurre un error durante la inicialización.
    """
    try:
        # Inicializar y configurar la aplicación
        app = init_app()
        return app
    except Exception as e:
        # Manejo de errores durante la inicialización
        raise RuntimeError(f"Error al inicializar la aplicación: {e}")


if __name__ == '__main__':
    """
    Este bloque se ejecuta solo si el archivo es ejecutado directamente.
    Inicializa la aplicación Flask y lanza el servidor local.
    """
    try:
        # Llamar a la función para inicializar la aplicación
        app = initialize_app()

        # Iniciar el servidor Flask en modo producción (debug desactivado)
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        # Registrar errores de ejecución en stderr
        print(f"Error al iniciar el servidor Flask: {e}", file=sys.stderr)
