import sqlite3
import json
from flask import jsonify
from flask_restful import Resource, reqparse
from models.user import UserModel


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


class UserList(Resource):
    def get(self):
        return {'users': [x.json() for x in UserModel.query.all()]}
        # return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}
        # return {'users': [user.json() for user in UserModel.query.all()]}class UserList(Resource):

    def delete(self):
        UserModel.delete_all()
        return({'mesage': 'All Userlist deleted'})
