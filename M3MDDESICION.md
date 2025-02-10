## Modelos de Decisión

## Documentación de la API para la Simulación de Monte Carlo

### Descripción General

Esta API permite ejecutar una simulación de Monte Carlo para el ahorro energético. Calcula estadísticas descriptivas y datos de simulación para graficar, basándose en parámetros como el rango de precios de energía, la producción solar y el consumo energético.

---

### Estructura del Proyecto

```
├── src/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── model_3_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── model_3_services.py
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

#### POST `/api/v1/modulo3/`

Este endpoint ejecuta la simulación de Monte Carlo para el ahorro energético.

##### Parámetros de Entrada

Enviar un JSON con los siguientes campos:

| Campo                    | Tipo          | Descripción                                                |
| ------------------------ | ------------- | ---------------------------------------------------------- |
| `num_simulaciones`       | `int`         | Número de simulaciones de Monte Carlo                      |
| `precio_energia_range`   | `list[float]` | Rango de precios por kWh de energía alterna (USD)          |
| `produccion_solar_range` | `list[float]` | Rango de producción promedio diaria de energía solar (kWh) |
| `consumo_energia_range`  | `list[float]` | Rango de consumo energético de la casa (kWh)               |
| `impuesto_mensual`       | `float`       | Impuesto total mensual de terceros (USD)                   |
| `region`                 | `str`         | Nombre de la región de la vivienda                         |
| `area_vivienda`          | `float`       | Área de la vivienda en m²                                  |
| `consumo_mensual`        | `float`       | Consumo mensual de la vivienda en kWh                      |

##### Ejemplo de Entrada

```json
{
  "num_simulaciones": 10000,
  "precio_energia_range": [0.05, 0.15],
  "produccion_solar_range": [3, 7],
  "consumo_energia_range": [10, 30],
  "impuesto_mensual": 5,
  "region": "SIERRA",
  "area_vivienda": 80,
  "consumo_mensual": 150
}
```

##### Respuesta

| Campo                           | Tipo    | Descripción                                      |
| ------------------------------- | ------- | ------------------------------------------------ |
| `region`                        | `str`   | Nombre de la región de la vivienda               |
| `area_vivienda`                 | `float` | Área de la vivienda en m²                        |
| `consumo_mensual`               | `float` | Consumo mensual de la vivienda en kWh            |
| `vpn_promedio`                  | `float` | Valor presente neto promedio                     |
| `roi_promedio`                  | `float` | Retorno sobre la inversión promedio              |
| `probabilidad_vpn_positivo`     | `float` | Probabilidad de obtener un VPN positivo (%)      |
| `periodo_recuperacion_promedio` | `float` | Periodo de recuperación promedio                 |
| `inversion_promedio`            | `float` | Inversión promedio                               |
| `produccion_anual_promedio`     | `float` | Producción anual promedio de energía solar (kWh) |

##### Ejemplo de Respuesta

```json
{
  "status": "success",
  "results": {
    "region": "SIERRA",
    "area_vivienda": 80,
    "consumo_mensual": 150,
    "vpn_promedio": 1200.5,
    "roi_promedio": 15.3,
    "probabilidad_vpn_positivo": 85.0,
    "periodo_recuperacion_promedio": 6.5,
    "inversion_promedio": 1000,
    "produccion_anual_promedio": 1825.0
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
      "message": "El valor de 'num_simulaciones' debe ser un entero positivo."
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

   - **URL:** `http://localhost:5000/api/v1/modulo3/`
   - **Método:** `POST`
   - **Headers:**
     - `Content-Type: application/json`
   - **Body:**
     ```json
     {
       "num_simulaciones": 10000,
       "precio_energia_range": [0.05, 0.15],
       "produccion_solar_range": [3, 7],
       "consumo_energia_range": [10, 30],
       "impuesto_mensual": 5,
       "region": "SIERRA",
       "area_vivienda": 80,
       "consumo_mensual": 150
     }
     ```

3. **Salida esperada:**
   ```json
   {
     "status": "success",
     "results": {
       "region": "SIERRA",
       "area_vivienda": 80,
       "consumo_mensual": 150,
       "vpn_promedio": 1200.5,
       "roi_promedio": 15.3,
       "probabilidad_vpn_positivo": 85.0,
       "periodo_recuperacion_promedio": 6.5,
       "inversion_promedio": 1000,
       "produccion_anual_promedio": 1825.0
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

### model_3_services.py

#### Función `run_monte_carlo_simulation`

```python
def run_monte_carlo_simulation(num_simulaciones, precio_energia_range, produccion_solar_range, consumo_energia_range, impuesto_mensual, region, area_vivienda, consumo_mensual):
    """
    Ejecuta la simulación de Monte Carlo para el ahorro energético basado en los datos proporcionados.

    Args:
        num_simulaciones (int): Número de simulaciones de Monte Carlo.
        precio_energia_range (tuple): Rango de precios por kWh de energía alterna (USD).
        produccion_solar_range (tuple): Rango de producción promedio diaria de energía solar (kWh).
        consumo_energia_range (tuple): Rango de consumo energético de la casa (kWh).
        impuesto_mensual (float): Impuesto total mensual de terceros (USD).
        region (str): Nombre de la región de la vivienda.
        area_vivienda (float): Área de la vivienda en m².
        consumo_mensual (float): Consumo mensual de la vivienda en kWh.

    Returns:
        dict: Resultados de la simulación con estadísticas descriptivas y datos de simulación para graficar.
    """
```

### model_3_routes.py

#### Ruta `simulate`

```python
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
```
