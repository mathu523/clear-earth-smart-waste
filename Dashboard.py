import streamlit as st
import pandas as pd
import os

ALERT_FILE = "alerts.csv"

def show():

    # ==============================
    # CUSTOM CSS STYLING
    # ==============================
    st.markdown("""
        <style>

        .stApp {
            background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
                        url("https://images.unsplash.com/photo-1501004318641-b39e6451bec6");
            background-size: cover;
            background-attachment: fixed;
        }

        .main-title {
            font-size: 48px;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(to right, #8E2DE2, #4A00E0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeIn 2s ease-in-out;
        }

        .subtitle {
            text-align: center;
            font-size: 20px;
            color: white;
            margin-bottom: 40px;
            animation: fadeIn 3s ease-in-out;
        }

        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            color: white;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            transition: 0.3s;
        }

        .glass-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.6);
        }

        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(20px);}
            to {opacity: 1; transform: translateY(0);}
        }

        </style>
    """, unsafe_allow_html=True)

    # ==============================
    # HERO SECTION
    # ==============================
    st.markdown('<div class="main-title"> 🌍 Clear Earth Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Smart Waste Monitoring & Sustainability Insights</div>', unsafe_allow_html=True)

    # ==============================
    # DATA SECTION
    # ==============================
    if not os.path.exists(ALERT_FILE):
        st.warning("No logs available yet.")
        return

    df = pd.read_csv(ALERT_FILE)

    if df.empty:
        st.info("No records found.")
        return

    total_logs = len(df)
    active_alerts = len(df[df["Final Status"] == "FULL"]) if "Final Status" in df.columns else 0
    avg_fill = round(df["Fill %"].mean(), 1) if "Fill %" in df.columns else 0

    # ==============================
    # KPI CARDS
    # ==============================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="glass-card">
                <h2>📦 {total_logs}</h2>
                <p>Total Logs</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="glass-card">
                <h2>🚨 {active_alerts}</h2>
                <p>Active Alerts</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="glass-card">
                <h2>📊 {avg_fill}%</h2>
                <p>Average Fill %</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ==============================
    # DATA PREVIEW SECTION
    # ==============================
    st.markdown('<div class="subtitle">Recent Activity</div>', unsafe_allow_html=True)

    st.dataframe(df.tail(5), width="stretch")
