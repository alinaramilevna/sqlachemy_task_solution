from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    is_private = BooleanField("Личное")
    job = StringField('title')
    work_size = IntegerField('work size')
    collaborators = StringField('collaborators')
    is_finished = BooleanField('is finished')
    submit = SubmitField('Применить')
