import streamlit as st
import sqlite3
from datetime import datetime
import os

from utils.sidebar import render_passenger_sidebar, render_crew_sidebar

# --- Auth Check ---
if not st.session_state.get("authenticated"):
    st.warning("⛔ Unauthorized access")
    st.stop()

role = st.session_state.get("role")
username = st.session_state.get("username")

# --- Sidebar ---
if role == "Passenger":
    render_passenger_sidebar(username)
elif role == "Crew":
    render_crew_sidebar(username)

# --- Hide Native Sidebar ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- Page Styles ---
st.markdown("""
    <style>
    html, body, [class*="stApp"] {
        background: linear-gradient(to right, #283e51, #485563);
        color: white;
    }
    .assistant-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        max-width: 720px;
        margin: auto;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
    }
    .header-title {
        font-size: 1.6rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        color: #ffffff;
    }
    .suggestion-box {
        margin: 0.5rem 0;
    }
    .suggestion-box button {
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- DB Setup ---
os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/messages.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight TEXT,
        sender TEXT,
        receiver TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# --- Header ---
st.markdown('<div class="header-title">🤖 AIRA Smart Assistant</div>', unsafe_allow_html=True)

# --- Flight Number ---
flight = st.text_input("Your Flight Number (e.g., UA1234)")

# --- Messaging Form ---
st.markdown("----")
st.subheader("💬 Message")

with st.form("message_form", clear_on_submit=True):
    default_msg = st.session_state.get("msg_box", "")
    user_input = st.text_area("Type your message to the crew..." if role == "Passenger" else "Respond to passenger...", value=default_msg, key="msg_box_input")
    send_btn = st.form_submit_button("Send")

    if send_btn:
        if flight.strip() and user_input.strip():
            receiver = "Crew" if role == "Passenger" else "Passenger"
            c.execute("""
                INSERT INTO messages (flight, sender, receiver, message)
                VALUES (?, ?, ?, ?)
            """, (flight.strip(), username, receiver, user_input.strip()))
            conn.commit()
            st.success("✅ Message sent successfully.")
            st.session_state["msg_box"] = ""  # Reset smart suggestion after send
        else:
            st.warning("⚠️ Please enter both flight number and message.")

# --- Smart Suggestion Engine ---
def generate_suggestions(text):
    text = text.lower()
    suggestions = []
    if "wheelchair" in text:
        suggestions.append("A wheelchair will be arranged for you at the gate.")
    if "baggage" in text or "luggage" in text:
        suggestions.append("Baggage info will be shared after landing.")
    if any(w in text for w in ["anxious", "scared", "nervous"]):
        suggestions.append("Would you like the crew to check in with you?")
    if "pregnant" in text:
        suggestions.append("We’ll ensure you receive priority boarding assistance.")
    if "autism" in text or "sensory" in text:
        suggestions.append("We’ll minimize noise and help make you comfortable.")
    if "first time" in text or "nervous flyer" in text:
        suggestions.append("We’re here to make your first flight easy and safe.")
    return suggestions

# --- Show Messages ---
st.markdown("---")
st.subheader("📨 Conversation History")

if flight.strip():
    c.execute("""
        SELECT sender, message, timestamp FROM messages
        WHERE flight = ?
        ORDER BY timestamp DESC
        LIMIT 10
    """, (flight.strip(),))
    rows = c.fetchall()

    if rows:
        for sender, msg, ts in rows:
            st.markdown(f"""
                <div style='padding: 0.5rem 1rem; margin-bottom: 0.5rem; background: rgba(255,255,255,0.06); border-radius: 6px;'>
                    <strong>{sender}</strong> <span style='float:right; font-size: 0.8rem;'>{ts}</span><br>
                    {msg}
                </div>
            """, unsafe_allow_html=True)

            # --- Smart Suggestions (Crew only for passenger messages) ---
            if role == "Crew" and sender != username:
                st.markdown("<div class='suggestion-box'><b>💡 Smart Suggestions:</b><br>", unsafe_allow_html=True)
                for suggestion in generate_suggestions(msg):
                    if st.button(suggestion, key=suggestion):
                        st.session_state["msg_box"] = suggestion
                        st.experimental_rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No messages yet.")
else:
    st.info("✈️ Please enter/select a flight number above to view messages.")

st.markdown('</div>', unsafe_allow_html=True)
conn.close()
