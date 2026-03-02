import streamlit as st
import pandas as pd
import plotly.express as px
from tipodoc import documento  
from filtros import funfiltro
from graficar import graficar_fun

# 1. Configuración de página con estilo
st.set_page_config(page_title="Dashboard de Confiabilidad", layout="wide", page_icon="📊")

# 2. CSS personalizado para mejorar la estética
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stExpander"] {
        border: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        background-color: white;
    }
    .stPlotlyChart {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: Carga y Configuración ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1622/1622857.png", width=80) # Icono decorativo #"
    st.title("Configuración")
    archivo = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])
    
    if archivo:
        st.success("Archivo cargado correctamente")
        st.divider()

# --- CUERPO PRINCIPAL ---
if archivo is not None:
    df, tipo_doc = documento(archivo)
    
    # Encabezado dinámico
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.title("📊 Panel de Visualización") #Dashboard de Visualización
        st.caption(f"Documento detectado: **{tipo_doc}**")
    
    # Filtros dentro de un expansor para limpiar la vista
    with st.expander("🔍 Ajustar Filtros de Datos", expanded=True):
        df_filtrado, proceso_sel, año_inicio, año_fin = funfiltro(df, tipo_doc)

    # Tabs para organizar la información
    tab1, tab2, tab3 = st.tabs(["📈 Gráficos Principales", "📝 Resumen Ejecutivo", "📋 Datos Crudos"])

    with tab1:
        st.subheader("Análisis de Indicadores")
        fig_disp, fig_mtbf13, fig_mtbf52, fig_fusion = graficar_fun(df_filtrado, tipo_doc, proceso_sel, año_inicio, año_fin)

        # Organización de gráficos en rejilla
        c1, c2 = st.columns(2)
        
        if fig_disp:
            with c1:
                st.plotly_chart(fig_disp, use_container_width=True)
        
        if fig_mtbf13:
            with c2:
                st.plotly_chart(fig_mtbf13, use_container_width=True)

        if fig_mtbf52:
            st.plotly_chart(fig_mtbf52, use_container_width=True)

    with tab2:
        st.subheader("Resumen de Gestión")
        if fig_fusion:
            # Una vista más limpia para el resumen
            st.plotly_chart(
                fig_fusion,
                use_container_width=True,
                config={
                    "toImageButtonOptions": {
                        "format": "png",
                        "filename": "indicadores_confiabilidad",
                        "height": 600,
                        "width": 1800,
                        "scale": 3
                    }
                }
            )
        else:
            st.info("No hay datos suficientes para generar el resumen.")

    with tab3:
        st.subheader("Explorador de Datos")
        st.dataframe(df_filtrado, use_container_width=True, height=400)
        
        # Botón de descarga rápido
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV filtrado", data=csv, file_name="datos_filtrados.csv", mime="text/csv")

# else:
#     # Estado inicial: Mensaje de bienvenida elegante
#     st.info("👋 Bienvenid@. Por favor, sube un archivo Excel en el panel lateral para comenzar el análisis.")

else:
    # Contenedor principal de bienvenida
    with st.container():
        st.markdown("<br>", unsafe_allow_html=True) # Espaciado
        
        # Título y Hero Section
        col_logo, col_text = st.columns([1, 4])
        with col_logo:
            st.image("https://cdn-icons-png.flaticon.com/512/2328/2328966.png", width=120) #https://cdn-icons-png.flaticon.com/512/4205/4205511.png
        with col_text:
            st.title("Bienvenido al Portal de Confiabilidad")
            st.subheader("Transforma tus datos de mantenimiento en decisiones estratégicas.")

        st.divider()

        # Guía de pasos rápidos en 3 columnas
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("### 1. Carga\nSube tu archivo `.xlsx` desde el panel lateral izquierdo.")
        with c2:
            st.info("### 2. Filtra\nSelecciona el proceso, año y tipo de documento a analizar.")
        with c3:
            st.info("### 3. Visualiza\nObtén gráficos de Disponibilidad, MTBF y resúmenes automáticos.")

        # Tip de formato (Muy útil para evitar errores del usuario)
        with st.expander("📌 Requisitos del archivo Excel", expanded=True):
            st.write("""
            Para que el sistema procese la información correctamente, asegúrate de que:
            * El archivo contenga las columnas según tipo documento **AM** (Año-Mes) o **A** (Año).
            * No existan filas vacías al inicio del documento y estar en la primera hoja.
            * El formato estándar columnas **Tipo AM**:
            * [Proceso] [Año] [Mes] [Disponibilidad] [MTBF 13W(h)] [MTBF 52W(h)].
            * El formato estándar columnas **Tipo A**:
            * [Proceso] [Año] [Disponibilidad] [MTBF 13W(h)] [MTBF 52W(h)].
            """)
