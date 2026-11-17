"""Page Object de la página de inicio de sesión."""
from selenium.webdriver.common.by import By

from paginas.pagina_base import PaginaBase


class PaginaLogin(PaginaBase):
    CAMPO_USUARIO = (By.CSS_SELECTOR, "[data-test='username']")
    CAMPO_CONTRASENA = (By.CSS_SELECTOR, "[data-test='password']")
    BOTON_INGRESAR = (By.CSS_SELECTOR, "[data-test='login-button']")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def cargar(self):
        self.abrir()
        self.esperar_visible(self.CAMPO_USUARIO)
        return self

    def iniciar_sesion(self, usuario, contrasena):
        # Si el dato viene vacío no se escribe nada, para simular el campo en blanco
        if usuario:
            self.escribir(self.CAMPO_USUARIO, usuario)
        if contrasena:
            self.escribir(self.CAMPO_CONTRASENA, contrasena)
        self.clic(self.BOTON_INGRESAR)

    def mensaje_error(self):
        return self.texto(self.MENSAJE_ERROR)

    def esta_visible(self):
        return self.existe(self.BOTON_INGRESAR)
