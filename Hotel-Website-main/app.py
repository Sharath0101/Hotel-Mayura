from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'mayura_secret_key'

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Customers
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    # Reviews
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            section TEXT,
            rating INTEGER,
            comment TEXT
        )
    ''')

    # Feedback
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            message TEXT
        )
    ''')

    # Food Orders (UPDATED – DO NOT SKIP)
    c.execute('''
        CREATE TABLE IF NOT EXISTS food_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            items TEXT,
            total INTEGER,
            order_type TEXT,
            room_no TEXT,
            floor TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------------- AUTH & HOME ----------------
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO customers (name, phone) VALUES (?, ?)',
            (name, phone)
        )
        conn.commit()

        session['user_id'] = c.lastrowid
        session['name'] = name

        conn.close()
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- PAGES ----------------
@app.route('/room-booking')
def room_booking():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('room-booking.html')


@app.route('/restaurant')
def restaurant():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('restaurant.html')


@app.route('/party-hall')
def party_hall():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('party-hall.html')


@app.route('/parking', methods=['GET', 'POST'])
def parking():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        return redirect(url_for('home'))

    return render_template('parking.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO customers (name, phone) VALUES (?, ?)',
            (name, phone)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('contact.html')

# ---------------- REVIEWS & FEEDBACK ----------------
@app.route('/reviews')
def reviews():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reviews')
    reviews = c.fetchall()
    conn.close()

    return render_template('reviews.html', reviews=reviews)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        customer_id = session['user_id']
        message = request.form['message']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO feedback (customer_id, message) VALUES (?, ?)',
            (customer_id, message)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('feedback.html')


@app.route('/submit-review', methods=['POST'])
def submit_review():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    section = request.form['section']
    rating = request.form['rating']
    comment = request.form['comment']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO reviews (customer_id, section, rating, comment) VALUES (?, ?, ?, ?)',
        (session['user_id'], section, rating, comment)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('reviews'))

# ---------------- FOOD ORDERING (FIXED & COMPLETE) ----------------
@app.route('/place-order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    name = session.get('name', 'Guest')
    phone = ''  # optional, not mandatory from frontend
    items = request.form['items']
    total = request.form['total']
    order_type = request.form.get('order_type', 'restaurant')
    room_no = request.form.get('room_no', '')
    floor = request.form.get('floor', '')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO food_orders 
        (name, phone, items, total, order_type, room_no, floor)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone, items, total, order_type, room_no, floor))
    conn.commit()
    conn.close()

    return redirect(url_for('restaurant'))

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
