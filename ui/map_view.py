# ui/map_view.py
"""Map visualization component."""

import geopandas as gpd
import pandas as pd
import plotly.express as px
import streamlit as st


def create_heatmap(gdf: gpd.GeoDataFrame):
    """Create choropleth map of municipalities.
    
    Args:
        gdf: GeoDataFrame with weighted_score column
        
    Returns:
        Plotly figure
    """
    gdf_plot = gdf.to_crs(epsg=4326)

    fig = px.choropleth_mapbox(
        gdf_plot,
        geojson=gdf_plot.geometry.__geo_interface__,
        locations=gdf_plot.index,
        color="weighted_score",
        color_continuous_scale=["#DFD1B6", "#6FB5BA", "#568EE2", "#3D517B"],
        range_color=[gdf_plot["weighted_score"].min(), gdf_plot["weighted_score"].max()],
        mapbox_style="open-street-map",
        zoom=8,
        center={"lat": 40.4168, "lon": -3.7038},
        opacity=0.7,
        title="Mapa de municipios según tu perfil",
        custom_data=[gdf_plot["Nombre"]],
        labels={"weighted_score": "Puntuación (más alto = mejor)"},
    )

    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>Puntuación: %{z:.1f}<extra></extra>"
    )
    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        clickmode="event+select",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig

# New function:
def render_map_view(gdf: gpd.GeoDataFrame, scores_df: pd.DataFrame) -> None:
    """Render map view with click handling.
    
    Args:
        gdf: GeoDataFrame with municipality boundaries and scores
        scores_df: DataFrame with municipality scores
    """
    if len(gdf) == 0:
        st.warning("No hay municipios disponibles para mostrar.")
        return

    # Check if in comparison mode
    in_comparison_mode = st.session_state.get("view_selector") == "⚖️ Comparación"
    
    if in_comparison_mode:
        st.markdown("**Consejo:** haz clic en un municipio del mapa para añadirlo a la comparación 👇")
    else:
        st.markdown("**Consejo:** haz clic en un municipio del mapa para ver más detalles abajo 👇")
    
    suppress = st.session_state.pop("suppress_map_selection", False)

    fig = create_heatmap(gdf)
    event = st.plotly_chart(
        fig,
        key="heatmap",
        width='stretch',
        on_select="rerun",
        selection_mode="points",
    )

    if not suppress and event and event.selection and event.selection["point_indices"]:
        idx = event.selection["point_indices"][0]
        clicked_name = gdf.iloc[idx]["Nombre"]
        selected_row = scores_df[scores_df["Nombre"] == clicked_name].iloc[0]

        if in_comparison_mode:
            # Add to comparison list
            if "comparison_municipalities" not in st.session_state:
                st.session_state["comparison_municipalities"] = []
            
            comparison_list = st.session_state["comparison_municipalities"]
            
            if selected_row["codigo"] not in comparison_list and len(comparison_list) < 4:
                comparison_list.append(selected_row["codigo"])
                st.session_state["comparison_municipalities"] = comparison_list
                st.rerun()
            elif selected_row["codigo"] in comparison_list:
                st.info(f"✓ {clicked_name} ya está en la comparación")
            else:
                st.warning("⚠️ Máximo 4 municipios en comparación. Elimina uno para añadir otro.")
        else:
            # Show details inline
            st.session_state["selected_municipality"] = selected_row
            st.session_state["details_origin"] = "map"
    
    # Show details inline in map view
    if "selected_municipality" in st.session_state and st.session_state.get("details_origin") == "map":
        st.markdown("---")
        from ui.details_view import render_details
        from core.data_loader import load_placeholder_images
        images = load_placeholder_images()
        render_details(st.session_state["selected_municipality"], images, scores_df)


