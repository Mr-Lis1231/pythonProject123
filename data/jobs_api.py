import flask
from flask import request, jsonify
from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint('news_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {'jobs': [item.to_dict(only=('id', 'job', 'work_size', 'collaborators', 'start_date',
                                     'end_date', 'is_finished', 'team_leader')) for item in jobs]})

@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify({'job': jobs.to_dict(only=('id', 'job', 'work_size', 'collaborators', 'start_date',
                                              'end_date', 'is_finished', 'team_leader'))})


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'work_size', 'collaborators', 'is_finished', 'team_leader']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()

    jobs = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        team_leader=request.json['team_leader']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/news/<int:jobs_id>', methods=['DELETE'])
def delete_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})