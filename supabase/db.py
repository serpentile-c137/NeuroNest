import os
import bcrypt
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Initialize Supabase client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def init_db():
    """
    Initialize database tables. 
    Note: You should create these tables in your Supabase dashboard:
    
    1. Create 'users' table with columns:
       - id (int8, primary key, auto-increment)
       - username (text, unique)
       - password_hash (text)
       - created_at (timestamptz, default now())
    
    2. Create 'palaces' table with columns:
       - id (int8, primary key, auto-increment)
       - user_id (int8, foreign key to users.id)
       - concepts (text)
       - story (text)
       - created_at (timestamptz, default now())
    
    Enable Row Level Security (RLS) and create policies as needed.
    """
    try:
        # Test connection
        response = supabase.table('users').select("id").limit(1).execute()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(username: str, password: str) -> bool:
    """Create a new user account"""
    try:
        # Check if user already exists
        existing_user = supabase.table('users').select("id").eq('username', username).execute()
        if existing_user.data:
            return False  # User already exists
        
        # Create new user
        hashed_password = hash_password(password)
        response = supabase.table('users').insert({
            'username': username,
            'password_hash': hashed_password
        }).execute()
        
        return len(response.data) > 0
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def authenticate(username: str, password: str) -> int:
    """Authenticate user and return user ID if successful"""
    try:
        response = supabase.table('users').select("id, password_hash").eq('username', username).execute()
        
        if not response.data:
            return None  # User not found
        
        user = response.data[0]
        if verify_password(password, user['password_hash']):
            return user['id']
        
        return None  # Invalid password
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None

def save_palace(user_id: int, concepts: list, story: str) -> bool:
    """Save a new memory palace"""
    try:
        response = supabase.table('palaces').insert({
            'user_id': user_id,
            'concepts': '\n'.join(concepts),
            'story': story
        }).execute()
        
        return len(response.data) > 0
    except Exception as e:
        print(f"Error saving palace: {e}")
        return False

def get_palaces(user_id: int) -> list:
    """Get all palaces for a user"""
    try:
        response = supabase.table('palaces').select("*").eq('user_id', user_id).order('created_at', desc=True).execute()
        
        # Convert to format expected by the app
        palaces = []
        for palace in response.data:
            palaces.append((
                palace['id'],
                palace['concepts'],
                palace['story'],
                palace['created_at']
            ))
        
        return palaces
    except Exception as e:
        print(f"Error getting palaces: {e}")
        return []

def get_palace_by_id(palace_id: int) -> tuple:
    """Get a specific palace by ID"""
    try:
        response = supabase.table('palaces').select("*").eq('id', palace_id).execute()
        
        if not response.data:
            return None
        
        palace = response.data[0]
        return (
            palace['id'],
            palace['concepts'],
            palace['story'],
            palace['created_at']
        )
    except Exception as e:
        print(f"Error getting palace by ID: {e}")
        return None

def delete_palace(palace_id: int, user_id: int) -> bool:
    """Delete a palace (with user verification)"""
    try:
        response = supabase.table('palaces').delete().eq('id', palace_id).eq('user_id', user_id).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error deleting palace: {e}")
        return False

def get_user_by_id(user_id: int) -> dict:
    """Get user information by ID"""
    try:
        response = supabase.table('users').select("id, username, created_at").eq('id', user_id).execute()
        
        if not response.data:
            return None
        
        return response.data[0]
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        return None