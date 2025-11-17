# core/accessibility.py
"""Accessibility computation: monthly commute hours from user preferences."""

import numpy as np
import pandas as pd
import streamlit as st
from typing import Dict, List, Optional, Literal

from config.constants import ACC_COLUMNS, edu_level_to_key


@st.cache_data
def compute_accessibility_hours(
    df: pd.DataFrame,
    w_car: float,
    w_sport: float,
    w_hospital: float,
    edu_has_kids: bool,
    edu_variant: Optional[Literal["public", "pubpriv"]],
    edu_levels: List[str],
    edu_acc_weight: float,
) -> pd.DataFrame:
    """Compute monthly accessibility hours per municipality.
    
    Aggregates round-trip travel time across essential services weighted by
    user preferences and visit frequency.
    
    Args:
        df: Municipality dataset
        w_car: Car usage weight [0,1] (0=only PT, 1=only car)
        w_sport: Sports frequency weight [0,1]
        w_hospital: Hospital usage weight [0,1]
        edu_has_kids: Whether to include education travel
        edu_variant: School type ('public' or 'pubpriv')
        edu_levels: Education stages to include
        edu_acc_weight: Education accessibility weight [0,1]
        
    Returns:
        DataFrame with AccessibilityHoursMonthly column
    """
    out = df[["codigo", "Nombre"]].copy()
    total = np.zeros(len(df), dtype=float)

    def blend_minutes(col_car: str, col_pt: str) -> np.ndarray:
        mc = df[col_car].astype(float)
        mp = df[col_pt].astype(float) if col_pt in df.columns else mc
        return w_car * mc + (1.0 - w_car) * mp

    def add_hours(key: str, minutes_one_way: np.ndarray, visits_per_month: float, weight: float = 1.0) -> None:
        nonlocal total
        hours = weight * visits_per_month * (2.0 * minutes_one_way) / 60.0
        out[f"hrs_{key}"] = hours
        total += hours

    # Supermarkets (8 visits/month, essential)
    mins_super = blend_minutes(
        ACC_COLUMNS["supermarket"]["coche"],
        ACC_COLUMNS["supermarket"]["TransportePublico"],
    )
    add_hours("supermarket", mins_super, 8.0, 1.0)

    # Gas stations (2 visits/month, car-dependent)
    mins_gas = df[ACC_COLUMNS["gas"]["coche"]].astype(float)
    add_hours("gas", mins_gas, 2.0, max(0.0, min(1.0, w_car)))

    # Sports facilities (4 visits/month)
    mins_sport = blend_minutes(
        ACC_COLUMNS["sport"]["coche"],
        ACC_COLUMNS["sport"]["TransportePublico"],
    )
    add_hours("sport", mins_sport, 4.0, max(0.0, min(1.0, w_sport)))

    # Healthcare: GP (0.25/month) + Pharmacy (1/month)
    mins_gp = blend_minutes(
        ACC_COLUMNS["gp"]["coche"],
        ACC_COLUMNS["gp"]["TransportePublico"],
    )
    add_hours("gp", mins_gp, 0.25, max(0.0, min(1.0, w_hospital)))

    mins_pharm = blend_minutes(
        ACC_COLUMNS["pharmacy"]["coche"],
        ACC_COLUMNS["pharmacy"]["TransportePublico"],
    )
    add_hours("pharmacy", mins_pharm, 1.0, max(0.0, min(1.0, w_hospital)))

    # Education (2 visits/month per level)
    if edu_has_kids and edu_variant in ("public", "pubpriv") and edu_levels and edu_acc_weight > 0.0:
        per_level = 1.0 / len(edu_levels)
        for level in edu_levels:
            svc_key = edu_level_to_key(level, edu_variant)
            cols = ACC_COLUMNS[svc_key]
            mins = blend_minutes(cols["coche"], cols["TransportePublico"])
            add_hours(
                f"edu_{level.lower()}",
                mins,
                2.0,
                per_level * edu_acc_weight,
            )

    out["AccessibilityHoursMonthly"] = total
    return out
