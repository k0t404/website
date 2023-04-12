import flask
from flask import request
from data import db_session
from .items import Items


blueprint = flask.Blueprint(
    'items_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/items')
def get_items():
    db_sess = db_session.create_session()
    items = db_sess.query(Items).all()
    return flask.jsonify({'items': [item.to_dict(only=('title', 'content', 'created_date', 'is_private', 'user.name',
                                                       'price', 'link'))
                                   for item in items]})


@blueprint.route('/api/items/<int:items_id>', methods=['GET'])
def get_one_items(items_id):
    db_sess = db_session.create_session()
    items = db_sess.query(Items).get(items_id)
    if not items:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'items': items.to_dict(only=(
                'title', 'content', 'user_id', 'is_private', 'price', 'link'))
        }
    )


@blueprint.route('/api/items', methods=['POST'])
def create_items():
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private', 'price', 'link']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    items = Items(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private'],
        price=request.json['price'],
        link=request.json['link']
    )
    db_sess.add(items)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/items/<int:items_id>', methods=['DELETE'])
def delete_items(items_id):
    db_sess = db_session.create_session()
    items = db_sess.query(Items).filter(id=items_id).first()
    if not items:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(items)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})
