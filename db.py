import sqlite3
import hashlib

DB_FILE = "neuronest.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS palaces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            concepts TEXT,
            story TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                     (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate(username, password):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()
    if user and user[1] == hash_password(password):
        return user[0]
    return None

def save_palace(user_id, concepts, story):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO palaces (user_id, concepts, story) VALUES (?, ?, ?)",
                 (user_id, "\n".join(concepts), story))
    conn.commit()
    conn.close()

def get_palaces(user_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, concepts, story, created_at
        FROM palaces
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,))
    return cur.fetchall()

def get_palace_by_id(palace_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, concepts, story, created_at FROM palaces WHERE id=?", (palace_id,))
    return cur.fetchone()

def delete_palace(palace_id, user_id):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM palaces WHERE id=? AND user_id=?", (palace_id, user_id))
    conn.commit()
    conn.close()
