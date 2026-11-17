## DEF-01 El ordenamiento por precio no funciona para problem_user

| Campo | Detalle |
|---|---|
| Caso de prueba relacionado | CP-10 |
| Severidad | Media |
| Prioridad | Media |
| Ambiente | Google Chrome en Windows 11, https://www.saucedemo.com |
| Evidencia | `reportes/capturas/CP-10.png` y `reportes/reporte_ronda1.html` |
| Reproducibilidad | 3 de 3 ejecuciones (16 de noviembre del 2026) |

### Pasos para reproducir
1. Iniciar sesión con `problem_user` y `secret_sauce`.
2. En el catálogo, seleccionar **Price (low to high)**.
3. Observar el orden de los precios.

### Resultado esperado
Los productos se muestran ordenados por precio de menor a mayor: 7.99, 9.99, 15.99, 15.99, 29.99, 49.99 (igual que con `standard_user` en CP-06).

### Resultado obtenido
El catálogo se mantiene en el orden original: 29.99, 9.99, 15.99, 49.99, 7.99, 15.99, y el selector sigue mostrando Name (A to Z).

### Estado
Nuevo
