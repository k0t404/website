from flask import Flask, jsonify
from data.users import User
from data import db_session, news_api, jobs_api
from flask_restful import abort, Api, Resource
from data.reqparse import parser


def abort_if_news_not_found(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        abort(404, message=f"User {users_id} not found")


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_news_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        return jsonify({'users': users.to_dict(only=('name', 'about', 'hashed_password', 'email'))})

    def delete(self, users_id):
        abort_if_news_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(only=('name', 'about', 'hashed_password', 'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            name=args['name'],
            about=args['about'],
            hashed_password=args['hashed_password'],
            email=args['email'],
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})