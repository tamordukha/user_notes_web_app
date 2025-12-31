# User Notes Web App (Flask)

A simple Flask web application where users can register, log in, and manage their personal notes.

Each user can only see and manage their own notes.

---

## Features
- User registration
- User login / logout (sessions)
- Create, read, edit, delete notes
- Notes are linked to a specific user
- Protected routes (login required)

---

## Tech Stack
- Python
- Flask
- SQLite
- Jinja2
- pytest

---

## Project Structure

```text
user-notes-web-app/
├── .github/
│   └── workflows/
│       └── ci.yaml
│
├── static/
│   └── style.css
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── notes.html
│   ├── create.html
│   └── edit.html
│
├── tests/
│   └── test_app.py
│
├── app.py
├── init_db.py
├── schema.sql
├── database.db
├── test.db
├── requirements.txt
├── README.md
├── .gitignore
```

### Notes
- `static/` — CSS files  
- `templates/` — HTML templates (Jinja2)  
- `tests/` — application tests (pytest)  
- `init_db.py` — database initialization script  
- `database.db` / `test.db` — local SQLite databases


## How to Run
```bash
pip install -r requirements.txt
python app.py
```

## Open in browser
http://127.0.0.1:5000

## How to Run Tests
```bash
pytest
```

## Notes
This project is built for learning purposes and introduces:
- authentication
- sessions
- user-specific data
- basic backend testing