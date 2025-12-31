import pytest
import sqlite3
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["DATABASE"] = "test.db"
    app.config["SECRET_KEY"] = "test-secret"

    with app.test_client() as client:
        yield client

def test_register(client):
    response = client.post("/register", data={"username": "Maktraher", "password": "mibombo"})
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", ("Maktraher",))
    user = cursor.fetchone()
    conn.close()

    assert user is not None
    assert response.status_code == 302

def test_login(client):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    data = ("Kislinka", "big bob")
    cursor.execute(query, data)
    conn.commit()
    conn.close()

    response = client.post("/login", data={"username": "Kislinka", "password": "big bob"})
    assert response.status_code == 302
    with client.session_transaction() as sess:
        assert "user_id" in sess


def test_routes(client):
    response = client.get("/notes", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_notes(client):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("Horse", "finger")
    )
    conn.commit()
    conn.close()
    client.post("/login", data={
    "username": "Horse",
    "password": "finger"
})
    response = client.post("/notes/create", data={
        "title": "feed cat",
        "content": "feed cat at 9:00 AM"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"feed cat" in response.data


