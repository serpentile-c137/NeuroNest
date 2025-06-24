import streamlit as st
from db import (
    init_db, create_user, authenticate,
    save_palace, get_palaces, get_palace_by_id, delete_palace
)
from ai_agent import generate_memory_palace

init_db()
st.set_page_config(page_title="NeuroNest", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "landing"

st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
    font-family: 'Inter', sans-serif;
}

.sidebar .css-1d391kg, .css-1d391kg {  /* Ensure sidebar is always styled */
    background-color: #111827 !important;
    color: white !important;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    color: white;
    padding: 1rem;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.2rem 2rem;
}
.navbar h1 {
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    margin: 0;
}
.navbar img { margin-right: 10px; }
.navbar a {
    margin-left: 1.5rem;
    text-decoration: none;
    color: white;
    font-weight: bold;
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
}
.navbar a:hover {
    color: #a855f7;
    background-color: #374151;
}

.stButton>button {
    background: linear-gradient(to right, #a855f7, #6366f1);
    color: white;
    font-weight: bold;
    border-radius: 8px;
}
.stButton>button:hover {
    background: linear-gradient(to right, #9333ea, #4f46e5);
}

.card {
    background-color: #111827;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4);
    color: white;
    max-width: 480px;
    margin: 4rem auto;
}

.auth-card {
    background-color: #111827;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4);
    color: white;
    max-width: 400px;
    margin: 2rem auto;
}

input, textarea {
    background-color: #1f2937 !important;
    color: white !important;
    border: 1px solid #4b5563 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}
.sidebar-palace-btn {
    background-color: #1f2937;
    color: white;
    border: 1px solid #4b5563;
    border-radius: 12px;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    text-align: left;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
}
.sidebar-palace-btn:hover {
    background-color: #374151;
    color: #a855f7;
}

/* Custom button styles for landing page */
.landing-button {
    padding: 1rem 2rem;
    font-size: 1rem;
    background: linear-gradient(to right, #a855f7, #6366f1);
    border: none;
    color: white;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
}

.cta-button {
    background-color: white;
    color: #4f46e5;
    padding: 0.75rem 1.5rem;
    font-weight: bold;
    border-radius: 8px;
    border: none;
    cursor: pointer;
}

/* Center the login/signup form */
.auth-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 70vh;
    padding: 2rem;
}
</style>
""", unsafe_allow_html=True)

def landing_page():
    # Create columns for the navbar buttons - keeping Sign In and Get Started close together
    col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
    
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; padding: 1.2rem 0;">
            <h1 style="font-size: 1.5rem; display: flex; align-items: center; margin: 0;">
                <img src="https://img.icons8.com/ios-filled/50/ffffff/brain.png" width="28" style="margin-right: 10px;"> 
                NeuroNest
            </h1>
        </div>
        """, unsafe_allow_html=True)
    
    # with col3:
    #     if st.button("Sign In", key="navbar_signin"):
    #         st.session_state.page = "auth"
    #         st.rerun()
    
    # with col4:
    #     if st.button("Get Started", key="navbar_getstarted"):
    #         st.session_state.page = "auth"
    #         st.rerun()
    
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 2rem;">
        <h1 style="font-size: 2.6rem; font-weight: 800;">Transform Your Notes Into <span style='color:#a855f7'>Vivid Memory <br>Palaces</span></h1>
        <p style="color: #d1d5db; font-size: 1.1rem;">Use AI-powered storytelling to turn any concept into an unforgettable visual journey. Remember more,<br> forget less.</p>
        <br>
        <form><input placeholder="What would you like to remember? (e.g., components of a plant cell)" style="padding: 1rem; width: 100%; max-width: 600px;"></form>
    </div>
    """, unsafe_allow_html=True)
    
    # Sign In To Create button - reduced width
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Sign In To Create", key="signin_to_create", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()
    
    st.markdown("""
    <div style="display: flex; justify-content: center; flex-wrap: wrap; margin-top: 1rem; gap: 2rem; padding: 0 2rem;">
        <div class="card" style="width: 300px; text-align: center;">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/storytelling.png" width="48" />
            <h3 style="color: #a855f7;">AI-Powered Stories</h3>
            <p>Turn concepts into vivid stories using AI trained on how memory works.</p>
        </div>
        <div class="card" style="width: 300px; text-align: center;">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/questions.png" width="48" />
            <h3 style="color: #a855f7;">Interactive Quizzes</h3>
            <p>Personalized questions that reinforce memory and track your learning.</p>
        </div>
        <div class="card" style="width: 300px; text-align: center;">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/books.png" width="48" />
            <h3 style="color: #a855f7;">Personal Library</h3>
            <p>Save, revisit, and organize your memory palaces in one place.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Final CTA section with Start Your Journey button inside the card
    st.markdown("""
    <div class="card" style="margin-top: 1rem; text-align: center;">
        <h2>Ready to Remember Everything?</h2>
        <p>Join thousands who've transformed their memory with NeuroNest.</p>
    """, unsafe_allow_html=True)
    
    # Start Your Journey button inside the card - reduced width
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Start Your Journey", key="start_journey", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Keep the original continue button as well
    # if st.button("Continue to Login / Signup"):
    #     st.session_state.page = "auth"
    #     st.rerun()

def login_signup_page():
    # Create a container to center the form
    # st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Use columns to center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.markdown("### Please SignUp or Login to Continue")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Sign In", use_container_width=True):
                user_id = authenticate(email, password)
                if user_id:
                    st.session_state.user_id = user_id
                    st.session_state.username = email
                    st.session_state.page = "app"
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        with tab2:
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_pass")
            if st.button("Sign Up", use_container_width=True):
                if create_user(email, password):
                    st.success("Account created! Please log in.")
                else:
                    st.error("Email already registered.")
        
        # Add a back to home button
        st.markdown("---")
        if st.button("← Back to Home", key="back_to_home", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def build_memory_palace_ui():
    st.subheader("🧠 Build a New Memory Palace")
    input_text = st.text_area(
        "Enter concepts (one per line)",
        height=100,
        placeholder="e.g. Photosynthesis\nQuantum Mechanics",
        label_visibility="collapsed"
    )
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
                st.rerun()

def show_selected_palace(palace):
    if palace:
        st.subheader("📚 Memory Palace")
        st.markdown(f"**Created at:** {palace[3]}")
        st.markdown(f"**Concepts:** {palace[1].replace(chr(10), ', ')}")
        st.markdown("---")
        st.markdown(palace[2], unsafe_allow_html=True)
        if st.button("🗑️ Delete This Palace"):
            delete_palace(palace[0], st.session_state.user_id)
            st.success("Palace deleted.")
            st.session_state.selected_palace_id = None
            st.rerun()

def logout():
    st.session_state.clear()
    st.session_state.page = "landing"
    st.rerun()

def main():
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "auth":
        login_signup_page()
    elif st.session_state.get("user_id") and st.session_state.page == "app":
        st.sidebar.markdown("# 🧠 NeuroNest")
        st.sidebar.markdown(f"**{st.session_state.username}**")
        st.sidebar.markdown("### 📂 My Palaces")
        palaces = get_palaces(st.session_state.user_id)

        for palace in palaces:
            label = f"🧠 {palace[3][:10]} — {palace[1].splitlines()[0][:25]}..."
            if st.sidebar.button(label, key=f"palace_{palace[0]}", help="Click to open", use_container_width=True):
                st.session_state.selected_palace_id = palace[0]
                st.rerun()

        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout"):
            logout()

        st.title("🧠 NeuroNest – Memory Palace Builder")
        build_memory_palace_ui()
        if st.session_state.get("selected_palace_id"):
            pal = get_palace_by_id(st.session_state.selected_palace_id)
            show_selected_palace(pal)
    else:
        st.session_state.page = "landing"
        st.rerun()

if __name__ == "__main__":
    main()