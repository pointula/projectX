from flask import Blueprint, render_template, url_for, flash, redirect, request
from projectX import db, login_manager
from flask_login import current_user, login_required, login_user, logout_user
from projectX.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from projectX.users.forms import (LoginForm, RegistrationForm, ResetPasswordForm, RequestResetForm,
                                RefererForm, PhoneNumberForm, ChangePasswordForm)
from secrets import token_hex
from .utils import send_reset_email, sign_up_message


users = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route('/signin', methods=['GET','POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('account.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Successfully Logged in as {form.username.data}', category='success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('account.dashboard'))
        else:
            flash('Unable to login, Either Your username or password is incorrect', category='danger')
    return render_template('signin.html', form=form, title='Pointula user signin')

@users.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('account.dashboard'))
    form = RegistrationForm()
    referal_code=token_hex(8)
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data)
        user = User(username=form.username.data, firstName=form.firstname.data,
        lastName=form.lastname.data,
        referal_code=referal_code,
        email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        user_login = User.query.filter_by(username = form.username.data).first()
        login_user(user_login)
        sign_up_message(form.email.data, form.username.data, referal_code)
        return redirect(url_for('users.confirm_referrer'))
    return render_template('signup.html', form=form, title='Pointula user signin')

@users.route('/signup/confirm-referer', methods=['GET','POST'])
@login_required
def confirm_referrer():
    form = RefererForm()
    if form.validate_on_submit():
        current_user.referer_username = form.referer_username.data
        db.session.commit()
        return redirect(url_for('users.confirm_number'))
    return render_template('confirm_referrer.html', form=form, title='Pointula confirm referal')

@users.route('/signup/add-phone-number', methods=['GET','POST'])
def confirm_number():
    form = PhoneNumberForm()
    if form.validate_on_submit():
        current_user.phoneNumber = form.phoneNumber.data
        db.session.commit()
        flash(f'Account Created Successfully for {current_user.username}', category='success')
        return redirect(url_for('account.dashboard'))
    return render_template('confirm_number.html', form=form, title='Pointula confirm phone number')

@users.route('/update-profile', methods = ['GET','POST'])
@login_required
def profile():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Password Changed Successfully', category='success')
        return redirect(url_for('users.profile'))
    return render_template('profile.html', form=form, title='Pointula user settings')

@users.route('/account-forget-password')
def forget_password():
    return render_template('profile.html', title='Forget password')

#mail--------------------------------------#
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.logout'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Confirmation email sent', category='success')
        return redirect(url_for('users.reset_request'))
    return render_template('reset_request.html', form=form, title='Pointula password reset request')


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.logout'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', category='danger')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash(f'Your Password has been updated successfully! Please Login.', category='success')
        return redirect(url_for('users.signin'))
    return render_template('reset_token.html', form=form, title='Pointula reset password')
