import sqlite3
connection = sqlite3.connect("tasks.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

'''
cursor.execute(
    "INSERT INTO tasks (title, status) VALUES (?, ?)",
    ("Read paper", "todo")
)

cursor.execute(
    "UPDATE tasks SET status = ? WHERE id = ?",
    ("done", 2)
)
'''

cursor.execute(
    "DELETE FROM tasks WHERE id = ?",
    (3,)
)

connection.commit()

cursor.execute("SELECT * FROM tasks")

rows = cursor.fetchall()
print(rows)

cursor.execute(
    "SELECT * FROM tasks WHERE id = ?",
    (2,)
)

row = cursor.fetchone()
print(row)

connection.close()