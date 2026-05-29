import streamlit as st
import pandas as pd
from utils.db import get_trend_data

TREND_FIELDS = {
    # Levels
    "lvl_ug_spt":        "Level — UG SPT (cm)",
    "lvl_grd_spt":       "Level — Grd SPT (cm)",
    "lvl_r1":            "Level — R1 (cm)",
    "lvl_r2":            "Level — R2 (cm)",
    "lvl_r3":            "Level — R3 (cm)",
    "lvl_r4":            "Level — R4 (cm)",
    "lvl_r5":            "Level — R5 (cm)",
    "lvl_r7":            "Level — R7 (cm)",
    "lvl_r8":            "Level — R8 (cm)",
    "lvl_mlt01":         "Level — MLT 01 (cm)",
    "lvl_mlt02":         "Level — MLT 02 (cm)",
    "lvl_mlt03":         "Level — MLT 03 (cm)",
    "lvl_old_znso4":     "Level — Old ZnSO₄ (cm)",
    "lvl_new_znso4":     "Level — New ZnSO₄ (cm)",
    "lvl_acid_storage":  "Level — Acid Storage (cm)",
    "lvl_acid_day_tank": "Level — Acid Day Tank (cm)",
    "lvl_water":         "Level — Water Tank (cm)",
    # Chemicals
    "acid_r1":           "Acid — R1 (ltr)",
    "acid_r2":           "Acid — R2 (ltr)",
    "acid_r3":           "Acid — R3 (ltr)",
    "acid_ug_spt":       "Acid — UG SPT (ltr)",
    "acid_grd_spt":      "Acid — Grd SPT (ltr)",
    "zn_r4":             "Zn Dust — R4 (kg)",
    "zn_r5":             "Zn Dust — R5 (kg)",
    "zn_r6":             "Zn Dust — R6 (kg)",
    "zn_r7":             "Zn Dust — R7 (kg)",
    "pat_kg":            "PAT (kg)",
    "lead_acetate_kg":   "Lead Acetate (kg)",
    # Production
    "cake_cu_cement":    "Cake — Cu Cement (WMT)",
    "cake_cd_sponge":    "Cake — Cd Sponge (WMT)",
    "cake_co_cake":      "Cake — Co Cake (WMT)",
    "water_consumption": "Water Consumption (m³)",
    # Staffing
    "helpers":  "Helpers",
    "absent":   "Absent",
    "overtime": "Overtime",
    "near_miss":"Near Miss",
}


def show():
    st.markdown("## 📈 TREND ANALYSIS")
    st.markdown('<div style="font-family:Share Tech Mono,monospace;color:#64748b;font-size:12px;">Historical trends across all shifts</div>', unsafe_allow_html=True)
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        field = st.selectbox("Parameter", list(TREND_FIELDS.keys()),
                             format_func=lambda x: TREND_FIELDS[x])
    with c2:
        days = st.selectbox("Time Range", [1, 3, 7, 14, 30],
                            format_func=lambda x: f"Last {x} day{'s' if x>1 else ''}", index=2)

    data = get_trend_data(field, days)
    if not data:
        st.info("No data in this time range yet.")
        return

    df = pd.DataFrame(data)
    df["submitted_at"] = pd.to_datetime(df["submitted_at"])
    df = df.dropna(subset=[field])
    df[field] = pd.to_numeric(df[field], errors="coerce")
    df = df.dropna(subset=[field])

    if df.empty:
        st.info("All values in this range are empty / non-numeric.")
        return

    label = TREND_FIELDS[field]

    # Stats bar
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Latest",  f"{df[field].iloc[-1]:.2f}")
    with c2: st.metric("Average", f"{df[field].mean():.2f}")
    with c3: st.metric("Min",     f"{df[field].min():.2f}")
    with c4: st.metric("Max",     f"{df[field].max():.2f}")

    st.markdown("<br>", unsafe_allow_html=True)
    chart_df = df.set_index("submitted_at")[[field]]
    chart_df.columns = [label]
    st.line_chart(chart_df, use_container_width=True)

    with st.expander("📋 Raw Data"):
        st.dataframe(df[["submitted_at","report_date","shift",field]], use_container_width=True)
