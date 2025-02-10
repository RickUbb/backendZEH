---
Los ejemplos de los endpoints se pueden usar y ver en POSTMAN importando el archivo "ZEH Examples.postman_collection.json" adjunto en este repositorio.
---

### **1. Programación Lineal (Módulo 1): Optimización de Paneles Solares y Baterías**

#### **Teoría Detallada**

**Objetivo**: Minimizar el costo total de un sistema solar-batería, asegurando que la energía generada cubra el consumo diario.

---

#### **Ecuaciones Matemáticas y Variables**

1. **Variables de Decisión**:

   - `\(X_1\)`: Área de paneles solares (m²) → **Entera** (no se instalan fracciones de panel).
   - `\(X_2\)`: Capacidad de la batería (kWh) → **Entera** (baterías discretas).
   - `\(X_3^{(k)}\)`: Estado de carga (SoC) de la batería en el día `\(k\)` (kWh).
   - `\(E_k\)`: Excedente energético en el día `\(k\)` (kWh).
   - `\(D_k\)`: Déficit energético en el día `\(k\)` (kWh).

2. **Función Objetivo**:
   \[
   \text{Minimizar } Z = \underbrace{c*1 X_1}*{\text{Costo paneles}} + \underbrace{c*2 X_2}*{\text{Costo batería}} + \sum*{k=1}^K \left( \underbrace{c_3 E_k}*{\text{Beneficio excedente}} + \underbrace{c*4 D_k}*{\text{Costo déficit}} \right)
   \]

   - `\(c_1 = 100\)` USD/m², `\(c_2 = 500\)` USD/kWh, `\(c_3 = 0.05\)` USD/kWh, `\(c_4 = 0.25\)` USD/kWh.

3. **Restricciones**:

   - **Balance Energético**:
     \[
     X*3^{(k)} = \gamma X_3^{(k-1)} + \underbrace{X_1 G_k}*{\text{Generación}} - \underbrace{C*k}*{\text{Consumo}}, \quad \forall k = 1, ..., K
     \]

     - `\(G_k\)`: Generación solar en el día `\(k\)` (kWh/m²).
     - `\(C_k\)`: Consumo energético en el día `\(k\)` (kWh).
     - `\(\gamma = 0.9\)`: Eficiencia de carga/descarga de la batería.

   - **Límites Físicos**:
     \[
     0 \leq X_3^{(k)} \leq X_2 \quad \text{(La batería no puede sobrecargarse ni descargarse por debajo de 0)}
     \]
     \[
     |X_3^{(k)} - X_3^{(k-1)}| \leq r X_2 \quad \text{(Máxima tasa de carga/descarga diaria, \(r = 0.25\))}
     \]

   - **Criterio ZEH (Zero Energy Home)**:
     \[
     X*1 \sum*{k=1}^K G*k \geq \sum*{k=1}^K C_k \quad \text{(La energía generada debe cubrir el consumo total)}
     \]

---

#### **Implementación en Código**

```python
# Definición del modelo MILP (Mixed Integer Linear Programming)
modelo = pulp.LpProblem("Optimizacion_Energetica", pulp.LpMinimize)

# Variables enteras para paneles y batería
X1 = pulp.LpVariable("Area_Panel", lowBound=0, upBound=X_max, cat='Integer')
X2 = pulp.LpVariable("Capacidad_Bateria", lowBound=0, cat='Integer')

# Restricción de balance energético
for k in range(K):
    if k == 0:
        modelo += X3[k] == gamma * 0 + X1 * generacion_solar[k] - consumo_energia[k]
    else:
        modelo += X3[k] == gamma * X3[k-1] + X1 * generacion_solar[k] - consumo_energia[k]
```

````

#### **Análisis Crítico**

- **Limitaciones**:
  - Asume generación y consumo diarios **independientes** (no considera correlaciones climáticas).
  - No modela degradación de paneles/baterías a largo plazo.
- **Mejoras Propuestas**:
  - Usar **programación estocástica** para incorporar incertidumbre en `\(G_k\)` y `\(C_k\)`.
  - Incluir **costos de mantenimiento** en la función objetivo.

---

### **2. Optimización No Lineal (Módulo 2): Orientación Óptima de Paneles**

