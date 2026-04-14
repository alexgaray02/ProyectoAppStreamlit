# #############
# #graficar.py
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import pandas as pd
# from datetime import datetime

# MESES_ORDEN = [
#     "Enero","Febrero","Marzo","Abril","Mayo","Junio",
#     "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
# ]

# AÑO_ACTUAL = datetime.now().year

# # ===============================
# # HELPER: asignar color por año
# # ===============================
# def _colores_por_año(años_serie, color_actual, color_anteriores):
#     return [
#         color_actual if int(a) == AÑO_ACTUAL else color_anteriores
#         for a in años_serie
#     ]


# # ===============================
# # DISPONIBILIDAD (BARRAS)
# # ===============================
# def grafico_disponibilidad(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj):

#     colores = _colores_por_año(df["año"], color_actual, color_anteriores)

#     fig = go.Figure()
#     fig.add_trace(
#         go.Bar(
#             x=x_axis,
#             y=df["disponibilidad"],
#             marker_color=colores,
#             text=["<b>{:.2f}</b>".format(v) if pd.notna(v) else "" for v in df["disponibilidad"]],
#             textposition="outside",
#             textfont=dict(size=12, family="Arial Black")
#         )
#     )

#     max_data = df["disponibilidad"].max() if pd.notna(df["disponibilidad"].max()) else 0
#     max_y = max(100, max_data * 1.1, val_obj * 1.1)

#     # --- LÓGICA DE FILTRADO DE TICKS CERCANOS AL OBJETIVO ---
#     paso = int(max_y / 5) if int(max_y / 5) > 0 else 1
#     ticks_auto = list(range(0, int(max_y) + paso * 2, paso))
#     zona_exclusion = max_y * 0.06
#     ticks_limpios = [t for t in ticks_auto if abs(t - val_obj) > zona_exclusion]

#     if val_obj > 0:
#         fig.add_hline(
#             y=val_obj,
#             line_dash="dot",
#             line_color=color_objetivo,
#             line_width=2,
#             annotation_text=f"<b>{val_obj}</b>",
#             annotation_position="left",
#             annotation=dict(
#                 font=dict(color=color_objetivo, family="Arial Black"), # Se omitió 'size' para usar el default
#                 xanchor="right",
#                 xshift=-5
#             )
#         )

#     fig.update_layout(
#         title={"text": f"<b>Disponibilidad Proceso {proceso_sel}</b>", "x": 0.5},
#         xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
#         yaxis=dict(
#             title=dict(text="<b>Disponibilidad (%)</b>", font=dict(size=16)),
#             tickfont=dict(size=12, family="Arial Black"),
#             range=[0, max_y],
#             tickvals=ticks_limpios # <-- Se inyectan los ticks limpios aquí
#         ),
#         template="simple_white",
#         height=650,
#         width=1400,
#         margin=dict(l=80, r=40, t=100, b=200)
#     )
#     return fig


# # ===============================
# # MTBF 13W (LINEA)
# # ===============================
# def grafico_mtbf13(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj):

#     colores_marker = _colores_por_año(df["año"], color_actual, color_anteriores)

#     posiciones = []
#     for i in range(len(df)):
#         if i == 0:
#             posiciones.append("top center")
#         else:
#             if df["mtbf 13w(h)"].iloc[i] >= df["mtbf 13w(h)"].iloc[i-1]:
#                 posiciones.append("top center")
#             else:
#                 posiciones.append("bottom center")

#     fig = go.Figure()
#     fig.add_trace(
#         go.Scatter(
#             x=x_axis,
#             y=df["mtbf 13w(h)"],
#             mode="lines+markers+text",
#             line=dict(color="black", width=3),
#             marker=dict(
#                 size=10,
#                 color=colores_marker,
#                 line=dict(color="black", width=2)
#             ),
#             text=["<b>{:.1f}</b>".format(v) if pd.notna(v) else "" for v in df["mtbf 13w(h)"]],
#             textposition=posiciones,
#             textfont=dict(size=12)
#         )
#     )

#     max_data = df["mtbf 13w(h)"].max() if pd.notna(df["mtbf 13w(h)"].max()) else 0
#     max_y = max(max_data, val_obj) * 1.15 if max(max_data, val_obj) > 0 else 100

#     # --- LÓGICA DE FILTRADO DE TICKS CERCANOS AL OBJETIVO ---
#     paso = int(max_y / 5) if int(max_y / 5) > 0 else 1
#     ticks_auto = list(range(0, int(max_y) + paso * 2, paso))
#     zona_exclusion = max_y * 0.06
#     ticks_limpios = [t for t in ticks_auto if abs(t - val_obj) > zona_exclusion]

