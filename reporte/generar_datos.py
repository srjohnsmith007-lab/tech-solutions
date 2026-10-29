"""
generar_datos.py  ·  Ticket 1: Los datos del cliente

Crea el archivo datos/registros.csv con ventas SIMULADAS de LuxuryCo,
una boutique de accesorios de lujo. Es el archivo que el reporte lee después.

El archivo trae 100 ventas buenas y 5 filas dañadas a propósito, porque
el cliente casi nunca recibe el archivo limpio y el reporte tiene que
aprender a separarlas sin caerse.

Solo usa la librería estándar de Python (csv, random, datetime, os).

Cómo se ejecuta (dentro de la carpeta reporte/):
    python generar_datos.py
"""

import csv
import os
import random
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# 1. CONFIGURACIÓN: lo que se puede cambiar sin tocar la lógica
# ---------------------------------------------------------------------------

# Carpeta donde vive este script. Así el archivo se crea en el mismo lugar
# aunque el script se ejecute desde otra carpeta.
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA_BASE, "datos", "registros.csv")

CANTIDAD_FILAS_BUENAS = 100  # ventas válidas
SEMILLA = 47                 # misma semilla = siempre el mismo CSV (se puede repetir y comparar)

# Las 8 columnas del archivo, en el orden en que quedan en el CSV.
COLUMNAS = ["id", "fecha", "categoria", "producto", "cantidad", "valor",
            "medio_de_pago", "estado"]

# Catálogo de LuxuryCo: cada categoría tiene sus productos y el precio unitario
# en pesos colombianos. El reporte agrupa las ventas por "categoria".
CATALOGO = {
    "Relojes":    [("Reloj clásico", 1800000), ("Reloj deportivo", 1200000)],
    "Bolsos":     [("Bolso de mano", 950000), ("Maletín ejecutivo", 1100000)],
    "Joyas":      [("Collar de plata", 620000), ("Anillo de oro", 780000)],
    "Perfumes":   [("Perfume 100 ml", 380000), ("Perfume 50 ml", 240000)],
    "Gafas":      [("Gafas de sol", 450000), ("Gafas de lectura", 290000)],
    "Billeteras": [("Billetera de cuero", 280000), ("Tarjetero", 150000)],
}
CATEGORIAS = list(CATALOGO)

# Peso de cada categoría (en el mismo orden de CATEGORIAS): los perfumes y las
# gafas se venden más que los relojes, para que la gráfica no salga con todas
# las barras iguales.
PESOS_CATEGORIAS = [10, 14, 16, 26, 20, 14]

MEDIOS_DE_PAGO = ["Tarjeta", "Transferencia", "Efectivo"]
PESOS_PAGO = [50, 30, 20]

# Estados de la venta. Pocas canceladas, como en un negocio real.
ESTADOS = ["entregado", "pendiente", "cancelado"]
PESOS_ESTADOS = [88, 7, 5]

# Mes que cubre el reporte: septiembre de 2026 (30 días).
FECHA_INICIO = date(2026, 9, 1)
DIAS_DEL_MES = 30


# ---------------------------------------------------------------------------
# 2. FILAS BUENAS
# ---------------------------------------------------------------------------

def crear_venta(numero):
    """Devuelve una fila (lista de 8 valores) con una venta válida.

    numero: el consecutivo de la venta; se usa para armar el id (V001, V002...).
    """
    # Primero se elige la categoría y luego un producto de ESA categoría,
    # así nunca sale un "Perfume" dentro de la categoría "Relojes".
    categoria = random.choices(CATEGORIAS, weights=PESOS_CATEGORIAS)[0]
    producto, precio = random.choice(CATALOGO[categoria])

    # En una boutique de lujo casi siempre se vende 1 pieza; a veces 2 o 3.
    cantidad = random.choices([1, 2, 3], weights=[75, 18, 7])[0]

    # El valor SIEMPRE sale de multiplicar cantidad por el precio del producto.
    # Así el dato tiene sentido para el negocio (no hay valores al azar).
    valor = cantidad * precio

    # Fecha al azar dentro del mes, en formato AAAA-MM-DD (el que el reporte espera).
    fecha = FECHA_INICIO + timedelta(days=random.randint(0, DIAS_DEL_MES - 1))

    return [
        f"V{numero:03d}",                                        # id
        fecha.isoformat(),                                       # fecha
        categoria,                                               # categoria
        producto,                                                # producto
        cantidad,                                                # cantidad
        valor,                                                   # valor (número entero, sin $ ni puntos)
        random.choices(MEDIOS_DE_PAGO, weights=PESOS_PAGO)[0],   # medio_de_pago
        random.choices(ESTADOS, weights=PESOS_ESTADOS)[0],       # estado
    ]


