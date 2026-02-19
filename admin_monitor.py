import streamlit as st
import pandas as pd
import os

ALERT_FILE = "alerts.csv"

def show():

    # ===============================
    # BACKGROUND + DARK OVERLAY STYLE
    # ===============================
    st.markdown("""
    <style>

    /* FULL PAGE BACKGROUND */
    .stApp {
        background: 
            linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
            url("https://images.unsplash.com/photo-1508780709619-79562169bc64");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }

    /* SIDEBAR DARK */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* GLASS CARD STYLE */
    .glass {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.6);
        margin-bottom: 25px;
        color: white;
    }

    /* ALERT ANIMATION */
    .alert-box {
        background: linear-gradient(to right, #ff416c, #ff4b2b);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        animation: pulse 1.5s infinite;
        color: white;
    }

    @keyframes pulse {
        0% {transform: scale(1);}
        50% {transform: scale(1.05);}
        100% {transform: scale(1);}
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color:#8E2DE2;'>📊 Central Monitoring System</h1>", unsafe_allow_html=True)

    if not os.path.exists(ALERT_FILE):
        st.warning("No monitoring data available.")
        return

    df = pd.read_csv(ALERT_FILE)

    if df.empty:
        st.info("No logs recorded yet.")
        return

    total_logs = len(df)
    active_alerts = len(df[df["Final Status"] == "FULL"])
    normal_bins = len(df[df["Final Status"] == "NOT FULL"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="glass">
            <h2>📦 {total_logs}</h2>
            <p>Total Records</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if active_alerts > 0:
            st.markdown(f"""
            <div class="alert-box">
                🚨 {active_alerts} Active Alerts
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="glass">
                ✅ 0 Active Alerts
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="glass">
            <h2>🟢 {normal_bins}</h2>
            <p>Normal Bins</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("📄 Monitoring Logs")
    st.dataframe(df, width="stretch")

    st.subheader("🌍 Bin Location Map")

    df_map = df.copy()
    df_map["lat"] = pd.to_numeric(df_map["Latitude"], errors="coerce")
    df_map["lon"] = pd.to_numeric(df_map["Longitude"], errors="coerce")

    st.map(df_map.dropna(subset=["lat", "lon"]))
