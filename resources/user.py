import sqlite3
import json
from flask import jsonify, render_template
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt import jwt_required

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
    parser.add_argument('verified',
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


class Verify(Resource):
    def post(self, username):
        user = UserModel.find_by_username(username)
        user.verified = True
        user.save_to_db()        
        return "Succesfully verified. Log in to the site"
        
    def get(self, username):
        user = UserModel.find_by_username(username)                
        return user.verified


class User(Resource):
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
    parser.add_argument('verified',
                        type=bool,
                        required=False,
                        help="This field cannot be blank."
                        )

    def get(self, username):
        user = UserModel.find_by_username(username)
        return user.json()
        # return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}
        # return {'users': [user.json() for user in UserModel.query.all()]}class UserList(Resource):

    def delete(self, username):
        UserModel.delete_all()
        return({'mesage': 'All Userlist deleted'})

    #@jwt_required()
    def put(self, username):
        data = User.parser.parse_args()
        user = UserModel.find_by_username(username)        
        user.username = data['username']
        user.password = data['password']
        user.email = data['email']                
        
        user.save_to_db()
        return {"message":"Info has successfuly updated"}



class UserList(Resource):
    def get(self):
        return {'users': [x.json() for x in UserModel.query.all()]}
        # return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}
        # return {'users': [user.json() for user in UserModel.query.all()]}class UserList(Resource):

    def delete(self):
        UserModel.delete_all()
        return({'mesage': 'All Userlist deleted'})
