"""Page Object de la página de inventario (catálogo de productos)."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from paginas.pagina_base import PaginaBase


class PaginaInventario(PaginaBase):
    TITULO = (By.CSS_SELECTOR, "[data-test='title']")
    PRECIOS = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    NOMBRES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    SELECTOR_ORDEN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    INSIGNIA_CARRITO = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    ENLACE_CARRITO = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    BOTON_MENU = (By.ID, "react-burger-menu-btn")
    ENLACE_SALIR = (By.CSS_SELECTOR, "[data-test='logout-sidebar-link']")

    @staticmethod
    def boton_agregar(producto):
        return (By.CSS_SELECTOR, f"[data-test='add-to-cart-{producto}']")

    @staticmethod
    def boton_quitar(producto):
        return (By.CSS_SELECTOR, f"[data-test='remove-{producto}']")

    def titulo(self):
        return self.texto(self.TITULO)

    def precios(self):
        """Devuelve la lista de precios mostrados, convertidos a número."""
        self.esperar_visible(self.PRECIOS)
        return [float(e.text.replace("$", "")) for e in self.driver.find_elements(*self.PRECIOS)]

    def catalogo(self):
        """Devuelve pares (nombre, precio) tal como los muestra el sitio."""
        self.esperar_visible(self.NOMBRES)
        nombres = [e.text for e in self.driver.find_elements(*self.NOMBRES)]
        return list(zip(nombres, self.precios()))

    def ordenar_por(self, valor):
        # Valores disponibles: az, za, lohi (precio menor a mayor), hilo (precio mayor a menor)
        Select(self.esperar_visible(self.SELECTOR_ORDEN)).select_by_value(valor)

    def agregar_al_carrito(self, producto):
        self.clic(self.boton_agregar(producto))

    def cantidad_en_carrito(self):
        if not self.existe(self.INSIGNIA_CARRITO):
            return 0
        return int(self.texto(self.INSIGNIA_CARRITO))

    def boton_quitar_visible(self, producto):
        return self.existe(self.boton_quitar(producto))

    def ir_al_carrito(self):
        self.clic(self.ENLACE_CARRITO)

    def cerrar_sesion(self):
        self.clic(self.BOTON_MENU)
        self.clic(self.ENLACE_SALIR)
