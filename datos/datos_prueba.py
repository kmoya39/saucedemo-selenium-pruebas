"""
Datos de prueba utilizados por los casos automatizados.

Los usuarios y la contraseña son públicos y aparecen en la misma página de inicio de SauceDemo.
Se separan del código de las pruebas para facilitar su mantenimiento (pruebas guiadas por datos).
"""

CONTRASENA_VALIDA = "secret_sauce"

USUARIOS = {
    "estandar": "standard_user",
    "bloqueado": "locked_out_user",
    "con_problemas": "problem_user",
}

# Mensajes que el sistema debe mostrar según la especificación del sitio
MENSAJES = {
    "credenciales_invalidas": "Epic sadface: Username and password do not match any user in this service",
    "usuario_bloqueado": "Epic sadface: Sorry, this user has been locked out.",
    "usuario_requerido": "Epic sadface: Username is required",
    "codigo_postal_requerido": "Error: Postal Code is required",
    "compra_completa": "Thank you for your order!",
}

# Datos del comprador para el proceso de pago
COMPRADOR = {
    "nombre": "Kevin",
    "apellido": "Moya",
    "codigo_postal": "10101",
}

PRODUCTO_MOCHILA = "sauce-labs-backpack"
NOMBRE_MOCHILA = "Sauce Labs Backpack"
