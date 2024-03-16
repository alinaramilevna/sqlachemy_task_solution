import flask
from flask import jsonify, make_response, request

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('job', 'work_size', 'team_leader', 'is_finished', 'collaborators', 'start_date'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'job': jobs.to_dict(only=(
                'job', 'work_size', 'team_leader', 'is_finished'))
        }
    )




@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['job', 'work_size', 'team_leader', 'collaborators', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    job = Jobs(
        job=request.json['job'],
        work_size=request.json['work_size'],
        team_leader=request.json['team_leader'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_jobs(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_jobs(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'empty request'}), 400)
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)

    job.job = request.json['job'] if 'job' in request.json else job.job
    job.work_size = request.json['work_size'] if 'work_size' in request.json else job.work_size
    job.team_leader = request.json['team_leader'] if 'team_leader' in request.json else job.team_leader
    job.collaborators = request.json['collaborators'] if 'collaborators' in request.json else job.collaborators
    job.is_finished = request.json['is_finished'] if 'is_finished' in request.json else job.is_finished
    db_sess.commit()
    return make_response(jsonify({'success': 'OK'}), 200)
