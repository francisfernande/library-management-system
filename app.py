from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "devkey")


# ---------- DATABASE CONNECTION ----------
def get_db():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    conn.autocommit = True
    return conn


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    next_page = request.args.get('next')

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM librarian WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['librarian'] = username
            return redirect(next_page if next_page else '/dashboard')
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
@app.route('/add_book')
def add_book():

    if 'librarian' not in session:
        return redirect('/login?next=/add_book_form')

    return redirect('/add_book_form')


# ---------------- ADD BOOK FORM ----------------
@app.route('/add_book_form', methods=['GET', 'POST'])
def add_book_form():

    if 'librarian' not in session:
        return redirect('/login')

    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']
        shelf = request.form['shelf']
        accession_no = request.form['accession_no']
        publisher = request.form['publisher']
        year = request.form['year']
        pages = request.form['pages']
        book_no = request.form['book_no']
        cost = request.form['cost']
        source = request.form['source']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO books
        (title, author, shelf, accession_no, publisher, year, pages, book_no, cost, source)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (title, author, shelf, accession_no, publisher, year, pages, book_no, cost, source)
        )

        cursor.close()
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

        cursor.execute("""
            INSERT INTO issued_books (book_id, student_name, issue_date, status)
            VALUES (%s, %s, CURRENT_DATE, 'Issued')
        """, (book_id, student))

        cursor.close()
        conn.close()

        return redirect('/dashboard')

    return render_template("issue_book.html")


# ---------------- VIEW BOOKS (PUBLIC) ----------------
@app.route('/view_books')
def view_books():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.id, b.title, b.author, b.shelf,
               b.accession_no, b.publisher, b.year, b.pages,
               b.book_no, b.cost, b.source,
               (SELECT student_name
                FROM issued_books i
                WHERE i.book_id = b.id AND i.status='Issued'
                ORDER BY i.id DESC LIMIT 1
               ) AS current_holder
        FROM books b
    """)

    books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view_books.html", books=books)


# ---------------- VIEW ISSUED BOOKS ----------------
@app.route('/issued_book')
def issued_books_page():

    if 'librarian' not in session:
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT issued_books.id,
               books.title,
               issued_books.student_name,
               issued_books.issue_date,
               issued_books.return_date,
               issued_books.status
        FROM issued_books
        JOIN books ON books.id = issued_books.book_id
    """)

    data = cursor.fetchall()

    cursor.close()
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
        SET return_date = CURRENT_DATE,
            status = 'Returned'
        WHERE id = %s
    """, (issued_id,))

    cursor.close()
    conn.close()

    return redirect('/issued_book')


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():

    session.pop('librarian', None)
    return redirect('/')


# ---------------- STATISTICS ----------------
@app.route('/statistics')
def statistics():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM issued_books WHERE status='Issued'")
    issued_count = cursor.fetchone()[0]

    available_books = total_books - issued_count

    cursor.execute("SELECT COUNT(DISTINCT student_name) FROM issued_books")
    total_students = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "statistics.html",
        total_books=total_books,
        issued_books=issued_count,
        available_books=available_books,
        total_students=total_students
    )


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)