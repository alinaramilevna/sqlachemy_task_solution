import json

from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/users.db")

    with open('data/users.json', 'r') as jsonfile:
        data = json.load(jsonfile)

    for d in data:
        db_sess = db_session.create_session()
        user = User()
        user.surname = d['surname']
        user.name = d['name']
        user.age = d['age']
        user.position = d['position']
        user.speciality = d['speciality']
        user.address = d['address']
        user.email = d['email']
        db_sess.add(user)
        db_sess.commit()


if __name__ == '__main__':
    main()
