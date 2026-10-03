import sqlite3

conn = sqlite3.connect("attendance.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    status TEXT NOT NULL
)
''')
c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "mahi07"))


conn.commit()
conn.close()
