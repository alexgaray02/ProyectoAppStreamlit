
# ################################################################
# # filtros.py
# import streamlit as st
# import pandas as pd

# MESES_ORDEN = [
#     "Enero","Febrero","Marzo","Abril","Mayo","Junio",
#     "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
# ]

# MESES_MAP = {m: i+1 for i, m in enumerate(MESES_ORDEN)}


# def funfiltro(df, tipo_doc):

#     df = df.copy()
#     df.columns = df.columns.str.strip().str.lower()

#     proceso_sel = []
#     año_inicio = None
#     año_fin = None

#     if "año" in df.columns:
#         df["año"] = pd.to_numeric(df["año"], errors="coerce")

#     # ==========================================
#     # FILTRO AÑO + MES
#     # ==========================================
#     if tipo_doc == "AM":

#         st.sidebar.header("Filtro Fecha")

#         años = sorted(df["año"].dropna().unique())

#         st.sidebar.subheader("Fecha Inicio")
#         col1, col2 = st.sidebar.columns(2)
#         with col1:
#             año_inicio = st.selectbox("Año", años, key="am_año_inicio")
#         with col2:
#             mes_inicio = st.selectbox("Mes", MESES_ORDEN, key="am_mes_inicio")

#         st.sidebar.subheader("Fecha Fin")
#         col3, col4 = st.sidebar.columns(2)
#         with col3:
#             año_fin = st.selectbox("Año ", años, key="am_año_fin")
#         with col4:
#             mes_fin = st.selectbox("Mes ", MESES_ORDEN, key="am_mes_fin")

#         if "fecha" not in df.columns:
#             mes_num = df["mes"].map(MESES_MAP)
#             mes_num = mes_num.fillna(1)
#             df["fecha"] = pd.to_datetime(
#                 dict(year=df["año"], month=mes_num, day=1),
#                 errors="coerce"
#             )

#         fecha_inicio = pd.Timestamp(año_inicio, MESES_MAP[mes_inicio], 1)
#         fecha_fin = pd.Timestamp(año_fin, MESES_MAP[mes_fin], 1)

#         if fecha_inicio <= fecha_fin:
#             df = df[(df["fecha"] >= fecha_inicio) & (df["fecha"] <= fecha_fin)]
#         else:
#             st.sidebar.warning("⚠ Fecha inicio no puede ser mayor que fecha fin")

#     # ==========================================
#     # SOLO AÑO
#     # ==========================================
#     elif tipo_doc == "A":

#         st.sidebar.header("Filtro por Año")
#         años = sorted(df["año"].dropna().unique())

#         if años:
#             año_inicio = st.sidebar.selectbox("Año Inicio", años, index=0, key="a_inicio")
#             año_fin = st.sidebar.selectbox("Año Fin", años, index=len(años)-1, key="a_fin")

#             if año_inicio <= año_fin:
#                 df = df[(df["año"] >= año_inicio) & (df["año"] <= año_fin)]
#             else:
#                 st.sidebar.warning("⚠ Año inicio no puede ser mayor que año fin")

#     if "proceso" in df.columns:
#         st.sidebar.header("Proceso")
#         procesos = sorted(df["proceso"].dropna().unique())
#         proceso_sel = st.sidebar.selectbox("Selecciona Proceso", procesos, key="proceso_select")
#         if proceso_sel:
#             df = df[df["proceso"] == proceso_sel]

#     # ==========================================
#     # SELECTOR DE COLORES
#     # ==========================================
#     st.sidebar.divider()
#     st.sidebar.header("🎨 Estilo de Gráficos")

#     color_actual = st.sidebar.color_picker(
#         "Color año actual", "#D42F2F",
#         # "#FF0000",
#         key="color_año_actual"
#     )
#     color_anteriores = st.sidebar.color_picker(
#         "Color años anteriores", "#000000",
#         # "#423B3B",
#         key="color_años_anteriores"
#     )

#     return df, proceso_sel, año_inicio, año_fin, color_actual, color_anteriores


###############################################################################



################################################################
# filtros.py
import streamlit as st
import pandas as pd

MESES_ORDEN = [
    "Enero","Febrero","Marzo","Abril","Mayo","Junio",
    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
]

MESES_MAP = {m: i+1 for i, m in enumerate(MESES_ORDEN)}
MESES_INV = {v: k for k, v in MESES_MAP.items()}  # {1: "Enero", 2: "Febrero", ...}


