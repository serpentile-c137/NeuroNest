import streamlit as st
from db import (
    init_db, create_user, authenticate,
    save_palace, get_palaces, get_palace_by_id, delete_palace, get_user_by_id
)
from ai_agent import generate_memory_palace, generate_quiz_questions

# Initialize database connection
if init_db():
    print("✅ Connected to Supabase database")
else:
    print("❌ Failed to connect to database. Please check your Supabase configuration.")

st.set_page_config(
    page_title="NeuroNest", 
    layout="wide", 
    page_icon="🧠",
    initial_sidebar_state="collapsed"  # Start with sidebar collapsed on mobile
)

if "page" not in st.session_state:
    st.session_state.page = "landing"

st.markdown("""
<style>
/* Base responsive styles */
body, .stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
    font-family: 'Inter', sans-serif;
}

/* Mobile-first approach */
.main .block-container {
    padding: 1rem;
    max-width: 100%;
}

/* Responsive sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
    color: white;
    padding: 1rem;
}

[data-testid="stSidebar"] > div:first-child {
    width: 100%;
    min-width: 280px;
}

/* Animated Logo Styles - Responsive */
@keyframes float {
    0% { transform: translateY(0px) rotate(0deg); }
    33% { transform: translateY(-5px) rotate(3deg); }
    66% { transform: translateY(3px) rotate(-2deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}

@keyframes glow {
    0% { text-shadow: 0 0 5px #a855f7, 0 0 10px #a855f7, 0 0 15px #a855f7; }
    50% { text-shadow: 0 0 10px #6366f1, 0 0 20px #6366f1, 0 0 30px #6366f1; }
    100% { text-shadow: 0 0 5px #a855f7, 0 0 10px #a855f7, 0 0 15px #a855f7; }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.03); }
    100% { transform: scale(1); }
}

.animated-header {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem 0;
    margin-bottom: 1rem;
    text-align: center;
}

.animated-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}

.brain-icon {
    animation: float 3s ease-in-out infinite, pulse 2s ease-in-out infinite;
    filter: drop-shadow(0 0 10px #a855f7);
    width: 40px;
    height: 40px;
}

.app-title {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(45deg, #a855f7, #6366f1, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: glow 2s ease-in-out infinite alternate;
    letter-spacing: 1px;
    margin: 0;
}

/* Hero section responsive */
.hero-section {
    text-align: center;
    padding: 1rem;
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 1.8rem;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 1rem;
}

.hero-subtitle {
    color: #d1d5db;
    font-size: 1rem;
    line-height: 1.4;
    margin-bottom: 1.5rem;
}

.hero-input {
    width: 100%;
    max-width: 600px;
    padding: 1rem;
    margin: 0 auto;
    display: block;
    background-color: #1f2937 !important;
    color: white !important;
    border: 1px solid #4b5563 !important;
    border-radius: 8px !important;
    box-sizing: border-box;
}

/* Button styles - responsive */
.stButton > button {
    background: linear-gradient(to right, #a855f7, #6366f1);
    color: white;
    font-weight: bold;
    border-radius: 8px;
    width: 100%;
    padding: 0.75rem 1.5rem;
    border: none;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(to right, #9333ea, #4f46e5);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
}

/* Card styles - responsive */
.card {
    background-color: #111827;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4);
    color: white;
    margin: 1rem auto;
    width: 100%;
    box-sizing: border-box;
}

.feature-cards {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
    padding: 1rem;
    margin-top: 2rem;
}

.feature-card {
    background-color: #111827;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4);
    color: white;
    text-align: center;
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-card img {
    width: 48px;
    height: 48px;
    margin-bottom: 1rem;
}

.feature-card h3 {
    color: #a855f7;
    margin: 1rem 0 0.5rem 0;
    font-size: 1.2rem;
}

.feature-card p {
    margin: 0;
    line-height: 1.5;
    font-size: 0.9rem;
}

/* Auth card styles */
.auth-card {
    background-color: #111827;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4);
    color: white;
    max-width: 400px;
    margin: 2rem auto;
    width: 100%;
    box-sizing: border-box;
}

/* Form styles - responsive */
input, textarea, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background-color: #1f2937 !important;
    color: white !important;
    border: 1px solid #4b5563 !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
    width: 100% !important;
    box-sizing: border-box !important;
    font-size: 1rem !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #a855f7 !important;
    box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2) !important;
}

/* Sidebar styles - responsive */
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
    width: 100%;
    box-sizing: border-box;
    transition: all 0.3s ease;
}

.sidebar-palace-btn:hover {
    background-color: #374151;
    color: #a855f7;
    transform: translateX(3px);
}

/* Content sections - responsive */
.palace-content {
    background-color: #1f2937;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border-left: 4px solid #a855f7;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

.quiz-section {
    background-color: #0f172a;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid #334155;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

/* Success and error messages */
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

/* Tab styles */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    background-color: #1f2937;
    color: white;
    border-radius: 8px 8px 0 0;
    padding: 0.75rem 1rem;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background-color: #a855f7;
    color: white;
}

/* Mobile specific adjustments */
@media (max-width: 768px) {
    .main .block-container {
        padding: 0.5rem;
    }
    
    .brain-icon {
        width: 35px;
        height: 35px;
    }
    
    .app-title {
        font-size: 1.8rem;
    }
    
    .hero-title {
        font-size: 1.5rem;
    }
    
    .hero-subtitle {
        font-size: 0.9rem;
    }
    
    .card, .auth-card {
        padding: 1rem;
        margin: 0.5rem;
    }
    
    .feature-card {
        padding: 1rem;
    }
    
    .feature-card h3 {
        font-size: 1.1rem;
    }
    
    .palace-content, .quiz-section {
        padding: 1rem;
    }
    
    /* Ensure sidebar is properly sized on mobile */
    [data-testid="stSidebar"] > div:first-child {
        min-width: 250px;
    }
}

/* Tablet adjustments */
@media (min-width: 769px) and (max-width: 1024px) {
    .feature-cards {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .brain-icon {
        width: 50px;
        height: 50px;
    }
    
    .app-title {
        font-size: 2.2rem;
    }
    
    .hero-title {
        font-size: 2rem;
    }
}

/* Desktop adjustments */
@media (min-width: 1025px) {
    .feature-cards {
        grid-template-columns: repeat(3, 1fr);
        max-width: 1200px;
        margin: 2rem auto;
    }
    
    .brain-icon {
        width: 60px;
        height: 60px;
    }
    
    .app-title {
        font-size: 2.5rem;
    }
    
    .hero-title {
        font-size: 2.6rem;
    }
    
    .hero-section {
        padding: 2rem;
    }
    
    .card {
        max-width: 480px;
    }
}

/* Large desktop adjustments */
@media (min-width: 1440px) {
    .main .block-container {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .hero-title {
        font-size: 3rem;
    }
    
    .app-title {
        font-size: 3rem;
    }
}

/* Print styles */
@media print {
    .animated-header, .stButton, .stSidebar {
        display: none !important;
    }
    
    .palace-content, .quiz-section {
        background-color: white !important;
        color: black !important;
        border: 1px solid #333 !important;
    }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    .card, .auth-card, .feature-card {
        border: 2px solid #ffffff;
    }
    
    .stButton > button {
        border: 2px solid #ffffff;
    }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
    .brain-icon {
        animation: none;
    }
    
    .app-title {
        animation: none;
    }
    
    .stButton > button:hover {
        transform: none;
    }
    
    .feature-card:hover {
        transform: none;
    }
}

/* Focus styles for accessibility */
.stButton > button:focus,
input:focus,
textarea:focus {
    outline: 2px solid #a855f7;
    outline-offset: 2px;
}

/* Ensure text remains readable */
* {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Responsive utilities */
.mobile-hide {
    display: block;
}

.mobile-show {
    display: none;
}

@media (max-width: 768px) {
    .mobile-hide {
        display: none;
    }
    
    .mobile-show {
        display: block;
    }
}
</style>
""", unsafe_allow_html=True)

