from flask import Flask, redirect, render_template
from data import db_session
from data.loginform import LoginForm, RegisterForm, JobsForm
from flask_login import LoginManager, login_user, logout_user, login_required
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = JobsForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        if session:
            job = Jobs(team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
            )
            session.add(job)
            session.commit()
            return redirect("/")
        return redirect('/logout')
    return render_template('addjob.html', title='44', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/')
def index():
    session = db_session.create_session()
    job = session.query(Jobs).all()
    return render_template('index.html', job=job)


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
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/success')
def success():
    return render_template('success.html', title='Отправлено')


def main():
    db_session.global_init("db/blogs.sqlite")
    app.run()

    # session = db_session.create_session()
    #
    # user = User()
    # user.surname = "Scott"
    # user.name = "Ridley"
    # user.age = 21
    # user.position = "captain"
    # user.speciality = "research engineer"
    # user.address = "module_1"
    # user.email = "scott_chief@mars.org"
    # user.hashed_password = "cap"
    # session.add(user)
    #
    # user2 = User()
    # user2.surname = "Alan"
    # user2.name = "Lay"
    # user2.age = 32
    # user2.position = "pilot"
    # user2.speciality = "main pilot"
    # user2.address = "module_2"
    # user2.email = "alan_pilot@mars.org"
    # user2.hashed_password = "tolip"
    # session.add(user2)
    #
    # user3 = User()
    # user3.surname = "Mark"
    # user3.name = "Toy"
    # user3.age = 27
    # user3.position = "student"
    # user3.speciality = "enjineer"
    # user3.address = "module_3"
    # user3.email = "student_mark@mars.org"
    # user3.hashed_password = "stu_dent"
    # session.add(user3)
    #
    # user4 = User()
    # user4.surname = "John"
    # user4.name = "Porter"
    # user4.age = 28
    # user4.position = "doctor"
    # user4.speciality = "main doctor"
    # user4.address = "module_7"
    # user4.email = "john_d@mars.org"
    # user4.hashed_password = "doc_porter"
    # session.add(user4)
    # session.commit()
    #
    # job = Jobs()
    # job.team_leader = 1
    # job.job = 'deployment of residential modules 1 and 2'
    # job.work_size = 15
    # job.collaborators = '2, 3'
    # job.is_finished = False
    # session.add(job)
    # session.commit()


if __name__ == '__main__':
    main()
