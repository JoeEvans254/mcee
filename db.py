import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the users table with phone_number column
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    phone_number TEXT
                )''')

# Create the genre table
cursor.execute('''CREATE TABLE IF NOT EXISTS genre (
                    id INTEGER PRIMARY KEY,
                    genre_name TEXT NOT NULL,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )''')

# Create the moods table
cursor.execute('''CREATE TABLE IF NOT EXISTS moods (
                    id INTEGER PRIMARY KEY,
                    mood_name TEXT NOT NULL,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )''')

# Create the scheduler table
cursor.execute('''CREATE TABLE IF NOT EXISTS scheduler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    signature_timestamp INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )''')

# Commit changes and close the connection
conn.commit()
conn.close()
