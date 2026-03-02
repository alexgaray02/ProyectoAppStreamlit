# filtros.py
import streamlit as st
import pandas as pd

MESES_ORDEN = [
    "Enero","Febrero","Marzo","Abril","Mayo","Junio",
    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
]

MESES_MAP = {m: i+1 for i, m in enumerate(MESES_ORDEN)}


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

        # Fecha inicio
        st.sidebar.subheader("Fecha Inicio")
        col1, col2 = st.sidebar.columns(2)

        with col1:
            año_inicio = st.selectbox("Año", años, key="am_año_inicio")

        with col2:
            mes_inicio = st.selectbox("Mes", MESES_ORDEN, key="am_mes_inicio")

        # Fecha fin
        st.sidebar.subheader("Fecha Fin")
        col3, col4 = st.sidebar.columns(2)

        with col3:
            año_fin = st.selectbox("Año ", años, key="am_año_fin")

        with col4:
            mes_fin = st.selectbox("Mes ", MESES_ORDEN, key="am_mes_fin")

        # Crear fecha si no existe
        if "fecha" not in df.columns:
            df["fecha"] = pd.to_datetime(
                dict(
                    year=df["año"],
                    month=df["mes"].map(MESES_MAP),
                    day=1
                ),
                errors="coerce"
            )

        fecha_inicio = pd.Timestamp(año_inicio, MESES_MAP[mes_inicio], 1)
        fecha_fin = pd.Timestamp(año_fin, MESES_MAP[mes_fin], 1)

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
                "Año Inicio",
                años,
                index=0,
                key="a_inicio"
            )

            año_fin = st.sidebar.selectbox(
                "Año Fin",
                años,
                index=len(años)-1,
                key="a_fin"
            )

            if año_inicio <= año_fin:
                df = df[(df["año"] >= año_inicio) & (df["año"] <= año_fin)]
            else:
                st.sidebar.warning("⚠ Año inicio no puede ser mayor que año fin")

    if "proceso" in df.columns:

        st.sidebar.header("Proceso")

        procesos = sorted(df["proceso"].dropna().unique())

        proceso_sel = st.sidebar.selectbox(
            "Selecciona Proceso",
            procesos,
            key="proceso_select"
        )

        if proceso_sel:
            df = df[df["proceso"] == proceso_sel]

            
    return df, proceso_sel, año_inicio, año_fin