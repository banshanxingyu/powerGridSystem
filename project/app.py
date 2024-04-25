# from project import create_app
from project.blueprint.auth import auth
from project.blueprint.historylogger import historyloggor
from project.blueprint.page_jump import page_jump
# , truncate
from flask import Flask
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)

# 数据库配置信息
HOSTNAME = 'localhost'
PORT = 3306
DATABASE = 'powerGridSystem'
USERNAME = 'root'
PASSWORD = 'Shjswj.999'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD,HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)

# 邮箱相关配置，如果需要如果不改变发送邮箱的话，这里不用改
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] =  587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '2840371551@qq.com'
app.config['MAIL_PASSWORD'] = 'nswcicqnfdsudfba'
MAIL_DEFAULT_SENDER = '2840371551@qq.com'
mail = Mail(app)


mail.init_app(app)
# db.init_app(app)


# app.add_template_filter(truncate, 'truncate')#

app.register_blueprint(auth)
app.register_blueprint(historyloggor)
app.register_blueprint(page_jump)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100))
#
# # 确保在应用上下文中执行数据库操作
# with app.app_context():
#     db.create_all()  # 创建数据库表
#     new_user = User(name="Alice")
#     db.session.add(new_user)
#     db.session.commit()

# @app.route('/import-csv')
# def import_csv():
#     # 读取CSV文件
#     data = pd.read_csv('data/auth_info.csv')
#
#     # 将数据导入到数据库
#     for index, row in data.iterrows():
#         user = User(name=row['name'], email=row['email'])
#         db.session.add(user)
#     db.session.commit()
#
#     return "Data imported successfully!"

if __name__ == '__main__':
    app.run(debug=True)