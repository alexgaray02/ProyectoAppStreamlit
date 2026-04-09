import streamlit as st


def plotly_scroll(fig, height=700, export_filename="grafico"):
    fig_width  = fig.layout.width  or 1400
    fig_height = fig.layout.height or 650

    # Inyectar CSS para que el contenedor de Streamlit no limite el ancho
    st.markdown("""
        <style>
        [data-testid="stIFrame"] {
            width: 100% !important;
            min-width: 100% !important;
        }
        section[data-testid="stMain"] > div {
            max-width: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    html = pio.to_html(
        fig,
        full_html=True,          # <-- full_html=True para iframe independiente
        include_plotlyjs="cdn",
        config={
            "toImageButtonOptions": {
                "format": "png",
                "filename": export_filename,
                "height": fig_height,
                "width": fig_width,
                "scale": 3
            },
            "displayModeBar": True,
            "scrollZoom": False
        }
    )

    # Envolver con scroll horizontal dentro del iframe
    html_scroll = html.replace(
        "<body>",
        f"""<body style="margin:0; padding:0; overflow-x:auto; overflow-y:hidden;">
        <div style="width:{fig_width}px;">"""
    ).replace("</body>", "</div></body>")

    components.html(html_scroll, height=height, scrolling=True)



