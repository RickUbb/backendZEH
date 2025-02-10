## Series de Tiempo

## Documentación de la API para la Predicción de Consumo Energético

### Descripción General

Esta API permite realizar predicciones del consumo energético utilizando un modelo ARIMA. Genera predicciones basadas en datos históricos de consumo, incluyendo un intervalo de confianza y un gráfico visual.

---

### Estructura del Proyecto

```
├── src/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── model_4_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── model_4_services.py
│   ├── __init__.py
├── main.py
├── README.md
├── requirements.txt
```

---

### Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/tuusuario/tu-repositorio.git
   cd ...#Ruta donde quedo el clone
   ```

2. **Crear un entorno virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

---

### Uso

1. **Ejecutar la aplicación**:

   ```bash
   python main.py
   ```

2. **Probar la API**:
   La API estará disponible en `http://localhost:5000`.

---

### Endpoints

#### POST `/api/v1/modulo4/`

Este endpoint ejecuta el modelo de predicción de consumo energético.

##### Parámetros de Entrada

Enviar un JSON con los siguientes campos:

| Campo                 | Tipo        | Descripción                                        |
| --------------------- | ----------- | -------------------------------------------------- |
| `electrodomesticos`   | `dict`      | Consumo diario de cada electrodoméstico (kWh)      |
| `dias_historicos`     | `int`       | Número de días históricos a considerar             |
| `orden_arima`         | `list[int]` | Orden del modelo ARIMA                             |
| `intervalo_confianza` | `float`     | Nivel de confianza para el intervalo de predicción |

##### Ejemplo de Entrada

```json
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
```

##### Respuesta

| Campo                 | Tipo    | Descripción                                     |
| --------------------- | ------- | ----------------------------------------------- |
| `historico`           | `list`  | Lista de datos históricos de consumo energético |
| `prediccion`          | `dict`  | Resultados de la predicción                     |
| `fecha_prediccion`    | `str`   | Fecha de la predicción                          |
| `consumo_predicho`    | `float` | Consumo energético predicho                     |
| `intervalo_confianza` | `dict`  | Intervalo de confianza para la predicción       |
| `inferior`            | `float` | Límite inferior del intervalo de confianza      |
| `superior`            | `float` | Límite superior del intervalo de confianza      |

##### Ejemplo de Respuesta

```json
{
  "status": "success",
  "results": {
    "historico": [
      {
        "Fecha": "2023-09-01",
        "Consumo Total (kWh)": 10.5,
        "Aire acondicionado": 1.5,
        "Televisor": 0.1,
        "Refrigeradora": 1.2,
        "Bombillas LED": 0.01,
        "Lavadora": 0.5,
        "Secadora": 2.0,
        "Microondas": 0.9,
        "Computadora de escritorio": 0.2,
        "Cargador de teléfono": 0.01
      }
      // Más registros históricos...
    ],
    "prediccion": {
      "fecha_prediccion": "2023-09-02",
      "consumo_predicho": 11.0,
      "intervalo_confianza": {
        "inferior": 10.0,
        "superior": 12.0
      }
    }
  }
}
```

---

### Manejo de Errores

- **400 Bad Request:**

  - Datos faltantes o inválidos en la solicitud.
  - Ejemplo de respuesta:
    ```json
    {
      "status": "error",
      "message": "Faltan claves requeridas: {'electrodomesticos', 'dias_historicos', 'orden_arima', 'intervalo_confianza'}"
    }
    ```

- **500 Internal Server Error:**
  - Error inesperado durante la ejecución del modelo.
  - Ejemplo de respuesta:
    ```json
    {
      "status": "error",
      "message": "Ocurrió un error inesperado. Por favor, intenta nuevamente."
    }
    ```

---

### Pruebas

1. **Herramientas sugeridas:**

   - [Postman](https://www.postman.com/) o [cURL](https://curl.se/) para probar manualmente.
   - `pytest` para pruebas unitarias.

2. **Ejemplo con Postman:**

   - **URL:** `http://localhost:5000/api/v1/modulo4/`
   - **Método:** `POST`
   - **Headers:**
     - `Content-Type: application/json`
   - **Body:**
     ```json
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
     ```

3. **Salida esperada:**
   ```json
   {
     "status": "success",
     "results": {
       "historico": [
         {
           "Fecha": "2023-09-01",
           "Consumo Total (kWh)": 10.5,
           "Aire acondicionado": 1.5,
           "Televisor": 0.1,
           "Refrigeradora": 1.2,
           "Bombillas LED": 0.01,
           "Lavadora": 0.5,
           "Secadora": 2.0,
           "Microondas": 0.9,
           "Computadora de escritorio": 0.2,
           "Cargador de teléfono": 0.01
         }
       ],
       "prediccion": {
         "fecha_prediccion": "2023-09-02",
         "consumo_predicho": 11.0,
         "intervalo_confianza": {
           "inferior": 10.0,
           "superior": 12.0
         }
       }
     }
   }
   ```

---

### Contribuciones

1. Haz un fork del repositorio.
2. Crea una rama: `git checkout -b feature-nueva-funcionalidad`.
3. Realiza commits: `git commit -m 'Añadida nueva funcionalidad'`.
4. Envía un pull request.

---

### Licencia

Este proyecto está licenciado bajo la MIT License.

---

## Documentación del Código

### model_4_services.py

#### Función `run_prediction`

```python
def run_prediction(data):
    """
    Ejecuta el modelo de predicción de consumo energético basado en los datos proporcionados.

    Args:
        data (dict): Parámetros del modelo.

    Returns:
        dict: Resultados de la predicción.
    """
```

### model_4_routes.py

#### Ruta `predict`

```python
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
```
