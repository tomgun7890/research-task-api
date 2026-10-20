import psycopg

connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="research_tasks",
    user="research_user",
    password="research_password"
)

cursor = connection.cursor()

cursor.execute(
    "INSERT INTO tasks (title, status)" \
    "VALUES (%s, %s)" \
    "RETURNING id",
    ("Write paper", "todo")
)

new_id = cursor.fetchone()[0]

connection.commit()

print("new id:", new_id)

cursor.close()
connection.close()