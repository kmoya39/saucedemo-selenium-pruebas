"""
Casos de prueba del proceso de compra (checkout).
Técnicas de diseño: casos de uso (flujo principal y flujo alterno) y valores límite (campo vacío).
"""
import pytest

from datos.datos_prueba import (USUARIOS, CONTRASENA_VALIDA, MENSAJES, COMPRADOR,
                                PRODUCTO_MOCHILA, NOMBRE_MOCHILA)
from paginas.pagina_login import PaginaLogin
from paginas.pagina_inventario import PaginaInventario
from paginas.pagina_compra import PaginaCarrito, PaginaCompra


def preparar_compra(driver):
    """Inicia sesión, agrega la mochila al carrito y entra al formulario de pago."""
    PaginaLogin(driver).cargar().iniciar_sesion(USUARIOS["estandar"], CONTRASENA_VALIDA)
    inventario = PaginaInventario(driver)
    inventario.agregar_al_carrito(PRODUCTO_MOCHILA)
    inventario.ir_al_carrito()
    carrito = PaginaCarrito(driver)
    productos = carrito.productos()
    carrito.ir_a_pagar()
    return productos, PaginaCompra(driver)


@pytest.mark.caso("CP-07", "Completar una compra con datos válidos")
def test_compra_completa(driver, registro):
    registro["esperado"] = ("Carrito con Sauce Labs Backpack; total = subtotal + impuesto; "
                            f"mensaje final: {MENSAJES['compra_completa']}")
    productos, compra = preparar_compra(driver)
    compra.llenar_datos(COMPRADOR["nombre"], COMPRADOR["apellido"], COMPRADOR["codigo_postal"])
    montos = compra.montos()
    compra.finalizar()
    mensaje = compra.mensaje_final()
    registro["obtenido"] = (f"Carrito con {', '.join(productos)}; subtotal ${montos['subtotal']}, "
                            f"impuesto ${montos['impuesto']}, total ${montos['total']}; mensaje final: {mensaje}")
    assert productos == [NOMBRE_MOCHILA]
    assert round(montos["subtotal"] + montos["impuesto"], 2) == montos["total"]
    assert mensaje == MENSAJES["compra_completa"]


@pytest.mark.caso("CP-08", "Intentar pagar sin código postal")
def test_compra_sin_codigo_postal(driver, registro):
    registro["esperado"] = MENSAJES["codigo_postal_requerido"]
    _, compra = preparar_compra(driver)
    compra.llenar_datos(COMPRADOR["nombre"], COMPRADOR["apellido"], "")
    registro["obtenido"] = compra.mensaje_error()
    assert registro["obtenido"] == registro["esperado"]
    assert compra.url_actual().endswith("/checkout-step-one.html")
