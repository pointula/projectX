from projectX import db, admin, app
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    availableFunds = db.Column(db.Integer, default=0)
    phoneNumber = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    referalBonus = db.Column(db.Integer, default = 0)
    referal_code = db.Column(db.String(20), unique=True, nullable=False)
    referer_username = db.Column(db.String(15))
    password = db.Column(db.String(100), nullable=False)
    transactions = db.relationship('Transaction', backref='transactions', lazy='dynamic')
    earnings = db.relationship('Earnings', backref='earning', lazy='dynamic')
    investment = db.relationship('Investment', backref='investments', lazy='dynamic')

    def __str__(self):
        return f'User {self.username}'

    def get_reset_token(self):
        s = Serializer(app.secret_key, expires_in=59)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    investment = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    amount = db.Column(db.String(30), nullable=False)
    accountNumber=db.Column(db.String(30), nullable=False)
    bankName = db.Column(db.String(30), nullable=False)

    def __str__(self):
        return f'Transaction {self.id}'

class Earnings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    percentage = db.Column(db.String(5), default='0')
    earned = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)