def funfiltro(df, tipo_doc):

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    proceso_sel = []
    año_inicio = None
    año_fin = None

    if "año" in df.columns:
        df["año"] = pd.to_numeric(df["año"], errors="coerce")

    # ==========================================
    # FILTRO AÑO + MES
    # ==========================================
    if tipo_doc == "AM":

        st.sidebar.header("Filtro Fecha")

        años = sorted(df["año"].dropna().unique())

        # ── Detectar mes real de inicio y fin ──────────────────────────
        año_real_min = int(años[0])
        año_real_max = int(años[-1])

        # Mes más temprano del primer año disponible  → default Fecha Inicio
        meses_en_año_min = df[df["año"] == año_real_min]["mes"].map(MESES_MAP).dropna()
        mes_real_inicio_num = int(meses_en_año_min.min()) if not meses_en_año_min.empty else 1

        # Mes más tardío del último año disponible → default Fecha Fin
        meses_en_año_max = df[df["año"] == año_real_max]["mes"].map(MESES_MAP).dropna()
        mes_real_fin_num = int(meses_en_año_max.max()) if not meses_en_año_max.empty else 12

        mes_real_inicio = MESES_INV[mes_real_inicio_num]   # ej. "Mayo"
        mes_real_fin    = MESES_INV[mes_real_fin_num]       # ej. "Enero"
        # ──────────────────────────────────────────────────────────────

        st.sidebar.subheader("Fecha Inicio")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            año_inicio = st.selectbox(
                "Año", años,
                index=0,                                        # primer año
                key="am_año_inicio"
            )
        with col2:
            mes_inicio = st.selectbox(
                "Mes", MESES_ORDEN,
                index=MESES_ORDEN.index(mes_real_inicio),       # ej. Mayo → index 4
                key="am_mes_inicio"
            )

        st.sidebar.subheader("Fecha Fin")
        col3, col4 = st.sidebar.columns(2)
        with col3:
            año_fin = st.selectbox(
                "Año ", años,
                index=len(años) - 1,                            # último año
                key="am_año_fin"
            )
        with col4:
            mes_fin = st.selectbox(
                "Mes ", MESES_ORDEN,
                index=MESES_ORDEN.index(mes_real_fin),          # ej. Enero → index 0
                key="am_mes_fin"
            )

        if "fecha" not in df.columns:
            mes_num = df["mes"].map(MESES_MAP).fillna(1)
            df["fecha"] = pd.to_datetime(
                dict(year=df["año"], month=mes_num, day=1),
                errors="coerce"
            )

        fecha_inicio = pd.Timestamp(año_inicio, MESES_MAP[mes_inicio], 1)
        fecha_fin    = pd.Timestamp(año_fin,    MESES_MAP[mes_fin],    1)

        if fecha_inicio <= fecha_fin:
            df = df[(df["fecha"] >= fecha_inicio) & (df["fecha"] <= fecha_fin)]
        else:
            st.sidebar.warning("⚠ Fecha inicio no puede ser mayor que fecha fin")

    # ==========================================
    # SOLO AÑO
    # ==========================================
    elif tipo_doc == "A":

        st.sidebar.header("Filtro por Año")
        años = sorted(df["año"].dropna().unique())

        if años:
            año_inicio = st.sidebar.selectbox(
                "Año Inicio", años,
                index=0,                    # primer año
                key="a_inicio"
            )
            año_fin = st.sidebar.selectbox(
                "Año Fin", años,
                index=len(años) - 1,        # último año
                key="a_fin"
            )

            if año_inicio <= año_fin:
                df = df[(df["año"] >= año_inicio) & (df["año"] <= año_fin)]
            else:
                st.sidebar.warning("⚠ Año inicio no puede ser mayor que año fin")

    if "proceso" in df.columns:
        st.sidebar.header("Proceso")
        procesos = sorted(df["proceso"].dropna().unique())
        proceso_sel = st.sidebar.selectbox("Selecciona Proceso", procesos, key="proceso_select")
        if proceso_sel:
            df = df[df["proceso"] == proceso_sel]

    # ==========================================
    # SELECTOR DE COLORES
    # ==========================================
    st.sidebar.divider()
    st.sidebar.header("🎨 Estilo de Gráficos")

    color_actual = st.sidebar.color_picker(
        "Color año actual", "#D42F2F",
        key="color_año_actual"
    )
    color_anteriores = st.sidebar.color_picker(
        "Color años anteriores", "#000000",
        key="color_años_anteriores"
    )

    return df, proceso_sel, año_inicio, año_fin, color_actual, color_anteriores