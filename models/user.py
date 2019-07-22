import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(1000))
    email = db.Column(db.String(80))
    notify = db.Column(db.Boolean, default=True)
    verified = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, email, notify, verified):
        """ self.id = _id """
        self.username = username
        self.password = password
        self.email = email
        self.notify = notify
        self.verified = verified

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'username': self.username, 'email': self.email, 'notify': self.notify, 'verified': self.verified}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
