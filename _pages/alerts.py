import streamlit as st
import pandas as pd
from utils.db import get_alerts, resolve_alert


def show():
    st.markdown("## ⚠️ ALERTS & WARNINGS LOG")
    st.markdown('<div style="font-family:Share Tech Mono,monospace;color:#64748b;font-size:12px;">'
                'Auto-detected breaches from submitted shift reports | NOT visible to operators</div>',
                unsafe_allow_html=True)
    st.markdown("---")

    c1,c2 = st.columns(2)
    with c1:
        f_status = st.selectbox("Status", ["All","Active Only","Resolved Only"])
    with c2:
        f_sev = st.selectbox("Severity", ["All","CRITICAL","WARNING"])

    if f_status == "Active Only":
        alerts = get_alerts(resolved=False)
    elif f_status == "Resolved Only":
        alerts = get_alerts(resolved=True)
    else:
        alerts = get_alerts()

    if f_sev != "All":
        alerts = [a for a in alerts if a["severity"] == f_sev]

    # KPI row
    active   = sum(1 for a in alerts if not a["resolved"])
    critical = sum(1 for a in alerts if a["severity"]=="CRITICAL" and not a["resolved"])
    warnings = sum(1 for a in alerts if a["severity"]=="WARNING"  and not a["resolved"])
    c1,c2,c3 = st.columns(3)
    for col,(label,val,color) in zip([c1,c2,c3],[
        ("ACTIVE ALERTS", active,   "#ffd60a"),
        ("CRITICAL",      critical, "#ff003c"),
        ("WARNINGS",      warnings, "#ff6b35"),
    ]):
        with col:
            st.markdown(f"""<div class="metric-card">
                <div style="font-size:10px;color:#64748b;font-family:'Share Tech Mono',monospace;">{label}</div>
                <div style="font-size:36px;font-weight:700;color:{color};font-family:'Rajdhani',sans-serif;">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not alerts:
        st.success("✅ No alerts found.")
        return

    for a in alerts:
        sev      = a["severity"]
        resolved = a["resolved"]
        if resolved:
            border, sev_color, bg = "#374151","#64748b","#11182722"
        elif sev == "CRITICAL":
            border, sev_color, bg = "#ff003c","#ff003c","#ff003c11"
        else:
            border, sev_color, bg = "#ffd60a","#ffd60a","#ffd60a11"

        status_txt = "✅ RESOLVED" if resolved else f"🔴 {sev}"
        col_main, col_btn = st.columns([6, 1])
        with col_main:
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {border};border-radius:8px;
                        padding:12px 16px;margin-bottom:6px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                <span style="font-family:'Rajdhani',sans-serif;font-size:17px;font-weight:700;color:{sev_color};">
                  {status_txt}
                </span>
                <span style="font-family:'Share Tech Mono',monospace;font-size:11px;color:#64748b;">
                  {a['triggered_at']}
                </span>
              </div>
              <div style="display:flex;gap:24px;flex-wrap:wrap;font-size:13px;">
                <div><span style="color:#64748b;font-size:11px;">PARAMETER</span><br>
                     <b style="color:{sev_color};">{a['parameter']}</b></div>
                <div><span style="color:#64748b;font-size:11px;">VALUE</span><br>
                     <b>{a['value']}</b></div>
                <div><span style="color:#64748b;font-size:11px;">BREACH</span><br>
                     <b style="color:{sev_color};">{a['limit_type']}</b></div>
                <div><span style="color:#64748b;font-size:11px;">OPERATOR</span><br>
                     <b>{a['submitted_by']}</b></div>
                <div><span style="color:#64748b;font-size:11px;">REPORT ID</span><br>
                     <b>#{a['report_id']}</b></div>
              </div>
            </div>""", unsafe_allow_html=True)
        with col_btn:
            if not resolved:
                if st.button("✅ Resolve", key=f"res_{a['id']}"):
                    resolve_alert(a["id"])
                    st.rerun()

    st.markdown("---")
    df = pd.DataFrame(alerts)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export Alerts CSV", csv, "alerts.csv", "text/csv")
