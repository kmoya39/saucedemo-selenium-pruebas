"""
Configuración general de la suite de pruebas.

Los valores se pueden sobrescribir con variables de entorno, por ejemplo:
    set BASE_URL=https://www.saucedemo.com     (Windows CMD)
    $env:HEADLESS="1"                          (Windows PowerShell)
"""
import os

# URL del sistema bajo prueba (SauceDemo, sitio público de Sauce Labs creado para practicar automatización)
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com").rstrip("/")

# Ejecutar el navegador sin interfaz gráfica (1 = sí, 0 = no)
HEADLESS = os.getenv("HEADLESS", "0") == "1"

# Tiempo máximo de espera explícita, en segundos
TIEMPO_ESPERA = int(os.getenv("TIEMPO_ESPERA", "10"))

# Carpeta donde se guardan las evidencias (capturas y resultados)
CARPETA_REPORTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reportes")
