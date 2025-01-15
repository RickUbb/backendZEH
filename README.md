# **Modulo 1 Optimización Energética API**

## 🌟 **Descripción**

Esta API permite la optimización energética mediante un modelo matemático implementado con `pulp`. Calcula:

- Área óptima de paneles solares.
- Capacidad óptima de batería.
- Estados diarios de carga de la batería.

Es ideal para proyectos de simulación energética y aplicaciones de gestión de energía.

---

## 📁 **Estructura del Proyecto**

├── src/
│ ├── routes/
│ │ ├── **init**.py # Inicialización del módulo de rutas
│ │ ├── model_1_routes.py # Definición de las rutas de la API para el modelo de optimización energética
│ │ ├── model_2_routes.py # Definición de las rutas de la API para la optimización de energía solar
│ │ ├── model_3_routes.py # Definición de las rutas de la API para la simulación de Monte Carlo
│ │ ├── model_4_routes.py # Definición de las rutas de la API para la predicción de consumo energético
│ ├── services/
│ │ ├── **init**.py # Inicialización del módulo de servicios
│ │ ├── model_1_services.py # Lógica del modelo de optimización energética
│ │ ├── model_2_services.py # Lógica para la optimización de energía solar
│ │ ├── model_3_services.py # Lógica para la simulación de Monte Carlo
│ │ ├── model_4_services.py # Lógica para la predicción de consumo energético
│ ├── **init**.py # Inicialización de la aplicación Flask
├── .gitignore # Archivos y carpetas a ignorar por Git
├── main.py # Punto de entrada principal de la API
├── README.md # Documentación del proyecto
├── requirements.txt # Dependencias del proyecto

---

````

---

## 🛠 **Instalación**

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tuusuario/tu-repositorio.git
   cd "C:\Users\ricar\OneDrive\Documentos\Local Proyects\Models"
````

2. **Crear un entorno virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   Crea un archivo `.env` basado en las necesidades del proyecto, si es requerido.

---

## 🚀 **Uso**

1. **Ejecutar la aplicación**:

   ```bash
   python main.py
   ```

2. **Probar la API**:
   La API estará disponible en `http://localhost:5000`.

3. **Endpoint principal**:

   **POST** `/optimize/`

   ### **Parámetros de Entrada**

   Enviar un JSON con los siguientes campos:
   | Campo | Tipo | Descripción |
   |---------------------|--------------|----------------------------------------------------------|
   | `K` | `int` | Número de días de simulación |
   | `c1` | `float` | Costo por m² de panel solar |
   | `c2` | `float` | Costo por kWh de batería |
   | `c3` | `float` | Tarifa por kWh de energía sobrante |
   | `c4` | `float` | Costo por kWh de déficit energético |
   | `gamma` | `float` | Eficiencia de la batería |
   | `r` | `float` | Tasa máxima de carga/descarga de la batería |
   | `X_max` | `float` | Área máxima disponible para paneles solares (m²) |
   | `generacion_solar` | `list[float]`| Lista con generación solar diaria (kWh/m²) |
   | `consumo_energia` | `list[float]`| Lista con consumo energético diario (kWh) |

   ### **Ejemplo de Entrada**

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
       5.1, 5.3, 5.7, 5.5, 4.9, 5.2, 5.4, 5.6, 5.5, 5.3, 5.0, 5.1, 5.2, 5.4,
       5.7, 5.3, 5.1, 5.6, 5.5, 5.4, 5.3, 5.7, 5.5, 5.1, 5.3, 5.4, 5.2, 5.1,
       5.3, 5.4
     ],
     "consumo_energia": [
       10.5, 11.0, 10.8, 10.3, 10.9, 10.4, 10.7, 11.1, 10.6, 10.2, 10.7, 10.9,
       10.5, 10.3, 10.8, 10.6, 10.4, 11.0, 10.9, 10.7, 10.8, 10.5, 10.6, 10.9,
       10.4, 10.2, 10.8, 10.7, 10.5, 10.6
     ]
   }
   ```

   ### **Respuesta**

   | Campo                   | Tipo          | Descripción                                          |
   | ----------------------- | ------------- | ---------------------------------------------------- |
   | `Area_Panel_m2`         | `float`       | Área óptima de panel solar (m²)                      |
   | `Capacidad_Bateria_kWh` | `float`       | Capacidad óptima de batería (kWh)                    |
   | `Estado_Carga_kWh`      | `list[float]` | Lista del estado de carga diario de la batería (kWh) |

   ### **Ejemplo de Respuesta**

   ```json
   {
     "status": "success",
     "results": {
       "Area_Panel_m2": 15.5,
       "Capacidad_Bateria_kWh": 12.3,
       "Estado_Carga_kWh": [3.2, 6.8, 7.0]
     }
   }
   ```

---

## ⚠️ **Manejo de Errores**

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

## 🧪 **Pruebas**

1. **Herramientas sugeridas:**

   - [Postman](https://www.postman.com/) o [cURL](https://curl.se/) para probar manualmente.
   - `pytest` para pruebas unitarias.

2. **Ejemplo con cURL**:

   ```bash
   curl -X POST http://localhost:5000/optimize/ \
   -H "Content-Type: application/json" \
   -d '{
       "K": 30,
       "c1": 100,
       "c2": 500,
       "c3": 0.05,
       "c4": 0.25,
       "gamma": 0.90,
       "r": 0.2,
       "X_max": 20,
       "generacion_solar": [4.5, 5.0, 4.8],
       "consumo_energia": [6.0, 6.5, 7.0]
   }'
   ```

3. **Salida esperada**:
   ```json
   {
     "status": "success",
     "results": {
       "Area_Panel_m2": 15.5,
       "Capacidad_Bateria_kWh": 12.3,
       "Estado_Carga_kWh": [3.2, 6.8, 7.0]
     }
   }
   ```

---

## 🖋 **Contribuciones**

1. Haz un fork del repositorio.
2. Crea una rama: `git checkout -b feature-nueva-funcionalidad`.
3. Realiza commits: `git commit -m 'Añadida nueva funcionalidad'`.
4. Envía un pull request.

---

# **Modulo 2 Optimización Solar API**

## 🌟 **Descripción**

Esta API permite calcular y optimizar la energía generada por un panel solar mediante un modelo matemático implementado con `numpy` y `scipy`. Calcula:

- Inclinación óptima del panel solar (θ) por hora.
- Orientación óptima del panel solar (φ) por hora.
- Energía generada hora a hora.
- Energía total generada durante el día.

Ideal para simulaciones y análisis de sistemas fotovoltaicos.

---

## 🚀 **Uso**

1. **Ejecutar la aplicación**:

   ```bash
   python main.py
   ```

2. **Probar la API**:
   La API estará disponible en `http://localhost:5000`.

