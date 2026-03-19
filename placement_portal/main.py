# Developed by Sarvesh Choudhary

from flask import Flask, render_template, request, redirect, session
import sqlite3
from database_helper import initialize_database

portal_app = Flask(__name__)
portal_app.secret_key = "sarvesh_secret"

initialize_database()

def connect_db():
    return sqlite3.connect("placement.db")

@portal_app.route("/")
def home():
    return redirect("/login")

@portal_app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM portal_users WHERE email=? AND password=?", (email,password))
        user = cur.fetchone()

        if user:
            session["user_id"] = user[0]
            role = user[4]

            if role == "admin":
                return redirect("/admin_dashboard")
            elif role == "student":
                return redirect("/student_dashboard")
            else:
                return redirect("/company_dashboard")
        else:
            return "Invalid login!"

    return render_template("login.html")

@portal_app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO portal_users(name,email,password,role) VALUES(?,?,?,?)",
                    (name,email,password,role))
        conn.commit()
        return redirect("/login")

    return render_template("register.html")

@portal_app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin.html")

@portal_app.route("/company_dashboard", methods=["GET","POST"])
def company_dashboard():
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        job = request.form["job"]
        cur.execute("INSERT INTO jobs(title) VALUES(?)", (job,))
        conn.commit()

    cur.execute("SELECT * FROM jobs")
    jobs = cur.fetchall()

    return render_template("company.html", jobs=jobs)

@portal_app.route("/student_dashboard")
def student_dashboard():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM jobs")
    jobs = cur.fetchall()

    return render_template("student.html", jobs=jobs)

@portal_app.route("/apply/<int:job_id>")
def apply(job_id):
    conn = connect_db()
    cur = conn.cursor()

    user_id = session.get("user_id")
    cur.execute("INSERT INTO applications(user_id, job_id) VALUES(?,?)", (user_id, job_id))
    conn.commit()

    return "Applied Successfully!"

if __name__ == "__main__":
    portal_app.run(debug=True)