#     if val_obj > 0:
#         fig.add_hline(
#             y=val_obj,
#             line_dash="dot",
#             line_color=color_objetivo,
#             line_width=2,
#             annotation_text=f"<b>{val_obj}</b>",
#             annotation_position="left",
#             annotation=dict(
#                 font=dict(color=color_objetivo, family="Arial Black"),
#                 xanchor="right",
#                 xshift=-5
#             )
#         )

#     fig.update_layout(
#         title={"text": f"<b>MTBF 13W Proceso {proceso_sel}</b>", "x": 0.5},
#         xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
#         yaxis=dict(
#             title=dict(text="<b>MTBF 13W (h)</b>", font=dict(size=16)),
#             tickfont=dict(size=12, family="Arial Black"),
#             range=[0, max_y],
#             tickvals=ticks_limpios # <-- Se inyectan los ticks limpios aquí
#         ),
#         template="simple_white",
#         height=650,
#         width=1400,
#         margin=dict(l=80, r=40, t=100, b=200)
#     )
#     return fig


# # ===============================
# # MTBF 52W (LINEA)
# # ===============================
# def grafico_mtbf52(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj):

#     colores_marker = _colores_por_año(df["año"], color_actual, color_anteriores)

#     posiciones = []
#     for i in range(len(df)):
#         if i == 0:
#             posiciones.append("top center")
#         else:
#             if df["mtbf 52w(h)"].iloc[i] >= df["mtbf 52w(h)"].iloc[i-1]:
#                 posiciones.append("top center")
#             else:
#                 posiciones.append("bottom center")

#     fig = go.Figure()
#     fig.add_trace(
#         go.Scatter(
#             x=x_axis,
#             y=df["mtbf 52w(h)"],
#             mode="lines+markers+text",
#             line=dict(color="black", width=3),
#             marker=dict(
#                 size=10,
#                 color=colores_marker,
#                 line=dict(color="black", width=2)
#             ),
#             text=["<b>{:.1f}</b>".format(v) if pd.notna(v) else "" for v in df["mtbf 52w(h)"]],
#             textposition=posiciones,
#             textfont=dict(size=12)
#         )
#     )

#     max_data = df["mtbf 52w(h)"].max() if pd.notna(df["mtbf 52w(h)"].max()) else 0
#     max_y = max(max_data, val_obj) * 1.15 if max(max_data, val_obj) > 0 else 100

#     # --- LÓGICA DE FILTRADO DE TICKS CERCANOS AL OBJETIVO ---
#     paso = int(max_y / 5) if int(max_y / 5) > 0 else 1
#     ticks_auto = list(range(0, int(max_y) + paso * 2, paso))
#     zona_exclusion = max_y * 0.06
#     ticks_limpios = [t for t in ticks_auto if abs(t - val_obj) > zona_exclusion]

#     if val_obj > 0:
#         fig.add_hline(
#             y=val_obj,
#             line_dash="dot",
#             line_color=color_objetivo,
#             line_width=2,
#             annotation_text=f"<b>{val_obj}</b>",
#             annotation_position="left",
#             annotation=dict(
#                 font=dict(color=color_objetivo, family="Arial Black"),
#                 xanchor="right",
#                 xshift=-5
#             )
#         )

#     fig.update_layout(
#         title={"text": f"<b>MTBF 52W Proceso {proceso_sel}</b>", "x": 0.5},
#         xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
#         yaxis=dict(
#             title=dict(text="<b>MTBF 52W (h)</b>", font=dict(size=16)),
#             tickfont=dict(size=12, family="Arial Black"),
#             range=[0, max_y],
#             tickvals=ticks_limpios # <-- Se inyectan los ticks limpios aquí
#         ),
#         template="simple_white",
#         height=650,
#         width=1400,
#         margin=dict(l=80, r=40, t=100, b=200)
#     )
#     return fig


# # ===============================
# # FUSIONAR (DESCARGA)
# # ===============================
# def fusionar_graficos(fig1, fig2, fig3, proceso_sel, color_objetivo, val_obj_disp, val_obj_mtbf13, val_obj_mtbf52):

#     fig = make_subplots(
#         rows=1, cols=3,
#         subplot_titles=[
#             f"<b>Disponibilidad Proceso {proceso_sel}</b>",
#             f"<b>MTBF 13W Proceso {proceso_sel}</b>",
#             f"<b>MTBF 52W Proceso {proceso_sel}</b>"
#         ]
#     )

