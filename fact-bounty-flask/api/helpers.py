import os
from threading import Thread
from flask import current_app, make_response, jsonify
from flask_mail import Message
from api.extensions import mail
from flask_bcrypt import Bcrypt
from .user import model

admin_username = os.environ.get("ADMIN_USERNAME")
admin_password = os.environ.get("ADMIN_PASSWORD")
admin_email = os.environ.get("ADMIN_EMAIL")
bcrypt_password = Bcrypt().generate_password_hash(admin_password).decode()
admin_role = "admin"


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, body):
    app = current_app._get_current_object()
    msg = Message(
        app.config["FACTBOUNTY_MAIL_SUBJECT_PREFIX"] + subject,
        sender=app.config["FACTBOUNTY_MAIL_SENDER"],
        recipients=[to],
    )
    msg.body = body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def create_admin():
    try:
        user = model.User(
            email=admin_email,
            password=bcrypt_password,
            name=admin_username,
            role=admin_role,
        )
        user.save()
    except Exception:
        response = {"message": "Something went wrong!!"}
        return make_response(jsonify(response)), 500
