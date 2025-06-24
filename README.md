# 🧠 NeuroNest - Memory Palace Builder

Transform your learning with AI-powered memory palaces that turn concepts into unforgettable visual journeys.

## 🌟 Features

- **AI-Powered Stories**: Convert any list of concepts into vivid, memorable stories using Google's Gemini AI
- **Personal Library**: Save, organize, and revisit all your memory palaces in one place
- **User Authentication**: Secure user accounts with encrypted password storage using SQLite
- **Responsive UI**: Beautiful, animated interface built with Streamlit
- **Local Database**: All data stored locally using SQLite - no external dependencies

## 🚀 Quick Start

**Why uv?**
- **Faster**: 10-100x faster than pip for package resolution and installation
- **Better dependency resolution**: More reliable than pip
- **Built-in virtual environment management**: Simplifies project setup
- **Drop-in pip replacement**: Same commands, better performance

### Prerequisites

- Python 3.9+
- [uv package manager](https://github.com/astral-sh/uv) (recommended) or pip
- Google AI API key (Gemini)

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
   git clone https://github.com/your-username/NeuroNest.git
   cd NeuroNest
   ```

3. **Create virtual environment and install dependencies**
   ```bash
   # Create and activate virtual environment with Python 3.9+
   uv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   
   # Install dependencies
   uv pip install streamlit google-generativeai python-dotenv
   ```

   **Alternative with pip:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install streamlit google-generativeai python-dotenv
   ```

4. **Set up environment variables**
   
   Create a `.env` file in your project root:
   ```env
   GOOGLE_API_KEY=your_google_ai_api_key_here
   ```

5. **Get your Google AI API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new API key
   - Add it to your `.env` file

6. **Run the application**
   ```bash
   # Make sure virtual environment is activated
   streamlit run app.py
   ```

   The app will automatically create the SQLite database (`neuronest.db`) on first run.

## 📚 How It Works

### The Memory Palace Technique

NeuroNest uses the ancient "Method of Loci" or Memory Palace technique, enhanced with AI storytelling:

1. **Input Concepts**: Enter the topics you want to remember (one per line)
2. **AI Story Generation**: Gemini AI creates a vivid, connected story placing concepts in different "rooms"
3. **Visual Memory**: The story creates mental images linking your concepts in a memorable palace
4. **Personal Library**: All your palaces are saved locally for easy access and review

### Example Usage

**Input concepts:**
```
Photosynthesis
Mitochondria
Cell Membrane
Chloroplast
DNA
```

**AI generates a story** like:
> **Room 1: The Sunlight Kitchen**
> In the first room of your memory palace, you walk into a bright kitchen where **Photosynthesis** is the chef. She's a green-skinned woman wearing a apron made of leaves, frantically cooking using only sunlight as her heat source...

The story continues, connecting each concept in a memorable, visual narrative.

## 🛠️ Project Structure

```
NeuroNest/
├── app.py              # Main Streamlit application & UI
├── ai_agent.py         # AI integration (Gemini API)
├── db.py              # SQLite database operations
├── .env               # Environment variables (create this)
├── neuronest.db       # SQLite database (auto-created)
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 📁 Database Schema

The SQLite database automatically creates two tables:

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
)
```

### Palaces Table
```sql
CREATE TABLE palaces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    concepts TEXT,
    story TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```

## 🔧 Configuration

### Required Dependencies

Create a `requirements.txt` file with:
```txt
streamlit>=1.28.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

### Environment Variables

Only one environment variable is required:
- `GOOGLE_API_KEY`: Your Google AI Studio API key

## 🎨 Features Deep Dive

### Memory Palace Generation
- **AI Model**: Uses Google's Gemini 1.5 Flash 8B for fast, creative story generation
- **Optimized Prompts**: Specifically designed for educational content and memory retention
- **Room-based Structure**: Organizes concepts into different "rooms" for better spatial memory
- **Handles 1-10+ concepts**: Optimal results with any number of concepts

### User Management
- **Secure Authentication**: Password hashing using SHA-256
- **Session Management**: Streamlit session state for user persistence
- **User Isolation**: Each user only sees their own memory palaces
- **Local Storage**: All data stored in local SQLite database

### User Interface
- **Modern Design**: Gradient backgrounds, custom styling, and smooth interactions
- **Responsive Layout**: Works on desktop and mobile devices
- **Landing Page**: Professional landing page with feature highlights
- **Sidebar Navigation**: Easy access to all your saved palaces
- **Real-time Updates**: Instant palace generation and saving

## 🚀 Usage Guide

### Creating Your First Memory Palace

1. **Sign Up/Login**: Create an account or login to existing account
2. **Enter Concepts**: In the text area, enter each concept on a new line
3. **Generate Palace**: Click "Generate Palace" and wait for AI to create your story
4. **Review**: Read through your personalized memory palace story
5. **Save**: Your palace is automatically saved to your personal library

### Managing Your Palaces

- **View All Palaces**: Check the sidebar for all your saved palaces
- **Quick Preview**: Palace buttons show creation date and first concept
- **Delete Palaces**: Remove unwanted palaces with the delete button
- **Instant Access**: Click any palace in the sidebar to view it immediately

## 🚀 Deployment

### Local Development
```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Run the application
streamlit run app.py
```

### Production Deployment

#### Streamlit Cloud
1. Push your code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your `GOOGLE_API_KEY` in the app settings
4. Deploy!

#### Other Platforms
- **Heroku**: Add `GOOGLE_API_KEY` to config vars
- **Railway**: Set environment variable in dashboard
- **Render**: Configure environment variable in service settings

## 🔍 Troubleshooting

### Common Issues

1. **"Invalid API Key" Error**
   - Verify your Google AI API key is correct in the `.env` file
   - Check that you have quota remaining on your Google AI account

2. **Database Errors**
   - Delete `neuronest.db` file and restart the app to recreate the database
   - Ensure you have write permissions in the project directory

3. **Import Errors**
   - Make sure all dependencies are installed: `uv pip install -r requirements.txt`
   - Verify you're using the correct virtual environment

4. **Streamlit Issues**
   - Clear browser cache and cookies
   - Try running in incognito/private mode
   - Check console for JavaScript errors

### Performance Tips

- **Concept Limit**: For best results, use 2-8 concepts per palace
- **Clear Concepts**: Use simple, clear concept names for better AI understanding  
- **Regular Cleanup**: Delete unused palaces to keep your library organized

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/NeuroNest.git
cd NeuroNest

# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install streamlit google-generativeai python-dotenv

# Create .env file with your API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# Run in development mode
streamlit run app.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Future Enhancements

- [ ] **Interactive Quizzes**: Generate quiz questions based on memory palaces
- [ ] **Image Generation**: Visual representations of memory palace rooms
- [ ] **Spaced Repetition**: Optimal review timing system
- [ ] **Export Functionality**: PDF and text export options
- [ ] **Palace Templates**: Pre-built palace structures for common topics
- [ ] **Collaboration**: Share palaces with other users
- [ ] **Mobile App**: Native mobile application
- [ ] **Voice Integration**: Audio narration of memory palaces
- [ ] **Analytics**: Track learning progress and retention
- [ ] **Multiple AI Models**: Support for different AI providers

## 🏆 Acknowledgments

- **Streamlit**: For the amazing web framework that makes Python web apps easy
- **Google AI**: For providing the powerful Gemini models
- **Memory Palace Technique**: Inspired by ancient mnemonics used by memory champions
- **Open Source Community**: For the tools and inspiration that made this possible

## 📞 Support

If you encounter any issues or have questions:

1. **Check the Troubleshooting section** above
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information about your problem
4. **Include**: Operating system, Python version, error messages, and steps to reproduce

## 🌟 Show Your Support

If you found NeuroNest helpful, please:
- ⭐ Star this repository
- 🐛 Report bugs or suggest features
- 🤝 Contribute to the project
- 📢 Share with others who might benefit

---

**Transform your learning today with NeuroNest!** 🧠✨

> "The art of memory is the art of attention." - Start building unforgettable memories with AI-powered storytelling.