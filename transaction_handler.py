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





def transaction_success():
    amount = request.args.get("amount")
    recipient_email = request.args.get("recipient_email")
    transaction_date = request.args.get("transaction_date")
    user_id = request.args.get("user_id")

    recipient_fullname = get_recipient_fullname_from_email(recipient_email)

    return render_template(
    "transaction_success.html",
    amount=amount,
    recipient_fullname=recipient_fullname,
    )
