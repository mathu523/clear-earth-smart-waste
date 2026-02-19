import streamlit as st

def show():
    st.markdown("""
    <style>
        .stApp {
            background: url("https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?q=80&w=2013&auto=format&fit=crop");
            background-size: cover;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("♻️ Clear Earth")
        st.subheader("Waste Management Portal")

        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if user == "admin" and pw == "earth123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Denied")
