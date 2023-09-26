from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('xyz.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 first_name TEXT,
                 last_name TEXT,
                 username TEXT,
                 email TEXT,
                 password TEXT,
                 dob TEXT,
                 otp TEXT,
                 amount TEXT)''')
    conn.commit()
    conn.close()

create_table()

def register_user(first_name, last_name, username, email, password, dob):
    conn = sqlite3.connect('xyz.db')
    conn.execute("INSERT INTO users (first_name,last_name,username,email,password, dob) VALUES (?, ?, ?, ?, ?, ?)", (first_name, last_name, username, email, password, dob))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('xyz.db')
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM users").fetchall()
    conn.close()
    return users

def create_table():
    conn = sqlite3.connect('xyz.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS products
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 price REAL,
                 description TEXT,
                 image_url TEXT)''')
    conn.commit()
    conn.close()

def add_product(name, price, description, image_url):
    conn = sqlite3.connect('xyz.db')
    conn.execute("INSERT INTO products (name, price, description, image_url) VALUES (?, ?, ?, ?)",
    (name, price, description, image_url))
    conn.commit()
    conn.close()

@app.route('/products')
def products():
    conn = sqlite3.connect('xyz.db')
    cur = conn.cursor()
    products = cur.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # You can implement the logic to add the product to the user's cart here
    # For simplicity, let's assume the cart is stored in the database as well
    conn = sqlite3.connect('xyz.db')
    cur = conn.cursor()
    product = cur.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    conn.close()
    return render_template('cart.html', product=product)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
    create_table()

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    user_name = request.form['user_name']
    email = request.form['email']
    password = request.form['password']
    dob = request.form['dob']

    register_user(first_name, last_name, user_name, email, password, dob)

    return render_template('otp.html')

    #return redirect(url_for('products', user_name=user_name))
    #return redirect(url_for('verify_otp', user_name=user_name))

@app.route('/success')
def success():
    users = get_users()
    print(users)
    return render_template('success.html', users = users)

def register_user(first_name, last_name, username, email, password, dob):
    amount = 1000
    otp = generate_otp()
    conn = sqlite3.connect('xyz.db')
    conn.execute(
        "INSERT INTO users (first_name, last_name, username, email, password, dob, otp, amount) VALUES (?, ?, ?, ?, ?, ?, ?,?)",
        (first_name, last_name, username, email, password, dob, otp, amount))
    
    #res= conn.execute(f'select * from users where username = {username}')
    #session['username'] = res.fetchone()[3]
    conn.commit()
    conn.close()
    send_otp_email(email, otp)
    


@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    return redirect(url_for('products'))
    otp = request.form['otp']
    print(session)
    #un = session['username']
    conn = sqlite3.connect('xyz.db')
    res = conn.execute(
        f"SELECT user_name,otp FROM users where username = {un}",)
    print(res)
    if res:
        if res==otp:
            return redirect(url_for('success', user_name = True))
    return redirect(url_for('products'))


def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))


def send_otp_email(email, otp):
    smtp_host = 'smtp.office365.com'
    smtp_port = 587
    sender_email = 'soumodeepsaha1@gmail.com'
    sender_password = '#myfamily@3112#'

    subject = 'OTP for Registration'
    message = f'Your OTP is: {otp}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(user=sender_email, password=sender_password)
        server.sendmail(sender_email, email, msg.as_string())

@app.route('/logout')
def logout():
    session.pop('userid')


if __name__ == '__main__':
    app.run(debug=True)