from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "blaDez_secret_key"  # Needed for login sessions

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",             # 👈 root user
        password="manikya07",    # 👈 your actual MySQL root password
        database="attendance_db"
    )


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
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
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        roll_no = request.form["roll_no"]
        class_name = request.form["class"]

        cursor.execute("INSERT INTO students (name, roll_no, class) VALUES (%s, %s, %s)", (name, roll_no, class_name))
        conn.commit()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()

    return render_template("students.html", students=students)

# ---------------- MARK ATTENDANCE ----------------
@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        student_id = request.form["student_id"]
        status = request.form["status"]
        date = request.form["date"]

        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)", (student_id, date, status))
        conn.commit()

    cursor.execute("SELECT a.id, s.name, a.date, a.status FROM attendance a JOIN students s ON a.student_id = s.id")
    records = cursor.fetchall()
    conn.close()

    return render_template("attendance.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)
