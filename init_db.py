import sqlite3

conn = sqlite3.connect("attendance.db")
c = conn.cursor()

# Users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Students table
c.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL,
    class TEXT NOT NULL
)
''')

# Attendance table
c.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
''')

# 👇 Add default user
c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "mahi07"))

conn.commit()
conn.close()
