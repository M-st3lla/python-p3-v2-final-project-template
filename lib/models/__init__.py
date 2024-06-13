import sqlite3
from datetime import datetime

CONN = sqlite3.connect('journal_away.db')
CURSOR = CONN.cursor()

def initialize_db():
    # user table
    CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS user_table (
        user_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        date_joined TEXT NOT NULL
    )
    ''')

    # category table
    CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS category_table (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_by TEXT NOT NULL,
        date_created TEXT,
        date_modified TEXT,
        FOREIGN KEY (created_by) REFERENCES user_table (user_id)
    )
    ''')

    # entry table
    CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS entry_table (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_name TEXT NOT NULL,
        description TEXT,
        created_by TEXT NOT NULL,
        date_created TEXT,
        FOREIGN KEY (created_by) REFERENCES user_table (user_id)
    )
    ''')

    # tag table
    CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS tag_table (
        tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag_name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_by TEXT,
        date_created TEXT,
        FOREIGN KEY (created_by) REFERENCES user_table(user_id)
    )
    ''')

    # category_tag table
    CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS category_tag (
        category_id INTEGER,
        tag_id INTEGER,
        created_by TEXT,
        FOREIGN KEY (category_id) REFERENCES category_table (category_id),
        FOREIGN KEY (tag_id) REFERENCES tag_table (tag_id),
        FOREIGN KEY (created_by) REFERENCES user_table(user_id)
    )
    ''')

    # Insert predefined categories if not already present
    predefined_categories = [
        ("food", "All about food and recipes"),
        ("fitness", "Fitness routines and health"),
        ("work or career", "Work-related notes and career progress"),
        ("travel", "Travel experiences and plans"),
        ("school", "School-related activities and notes")
    ]
    
    for category_name, description in predefined_categories:
        CURSOR.execute('''
        INSERT OR IGNORE INTO category_table (category_name, description, created_by, date_created, date_modified)
        VALUES (?, ?, 'predefined', ?, ?)
        ''', (category_name, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    CONN.commit()

initialize_db()
