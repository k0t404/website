import flask
from flask import request
from data import db_session
from .jobs import Jobs


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


def check():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    if jobs:
        return True
    return False


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return flask.jsonify({'jobs': [item.to_dict(only=('job', 'work_size', 'collaborators',
                                                      'start_date', 'is_finished')) for item in jobs]})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'jobs': jobs.to_dict(only=(
                'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished', 'category'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    if not check():
        return flask.jsonify({'error': ' Id already exists'})
    elif not all(key in request.json for key in
                 ['job', 'work_size', 'collaborators', 'category', 'is_finished']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    jobs = Jobs(
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        category=request.json['category'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})
