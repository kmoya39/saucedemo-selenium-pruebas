"""
Clase base del patrón Page Object Model (POM).

Reúne las acciones comunes a todas las páginas (esperar, hacer clic, escribir, leer texto),
de modo que cada página concreta solo describe sus localizadores y sus acciones de negocio.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config


class PaginaBase:
    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, config.TIEMPO_ESPERA)

    def abrir(self, ruta=""):
        self.driver.get(f"{config.BASE_URL}/{ruta}")

    def esperar_visible(self, localizador):
        return self.espera.until(EC.visibility_of_element_located(localizador))

    def clic(self, localizador):
        self.espera.until(EC.element_to_be_clickable(localizador)).click()

    def escribir(self, localizador, texto):
        campo = self.esperar_visible(localizador)
        campo.clear()
        campo.send_keys(texto)

    def texto(self, localizador):
        return self.esperar_visible(localizador).text

    def existe(self, localizador):
        return len(self.driver.find_elements(*localizador)) > 0

    def url_actual(self):
        return self.driver.current_url
