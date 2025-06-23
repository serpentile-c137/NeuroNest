import streamlit as st
from db import (
    init_db, create_user, authenticate,
    save_palace, get_palaces, get_palace_by_id, delete_palace
)
from ai_agent import generate_memory_palace

init_db()

# --- Inject modern CSS ---
st.markdown(
    """
    <style>
    /* Page background and fonts */
    body, .block-container {
        background-color: #f5f7fa;
        color: #333;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4, h5 {
        font-family: 'Inter', sans-serif;
    }
    /* Main card styling */
    .app-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    /* Sidebar branding */
    .sidebar .sidebar-content {
        background-color: #1f2937;
        color: white;
    }
    .sidebar .sidebar-content h2 {
        color: #fff;
    }
    /* Button hover effect */
    .stButton>button:hover {
        background-color: #2563eb;
        border-color: #2563eb;
    }
    /* Centered login/signup */
    .centered-box {
        max-width: 480px;
        margin: auto;
        margin-top: 5rem;
    }
    </style>
    """, unsafe_allow_html=True
)

def login_ui():
    st.markdown('<div class="centered-box app-card">', unsafe_allow_html=True)
    st.markdown("## Welcome to **NeuroNest**")
    st.markdown("Log in to access your Memory Palaces:")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        user_id = authenticate(username, password)
        if user_id:
            st.session_state.user_id = user_id
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.markdown('</div>', unsafe_allow_html=True)

def signup_ui():
    st.markdown('<div class="centered-box app-card">', unsafe_allow_html=True)
    st.markdown("## Join **NeuroNest**")
    username = st.text_input("Choose a username", key="signup_user")
    password = st.text_input("Create a password", type="password", key="signup_pass")
    if st.button("Sign Up"):
        if create_user(username, password):
            st.success("Account created! Please log in.")
        else:
            st.error("Username already exists.")
    st.markdown('</div>', unsafe_allow_html=True)

def build_memory_palace_ui():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.subheader("🧠 Build a New Memory Palace")
    input_text = st.text_area("Enter concepts (one per line)", height=200, placeholder="e.g. Photosynthesis\nQuantum Mechanics")
    if st.button("Generate Palace"):
        concepts = [c.strip() for c in input_text.splitlines() if c.strip()]
        if not concepts:
            st.warning("Add at least one concept.")
        else:
            with st.spinner("Generating..."):
                story = generate_memory_palace(concepts, st.session_state.user_id)
                save_palace(st.session_state.user_id, concepts, story)
                palaces = get_palaces(st.session_state.user_id)
                if palaces:
                    st.session_state.selected_palace_id = palaces[0][0]
                st.success("🎉 Palace created!")
    st.markdown('</div>', unsafe_allow_html=True)

def show_selected_palace(palace):
    if palace:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("📚 Memory Palace")
        st.markdown(f"**Created at:** {palace[3]}")
        st.markdown(f"**Concepts:** {palace[1].replace(chr(10), ', ')}")
        st.markdown("---")
        st.markdown(palace[2], unsafe_allow_html=True)
        if st.button("🗑️ Delete This Palace"):
            delete_palace(palace[0], st.session_state.user_id)
            st.success("Palindrome deleted.")
            st.session_state.selected_palace_id = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def logout():
    st.session_state.clear()
    st.rerun()

def main():
    st.set_page_config(page_title="NeuroNest", layout="wide")
    if "user_id" not in st.session_state:
        action = st.radio("", ["Login", "Sign up"], horizontal=True)
        if action == "Login":
            login_ui()
        else:
            signup_ui()
    else:
        st.sidebar.markdown("# 🧠 NeuroNest")
        st.sidebar.markdown(f"**{st.session_state.username}**")
        st.sidebar.markdown("### 📂 My Palaces")

        palaces = get_palaces(st.session_state.user_id)
        options = ["(none)"] + [f"{p[3]} — {p[1].splitlines()[0][:30]}..." for p in palaces]
        choice = st.sidebar.selectbox("", options)

        if choice != "(none)":
            idx = options.index(choice) - 1
            st.session_state.selected_palace_id = palaces[idx][0]
        elif "selected_palace_id" not in st.session_state:
            st.session_state.selected_palace_id = None

        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout"):
            logout()

        st.title("🧠 NeuroNest – Memory Palace Builder")
        build_memory_palace_ui()

        if st.session_state.get("selected_palace_id"):
            pal = get_palace_by_id(st.session_state.selected_palace_id)
            show_selected_palace(pal)

if __name__ == "__main__":
    main()
