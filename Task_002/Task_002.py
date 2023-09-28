# Создать страницу, на которой будет форма для ввода имени и электронной почты, 
# при отправке которой будет создан cookie-файл с данными пользователя, а также будет 
# произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён 
# cookie-файл с данными пользователя и произведено перенаправление на страницу ввода имени 
# и электронной почты.

from flask import Flask, redirect, request, render_template, flash, session, url_for

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '12345fffff'

@app.route('/')
def index():
    if 'name' in session and 'email' in session:
        return f'Привет, {session["name"]}, {session["email"]}'
    else:
        return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        if not name or not email:
            flash('Введите имя и электронную почту!', 'danger')
            return redirect(url_for('login'))

        session['name'] = name
        session['email'] = email

        # Установите срок действия cookie (например, на 30 дней)
        session.permanent = True

        flash('Вы вошли!', 'success')
        return redirect(url_for('main'))
    return render_template('form.html')

@app.route('/main/', methods=['GET', 'POST'])
def main():
    if 'name' in session and 'email' in session:
        context = {
            'name': session['name'],
            'email': session['email'],
        }
        return render_template('main.html', **context)
    else:
        return redirect(url_for('login'))

@app.route('/logout/', methods=['POST'])
def logout():
    # Удалите cookie-файлы с данными пользователя
    session.pop('name', None)
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
