import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

DATABASE_PATH = 'users.db'

class User(UserMixin):
    def __init__(self, id, email, name, password_hash):
        self.id = id
        self.email = email
        self.name = name
        self.password_hash = password_hash
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get(user_id):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, name, password_hash FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None
    
    @staticmethod
    def get_by_email(email):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, name, password_hash FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None
    
    @staticmethod
    def create(email, name, password):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        existing_user = User.get_by_email(email)
        if existing_user:
            conn.close()
            return None
        
        password_hash = generate_password_hash(password)
        
        try:
            cursor.execute(
                'INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)',
                (email, name, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return User(user_id, email, name, password_hash)
        except sqlite3.IntegrityError:
            conn.close()
            return None

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