def landing_page():
    """Landing page with hero section and features"""
    # Animated Header with centered logo
    st.markdown("""
    <div class="animated-header">
        <div class="animated-logo">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/brain.png" class="brain-icon" alt="Brain Icon"> 
            <h1 class="app-title">NeuroNest</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Transform Your Notes Into <span style='color:#a855f7'>Vivid Memory Palaces</span></h1>
        <p class="hero-subtitle">Use AI-powered storytelling to turn any concept into an unforgettable visual journey. Remember more, forget less.</p>
        <input class="hero-input" placeholder="What would you like to remember? (e.g., components of a plant cell)" readonly>
    </div>
    """, unsafe_allow_html=True)
    
    # Responsive button layout
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Sign In To Create", key="signin_to_create", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()
    
    # Feature cards with responsive grid
    st.markdown("""
    <div class="feature-cards">
        <div class="feature-card">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/storytelling.png" alt="Storytelling Icon" />
            <h3>AI-Powered Stories</h3>
            <p>Turn concepts into vivid stories using AI trained on how memory works.</p>
        </div>
        <div class="feature-card">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/questions.png" alt="Questions Icon" />
            <h3>Interactive Quizzes</h3>
            <p>Personalized questions that reinforce memory and track your learning.</p>
        </div>
        <div class="feature-card">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/books.png" alt="Books Icon" />
            <h3>Personal Library</h3>
            <p>Save, revisit, and organize your memory palaces in one place.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div class="card" style="text-align: center; margin-top: 2rem;">
        <h2>Ready to Remember Everything?</h2>
        <p>Join thousands who've transformed their memory with NeuroNest.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Your Journey", key="start_journey", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()

def login_signup_page():
    """Login and signup page"""
    # Animated Header for auth page too
    st.markdown("""
    <div class="animated-header">
        <div class="animated-logo">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/brain.png" class="brain-icon" alt="Brain Icon"> 
            <h1 class="app-title">NeuroNest</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Responsive layout for auth
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    
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
        
        # Responsive layout for palace info
        col1, col2 = st.columns([2, 1])
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
        
        # Display the palace story with responsive container
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
    with st.sidebar:
        st.markdown("# 🧠 NeuroNest")
        
        # User info
        user_info = get_user_by_id(st.session_state.user_id)
        if user_info:
            st.markdown(f"**Welcome, {user_info['username']}!**")
        
        st.markdown("### 📂 My Memory Palaces")
        
        palaces = get_palaces(st.session_state.user_id)
        
        if not palaces:
            st.info("No memory palaces yet. Create your first one!")
        else:
            for palace in palaces:
                # Create a shorter label for the sidebar
                date_str = palace[3][:10]  # Just the date part
                first_concept = palace[1].split('\n')[0][:20]
                if len(palace[1].split('\n')[0]) > 20:
                    first_concept += "..."
                
                label = f"🏰 {date_str}\n{first_concept}"
                
                if st.button(
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
        
        st.markdown("---")
        st.markdown(f"**Total Palaces:** {len(palaces)}")
        
        if st.button("🚪 Logout", use_container_width=True):
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