# ---------------------------------------------------------------------------
# 3. FILAS DAÑADAS (a propósito)
# ---------------------------------------------------------------------------

def crear_filas_danadas(primer_numero):
    """Devuelve 5 filas rotas, cada una con un tipo de error distinto.

    Son los errores típicos que el cliente describió: filas incompletas,
    valores mal escritos y fechas raras. Sirven para probar que el reporte
    las separa y las cuenta sin detenerse.
    """
    n = primer_numero
    return [
        # 1) Valor vacío: la venta existe pero no se sabe cuánto costó.
        [f"V{n:03d}", "2026-09-05", "Perfumes", "Perfume 100 ml", 2, "", "Tarjeta", "entregado"],
        # 2) Texto donde va un número: alguien escribió el valor con letras.
        [f"V{n + 1:03d}", "2026-09-12", "Gafas", "Gafas de sol", 1, "cuatrocientos mil", "Transferencia", "entregado"],
        # 3) Fecha mal escrita: el mes 13 no existe.
        [f"V{n + 2:03d}", "2026-13-40", "Relojes", "Reloj clásico", 1, 1800000, "Tarjeta", "entregado"],
        # 4) Fila incompleta: falta la categoría.
        [f"V{n + 3:03d}", "2026-09-20", "", "Tarjetero", 2, 300000, "Efectivo", "pendiente"],
        # 5) Cantidad con texto: no se puede contar ni multiplicar.
        [f"V{n + 4:03d}", "2026-09-27", "Bolsos", "Bolso de mano", "dos", 1900000, "Transferencia", "entregado"],
    ]


# ---------------------------------------------------------------------------
# 4. PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    # Fijar la semilla hace que cada ejecución produzca exactamente los mismos datos.
    random.seed(SEMILLA)

    # Construir las 100 ventas buenas (V001 ... V100).
    filas = [crear_venta(n) for n in range(1, CANTIDAD_FILAS_BUENAS + 1)]

    # Construir las 5 dañadas (V101 ... V105) y mezclarlas entre las buenas.
    # Se insertan en posiciones al azar: en la vida real las filas malas
    # no vienen todas juntas al final del archivo.
    danadas = crear_filas_danadas(CANTIDAD_FILAS_BUENAS + 1)
    for fila in danadas:
        posicion = random.randint(0, len(filas))
        filas.insert(posicion, fila)

    # Crear la carpeta datos/ si todavía no existe (exist_ok evita el error si ya está).
    os.makedirs(os.path.dirname(RUTA_CSV), exist_ok=True)

    # Escribir el CSV. newline="" evita líneas en blanco extra en Windows;
    # utf-8 deja bien las tildes (categoría, clásico, Joyas).
    try:
        with open(RUTA_CSV, "w", newline="", encoding="utf-8") as archivo:
            # lineterminator="\n": mismo fin de línea en Windows, Mac y Linux, para que
            # Git no marque el CSV como "cambiado" cuando otro compañero lo regenera.
            escritor = csv.writer(archivo, lineterminator="\n")
            escritor.writerow(COLUMNAS)   # primera línea: los nombres de las columnas
            escritor.writerows(filas)     # el resto: una venta por línea
    except OSError as error:
        # Por ejemplo: el CSV está abierto en Excel y Windows no deja sobrescribirlo.
        print(f"No se pudo crear el archivo: {error}")
        print("Cierra el CSV si lo tienes abierto en Excel y vuelve a intentarlo.")
        return

    print(f"Archivo creado: {RUTA_CSV}")
    print(f"Filas buenas: {CANTIDAD_FILAS_BUENAS} | Filas dañadas: {len(danadas)} "
          f"| Total: {len(filas)}")


# Esta condición hace que main() solo corra al ejecutar el archivo directamente
# (python generar_datos.py), y no cuando otro archivo lo importe.
if __name__ == "__main__":
    main()
