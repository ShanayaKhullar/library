import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

#To connect to a MySQL database in Python, you can use the mysql-connector library. If you haven't installed it yet, you can do so using:


Here's a simple example of Python code to connect to a MySQL database:


# Replace these values with your MySQL server information
host = "your_mysql_host"
user = "your_mysql_user"
password = "your_mysql_password"
database = "your_mysql_database"

try:
    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(
        host="localhost:3306"user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected to MySQL database")

        # Perform database operations here

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the connection when done
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed")




app = Flask(__name__)

# Create a SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
import os


from flask import Flask, flash, redirect, render_template, request, session
#from helpers import apology, login_required, lookup, usd
# Configure application
app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


try:
    # Establish a connection to the MySQL server
    con= mysql.connector.connect(host="localhost:3306" , user="root", password="root", database="lib")

# Replace 'your_host', 'your_database', 'your_user', and 'your_password' with your actual database information


# Check if the connection is successful

# Perform database operations here

# Close the connection when done



app.route("/", methods=["GET", "POST"])
def index():
    lib_db = con.execute("SELECT title, available from books")

@app.route("/addbook", methods=["GET", "POST"])
def addbook():
    t = request.form.get("title")
    addbook_db=con.execute("SELECT * FROM BOOKS WHEReE TITLE=?",t)
    if addbook_db is not None:
        return apology("cannot add book, book already exists, only 1 copy allowed")

    con.execute('INSERT INTO books (title, available) VALUES (?, ?)',t,True)
    flash("Book Added!")
    return redirect("/")

@app.route("/removebook", methods=["GET", "POST"])
def removebook():
    t = request.form.get("title")
    removebook_db=con.execute("SELECT * FROM BOOKS WHERE TITLE=?",t)
    if  removebook_db is None:
        return apology("cannot remove book, book title does not exist")
    db.execute("DELETE  FROM BOOKS WHERE TITLE=?",t)
    flash("Book Removed!")
    return redirect("/")

@app.route("/addborrower", methods=["GET", "POST"])
def addborrower():
    e = request.form.get("email")
    addborrower_db=con.execute("SELECT * FROM BOrrower  WHERE email =?",e)
    if addborrower_db is not None:
        return apology("cannot add borrower , borrower already  exists")
    con.execute("insert into borrower (email) values (?)",e)
    flash("Borrower Added!")
    return redirect("/")

@app.route("/issuebook", methods=["GET", "POST"])
def issuebook():
    e=request.form.get("email")
    issuebook_db=con.execute("SELECT * FROM BORROWER WHERE email = ?",e)
#    if issuebook_db is None:
#       return apology("borrower does not exist")
    t=request.form.get("title")
    issuebook_db= con.execute("SELECT * FROM BOoks  WHERE title  = ? and available = True",e)
    if issuebook_db is None:
        return apology("title does not exist or is already borrowed")
    db.execute("update BOoks set available=False  WHERE title  = ?",t)
    flash("Book issued!")
    return redirect("/")

@app.route("/returnbook",methods=["GET", "POST"])
def returnbook():
        e = request.form.get("email")
        returnbook_db=db.execute("SELECT * FROM BORROWER WHERE email = ?",e)
        if returnbook_db is None:
            return apology("email id of borrower does not exist")
        t=request.form.get("title")
        returnbook_db=db.execute("SELECT * FROM BOok WHERE title = ? and available=False",t)
        if returnbook_db is None:
             return apology("book of is not in library or has not been issued")
        db.execute("update book set available  = False where title= ?",t)
        flash("Book returned!")
        return redirect("/")
