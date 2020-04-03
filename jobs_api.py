from datetime import datetime, timedelta

from flask import Flask, jsonify, Blueprint, request

from data import db_session
from data.jobs import Jobs

blueprint = Blueprint('jobs_api', __name__,
                            template_folder='templates')



@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict()
                 for item in jobs]
        }
    )

@blueprint.route('/api/jobs/<int:jobs_id>',  methods=['GET'])
def get_one_jobs(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators',
                                       'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['PUT'])
def correct_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == request.json['id']).first()
    k = ['job', 'team_leader', 'work_size', 'collaborators',
     'start_date', 'end_date', 'is_finished']
    for key in k:
        if key in request.json:
            if key == 'job':
                jobs.job=request.json[key]
            if key == 'team_leader':
                jobs.job=request.json[key]
            if key == 'work_size':
                jobs.job=request.json[key]
            if key == 'collaborators':
                jobs.job=request.json[key]
            if key == 'start_date':
                jobs.job=request.json[key]
            if key == 'end_date':
                jobs.job=request.json[key]
            if key == 'is_finished':
                jobs.job=request.json[key]
    session.add(jobs)
    session.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'collaborators',
                  'is_finished']):
        print(request.json)
        return jsonify({'error': 'Bad333 request'})
    session = db_session.create_session()
    jobs = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(request.json['work_size']),
        is_finished=request.json['is_finished']
    )
    if session.query(Jobs).filter(Jobs.id == jobs.id).first():
        return jsonify({'error': 'Id already exists'})
    session.add(jobs)
    session.commit()
    return jsonify({'success': 'OK'})