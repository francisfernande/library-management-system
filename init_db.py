import sqlite3

def create_tables():

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    # 1️⃣ Create tables first (if not exists)
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
        username TEXT UNIQUE,
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

    # 2️⃣ Alter issued_books to add new columns (if they don't exist yet)
    try:
        cursor.execute("ALTER TABLE issued_books ADD COLUMN return_date TEXT")
    except sqlite3.OperationalError:
        pass  # column already exists

    try:
        cursor.execute("ALTER TABLE issued_books ADD COLUMN status TEXT DEFAULT 'Issued'")
    except sqlite3.OperationalError:
        pass  # column already exists

    # 3️⃣ Check table structure
    cursor.execute("PRAGMA table_info(issued_books)")
    for col in cursor.fetchall():
        print(col)

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