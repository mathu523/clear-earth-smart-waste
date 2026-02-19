import streamlit as st

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Clear Earth - Smart Waste System",
    page_icon="♻️",
    layout="wide"
)

# ==============================
# GLOBAL SIDEBAR STYLING
# ==============================
st.markdown("""
<style>

/* SIDEBAR BACKGROUND */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #111827);
    padding-top: 30px;
}

/* Sidebar text color */
section[data-testid="stSidebar"] * {
    color: white !important;
    font-family: 'Segoe UI', sans-serif;
}

/* EcoWaste Title */
.sidebar-logo {
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 25px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Navigation Label */
.sidebar-label {
    font-size: 14px;
    color: #9ca3af;
    margin-bottom: 10px;
}

/* Radio Buttons */
div[role="radiogroup"] > label {
    padding: 12px 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    transition: 0.3s;
}

div[role="radiogroup"] > label:hover {
    background-color: rgba(255,255,255,0.1);
    transform: translateX(5px);
}

/* Logout Button */
.stButton > button {
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    color: white;
    border-radius: 8px;
    padding: 10px 15px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE INIT
# ==============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==============================
# LOGIN ROUTING
# ==============================
if not st.session_state.logged_in:
    import login
    login.show()

# ==============================
# MAIN APPLICATION
# ==============================
else:

    # Sidebar Branding
    st.sidebar.markdown(
        '<div class="sidebar-logo">🌿 EcoWaste</div>',
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        '<div class="sidebar-label">Navigation</div>',
        unsafe_allow_html=True
    )

    page = st.sidebar.radio(
        "",
        ["Dashboard", "AI Detection", "Admin Monitor"]
    )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Page Routing
    if page == "Dashboard":
        import Dashboard
        Dashboard.show()

    elif page == "AI Detection":
        import ai_detection
        ai_detection.show()

    elif page == "Admin Monitor":
        import admin_monitor
        admin_monitor.show()
