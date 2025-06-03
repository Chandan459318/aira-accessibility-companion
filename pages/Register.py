# pages/Register.py

import streamlit as st
import sqlite3
import hashlib
import time


# --- Page Setup ---
st.set_page_config(page_title="Register - AIRA", page_icon="📝", layout="centered")

# --- Hide sidebar and default nav ---
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
            display: none !important;
        }
        #MainMenu, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# Hashing password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register new user
def register_user(username, password, role):
    try:
        conn = sqlite3.connect("data/users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  (username, hash_password(password), role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# UI
st.title("📝 Register New User")
st.write("Create a new Passenger or Crew account below.")

with st.form("register_form"):
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    role = st.selectbox("Select Role", ["Passenger", "Crew"])
    submit = st.form_submit_button("Register")

    if submit:
        if not username or not password:
            st.warning("Please fill in all fields.")
        else:
            success = register_user(username, password, role)
            if success:
                st.success("✅ Registration successful! You can now log in from the main page.")
                time.sleep(2)  # short delay so user sees the success message
                st.switch_page("app.py")
            else:
                st.error("❌ Username already exists. Please choose a different one.")
