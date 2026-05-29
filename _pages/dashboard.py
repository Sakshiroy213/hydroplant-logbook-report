import streamlit as st
import pandas as pd
from utils.db import get_all_reports, get_stats


def show():
    st.markdown("## 📊 ADMIN DASHBOARD — SHIFT REPORTS")
    st.markdown('<div style="font-family:Share Tech Mono,monospace;color:#64748b;font-size:12px;">Overview of all submitted shift reports</div>', unsafe_allow_html=True)
    st.markdown("---")

    stats = get_stats()
    c1,c2,c3,c4 = st.columns(4)
    for col,(label,val,color) in zip([c1,c2,c3,c4],[
        ("📋 TOTAL REPORTS",   stats["total_reports"],  "#00d4ff"),
        ("📅 LAST 24H",        stats["reports_24h"],    "#00ff88"),
        ("⚠️ ACTIVE ALERTS",  stats["active_alerts"],  "#ffd60a"),
        ("🚨 CRITICAL",        stats["critical_alerts"],"#ff003c"),
    ]):
        with col:
            st.markdown(f"""<div class="metric-card">
                <div style="font-size:10px;color:#64748b;font-family:'Share Tech Mono',monospace;">{label}</div>
                <div style="font-size:36px;font-weight:700;color:{color};font-family:'Rajdhani',sans-serif;">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    reports = get_all_reports(200)
    if not reports:
        st.info("No shift reports submitted yet.")
        return

    df = pd.DataFrame(reports)

    # ── Summary view tabs ──────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(["📋 All Reports", "🧪 Chemicals", "📏 Levels", "🎂 Production"])

    with tab1:
        cols = ["id","submitted_at","report_date","shift","shift_incharge_no",
                "submitted_by","helpers","absent","overtime","near_miss",
                "water_consumption","has_warnings","remarks"]
        show_df = df[[c for c in cols if c in df.columns]].copy()
        show_df.rename(columns={
            "id":"ID","submitted_at":"Submitted","report_date":"Date",
            "shift":"Shift","shift_incharge_no":"Incharge No",
            "submitted_by":"By","helpers":"Helpers","absent":"Absent",
            "overtime":"OT","near_miss":"Near Miss",
            "water_consumption":"Water (m³)","has_warnings":"⚠️","remarks":"Remarks"
        }, inplace=True)

        def hl(row):
            return ['background-color:#ff003c11']*len(row) if row.get("⚠️",0)==1 else ['']*len(row)

        st.dataframe(show_df.style.apply(hl, axis=1), use_container_width=True, height=420)

    with tab2:
        chem_cols = ["id","report_date","shift","submitted_by",
                     "pf_g_spt","pf_ug_spt",
                     "zn_r4","zn_r5","zn_r6","zn_r7",
                     "acid_ug_spt","acid_grd_spt","acid_r1","acid_r2","acid_r3",
                     "acid_r8","acid_r9","acid_r10","acid_wr03",
                     "pat_kg","lead_acetate_kg"]
        chem_df = df[[c for c in chem_cols if c in df.columns]].copy()
        st.dataframe(chem_df, use_container_width=True, height=420)

    with tab3:
        lvl_cols = ["id","report_date","shift","submitted_by",
                    "lvl_ug_spt","lvl_grd_spt",
                    "lvl_r1","lvl_r2","lvl_r3","lvl_r4","lvl_r5",
                    "lvl_r6","lvl_r7","lvl_r8","lvl_r9","lvl_r10",
                    "lvl_wr1","lvl_wr2","lvl_wr3","lvl_wr4",
                    "lvl_mlt01","lvl_mlt02","lvl_mlt03",
                    "lvl_old_znso4","lvl_new_znso4",
                    "lvl_acid_storage","lvl_acid_day_tank","lvl_water"]
        lvl_df = df[[c for c in lvl_cols if c in df.columns]].copy()
        st.dataframe(lvl_df, use_container_width=True, height=420)

    with tab4:
        prod_cols = ["id","report_date","shift","submitted_by",
                     "cake_cu_cement","cake_cd_sponge","cake_co_cake","water_consumption"]
        prod_df = df[[c for c in prod_cols if c in df.columns]].copy()
        # Totals row
        numeric_p = prod_df.select_dtypes("number").columns.tolist()
        totals = prod_df[numeric_p].sum()
        st.dataframe(prod_df, use_container_width=True, height=380)
        st.markdown("**Totals (all records shown):**")
        tc1,tc2,tc3,tc4 = st.columns(4)
        for col,k,label in [
            (tc1,"cake_cu_cement","Cu Cement (WMT)"),
            (tc2,"cake_cd_sponge","Cd Sponge (WMT)"),
            (tc3,"cake_co_cake","Co Cake (WMT)"),
            (tc4,"water_consumption","Water (m³)"),
        ]:
            with col:
                v = totals.get(k, 0)
                st.metric(label, f"{v:.2f}")

    st.markdown("---")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ DOWNLOAD ALL DATA (CSV)", csv,
                       f"shift_reports_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                       "text/csv")
