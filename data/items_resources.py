import flask
from flask import Flask, jsonify
from data.items import Items
from data import db_session, items_api
from flask_restful import abort, Api, Resource
from data.reqparse import parser


def abort_if_item_not_found(items_id):
    session = db_session.create_session()
    items = session.query(Items).get(items_id)
    if not items:
        abort(404, message=f"Item {items_id} not found")


class ItemResource(Resource):
    def get(self, items_id):
        abort_if_item_not_found(items_id)
        session = db_session.create_session()
        items = session.query(Items).get(items_id)
        return jsonify({'news': items.to_dict(
            only=('title', 'content', 'user_id', 'is_private', 'price', 'link'))})

    def delete(self, items_id):
        abort_if_item_not_found(items_id)
        session = db_session.create_session()
        items = session.query(Items).get(items_id)
        session.delete(items)
        session.commit()
        return jsonify({'success': 'OK'})


class ItemListResource(Resource):
    def get(self):
        session = db_session.create_session()
        items = session.query(Items).all()
        return jsonify({'news': [item.to_dict(
            only=('title', 'content', 'user.name', 'price', 'link')) for item in items]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        items = Items(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_published=args['is_published'],
            is_private=args['is_private'],
            price=args['price'],
            link=args['link']
        )
        session.add(items)
        session.commit()
        return jsonify({'success': 'OK'})