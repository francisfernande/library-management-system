import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE books ADD COLUMN accession_no TEXT")
cursor.execute("ALTER TABLE books ADD COLUMN publisher TEXT")
cursor.execute("ALTER TABLE books ADD COLUMN year INTEGER")
cursor.execute("ALTER TABLE books ADD COLUMN pages INTEGER")
cursor.execute("ALTER TABLE books ADD COLUMN book_no TEXT")
cursor.execute("ALTER TABLE books ADD COLUMN cost REAL")
cursor.execute("ALTER TABLE books ADD COLUMN source TEXT")

conn.commit()
conn.close()

print("Database updated successfully!")