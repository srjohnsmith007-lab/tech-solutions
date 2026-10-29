"""
grafica.py  ·  Ticket 3: La gráfica

Contiene la función crear_grafica(categorias, valores, ruta), que guarda una
gráfica de barras interactiva (Plotly) en un archivo HTML.

Se usa desde reporte.py, pero también se puede probar sola:
    python grafica.py
"""

import os

import plotly.graph_objects as go

# Datos del cliente para el título. Si cambia el cliente o el mes, se cambian aquí.
NOMBRE_NEGOCIO = "LuxuryCo"
MES = "septiembre de 2026"

# Color de marca del cliente: dorado oscuro para las barras, gris para el texto.
COLOR_BARRAS = "#B8860B"
COLOR_TEXTO = "#333333"


def formato_pesos(numero):
    """Convierte 22800000 en '$22.800.000' (punto como separador de miles)."""
    # f"{numero:,.0f}" da '22,800,000'; luego cambiamos las comas por puntos.
    return "$" + f"{numero:,.0f}".replace(",", ".")


def crear_grafica(categorias, valores, ruta):
    """Guarda una gráfica de barras interactiva en 'ruta' (un archivo .html).

    categorias: lista con los nombres, por ejemplo ["Relojes", "Joyas"]
    valores:    lista con el valor de cada categoría, en el mismo orden
    ruta:       dónde guardar el archivo, por ejemplo "salida/grafica.html"
    No devuelve nada: solo crea el archivo.
    """
    # Si las listas no tienen el mismo largo o están vacías, no hay gráfica que hacer.
    if not categorias or len(categorias) != len(valores):
        print("No se pudo crear la gráfica: las listas están vacías o no coinciden.")
        return

    # 1) Ordenar de mayor a menor. zip junta (valor, categoría) para que cada
    #    categoría se mueva junto con su valor al ordenar.
    pares = sorted(zip(valores, categorias), reverse=True)
    valores_ordenados = [valor for valor, _ in pares]
    categorias_ordenadas = [categoria for _, categoria in pares]

    # 2) El total sirve para calcular el porcentaje que muestra el mouse.
    total = sum(valores_ordenados)
    porcentajes = [valor / total * 100 if total else 0 for valor in valores_ordenados]

    # 3) Texto que va encima de cada barra, con formato de pesos.
    textos = [formato_pesos(valor) for valor in valores_ordenados]

    # 4) Información que aparece al pasar el mouse: categoría, valor y porcentaje.
    #    customdata lleva el valor ya formateado y el porcentaje de cada barra.
    datos_hover = [[formato_pesos(v), f"{p:.1f}"] for v, p in zip(valores_ordenados, porcentajes)]

    figura = go.Figure(
        go.Bar(
            x=categorias_ordenadas,
            y=valores_ordenados,
            text=textos,
            textposition="outside",          # el valor queda encima de la barra
            marker_color=COLOR_BARRAS,       # un solo color de marca, sin leyenda repetida
            customdata=datos_hover,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Valor: %{customdata[0]}<br>"
                "Del total: %{customdata[1]}%"
                "<extra></extra>"            # quita el recuadro con el nombre de la serie
            ),
        )
    )

    figura.update_layout(
        template="plotly_white",             # fondo limpio, sin cuadrícula pesada
        # Título y subtítulo con el negocio y el mes (el <sup> hace el texto más pequeño).
        title=dict(
            text=f"Ventas por categoría · {NOMBRE_NEGOCIO}"
                 f"<br><sup>Reporte de {MES} · Total: {formato_pesos(total)}</sup>",
            x=0.5,                           # centrado
        ),
        xaxis_title="Categoría",             # ejes con nombre
        yaxis_title="Valor vendido (pesos)",
        showlegend=False,                    # no hace falta leyenda: el eje X ya nombra cada barra
        font=dict(family="Arial, sans-serif", size=14, color=COLOR_TEXTO),  # fuente legible
        yaxis=dict(tickformat=",.0f", range=[0, max(valores_ordenados) * 1.15]),  # espacio para el texto
    )

    # Crear la carpeta de salida si no existe (por ejemplo "salida/").
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)

    # include_plotlyjs="cdn": el HTML pesa poco, pero necesita internet para abrirse.
    figura.write_html(ruta, include_plotlyjs="cdn")
    print(f"Gráfica guardada en: {ruta}")


# Prueba rápida: solo corre con "python grafica.py", no cuando reporte.py la importa.
if __name__ == "__main__":
    crear_grafica(
        ["Relojes", "Joyas", "Gafas", "Bolsos", "Perfumes", "Billeteras"],
        [22800000, 14940000, 13160000, 12300000, 11800000, 3180000],
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "salida", "grafica.html"),
    )
