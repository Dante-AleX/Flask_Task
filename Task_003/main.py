# Создать форму для регистрации пользователей на сайте. Форма должна содержать поля: 
# "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
# При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.


from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)

app.config['SECRET_KEY'] = b'7f520ea781d96a929e16407fd380392cb06f1d4c2c294fab'

csrf = CSRFProtect(app)


@app.route('/')
def index():
    return 'Hi! This is the main page.'


@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
        print('Database initialized')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (username, password) in db():
            return "Вы вошли "
        return f'неправильный {escape(username)} логин или пароль'
    return render_template('login.html') 


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter((User.name == name) | (User.email == email)).first()

        if existing_user:
            error_msg = 'Username or email already exists.'
            form.name.errors.append(error_msg)
            return render_template('register.html', form=form)

        user = User(name=name, email=email, password=password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return 'Registered success!'
    return render_template('register.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
