"""
Casos de prueba del módulo de autenticación.
Técnicas de diseño: partición de equivalencia y tabla de decisión.
"""
import pytest

from datos.datos_prueba import USUARIOS, CONTRASENA_VALIDA, MENSAJES
from paginas.pagina_login import PaginaLogin
from paginas.pagina_inventario import PaginaInventario


@pytest.mark.caso("CP-01", "Inicio de sesión con credenciales válidas")
def test_inicio_sesion_valido(driver, registro):
    registro["esperado"] = "Redirige a /inventory.html y muestra el título Products"
    PaginaLogin(driver).cargar().iniciar_sesion(USUARIOS["estandar"], CONTRASENA_VALIDA)
    inventario = PaginaInventario(driver)
    titulo = inventario.titulo()
    registro["obtenido"] = f"URL {inventario.url_actual().split('/')[-1]} con título {titulo}"
    assert inventario.url_actual().endswith("/inventory.html")
    assert titulo == "Products"


@pytest.mark.caso("CP-02", "Inicio de sesión con contraseña incorrecta")
def test_inicio_sesion_contrasena_incorrecta(driver, registro):
    registro["esperado"] = MENSAJES["credenciales_invalidas"]
    login = PaginaLogin(driver).cargar()
    login.iniciar_sesion(USUARIOS["estandar"], "clave_incorrecta")
    registro["obtenido"] = login.mensaje_error()
    assert registro["obtenido"] == registro["esperado"]
    assert login.esta_visible()


@pytest.mark.caso("CP-03", "Inicio de sesión con usuario bloqueado")
def test_inicio_sesion_usuario_bloqueado(driver, registro):
    registro["esperado"] = MENSAJES["usuario_bloqueado"]
    login = PaginaLogin(driver).cargar()
    login.iniciar_sesion(USUARIOS["bloqueado"], CONTRASENA_VALIDA)
    registro["obtenido"] = login.mensaje_error()
    assert registro["obtenido"] == registro["esperado"]


@pytest.mark.caso("CP-04", "Inicio de sesión con el campo de usuario vacío")
def test_inicio_sesion_usuario_vacio(driver, registro):
    registro["esperado"] = MENSAJES["usuario_requerido"]
    login = PaginaLogin(driver).cargar()
    login.iniciar_sesion("", CONTRASENA_VALIDA)
    registro["obtenido"] = login.mensaje_error()
    assert registro["obtenido"] == registro["esperado"]
