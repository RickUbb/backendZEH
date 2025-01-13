"""
SolarPanelService.py

Este módulo define la lógica para calcular y optimizar la energía generada
por un panel solar utilizando `numpy` y `scipy`.
"""

import numpy as np
from scipy.optimize import minimize


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
    A = data['A']
    eta = data['eta']
    I_promedio = data['I_promedio']
    horas_sol = int(data['horas_sol'])

    horas = np.arange(6, 6 + horas_sol)
    altitud_solar = np.radians(45 + 15 * np.sin((horas - 12) * np.pi / 12))
    azimut_solar = np.radians((horas - 12) * 15)

    def energia(theta_phi, beta, alpha, area, eficiencia, radiacion):
        theta, phi = theta_phi
        theta_rad = np.radians(theta)
        phi_rad = np.radians(phi)
        return -area * eficiencia * radiacion * (
            np.sin(theta_rad) * np.sin(beta) + np.cos(theta_rad) *
            np.cos(beta) * np.cos(phi_rad - alpha)
        )

    bounds = [(0, 90), (-180, 180)]
    resultados = []
    energia_total = 0

    for t, (beta, alpha) in enumerate(zip(altitud_solar, azimut_solar)):
        radiacion_hora = I_promedio * np.random.uniform(0.7, 1.3)
        res = minimize(energia, [30, 0], args=(
            beta, alpha, A, eta, radiacion_hora), bounds=bounds, method='L-BFGS-B')
        theta_opt, phi_opt = res.x
        energia_hora = -res.fun
        energia_total += energia_hora
        resultados.append({
            "Hora": int(horas[t]),
            "Radiación Solar (kWh/m²)": float(radiacion_hora),
            "Inclinación (θ)": float(theta_opt),
            "Orientación (φ)": float(phi_opt),
            "Energía Generada (kWh)": float(energia_hora)
        })

    return resultados, float(energia_total)
