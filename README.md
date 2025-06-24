# 🧠 NeuroNest - Memory Palace Builder

Transform your learning with AI-powered memory palaces that turn concepts into unforgettable visual journeys.

## 🌟 Features

- **AI-Powered Stories**: Convert any list of concepts into vivid, memorable stories using Google's Gemini AI
- **Interactive Quizzes**: Generate personalized quiz questions based on your memory palaces
- **Personal Library**: Save, organize, and revisit all your memory palaces in one place
- **User Authentication**: Secure user accounts with encrypted password storage
- **Responsive UI**: Beautiful, animated interface built with Streamlit

## 🚀 Quick Start

**Why uv?**
- **Faster**: 10-100x faster than pip for package resolution and installation
- **Better dependency resolution**: More reliable than pip
- **Built-in virtual environment management**: Simplifies project setup
- **Drop-in pip replacement**: Same commands, better performance

### Prerequisites

- Python 3.9+
- [uv package manager](https://github.com/astral-sh/uv)
- Google AI API key (Gemini)
- Supabase account and project

### Installation

1. **Install uv package manager** (if you haven't already)
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or via pip
   pip install uv
   ```

2. **Clone the repository**
   ```bash
   git clone https://github.com/serpentile-c137/NeuroNest.git
   cd neuronest
   ```

3. **Create virtual environment and install dependencies**
   ```bash
   # Create and activate virtual environment with Python 3.8+
   uv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   
   # Install dependencies
   uv pip install -r requirements.txt
   # Or if you alredy have pyptoject.toml
   uv sync

   # If you want to manually install
   uv add streamlit google-generativeai supabase python-dotenv bcrypt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in your project root:
   ```env
   GOOGLE_API_KEY=your_google_ai_api_key_here
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   ```

5. **Set up Supabase database**
   
   Create these tables in your Supabase dashboard:

   **Users table:**
   ```sql
   -- Create users table
    CREATE TABLE IF NOT EXISTS users (
        id BIGSERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
   ```

   **Palaces table:**
   ```sql
   -- Create palaces table
    CREATE TABLE IF NOT EXISTS palaces (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        concepts TEXT NOT NULL,
        story TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
   ```

   Enable Row Level Security (RLS) if needed for your use case.
   ```sql
    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
    CREATE INDEX IF NOT EXISTS idx_palaces_user_id ON palaces(user_id);
    CREATE INDEX IF NOT EXISTS idx_palaces_created_at ON palaces(created_at DESC);

    -- Enable Row Level Security (RLS)
    ALTER TABLE users ENABLE ROW LEVEL SECURITY;
    ALTER TABLE palaces ENABLE ROW LEVEL SECURITY;

    -- Create RLS policies
    -- Users can only see their own data
    CREATE POLICY "Users can view own profile" ON users
        FOR SELECT USING (auth.uid()::text = id::text);

    CREATE POLICY "Users can update own profile" ON users
        FOR UPDATE USING (auth.uid()::text = id::text);
   ```

6. **Run the application**
   ```bash
   # Make sure virtual environment is activated
   streamlit run app.py
   ```

## 📚 How It Works

### The Memory Palace Technique

NeuroNest uses the ancient "Method of Loci" or Memory Palace technique, enhanced with AI storytelling:

1. **Input Concepts**: Enter the topics you want to remember
2. **AI Story Generation**: Gemini AI creates a vivid, connected story
3. **Visual Memory**: The story creates mental images linking your concepts
4. **Reinforcement**: Quiz questions help strengthen the memory connections

### Example Usage

**Input concepts:**
```
Photosynthesis
Mitochondria
Streamlit
Generative AI
CrewAI, etc.
```

**AI generates a story** connecting these concepts in a memorable, visual narrative that's easy to recall.

## 🛠️ Project Structure

```
neuronest/
├── app.py              # Main Streamlit application
├── ai_agent.py         # AI integration (Gemini API)
├── db.py              # Database operations (Supabase)
├── .env               # Environment variables (create this)
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🔧 Configuration

### Required Dependencies

Create a `requirements.txt` file with:

```txt
streamlit
google-generativeai
supabase
python-dotenv
bcrypt
```

### API Keys Setup

1. **Google AI API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new API key
   - Add to your `.env` file

2. **Supabase Setup**:
   - Create a new project at [Supabase](https://supabase.com)
   - Get your project URL and anon key from Settings > API
   - Add to your `.env` file

## 🎨 Features Deep Dive

### Memory Palace Generation
- Uses Google's Gemini 1.5 Flash model for fast, creative story generation
- Optimized prompts for educational content and memory retention
- Handles 1-10 concepts per palace for optimal results

### User Management
- Secure password hashing with bcrypt
- Session management through Streamlit's session state
- User isolation - each user only sees their own palaces

### Interactive Quizzes
- Automatically generated based on the memory palace story
- Multiple choice format with 4 options per question
- Immediate feedback and learning reinforcement

## 🚀 Deployment

### Local Development
```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Run the application
streamlit run app.py
```

### Production Deployment
- Deploy to Streamlit Cloud, Heroku, or your preferred platform
- Ensure all environment variables are properly set
- Consider upgrading to Supabase Pro for production usage

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check that all environment variables are properly set
2. Verify your Google AI API key has sufficient quota
3. Ensure your Supabase database tables are created correctly
4. Check the console for any error messages

## 🔮 Future Enhancements

- [ ] Image generation for visual memory palaces
- [ ] Spaced repetition system for optimal review timing
- [ ] Mobile app version
- [ ] Collaborative memory palaces
- [ ] Advanced analytics and progress tracking
- [ ] Export functionality (PDF, text)
- [ ] Multiple AI model support

## 🏆 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Powered by [Google's Gemini AI](https://deepmind.google/technologies/gemini/) for story generation
- Database and authentication via [Supabase](https://supabase.com/)
- Inspired by the ancient Memory Palace technique used by memory champions

---

**Transform your learning today with NeuroNest!** 🧠✨
