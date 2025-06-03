import streamlit as st
import sqlite3
import os


from utils.sidebar import render_passenger_sidebar, render_crew_sidebar

if not st.session_state.get("authenticated"):
    st.warning("⛔ Unauthorized access")
    st.stop()

role = st.session_state.get("role")
username = st.session_state.get("username")

if role == "Passenger":
    render_passenger_sidebar(username)
elif role == "Crew":
    render_crew_sidebar(username)

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)


# --- AUTH GUARD ---
#if not st.session_state.get("authenticated") or st.session_state.get("role") != "Passenger":
#    st.warning("⛔ Unauthorized Access. Please log in as a Passenger.")
#    st.stop()

# --- STYLE ---
#st.set_page_config(page_title="Passenger Form", layout="centered")

st.markdown("""
    <style>
    html, body, [class*="stApp"] {
        background: linear-gradient(to right, #1e3c72, #2a5298);
        font-family: 'Segoe UI', sans-serif;
        color: white;
    }
    .form-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem 2.5rem;
        border-radius: 10px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
        width: 100%;
        max-width: 600px;
        margin: auto;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .form-header {
        font-size: 1.8rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1.2rem;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# --- DB Setup ---
os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/passengers.db")
c = conn.cursor()
#c.execute("DROP TABLE IF EXISTS passengers")
c.execute("""

    CREATE TABLE IF NOT EXISTS passengers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        name TEXT,
        flight TEXT,
        seat TEXT,
        accessibility_needs TEXT,
        assistance_notes TEXT,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# --- UI ---
#st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="form-header">🧑‍✈️ AIRA Travel Support Form</div>', unsafe_allow_html=True)

with st.form("passenger_form"):
    name = st.text_input("Full Name")
    flight = st.text_input("Flight Number (e.g., UA1234)")
    seat = st.text_input("Seat Number")
    needs = st.multiselect(
        "Accessibility Needs",
        [
            "Wheelchair assistance",
            "Hearing impairment support",
            "Visual impairment support",
            "Elderly passenger",
            "Pregnant passenger",
            "Injury recovery",
            "Autism/sensory sensitivity",
            "First-time flyer/anxiety",
            "Other"
        ]
    )
    notes = st.text_area("Additional Notes (Optional)")
    submitted = st.form_submit_button("Submit")

    if submitted:
        c.execute("""
            INSERT INTO passengers (username, name, flight, seat, accessibility_needs, assistance_notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            st.session_state["username"],
            name, flight, seat,
            ", ".join(needs), notes
        ))
        conn.commit()
        st.success("✅ Travel support request submitted successfully!")

st.markdown('</div>', unsafe_allow_html=True)
conn.close()
