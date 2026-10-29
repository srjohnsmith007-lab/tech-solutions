# LuxuryCo · Reporte automatico

## Que construimos y para quien

LuxuryCo construye un reporte automatico para su propio producto: un script en Python que toma los datos de ejemplo (usuarios, ventas y solicitudes), genera un resumen y una grafica, y los publica en una pagina web. Es para el equipo de LuxuryCo, que necesita ver su actividad sin abrir hojas de calculo.

## Opcion elegida

**Opcion A - Reporte automatico.** El reporte se ejecuta solo cada semana y se publica en GitHub Pages.

## Quien hace que

| Integrante | Responsabilidad |
| ---------- | --------------- |
| Samuel | Lider de proyecto; define los datos que usa el reporte |
| Santiago | README del proyecto y documentacion |
| Angelo | Carpeta del proyecto y .gitignore |

## La ruta

1. **Kickoff · Hoy:** tablero con los tickets del proyecto y este README.
2. **Encargo 2:** un script en Python que lee los datos y genera el reporte (resumen y grafica), sin caerse con datos malos.
3. **Encargo 3:** GitHub Actions ejecuta el script solo, en la nube.
4. **Encargo 4:** el reporte se publica en una pagina web con GitHub Pages.

---

## Sprint 1 · El primer pedido del cliente

### Cliente y qué pidió

**Cliente:** LuxuryCo, boutique de accesorios de lujo (relojes, bolsos, joyas, perfumes, gafas y billeteras). Su gerente de operaciones, Laura Restrepo, pidió automatizar el reporte del mes: hoy lo revisan a mano en Excel y tarda horas.

El programa debe leer el archivo de ventas del mes y entregar:

- Cuántos registros hay.
- Cómo se reparten por categoría.
- Cuánto suman.
- Una gráfica para la reunión de gerencia.

Además, el archivo casi nunca llega limpio (filas incompletas, valores mal escritos, fechas raras): el programa **no se puede detener** por eso, tiene que separar esas filas y decir cuántas fueron. Y el nombre del archivo y la columna que se suma deben poder cambiarse sin abrir el código.

### Qué hay en esta carpeta

| Archivo | Qué hace | Ticket |
| ------- | -------- | ------ |
| `generar_datos.py` | Crea `datos/registros.csv` con las ventas simuladas del cliente | 1 |
| `datos/registros.csv` | Los datos: 105 filas (100 buenas y 5 dañadas a propósito) | 1 |
| `reporte.py` | Programa principal: calcula y escribe `salida/reporte.md` | 2 |
| `grafica.py` | Crea la gráfica interactiva `salida/grafica.html` | 3 |

### Cómo se ejecuta, paso a paso

1. Instala [Python 3](https://www.python.org/downloads/) (en Windows, marca "Add Python to PATH").
2. Clona el repositorio y entra a la carpeta del proyecto:

   ```bash
   git clone https://github.com/srjohnsmith007-lab/tech-solutions.git
   cd tech-solutions/reporte
   ```

3. Genera los datos (no necesita instalar nada, solo usa la librería estándar):

   ```bash
   python generar_datos.py
   ```

   Debe imprimir `Filas buenas: 100 | Filas dañadas: 5 | Total: 105` y crear `datos/registros.csv`.

4. Para el reporte completo (cuando los tickets 2 y 3 estén fusionados), instala las librerías y ejecuta:

   ```bash
   pip install -r requirements.txt
   python reporte.py
   ```

   El resultado queda en la carpeta `salida/`: `reporte.md` y `grafica.html`.

Cada vez que se ejecuta `generar_datos.py` sale **el mismo archivo** (usa una semilla fija), así todo el equipo trabaja con los mismos datos.

### Cómo abrir el CSV en Excel

En Excel en español, hacer doble clic en un CSV separado por comas puede dejar todo en una sola columna. Para verlo bien:

1. Abre Excel con un libro en blanco.
2. **Datos → Desde texto/CSV** y elige `datos/registros.csv`.
3. Origen del archivo: **UTF-8**. Delimitador: **coma**. Cargar.

### Las columnas de `registros.csv`

| Columna | Qué es | Ejemplo |
| ------- | ------ | ------- |
| `id` | Consecutivo de la venta | `V001` |
| `fecha` | Día de la venta, formato AAAA-MM-DD (septiembre de 2026) | `2026-09-19` |
| `categoria` | **Categoría**: Relojes, Bolsos, Joyas, Perfumes, Gafas o Billeteras | `Joyas` |
| `producto` | Producto vendido dentro de la categoría | `Anillo de oro` |
| `cantidad` | Unidades vendidas | `1` |
| `valor` | **Valor numérico**: cantidad × precio, en pesos, sin `$` ni puntos | `780000` |
| `medio_de_pago` | Tarjeta, Transferencia o Efectivo | `Tarjeta` |
| `estado` | **Estado**: entregado, pendiente o cancelado | `entregado` |

El `valor` siempre es `cantidad × precio del producto` (los precios están en el catálogo de `generar_datos.py`).

### Las 5 filas dañadas (a propósito)

| Fila | Problema |
| ---- | -------- |
| `V101` | `valor` vacío |
| `V102` | `valor` con texto (`cuatrocientos mil`) en vez de número |
| `V103` | Fecha mal escrita (`2026-13-40`, el mes 13 no existe) |
| `V104` | Fila incompleta: falta la `categoria` |
| `V105` | `cantidad` con texto (`dos`) |

Están mezcladas entre las filas buenas, no todas al final, como pasa en la vida real. El reporte debe dar: **105 leídas = 100 válidas + 5 descartadas**.

### Un pedazo del reporte como ejemplo

Así debe verse `salida/reporte.md` con estos datos (lo genera `reporte.py`):

```markdown
# Reporte del mes: LuxuryCo

## Resumen

| Dato | Valor |
|---|---|
| Filas leídas | 105 |
| Registros válidos | 100 |
| Filas descartadas | 5 |
| Valor total | $78.180.000 |

## Por categoría

| Categoría | Registros | Valor |
|---|---|---|
| Relojes | 14 | $22.800.000 |
| Joyas | 17 | $14.940.000 |
| Gafas | 23 | $13.160.000 |
```
