# from flask import Flask, render_template, request, redirect, url_for
# import mysql.connector

# app = Flask(__name__)

# # MySQL connection
# db = mysql.connector.connect(
# #     spring.datasource.username=root
# # spring.datasource.password=#Pradeep111
#     host="localhost",
#     user="root",    # <-- your MySQL username
#     password="#Pradeep111", # <-- your MySQL password
#     database="ecg_reg"
# )
# cursor = db.cursor()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/register', methods=['POST'])
# def register():
#     username = request.form['username']
#     email = request.form['email']
#     password = request.form['password']

#     try:
#         cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
#         db.commit()
#         return redirect(url_for('index'))
#     except mysql.connector.Error as err:
#         return f"Error: {err}"

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']

#     cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
#     user = cursor.fetchone()
#     if user:
#         return render_template('index2.html')
#     else:
#         return render_template('index.html', error="Invalid credentials!")

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
#import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for flash messages

# Configure MySQL
#     user="root",    # <-- your MySQL username
#     password="#Pradeep111", # <-- your MySQL password
#     database="ecg_reg"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "#Pradeep111"
app.config['MYSQL_DB'] = "ecg_reg"

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    mysql.connection.commit()
    cursor.close()

    flash('Registration successful! Please log in.')
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return redirect(url_for('dashboard'))
    else:
        flash('User not existing or wrong password!', 'error')
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)