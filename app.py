from flask import Flask, render_template, redirect, request, flash, session, url_for, g, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3 as sql
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from UserLogin import UserLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OKDSFKJ4DEasnbiuoef-8943JK5T98I4P398F3'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 * 10

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для этой страницы требуется вход'
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sql.connect('urfube.db')
    conn.row_factory = sql.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route('/')
def index():
    return render_template('index.html', videos=dbase.getVideos())


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/profile')

    if request.method == 'POST':
        user = dbase.getUserByName(request.form['username'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get('next') or '/profile')
        else:
            flash('Не верный логин/пароль', 'invalid')

    return render_template('login.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect('/profile')

    if request.method == 'POST':
        if len(request.form['mail']) <= 4 or '.' not in request.form['mail'] or '@' not in request.form['mail']:
            flash('Почта введена некорректно!', 'invalid')
        elif request.form['password'] != request.form['password2']:
            flash('Пароли не совпадают!', 'invalid')
        elif len(request.form['password']) <= 6:
            flash('Пароль должен быть длиннее 6 символов!', 'invalid')
        elif len(request.form['username']) <= 3:
            flash('Логин должен быть длиннее 3 символов!', 'invalid')
        else:
            pas = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['username'], request.form['mail'], pas)
            if res:
                flash('Успешная регистрация!', 'success')
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавлении в БД', 'invalid')

    return render_template('registration.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из профиля', 'success')
    return redirect('/login')


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    return render_template('upload.html')


@app.route('/uploadvideo', methods=['POST', 'GET'])
@login_required
def uploadvideo():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyFormat(file.filename):
            try:
                vid = file.read()
                res = dbase.addVideo(request.form['title'], request.form['description'], current_user.getName(), vid)
                if not res:
                    flash('Ошибка', 'invalid')
            except FileNotFoundError as e:
                flash('Ошибка чтения файла', 'invalid')
        else:
            flash('Ошибка добавления видео', 'invalid')

    return redirect(url_for('profile'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', videos=dbase.getVideosByUser(current_user.getName()))


@app.route('/usevideo')
def usevideo():
    vid = dbase.getThatVideo("q3e5Ask1GzXndyOr")
    vid = vid['video']

    h = make_response(vid)
    h.headers['Content-Type'] = 'video/mp4'
    return h


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ''

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/uploadava', methods=['POST', 'GET'])
@login_required
def uploadava():
    if request.method == "POST":
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash('Ошибка обновления аватара', 'invalid')

                flash('Аватар обновлен', 'success')
            except FileNotFoundError as e:
                flash('Ошибка чтения файла', 'invalid')
        else:
            flash('Ошибка обновления аватара', 'invalid')

    return redirect(url_for('profile'))


@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    whats = ''
    videos = ''
    if request.method == 'POST':
        whats = request.form['search']

        videos = dbase.getVideosBySearch(request.form['search'])
        if not videos:
            videos = 'Видео не найдено'

    return render_template('search.html', videos=videos, whats=whats)


@app.route('/video/<video_id>')
def video(video_id):
    return render_template('video.html', video=dbase.getThatVideo(video_id))


@app.route('/normunik')
@login_required
def xd():
    return render_template('xd.html')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html'), 404


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run(debug=True)
