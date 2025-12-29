CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE CHECK(username <> ''),
    password TEXT NOT NULL CHECK(password <> '')
);

CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL CHECK(title <> ''),
    content TEXT NOT NULL CHECK(content <> ''),
    created_at TEXT NOT NULL CHECK(created_at <> '')
)