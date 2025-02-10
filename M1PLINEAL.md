## Programación Lineal

## Documentación de la API

### **Descripción General**

Esta API permite la optimización energética mediante un modelo matemático implementado con `pulp`. Calcula:

- Área óptima de paneles solares.
- Capacidad óptima de batería.
- Estados diarios de carga de la batería.

Es ideal para proyectos de simulación energética y aplicaciones de gestión de energía.

---

### **Estructura del Proyecto**

```
├── src/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── model_1_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── model_1_services.py
│   ├── __init__.py
├── main.py
├── README.md
├── requirements.txt
```

---

### **Instalación**

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

### **Uso**

1. **Ejecutar la aplicación**:

   ```bash
   python main.py
   ```

2. **Probar la API**:
   La API estará disponible en `http://localhost:5000`.

---

### **Endpoints**

#### **POST** `/api/v1/modulo1/`

Este endpoint ejecuta el modelo de optimización energética.

##### **Parámetros de Entrada**

Enviar un JSON con los siguientes campos:

| Campo              | Tipo          | Descripción                                      |
| ------------------ | ------------- | ------------------------------------------------ |
| `K`                | `int`         | Número de días de simulación                     |
| `c1`               | `float`       | Costo por m² de panel solar                      |
| `c2`               | `float`       | Costo por kWh de batería                         |
| `c3`               | `float`       | Tarifa por kWh de energía sobrante               |
| `c4`               | `float`       | Costo por kWh de déficit energético              |
| `gamma`            | `float`       | Eficiencia de la batería                         |
| `r`                | `float`       | Tasa máxima de carga/descarga de la batería      |
| `X_max`            | `float`       | Área máxima disponible para paneles solares (m²) |
| `generacion_solar` | `list[float]` | Lista con generación solar diaria (kWh/m²)       |
| `consumo_energia`  | `list[float]` | Lista con consumo energético diario (kWh)        |

##### **Ejemplo de Entrada**

```json
{
  "K": 30,
  "c1": 100,
  "c2": 500,
  "c3": 0.05,
  "c4": 0.25,
  "gamma": 0.9,
  "r": 0.2,
  "X_max": 20,
  "generacion_solar": [
    4.5, 5.0, 4.8, 5.1, 5.3, 5.7, 5.5, 4.9, 5.2, 5.4, 5.6, 5.5, 5.3, 5.0, 5.1,
    5.2, 5.4, 5.7, 5.3, 5.1, 5.6, 5.5, 5.4, 5.3, 5.7, 5.5, 5.1, 5.3, 5.4, 5.2
  ],
  "consumo_energia": [
    10.5, 11.0, 10.8, 10.3, 10.9, 10.4, 10.7, 11.1, 10.6, 10.2, 10.7, 10.9,
    10.5, 10.3, 10.8, 10.6, 10.4, 11.0, 10.9, 10.7, 10.8, 10.5, 10.6, 10.9,
    10.4, 10.2, 10.8, 10.7, 10.5, 10.6
  ]
}
```

##### **Respuesta**

| Campo                   | Tipo          | Descripción                                          |
| ----------------------- | ------------- | ---------------------------------------------------- |
| `Area_Panel_m2`         | `float`       | Área óptima de panel solar (m²)                      |
| `Capacidad_Bateria_kWh` | `float`       | Capacidad óptima de batería (kWh)                    |
| `Estado_Carga_kWh`      | `list[float]` | Lista del estado de carga diario de la batería (kWh) |

##### **Ejemplo de Respuesta**

```json
{
  "status": "success",
  "results": {
    "Area_Panel_m2": 15.5,
    "Capacidad_Bateria_kWh": 12.3,
    "Estado_Carga_kWh": [3.2, 6.8, 7.0, ...]
  }
}
```

---

### **Manejo de Errores**

- **400 Bad Request:**

  - Datos faltantes o inválidos en la solicitud.
  - Ejemplo de respuesta:
    ```json
    {
      "status": "error",
      "message": "El valor de 'K' debe ser un entero positivo."
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

### **Pruebas**

1. **Herramientas sugeridas:**

   - [Postman](https://www.postman.com/) o [cURL](https://curl.se/) para probar manualmente.
   - `pytest` para pruebas unitarias.

2. **Ejemplo con Postman:**

   - **URL:** `http://localhost:5000/api/v1/modulo1/`
   - **Método:** `POST`
   - **Headers:**
     - `Content-Type: application/json`
   - **Body:**
     ```json
     {
       "K": 30,
       "c1": 100,
       "c2": 500,
       "c3": 0.05,
       "c4": 0.25,
       "gamma": 0.9,
       "r": 0.2,
       "X_max": 20,
       "generacion_solar": [
         4.5, 5.0, 4.8, 5.1, 5.3, 5.7, 5.5, 4.9, 5.2, 5.4, 5.6, 5.5, 5.3, 5.0,
         5.1, 5.2, 5.4, 5.7, 5.3, 5.1, 5.6, 5.5, 5.4, 5.3, 5.7, 5.5, 5.1, 5.3,
         5.4, 5.2
       ],
       "consumo_energia": [
         10.5, 11.0, 10.8, 10.3, 10.9, 10.4, 10.7, 11.1, 10.6, 10.2, 10.7, 10.9,
         10.5, 10.3, 10.8, 10.6, 10.4, 11.0, 10.9, 10.7, 10.8, 10.5, 10.6, 10.9,
         10.4, 10.2, 10.8, 10.7, 10.5, 10.6
       ]
     }
     ```

3. **Salida esperada:**
   ```json
   {
     "status": "success",
     "results": {
       "Area_Panel_m2": 15.5,
       "Capacidad_Bateria_kWh": 12.3,
       "Estado_Carga_kWh": [3.2, 6.8, 7.0, ...]
     }
   }
   ```

---

### **Contribuciones**

1. Haz un fork del repositorio.
2. Crea una rama: `git checkout -b feature-nueva-funcionalidad`.
3. Realiza commits: `git commit -m 'Añadida nueva funcionalidad'`.
4. Envía un pull request.

---

### **Licencia**

Este proyecto está licenciado bajo la MIT License.

---

## **Documentación del Código**

### **model_1_services.py**

#### **Función `run_optimization`**

```python
def run_optimization(data):
    """
    Ejecuta el modelo de optimización energética basado en los datos proporcionados.

    Args:
        data (dict): Diccionario con los parámetros del modelo. Debe contener:
            - K (int): Número de días.
            - c1, c2, c3, c4 (float): Costos asociados al modelo.
            - gamma (float): Eficiencia de la batería.
            - r (float): Tasa máxima de carga/descarga.
            - X_max (float): Área máxima disponible para paneles solares.
            - generacion_solar (list[float]): Energía generada por m² (kWh/m²) diaria.
            - consumo_energia (list[float]): Energía consumida diariamente (kWh).

    Returns:
        dict: Resultados de la optimización con los valores óptimos de las variables.
            - Area_Panel_m2: Área óptima de paneles solares (entera).
            - Capacidad_Bateria_kWh: Capacidad óptima de la batería (entera).
            - Generacion_Solar_kWh_m2: Lista con la generación solar por día.
            - Consumo_Energetico_kWh: Lista con el consumo energético por día.
            - Estado_Carga_kWh: Lista con el estado de carga de la batería por día.
    """
```

### **model_1_routes.py**

#### **Ruta `optimize`**

```python
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
```

---
