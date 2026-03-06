import sqlite3

def create_tables():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    # Books Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            shelf TEXT NOT NULL,
            available INTEGER DEFAULT 1
        )
    """)

    # Students Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Librarian Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS librarian (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            student_name TEXT,
            issue_date TEXT)""")
            
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
    except:
        print("Librarian already exists.")

    conn.close()


if __name__ == "__main__":
    create_tables()
    insert_default_librarian()