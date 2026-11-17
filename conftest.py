"""
Configuración compartida de pytest.

- Crea y cierra el navegador Chrome para cada caso de prueba (fixture `driver`).
- Ofrece la fixture `registro`, donde cada caso anota su resultado esperado y su resultado obtenido.
- Al terminar cada caso toma una captura de pantalla como evidencia.
- Al final de la ejecución genera reportes/resultados.csv y reportes/resultados.json.
"""
import csv
import json
import os
import platform
from datetime import datetime

import pytest
import selenium
from selenium import webdriver

import config

RESULTADOS = []
os.makedirs(os.path.join(config.CARPETA_REPORTES, "capturas"), exist_ok=True)


@pytest.fixture
def driver():
    opciones = webdriver.ChromeOptions()
    if config.HEADLESS:
        opciones.add_argument("--headless=new")
    opciones.add_argument("--window-size=1366,900")
    # Evita la ventana de Chrome que pregunta por contraseñas filtradas y bloquea la prueba
    opciones.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    opciones.add_argument("--disable-features=PasswordLeakDetection")
    # Selenium Manager descarga automáticamente el ChromeDriver compatible con el Chrome instalado
    navegador = webdriver.Chrome(options=opciones)
    yield navegador
    navegador.quit()


@pytest.fixture
def registro(request):
    """Diccionario donde el caso anota lo esperado y lo obtenido para el informe de pruebas."""
    datos = {"esperado": "", "obtenido": ""}
    request.node.registro = datos
    return datos


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    resultado = yield
    reporte = resultado.get_result()
    if reporte.when != "call":
        return

    marca = item.get_closest_marker("caso")
    id_caso, nombre = (marca.args if marca else (item.name, item.name))
    datos = getattr(item, "registro", {"esperado": "", "obtenido": ""})

    # Captura de pantalla como evidencia del estado final del caso
    captura = ""
    navegador = item.funcargs.get("driver")
    if navegador is not None:
        captura = os.path.join("capturas", f"{id_caso}.png")
        navegador.save_screenshot(os.path.join(config.CARPETA_REPORTES, captura))

    estado = "Aprobado" if reporte.passed else "Fallido"
    detalle = ""
    if reporte.failed:
        detalle = str(call.excinfo.value).splitlines()[0] if call.excinfo else "Error"

    RESULTADOS.append({
        "id": id_caso,
        "nombre": nombre,
        "esperado": datos.get("esperado", ""),
        "obtenido": datos.get("obtenido", ""),
        "estado": estado,
        "duracion_s": round(reporte.duration, 2),
        "detalle": detalle,
        "captura": captura,
    })


def pytest_sessionfinish(session, exitstatus):
    if not RESULTADOS:
        return
    RESULTADOS.sort(key=lambda r: r["id"])
    ruta_csv = os.path.join(config.CARPETA_REPORTES, "resultados.csv")
    with open(ruta_csv, "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(RESULTADOS[0].keys()))
        escritor.writeheader()
        escritor.writerows(RESULTADOS)

    resumen = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": config.BASE_URL,
        "sistema": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "selenium": selenium.__version__,
        "total": len(RESULTADOS),
        "aprobados": sum(r["estado"] == "Aprobado" for r in RESULTADOS),
        "fallidos": sum(r["estado"] == "Fallido" for r in RESULTADOS),
        "casos": RESULTADOS,
    }
    with open(os.path.join(config.CARPETA_REPORTES, "resultados.json"), "w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, ensure_ascii=False, indent=2)
