import os
import psycopg

def row_to_task(row):
    return {
        "id": row[0],
        "title": row[1],
        "status": row[2],
        "priority": row[4]
    }

def get_postgres_connection():
    connection = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    return connection