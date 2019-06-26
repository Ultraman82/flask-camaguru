from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, UserList
from resources.picture import Picture, PictureList
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = 'abcd'

CORS(app)
#CORS(app, resources={r"/api/*": {"Access-Control-Allow-Origin": "127.0.0.1:3000"}})
api = Api(app)

jwt = JWT(app, authenticate, identity)


api.add_resource(Picture, '/picture/<string:imgpath>')
#api.add_resource(PictureEdit, '/pictureedit/<int:id>')
api.add_resource(PictureList, '/pictures')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
#api.add_resource(UserCart, '/user/<string:username>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5500, debug=True)
