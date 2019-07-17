from db import db
from sqlalchemy.sql import func


class PictureModel(db.Model):
    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(60000))
    date = db.Column(db.String(50))
    like = db.Column(db.String(200))
    comments = db.Column(db.String(300))
    username = db.Column(db.String(20))
    icon = db.Column(db.Integer)

    def __init__(self, image, date, like, comments, username, icon):

        self.image = image
        self.date = date
        self.like = like
        self.comments = comments
        self.username = username
        self.icon = icon

    def json(self):
        return {'image': self.image, 'date': self.date, "id": self.id,
                'like': self.like, 'comments': self.comments, 'username': self.username, 'icon': self.icon}

    @classmethod
    def find_by_image(cls, image):
        # SELECT * FROM items WHERE image=image LIMIT 1
        return cls.query.filter_by(image=image).first()

    @classmethod
    def find_by_id(cls, id):
        # SELECT * FROM items WHERE image=image LIMIT 1
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_page(cls, page):
        # SELECT * FROM items WHERE image=image LIMIT 1
        return cls.query.filter(PictureModel.id <= (page * 5) + 5, PictureModel.id > page * 5).all()

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
