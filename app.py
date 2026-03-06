from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "devkey")


# ---------- DATABASE CONNECTION ----------
def get_db():
    return sqlite3.connect("library.db", timeout=20)


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM librarian WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session['librarian'] = username
            return redirect('/dashboard')
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():

    if 'librarian' not in session:
        return redirect('/login')

    return render_template("dashboard.html")


# ---------------- ADD BOOK ----------------
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():

    if 'librarian' not in session:
        return redirect('/login')

    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']
        shelf = request.form['shelf']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO books (title, author, shelf) VALUES (?, ?, ?)",
            (title, author, shelf)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template("add_book.html")


# ---------------- ISSUE BOOK ----------------
@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():

    if 'librarian' not in session:
        return redirect('/login')

    if request.method == 'POST':

        book_id = request.form['book_id']
        student = request.form['student']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO issued_books (book_id, student_name, issue_date, status) VALUES (?, ?, date('now'), 'Issued')",
            (book_id, student)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template("issue_book.html")


# ---------------- VIEW BOOKS (PUBLIC) ----------------
@app.route('/view_books')
def view_books():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    conn.close()

    return render_template("view_books.html", books=books)


# ---------------- VIEW ISSUED BOOKS ----------------
@app.route('/issued_book')
def issued_books():

    if 'librarian' not in session:
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT issued_books.id, books.title, issued_books.student_name, issued_books.issue_date,
             issued_books.return_date, issued_books.status
        FROM issued_books
        JOIN books ON books.id = issued_books.book_id
    """)

    data = cursor.fetchall()
    conn.close()

    return render_template("issued_book.html", books=data)
# ---------------- RETURN BOOK ----------------
@app.route('/return_book/<int:issued_id>')
def return_book(issued_id):
    if 'librarian' not in session:
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE issued_books
        SET return_date = date('now'), status = 'Returned'
        WHERE id = ?
    """, (issued_id,))

    conn.commit()
    conn.close()

    return redirect('/issued_book')
# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():

    session.pop('librarian', None)
    return redirect('/')


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000,debug=False)