#     for trace in fig1.data:
#         fig.add_trace(trace, row=1, col=1)
#     for trace in fig2.data:
#         fig.add_trace(trace, row=1, col=2)
#     for trace in fig3.data:
#         fig.add_trace(trace, row=1, col=3)

#     if val_obj_disp > 0:
#         fig.add_hline(
#             y=val_obj_disp, line_dash="dot", line_color=color_objetivo, line_width=2,
#             annotation_text=f"<b>{val_obj_disp}</b>", annotation_position="left", 
#             annotation=dict(font=dict(color=color_objetivo, family="Arial Black"), xanchor="right", xshift=-5), 
#             row=1, col=1
#         )
#     if val_obj_mtbf13 > 0:
#         fig.add_hline(
#             y=val_obj_mtbf13, line_dash="dot", line_color=color_objetivo, line_width=2,
#             annotation_text=f"<b>{val_obj_mtbf13}</b>", annotation_position="left", 
#             annotation=dict(font=dict(color=color_objetivo, family="Arial Black"), xanchor="right", xshift=-5), 
#             row=1, col=2
#         )
#     if val_obj_mtbf52 > 0:
#         fig.add_hline(
#             y=val_obj_mtbf52, line_dash="dot", line_color=color_objetivo, line_width=2,
#             annotation_text=f"<b>{val_obj_mtbf52}</b>", annotation_position="left", 
#             annotation=dict(font=dict(color=color_objetivo, family="Arial Black"), xanchor="right", xshift=-5), 
#             row=1, col=3
#         )

#     fig.update_layout(
#         template="simple_white",
#         height=600,
#         width=1800,
#         showlegend=False,
#         margin=dict(l=80, r=40, t=100, b=200)
#     )
    
#     # Heredamos el rango Y y los Ticks Limpios de cada gráfico individual
#     if fig1.layout.yaxis.range: 
#         fig.update_yaxes(range=fig1.layout.yaxis.range, tickvals=fig1.layout.yaxis.tickvals, row=1, col=1)
#     if fig2.layout.yaxis.range: 
#         fig.update_yaxes(range=fig2.layout.yaxis.range, tickvals=fig2.layout.yaxis.tickvals, row=1, col=2)
#     if fig3.layout.yaxis.range: 
#         fig.update_yaxes(range=fig3.layout.yaxis.range, tickvals=fig3.layout.yaxis.tickvals, row=1, col=3)

#     return fig


# # ===============================
# # FUNCION PRINCIPAL
# # ===============================
# def graficar_fun(df_filtrado, tipo_doc, proceso_sel, año_inicio, año_fin,
#                  color_actual="#FF0000", color_anteriores="#423B3B", 
#                  color_objetivo="#00205B", val_obj_disp=0, val_obj_mtbf13=0, val_obj_mtbf52=0):

#     if df_filtrado.empty:
#         return None, None, None, None

#     df = df_filtrado.copy()
#     df.columns = df.columns.str.strip().str.lower()

#     df["disponibilidad"] = pd.to_numeric(df["disponibilidad"], errors="coerce")
#     df["mtbf 13w(h)"] = pd.to_numeric(df["mtbf 13w(h)"], errors="coerce")
#     df["mtbf 52w(h)"] = pd.to_numeric(df["mtbf 52w(h)"], errors="coerce")

#     if tipo_doc == "AM":
#         df["mes"] = df["mes"].astype(str).str.strip().str.capitalize()
#         df["mes"] = df["mes"].replace(["Nan", "None"], "").fillna("")
#         orden_meses = [""] + MESES_ORDEN
#         df["mes"] = pd.Categorical(df["mes"], categories=orden_meses, ordered=True)
#         df = df.sort_values(["año", "mes"])
#         x_axis = [df["año"].astype(str), df["mes"]]
#     else:
#         df = df.sort_values("año")
#         df["año"] = df["año"].astype(str)
#         x_axis = df["año"]

#     fig_disp   = grafico_disponibilidad(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj_disp)
#     fig_mtbf13 = grafico_mtbf13(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj_mtbf13)
#     fig_mtbf52 = grafico_mtbf52(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj_mtbf52)
    
#     fig_fusion = fusionar_graficos(fig_disp, fig_mtbf13, fig_mtbf52, proceso_sel, color_objetivo, val_obj_disp, val_obj_mtbf13, val_obj_mtbf52)

#     return fig_disp, fig_mtbf13, fig_mtbf52, fig_fusion

#################################################################



# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import pandas as pd
# from datetime import datetime

# MESES_ORDEN = [
#     "Enero","Febrero","Marzo","Abril","Mayo","Junio",
#     "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
# ]

# AÑO_ACTUAL = datetime.now().year

