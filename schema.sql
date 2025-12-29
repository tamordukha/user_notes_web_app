CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE CHECK(username <> ''),
    password TEXT NOT NULL CHECK(password <> '')
);
