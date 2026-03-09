from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# create database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# LOGIN
@app.route("/", methods=["GET","POST"])
def login():

    message=""

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
        user=cursor.fetchone()

        conn.close()

        if user:
            message="Login Successful"
        else:
            message="Invalid Username or Password"

    return render_template("login.html",message=message)



# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():

    message=""

    if request.method=="POST":

        email=request.form["email"]
        username=request.form["username"]
        password=request.form["password"]
        confirm=request.form["confirm"]

        if password!=confirm:
            message="Passwords do not match"

        else:

            conn=sqlite3.connect("database.db")
            cursor=conn.cursor()

            # check username exists
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user=cursor.fetchone()

            if user:
                message="Username already exists"

            else:
                cursor.execute(
                    "INSERT INTO users(email,username,password) VALUES(?,?,?)",
                    (email,username,password)
                )
                conn.commit()
                message="Registration Successful. Now login."

            conn.close()

    return render_template("register.html",message=message)



if __name__=="__main__":
    app.run(debug=True)