# # ===============================
# # HELPER: asignar color por año
# # ===============================
# def _colores_por_año(años_serie, color_actual, color_anteriores):
#     return [
#         color_actual if int(a) == AÑO_ACTUAL else color_anteriores
#         for a in años_serie
#     ]


# # ===============================
# # DISPONIBILIDAD (BARRAS)
# # ===============================
# def grafico_disponibilidad(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj):

#     colores = _colores_por_año(df["año"], color_actual, color_anteriores)

#     fig = go.Figure()
#     fig.add_trace(
#         go.Bar(
#             x=x_axis,
#             y=df["disponibilidad"],
#             marker_color=colores,
#             text=["<b>{:.2f}</b>".format(v) if pd.notna(v) else "" for v in df["disponibilidad"]],
#             textposition="outside",
#             textfont=dict(size=12, family="Arial Black")
#         )
#     )

#     # --- LÓGICA CORREGIDA PARA LÍMITE 100 ---
#     max_data = df["disponibilidad"].max() if pd.notna(df["disponibilidad"].max()) else 0
#     max_y = 100 if max(max_data, val_obj) <= 100 else max(max_data, val_obj) * 1.1

#     # Ticks estándar y limpios
#     if max_y <= 100:
#         ticks_auto = [0, 20, 40, 60, 80, 100]
#     else:
#         paso = int(max_y / 5) if int(max_y / 5) > 0 else 1
#         ticks_auto = list(range(0, int(max_y) + paso, paso))

#     zona_exclusion = max_y * 0.05
    
#     # --- FILTRADO DE TICKS SEGÚN TU REGLA ---
#     ticks_limpios = []
#     for t in ticks_auto:
#         if t == val_obj:
#             continue # Si el tick es exactamente el objetivo (ej. 100), lo quitamos para no duplicar.
#         if t == 100:
#             ticks_limpios.append(t) # Siempre forzamos que salga el 100 si el objetivo no es 100.
#         elif abs(t - val_obj) > zona_exclusion:
#             ticks_limpios.append(t) # Para los demás (0, 20, 40...), los quitamos solo si chocan con el objetivo.

#     if val_obj > 0:
#         fig.add_hline(
#             y=val_obj,
#             line_dash="dot",
#             line_color=color_objetivo,
#             line_width=2,
#             annotation_text=f"<b>{val_obj}</b>",
#             annotation_position="left",
#             annotation=dict(
#                 font=dict(color=color_objetivo, family="Arial Black"), 
#                 xanchor="right",
#                 xshift=-5
#             )
#         )

#     fig.update_layout(
#         title={"text": f"<b>Disponibilidad Proceso {proceso_sel}</b>", "x": 0.5},
#         xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
#         yaxis=dict(
#             title=dict(text="<b>Disponibilidad (%)</b>", font=dict(size=16)),
#             tickfont=dict(size=12, family="Arial Black"),
#             range=[0, max_y],
#             tickvals=ticks_limpios # <-- Se inyectan los ticks perfectamente calculados
#         ),
#         template="simple_white",
#         height=650,
#         width=1400,
#         margin=dict(l=80, r=40, t=100, b=200)
#     )
#     return fig


# # ===============================
# # MTBF 13W (LINEA)
# # ===============================
# def grafico_mtbf13(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj):

#     colores_marker = _colores_por_año(df["año"], color_actual, color_anteriores)

#     posiciones = []
#     for i in range(len(df)):
#         if i == 0:
#             posiciones.append("top center")
#         else:
#             if df["mtbf 13w(h)"].iloc[i] >= df["mtbf 13w(h)"].iloc[i-1]:
#                 posiciones.append("top center")
#             else:
#                 posiciones.append("bottom center")

#     fig = go.Figure()
#     fig.add_trace(
#         go.Scatter(
#             x=x_axis,
#             y=df["mtbf 13w(h)"],
#             mode="lines+markers+text",
#             line=dict(color="black", width=3),
#             marker=dict(
#                 size=10,
#                 color=colores_marker,
#                 line=dict(color="black", width=2)
#             ),
#             text=["<b>{:.1f}</b>".format(v) if pd.notna(v) else "" for v in df["mtbf 13w(h)"]],
#             textposition=posiciones,
#             textfont=dict(size=12)
#         )
#     )

#     max_data = df["mtbf 13w(h)"].max() if pd.notna(df["mtbf 13w(h)"].max()) else 0
#     max_y = max(max_data, val_obj) * 1.15 if max(max_data, val_obj) > 0 else 100

