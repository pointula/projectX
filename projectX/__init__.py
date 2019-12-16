from flask import Flask, session
from flask_admin import Admin, BaseView, expose
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqlamodel import ModelView
from flask_login import LoginManager
from flask_mail import Mail
import os

import sys
'''
sys.path.extend(['', 'C:\\Users\\HP\\Desktop\\flask_venv', 'C:\\Users\\HP\\Desktop\\flask_venv\\lib\\site-packages'])
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = '9036d1718a623ecf0667e8f15dbe9b8286e79f7247322d958a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:tokelee@localhost:3306/projectx'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

#mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = 'wpfwklcnrxatsegl' #os.environ.get('MAIL_PASSWORD')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
admin = Admin(app, name='ProjectX', url='/admin_test')
mail = Mail(app)

#login configs
login_manager.login_message = 'Hmm, Please login to access this page'
login_manager.session_protection = 'strong'
login_manager.login_message_category = 'danger'
login_manager.login_view = 'users.signin'

from .models import User, Transaction, Earnings, Investment


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

admin.add_view(MyView(name='Hello'))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Transaction, db.session))
admin.add_view(ModelView(Earnings, db.session))
admin.add_view(ModelView(Investment, db.session))


from projectX.main.routes import main
from projectX.account.routes import account
from projectX.users.routes import users
from projectX.errors.handlers import errors

app.register_blueprint(main)
app.register_blueprint(account)
app.register_blueprint(users)
app.register_blueprint(errors)