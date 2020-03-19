from datetime import datetime

from flask import jsonify
from flask_restful import abort, Resource
import datetime
from data import db_session
from data.jobs import Jobs
from flask_restful import reqparse



def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def parse(self):
        parser = reqparse.RequestParser()
        parser.add_argument('job', required=False)
        parser.add_argument('team_leader', required=False, type=int)
        parser.add_argument('work_size', required=False, type=int)
        parser.add_argument('collaborators', required=False)
        parser.add_argument('is_finished', required=False, type=bool)
        return parser

    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('job', 'work_size', 'collaborators', 'team_leader', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        args = self.parse().parse_args()
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        if args['work_size'] is not None:
            job.work_size = args['work_size']
        if args['job'] is not None:
            job.job = args['job']
        if args['collaborators'] is not None:
            job.collaborators = args['collaborators']
        if args['team_leader'] is not None:
            job.team_leader = args['team_leader']
        if args['is_finished'] is not None:
            job.is_finished = args['is_finished']
        session.commit()
        return jsonify({'success': 'OK'})




class JobsListResource(Resource):
    def parse(self):
        parser = reqparse.RequestParser()
        parser.add_argument('job', required=True)
        parser.add_argument('team_leader', required=True, type=int)
        parser.add_argument('work_size', required=True, type=int)
        parser.add_argument('collaborators', required=True)
        parser.add_argument('is_finished', required=True, type=bool)
        return parser

    def get(self):
        session = db_session.create_session()
        job = session.query(Jobs).all()
        return jsonify({'job': [item.to_dict(
            only=('job', 'work_size', 'collaborators', 'team_leader', 'is_finished')) for item in job]})

    def post(self):
        args = self.parse().parse_args()
        session = db_session.create_session()
        job = Jobs(
            work_size=args['work_size'],
            job=args['job'],
            collaborators=args['collaborators'],
            team_leader=args['team_leader'],
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
            is_finished=args['is_finished']
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})