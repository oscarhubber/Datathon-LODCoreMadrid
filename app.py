# app.py
"""LodCORE Madrid - Municipality Finder
Main Streamlit application for ranking municipalities by accessibility and quality of life.
"""

import numpy as np
import streamlit as st

from config.styles import apply_styles
from config.constants import CRITERIA, BENEFIT_COLUMNS, COST_COLUMNS
from core.data_loader import load_data, load_placeholder_images
from core.accessibility import compute_accessibility_hours
from core.ahp import preferences_to_weights, preferences_to_matrix, compute_cr
from core.scoring import normalize_criteria, compute_scores, equal_weights
from ui.questionnaire import render_questionnaire
from ui.map_view import render_map_view
from ui.list_view import render_list_view
from ui.details_view import render_details
from ui.sensitivity import render_sensitivity


def main() -> None:
    """Main application entry point."""
    # Apply styles and page config
    apply_styles()
    
    # Handle view switching state
    if "view_selector" not in st.session_state:
        st.session_state["view_selector"] = "🗺️ Mapa de municipios"
    
    if st.session_state.get("switch_view_to"):
        st.session_state["view_selector"] = st.session_state["switch_view_to"]
        st.session_state["switch_view_to"] = None
    
    if st.session_state.get("clear_comparison_only"):
        for key in ["comparison_municipality", "comparison_selector_in_panel", "clear_comparison_only"]:
            st.session_state.pop(key, None)
    
    # Header
    st.markdown('<h1 class="main-header">🏘️ Living on the Edge</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="tagline">Encuentra tu municipio ideal en la Comunidad de Madrid según tu estilo de vida, tu familia y tus prioridades.</p>',
        unsafe_allow_html=True,
    )
    
    # Load data
    df_raw, gdf_raw = load_data()
    images = load_placeholder_images()
    
    # Render questionnaire and get user preferences
    prefs = render_questionnaire(df_raw)
    
    # Filter by population
    df = df_raw.copy()
    if "IDE_PoblacionTotal" in df.columns:
        df = df[(df["IDE_PoblacionTotal"] >= prefs["pop_min"]) & 
                (df["IDE_PoblacionTotal"] <= prefs["pop_max"])].copy()
    
    # Compute accessibility
    acc_df = compute_accessibility_hours(
        df=df,
        w_car=prefs["w_car"],
        w_sport=prefs["w_sport"],
        w_hospital=prefs["w_hospital"],
        edu_has_kids=prefs["edu_has_kids"],
        edu_variant=prefs["edu_variant"],
        edu_levels=prefs["edu_levels"],
        edu_acc_weight=prefs["edu_trade"],
    )
    
    df_scored = df.merge(acc_df[["codigo", "AccessibilityHoursMonthly"]], on="codigo", how="left")
    
    # Normalize criteria
    norm_df = normalize_criteria(df_scored, BENEFIT_COLUMNS, COST_COLUMNS)
    
    # Compute weights via AHP
    try:
        inverted_ranks = [11 - r for r in prefs["ranks"]]
        w_vec = preferences_to_weights(np.array(inverted_ranks, dtype=float), mode="ranking")
        weights = {CRITERIA[i]: float(w_vec[i]) for i in range(len(CRITERIA))}
        
        A = preferences_to_matrix(np.array(inverted_ranks, dtype=float), "ranking")
        cr = compute_cr(A)
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Calidad de pesos")
        if cr < 0.10:
            st.sidebar.success(f"✅ Consistencia: {cr:.3f} (buena)")
        else:
            st.sidebar.warning(f"⚠️ Consistencia: {cr:.3f} (ajustado automáticamente)")
            st.sidebar.caption("Tus preferencias tenían pequeñas inconsistencias. Los pesos se han corregido matemáticamente.")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {e}")
        st.sidebar.info("Usando pesos iguales como respaldo.")
        weights = equal_weights(CRITERIA)
    
    # Compute scores
    with st.spinner("Calculando puntuaciones de municipios..."):
        scores_df = compute_scores(norm_df, weights)
    
    # Prepare map data
    with st.spinner("Preparando mapa..."):
        gdf = gdf_raw.merge(
            scores_df[["codigo", "Nombre", "Score", "weighted_score", "AccessibilityHoursMonthly",
                      "IDE_PoblacionTotal", "IDE_PrecioPorMetroCuadrado"] +
                     [c for c in scores_df.columns if c.startswith("NORM_") or c.startswith("CONTRIB_")]],
            on=["Nombre"],
            how="inner",
        )
    
    # Show municipality details if selected
    if "selected_municipality" in st.session_state:
        st.markdown("---")
        render_details(st.session_state["selected_municipality"], images, scores_df)
    
    # Main view selector
    view_option = st.radio(
        "Selecciona vista:",
        ["🗺️ Mapa de municipios", "📋 Lista de municipios"],
        horizontal=True,
        key="view_selector",
    )
    
    # CSV download
    st.download_button(
        label="📥 Descargar resultados (CSV)",
        data=scores_df.to_csv(index=False).encode("utf-8"),
        file_name="lodcore_municipios.csv",
        mime="text/csv",
        help="Descarga todos los municipios con sus puntuaciones y detalles"
    )
    
    # Render selected view
    if view_option == "🗺️ Mapa de municipios":
        render_map_view(gdf, scores_df)
    else:
        render_list_view(scores_df, images)
    
    # Sensitivity analysis
    render_sensitivity(scores_df, weights, norm_df, compute_scores)


if __name__ == "__main__":
    main()
