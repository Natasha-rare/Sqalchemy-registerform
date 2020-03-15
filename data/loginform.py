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
    day = IntegerField('Day of the week', validators=[DataRequired()])
    lesson = StringField('Lesson', validators=[DataRequired()])
    lesson_number = IntegerField('Number of lesson', validators=[DataRequired()])
    # teacher_name = StringField('Teacher name', validators=[DataRequired()])
    homework = StringField('Homework', validators=[DataRequired()])
    notes = StringField('Notes', validators=[DataRequired()])
    submit = SubmitField('Submit')