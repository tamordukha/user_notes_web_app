import sqlite3

# 1. Создаем соединение с файлом (если его нет, он создастся)
connection = sqlite3.connect('database.db')

# 2. Читаем схему и выполняем её
with open('schema.sql') as f:
    connection.executescript(f.read())

connection.close()
