# **Optimización Energética API**

## 🌟 **Descripción**
Esta API permite la optimización energética mediante un modelo matemático implementado con `pulp`. Calcula:
- Área óptima de paneles solares.
- Capacidad óptima de batería.
- Estados diarios de carga de la batería.

Es ideal para proyectos de simulación energética y aplicaciones de gestión de energía.

---

## 📁 **Estructura del Proyecto**

├── src/
│   ├── routes/
│   │   ├── __init__.py        # Inicialización del módulo de rutas
│   │   ├── ModelRoutes.py     # Definición de las rutas de la API
│   ├── services/
│   │   ├── __init__.py        # Inicialización del módulo de servicios
│   │   ├── ModelServices.py   # Lógica del modelo de optimización
│   ├── __init__.py            # Inicialización de la aplicación Flask
├── .gitignore                 # Archivos y carpetas a ignorar por Git
├── main.py                    # Punto de entrada principal de la API
├── README.md                  # Documentación del proyecto
├── requirements.txt           # Dependencias del proyecto
```

---

## 🛠 **Instalación**

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tuusuario/tu-repositorio.git
   cd "C:\Users\ricar\OneDrive\Documentos\Local Proyects\Models"
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
   | Campo               | Tipo         | Descripción                                              |
   |---------------------|--------------|----------------------------------------------------------|
   | `K`                 | `int`        | Número de días de simulación                             |
   | `c1`                | `float`      | Costo por m² de panel solar                              |
   | `c2`                | `float`      | Costo por kWh de batería                                 |
   | `c3`                | `float`      | Tarifa por kWh de energía sobrante                       |
   | `c4`                | `float`      | Costo por kWh de déficit energético                      |
   | `gamma`             | `float`      | Eficiencia de la batería                                 |
   | `r`                 | `float`      | Tasa máxima de carga/descarga de la batería              |
   | `X_max`             | `float`      | Área máxima disponible para paneles solares (m²)        |
   | `generacion_solar`  | `list[float]`| Lista con generación solar diaria (kWh/m²)              |
   | `consumo_energia`   | `list[float]`| Lista con consumo energético diario (kWh)               |

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
      "generacion_solar": [5.1, 5.3, 5.7, 5.5, 4.9, 5.2, 5.4, 5.6, 5.5, 5.3, 5.0, 5.1, 5.2, 5.4, 5.7, 5.3, 5.1, 5.6, 5.5, 5.4, 5.3, 5.7, 5.5, 5.1, 5.3, 5.4, 5.2, 5.1, 5.3, 5.4],
      "consumo_energia": [10.5, 11.0, 10.8, 10.3, 10.9, 10.4, 10.7, 11.1, 10.6, 10.2, 10.7, 10.9, 10.5, 10.3, 10.8, 10.6, 10.4, 11.0, 10.9, 10.7, 10.8, 10.5, 10.6, 10.9, 10.4, 10.2, 10.8, 10.7, 10.5, 10.6]
   }
   ```

   ### **Respuesta**
   | Campo                  | Tipo          | Descripción                                              |
   |------------------------|---------------|----------------------------------------------------------|
   | `Area_Panel_m2`        | `float`       | Área óptima de panel solar (m²)                          |
   | `Capacidad_Bateria_kWh`| `float`       | Capacidad óptima de batería (kWh)                        |
   | `Estado_Carga_kWh`     | `list[float]` | Lista del estado de carga diario de la batería (kWh)     |

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

## 📜 **Licencia**

Este proyecto está licenciado bajo la [MIT License](LICENSE).
```