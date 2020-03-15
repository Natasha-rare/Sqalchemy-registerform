from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = StringField('Login/ email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    class1 = IntegerField('Class', validators=[DataRequired()])
    submit = SubmitField('Войти')


class TimeTableForm(FlaskForm):
    day = IntegerField('Day of the week', default=1)
    lesson = StringField('Lesson', default='Математика')
    lesson_number = IntegerField('Number of lesson', default=1)
    homework = StringField('Homework', default='Не задано')
    notes = StringField('Notes', default='Можете отдохнуть ^.^')
    submit = SubmitField('Submit')

