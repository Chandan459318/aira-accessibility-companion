import streamlit as st
import sqlite3
from datetime import datetime
import os
from utils.sidebar import render_passenger_sidebar, render_crew_sidebar

# --- Auth Check ---
if not st.session_state.get("authenticated"):
    st.warning("⛔ Unauthorized access")
    st.stop()

# --- Role-Based Sidebar ---
role = st.session_state.get("role")
username = st.session_state.get("username")

if role == "Passenger":
    render_passenger_sidebar(username)
elif role == "Crew":
    render_crew_sidebar(username)

# --- Hide Default Sidebar Nav ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none !important; }
    html, body, [class*="stApp"] {
        background: linear-gradient(to right, #283e51, #485563);
        color: white;
    }
    .stTextInput>div>div>input,
    .stTextArea>div>textarea {
        background-color: #2e2e2e;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Page Header ---
st.title("🛫 Flight Info Update")

# --- DB Setup ---
os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/messages.db", check_same_thread=False)
c = conn.cursor()

# --- Message Type ---
update_type = st.radio("Choose update type", ["Boarding", "Landing & Luggage"])

# --- Input Fields ---
flight = st.text_input("Flight Number")
update_message = st.text_area("Enter update message (e.g., 'Boarding starts at Gate 12')")

# --- Submission ---
if st.button("📤 Send Update"):
    if flight.strip() and update_message.strip():
        tag = "[Boarding]" if update_type == "Boarding" else "[Landing]"
        full_message = f"{tag} {update_message.strip()}"

        try:
            c.execute("""
                INSERT INTO messages (flight, sender, receiver, message, status)
                VALUES (?, ?, ?, ?, ?)
            """, (flight.strip(), "Crew", "Passenger", full_message, "delivered"))
            conn.commit()
            st.success("✅ Update message sent to passengers.")
        except sqlite3.OperationalError as e:
            st.error(f"❌ Database error: {e}")
    else:
        st.warning("⚠️ Please fill in both Flight Number and Update Message.")

conn.close()
