"""
reporte.py  ·  Ticket 2: El reporte
Proyecto: LuxuryCo - Automatización del reporte mensual
Autor: Samuel Hernández (srjohnsmith007-lab)

Este script principal:
1. Lee el archivo CSV de ventas (datos/registros.csv).
2. Valida cada fila con control de excepciones (try / except).
   Separa y cuenta las filas dañadas sin detener la ejecución.
3. Totaliza los registros válidos, valor total y ventas por categoría.
4. Llama a la función crear_grafica() de grafica.py (Ticket 3).
5. Genera el documento de resumen en Markdown (salida/reporte.md).
"""

import csv
import os
from datetime import datetime
from collections import defaultdict
from grafica import crear_grafica


def formatear_pesos(numero):
    """
    Convierte un número a formato de moneda con separador de miles en puntos.
    Ejemplo: 4350000 -> '$4.350.000'
    """
    return "$" + f"{numero:,.0f}".replace(",", ".")


def procesar_reporte(archivo_csv="datos/registros.csv", salida_reporte="salida/reporte.md", salida_grafica="salida/grafica.html"):
    """
    Función principal que ejecuta el flujo de consolidación del reporte mensual.
    
    Parámetros:
    - archivo_csv: Ruta del archivo generado por Ticket 1.
    - salida_reporte: Ruta donde se guardará el resumen en Markdown.
    - salida_grafica: Ruta donde la función de Ticket 3 generará el HTML.
    """
    # 1. Validación de existencia del archivo fuente
    if not os.path.exists(archivo_csv):
        print(f"Error: No se encontró el archivo de datos en '{archivo_csv}'.")
        print("Asegúrate de ejecutar primero: python generar_datos.py")
        return

    # Contadores y acumuladores requeridos por la guía
    filas_leidas = 0
    registros_validos = 0
    filas_descartadas = 0
    valor_total = 0

    # Diccionario para agrupar ventas y registros por cada categoría
    ventas_por_categoria = defaultdict(lambda: {"registros": 0, "valor": 0})

    # 2. Lectura y procesamiento fila por fila
    with open(archivo_csv, mode="r", encoding="utf-8") as f:
        lector = csv.reader(f)
        encabezados = next(lector, None)  # Saltamos la fila de títulos

        for fila in lector:
            filas_leidas += 1

            # Bloque try/except: ninguna fila dañada detiene el programa
            try:
                # Comprobar que la fila tenga al menos 8 columnas
                if len(fila) < 8:
                    raise ValueError("Fila con columnas incompletas")

                # Extracción de campos según el esquema del CSV
                # 0: id, 1: fecha, 2: categoria, 3: producto, 4: cantidad, 5: valor, 6: medio_de_pago, 7: estado
                id_venta = fila[0].strip()
                fecha_str = fila[1].strip()
                categoria = fila[2].strip()
                producto = fila[3].strip()
                cantidad_str = fila[4].strip()
                valor_str = fila[5].strip()
                medio_pago = fila[6].strip()
                estado = fila[7].strip()

                # Validación 1: Campos obligatorios de texto no vacíos
                if not id_venta or not categoria or not producto:
                    raise ValueError("Campo obligatorio de texto vacío")

                # Validación 2: Fecha con formato válido YYYY-MM-DD
                datetime.strptime(fecha_str[:10], "%Y-%m-%d")

                # Validación 3: Cantidad numérica entera mayor a 0
                cantidad = int(cantidad_str)
                if cantidad <= 0:
                    raise ValueError("Cantidad debe ser un entero positivo")

                # Validación 4: Valor numérico mayor a 0
                valor = float(valor_str)
                if valor <= 0:
                    raise ValueError("El valor de la venta debe ser mayor a 0")

                # Si todas las validaciones pasaron, acumulamos los datos válidos
                registros_validos += 1
                valor_total += valor
                ventas_por_categoria[categoria]["registros"] += 1
                ventas_por_categoria[categoria]["valor"] += valor

            except Exception as e:
                # Cualquier fila con datos corruptos se suma a descartadas y continúa
                filas_descartadas += 1
                continue

    # 3. Llamar a la función de gráfica (Ticket 3)
    # Ordenamos las categorías por valor total descendente
    categorias_ordenadas = sorted(
        ventas_por_categoria.keys(),
        key=lambda c: ventas_por_categoria[c]["valor"],
        reverse=True
    )
    valores_ordenados = [ventas_por_categoria[c]["valor"] for c in categorias_ordenadas]

    # Generamos la gráfica interactiva llamando a Ticket 3
    crear_grafica(categorias_ordenadas, valores_ordenados, salida_grafica)

    # 4. Generación del reporte en Markdown (salida/reporte.md)
    fecha_generacion = datetime.now().strftime("%Y-%m-%d")

    lineas_md = [
        "# Reporte del mes: LuxuryCo",
        f"Generado el: {fecha_generacion}",
        "",
        "## Resumen",
        "| Dato | Valor |",
        "|---|---|",
        f"| Filas leídas | {filas_leidas} |",
        f"| Registros válidos | {registros_validos} |",
        f"| Filas descartadas | {filas_descartadas} |",
        f"| Valor total | {formatear_pesos(valor_total)} |",
        "",
        "## Por categoría",
        "| Categoría | Registros | Valor |",
        "|---|---|---|",
    ]

    for cat in categorias_ordenadas:
        datos = ventas_por_categoria[cat]
        lineas_md.append(f"| {cat} | {datos['registros']} | {formatear_pesos(datos['valor'])} |")

    lineas_md.extend([
        "",
        "## Gráfica",
        f"Ver `{salida_grafica}`"
    ])

    # Aseguramos que la carpeta de salida exista
    os.makedirs(os.path.dirname(salida_reporte), exist_ok=True)

    with open(salida_reporte, mode="w", encoding="utf-8") as f_out:
        f_out.write("\n".join(lineas_md) + "\n")

    # 5. Salida por consola para comprobación inmediata
    print(f"Reporte generado exitosamente en: {salida_reporte}")
    print(f" -> Filas leídas: {filas_leidas}")
    print(f" -> Registros válidos: {registros_validos}")
    print(f" -> Filas descartadas: {filas_descartadas}")
    print(f" -> Comprobación matemática: {registros_validos} + {filas_descartadas} = {filas_leidas}")


if __name__ == "__main__":
    procesar_reporte()
