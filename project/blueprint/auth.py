import csv
import os
from flask import Blueprint, render_template, redirect, request, jsonify, url_for, session, current_app, flash, render_template_string
from flask_mail import Message

from itsdangerous import json

import random
import string


auth = Blueprint('auth', __name__)

# 登录的后端逻辑
@auth.route('/')
def root():
    return redirect(url_for('.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Email: {email}, Password: {password}")

        # 添加登录验证逻辑
        if validate_login(email, password):
            return redirect(url_for('auth.login_success'))
        else:
            flash('邮箱或密码错误，请重试。')  # 显示错误消息
            return render_template('login.html')

    return render_template('login.html')

def validate_login(email, password):
    file_path = 'data/auth_info.csv'
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == email and row[1] == password:
                    return True
    except FileNotFoundError:
        return False
    return False

@auth.route('/login_success')
def login_success():
    return render_template('home2.html')








# 注册的后端逻辑
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_input_code = request.form['verification_code']

        # 验证验证码是否正确
        if session.get('verification_code') != user_input_code:
            return jsonify({"error": "验证码错误，请重新输入！"}), 400

        # 检查邮箱是否已注册
        if email_exists(email):
            return jsonify({"error": "该邮箱已被注册。"}), 409

        # 保存用户信息
        save_user(email, password)
        return jsonify({"message": "注册成功！请登录。", "redirect": url_for('auth.registration_success')}), 200

    return render_template('register.html')

def email_exists(email):
    file_path = 'data/auth_info.csv'
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == email:
                    return True
    except FileNotFoundError:
        return False
    return False

@auth.route('/registration_success')
def registration_success():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>注册成功</title>
        <style>
            .message-box {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 300px;
                padding: 20px;
                background-color: #f8f9fa;
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
        </style>
        <script type="text/javascript">
            setTimeout(function() {
                window.location.href = "{{ url_for('auth.login') }}";
            }, 2000); // 3秒后跳转到登录页面
        </script>
    </head>
    <body>
        <div class="message-box">
            <p>注册成功！即将跳转到登录页面。</p>
        </div>
    </body>
    </html>
    ''')
def save_user(email, password):
    file_path = 'data/auth_info.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([email, password])


@auth.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    data = request.get_json()
    email = data['email']
    verification_code = generate_verification_code()

    mail = current_app.extensions['mail']
    msg = Message('验证信息', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'您的验证码是 {verification_code}.'
    mail.send(msg)

    session['verification_code'] = verification_code  # 保存验证码到 session
    return jsonify({"message": "验证码发送成功"})


def generate_verification_code():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))


#这个是核心界面
@auth.route('/history', methods=['GET', 'POST'])
def history():
    return render_template('history.html')  # **data





# def create_app():
#     app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
#     app.secret_key = 'OHsoiiohsadoihoisadhfoi'
#
#     @app.route('/home')
#     def home():
#         return render_template('home.html')
#
#     @app.route('/')
#     def login():
#         return render_template('login.html')
#
#     @app.route('/analyse')
#     def analyse():
#         return render_template('analyse.html')
#
#     @app.route('/history', methods=['GET', 'POST'])
#     def history():
#         data = {'title': ''}
#         error = ''
#         res = ''
#         if request.method == 'POST':
#             # print(111)
#             data = dict(request.form)
#             res = data['title']
#             res = 2 * int(res)
#
#         # print(data)
#         return render_template('history.html', res=res)  # **data
#
#     @app.route('/view')
#     def view():
#         return render_template('view.html')
#
#     return app