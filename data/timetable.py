import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class TimeTable(SqlAlchemyBase):
    __tablename__ = 'timetable'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    day = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    lesson = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    lesson_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # teacher_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    homework = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    notes = sqlalchemy.Column(sqlalchemy.String, default='')
