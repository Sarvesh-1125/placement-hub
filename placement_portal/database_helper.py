import sqlite3

def initialize_database():
    conn = sqlite3.connect("placement.db")
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS portal_users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT,
        role TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS applications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        job_id INTEGER
    )""")

    cur.execute("INSERT OR IGNORE INTO portal_users(id,name,email,password,role) VALUES(1,'Admin','admin@gmail.com','admin','admin')")

    conn.commit()
    conn.close()