#     paso = int(max_y / 5) if int(max_y / 5) > 0 else 1
#     ticks_auto = list(range(0, int(max_y) + paso * 2, paso))
#     zona_exclusion = max_y * 0.06
#     ticks_limpios = [t for t in ticks_auto if abs(t - val_obj) > zona_exclusion]

#     if val_obj > 0:
#         fig.add_hline(
#             y=val_obj,
#             line_dash="dot",
#             line_color=color_objetivo,
#             line_width=2,
#             annotation_text=f"<b>{val_obj}</b>",
#             annotation_position="left",
#             annotation=dict(
#                 font=dict(color=color_objetivo, family="Arial Black"),
#                 xanchor="right",
#                 xshift=-5
#             )
#         )

#     fig.update_layout(
#         title={"text": f"<b>MTBF 13W Proceso {proceso_sel}</b>", "x": 0.5},
#         xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
#         yaxis=dict(
#             title=dict(text="<b>MTBF 13W (h)</b>", font=dict(size=16)),
#             tickfont=dict(size=12, family="Arial Black"),
#             range=[0, max_y],
#             tickvals=ticks_limpios
#         ),
#         template="simple_white",
#         height=650,
#         width=1400,
#         margin=dict(l=80, r=40, t=100, b=200)
#     )
#     return fig


# # ===============================
# # MTBF 52W (LINEA)
# # ===============================
# def grafico_mtbf52(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj):

#     colores_marker = _colores_por_año(df["año"], color_actual, color_anteriores)

#     posiciones = []
#     for i in range(len(df)):
#         if i == 0:
#             posiciones.append("top center")
#         else:
#             if df["mtbf 52w(h)"].iloc[i] >= df["mtbf 52w(h)"].iloc[i-1]:
#                 posiciones.append("top center")
#             else:
#                 posiciones.append("bottom center")

#     fig = go.Figure()
#     fig.add_trace(
#         go.Scatter(
#             x=x_axis,
#             y=df["mtbf 52w(h)"],
#             mode="lines+markers+text",
#             line=dict(color="black", width=3),
#             marker=dict(
#                 size=10,
#                 color=colores_marker,
#                 line=dict(color="black", width=2)
#             ),
#             text=["<b>{:.1f}</b>".format(v) if pd.notna(v) else "" for v in df["mtbf 52w(h)"]],
#             textposition=posiciones,
#             textfont=dict(size=12)
#         )
#     )

#     max_data = df["mtbf 52w(h)"].max() if pd.notna(df["mtbf 52w(h)"].max()) else 0
#     max_y = max(max_data, val_obj) * 1.15 if max(max_data, val_obj) > 0 else 100

#     paso = int(max_y / 5) if int(max_y / 5) > 0 else 1
#     ticks_auto = list(range(0, int(max_y) + paso * 2, paso))
#     zona_exclusion = max_y * 0.06
#     ticks_limpios = [t for t in ticks_auto if abs(t - val_obj) > zona_exclusion]

#     if val_obj > 0:
#         fig.add_hline(
#             y=val_obj,
#             line_dash="dot",
#             line_color=color_objetivo,
#             line_width=2,
#             annotation_text=f"<b>{val_obj}</b>",
#             annotation_position="left",
#             annotation=dict(
#                 font=dict(color=color_objetivo, family="Arial Black"),
#                 xanchor="right",
#                 xshift=-5
#             )
#         )

#     fig.update_layout(
#         title={"text": f"<b>MTBF 52W Proceso {proceso_sel}</b>", "x": 0.5},
#         xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
#         yaxis=dict(
#             title=dict(text="<b>MTBF 52W (h)</b>", font=dict(size=16)),
#             tickfont=dict(size=12, family="Arial Black"),
#             range=[0, max_y],
#             tickvals=ticks_limpios
#         ),
#         template="simple_white",
#         height=650,
#         width=1400,
#         margin=dict(l=80, r=40, t=100, b=200)
#     )
#     return fig


# # ===============================
# # FUSIONAR (DESCARGA)
# # ===============================
# def fusionar_graficos(fig1, fig2, fig3, proceso_sel, color_objetivo, val_obj_disp, val_obj_mtbf13, val_obj_mtbf52):

#     fig = make_subplots(
#         rows=1, cols=3,
#         subplot_titles=[
#             f"<b>Disponibilidad Proceso {proceso_sel}</b>",
#             f"<b>MTBF 13W Proceso {proceso_sel}</b>",
#             f"<b>MTBF 52W Proceso {proceso_sel}</b>"
#         ]
#     )

