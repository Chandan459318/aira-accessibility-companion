import streamlit as st
import sqlite3
import os

from utils.sidebar import render_passenger_sidebar, render_crew_sidebar

# --- Access Control ---
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
    html, body, [class*="stApp"] {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .section {
        background: rgba(255,255,255,0.05);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- DB Setup ---
os.makedirs("data", exist_ok=True)

conn1 = sqlite3.connect("data/passengers.db")
c1 = conn1.cursor()
c1.execute("""
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
conn1.commit()

c1.execute("SELECT * FROM passengers")
passengers = c1.fetchall()

conn2 = sqlite3.connect("data/messages.db")
c2 = conn2.cursor()
c2.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight TEXT,
        sender TEXT,
        receiver TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn2.commit()

# --- Filters ---
st.header("📋 Passenger Support Requests")

flights = sorted({row[3] for row in passengers})
selected_flight = st.selectbox("✈️ Filter by Flight", flights) if flights else ""
needs = sorted({need for row in passengers for need in row[5].split(", ") if row[5]})
selected_need = st.selectbox("🧹 Filter by Need", ["All"] + needs) if needs else "All"

# --- Display Filtered Passengers ---
filtered = [
    row for row in passengers
    if row[3] == selected_flight and (selected_need == "All" or selected_need in row[5])
]

if filtered:
    st.dataframe({
        "Name": [row[2] for row in filtered],
        "Seat": [row[4] for row in filtered],
        "Accessibility Needs": [row[5] for row in filtered],
        "Notes": [row[6] for row in filtered],
        "Submitted At": [row[7] for row in filtered]
    }, use_container_width=True)
else:
    st.info("No matching passenger requests.")

# --- Priority Flags ---
st.subheader("🚨 Priority Passengers")
priority_tags = ["wheelchair", "pregnant", "elderly"]
for row in filtered:
    if any(tag in row[5].lower() for tag in priority_tags):
        st.error(f"🔴 {row[2]} - {row[5]} (Seat: {row[4]})")

# --- In-Flight Messages View ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.header("💬 In-Flight Passenger Messages")

c2.execute("""
    SELECT sender, message, timestamp FROM messages
    WHERE flight = ? AND receiver = 'Crew'
    ORDER BY timestamp DESC
    LIMIT 10
""", (selected_flight,))
msgs = c2.fetchall()

if msgs:
    for sender, msg, ts in msgs:
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.06); padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 0.5rem;'>
                <strong>{sender}</strong> <span style='float:right; font-size: 0.8rem;'>{ts}</span><br>
                {msg}
            </div>
        """, unsafe_allow_html=True)
else:
    st.caption("No passenger messages for this flight yet.")

st.markdown("</div>", unsafe_allow_html=True)

# --- Reply Section ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.header("✉️ Respond to Passenger Messages")

c2.execute("""
    SELECT id, sender, message, timestamp FROM messages
    WHERE flight = ? AND receiver = 'Crew'
    ORDER BY timestamp DESC
""", (selected_flight,))
incoming = c2.fetchall()

if incoming:
    for msg_id, sender, msg, ts in incoming:
        with st.expander(f"{sender} at {ts}"):
            st.write(msg)
            reply = st.text_area("Your Reply", key=f"reply_{msg_id}")

            if f"reply_sent_{msg_id}" not in st.session_state:
                st.session_state[f"reply_sent_{msg_id}"] = False

            if st.button("Send Reply", key=f"send_{msg_id}"):
                c2.execute("""
                    INSERT INTO messages (flight, sender, receiver, message)
                    VALUES (?, ?, ?, ?)
                """, (selected_flight, st.session_state["username"], sender, reply.strip()))
                conn2.commit()
                st.session_state[f"reply_sent_{msg_id}"] = True
                st.rerun()

            if st.session_state[f"reply_sent_{msg_id}"]:
                st.success("✅ Reply sent!")
                st.session_state[f"reply_sent_{msg_id}"] = False
else:
    st.caption("No passenger messages pending reply.")

st.markdown("</div>", unsafe_allow_html=True)

conn1.close()
conn2.close()
