from flask import Flask
import sqlite3
import json
from flask import jsonify
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_mail import Mail, Message
import os


class Verify(Resource):
    def get(self):
        msg = Message(subject="sds",
                      # sender=app.config.get("MAIL_USERNAME"),
                      sender="d",
                      # replace with your email for testing
                      recipients=["sojuse@virtualemail.info"],
                      body="This is a test email I sent with Gmail and Python!")
        mail.send(msg)

        return {"message": "Verification email has been sent"}, 201


class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field :wnnot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('email',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('notify',
                        type=bool,
                        required=False,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201
