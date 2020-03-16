from flask import Flask, redirect, render_template, abort, request
from data import db_session
from data.loginform import LoginForm, RegisterForm, JobsForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
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
    return render_template('addjob.html', title='Добавление работы', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.team_leader == 1)|(Jobs.team_leader == current_user.id)).first()
        if jobs:
            form.team_leader.data = jobs.team_leader
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.team_leader == 1) | (Jobs.team_leader == current_user.id)).first()
        if jobs:
            jobs.team_leader = form.team_leader.data
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob.html', title='Редактирование работы', form=form)


@app.route('/')
def index():
    session = db_session.create_session()
    job = session.query(Jobs).all()
    return render_template('index.html', job=job)

@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == id,
                                      (Jobs.team_leader == 1) | (Jobs.team_leader == current_user.id)).first()
    if jobs:
        session.delete(jobs)
        session.commit()
    else:
        abort(404)
    return redirect('/')

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


if __name__ == '__main__':
    main()