#     for trace in fig1.data:
#         fig.add_trace(trace, row=1, col=1)
#     for trace in fig2.data:
#         fig.add_trace(trace, row=1, col=2)
#     for trace in fig3.data:
#         fig.add_trace(trace, row=1, col=3)

#     if val_obj_disp > 0:
#         fig.add_hline(
#             y=val_obj_disp, line_dash="dot", line_color=color_objetivo, line_width=2,
#             annotation_text=f"<b>{val_obj_disp}</b>", annotation_position="left", 
#             annotation=dict(font=dict(color=color_objetivo, family="Arial Black"), xanchor="right", xshift=-5), 
#             row=1, col=1
#         )
#     if val_obj_mtbf13 > 0:
#         fig.add_hline(
#             y=val_obj_mtbf13, line_dash="dot", line_color=color_objetivo, line_width=2,
#             annotation_text=f"<b>{val_obj_mtbf13}</b>", annotation_position="left", 
#             annotation=dict(font=dict(color=color_objetivo, family="Arial Black"), xanchor="right", xshift=-5), 
#             row=1, col=2
#         )
#     if val_obj_mtbf52 > 0:
#         fig.add_hline(
#             y=val_obj_mtbf52, line_dash="dot", line_color=color_objetivo, line_width=2,
#             annotation_text=f"<b>{val_obj_mtbf52}</b>", annotation_position="left", 
#             annotation=dict(font=dict(color=color_objetivo, family="Arial Black"), xanchor="right", xshift=-5), 
#             row=1, col=3
#         )

#     fig.update_layout(
#         template="simple_white",
#         height=600,
#         width=1800,
#         showlegend=False,
#         margin=dict(l=80, r=40, t=100, b=200)
#     )
    
#     if fig1.layout.yaxis.range: 
#         fig.update_yaxes(range=fig1.layout.yaxis.range, tickvals=fig1.layout.yaxis.tickvals, row=1, col=1)
#     if fig2.layout.yaxis.range: 
#         fig.update_yaxes(range=fig2.layout.yaxis.range, tickvals=fig2.layout.yaxis.tickvals, row=1, col=2)
#     if fig3.layout.yaxis.range: 
#         fig.update_yaxes(range=fig3.layout.yaxis.range, tickvals=fig3.layout.yaxis.tickvals, row=1, col=3)

#     return fig


# # ===============================
# # FUNCION PRINCIPAL
# # ===============================
# def graficar_fun(df_filtrado, tipo_doc, proceso_sel, año_inicio, año_fin,
#                  color_actual="#FF0000", color_anteriores="#423B3B", 
#                  color_objetivo="#00205B", val_obj_disp=0, val_obj_mtbf13=0, val_obj_mtbf52=0):

#     if df_filtrado.empty:
#         return None, None, None, None

#     df = df_filtrado.copy()
#     df.columns = df.columns.str.strip().str.lower()

#     df["disponibilidad"] = pd.to_numeric(df["disponibilidad"], errors="coerce")
#     df["mtbf 13w(h)"] = pd.to_numeric(df["mtbf 13w(h)"], errors="coerce")
#     df["mtbf 52w(h)"] = pd.to_numeric(df["mtbf 52w(h)"], errors="coerce")

#     if tipo_doc == "AM":
#         df["mes"] = df["mes"].astype(str).str.strip().str.capitalize()
#         df["mes"] = df["mes"].replace(["Nan", "None"], "").fillna("")
#         orden_meses = [""] + MESES_ORDEN
#         df["mes"] = pd.Categorical(df["mes"], categories=orden_meses, ordered=True)
#         df = df.sort_values(["año", "mes"])
#         x_axis = [df["año"].astype(str), df["mes"]]
#     else:
#         df = df.sort_values("año")
#         df["año"] = df["año"].astype(str)
#         x_axis = df["año"]

#     fig_disp   = grafico_disponibilidad(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj_disp)
#     fig_mtbf13 = grafico_mtbf13(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj_mtbf13)
#     fig_mtbf52 = grafico_mtbf52(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj_mtbf52)
    
#     fig_fusion = fusionar_graficos(fig_disp, fig_mtbf13, fig_mtbf52, proceso_sel, color_objetivo, val_obj_disp, val_obj_mtbf13, val_obj_mtbf52)

#     return fig_disp, fig_mtbf13, fig_mtbf52, fig_fusion