#### **Teoría Detallada**

**Objetivo**: Maximizar la energía generada `\(E(\theta, \phi)\)` ajustando la inclinación (`\(\theta\)`) y orientación (`\(\phi\)`) del panel.

---

#### **Ecuaciones Matemáticas**

1. **Modelo de Radiación Solar**:
   \[
   E(\theta, \phi) = A \cdot \eta \cdot I \cdot \left( \sin\theta \sin\beta + \cos\theta \cos\beta \cos(\phi - \alpha) \right)
   \]

   - `\(A = 10\)` m²: Área del panel.
   - `\(\eta = 0.2\)`: Eficiencia del panel.
   - `\(I = 5.5\)` kWh/m²: Radiación solar.
   - `\(\beta\)`: Altitud solar (ángulo sobre el horizonte).
   - `\(\alpha\)`: Azimut solar (ángulo respecto al norte).

2. **Optimización**:
   \[
   \text{Maximizar } E(\theta, \phi) \quad \text{sujeto a } 0 \leq \theta \leq 90°, \quad -180° \leq \phi \leq 180°
   \]

---

#### **Implementación en Código**

```python
def energia(theta_phi, beta, alpha, area, eficiencia, radiacion):
    theta, phi = theta_phi
    theta_rad = np.radians(theta)
    phi_rad = np.radians(phi)
    return -area * eficiencia * radiacion * (
        np.sin(theta_rad) * np.sin(beta) +
        np.cos(theta_rad) * np.cos(beta) * np.cos(phi_rad - alpha)
    )

# Minimizar la función negativa para maximizar energía
res = minimize(energia, [30, 0], args=(beta, alpha, A, eta, radiacion_hora),
              bounds=[(0, 90), (-180, 180)], method='L-BFGS-B')
```

#### **Análisis Crítico**

- **Limitaciones**:
  - Modelo **determinista**: No considera nubosidad o sombras variables.
  - Asume radiación solar constante por hora.
- **Mejoras Propuestas**:
  - Usar datos reales de radiación horaria (API de NSRDB).
  - Incluir un **seguidor solar dinámico** en tiempo real.

---

### **3. Modelos de Decisión (Módulo 3): Simulación de Monte Carlo**

#### **Teoría Detallada**

**Objetivo**: Evaluar la **viabilidad financiera** de instalar paneles solares bajo incertidumbre.

---

#### **Ecuaciones Matemáticas**

1. **Variables Aleatorias**:

   - `\(P \sim U(0.05, 0.15)\)`: Precio de energía (USD/kWh).
   - `\(G \sim U(3, 7)\)`: Generación solar diaria (kWh/m²).
   - `\(C \sim U(10, 30)\)`: Consumo diario (kWh).

2. **Ahorro Anual**:
   \[
   \text{Ahorro} = \left( C - G \right) \cdot P \cdot 365 \quad \text{(Si } C > G \text{)}
   \]

3. **Valor Presente Neto (VPN)**:
   \[
   \text{VPN} = -I*0 + \sum*{t=1}^{T} \frac{\text{Ahorro}\_t}{(1 + r)^t}
   \]

   - `\(I_0 = 1000\)` USD: Inversión inicial.
   - `\(r = 0.05\)`: Tasa de descuento anual.

4. **Retorno sobre Inversión (ROI)**:
   \[
   \text{ROI} = \left( \frac{\text{Ahorro Anual}}{I_0} \right) \times 100\%
   \]

---

#### **Implementación en Código**

```python
# Simulación de Monte Carlo
for _ in range(num_simulaciones):
    precio_energia = np.random.uniform(0.05, 0.15)
    produccion_solar = np.random.uniform(3, 7)
    consumo_energia = np.random.uniform(10, 30)

    energia_red = max(0, consumo_energia - produccion_solar)
    ahorro_anual = energia_red * precio_energia * 365

    # Cálculo de VPN y ROI
    periodo_recuperacion = inversion_inicial / ahorro_anual
    roi = (ahorro_anual * 100) / inversion_inicial
    vpn = ahorro_anual / (1 + 0.05) ** periodo_recuperacion
```

#### **Análisis Crítico**

- **Limitaciones**:
  - Asume **independencia** entre `\(P\)`, `\(G\)`, y `\(C\)` (poco realista).
  - No considera inflación o cambios en políticas energéticas.
