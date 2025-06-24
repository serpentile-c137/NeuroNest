import streamlit as st
from db import (
    init_db, create_user, authenticate,
    save_palace, get_palaces, get_palace_by_id, delete_palace, get_user_by_id
)
from ai_agent import generate_memory_palace, generate_quiz_questions

# Initialize database connection
if init_db():
    # st.success("✅ Connected to Supabase database", icon="✅")
    print("✅ Connected to Supabase database")
else:
    print("❌ Failed to connect to database. Please check your Supabase configuration.")
    # st.error("❌ Failed to connect to database. Please check your Supabase configuration.", icon="❌")

st.set_page_config(page_title="NeuroNest", layout="wide", page_icon="🧠")

if "page" not in st.session_state:
    st.session_state.page = "landing"

st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
    font-family: 'Inter', sans-serif;
}

.sidebar .css-1d391kg, .css-1d391kg {
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

.success-message {
    background-color: #10b981;
    color: white;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.error-message {
    background-color: #ef4444;
    color: white;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.palace-content {
    background-color: #1f2937;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border-left: 4px solid #a855f7;
}

.quiz-section {
    background-color: #0f172a;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

def landing_page():
    """Landing page with hero section and features"""
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
    
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 2rem;">
        <h1 style="font-size: 2.6rem; font-weight: 800;">Transform Your Notes Into <span style='color:#a855f7'>Vivid Memory <br>Palaces</span></h1>
        <p style="color: #d1d5db; font-size: 1.1rem;">Use AI-powered storytelling to turn any concept into an unforgettable visual journey. Remember more,<br> forget less.</p>
        <br>
        <form><input placeholder="What would you like to remember? (e.g., components of a plant cell)" style="padding: 1rem; width: 100%; max-width: 600px;"></form>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    st.markdown("""
    <div class="card" style="margin-top: 1rem; text-align: center;">
        <h2>Ready to Remember Everything?</h2>
        <p>Join thousands who've transformed their memory with NeuroNest.</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Start Your Journey", key="start_journey", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def login_signup_page():
    """Login and signup page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Please SignUp or Login to Continue")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_pass")
                login_button = st.form_submit_button("Sign In", use_container_width=True)
                
                if login_button:
                    if not email or not password:
                        st.error("Please fill in all fields")
                    else:
                        with st.spinner("Authenticating..."):
                            user_id = authenticate(email, password)
                            if user_id:
                                st.session_state.user_id = user_id
                                st.session_state.username = email
                                st.session_state.page = "app"
                                st.success("Login successful!")
                                st.rerun()
                            else:
                                st.error("Invalid credentials. Please check your email and password.")
        
        with tab2:
            with st.form("signup_form"):
                email = st.text_input("Email", key="signup_email")
                password = st.text_input("Password", type="password", key="signup_pass")
                confirm_password = st.text_input("Confirm Password", type="password", key="confirm_pass")
                signup_button = st.form_submit_button("Sign Up", use_container_width=True)
                
                if signup_button:
                    if not email or not password or not confirm_password:
                        st.error("Please fill in all fields")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        with st.spinner("Creating account..."):
                            if create_user(email, password):
                                st.success("Account created successfully! Please log in.")
                            else:
                                st.error("Email already registered or error creating account.")
        
        st.markdown("---")
        if st.button("← Back to Home", key="back_to_home", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

def build_memory_palace_ui():
    """UI for building a new memory palace"""
    st.subheader("🧠 Build a New Memory Palace")
    
    with st.form("palace_form"):
        input_text = st.text_area(
            "Enter concepts (one per line)",
            height=100,
            placeholder="e.g.\nPhotosynthesis\nQuantum Mechanics\nMitochondria\nDNA Structure",
            help="Enter each concept on a new line. The AI will create a story connecting all concepts."
        )
        
        generate_button = st.form_submit_button("🏰 Generate Palace", use_container_width=True)
        
        if generate_button:
            concepts = [c.strip() for c in input_text.splitlines() if c.strip()]
            if not concepts:
                st.warning("⚠️ Please add at least one concept.")
            elif len(concepts) > 10:
                st.warning("⚠️ Please limit to 10 concepts for optimal results.")
            else:
                with st.spinner("🤖 AI is creating your memory palace..."):
                    story = generate_memory_palace(concepts, st.session_state.user_id)
                    if save_palace(st.session_state.user_id, concepts, story):
                        st.success("🎉 Memory palace created successfully!")
                        
                        # Auto-select the newly created palace
                        palaces = get_palaces(st.session_state.user_id)
                        if palaces:
                            st.session_state.selected_palace_id = palaces[0][0]
                        st.rerun()
                    else:
                        st.error("❌ Failed to save memory palace. Please try again.")

def show_selected_palace(palace):
    """Display the selected memory palace"""
    if palace:
        st.subheader("📚 Memory Palace")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Created:** {palace[3][:19].replace('T', ' ')}")
            concepts_list = palace[1].replace('\n', ', ')
            st.markdown(f"**Concepts:** {concepts_list}")
        
        with col2:
            if st.button("🗑️ Delete Palace", key="delete_palace"):
                if delete_palace(palace[0], st.session_state.user_id):
                    st.success("🗑️ Palace deleted successfully!")
                    st.session_state.selected_palace_id = None
                    st.rerun()
                else:
                    st.error("❌ Failed to delete palace.")
        
        st.markdown("---")
        
        # Display the palace story
        # st.markdown('<div class="palace-content">', unsafe_allow_html=True)
        st.markdown(palace[2])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quiz section
        st.markdown("### 🧩 Test Your Memory")
        if st.button("📝 Generate Quiz Questions", key="generate_quiz"):
            with st.spinner("Creating quiz questions..."):
                concepts = palace[1].split('\n')
                quiz = generate_quiz_questions(concepts, palace[2])
                st.session_state.current_quiz = quiz
                st.rerun()
        
        if hasattr(st.session_state, 'current_quiz') and st.session_state.current_quiz:
            # st.markdown('<div class="quiz-section">', unsafe_allow_html=True)
            st.markdown(st.session_state.current_quiz)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🔄 Clear Quiz", key="clear_quiz"):
                if hasattr(st.session_state, 'current_quiz'):
                    del st.session_state.current_quiz
                st.rerun()

def sidebar_navigation():
    """Sidebar with navigation and palace list"""
    st.sidebar.markdown("# 🧠 NeuroNest")
    
    # User info
    user_info = get_user_by_id(st.session_state.user_id)
    if user_info:
        st.sidebar.markdown(f"**Welcome, {user_info['username']}!**")
    
    st.sidebar.markdown("### 📂 My Memory Palaces")
    
    palaces = get_palaces(st.session_state.user_id)
    
    if not palaces:
        st.sidebar.info("No memory palaces yet. Create your first one!")
    else:
        for palace in palaces:
            # Create a shorter label for the sidebar
            date_str = palace[3][:10]  # Just the date part
            first_concept = palace[1].split('\n')[0][:20]
            if len(palace[1].split('\n')[0]) > 20:
                first_concept += "..."
            
            label = f"🏰 {date_str}\n{first_concept}"
            
            if st.sidebar.button(
                label, 
                key=f"palace_{palace[0]}", 
                help=f"Concepts: {palace[1].replace(chr(10), ', ')}", 
                use_container_width=True
            ):
                st.session_state.selected_palace_id = palace[0]
                # Clear any existing quiz when switching palaces
                if hasattr(st.session_state, 'current_quiz'):
                    del st.session_state.current_quiz
                st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Total Palaces:** {len(palaces)}")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout()

def logout():
    """Clear session and return to landing page"""
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.page = "landing"
    st.rerun()

def main():
    """Main application logic"""
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "auth":
        login_signup_page()
    elif st.session_state.get("user_id") and st.session_state.page == "app":
        # Main app interface
        sidebar_navigation()
        
        st.title("🧠 NeuroNest – Memory Palace Builder")
        st.markdown("*Transform your learning with AI-powered memory palaces*")
        
        # Main content area
        build_memory_palace_ui()
        
        # Show selected palace if any
        if st.session_state.get("selected_palace_id"):
            palace = get_palace_by_id(st.session_state.selected_palace_id)
            if palace:
                show_selected_palace(palace)
            else:
                st.error("Palace not found or deleted.")
                st.session_state.selected_palace_id = None
    else:
        # Default fallback
        st.session_state.page = "landing"
        st.rerun()

if __name__ == "__main__":
    main()