# Simulación: Mi primera ejecución de pruebas

Suite de pruebas automatizadas con **Selenium WebDriver** sobre el sitio de práctica
[SauceDemo](https://www.saucedemo.com), creado por Sauce Labs para practicar automatización.

Curso Calidad del Software (SC-405), Universidad Fidélitas. Autor: Kevin Alexander Moya Jiménez.

## Tecnologías

| Herramienta | Uso |
|---|---|
| Python 3.12 o superior | Lenguaje de programación |
| Selenium WebDriver 4 | Automatización del navegador Chrome |
| pytest + pytest-html | Ejecución de los casos y reporte HTML |
| Git + GitHub | Control de versiones del código |
| GitHub Issues | Gestión de los casos de prueba y de los defectos |
| GitHub Actions | Ejecución automática de la suite en la nube |

## Estructura (patrón Page Object Model)

```
config.py               URL, modo sin interfaz y tiempo de espera
conftest.py             Navegador, evidencias y resultados esperado vs. obtenido
datos/datos_prueba.py   Usuarios, mensajes y datos del comprador
paginas/                Un Page Object por página del sitio
pruebas/                Casos de prueba CP-01 a CP-10
casos_prueba/           Diseño de cada caso (se publica en GitHub Issues)
herramientas/           Script para crear los issues
reportes/               Reporte HTML, resultados.csv, resultados.json y capturas
```

## Cómo ejecutar (Windows)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

Requiere Google Chrome instalado. Selenium Manager descarga el ChromeDriver correcto.
Para ejecutar sin abrir la ventana del navegador: `$env:HEADLESS="1"; pytest`

Al terminar, abrir `reportes/reporte_pruebas.html`. Las capturas quedan en `reportes/capturas/`.

## Casos de prueba

| ID | Caso | Módulo |
|---|---|---|
| CP-01 | Inicio de sesión con credenciales válidas | Autenticación |
| CP-02 | Inicio de sesión con contraseña incorrecta | Autenticación |
| CP-03 | Inicio de sesión con usuario bloqueado | Autenticación |
| CP-04 | Inicio de sesión con el campo de usuario vacío | Autenticación |
| CP-05 | Agregar un producto al carrito | Catálogo y carrito |
| CP-06 | Ordenar productos por precio de menor a mayor | Catálogo y carrito |
| CP-07 | Completar una compra con datos válidos | Proceso de compra |
| CP-08 | Intentar pagar sin código postal | Proceso de compra |
| CP-09 | Cerrar sesión desde el menú lateral | Autenticación |
| CP-10 | Ordenar productos por precio con problem_user | Catálogo y carrito |
