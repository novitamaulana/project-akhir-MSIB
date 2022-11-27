from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import werkzeug

app = Flask(__name__)
app.secret_key = "membuatLoginFLask1"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'msib'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
@app.route('/', methods=['GET','POST']) 
def index():
    return render_template('Login.html')

@app.route('/login', methods=['GET', 'POST']) 
def Login():
    msg=''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT email, password FROM users WHERE email = %s AND password = %s", (email, password,))
        user = cur.fetchone()

        if user :
            session['login'] = True
            session['password'] = user['password']
            session['email'] = user['email']
            return 'Login Sukses'
        else : 
            return 'Login salah'
    return render_template("Login.html")


@app.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    if request.method == "GET":
        details = request.form
        FirstName = details['first_name']
        LastName = details['last_name']
        Email = details['email']
        Password = details['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", (FirstName, LastName, Email, Password))
        mysql.connection.commit()
        cur.close()
        return 'sukses'
    return render_template('SignUp.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

if __name__ == '__main__' :
    app.run(debug=True)
