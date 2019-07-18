import os
from flask_cors import CORS
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister, UserList, Verify
# SMTP
import os
from flask_mail import Mail, Message
from models.user import UserModel
from resources.picture import Picture, PictureList, AddLike, AddComment
#from resources.verify import Verify
app = Flask(__name__)

# print(os.environ)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_DEFAULT_SENDER": os.environ['EMAIL_USER'],
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}
app.config.update(mail_settings)
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = 'abcd'

CORS(app)
api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Picture, '/picture')
api.add_resource(PictureList, '/pictures/<int:page>')
api.add_resource(Verify, '/verify/<string:username>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
api.add_resource(AddLike, '/addlike/<int:id>')
api.add_resource(AddComment, '/addcomment/<int:id>')
#api.add_resource(CheckVerify, '/checkverified/<string:username>')
#api.add_resource(Verify, '/verify')
#api.add_resource(PictureEdit, '/pictureedit/<int:id>')



@app.route('/verify_mail/<string:username>')
def get(username):
    email = UserModel.find_by_username(username).email
    message = "<form action='http://localhost:5000/verify/%s' method='post'><input type='submit' value='Submit'></input></form>" % username    
    #message = "<a href='http://localhost:5000/verify/%s'>Click here to verify" % username    
    msg = Message(subject=username,
                  recipients=[email],
                  body=message)
    mail.send(msg)
    return {"message": "Verification email has been sent"}, 201


""" @app.route('/verify/<string:username>')
def index(username):
    msg = Message(subject=username,
                  recipients="lomupor@quickemail.info",
                  body="This is a test email from 42 camaguru project by Edgar")
    mail.send(msg)
    return {"message": "Verification email has been sent"}, 201 """


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
