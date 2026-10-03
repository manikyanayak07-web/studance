import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "blaDez_secret_key"  # Needed for login sessions

# Database connection
def get_db_connection():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials! Try again."

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# ---------------- ADD STUDENT ----------------
@app.route("/students", methods=["GET", "POST"])
def students():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        roll_no = request.form["roll_no"]
        class_name = request.form["class"]

        cursor.execute("INSERT INTO students (name, roll_no, class) VALUES (?, ?, ?)", (name, roll_no, class_name))
        conn.commit()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()

    return render_template("students.html", students=students)

# ---------------- MARK ATTENDANCE ----------------
@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        student_id = request.form["student_id"]
        status = request.form["status"]
        date = request.form["date"]

        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date, status))
        conn.commit()

    cursor.execute("SELECT a.id, s.name, a.date, a.status FROM attendance a JOIN students s ON a.student_id = s.id")
    records = cursor.fetchall()
    conn.close()

    return render_template("attendance.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)
