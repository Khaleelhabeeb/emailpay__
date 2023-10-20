from flask import flash, request, redirect, session, url_for, render_template
from decimal import Decimal
from db_operations import get_recipient_fullname_from_email
from main import mysql
from datetime import datetime


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


def send_money():
    if "logged_in" in session and session["logged_in"]:
        recipient_email = request.form["recipient_email"]
        amount = Decimal(request.form["amount"])

        # Fetch the user's ID from the session
        user_id = session.get("user_id")

        if user_id:
            try:
                cur = mysql.connection.cursor()

                # Get sender's balance and check if it's greater than or equal to the amount to be sent
                cur.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
                sender_balance = Decimal(cur.fetchone()[0])

                if sender_balance >= amount:
                    # Deduct the amount from sender's balance
                    new_balance_sender = sender_balance - amount
                    cur.execute(
                        "UPDATE users SET balance = %s WHERE id = %s",
                        (new_balance_sender, user_id),
                    )

                    # Find recipient by email
                    cur.execute(
                        "SELECT id, balance FROM users WHERE email = %s",
                        (recipient_email,),
                    )
                    recipient_data = cur.fetchone()

                    if recipient_data:
                        recipient_id, recipient_balance = recipient_data

                        # Add the amount to recipient's balance
                        new_balance_recipient = Decimal(recipient_balance) + amount
                        cur.execute(
                            "UPDATE users SET balance = %s WHERE id = %s",
                            (new_balance_recipient, recipient_id),
                        )

                        # Update total_sent for the sender and total_received for the recipient
                        cur.execute(
                            "UPDATE users SET total_sent = total_sent + %s WHERE id = %s",
                            (amount, user_id),
                        )
                        cur.execute(
                            "UPDATE users SET total_received = total_received + %s WHERE id = %s",
                            (amount, recipient_id),
                        )

                        current_date = datetime.now()

                        # Get sender's email from the session
                        user_id = session.get("user_id")

                        # Create a transaction record
                        cur.execute(
                            "INSERT INTO transactions (sender_id, recipient_id, amount) VALUES (%s, %s, %s)",
                            (user_id, recipient_id, amount),
                        )
                        mysql.connection.commit()

                        return redirect(
                            url_for(
                                "transaction_success_route",
                                amount=amount,
                                recipient_email=recipient_email,
                                transaction_date=current_date,
                                user_id=user_id,
                            )
                        )
                    else:
                        flash("Recipient not found.", "danger")
                else:
                    flash("Insufficient balance.", "danger")

                cur.close()

            except Exception as e:
                # Handle database errors
                print("Error:", str(e))
                flash("Error processing the transaction.", "danger")
        else:
            flash("User ID not found in the session.", "danger")
    else:
        flash("Please log in to send money.", "warning")

    return redirect(url_for("dashboard"))


def transaction_success():
    amount = request.args.get("amount")
    recipient_email = request.args.get("recipient_email")
    transaction_date = request.args.get("current_date")
    user_id = request.args.get("user_id")
    return render_template(
        "transaction_success.html",
        amount=amount,
        recipient_email=recipient_email,
        transaction_date=current_date,
        user_id=user_id,
    )


current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