#################################################################
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
def grafico_disponibilidad(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj):

    colores = _colores_por_año(df["año"], color_actual, color_anteriores)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=x_axis,
            y=df["disponibilidad"],
            marker_color=colores,
            text=["<b>{:.2f}</b>".format(v) if pd.notna(v) else "" for v in df["disponibilidad"]],
            textposition="outside",
            textfont=dict(size=12, family="Arial Black")
        )
    )

    max_data = df["disponibilidad"].max() if pd.notna(df["disponibilidad"].max()) else 0
    max_y = 100 if max(max_data, val_obj) <= 100 else max(max_data, val_obj) * 1.1

    if max_y <= 100:
        ticks_auto = [0, 20, 40, 60, 80, 100]
    else:
        paso = int(max_y / 5) if int(max_y / 5) > 0 else 1
        ticks_auto = list(range(0, int(max_y) + paso, paso))

    zona_exclusion = max_y * 0.05
    ticks_limpios = []
    
    for t in ticks_auto:
        if t == val_obj:
            continue
        if t == 100:
            ticks_limpios.append(t)
        elif abs(t - val_obj) > zona_exclusion:
            ticks_limpios.append(t)

    # --- NUEVA LÓGICA: Inyectar el objetivo directamente en el Eje Y ---
    final_tickvals = ticks_limpios.copy()
    final_ticktext = [str(t) for t in ticks_limpios]
    
    if val_obj > 0:
        final_tickvals.append(val_obj)
        # Usamos HTML para pintar solo este número en el eje
        final_ticktext.append(f"<span style='color:{color_objetivo};'><b>{val_obj}</b></span>")
        
        # Trazamos la línea sin el texto flotante problemático
        fig.add_hline(
            y=val_obj,
            line_dash="dot",
            line_color=color_objetivo,
            line_width=2
        )

    fig.update_layout(
        title={"text": f"<b>Disponibilidad Proceso {proceso_sel}</b>", "x": 0.5, "pad": {"b": 20}},
        xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
        yaxis=dict(
            title=dict(text="<b>Disponibilidad (%)</b>", font=dict(size=16)),
            tickfont=dict(size=12, family="Arial Black"),
            range=[0, max_y + 10], 
            tickvals=final_tickvals, # Usamos los valores calculados
            ticktext=final_ticktext  # Usamos los textos coloreados
        ),
        template="simple_white",
        height=650,
        width=1400,
        margin=dict(l=80, r=40, t=130, b=200)
    )
    return fig


# ===============================
# MTBF 13W (LINEA)
# ===============================
def grafico_mtbf13(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj):

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
            text=["<b>{:.1f}</b>".format(v) if pd.notna(v) else "" for v in df["mtbf 13w(h)"]],
            textposition=posiciones,
            textfont=dict(size=12)
        )
    )

    max_data = df["mtbf 13w(h)"].max() if pd.notna(df["mtbf 13w(h)"].max()) else 0
    max_y = max(max_data, val_obj) * 1.25 if max(max_data, val_obj) > 0 else 100

    paso = int(max_y / 5) if int(max_y / 5) > 0 else 1
    ticks_auto = list(range(0, int(max_y) + paso * 2, paso))
    zona_exclusion = max_y * 0.06
    
    # Filtramos ticks cercanos y evitamos duplicar si el auto-tick cae exacto en el objetivo
    ticks_limpios = [t for t in ticks_auto if abs(t - val_obj) > zona_exclusion and t != val_obj]

    # --- Inyectar el objetivo en el Eje Y ---
    final_tickvals = ticks_limpios.copy()
    final_ticktext = [str(t) for t in ticks_limpios]
    
    if val_obj > 0:
        final_tickvals.append(val_obj)
        final_ticktext.append(f"<span style='color:{color_objetivo};'><b>{val_obj}</b></span>")
        
        fig.add_hline(
            y=val_obj,
            line_dash="dot",
            line_color=color_objetivo,
            line_width=2
        )

    fig.update_layout(
        title={"text": f"<b>MTBF 13W Proceso {proceso_sel}</b>", "x": 0.5, "pad": {"b": 20}},
        xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
        yaxis=dict(
            title=dict(text="<b>MTBF 13W (h)</b>", font=dict(size=16)),
            tickfont=dict(size=12, family="Arial Black"),
            range=[0, max_y],
            tickvals=final_tickvals,
            ticktext=final_ticktext
        ),
        template="simple_white",
        height=650,
        width=1400,
        margin=dict(l=80, r=40, t=130, b=200)
    )
    return fig


