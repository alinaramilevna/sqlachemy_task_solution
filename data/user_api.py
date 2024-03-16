import flask
from flask import jsonify, make_response, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify({
        'user': [item.to_dict(only=['id', 'surname', 'name', 'age', 'position', 'speciality',
                                    'address', 'email', 'city_from']) for item in users]
    })


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'not found'}), 404)
    return make_response(jsonify({
        'user': user.to_dict(only=('id', 'name', 'surname', 'age', 'position', 'speciality',
                                   'address', 'email', 'city_from'))
    }), 200)


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'empty request'}), 400)
    elif not all([key in request.json for key in ['name', 'surname', 'age', 'position', 'speciality',
                                                  'address', 'email', 'city_from', 'password']]):
        return make_response(jsonify({'error': 'bad request'}, 400))
    db_sess = db_session.create_session()
    user = User(
        name=request.json['name'],
        surname=request.json['surname'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        city_from=request.json['city_from']
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return make_response(jsonify({'id': user.id}), 200)


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return make_response(jsonify({'success': 'OK'}), 200)


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'empty request'}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'not found'}), 404)
    user.name = request.json['name'] if 'name' in request.json else user.name
    user.surname = request.json['surname'] if 'surname' in request.json else user.surname
    user.age = request.json['age'] if 'age' in request.json else user.age
    user.position = request.json['position'] if 'position' in request.json else user.position
    user.speciality = request.json['speciality'] if 'speciality' in request.json else user.speciality
    user.address = request.json['address'] if 'address' in request.json else user.address
    user.email = request.json['email'] if 'email' in request.json else user.email
    user.city_from = request.json['city_from'] if 'city_from' in request.json else user.city_from
    db_sess.commit()
    return make_response(jsonify({'success': 'OK'}), 200)
