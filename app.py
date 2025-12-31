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

        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect("/notes")

        return "Incorrect password or username"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        data = (username, password)
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
        data = (user_id, title, content, created_at)
        cursor.execute(query, data)
        conn.commit()
        conn.close()

        return redirect("/notes")

    return render_template("create.html")

@app.route("/notes/edit/<int:note_id>", methods=["GET", "POST"])
def edit(note_id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM notes WHERE id = ? AND user_id = ?",
        (note_id, user_id)
    )
    note = cursor.fetchone()

    if note is None:
        conn.close()
        return "Note not found", 404

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        cursor.execute(
            """
            UPDATE notes
            SET title = ?, content = ?
            WHERE id = ? AND user_id = ?
            """,
            (title, content, note_id, user_id)
        )
        conn.commit()
        conn.close()

        return redirect("/notes")

    conn.close()
    return render_template("edit.html", note=note)

@app.route("/notes/delete/<int:note_id>", methods=["POST"])
def delete(note_id):
    if "user_id" not in session:
        return redirect("/login")

    #user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id = ? AND user_id = ?",
        (note_id, session["user_id"])
    )
    conn.commit()
    conn.close()

    return redirect("/notes")


if __name__ == "__main__":
    app.run(debug=True)