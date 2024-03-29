import os
from functools import wraps
from flask import Flask, render_template, make_response, request, redirect, url_for, session
import sqlite3
import error_msgs
import re
import hashlib
import os
from dataclasses import dataclass
from datetime import timedelta
salt_for_hashing = 'dream_team'

app = Flask(__name__)
app.secret_key = hashlib.sha1('secret_key'.encode()).hexdigest()

#вермя жизни сессии
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=30)

@dataclass
class User:
    id: int
    f_name: str
    l_name: str
    m_name: str
    login: str
    password: str
    token: str
    avatar_path: str
    def to_dict(self):
        return {
            'id': self.id,
            'f_name': self.f_name,
            'l_name': self.l_name,
            'm_name': self.m_name,
            'login': self.login,
            'token': self.token,
            'avatar_path': self.avatar_path
        }
def hashing(login, password):
    return hashlib.sha1(f"{salt_for_hashing}:{login}:{password}".encode()).hexdigest()
def add_user(f_name, l_name, m_name, login, password):
    db = sqlite3.connect("database.db")
    sql = db.cursor()
    hash = hashing(login, password)
    sql.execute("""INSERT INTO users (f_name, l_name, m_name, login, password, token) VALUES (?, ?, ?, ?, ?, ?)""",
                (f_name, l_name, m_name, login, password, hash))
    db.commit()
    db.close()
    return hash
def find_users(*args, **kwargs):
    result = []
    db = sqlite3.connect("database.db")
    sql = db.cursor()
    if args and args[0] == 'all':
        answer = sql.execute("""SELECT * FROM users""").fetchall()
        if answer: result = [User(*item) for item in answer]
    else:
        try:
            string = ''
            for item in kwargs.items():
                string += f"{item[0]} = '{item[1]}', "
            string = string.strip()[:-1]
            answer = sql.execute(f"""SELECT * FROM users WHERE {string}""").fetchall()
            if answer: result = [User(*item) for item in answer]
        except:
            pass
    db.close()
    return result
def update_user(login, **kwargs):
    db = sqlite3.connect('database.db')
    sql = db.cursor()
    try:
        req = ''
        for i in kwargs.items():
            req += f"{i[0]} = {i[1]}, "
        req = req.strip()[:-1]
        req = f"""UPDATE users SET {req} WHERE login='{login}'"""
        sql.execute(req)
    except:
        pass
    db.commit()
    db.close()

def find_user_by_token(token):
    try:
        return find_users(token=token)[0]
    except:
        return None
def find_user_by_login(login):
    try:
        return find_users(login=login)[0]
    except:
        return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def not_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

nav_btn_count = 2
def set_active_btn(index):
    if not index: return ["false" for i in range(nav_btn_count)]
    arr = ["false" for i in range(nav_btn_count)]
    arr[index - 1] = 'true'
    return arr

@app.route('/', methods=['GET'])
@login_required
def home():
    user = find_user_by_token(session.get('token')).to_dict()
    return render_template("index.html", is_active=set_active_btn(1), user=user)
@app.route('/courses')
def courses():
    user = find_user_by_token(session.get('token')).to_dict()
    return render_template("courses.html", is_active=set_active_btn(2), user=user)

@app.route('/settings')
def settings():
    user = find_user_by_token(session.get('token')).to_dict()
    return render_template("settings.html", is_active=set_active_btn(0), user=user)

@app.route('/registration', methods=['GET', 'POST'])
@not_login
def registration():
    if request.method == 'POST':
        js = request.get_json(".")
        f_name = js.get('f_name').lower().capitalize().strip()
        l_name = js.get('l_name').lower().capitalize().strip()
        m_name = js.get('m_name').lower().capitalize().strip()
        login = js.get('login').strip()
        password = js.get('password')
        password2 = js.get('password2')

        if (find_users(login=login)):
            resp = make_response(error_msgs.msg_1, 400)
            return resp
        if (password != password2) or (len(password) < 8 or len(password) > 20) or not re.match(r'^[A-z]+|[А-я]+.{1,30}$', f_name) or not re.match(r'^[A-z]+|[А-я]+.{1,30}$', l_name) or not re.match(r"^(?=.*[A-z])(?=.*[0-9!@#$%^&*]).{8,20}$", password):
            resp = make_response(error_msgs.msg_2, 400)
            return resp
        session['token'] = add_user(f_name, l_name, m_name, login, password)
        return make_response("Success", 200)
    return render_template("registration.html")

@app.route('/login', methods=['GET', 'POST'])
@not_login
def login():
    if request.method == 'POST':
        js = request.get_json('.')
        login = js.get('login').strip()
        password = js.get('password')

        db_user = find_user_by_login(login)
        if (not db_user or db_user.password != password):
            return make_response(error_msgs.msg_3, 400)
        token = hashing(login, password)
        update_user(db_user.login, token=token)
        session['token'] = token
        return make_response("Success", 200)


    return render_template("login.html")

@app.route('/logout')
def logout():
    token = session.get('token')
    if not token: return redirect(url_for('login'))
    session.pop('token', None)
    update_user(find_user_by_token(token).login, token='')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

