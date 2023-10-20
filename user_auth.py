from main import app, session
from flask import flash, redirect, url_for, session, request, render_template
from main import mysql


class UserProfile:
    def __init__(self, id, username, email, password, balance, fullname, total_sent, total_received):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.balance = balance
        self.fullname = fullname
        self.total_sent = total_sent
        self.total_received = total_received


def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        fullname = request.form["fullname"]

        # Check if the username or email already exists in the database
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = %s OR email = %s", (username, email)
        )
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            flash("Username or email already exists.", "danger")
        else:
            # Insert the new user into the database
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (username, email, password, fullname) VALUES (%s, %s, %s, %s)",
                (username, email, password, fullname),
            )
            mysql.connection.commit()
            cur.close()
            flash("Registration successful. You can now log in.", "success")
            return redirect(url_for("login_route"))

    return render_template("register.html")


def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if the username and password are valid in the database
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT id, username, email, password, balance, fullname, total_sent, total_received FROM users WHERE username = %s AND password = %s",
            (username, password),
        )
        user_data = cur.fetchone()
        cur.close()

        if user_data:
            user = UserProfile(*user_data)  # Create a UserProfile object
            flash("Login successful.", "success")
            session[
                "logged_in"
            ] = True  # Set  session variable to indicate the user is logged in
            session["username"] = user.username  # Store the username in the session
            session["user_id"] = user.id  # Store the user ID in the session
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")
