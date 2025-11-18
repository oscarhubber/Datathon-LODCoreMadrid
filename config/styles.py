# config/styles.py
"""CSS styles and page configuration for LodCORE app."""

import streamlit as st

CSS_STYLES = """
<style>
:root {
    --color-slate: #3D517B;
    --color-primary: #568EE2;
    --color-navy: #051C33;
    --color-teal: #6FB5BA;
    --color-sand: #DFD1B6;
    --color-lilac: #A59FD0;
    --color-error: #C33241;
    --color-success: #377F86;
    --color-warning: #C35309;
}

/* Light mode background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, var(--background-color) 0%, var(--color-sand) 100%);
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #0e1117 0%, #1a1d29 100%);
    }
}

.main-header {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--color-primary), var(--color-slate));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 1rem;
}

.tagline {
    color: var(--text-color);
    font-style: italic;
    text-align: center;
    margin-top: 0;
    margin-bottom: 1.5rem;
    opacity: 0.8;
}


# /* Municipality cards - theme aware */
# .municipality-card {
#     background: linear-gradient(135deg, #568EE2 0%, #6FB5BA 100%);
#     padding: 0.06rem;
#     border-radius: 2px;
#     box-shadow: 0 2px 2px rgba(0, 0, 0, 0.1);
#     margin: 0.5rem 0;
#     border-left: 3px solid #3D517B;
#     transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
#     min-height: 2px;
#     max-height: 3px;
# }
# .municipality-card:hover {
#     transform: translateY(-2px);
#     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
# }


.score-badge {
    background: linear-gradient(90deg, var(--color-primary), var(--color-teal));
    color: #ffffff !important;
    padding: 0.5rem 1rem;
    border-radius: 999px;
    font-weight: 600;
    display: inline-block;
    margin: 0.3rem 0;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    font-size: 0.9rem;
}

.municipality-name {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--color-primary);
    margin-bottom: 0.8rem;
}

.detail-panel {
    background: var(--background-color);
    border: 1px solid var(--color-primary);
    border-radius: 15px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.concept-icon {
    font-size: 1.3rem;
    margin-right: 0.5rem;
}

/* Buttons - theme aware with white text */
.stButton > button {
    background: linear-gradient(90deg, var(--color-primary), var(--color-teal)) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 999px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    color: #ffffff !important;
}
.stButton > button:active,
.stButton > button:focus {
    color: #ffffff !important;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(90deg, var(--color-success), var(--color-teal)) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 999px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
}
.stDownloadButton > button:hover {
    color: #ffffff !important;
}

.comparison-header {
    background: var(--color-slate);
    color: #ffffff;
    padding: 0.8rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 1rem;
    font-weight: 600;
}

.plot-container {
    border-radius: 16px;
    overflow: hidden;
}

/* Radio buttons - ensure visibility */
[data-testid="stRadio"] label {
    color: var(--text-color) !important;
}

/* Selectbox - ensure visibility */
[data-testid="stSelectbox"] label {
    color: var(--text-color) !important;
}

/* Number input - ensure visibility */
[data-testid="stNumberInput"] label {
    color: var(--text-color) !important;
}

/* Slider - ensure visibility */
[data-testid="stSlider"] label {
    color: var(--text-color) !important;
}

/* Multiselect - ensure visibility */
[data-testid="stMultiSelect"] label {
    color: var(--text-color) !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--color-navy) 0%, #1a1d29 100%);
}

[data-testid="stSidebar"] * {
    color: #F9FAFB !important;
}

/* Sidebar selectbox - fix selected option visibility */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: #F9FAFB !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] input {
    color: #F9FAFB !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #F9FAFB !important;
}

/* Sidebar multiselect */
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: var(--color-primary) !important;
    color: #ffffff !important;
}

/* Sidebar number input - fix all elements */
[data-testid="stSidebar"] input[type="number"] {
    color: #051C33 !important;
    background-color: #F9FAFB !important;
}

[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
    color: #F9FAFB !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
}

[data-testid="stSidebar"] [data-testid="stNumberInput"] button:hover {
    background-color: rgba(255, 255, 255, 0.2) !important;
}

[data-testid="stSidebar"] [data-testid="stNumberInput"] svg {
    fill: #F9FAFB !important;
}


/* Sidebar slider */
[data-testid="stSidebar"] [data-baseweb="slider"] {
    color: #F9FAFB !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(90deg, var(--color-primary), var(--color-teal)) !important;
    color: #ffffff !important;
}

/* Expander - theme aware */
[data-testid="stExpander"] {
    background: var(--background-color);
    border: 1px solid var(--color-primary);
    border-radius: 10px;
}

/* Dataframe - ensure readability */
[data-testid="stDataFrame"] {
    background: var(--background-color);
}

/* Metric - theme aware */
[data-testid="stMetric"] {
    background: var(--background-color);
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid rgba(86, 142, 226, 0.3);
}
</style>
"""


def apply_styles() -> None:
    """Apply page configuration and custom CSS styles."""
    st.set_page_config(
        page_title="Living on the Edge",
        page_icon="🏘️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
