from flask import jsonify
from flask_restful import abort, Resource
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from data.users import User
from data.reqparser import parser


def abort_if_news_not_found(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        abort(404, message=f"News {users_id} not found")


def set_password(password):
     return generate_password_hash(password)


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_news_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        return jsonify({'users': [users.to_dict(
            only=('name','surname', 'age', 'address', 'email',
                  'position', 'speciality', 'hashed_password'))]})


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
        return jsonify({'users': [item.to_dict(only=('name',
                'surname', 'age', 'address', 'email',
                  'position', 'speciality', 'hashed_password')) for item in users]})


    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})