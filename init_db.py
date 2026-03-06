import sqlite3

def create_tables():

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        shelf TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS librarian (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issued_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        student_name TEXT,
        issue_date TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_default_librarian():

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO librarian (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )
        conn.commit()
        print("Default librarian created!")

    except sqlite3.IntegrityError:
        print("Librarian already exists")

    conn.close()


create_tables()
insert_default_librarian()

print("Database Ready")