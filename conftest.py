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
import subprocess
from datetime import datetime

import pytest
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.selenium_manager import SeleniumManager

import config

RESULTADOS = []
os.makedirs(os.path.join(config.CARPETA_REPORTES, "capturas"), exist_ok=True)


@pytest.fixture(scope="session")
def ruta_chromedriver():
    """
    Obtiene una sola vez la ruta del ChromeDriver compatible con el Chrome instalado.

    Se invoca Selenium Manager con la entrada estándar redirigida a DEVNULL porque en Windows,
    cuando pytest captura la consola, la llamada interna de Selenium puede fallar con
    "WinError 6 The handle is invalid". Si existe la variable CHROMEDRIVER, se usa esa ruta.
    """
    if os.getenv("CHROMEDRIVER"):
        return os.getenv("CHROMEDRIVER")
    comando = [str(SeleniumManager._get_binary()), "--browser", "chrome",
               "--language-binding", "python", "--output", "json"]
    for _ in range(3):  # reintentos por si la red falla al descargar el driver
        salida = subprocess.run(comando, stdin=subprocess.DEVNULL, capture_output=True, text=True)
        try:
            return json.loads(salida.stdout)["result"]["driver_path"]
        except (ValueError, KeyError):
            continue
    pytest.exit(f"No se pudo obtener ChromeDriver con Selenium Manager: {salida.stderr or salida.stdout}")


@pytest.fixture
def driver(ruta_chromedriver):
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
    navegador = webdriver.Chrome(service=Service(executable_path=ruta_chromedriver), options=opciones)
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
    # Se registra la fase de ejecución y también los errores de preparación (por ejemplo, el navegador)
    if reporte.when != "call" and not (reporte.when == "setup" and reporte.failed):
        return

    marca = item.get_closest_marker("caso")
    id_caso, nombre = (marca.args if marca else (item.name, item.name))
    datos = getattr(item, "registro", {"esperado": "", "obtenido": ""})

    # Captura de pantalla como evidencia del estado final del caso
    captura = ""
    navegador = item.funcargs.get("driver")
    if navegador is not None and reporte.when == "call":
        captura = os.path.join("capturas", f"{id_caso}.png")
        navegador.save_screenshot(os.path.join(config.CARPETA_REPORTES, captura))

    if reporte.when == "setup":
        estado = "Error de ambiente"
    else:
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
        "errores": sum(r["estado"] == "Error de ambiente" for r in RESULTADOS),
        "casos": RESULTADOS,
    }
    with open(os.path.join(config.CARPETA_REPORTES, "resultados.json"), "w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, ensure_ascii=False, indent=2)
