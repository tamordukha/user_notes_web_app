from flask import Flask, render_template, request, redirect, url_for, session
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

        if user:
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

if __name__ == "__main__":
    app.run(debug=True)