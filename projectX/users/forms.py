from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, Length
from projectX.models import User
from werkzeug.security import check_password_hash
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(5,20), Regexp('^[A-Za-z0-9_]{3,}$',
                message='Username can only contain letters, numbers and underscore')])
    firstname = StringField('First Name', validators=[DataRequired(), Length(5,20), Regexp('^[A-Za-z]{3,}$',
                message='Name can only contain letters')])
    lastname = StringField('Last Name', validators=[DataRequired(), Regexp('^[A-Za-z]{3,}$',
                message='Name can only contain letters')])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), 
                EqualTo('confirm_password', message='Password must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    terms_and_condition = BooleanField(validators=[DataRequired()])

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValueError('This Username has been taken')

    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValueError('This Email has been taken')
    
class RefererForm(FlaskForm):
    referer_username = StringField('Referer Code')

class PhoneNumberForm(FlaskForm):
    phoneNumber = IntegerField('Phone number')
    
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('Password', validators=[DataRequired(), 
                EqualTo('confirm_new_password', message='New password must match')])
    confirm_new_password = PasswordField('Confirm Password', validators=[DataRequired()])

    def validate_current_password(self, current_password):
        password = check_password_hash(current_user.password, current_password.data)
        if not password:
            raise ValueError('Old Password does not match our record. Note that password might be case sensitive')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), 
                EqualTo('confirm_password', message='New password must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])

class RequestResetForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])

    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if not email:
            raise ValueError('This Email Does not exist')