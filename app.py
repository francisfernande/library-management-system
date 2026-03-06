from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"


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

        conn = sqlite3.connect("library.db")
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

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO books (title, author, shelf) VALUES (?, ?, ?)",
            (title, author, shelf)
        )

        conn.commit()
        conn.close()

        return "<h3>Book Added Successfully!</h3><a href='/dashboard'>Back to Dashboard</a>"

    return render_template("add_book.html")

# ---------------- ISSUE BOOK ----------------
@app.route('/issue_book', methods=['GET','POST'])
def issue_book():

    if 'librarian' not in session:
        return redirect('/login')

    if request.method == 'POST':

        book_id = request.form['book_id']
        student = request.form['student']

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO issued_books (book_id, student_name, issue_date) VALUES (?, ?, date('now'))",
            (book_id, student)
        )

        conn.commit()
        conn.close()

        return "<h3>Book Issued Successfully</h3><a href='/dashboard'>Back to Dashboard</a>"

    return render_template("issue_book.html")

# ---------------- VIEW BOOKS ----------------
@app.route('/view_books')
def view_books():

    conn = sqlite3.connect("library.db")
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

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()


    cursor.execute("""
    SELECT issued_books.id, books.title, issued_books.student_name, issued_books.issue_date
    FROM issued_books
    JOIN books ON books.id = issued_books.book_id
    """)

    data = cursor.fetchall()
    conn.close()

    return render_template("issued_book.html", books=data)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('librarian', None)
    return redirect('/')


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)