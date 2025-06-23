import streamlit as st
from db import (
    init_db, create_user, authenticate,
    save_palace, get_palaces, get_palace_by_id, delete_palace
)
from ai_agent import generate_memory_palace

init_db()

# --- Dark Mode CSS + Navbar + Centered Container ---
st.markdown("""
<style>
body, .block-container {
    background: linear-gradient(to bottom right, #1e1e2f, #1a1a2b);
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
    max-width: 820px;
    margin: auto;
}

h1, h2, h3, h4, .title, .subtitle, label, .stRadio > div {
    color: #ffffff;
}

input, textarea, .stTextInput > div > input, .stTextArea > div > textarea {
    background-color: #121212 !important;
    color: #ffffff !important;
    border: 1px solid #444 !important;
    border-radius: 8px;
    padding: 0.5rem;
}

.stButton>button {
    background: linear-gradient(to right, #a855f7, #3b82f6);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    margin-top: 1rem;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: linear-gradient(to right, #9333ea, #2563eb);
    transform: scale(1.03);
}

.stMarkdown a {
    color: #a855f7 !important;
    font-weight: 500;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
    border-radius: 1rem;
    margin-bottom: 2rem;
}

.navbar h2 {
    margin: 0;
    font-size: 1.5rem;
    color: white;
}

.navbar a {
    margin-left: 1rem;
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: 0.3s;
}

.navbar a:hover {
    color: #a855f7;
}

.hero {
    text-align: center;
    padding: 4rem 2rem 2rem;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(to right, #a855f7, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    font-size: 1.25rem;
    color: #cccccc;
    max-width: 700px;
    margin: 1rem auto;
}

.input-card, .app-card {
    background-color: #21213a;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    margin: 2rem auto;
    width: 100%;
    max-width: 480px;
    animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.feature-section {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    padding: 2rem 0;
}

.feature-box {
    flex: 1 1 280px;
    background-color: #21213a;
    border-radius: 12px;
    padding: 1.5rem;
    color: #ffffff;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    animation: fadeIn 0.6s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

def navbar():
    st.markdown("""
    <div class='navbar'>
        <h2>🧠 NeuroNest</h2>
        <div>
            <a href='?page=auth'>Sign In</a>
            <a href='?page=signup'>Get Started</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def landing_page():
    navbar()
    st.markdown("""
    <div class="hero">
        <img src="https://img.icons8.com/ios-filled/100/brain.png" height="48">
        <h1>Transform Your Notes Into <span style="color:#3b82f6">Vivid Memory Palaces</span></h1>
        <p>Use AI-powered storytelling to turn any concept into an unforgettable visual journey. Remember more, forget less.</p>
        <a href="?page=auth"><button style='width:100%;margin-top:2rem;'>Sign In To Create</button></a>
    </div>

    <div class="feature-section">
        <div class="feature-box">
            <h3>🧠 AI-Powered Stories</h3>
            <p>Transform any concept into a vivid, memorable story using advanced AI that understands how memory works.</p>
        </div>
        <div class="feature-box">
            <h3>📖 Interactive Quizzes</h3>
            <p>Reinforce your memory with personalized recall questions that adapt to your learning progress.</p>
        </div>
        <div class="feature-box">
            <h3>👥 Personal Library</h3>
            <p>Build your collection of memory palaces and track your learning journey over time.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def login_ui():
    navbar()
    st.markdown("""
    <div class="input-card">
        <h2 style="text-align:center;">🔐 Welcome Back</h2>
        <p style="text-align:center; color: #bbb;">Sign in to access your memory palaces</p>
    """, unsafe_allow_html=True)
    username = st.text_input("Email", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Sign In"):
        user_id = authenticate(username, password)
        if user_id:
            st.session_state.user_id = user_id
            st.session_state.username = username
            st.query_params.clear()
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.markdown("<p style='text-align:center'>Don't have an account? <a href='?page=signup'>Sign Up</a></p></div>", unsafe_allow_html=True)

def signup_ui():
    navbar()
    st.markdown("""
    <div class="input-card">
        <h2 style="text-align:center;">✨ Create your NeuroNest account</h2>
    """, unsafe_allow_html=True)
    username = st.text_input("Choose a username", key="signup_user")
    password = st.text_input("Create a password", type="password", key="signup_pass")
    if st.button("Sign Up"):
        if create_user(username, password):
            st.success("Account created! Please log in.")
        else:
            st.error("Username already exists.")
    st.markdown("<p style='text-align:center'>Already have an account? <a href='?page=auth'>Login</a></p></div>", unsafe_allow_html=True)

def build_memory_palace_ui():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.subheader("🧠 Build a New Memory Palace")
    input_text = st.text_area("Concepts (one per line)", height=200, placeholder="e.g. Gravity\nPhotosynthesis\nMitochondria")
    if st.button("Generate Palace"):
        concepts = [c.strip() for c in input_text.splitlines() if c.strip()]
        if not concepts:
            st.warning("Please enter some concepts.")
        else:
            with st.spinner("Building your palace..."):
                story = generate_memory_palace(concepts, st.session_state.user_id)
                save_palace(st.session_state.user_id, concepts, story)
                palaces = get_palaces(st.session_state.user_id)
                if palaces:
                    st.session_state.selected_palace_id = palaces[0][0]
                st.success("Memory Palace created!")
    st.markdown('</div>', unsafe_allow_html=True)

def show_selected_palace(palace):
    if palace:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("📘 Memory Palace")
        st.markdown(f"**🕒 Created:** {palace[3]}")
        st.markdown(f"**🧩 Concepts:** {palace[1].replace(chr(10), ', ')}")
        st.markdown("---")
        st.markdown(palace[2], unsafe_allow_html=True)
        if st.button("🗑️ Delete This Palace"):
            delete_palace(palace[0], st.session_state.user_id)
            st.success("Palace deleted.")
            st.session_state.selected_palace_id = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def logout():
    st.session_state.clear()
    st.rerun()

def main():
    st.set_page_config(page_title="NeuroNest", layout="wide")

    query_params = st.query_params
    page = query_params.get("page", "home")

    if "user_id" not in st.session_state:
        if page == "auth":
            login_ui()
        elif page == "signup":
            signup_ui()
        else:
            landing_page()
    else:
        st.sidebar.markdown("## 📁 Your Palaces")
        st.sidebar.markdown(f"👤 {st.session_state.username}")

        palaces = get_palaces(st.session_state.user_id)
        options = ["(none)"] + [f"{p[3]} – {p[1].splitlines()[0][:30]}..." for p in palaces]
        choice = st.sidebar.selectbox("Select Palace", options)

        if choice != "(none)":
            idx = options.index(choice) - 1
            st.session_state.selected_palace_id = palaces[idx][0]
        elif "selected_palace_id" not in st.session_state:
            st.session_state.selected_palace_id = None

        if st.sidebar.button("🚪 Logout"):
            logout()

        st.title("🌌 NeuroNest – Your Memory Universe")
        build_memory_palace_ui()

        if st.session_state.get("selected_palace_id"):
            pal = get_palace_by_id(st.session_state.selected_palace_id)
            show_selected_palace(pal)

if __name__ == "__main__":
    main()