# ===============================
# MTBF 52W (LINEA)
# ===============================
def grafico_mtbf52(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj):

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
            text=["<b>{:.1f}</b>".format(v) if pd.notna(v) else "" for v in df["mtbf 52w(h)"]],
            textposition=posiciones,
            textfont=dict(size=12)
        )
    )

    max_data = df["mtbf 52w(h)"].max() if pd.notna(df["mtbf 52w(h)"].max()) else 0
    max_y = max(max_data, val_obj) * 1.25 if max(max_data, val_obj) > 0 else 100

    paso = int(max_y / 5) if int(max_y / 5) > 0 else 1
    ticks_auto = list(range(0, int(max_y) + paso * 2, paso))
    zona_exclusion = max_y * 0.06
    
    ticks_limpios = [t for t in ticks_auto if abs(t - val_obj) > zona_exclusion and t != val_obj]

    # --- Inyectar el objetivo en el Eje Y ---
    final_tickvals = ticks_limpios.copy()
    final_ticktext = [str(t) for t in ticks_limpios]
    
    if val_obj > 0:
        final_tickvals.append(val_obj)
        final_ticktext.append(f"<span style='color:{color_objetivo};'><b>{val_obj}</b></span>")
        
        fig.add_hline(
            y=val_obj,
            line_dash="dot",
            line_color=color_objetivo,
            line_width=2
        )

    fig.update_layout(
        title={"text": f"<b>MTBF 52W Proceso {proceso_sel}</b>", "x": 0.5, "pad": {"b": 20}},
        xaxis=dict(tickfont=dict(size=12, family="Arial Black")),
        yaxis=dict(
            title=dict(text="<b>MTBF 52W (h)</b>", font=dict(size=16)),
            tickfont=dict(size=12, family="Arial Black"),
            range=[0, max_y],
            tickvals=final_tickvals,
            ticktext=final_ticktext
        ),
        template="simple_white",
        height=650,
        width=1400,
        margin=dict(l=80, r=40, t=130, b=200)
    )
    return fig


# ===============================
# FUSIONAR (DESCARGA)
# ===============================
def fusionar_graficos(fig1, fig2, fig3, proceso_sel, color_objetivo, val_obj_disp, val_obj_mtbf13, val_obj_mtbf52):

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

    # Añadimos solo las líneas punteadas limpias (sin texto flotante)
    if val_obj_disp > 0:
        fig.add_hline(y=val_obj_disp, line_dash="dot", line_color=color_objetivo, line_width=2, row=1, col=1)
    if val_obj_mtbf13 > 0:
        fig.add_hline(y=val_obj_mtbf13, line_dash="dot", line_color=color_objetivo, line_width=2, row=1, col=2)
    if val_obj_mtbf52 > 0:
        fig.add_hline(y=val_obj_mtbf52, line_dash="dot", line_color=color_objetivo, line_width=2, row=1, col=3)

    fig.update_layout(
        template="simple_white",
        height=600,
        width=1800,
        showlegend=False,
        margin=dict(l=80, r=40, t=130, b=200) 
    )
    
    for annotation in fig['layout']['annotations']:
        annotation['yshift'] = 20 
    
    # Heredamos explícitamente tanto el rango como los Ticks y el TEXTO de los Ticks (con colores)
    if fig1.layout.yaxis.range: 
        fig.update_yaxes(range=fig1.layout.yaxis.range, tickvals=fig1.layout.yaxis.tickvals, ticktext=fig1.layout.yaxis.ticktext, row=1, col=1)
    if fig2.layout.yaxis.range: 
        fig.update_yaxes(range=fig2.layout.yaxis.range, tickvals=fig2.layout.yaxis.tickvals, ticktext=fig2.layout.yaxis.ticktext, row=1, col=2)
    if fig3.layout.yaxis.range: 
        fig.update_yaxes(range=fig3.layout.yaxis.range, tickvals=fig3.layout.yaxis.tickvals, ticktext=fig3.layout.yaxis.ticktext, row=1, col=3)

    return fig


# ===============================
# FUNCION PRINCIPAL
# ===============================
def graficar_fun(df_filtrado, tipo_doc, proceso_sel, año_inicio, año_fin,
                 color_actual="#FF0000", color_anteriores="#423B3B", 
                 color_objetivo="#00205B", val_obj_disp=0, val_obj_mtbf13=0, val_obj_mtbf52=0):

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

    fig_disp   = grafico_disponibilidad(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj_disp)
    fig_mtbf13 = grafico_mtbf13(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj_mtbf13)
    fig_mtbf52 = grafico_mtbf52(df, proceso_sel, x_axis, color_actual, color_anteriores, color_objetivo, val_obj_mtbf52)
    
    fig_fusion = fusionar_graficos(fig_disp, fig_mtbf13, fig_mtbf52, proceso_sel, color_objetivo, val_obj_disp, val_obj_mtbf13, val_obj_mtbf52)

    return fig_disp, fig_mtbf13, fig_mtbf52, fig_fusion