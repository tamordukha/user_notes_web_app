from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = "something-secret"

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        data = [username, password]
        cursor.execute(query, data)
        
        # Получаем одну запись (если нашли)
        user = cursor.fetchone()
        conn.close()

        if "user_id" not in session:
            return redirect("/login")

        elif user:
            session["user_id"] = user["id"] 
            return redirect("/notes")
        else:
            return "Incorrect username or password", 401
    
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        data = [username, password]
        try:
            cursor.execute(query, data)
            conn.commit()
        except sqlite3.IntegrityError:
            return "This username is already taken.", 400
        finally:
            conn.close()

        return redirect("/login")
    
    return render_template("register.html")

@app.route("/notes")
def notes():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM notes WHERE user_id = ?"
    cursor.execute(
        query,
        (user_id,)
    )
    notes = cursor.fetchall()
    conn.close()

    return render_template("notes.html", notes=notes)

@app.route("/notes/create", methods=["GET","POST"])
def create():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        query = "INSERT INTO notes (user_id, title, content, created_at) VALUES (?, ?, ?, ?)"
        data = [user_id, title, content, created_at]
        cursor.execute(query, data)
        conn.commit()
        conn.close()

        return redirect("/notes")

    return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)