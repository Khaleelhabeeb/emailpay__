from flask import (
    Flask,
    render_template,
    redirect,
    session,
    url_for,
    flash,
)
import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "**************************"

# MySQL configuration
app.config['DB_USER'] = os.environ.get('DB_USER')
app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD')
app.config['DB_HOST'] = os.environ.get('DB_HOST')
app.config['DB_NAME'] = os.environ.get('DB_NAME')
load_dotenv()

mysql = MySQL(app)

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)


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


# main page route
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test_mysql")
def test_mysql_connection():
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT 1")
        result = cur.fetchone()

    return f"MySQL Connection Test: {result[0]}"


# registration route
@app.route("/register", methods=["GET", "POST"])
def register_route():
    from user_auth import register

    return register()


# login route
@app.route("/login", methods=["GET", "POST"])
def login_route():
    from user_auth import login

    return login()


@app.route("/dashboard")
def dashboard():
    if "logged_in" in session and session["logged_in"]:
        # Fetch the logged-in user's username from the session
        username = session["username"]

        from db_operations import (
            get_user_profile_by_username,
            get_transaction_history,
            get_recipient_fullname_from_email,
        )

        # Fetch the user's profile from the database based on the username
        user_profile = get_user_profile_by_username(username)

        if user_profile:
            user_id = user_profile.id
            # Fetch transaction history for the logged-in user
            transaction_history = get_transaction_history(user_id)

            return render_template(
                "dashboard.html", user=user_profile, transactions=transaction_history
            )
        else:
            flash("User profile not found.", "error")
            return redirect(url_for("login"))

    else:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("login"))
    
# Custom middleware to update session's last activity timestamp
@app.before_request
def before_request():
    session.permanent = True
    if "last_activity" in session:
        # Check if the session has expired
        now = datetime.now()
        last_activity = session["last_activity"].replace(tzinfo=None)  # Convert to naive datetime
        if (now - last_activity).total_seconds() > app.permanent_session_lifetime.total_seconds():
            session.clear()  
    session["last_activity"] = datetime.now()


@app.route("/send_money", methods=["POST"])
def send_money_route():
    from transaction_handler import send_money

    return send_money()


@app.route("/transaction_success")
def transaction_success_route():
    from transaction_handler import transaction_success

    return transaction_success()

@app.route("/settings")
def settings():
    username = session["username"]
    return render_template("settings.html", username=username)


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

