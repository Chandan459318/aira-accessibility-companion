import streamlit as st
import sqlite3
import hashlib
import time

# --- Page Config ---
st.set_page_config(page_title="AIRA - Accessibility Companion", layout="wide")

# --- Creative CSS Styling ---
st.markdown("""
    <style>
    html, body, [class*="stApp"] {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        font-family: 'Segoe UI', sans-serif;
        color: white;
    }

    [data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="stSidebarNavItems"] {
        display: none !important;
    }

    .centered-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .login-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
        width: 100%;
        max-width: 420px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.1);
        transition: 0.3s ease;
    }

    .login-box:hover {
        box-shadow: 0 0 25px rgba(255,255,255,0.2);
    }

    .login-header {
        font-size: 1.7rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #ffffff;
        text-align: center;
    }

    button[kind="secondary"] {
        color: white !important;
        background-color: transparent !important;
        border: 1px solid white !important;
    }

    button[kind="secondary"]:hover {
        background-color: rgba(255,255,255,0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session Defaults ---
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("role", None)
st.session_state.setdefault("username", None)
st.session_state.setdefault("show_register", False)

# --- Helpers ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(username, password):
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def register_user(username, password, role):
    conn = sqlite3.connect("data/users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )""")
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  (username, hash_password(password), role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# --- Registration ---
if st.session_state["show_register"]:
    #st.markdown('<div class="centered-container"><div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-header">📝 Register</div>', unsafe_allow_html=True)
    with st.form("register_form"):
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        new_role = st.selectbox("Select Role", ["Passenger", "Crew"])
        if st.form_submit_button("Register"):
            if register_user(new_user, new_pass, new_role):
                st.success("✅ Registration successful! Please log in.")
                time.sleep(2)
                st.session_state["show_register"] = False
                st.rerun()
            else:
                st.error("❌ Username already exists.")
    if st.button("🔙 Back to Login"):
        st.session_state["show_register"] = False
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- Login ---
elif not st.session_state["authenticated"]:
    #st.markdown('<div class="centered-container"><div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-header">🔐 Login to AIRA</div>', unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            role = verify_login(username, password)
            if role:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["role"] = role
                st.rerun()
            else:
                st.error("❌ Invalid credentials.")
    if st.button("Don't have an account? Register"):
        st.session_state["show_register"] = True
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- Redirect after login ---
else:
    role = st.session_state["role"]
    if role == "Passenger":
        st.switch_page("pages/1_Passenger_Form.py")
    elif role == "Crew":
        st.switch_page("pages/3_Crew_Dashboard.py")
