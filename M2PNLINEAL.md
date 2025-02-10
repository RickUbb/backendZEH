## Programación No Lineal

## **Documentación de la API para la Optimización de Energía Solar**

### **Descripción General**

Esta API permite calcular y optimizar la energía generada por un panel solar mediante un modelo matemático implementado con `numpy` y `scipy`. Calcula:

- Inclinación óptima del panel solar (θ) por hora.
- Orientación óptima del panel solar (φ) por hora.
- Energía generada hora a hora.
- Energía total generada durante el día.

Ideal para simulaciones y análisis de sistemas fotovoltaicos.

---

### **Estructura del Proyecto**

```
├── src/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── model_2_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── model_2_services.py
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

#### **POST** `/api/v1/modulo2/`

Este endpoint ejecuta el modelo de optimización de energía solar.

##### **Parámetros de Entrada**

Enviar un JSON con los siguientes campos:

| Campo        | Tipo    | Descripción                                              |
| ------------ | ------- | -------------------------------------------------------- |
| `A`          | `float` | Área del panel solar (m²)                                |
| `eta`        | `float` | Eficiencia del panel solar (en porcentaje, e.g., `0.20`) |
| `I_promedio` | `float` | Radiación solar promedio diaria (kWh/m²)                 |
| `horas_sol`  | `int`   | Duración del día (en horas)                              |

##### **Ejemplo de Entrada**

```json
{
  "A": 10,
  "eta": 0.2,
  "I_promedio": 5.5,
  "horas_sol": 12
}
```

##### **Respuesta**

| Campo              | Tipo    | Descripción                                 |
| ------------------ | ------- | ------------------------------------------- |
| `Hora`             | `int`   | Hora del día                                |
| `Radiación Solar`  | `float` | Radiación solar en esa hora (kWh/m²)        |
| `Inclinación (θ)`  | `float` | Inclinación óptima del panel solar (°)      |
| `Orientación (φ)`  | `float` | Orientación óptima del panel solar (°)      |
| `Energía Generada` | `float` | Energía generada por hora (kWh)             |
| `total_energy`     | `float` | Energía total generada durante el día (kWh) |

##### **Ejemplo de Respuesta**

```json
{
  "status": "success",
  "results": [
    {
      "Hora": 6,
      "Radiación Solar (kWh/m²)": 5.1,
      "Inclinación (θ)": 28.34,
      "Orientación (φ)": -10.23,
      "Energía Generada (kWh)": 8.23
    },
    {
      "Hora": 7,
      "Radiación Solar (kWh/m²)": 6.0,
      "Inclinación (θ)": 32.12,
      "Orientación (φ)": -5.1,
      "Energía Generada (kWh)": 9.41
    }
    // Más registros por cada hora del día...
  ],
  "total_energy": 85.3
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
      "message": "Faltan claves requeridas: {'A', 'eta'}"
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

2. **Ejemplo con cURL:**

   ```bash
   curl -X POST http://localhost:5000/api/v1/modulo2/ \
   -H "Content-Type: application/json" \
   -d '{
       "A": 10,
       "eta": 0.20,
       "I_promedio": 5.5,
       "horas_sol": 12
   }'
   ```

3. **Salida esperada:**
   ```json
   {
     "status": "success",
     "results": [
       {
         "Hora": 6,
         "Radiación Solar (kWh/m²)": 5.1,
         "Inclinación (θ)": 28.34,
         "Orientación (φ)": -10.23,
         "Energía Generada (kWh)": 8.23
       }
     ],
     "total_energy": 85.3
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

### **model_2_services.py**

#### **Función `optimize_solar_energy`**

```python
def optimize_solar_energy(data):
    """
    Optimiza la energía generada por paneles solares.
    Args:
        data (dict): Diccionario con los parámetros del modelo. Debe contener:
            - A (float): Área del panel solar (m²).
            - eta (float): Eficiencia del panel (%).
            - I_promedio (float): Radiación solar promedio diaria (kWh/m²).
            - horas_sol (int): Duración del día (horas).

    Returns:
        tuple: Lista de resultados hora a hora y energía total generada.
    """
```

### **model_2_routes.py**

#### **Ruta `optimize`**

```python
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
```

---