3. **Endpoint principal**:

   **POST** `/api/v1/solar/`

   ### **Parámetros de Entrada**

   Enviar un JSON con los siguientes campos:
   | Campo | Tipo | Descripción |
   |----------------|-----------|-----------------------------------------------------------|
   | `A` | `float` | Área del panel solar (m²) |
   | `eta` | `float` | Eficiencia del panel solar (en porcentaje, e.g., `0.20`) |
   | `I_promedio` | `float` | Radiación solar promedio diaria (kWh/m²) |
   | `horas_sol` | `int` | Duración del día (en horas) |

   ### **Ejemplo de Entrada**

   ```json
   {
     "A": 10,
     "eta": 0.2,
     "I_promedio": 5.5,
     "horas_sol": 12
   }
   ```

   ### **Respuesta**

   | Campo              | Tipo    | Descripción                                 |
   | ------------------ | ------- | ------------------------------------------- |
   | `Hora`             | `int`   | Hora del día                                |
   | `Radiación Solar`  | `float` | Radiación solar en esa hora (kWh/m²)        |
   | `Inclinación (θ)`  | `float` | Inclinación óptima del panel solar (°)      |
   | `Orientación (φ)`  | `float` | Orientación óptima del panel solar (°)      |
   | `Energía Generada` | `float` | Energía generada por hora (kWh)             |
   | `total_energy`     | `float` | Energía total generada durante el día (kWh) |

   ### **Ejemplo de Respuesta**

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

## ⚠️ **Manejo de Errores**

- **400 Bad Request**:

  - Datos faltantes o inválidos en la solicitud.
  - Ejemplo de respuesta:
    ```json
    {
      "status": "error",
      "message": "Faltan claves requeridas: {'A', 'eta'}"
    }
    ```

- **500 Internal Server Error**:
  - Error inesperado durante la ejecución del modelo.
  - Ejemplo de respuesta:
    ```json
    {
      "status": "error",
      "message": "Ocurrió un error inesperado. Por favor, intenta nuevamente."
    }
    ```

---

## 🧪 **Pruebas**

1. **Herramientas sugeridas**:

   - [Postman](https://www.postman.com/) o [cURL](https://curl.se/) para probar manualmente.
   - `pytest` para pruebas unitarias.

2. **Ejemplo con cURL**:

   ```bash
   curl -X POST http://localhost:5000/api/v1/solar/ \
   -H "Content-Type: application/json" \
   -d '{
       "A": 10,
       "eta": 0.20,
       "I_promedio": 5.5,
       "horas_sol": 12
   }'
   ```

3. **Salida esperada**:
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

## 🖋 **Contribuciones**

1. Haz un fork del repositorio.
2. Crea una rama: `git checkout -b feature-nueva-funcionalidad`.
3. Realiza commits: `git commit -m 'Añadida nueva funcionalidad'`.
4. Envía un pull request.

---

## 📜 **Licencia**

Este proyecto está licenciado bajo la [MIT License](LICENSE).

```

Este README proporciona una guía completa para la instalación, uso y pruebas de la API de optimización solar. Si necesitas ajustes, ¡avísame! 😊
```
