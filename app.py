import os
from flask_cors import CORS
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister, UserList, Verify, User
from models.user import UserModel
from models.picture import PictureModel
from resources.picture import Picture, PictureList, AddComment, DeletePost, AddLike
from flask_restful import Resource, reqparse
import whirlpool
import random
from flask_mail import Mail, Message
from flask import jsonify 

app = Flask(__name__)

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

api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')    
api.add_resource(User, '/user/<string:username>')    
api.add_resource(Verify, '/verify/<string:username>')
api.add_resource(Picture, '/picture')
api.add_resource(PictureList, '/pictures/<int:page>')
api.add_resource(AddComment, '/addcomment/<int:id>')
api.add_resource(DeletePost, '/deletepost/<int:id>')
api.add_resource(AddLike, '/addlike/<int:id>')


@app.route('/resetpass/<string:email>', methods=['POST'])
def reset(email):        
    user = UserModel.find_by_email(email)    
    if user :
        newpass = str(random.randint(1000,9999))
        wp = whirlpool.new(newpass.encode('utf-8'))
        hashed_string = wp.hexdigest()
        user.password = hashed_string
        msg = Message(subject="42-camaguru",
                    recipients=[email],
                    body="your new password is %s" % newpass)
        mail.send(msg)
        user.save_to_db()
        return jsonify({"message": "Password reset email has been sent"})
    else:
        return jsonify({"message": "No matched user has found"})

@app.route('/likenotify/<string:username>', methods=['POST'])
def index(username):            
    user = UserModel.find_by_username(username).json()
    print(user)
    
    if user['notify']:
        message = "Somebody likes your photo!"
        msg = Message(subject=username,
                    recipients=[user['email']],
                    body=message)
        mail.send(msg)
        return "Like notification has sent email has been sent"
    return "Notification settig is false"

@app.route('/verify_mail/<string:username>')
def get(username):
    email = UserModel.find_by_username(username).email
    message = "<form action='http://localhost:5000/verify/%s' method='post'><input type='submit' value='Submit'></input></form>" % username    
    msg = Message(subject=username,
                  recipients=[email],
                  body=message)
    mail.send(msg)
    return jsonify({"message": "Verification email has been sent"})

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
