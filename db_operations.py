from flask_mysqldb import MySQL
from main import app


mysql = MySQL(app)


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


def get_user_profile_by_username(username):
    try:
        # Create a cursor
        with mysql.connection.cursor() as cur:

            # Execute the SQL query to fetch the user's profile based on username
            cur.execute(
                "SELECT id, username, email, password, balance, fullname, total_sent, total_received FROM users WHERE username = %s",
                (username,),
            )

            # Fetch the user's profile data
            user_data = cur.fetchone()

        if user_data:
            user_profile = UserProfile(*user_data)
            return user_profile
        else:
            return None  # User not found with the given username

    except Exception as e:
        # Handle database errors here (e.g., connection issues, SQL errors)
        print("Error fetching user profile:", str(e))
        return None


def get_transaction_history(user_id, limit=10):
    try:
        # Create a cursor
        with mysql.connection.cursor() as cur:

            # Execute the SQL query to fetch transaction history for the user
            cur.execute(
                "SELECT sender_id, id, amount FROM transactions WHERE recipient_id = %s",
                (user_id,),
            )

            # Fetch transaction history data
            transaction_history = cur.fetchall()

        return transaction_history

    except Exception as e:
        # Handle database errors here (e.g., connection issues, SQL errors)
        print("Error fetching transaction history:", str(e))
        return None


def get_recipient_fullname_from_email(email):
    # Establish a database connection
    with mysql.connection.cursor() as cur:

        # Query to fetch recipient's fullname based on email address
        cur.execute("SELECT fullname FROM users WHERE email = %s", (email,))

        # Fetch the result
        recipient_fullname = cur.fetchone()

        # Return recipient's fullname (or None if not found)
        return recipient_fullname[0] if recipient_fullname else None

