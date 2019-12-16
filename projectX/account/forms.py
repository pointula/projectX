from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class WithdrawalForm(FlaskForm):
    banks = [
        ('first_bank','First Bank'),
        ('gtbank', 'Guarantee Trust Bank'),
        ('wema_bank', 'Wema Bank'),
        ('zenith_bank', 'Zenith Bank'),
    ]
    amount = IntegerField('Amount', validators=[DataRequired()])
    account_number = StringField('Account Number')
    bank_name = SelectField(u'Bank Name', choices=banks, validators=[DataRequired()])

class InvestForm(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()])
    terms_and_condition = BooleanField(validators=[DataRequired()])

class ReferalForm(FlaskForm):
    submit=SubmitField('Move money')

class TerminateForm(FlaskForm):
    submit=SubmitField('Terminate')