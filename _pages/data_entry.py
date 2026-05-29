import streamlit as st
from datetime import datetime, date
from utils.db import insert_report, insert_alerts, check_alerts_from_report, log_audit


def level_input(label, key, default=None):
    """Returns float or None. Handles 'E' (empty) as None."""
    col_a, col_b = st.columns([3, 1])
    with col_a:
        val = st.text_input(label, value="" if default is None else str(default), key=key,
                            placeholder="cm  or  E = Empty")
    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
    v = val.strip().upper()
    if v in ("E", "EMPTY", ""):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def show():
    st.markdown("## 📝 SHIFT REPORT — DATA ENTRY")
    st.markdown('<div style="font-family:Share Tech Mono,monospace;color:#64748b;font-size:12px;">'
                'Complete all sections and submit once per shift | E = Empty tank</div>', unsafe_allow_html=True)
    st.markdown("---")

    now = datetime.now()

    # ── Header info bar ────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    hour = now.hour
    shift_auto = "A" if 6 <= hour < 14 else ("B" if 14 <= hour < 22 else "C")
    for col, label, value in [
        (c1, "DATE",     now.strftime("%d %b %Y")),
        (c2, "TIME",     now.strftime("%H:%M:%S")),
        (c3, "OPERATOR", st.session_state.user.upper()),
        (c4, "SHIFT",    f"{shift_auto} — {'Morning' if shift_auto=='A' else 'Afternoon' if shift_auto=='B' else 'Night'}"),
    ]:
        with col:
            st.markdown(f"""<div class="metric-card">
                <div style="font-size:10px;color:#64748b;font-family:'Share Tech Mono',monospace;">{label}</div>
                <div style="font-size:17px;font-weight:700;color:#00d4ff;font-family:'Rajdhani',sans-serif;">{value}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    with st.form("shift_report_form", clear_on_submit=True):

        # ── SEC 1 : Shift Identification ──────────────────────────────────────
        st.markdown("### 🏭 SECTION 1 — SHIFT IDENTIFICATION")
        c1, c2, c3 = st.columns(3)
        with c1:
            report_date = st.date_input("Date *", value=date.today())
        with c2:
            shift = st.selectbox("Shift *", ["A — Morning (06–14)", "B — Afternoon (14–22)", "C — Night (22–06)"],
                                 index=["A","B","C"].index(shift_auto))
        with c3:
            shift_incharge_no = st.selectbox("Shift Incharge No. *",
                                             ["01","02","03","04","05","06"])

        c1, c2, c3 = st.columns(3)
        with c1:
            opt_filter = st.selectbox("Opt. Filter", ["01","02","03","04"])
        with c2:
            reactor_opt = st.selectbox("Reactor Opt.", ["01","02","03","04","05"])
        with c3:
            near_miss = st.number_input("Near Miss", min_value=0, value=0, step=1)

        c1, c2, c3 = st.columns(3)
        with c1:
            helpers = st.number_input("Helpers", min_value=0, value=0, step=1)
        with c2:
            absent = st.number_input("Absent", min_value=0, value=0, step=1)
        with c3:
            overtime = st.number_input("Over Time (persons)", min_value=0, value=0, step=1)

        st.markdown("---")

        # ── SEC 2 : PF Cake Charging ──────────────────────────────────────────
        st.markdown("### 🧱 SECTION 2 — PF CAKE CHARGING (WMT)")
        c1, c2 = st.columns(2)
        with c1:
            pf_g_spt  = st.number_input("G/SPT (WMT)", min_value=0.0, value=0.0, step=0.001, format="%.3f")
        with c2:
            pf_ug_spt = st.number_input("U/G SPT (WMT)", min_value=0.0, value=0.0, step=0.001, format="%.3f")

        st.markdown("---")

        # ── SEC 3 : Zn Dust Charging ──────────────────────────────────────────
        st.markdown("### ⚗️ SECTION 3 — Zn DUST CHARGING (kg)")
        c1, c2, c3, c4 = st.columns(4)
        with c1: zn_r4 = st.number_input("R4 (kg)", min_value=0.0, value=0.0, step=1.0)
        with c2: zn_r5 = st.number_input("R5 (kg)", min_value=0.0, value=0.0, step=1.0)
        with c3: zn_r6 = st.number_input("R6 (kg)", min_value=0.0, value=0.0, step=1.0)
        with c4: zn_r7 = st.number_input("R7 (kg)", min_value=0.0, value=0.0, step=1.0)

        st.markdown("---")

        # ── SEC 4 : Acid ──────────────────────────────────────────────────────
        st.markdown("### 🧪 SECTION 4 — ACID DOSING (litres)")
        c1, c2, c3 = st.columns(3)
        with c1: acid_ug_spt  = st.number_input("UG SPT (ltr)",  min_value=0.0, value=0.0, step=10.0)
        with c2: acid_grd_spt = st.number_input("Grd SPT (ltr)", min_value=0.0, value=0.0, step=10.0)
        with c3: acid_r1      = st.number_input("R1 (ltr)",      min_value=0.0, value=0.0, step=10.0)
        c1, c2, c3 = st.columns(3)
        with c1: acid_r2  = st.number_input("R2 (ltr)",   min_value=0.0, value=0.0, step=10.0)
        with c2: acid_r3  = st.number_input("R3 (ltr)",   min_value=0.0, value=0.0, step=10.0)
        with c3: acid_r8  = st.number_input("R8 (ltr)",   min_value=0.0, value=0.0, step=10.0)
        c1, c2, c3 = st.columns(3)
        with c1: acid_r9  = st.number_input("R9 (ltr)",   min_value=0.0, value=0.0, step=10.0)
        with c2: acid_r10 = st.number_input("R10 (ltr)",  min_value=0.0, value=0.0, step=10.0)
        with c3: acid_wr03 = st.number_input("WR-03 (ltr)", min_value=0.0, value=0.0, step=10.0)

        st.markdown("---")

        # ── SEC 5 : PAT & Lead Acetate ────────────────────────────────────────
        st.markdown("### 🔬 SECTION 5 — PAT & LEAD ACETATE (kg)")
        c1, c2 = st.columns(2)
        with c1: pat_kg         = st.number_input("PAT (kg)",          min_value=0.0, value=0.0, step=0.5)
        with c2: lead_acetate_kg = st.number_input("Lead Acetate (kg)", min_value=0.0, value=0.0, step=0.5)

        st.markdown("---")

        # ── SEC 6 : Levels ────────────────────────────────────────────────────
        st.markdown("### 📏 SECTION 6 — TANK LEVELS (cm  |  E = Empty)")
        st.markdown('<div style="font-size:11px;color:#64748b;font-family:Share Tech Mono,monospace;margin-bottom:8px;">Enter numeric cm value or type E for empty tanks</div>', unsafe_allow_html=True)

        st.markdown("**SPT Tanks**")
        c1, c2 = st.columns(2)
        with c1: raw_ug_spt  = st.text_input("UG SPT (cm)",  key="lvl_ug_spt",  placeholder="cm or E")
        with c2: raw_grd_spt = st.text_input("Grd SPT (cm)", key="lvl_grd_spt", placeholder="cm or E")

        st.markdown("**Reactors R1–R10**")
        c1,c2,c3,c4,c5 = st.columns(5)
        with c1: raw_r1  = st.text_input("R1",  key="lvl_r1",  placeholder="cm or E")
        with c2: raw_r2  = st.text_input("R2",  key="lvl_r2",  placeholder="cm or E")
        with c3: raw_r3  = st.text_input("R3",  key="lvl_r3",  placeholder="cm or E")
        with c4: raw_r4  = st.text_input("R4",  key="lvl_r4",  placeholder="cm or E")
        with c5: raw_r5  = st.text_input("R5",  key="lvl_r5",  placeholder="cm or E")
        c1,c2,c3,c4,c5 = st.columns(5)
        with c1: raw_r6  = st.text_input("R6",  key="lvl_r6",  placeholder="cm or E")
        with c2: raw_r7  = st.text_input("R7",  key="lvl_r7",  placeholder="cm or E")
        with c3: raw_r8  = st.text_input("R8",  key="lvl_r8",  placeholder="cm or E")
        with c4: raw_r9  = st.text_input("R9",  key="lvl_r9",  placeholder="cm or E")
        with c5: raw_r10 = st.text_input("R10", key="lvl_r10", placeholder="cm or E")

        st.markdown("**Wash Reactors (WR)**")
        c1,c2,c3,c4 = st.columns(4)
        with c1: raw_wr1 = st.text_input("WR1", key="lvl_wr1", placeholder="cm or E")
        with c2: raw_wr2 = st.text_input("WR2", key="lvl_wr2", placeholder="cm or E")
        with c3: raw_wr3 = st.text_input("WR3", key="lvl_wr3", placeholder="cm or E")
        with c4: raw_wr4 = st.text_input("WR4", key="lvl_wr4", placeholder="cm or E")

        st.markdown("**MLT Tanks**")
        c1,c2,c3 = st.columns(3)
        with c1: raw_mlt01 = st.text_input("MLT 01", key="lvl_mlt01", placeholder="cm or E")
        with c2: raw_mlt02 = st.text_input("MLT 02", key="lvl_mlt02", placeholder="cm or E")
        with c3: raw_mlt03 = st.text_input("MLT 03", key="lvl_mlt03", placeholder="cm or E")

        st.markdown("**Storage Tanks**")
        c1,c2,c3,c4,c5 = st.columns(5)
        with c1: raw_old_znso4    = st.text_input("Old ZnSO₄",    key="lvl_old_znso4",    placeholder="cm")
        with c2: raw_new_znso4    = st.text_input("New ZnSO₄",    key="lvl_new_znso4",    placeholder="cm")
        with c3: raw_acid_storage = st.text_input("Acid Storage",  key="lvl_acid_storage", placeholder="cm")
        with c4: raw_acid_day     = st.text_input("Acid Day Tank", key="lvl_acid_day",     placeholder="cm")
        with c5: raw_water        = st.text_input("Water Tank",    key="lvl_water",        placeholder="cm")

        st.markdown("---")

        # ── SEC 7 : Cake Output ───────────────────────────────────────────────
        st.markdown("### 🎂 SECTION 7 — CAKE OUTPUT (WMT)")
        c1,c2,c3 = st.columns(3)
        with c1: cake_cu  = st.number_input("Cu Cement (WMT)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
        with c2: cake_cd  = st.number_input("Cd Sponge (WMT)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
        with c3: cake_co  = st.number_input("Co Cake (WMT)",   min_value=0.0, value=0.0, step=0.01, format="%.2f")

        st.markdown("---")

        # ── SEC 8 : Water Consumption ─────────────────────────────────────────
        st.markdown("### 💧 SECTION 8 — WATER CONSUMPTION")
        water_consump = st.number_input("Total Water Consumed (m³)", min_value=0.0, value=0.0, step=0.5)

        st.markdown("---")

        # ── SEC 9 : Remarks ───────────────────────────────────────────────────
        st.markdown("### 📋 SECTION 9 — REMARKS & OBSERVATIONS")
        remarks = st.text_area(
            "Remarks (list all issues, maintenance, near misses, pending work...)",
            placeholder="e.g.\n1. Housekeeping ongoing\n2. R4-R5 steam line insulation pending\n3. Leakage from R1 & MLT2 pump",
            height=160
        )

        st.markdown("<br>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns([2,1,2])
        with c2:
            submitted = st.form_submit_button("✅  SUBMIT SHIFT REPORT", use_container_width=True)

    # ── On Submit ──────────────────────────────────────────────────────────────
    def parse_level(raw):
        v = raw.strip().upper()
        if v in ("E", "EMPTY", ""):
            return None
        try:
            return float(v)
        except ValueError:
            return None

    if submitted:
        data = {
            "report_date":       report_date.strftime("%Y-%m-%d"),
            "shift":             shift,
            "shift_incharge_no": shift_incharge_no,
            "opt_filter":        opt_filter,
            "reactor_opt":       reactor_opt,
            "helpers":           int(helpers),
            "absent":            int(absent),
            "overtime":          int(overtime),
            "near_miss":         int(near_miss),
            # PF Cake
            "pf_g_spt":          pf_g_spt,
            "pf_ug_spt":         pf_ug_spt,
            # Zn Dust
            "zn_r4": zn_r4, "zn_r5": zn_r5, "zn_r6": zn_r6, "zn_r7": zn_r7,
            # Acid
            "acid_ug_spt":  acid_ug_spt,  "acid_grd_spt": acid_grd_spt,
            "acid_r1":      acid_r1,       "acid_r2":      acid_r2,
            "acid_r3":      acid_r3,       "acid_r8":      acid_r8,
            "acid_r9":      acid_r9,       "acid_r10":     acid_r10,
            "acid_wr03":    acid_wr03,
            # PAT / Lead Acetate
            "pat_kg": pat_kg, "lead_acetate_kg": lead_acetate_kg,
            # Levels — numeric or None
            "lvl_ug_spt":       parse_level(raw_ug_spt),
            "lvl_grd_spt":      parse_level(raw_grd_spt),
            "lvl_r1":           parse_level(raw_r1),
            "lvl_r2":           parse_level(raw_r2),
            "lvl_r3":           parse_level(raw_r3),
            "lvl_r4":           parse_level(raw_r4),
            "lvl_r5":           parse_level(raw_r5),
            "lvl_r6":           raw_r6.strip() or None,    # stored as-is (could be "E")
            "lvl_r7":           parse_level(raw_r7),
            "lvl_r8":           parse_level(raw_r8),
            "lvl_r9":           raw_r9.strip() or None,
            "lvl_r10":          raw_r10.strip() or None,
            "lvl_wr1":          parse_level(raw_wr1),
            "lvl_wr2":          parse_level(raw_wr2),
            "lvl_wr3":          parse_level(raw_wr3),
            "lvl_wr4":          parse_level(raw_wr4),
            "lvl_mlt01":        parse_level(raw_mlt01),
            "lvl_mlt02":        parse_level(raw_mlt02),
            "lvl_mlt03":        parse_level(raw_mlt03),
            "lvl_old_znso4":    parse_level(raw_old_znso4),
            "lvl_new_znso4":    parse_level(raw_new_znso4),
            "lvl_acid_storage": parse_level(raw_acid_storage),
            "lvl_acid_day_tank":parse_level(raw_acid_day),
            "lvl_water":        parse_level(raw_water),
            # Cake
            "cake_cu_cement": cake_cu, "cake_cd_sponge": cake_cd, "cake_co_cake": cake_co,
            # Water
            "water_consumption": water_consump,
            # Meta
            "remarks":      remarks,
            "submitted_by": st.session_state.user,
            "has_warnings": 0,
        }

        # Check alerts silently
        # Temporarily insert with has_warnings=0, get ID, then check
        report_id = insert_report(data)
        alerts = check_alerts_from_report(data, report_id)
        if alerts:
            insert_alerts(alerts)
            # Update has_warnings flag
            from utils.db import get_conn
            conn = get_conn()
            conn.execute("UPDATE shift_reports SET has_warnings=1 WHERE id=?", (report_id,))
            conn.commit()
            conn.close()

        log_audit(st.session_state.user, "SUBMIT_REPORT",
                  f"Report #{report_id} | {report_date} | Shift {shift}")

        st.success(f"""
        ✅ **Shift Report Submitted Successfully!**  
        📅 Date: **{report_date}** | 🔄 Shift: **{shift}** | 👤 By: **{st.session_state.user}**  
        📌 Report ID: `#{report_id}` | ⏱️ Time: **{datetime.now().strftime('%H:%M:%S')}**
        """)
        st.balloons()
