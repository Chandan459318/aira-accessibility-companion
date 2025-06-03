import streamlit as st

def render_sidebar_header(username, role):
    st.sidebar.markdown(f"### 👋 Welcome, {username}")
    st.sidebar.markdown(f"**Role:** `{role}`")
    st.sidebar.markdown("---")
    if st.sidebar.button("🔓 Logout", key=f"logout_{username}"):
        for k in ["authenticated", "username", "role"]:
            st.session_state[k] = None
        st.switch_page("app.py")

def render_passenger_sidebar(username):
    render_sidebar_header(username, "Passenger")
    st.sidebar.page_link("pages/1_Passenger_Form.py", label="✍️ Travel Support Form")
    st.sidebar.page_link("pages/2_AI_Assistant.py", label="💬 AI Assistant")

def render_crew_sidebar(username):
    render_sidebar_header(username, "Crew")
    st.sidebar.page_link("pages/3_Crew_Dashboard.py", label="📋 Crew Dashboard")
    st.sidebar.page_link("pages/2_AI_Assistant.py", label="💬 AI Assistant")
    st.sidebar.page_link("pages/4_Flight_Info_Update.py", label="🛫 Flight Info Update")
