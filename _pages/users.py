import streamlit as st
import pandas as pd
from utils.db import get_all_users, add_user, delete_user, get_conn, log_audit


def show():
    st.markdown("## 👥 USER MANAGEMENT")
    st.markdown('<div style="font-family:Share Tech Mono,monospace;color:#64748b;font-size:12px;">Manage shift incharges and admin accounts</div>', unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["👥 All Users", "➕ Add User", "📋 Audit Log"])

    with tab1:
        users = get_all_users()
        for u in users:
            c1,c2,c3,c4,c5,c6 = st.columns([1.5,2,1.2,1.2,2,0.8])
            with c1: st.markdown(f"`{u['username']}`")
            with c2: st.markdown(f"**{u['full_name'] or '—'}**")
            with c3:
                color = "#00d4ff" if u["role"]=="admin" else "#00ff88"
                st.markdown(f'<span style="color:{color};font-weight:700;">{u["role"].upper()}</span>', unsafe_allow_html=True)
            with c4: st.markdown(f"Shift {u['shift'] or '—'}")
            with c5: st.markdown(f'<span style="font-size:11px;color:#64748b;font-family:Share Tech Mono,monospace;">{u["created_at"]}</span>', unsafe_allow_html=True)
            with c6:
                if u["username"] not in ("admin", st.session_state.user):
                    if st.button("🗑️", key=f"del_{u['id']}"):
                        delete_user(u["id"])
                        log_audit(st.session_state.user, "DELETE_USER", u["username"])
                        st.success(f"Deleted {u['username']}")
                        st.rerun()

    with tab2:
        with st.form("add_user"):
            c1,c2 = st.columns(2)
            with c1:
                nu = st.text_input("Username *")
                np = st.text_input("Password *", type="password")
                nr = st.selectbox("Role", ["operator","admin"])
            with c2:
                nf = st.text_input("Full Name")
                ns = st.selectbox("Default Shift", ["A — Morning","B — Afternoon","C — Night","All"])
            ok = st.form_submit_button("➕ Create User")
            if ok:
                if nu and np:
                    success, msg = add_user(nu, np, nr, nf, ns)
                    if success:
                        log_audit(st.session_state.user, "CREATE_USER", nu)
                        st.success(f"✅ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
                else:
                    st.error("Username and password are required.")

    with tab3:
        conn = get_conn()
        rows = conn.execute("SELECT * FROM audit_log ORDER BY ts DESC LIMIT 200").fetchall()
        conn.close()
        if rows:
            df = pd.DataFrame([dict(r) for r in rows])
            st.dataframe(df, use_container_width=True, height=400)
        else:
            st.info("No audit events yet.")
