"""
Casos de prueba del catálogo de productos y la sesión.
Técnicas de diseño: transición de estados y partición de equivalencia.
"""
import pytest

from datos.datos_prueba import USUARIOS, CONTRASENA_VALIDA, PRODUCTO_MOCHILA
from paginas.pagina_login import PaginaLogin
from paginas.pagina_inventario import PaginaInventario


def ingresar(driver, usuario=USUARIOS["estandar"]):
    """Paso previo común: iniciar sesión y devolver la página de inventario."""
    PaginaLogin(driver).cargar().iniciar_sesion(usuario, CONTRASENA_VALIDA)
    inventario = PaginaInventario(driver)
    inventario.titulo()  # espera a que cargue el catálogo
    return inventario


@pytest.mark.caso("CP-05", "Agregar un producto al carrito")
def test_agregar_producto_carrito(driver, registro):
    registro["esperado"] = "Insignia del carrito = 1 y el botón cambia a Remove"
    inventario = ingresar(driver)
    inventario.agregar_al_carrito(PRODUCTO_MOCHILA)
    cantidad = inventario.cantidad_en_carrito()
    boton_quitar = inventario.boton_quitar_visible(PRODUCTO_MOCHILA)
    registro["obtenido"] = f"Insignia del carrito = {cantidad}; botón Remove visible = {'sí' if boton_quitar else 'no'}"
    assert cantidad == 1
    assert boton_quitar


@pytest.mark.caso("CP-06", "Ordenar productos por precio de menor a mayor")
def test_ordenar_precio_menor_mayor(driver, registro):
    inventario = ingresar(driver)
    esperado = sorted(inventario.precios())
    registro["esperado"] = f"Precios en orden ascendente: {esperado}"
    inventario.ordenar_por("lohi")
    obtenido = inventario.precios()
    registro["obtenido"] = f"Precios mostrados: {obtenido}"
    assert obtenido == esperado


@pytest.mark.caso("CP-09", "Cerrar sesión desde el menú lateral")
def test_cerrar_sesion(driver, registro):
    registro["esperado"] = "Regresa a la página de inicio de sesión y no permite volver al inventario sin autenticarse"
    inventario = ingresar(driver)
    inventario.cerrar_sesion()
    login = PaginaLogin(driver)
    login.esperar_visible(PaginaLogin.BOTON_INGRESAR)
    en_login = login.esta_visible()
    # Intento de acceso directo al inventario después de cerrar sesión
    inventario.abrir("inventory.html")
    mensaje = login.mensaje_error()
    registro["obtenido"] = f"Formulario de login visible = {'sí' if en_login else 'no'}; acceso directo bloqueado con mensaje: {mensaje}"
    assert en_login
    assert "when you are logged in" in mensaje


@pytest.mark.caso("CP-10", "Ordenar productos por precio con el usuario problem_user")
def test_ordenar_precio_usuario_con_problemas(driver, registro):
    # Mismo escenario que CP-06, pero con otra clase de equivalencia de usuario.
    # Se espera el mismo comportamiento: el orden no debe depender del usuario.
    inventario = ingresar(driver, USUARIOS["con_problemas"])
    esperado = sorted(inventario.precios())
    registro["esperado"] = f"Precios en orden ascendente: {esperado}"
    inventario.ordenar_por("lohi")
    obtenido = inventario.precios()
    registro["obtenido"] = f"Precios mostrados: {obtenido}"
    assert obtenido == esperado, "El catálogo no se ordenó por precio para problem_user"
