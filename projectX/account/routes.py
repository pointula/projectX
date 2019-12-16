from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from projectX import db
from projectX.models import User, Transaction, Earnings, Investment
from projectX.account.forms import WithdrawalForm, InvestForm, ReferalForm, TerminateForm
from babel.numbers import format_decimal, format_percent
from .utils import withdrawal_request, user_withdrawal_request

account = Blueprint('account', __name__)

@account.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    form = TerminateForm()
    from datetime import datetime
    user = User.query.all()
    available = Earnings.query.filter_by(user_id=current_user.id).all()
    investment_history = Investment.query.filter_by(user_id=current_user.id).all()
    total_investment = sum([object.investment for object in investment_history])
    total_available = sum([object.earned for object in available])

    if form.validate_on_submit():
        if total_investment == 0:
            flash('Nothing to terminate because you do not have an active investment', category='danger')
        else:
            flash('Sorry, You cannot terminate your investment until after 45days', 'danger')

    try:
        total_asset = total_available + total_investment + current_user.availableFunds + current_user.referalBonus
        earning=Earnings.query.filter_by(user_id=current_user.id)[-1]
        total_investment = format_decimal(total_investment, locale='en_US')
    except:
        earning = 0
    
    total_asset = format_decimal(total_asset, locale='en_US')
    totalAsset = format_decimal(current_user.availableFunds + current_user.referalBonus, locale='en_US')
    available_funds = format_decimal(total_available + current_user.availableFunds, locale='en_US')
    #investment = format_decimal(current_user.investment, locale='en_US')
    referal_bonus = format_decimal(current_user.referalBonus, locale='en_US')
    try:
        earnings = format_decimal(earning.earned, locale='en_US')
        percentage = format_percent(earning.percentage, locale='en_US', decimal_quantization=False)

        return render_template('dashboard.html', total_asset=total_asset, referal_bonus=referal_bonus, form=form,
        earnings=earnings, percentage=percentage, title=f'Dashboard - {current_user.username.title()}',
        user=user, totalAsset=totalAsset, available_funds=available_funds, total_investment=total_investment, int=int)
    except:
        earnings = format_decimal(earning, locale='en_US')
        return render_template('dashboard.html', total_asset=total_asset, referal_bonus=referal_bonus, 
        earnings=earnings, form=form, title=f'Dashboard - {current_user.username.title()}',
        user=user, totalAsset=totalAsset, available_funds=available_funds, total_investment=total_investment, int=int) 
    

@account.route('/dashboard/add_funds')
@login_required
def add_funds():
    transaction_history = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('add_funds.html', transaction_history=transaction_history, title=f'Pointula deposit')

@account.route('/assist')
def assist():
    user=User.query.all()
    return render_template('assist.html', user=user, Earnings=Earnings, sum=sum, int=int, str=str)

@account.route('/dashboard/fundswithdrawal', methods=['POST', 'GET'])
@login_required
def withdraw():
    transaction_history = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    form = WithdrawalForm()
    available = Earnings.query.filter_by(user_id=current_user.id).all()
    total_available = sum([object.earned for object in available])
    if form.validate_on_submit():
        if form.amount.data <= current_user.availableFunds + total_available:
            transaction = Transaction(user_id=current_user.id, amount=form.amount.data, 
            accountNumber=form.account_number.data, bankName=form.bank_name.data)
            current_user.availableFunds = current_user.availableFunds - form.amount.data
            db.session.add(transaction)
            db.session.commit()

            user_withdrawal_request(current_user.email, form.bank_name.data, form.amount.data, current_user.firstName, current_user.lastName)
            withdrawal_request(form.bank_name.data, form.amount.data, current_user.firstName, current_user.lastName)
            flash('Thank You! Your withdrawal request has been submitted for review', category='success')
            return redirect(url_for('account.dashboard'))
        else:
            flash('The amount you entered exceeds your available balance', category='danger')
    return render_template('withdraw.html', form=form, transaction_history=transaction_history, title=f'Pointula withdrawal')

@account.route('/dashboard/earnings')
@login_required
def earnings():
    earning = Earnings.query.filter_by(user_id=current_user.id).order_by(Earnings.date.desc()).all()
    return render_template('earnings.html', earning=earning, float=float, format_percent=format_percent, title=f'Your earnings')

@account.route("/dashboard/refer-someone", methods=['POST', 'GET'])
@login_required
def refer():
    form=ReferalForm()
    if form.validate_on_submit():
        if current_user.referalBonus > 0:
            current_user.availableFunds = current_user.availableFunds+current_user.referalBonus
            current_user.referalBonus = 0
            db.session.commit()
            flash('Referal funds have been successfully moved to your available balance', category='success')
            return redirect(url_for('account.dashboard'))
        else:
            flash('No money to move, refer someone now to get bonus', category='danger')
    return render_template('referral.html', form=form, title=f'Pointula referal')

@account.route("/dashboard/invest", methods=['GET', 'POST'])
@login_required
def invest():
    form = InvestForm()
    available = Earnings.query.filter_by(user_id=current_user.id).all()
    total_available = sum([object.earned for object in available])
    if form.validate_on_submit():
        if not form.amount.data < 20000:
            if form.amount.data <= current_user.availableFunds + total_available:
                if form.amount.data > current_user.availableFunds + total_available:
                    current_user.availableFunds = 0
                    investment = Investment(user_id = current_user.id, investment=form.amount.data)
                else:
                    investment = Investment(user_id = current_user.id, investment=form.amount.data)
                    current_user.availableFunds = current_user.availableFunds - form.amount.data
                db.session.add(investment)
                db.session.commit()
                flash('Your funds has been invested successfully', category='success')
                return redirect(url_for('account.dashboard'))
            else:
                flash('The amount you entered exceeds your available balance', category='danger')
        else:
                flash('Hmm, looks like you are trying to invest an amount less than ₦20,000.', category='danger')
    return render_template('invest.html', form=form, title=f'Pointula invest money')
