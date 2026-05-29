import streamlit as st
from utils.db import change_password, log_audit


def show():
    st.markdown("## 🔑 CHANGE PASSWORD")
    st.markdown(
        '<div style="font-family:Share Tech Mono,monospace;color:#64748b;font-size:12px;">'
        f'Updating password for account: <b style="color:#00d4ff;">{st.session_state.user}</b>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown(
            '<div style="background:#111827;border:1px solid #1e3a5f;border-radius:12px;'
            'padding:2rem;box-shadow:0 0 40px #00d4ff0a;">',
            unsafe_allow_html=True,
        )

        st.markdown("#### 🔐 UPDATE YOUR PASSWORD")
        st.markdown('<hr>', unsafe_allow_html=True)

        current_pw = st.text_input("🔒  Current Password", type="password",
                                   placeholder="Enter your current password",
                                   key="cp_current")
        new_pw = st.text_input("🔑  New Password", type="password",
                               placeholder="Enter new password (min 6 chars)",
                               key="cp_new")
        confirm_pw = st.text_input("✅  Confirm New Password", type="password",
                                   placeholder="Re-enter new password",
                                   key="cp_confirm")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("💾  SAVE NEW PASSWORD", use_container_width=True):
            # Validation
            if not current_pw or not new_pw or not confirm_pw:
                st.error("❌ All fields are required.")
            elif len(new_pw) < 6:
                st.error("❌ New password must be at least 6 characters.")
            elif new_pw != confirm_pw:
                st.error("❌ New passwords do not match.")
            elif new_pw == current_pw:
                st.warning("⚠️ New password must be different from your current password.")
            else:
                success, msg = change_password(st.session_state.user, current_pw, new_pw)
                if success:
                    log_audit(st.session_state.user, "CHANGE_PASSWORD", "Password changed successfully")
                    st.success(f"✅ {msg} Please use your new password the next time you log in.")
                else:
                    st.error(f"❌ {msg}")

        st.markdown(
            '<div style="margin-top:1rem;font-size:11px;color:#64748b;font-family:Share Tech Mono,monospace;'
            'text-align:center;">All password changes are logged in the audit trail.</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
