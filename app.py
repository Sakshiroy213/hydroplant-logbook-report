import streamlit as st
from utils.db import init_db
from utils.auth import check_login

st.set_page_config(
    page_title="HydroPlant Monitor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600&display=swap');

:root {
    --primary: #00d4ff;
    --accent: #ff6b35;
    --warning: #ffd60a;
    --danger: #ff003c;
    --success: #00ff88;
    --bg: #0a0e1a;
    --surface: #111827;
    --surface2: #1f2937;
    --text: #e2e8f0;
    --muted: #64748b;
}

.stApp {
    background-color: var(--bg);
    font-family: 'Exo 2', sans-serif;
    color: var(--text);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #0a0e1a 100%);
    border-right: 1px solid #1e3a5f;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00d4ff22, #00d4ff44);
    color: var(--primary);
    border: 1px solid var(--primary);
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-radius: 4px;
    transition: all 0.3s;
}
.stButton > button:hover {
    background: var(--primary);
    color: #000;
    box-shadow: 0 0 20px #00d4ff66;
}

/* Headers */
h1, h2, h3 {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    letter-spacing: 2px;
}

/* Inputs */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background-color: var(--surface2) !important;
    border: 1px solid #1e3a5f !important;
    color: var(--text) !important;
    border-radius: 4px !important;
}

/* Metric cards */
.metric-card {
    background: var(--surface);
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--primary), transparent);
}

/* Warning badge */
.badge-warning {
    background: #ffd60a22;
    color: var(--warning);
    border: 1px solid var(--warning);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 12px;
    font-weight: 600;
}
.badge-danger {
    background: #ff003c22;
    color: var(--danger);
    border: 1px solid var(--danger);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 12px;
    font-weight: 600;
}
.badge-ok {
    background: #00ff8822;
    color: var(--success);
    border: 1px solid var(--success);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 12px;
    font-weight: 600;
}

/* Login box */
.login-container {
    max-width: 420px;
    margin: 80px auto;
    background: var(--surface);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 2.5rem;
    box-shadow: 0 0 60px #00d4ff11;
}

/* Table styling */
.stDataFrame {
    background: var(--surface) !important;
}

/* Divider */
hr {
    border-color: #1e3a5f !important;
}

/* Alert boxes */
.stAlert {
    border-radius: 6px;
    font-family: 'Share Tech Mono', monospace;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    font-family: 'Exo 2', sans-serif;
}

/* Logo text */
.logo-text {
    font-family: 'Rajdhani', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--primary);
    letter-spacing: 3px;
    text-shadow: 0 0 20px #00d4ff66;
}
.logo-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

# Initialize DB
init_db()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None


def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; margin-bottom:2rem;">'
                    '<div class="logo-text">⚡ HYDROPLANT</div>'
                    '<div class="logo-sub">REACTOR MONITORING SYSTEM v2.0</div>'
                    '</div>', unsafe_allow_html=True)

        st.markdown("#### SHIFT INCHARGE LOGIN")
        st.markdown('<hr>', unsafe_allow_html=True)

        username = st.text_input("👤  Username", placeholder="Enter your username")
        password = st.text_input("🔒  Password", type="password", placeholder="Enter your password")

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            login_btn = st.button("🔑  AUTHENTICATE", use_container_width=True)

        if login_btn:
            result = check_login(username, password)
            if result:
                st.session_state.logged_in = True
                st.session_state.user = result["username"]
                st.session_state.role = result["role"]
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Access denied.")

        st.markdown('<hr>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; font-size:11px; color:#64748b;">AUTHORIZED PERSONNEL ONLY<br>All activity is logged and monitored</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def sidebar():
    with st.sidebar:
        st.markdown('<div style="padding: 1rem 0;">'
                    '<div class="logo-text" style="font-size:22px;">⚡ HYDROPLANT</div>'
                    '<div class="logo-sub">MONITORING SYSTEM</div>'
                    '</div>', unsafe_allow_html=True)
        st.markdown("---")

        st.markdown(f"**👤 Logged in as:** `{st.session_state.user}`")
        st.markdown(f"**🎖️ Role:** `{st.session_state.role.upper()}`")
        st.markdown("---")

        # All users can access all pages; admin gets User Management too
        nav_options = [
            "📝 Data Entry",
            "📊 Dashboard",
            "⚠️ Alerts & Warnings",
            "📈 Trend Analysis",
            "🔑 Change Password",
        ]
        if st.session_state.role == "admin":
            nav_options.append("👥 User Management")

        page = st.radio("📊 NAVIGATION", nav_options)

        st.markdown("---")
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()

        st.markdown('<div style="position:absolute; bottom:1rem; left:1rem; right:1rem; font-size:10px; color:#374151; text-align:center;">© 2025 HydroPlant Systems</div>', unsafe_allow_html=True)
    return page


# Routing
if not st.session_state.logged_in:
    login_page()
else:
    page = sidebar()

    if "Data Entry" in page:
        from _pages.data_entry import show
        show()
    elif "Dashboard" in page:
        from _pages.dashboard import show
        show()
    elif "Alerts" in page:
        from _pages.alerts import show
        show()
    elif "Trend" in page:
        from _pages.trends import show
        show()
    elif "Change Password" in page:
        from _pages.change_password import show
        show()
    elif "User Management" in page:
        from _pages.users import show
        show()