- **Mejoras Propuestas**:
  - Usar **Copulas** para modelar dependencias entre variables.
  - Incluir un modelo de **inflación estocástica**.

---

### **4. Series de Tiempo (Módulo 4): Predicción con ARIMA**

#### **Teoría Detallada**

**Objetivo**: Predecir el consumo energético futuro usando patrones históricos.

---

#### **Ecuaciones Matemáticas**

1. **Modelo ARIMA(p, d, q)**:
   \[
   \underbrace{(1 - \phi*1 B - \dots - \phi_p B^p)}*{\text{AR(p)}} \underbrace{(1 - B)^d}_{\text{I(d)}} y_t = \underbrace{(1 + \theta_1 B + \dots + \theta_q B^q) \varepsilon_t}_{\text{MA(q)}}
   \]

   - `\(B\)`: Operador de retardo (`\(B y_t = y_{t-1}\)`).
   - `\(\phi_i\)`: Coeficientes autoregresivos.
   - `\(\theta_i\)`: Coeficientes de media móvil.
   - `\(\varepsilon_t\)`: Ruido blanco (media cero, varianza constante).

2. **Predicción con Intervalo de Confianza**:
   \[
   \hat{y}_{t+1} \pm z_{\alpha/2} \cdot \sigma\_{\varepsilon}
   \]
   - `\(z_{\alpha/2}\)`: Valor crítico de la distribución normal (ej: 1.96 para 95% de confianza).
   - `\(\sigma_{\varepsilon}\)`: Desviación estándar de los residuos.

---

#### **Implementación en Código**

```python
# Ajuste del modelo ARIMA(5,1,0)
modelo = ARIMA(serie_temporal, order=(5, 1, 0))
modelo_fit = modelo.fit()

# Predicción con intervalo de confianza
prediccion = modelo_fit.get_forecast(steps=1)
prediccion_valor = prediccion.predicted_mean.iloc[0]
intervalo = prediccion.conf_int(alpha=0.05).iloc[0]
```

#### **Análisis Crítico**

- **Limitaciones**:
  - **Univariante**: Ignora variables exógenas (ej: temperatura).
  - **Estacionariedad**: Requiere diferenciación manual (`\(d=1\)`).
- **Mejoras Propuestas**:
  - Usar **SARIMAX** para incluir estacionalidad y variables externas.
  - Automatizar la selección de `\(p, d, q\)` con **AutoARIMA**.

---

### **Resumen Integrador**

| **Concepto**                 | **Programación Lineal**       | **Optimización No Lineal**       | **Monte Carlo**            | **Series de Tiempo**       |
| ---------------------------- | ----------------------------- | -------------------------------- | -------------------------- | -------------------------- |
| **Naturaleza del Problema**  | Determinista, lineal          | Determinista, no lineal          | Estocástico                | Estocástico, temporal      |
| **Variables Clave**          | `\(X_1, X_2, E_k, D_k\)`      | `\(\theta, \phi\)`               | `\(P, G, C\)`              | `\(y_t, \varepsilon_t\)`   |
| **Herramientas Matemáticas** | MILP, Simplex, Branch & Bound | Optimización con restricciones   | Distribuciones Uniformes   | ARIMA, Diferenciación      |
| **Limitaciones**             | Supuestos simplificados       | Modelo físico idealizado         | Independencia de variables | Univariante, no estacional |
| **Mejoras Futuras**          | Programación Estocástica      | Datos satelitales en tiempo real | Modelos de Copulas         | SARIMAX, Prophet           |

---

### **Conclusión General**

Cada módulo aborda una faceta crítica del diseño de sistemas energéticos:

1. **Programación Lineal**: Dimensionamiento óptimo de recursos físicos.
2. **Optimización No Lineal**: Ajuste fino de parámetros operativos.
3. **Monte Carlo**: Evaluación de riesgos financieros.
4. **Series de Tiempo**: Pronóstico de demanda energética.

Al integrar estos módulos, se logra un sistema holístico para la toma de decisiones en energía renovable, desde la instalación hasta la operación diaria. ¿Te gustaría explorar algún módulo en mayor profundidad? 😊

```

```
````
