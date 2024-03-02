import datetime
import json

from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/users.db")
    db_session.global_init("db/news.db")

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

    with open('data/news.json', 'r') as jsonfile:
        news = json.load(jsonfile)

    for n in news:
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = n['team_leader']
        job.job = n['job']
        job.work_size = n['work_size']
        job.collaborators = n['collaborators']
        if n['start_date'] == 'now':
            job.start_date = datetime.datetime.now()
        job.is_finished = n['is_finished']
        db_sess.add(job)
        db_sess.commit()

    # app.run()









if __name__ == '__main__':
    main()
