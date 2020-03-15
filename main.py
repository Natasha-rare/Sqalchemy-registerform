from flask import Flask, redirect, render_template
from data import db_session
from data.loginform import TimeTableForm, LoginForm, RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required
from data.teachers import Teacher
from data.timetable import TimeTable
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(teacher):
    session = db_session.create_session()
    return session.query(Teacher).get(teacher)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global captain
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            captain = user.id
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addtimetable', methods=['GET', 'POST'])
def addtimetable():
    form = TimeTableForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        if session:
            timetable = TimeTable(day=form.day.data,
            lesson=form.lesson.data,
            lesson_number=form.lesson_number.data,
            homework=form.homework.data,
            notes=form.notes.data
            )
            session.add(timetable)
            session.commit()
            return redirect("/")
        return redirect('/logout')
    return render_template('addtimetable.html', h='Добавление работы', title='44', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/')
def index():
    session = db_session.create_session()
    timetable = session.query(TimeTable).all()
    return render_template('index.html', timetable=timetable)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            class1=form.class1.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/success')
def success():
    return render_template('success.html', title='Отправлено')


@app.route('/change')
def change():
    form = TimeTableForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        if session:
            timetable = TimeTable(id=form.id.data,
                                  day=form.day.data,
                                  lesson=form.lesson.data,
                                  lesson_number=form.lesson_number.data,
                                  homework=form.homework.data,
                                  notes=form.notes.data
                                  )
            session.commit()
            return redirect("/")
        else:
            return redirect('/logout')
    return render_template('addjob.html', title='44', h='Изменение работы', form=form)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.run()


if __name__ == '__main__':
    main()
