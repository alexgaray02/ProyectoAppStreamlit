def plotly_scroll(fig, height=700, export_filename="grafico"):
    """
    Renderiza Plotly con tamaño fijo garantizado.
    - Scroll horizontal en pantallas pequeñas
    - Exportación siempre al tamaño real del gráfico (sin depender de pantalla)
    """
    fig_width  = fig.layout.width  or 1400
    fig_height = fig.layout.height or 650

    html = pio.to_html(
        fig,
        full_html=False,
        include_plotlyjs="cdn",
        config={
            "toImageButtonOptions": {
                "format": "png",
                "filename": export_filename,
                "height": fig_height,
                "width": fig_width,
                "scale": 3          # resolución 3x → alta calidad
            },
            "displayModeBar": True,
            "scrollZoom": False
        }
    )

    wrapped = f"""
        <div style="
            overflow-x: auto;
            overflow-y: hidden;
            width: 100%;
            min-width: 0;
        ">
            <div style="width: {fig_width}px; min-width: {fig_width}px;">
                {html}
            </div>
        </div>
    """
    components.html(wrapped, height=height, scrolling=False)