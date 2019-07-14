from db import db
from sqlalchemy.sql import func


class PictureModel(db.Model):
    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key=True)
    imgpath = db.Column(db.String(80))
    date = db.Column(db.String(50))
    like = db.Column(db.Integer, default=0)
    comments = db.Column(db.String(300))
    username = db.Column(db.String(20))

    def __init__(self, imgpath, date, like, comments, username):

        self.imgpath = imgpath
        self.date = date
        self.like = like
        self.comments = comments
        self.username = username

    def json(self):
        return {'imgpath': self.imgpath, 'date': self.date, "id": self.id,
                'like': self.like, 'comments': self.comments, 'username': self.username}

    @classmethod
    def find_by_imgpath(cls, imgpath):
        # SELECT * FROM items WHERE imgpath=imgpath LIMIT 1
        return cls.query.filter_by(imgpath=imgpath).first()

    @classmethod
    def find_by_id(cls, id):
        # SELECT * FROM items WHERE imgpath=imgpath LIMIT 1
        return cls.query.filter_by(id=id).first()

    @classmethod
    def delete_all(cls):
        db.session.query(cls).delete()
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def drop_table(self):
        self.drop()
        db.session.commit()
