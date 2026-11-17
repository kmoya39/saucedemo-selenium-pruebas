"""Page Objects del carrito y del proceso de pago (checkout)."""
from selenium.webdriver.common.by import By

from paginas.pagina_base import PaginaBase


class PaginaCarrito(PaginaBase):
    NOMBRES_PRODUCTOS = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    BOTON_PAGAR = (By.CSS_SELECTOR, "[data-test='checkout']")

    def productos(self):
        self.esperar_visible(self.NOMBRES_PRODUCTOS)
        return [e.text for e in self.driver.find_elements(*self.NOMBRES_PRODUCTOS)]

    def ir_a_pagar(self):
        self.clic(self.BOTON_PAGAR)


class PaginaCompra(PaginaBase):
    CAMPO_NOMBRE = (By.CSS_SELECTOR, "[data-test='firstName']")
    CAMPO_APELLIDO = (By.CSS_SELECTOR, "[data-test='lastName']")
    CAMPO_CODIGO_POSTAL = (By.CSS_SELECTOR, "[data-test='postalCode']")
    BOTON_CONTINUAR = (By.CSS_SELECTOR, "[data-test='continue']")
    BOTON_FINALIZAR = (By.CSS_SELECTOR, "[data-test='finish']")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    IMPUESTO = (By.CSS_SELECTOR, "[data-test='tax-label']")
    TOTAL = (By.CSS_SELECTOR, "[data-test='total-label']")
    ENCABEZADO_FINAL = (By.CSS_SELECTOR, "[data-test='complete-header']")

    def llenar_datos(self, nombre, apellido, codigo_postal):
        if nombre:
            self.escribir(self.CAMPO_NOMBRE, nombre)
        if apellido:
            self.escribir(self.CAMPO_APELLIDO, apellido)
        if codigo_postal:
            self.escribir(self.CAMPO_CODIGO_POSTAL, codigo_postal)
        self.clic(self.BOTON_CONTINUAR)

    @staticmethod
    def _monto(texto):
        # Convierte textos como "Item total: $29.99" en 29.99
        return float(texto.split("$")[-1])

    def montos(self):
        return {
            "subtotal": self._monto(self.texto(self.SUBTOTAL)),
            "impuesto": self._monto(self.texto(self.IMPUESTO)),
            "total": self._monto(self.texto(self.TOTAL)),
        }

    def finalizar(self):
        self.clic(self.BOTON_FINALIZAR)

    def mensaje_final(self):
        return self.texto(self.ENCABEZADO_FINAL)

    def mensaje_error(self):
        return self.texto(self.MENSAJE_ERROR)
