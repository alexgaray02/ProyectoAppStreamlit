#########################################################################


# graficar.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime

MESES_ORDEN = [
    "Enero","Febrero","Marzo","Abril","Mayo","Junio",
    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
]

AÑO_ACTUAL = datetime.now().year

# ===============================
# HELPER: asignar color por año
# ===============================
def _colores_por_año(años_serie, color_actual, color_anteriores):
    return [
        color_actual if int(a) == AÑO_ACTUAL else color_anteriores
        for a in años_serie
    ]


# ===============================
# DISPONIBILIDAD (BARRAS)
# ===============================
def grafico_disponibilidad(df, proceso_sel, x_axis, color_actual, color_anteriores):

    colores = _colores_por_año(df["año"], color_actual, color_anteriores)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=x_axis,
            y=df["disponibilidad"],
            marker_color=colores,
            text=["<b>{:.2f}</b>".format(v) for v in df["disponibilidad"]],
            textposition="outside",
            textfont=dict(size=12, family="Arial Black")
        )
    )

    fig.update_layout(
        title={"text": f"<b>Disponibilidad Proceso {proceso_sel}</b>", "x": 0.5},
        xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
        yaxis=dict(
            title=dict(text="<b>Disponibilidad (%)</b>", font=dict(size=16)),
            tickfont=dict(size=12, family="Arial Black"),
            range=[0, 100]
        ),
        template="simple_white",
        height=650,
        width=1400,
        margin=dict(l=80, r=40, t=100, b=200)
    )
    return fig


# ===============================
# MTBF 13W (LINEA)
# ===============================
def grafico_mtbf13(df, proceso_sel, x_axis, color_actual, color_anteriores):

    colores_marker = _colores_por_año(df["año"], color_actual, color_anteriores)

    posiciones = []
    for i in range(len(df)):
        if i == 0:
            posiciones.append("top center")
        else:
            if df["mtbf 13w(h)"].iloc[i] >= df["mtbf 13w(h)"].iloc[i-1]:
                posiciones.append("top center")
            else:
                posiciones.append("bottom center")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_axis,
            y=df["mtbf 13w(h)"],
            mode="lines+markers+text",
            line=dict(color="black", width=3),
            marker=dict(
                size=10,
                color=colores_marker,
                line=dict(color="black", width=2)
            ),
            text=["<b>{:.1f}</b>".format(v) for v in df["mtbf 13w(h)"]],
            textposition=posiciones,
            textfont=dict(size=12)
        )
    )

    fig.update_layout(
        title={"text": f"<b>MTBF 13W Proceso {proceso_sel}</b>", "x": 0.5},
        xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
        yaxis=dict(
            title=dict(text="<b>MTBF 13W (h)</b>", font=dict(size=16)),
            tickfont=dict(size=12, family="Arial Black")
        ),
        template="simple_white",
        height=650,
        width=1400,
        margin=dict(l=80, r=40, t=100, b=200)
    )
    return fig


# ===============================
# MTBF 52W (LINEA)
# ===============================
def grafico_mtbf52(df, proceso_sel, x_axis, color_actual, color_anteriores):

    colores_marker = _colores_por_año(df["año"], color_actual, color_anteriores)

    posiciones = []
    for i in range(len(df)):
        if i == 0:
            posiciones.append("top center")
        else:
            if df["mtbf 52w(h)"].iloc[i] >= df["mtbf 52w(h)"].iloc[i-1]:
                posiciones.append("top center")
            else:
                posiciones.append("bottom center")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_axis,
            y=df["mtbf 52w(h)"],
            mode="lines+markers+text",
            line=dict(color="black", width=3),
            marker=dict(
                size=10,
                color=colores_marker,
                line=dict(color="black", width=2)
            ),
            text=["<b>{:.1f}</b>".format(v) for v in df["mtbf 52w(h)"]],
            textposition=posiciones,
            textfont=dict(size=12)
        )
    )

    fig.update_layout(
        title={"text": f"<b>MTBF 52W Proceso {proceso_sel}</b>", "x": 0.5},
        xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
        yaxis=dict(
            title=dict(text="<b>MTBF 52W (h)</b>", font=dict(size=16)),
            tickfont=dict(size=12, family="Arial Black")
        ),
        template="simple_white",
        height=650,
        width=1400,
        margin=dict(l=80, r=40, t=100, b=200)
    )
    return fig


# ===============================
# FUSIONAR (DESCARGA)
# ===============================
def fusionar_graficos(fig1, fig2, fig3, proceso_sel):

    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=[
            f"<b>Disponibilidad Proceso {proceso_sel}</b>",
            f"<b>MTBF 13W Proceso {proceso_sel}</b>",
            f"<b>MTBF 52W Proceso {proceso_sel}</b>"
        ]
    )

    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)
    for trace in fig3.data:
        fig.add_trace(trace, row=1, col=3)

    fig.update_layout(
        template="simple_white",
        height=600,
        width=1800,
        showlegend=False,
        margin=dict(l=80, r=40, t=100, b=200)
    )
    return fig


# ===============================
# FUNCION PRINCIPAL
# ===============================
def graficar_fun(df_filtrado, tipo_doc, proceso_sel, año_inicio, año_fin,
                 color_actual="#FF0000", color_anteriores="#423B3B"):

    if df_filtrado.empty:
        return None, None, None, None

    df = df_filtrado.copy()
    df.columns = df.columns.str.strip().str.lower()

    df["disponibilidad"] = pd.to_numeric(df["disponibilidad"], errors="coerce")
    df["mtbf 13w(h)"] = pd.to_numeric(df["mtbf 13w(h)"], errors="coerce")
    df["mtbf 52w(h)"] = pd.to_numeric(df["mtbf 52w(h)"], errors="coerce")

    if tipo_doc == "AM":
        df["mes"] = df["mes"].astype(str).str.strip().str.capitalize()
        df["mes"] = df["mes"].replace(["Nan", "None"], "").fillna("")
        orden_meses = [""] + MESES_ORDEN
        df["mes"] = pd.Categorical(df["mes"], categories=orden_meses, ordered=True)
        df = df.sort_values(["año", "mes"])
        x_axis = [df["año"].astype(str), df["mes"]]
    else:
        df = df.sort_values("año")
        df["año"] = df["año"].astype(str)
        x_axis = df["año"]

    fig_disp   = grafico_disponibilidad(df, proceso_sel, x_axis, color_actual, color_anteriores)
    fig_mtbf13 = grafico_mtbf13(df, proceso_sel, x_axis, color_actual, color_anteriores)
    fig_mtbf52 = grafico_mtbf52(df, proceso_sel, x_axis, color_actual, color_anteriores)
    fig_fusion = fusionar_graficos(fig_disp, fig_mtbf13, fig_mtbf52, proceso_sel)

    return fig_disp, fig_mtbf13, fig_mtbf52, fig_fusion