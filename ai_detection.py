import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage
from twilio.rest import Client

ALERT_FILE = "alerts.csv"
MAX_CAPACITY = 20.0
FULL_THRESHOLD = 80

# =====================================================
# EMAIL FUNCTION
# =====================================================
def send_email_alert(bin_id, location, fill_percent):
    try:
        SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
        SENDER_PASSWORD = st.secrets["SENDER_PASSWORD"]
        RECEIVER_EMAIL = st.secrets["RECEIVER_EMAIL"]
    except:
        st.error("Check email secrets in secrets.toml")
        return False

    subject = f"🚨 ALERT: Bin {bin_id} is FULL ({fill_percent}%)"
    body = f"""
Bin ID: {bin_id}
Location: {location}
Fill Level: {fill_percent}%
Time: {datetime.now()}
"""

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)

        return True
    except Exception as e:
        st.error(f"Email Error: {e}")
        return False


# =====================================================
# SMS FUNCTION (Twilio)
# =====================================================
def send_sms_alert(bin_id, location, fill_percent):
    try:
        account_sid = st.secrets["TWILIO_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
        twilio_number = st.secrets["TWILIO_NUMBER"]
        receiver_number = st.secrets["RECEIVER_NUMBER"]
    except:
        st.error("Check Twilio secrets in secrets.toml")
        return False

    message_body = f"🚨 ALERT! Bin {bin_id} at {location} is FULL ({fill_percent}%). Immediate pickup required."

    try:
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message_body,
            from_=twilio_number,
            to=receiver_number
        )
        return True
    except Exception as e:
        st.error(f"SMS Error: {e}")
        return False


# =====================================================
# MAIN PAGE UI
# =====================================================
def show():

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)),
                    url("https://images.unsplash.com/photo-1492724441997-5dc865305da7");
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }

    .status-full {
        color: white;
        background: linear-gradient(to right, #ff416c, #ff4b2b);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        animation: pulse 1.5s infinite;
    }

    .status-ok {
        color: white;
        background: linear-gradient(to right, #11998e, #38ef7d);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }

    @keyframes pulse {
        0% {transform: scale(1);}
        50% {transform: scale(1.05);}
        100% {transform: scale(1);}
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color:#8E2DE2;'>🤖 Smart Bin AI Detection</h1>", unsafe_allow_html=True)

    # Create CSV if not exists
    if not os.path.exists(ALERT_FILE):
        pd.DataFrame(columns=[
            "Time", "Bin ID", "Location", "Latitude", "Longitude",
            "Weight (kg)", "Fill %", "Image Status", "Final Status"
        ]).to_csv(ALERT_FILE, index=False)

    col1, col2 = st.columns(2)

    with col1:
        bin_id = st.text_input("Bin ID", "BIN_NY_01")
        location = st.text_input("Location", "Central Park")
        weight = st.slider("Weight (kg)", 0.0, 30.0, 5.0)
        lat, lon = 40.7850, -73.9682

    with col2:
        cam = st.camera_input("📸 Scan Bin Contents")

    # Detection Logic
    fill_pct = min((weight / MAX_CAPACITY) * 100, 100)
    img_status = "NOT PROVIDED"

    if cam:
        img = Image.open(cam)
        img_np = np.array(img)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        density = np.count_nonzero(edges) / edges.size
        img_status = "FULL" if density > 0.07 else "NOT FULL"

    weight_status = "FULL" if fill_pct >= FULL_THRESHOLD else "NOT FULL"
    final_status = "FULL" if (weight_status == "FULL" or img_status == "FULL") else "NOT FULL"

    st.markdown("<br>", unsafe_allow_html=True)

    if final_status == "FULL":
        st.markdown('<div class="status-full">🚨 BIN FULL - ACTION REQUIRED</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-ok">✅ BIN STATUS NORMAL</div>', unsafe_allow_html=True)

    st.progress(int(fill_pct))

    # =====================================================
    # PROCESS BUTTON
    # =====================================================
    if st.button("🚀 Process & Notify", use_container_width=True):

        df = pd.read_csv(ALERT_FILE)

        new_data = pd.DataFrame([{
            "Time": datetime.now(),
            "Bin ID": bin_id,
            "Location": location,
            "Latitude": lat,
            "Longitude": lon,
            "Weight (kg)": weight,
            "Fill %": round(fill_pct, 1),
            "Image Status": img_status,
            "Final Status": final_status
        }])

        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(ALERT_FILE, index=False)

        if final_status == "FULL":

            email_sent = send_email_alert(bin_id, location, round(fill_pct,1))
            sms_sent = send_sms_alert(bin_id, location, round(fill_pct,1))

            if email_sent and sms_sent:
                st.success("Authorities notified via Email & SMS successfully!")
            else:
                st.warning("Alert triggered but check email/SMS configuration.")

        else:
            st.success("Log saved successfully!")
