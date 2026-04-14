###############################################################################


###############################################################
# filtros.py
import streamlit as st
import pandas as pd

MESES_ORDEN = [
    "Enero","Febrero","Marzo","Abril","Mayo","Junio",
    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
]

MESES_MAP = {m: i+1 for i, m in enumerate(MESES_ORDEN)}
MESES_INV = {v: k for k, v in MESES_MAP.items()}


def normalizar_mes(serie):
    """Normaliza la columna mes para evitar fallos por encoding, espacios o capitalización."""
    return (
        serie.astype(str)
        .str.strip()
        .str.capitalize()
        .replace("", pd.NA)
        .replace("Nan", pd.NA)
        .map(MESES_MAP)
        .dropna()
    )


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
        año_real_min = int(años[0])
        año_real_max = int(años[-1])

        # ── Detectar mes real de inicio y fin desde los datos ──────────
        tiene_mes = (
            "mes" in df.columns
            and df["mes"].notna().any()
            and (df["mes"].astype(str).str.strip() != "").any()
        )

        if tiene_mes:
            # Solo filas con mes válido reconocido
            mes_normalizado = df["mes"].astype(str).str.strip().str.capitalize()
            df_con_mes = df[mes_normalizado.isin(MESES_MAP)]

            meses_año_min = normalizar_mes(df_con_mes[df_con_mes["año"] == año_real_min]["mes"])
            mes_real_inicio_num = int(meses_año_min.min()) if not meses_año_min.empty else 1

            meses_año_max = normalizar_mes(df_con_mes[df_con_mes["año"] == año_real_max]["mes"])
            mes_real_fin_num = int(meses_año_max.max()) if not meses_año_max.empty else 12
        else:
            mes_real_inicio_num = 1
            mes_real_fin_num    = 12

        mes_real_inicio = MESES_INV.get(mes_real_inicio_num, "Enero")
        mes_real_fin    = MESES_INV.get(mes_real_fin_num,    "Diciembre")
        # ──────────────────────────────────────────────────────────────

        st.sidebar.subheader("Fecha Inicio")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            año_inicio = st.selectbox(
                "Año", años,
                index=0,
                key="am_año_inicio"
            )
        with col2:
            mes_inicio = st.selectbox(
                "Mes", MESES_ORDEN,
                index=MESES_ORDEN.index(mes_real_inicio),
                key="am_mes_inicio"
            )

        st.sidebar.subheader("Fecha Fin")
        col3, col4 = st.sidebar.columns(2)
        with col3:
            año_fin = st.selectbox(
                "Año ", años,
                index=len(años) - 1,
                key="am_año_fin"
            )
        with col4:
            mes_fin = st.selectbox(
                "Mes ", MESES_ORDEN,
                index=MESES_ORDEN.index(mes_real_fin),
                key="am_mes_fin"
            )

        # Construir columna fecha si no existe
        if "fecha" not in df.columns:
            mes_num = normalizar_mes(df["mes"]).reindex(df.index)
            mes_num = mes_num.fillna(1)
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
                index=0,
                key="a_inicio"
            )
            año_fin = st.sidebar.selectbox(
                "Año Fin", años,
                index=len(años) - 1,
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

    # # ==========================================
    # # SELECTOR DE COLORES
    # # ==========================================
    # st.sidebar.divider()
    # st.sidebar.header("🎨 Estilo de Gráficos")

    # color_actual = st.sidebar.color_picker(
    #     "Color año actual", "#D42F2F",
    #     key="color_año_actual"
    # )
    # color_anteriores = st.sidebar.color_picker(
    #     "Color años anteriores", "#000000",
    #     key="color_años_anteriores"
    # )

    # return df, proceso_sel, año_inicio, año_fin, color_actual, color_anteriores

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
    
    # AÑADIDO: Color de la línea de objetivo
    color_objetivo = st.sidebar.color_picker(
        "Color línea objetivo", "#00205B",
        key="color_linea_objetivo"
    )

    # AÑADIDO: Retornar color_objetivo al final
    return df, proceso_sel, año_inicio, año_fin, color_actual, color_anteriores, color_objetivo






##########################################################################


